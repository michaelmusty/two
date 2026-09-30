"""Small ctypes interface to compiled FLINT Cauchy actions.

Only normalized residuals and approximate corrections cross the double
interface. Geometry, residual arithmetic, and accumulated iterates stay in
FLINT. Ball radii describe arithmetic on supplied data, not geometry errors.
"""
import ctypes as ct
from concurrent.futures import ThreadPoolExecutor
import hashlib
import math
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
METHODS = {'horner': 0, 'rectangular': 1}


def build():
    """Build a source/flags/version-addressed library; never install packages."""
    source = HERE / 'cm_acb.c'
    flags = shlex.split(subprocess.check_output(
        ['pkg-config', '--cflags', '--libs', 'flint'], text=True))
    version = subprocess.check_output(['pkg-config', '--modversion', 'flint'], text=True).strip()
    compiler = shlex.split(os.environ.get('CC', 'cc'))
    identity = source.read_bytes() + repr((compiler, flags, version)).encode()
    digest = hashlib.sha256(identity).hexdigest()[:20]
    directory = HERE / '.build'
    directory.mkdir(exist_ok=True)
    library = directory / f'cm_acb_{digest}.so'
    if not library.exists():
        fd, temporary = tempfile.mkstemp(prefix='cm_acb_', suffix='.so', dir=directory)
        os.close(fd)
        try:
            subprocess.run([*compiler, '-std=c11', '-O3', '-Wall', '-Wextra', '-Werror',
                            '-fPIC', '-shared', str(source), '-o', temporary, *flags], check=True)
            os.replace(temporary, library)
        finally:
            Path(temporary).unlink(missing_ok=True)
    return library


class Backend:
    def __init__(self, digits=50, guard_bits=40):
        if digits < 20 or guard_bits < 0:
            raise ValueError('require at least 20 decimal digits and nonnegative guard bits')
        self.digits = digits
        self.bits = math.ceil(digits * math.log2(10)) + guard_bits
        self.serialization_digits = math.ceil(self.bits * math.log10(2)) + 10
        self.source_sha256 = hashlib.sha256((HERE/'cm_acb.c').read_bytes()).hexdigest()
        self.path = build()
        self.lib = ct.CDLL(str(self.path))
        pointer, integer, scalar, string = ct.c_void_p, ct.c_long, ct.c_int, ct.c_char_p
        doubles, longs = ct.POINTER(ct.c_double), ct.POINTER(ct.c_long)
        signatures = {
            'cm_version': (string, []), 'cm_free': (None, [pointer]),
            'cm_vec_new': (pointer, [integer]), 'cm_vec_free': (None, [pointer]),
            'cm_vec_set_str': (scalar, [pointer, integer, string, string, integer]),
            'cm_vec_set_double': (scalar, [pointer, doubles]),
            'cm_vec_component': (pointer, [pointer, integer, scalar, integer]),
            'cm_vec_bound': (pointer, [pointer, integer, integer, scalar, integer, integer]),
            'cm_vec_scaled_doubles': (scalar, [pointer, integer, integer, doubles, longs]),
            'cm_vec_add_correction': (scalar, [pointer, integer, integer, doubles, longs, integer]),
            'cm_vec_write': (scalar, [pointer, string]),
            'cm_vec_read': (pointer, [string, integer]),
            'cm_op_new': (pointer, [integer, pointer, pointer, string, integer]),
            'cm_op_free': (None, [pointer]),
            'cm_op_apply': (scalar, [pointer, pointer, pointer, integer, integer, integer, scalar]),
            'cm_evaluate': (scalar, [pointer, pointer, integer, integer, pointer, integer, scalar]),
            'cm_stabilized_residual': (scalar, [pointer, pointer, pointer, integer, integer, integer, integer]),
            'cm_vec_sub': (scalar, [pointer, pointer, pointer, integer]),
            'cm_weighted_sub': (scalar, [pointer, pointer, pointer, pointer, integer, integer]),
        }
        for name, (result, arguments) in signatures.items():
            fn = getattr(self.lib, name)
            fn.restype, fn.argtypes = result, arguments
        self.version = self.lib.cm_version().decode()

    def string(self, pointer):
        if not pointer:
            raise RuntimeError('invalid native string result')
        try:
            return ct.string_at(pointer).decode()
        finally:
            self.lib.cm_free(pointer)

    def vector(self, values, *, doubles=False):
        data = np.asarray(values, dtype=np.complex128 if doubles else object)
        if data.ndim == 1:
            data = data[:, None]
        if data.ndim != 2:
            raise ValueError('expected a vector or matrix')
        result = Vector(self, *data.shape)
        if doubles:
            flat = np.ascontiguousarray(data.T, dtype=np.complex128).ravel()
            check(self.lib.cm_vec_set_double(result.ptr, double_pointer(flat)))
        else:
            for i, value in enumerate(data.T.ravel()):
                z = mp.mpc(value)
                re = mp.nstr(z.real, self.serialization_digits).encode()
                im = mp.nstr(z.imag, self.serialization_digits).encode()
                check(self.lib.cm_vec_set_str(result.ptr, i, re, im, self.bits))
        return result

    def read(self, path, rows, columns):
        pointer = self.lib.cm_vec_read(os.fsencode(path), rows*columns)
        if not pointer:
            raise ValueError(f'cannot read native vector: {path}')
        return Vector(self, rows, columns, pointer=pointer)


def check(ok):
    if not ok:
        raise ArithmeticError('native action failed or produced nonfinite data')


def double_pointer(array):
    return array.ctypes.data_as(ct.POINTER(ct.c_double))


class Vector:
    def __init__(self, backend, rows, columns=1, *, pointer=None):
        if rows <= 0 or columns <= 0:
            raise ValueError('vector dimensions must be positive')
        self.backend, self.rows, self.columns = backend, rows, columns
        self.ptr = pointer or backend.lib.cm_vec_new(rows*columns)
        if not self.ptr:
            raise MemoryError('cannot allocate native vector')

    def __del__(self):
        if getattr(self, 'ptr', None):
            self.backend.lib.cm_vec_free(self.ptr)
            self.ptr = None

    def component(self, row, column=0, part=0):
        if not 0 <= row < self.rows or not 0 <= column < self.columns:
            raise IndexError('vector index outside shape')
        return self.backend.string(self.backend.lib.cm_vec_component(
            self.ptr, column*self.rows+row, part, self.backend.serialization_digits))

    def to_mpmath(self, rows=None):
        rows = self.rows if rows is None else min(rows, self.rows)
        return mp.matrix([[mp.mpc(self.component(i, j, 0), self.component(i, j, 1))
                           for j in range(self.columns)] for i in range(rows)])

    def bounds(self, mode=2):
        b = self.backend
        return [mp.mpf(b.string(b.lib.cm_vec_bound(
            self.ptr, c*self.rows, self.rows, mode, b.bits, b.serialization_digits)))
            for c in range(self.columns)]

    def scaled_doubles(self):
        flat = np.empty(self.rows*self.columns, dtype=np.complex128)
        exponents = np.empty(self.columns, dtype=ct.c_long)
        check(self.backend.lib.cm_vec_scaled_doubles(self.ptr, self.rows, self.columns,
              double_pointer(flat), exponents.ctypes.data_as(ct.POINTER(ct.c_long))))
        return flat.reshape(self.columns, self.rows).T, exponents

    def add_correction(self, correction, exponents):
        correction = np.asarray(correction)
        if correction.shape != (self.rows, self.columns) or len(exponents) != self.columns:
            raise ValueError('correction shape mismatch')
        flat = np.ascontiguousarray(correction.T, dtype=np.complex128).ravel()
        exponents = np.ascontiguousarray(exponents, dtype=ct.c_long)
        check(self.backend.lib.cm_vec_add_correction(self.ptr, self.rows, self.columns,
              double_pointer(flat), exponents.ctypes.data_as(ct.POINTER(ct.c_long)), self.backend.bits))

    def subtract(self, other):
        self.require_shape(other)
        result = Vector(self.backend, self.rows, self.columns)
        check(self.backend.lib.cm_vec_sub(result.ptr, self.ptr, other.ptr, self.backend.bits))
        return result

    def require_shape(self, other):
        if (self.rows, self.columns) != (other.rows, other.columns) or self.backend is not other.backend:
            raise ValueError('incompatible native vectors')

    def write(self, path):
        check(self.backend.lib.cm_vec_write(self.ptr, os.fsencode(path)))


class CauchyOperator:
    def __init__(self, backend, n, nodes, weights, offset='0.37', method='rectangular', threads=1):
        nodes.require_shape(weights)
        if nodes.backend is not backend or nodes.columns != 1 or n > nodes.rows or not 1 <= threads <= 16:
            raise ValueError('invalid Cauchy nodes')
        self.backend, self.n, self.count = backend, n, nodes.rows
        self.method = METHODS[method]
        self.plans = []
        self.pool = None
        for _ in range(threads):
            pointer = backend.lib.cm_op_new(n, nodes.ptr, weights.ptr, str(offset).encode(), backend.bits)
            if not pointer:
                raise ValueError('invalid native Cauchy plan')
            self.plans.append(pointer)
        if threads > 1:
            self.pool = ThreadPoolExecutor(max_workers=threads)

    def __del__(self):
        self.close()

    def close(self):
        if getattr(self, 'pool', None):
            self.pool.shutdown(wait=True)
            self.pool = None
        for pointer in getattr(self, 'plans', []):
            self.backend.lib.cm_op_free(pointer)
        self.plans = []

    def _apply_columns(self, index, result, coefficients, first, stop):
        # Every worker owns its nodes, FFT plan, and scratch arrays. Only
        # immutable input data and disjoint output columns are shared.
        check(self.backend.lib.cm_op_apply(self.plans[index], result.ptr, coefficients.ptr,
              coefficients.columns, first, stop, self.method))

    def apply(self, coefficients):
        if coefficients.rows != self.n or coefficients.backend is not self.backend:
            raise ValueError('coefficient shape/backend mismatch')
        if not self.plans:
            raise RuntimeError('Cauchy operator is closed')
        result = Vector(self.backend, self.n, coefficients.columns)
        workers = min(len(self.plans), coefficients.columns)
        if workers == 1:
            self._apply_columns(0, result, coefficients, 0, coefficients.columns)
        else:
            futures = [self.pool.submit(self._apply_columns, index, result, coefficients,
                       index*coefficients.columns//workers, (index+1)*coefficients.columns//workers)
                       for index in range(workers)]
            for future in futures:
                future.result()
        return result

    def residual(self, x, basis, *, return_defect=False):
        if basis.rows != self.n or basis.backend is not self.backend or x.columns > basis.columns:
            raise ValueError('stabilizing basis shape/backend mismatch')
        result = self.apply(x)
        defect = x.subtract(result) if return_defect else None
        check(self.backend.lib.cm_stabilized_residual(result.ptr, x.ptr, basis.ptr,
              self.n, x.columns, basis.columns, self.backend.bits))
        return (result, defect) if return_defect else result


def evaluate(coefficients, nodes, method='rectangular'):
    if nodes.columns != 1 or nodes.backend is not coefficients.backend:
        raise ValueError('incompatible evaluation nodes')
    b = coefficients.backend
    result = Vector(b, nodes.rows, coefficients.columns)
    check(b.lib.cm_evaluate(result.ptr, coefficients.ptr, coefficients.rows,
          coefficients.columns, nodes.ptr, b.bits, METHODS[method]))
    return result


def weighted_difference(left, right, weights):
    left.require_shape(right)
    if weights.rows != left.rows or weights.columns != 1 or weights.backend is not left.backend:
        raise ValueError('weight shape/backend mismatch')
    b = left.backend
    result = Vector(b, left.rows, left.columns)
    check(b.lib.cm_weighted_sub(result.ptr, left.ptr, right.ptr, weights.ptr, left.columns, b.bits))
    return result
