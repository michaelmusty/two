"""Reuse the local Belyi Cauchy/Arnoldi engine on the genus-64 level cover.

The cover has a positive-genus base and is not presented as a Belyi map.
Only the input geometry and old/new projections are new. Numerical pilot
nodes are double precision; native arithmetic does not certify geometry.
"""
import argparse
from dataclasses import dataclass
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import time

import numpy as np
from scipy.linalg import lu_factor, lu_solve, qr
from scipy.sparse.linalg import LinearOperator, eigs

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data/computed'
spec = importlib.util.spec_from_file_location('cm_scalar', HERE/'68_cm_differentials.py')
scalar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scalar)


class Geometry:
    def __init__(self, path=DATA/'cover_geometry.json'):
        self.path = Path(path)
        raw = json.loads(self.path.read_text())
        pairs = np.asarray(raw['cm_actions'])
        ab = pairs[..., 0] + 1j*pairs[..., 1]
        self.elliptic = np.asarray(raw['elliptic_image'], dtype=int)-1
        assert sorted(self.elliptic) == [0, 1, 2]
        assert np.array_equal(self.elliptic[self.elliptic], np.arange(3))
        fixed = np.flatnonzero(self.elliptic == np.arange(3))
        assert len(fixed) == 1
        self.fixed = int(fixed[0])
        self.moving = min(i for i in range(3) if i != self.fixed)
        self.partner = int(self.elliptic[self.moving])
        mask = np.abs(ab[:, 1]) > 1e-10
        self.images = np.asarray(raw['side_images'], dtype=int)[mask]-1
        a, b = ab[mask].T
        self.actions = (-b/a, a/a.conjugate(), 1/np.abs(a)**2)
        self.zeta = np.exp(2j*np.pi/32)
        self.sha256 = hashlib.sha256(self.path.read_bytes()).hexdigest()

    def reduce(self, points, initial_sheet):
        words = [[] for _ in points]
        v, derivative, steps, error = scalar.reduce_points(points, self.actions, words=words)
        sheets = np.full(len(v), initial_sheet, dtype=int)
        for i, word in enumerate(words):
            for generator, turn in word:
                if turn % 2:
                    sheets[i] = self.elliptic[sheets[i]]
                sheets[i] = self.images[generator, sheets[i]]
        return v, derivative, sheets, steps, error


def embed_new(v):
    n = len(v)//2
    out = np.empty((3*n,)+v.shape[1:], dtype=complex)
    out[:n] = -2*v[:n]
    out[n::2] = v[n:]
    out[n+1::2] = v[:n]
    return out


def project_new(v):
    n = len(v)//3
    return np.concatenate(((v[n+1::2]-v[:n])/3, v[n::2]), axis=0)


def embed_old(v):
    n = len(v)
    out = np.zeros((3*n,)+v.shape[1:], dtype=complex)
    out[:n] = v
    out[n+1::2] = v
    return out


@dataclass
class Problem:
    n: int
    count: int
    nodes: np.ndarray
    weights: np.ndarray
    centers: np.ndarray
    offset: float
    stats: dict

    def apply(self, coefficients):
        vector = coefficients.ndim == 1
        if vector:
            coefficients = coefficients[:, None]
        assert coefficients.shape[0] == 3*self.n
        values = np.empty((2*self.count, coefficients.shape[1]), dtype=complex)
        for center, block in enumerate((coefficients[:self.n], coefficients[self.n:])):
            select = self.centers == center
            values[select] = np.polynomial.polynomial.polyval(self.nodes[select], block).T
        values *= self.weights[:, None]
        parts = []
        for center, length in enumerate((self.n, 2*self.n)):
            transform = np.fft.fft(values[center*self.count:(center+1)*self.count], axis=0)
            phase = np.exp(-2j*np.pi*np.arange(length)*self.offset/self.count)/self.count
            parts.append(transform[:length]*phase[:, None])
        out = np.concatenate(parts, axis=0)
        return out[:, 0] if vector else out

    def apply_new(self, coefficients):
        return project_new(self.apply(embed_new(coefficients)))

    def dense_new(self):
        # Each input monomial is evaluated once. Applying Horner to many
        # mostly-zero basis vectors would add an unnecessary factor of n.
        matrix = np.empty((2*self.n, 2*self.n), dtype=complex)
        powers = np.where(self.centers == 0, self.nodes, self.nodes**2)
        rowphase = np.exp(-2j*np.pi*np.arange(2*self.n)*self.offset/self.count)/self.count
        for sector in (0, 1):
            factor = (np.where(self.centers == 0, -2, self.nodes) if sector == 0
                      else (self.centers == 1).astype(complex))
            for start in range(0, self.n, 64):
                stop = min(start+64, self.n)
                values = np.vander(powers, N=stop-start, increasing=True)
                values *= (self.weights*factor*powers**start)[:, None]
                f0 = np.fft.fft(values[:self.count], axis=0)[:self.n]*rowphase[:self.n, None]
                f1 = np.fft.fft(values[self.count:], axis=0)[:2*self.n]*rowphase[:, None]
                matrix[:, sector*self.n+start:sector*self.n+stop] = np.concatenate(
                    ((f1[1::2]-f0)/3, f1[::2]), axis=0)
        return matrix


def make_problem(geometry, n, radius=0.99991, oversample=2, offset=0):
    if n < 1 or oversample < 1 or not 0 < radius < 1:
        raise ValueError('invalid truncation, oversampling or radius')
    count = 2*n*oversample
    nodes, weights, centers, errors, maxsteps = [], [], [], [], []
    theta = 2*np.pi*(np.arange(count)+offset)/count
    for exponent, sheet in ((32, geometry.fixed), (16, geometry.moving)):
        w = radius*np.exp(1j*theta/exponent)
        v, derivative, target, steps, error = geometry.reduce(w, sheet)
        fold = np.where(target == geometry.partner, geometry.zeta, 1)
        vf = fold*v/radius
        center = (target != geometry.fixed).astype(int)
        target_exp = np.where(center == 0, 32, 16)
        nodes.append(vf**target_exp)
        weights.append(derivative*fold*vf**(target_exp-1)/(w/radius)**(exponent-1))
        centers.append(center)
        errors.append(float(error))
        maxsteps.append(int(max(steps)))
    return Problem(n, count, np.concatenate(nodes), np.concatenate(weights),
                   np.concatenate(centers), offset,
                   {'radius': radius, 'samples_per_orbit': count,
                    'geometry_sha256': geometry.sha256,
                    'max_reduction_steps': max(maxsteps),
                    'metric_relative_error': max(errors),
                    'nodes_precision': 'double; native arithmetic is on these supplied values'})


def build_bridge(belyi_root):
    source = Path(belyi_root)/'Cext/powser_arnoldi.c'
    wrapper = HERE/'belyi_cauchy_bridge.c'
    if not source.is_file():
        raise FileNotFoundError(source)
    compiler = shlex.split(os.environ.get('CC', 'cc'))
    flags = shlex.split(subprocess.check_output(['pkg-config', '--cflags', '--libs', 'flint'], text=True))
    digest = hashlib.sha256(source.read_bytes()+wrapper.read_bytes()+repr((compiler, flags)).encode()).hexdigest()
    directory = HERE/'.build'
    directory.mkdir(exist_ok=True)
    binary = directory/f'belyi_bridge_{digest[:20]}'
    if not binary.exists():
        with tempfile.TemporaryDirectory(dir=directory) as temp:
            target = Path(temp)/'bridge'
            subprocess.run([*compiler, '-O3', '-std=c11', '-D_POSIX_C_SOURCE=200809L',
                            '-pthread', '-I', str(source.parent), str(wrapper), '-o', str(target),
                            *flags, '-lmpfr', '-lgmp', '-lm'], check=True)
            os.replace(target, binary)
    return binary, {'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                    'wrapper_sha256': hashlib.sha256(wrapper.read_bytes()).hexdigest()}


def native(problem, coefficients, mode='new', belyi_root='/Users/musty/Belyi', digits=40,
           eps_digits=6, maxiter=64, threads=4, timeout=180):
    if problem.offset != 0:
        raise ValueError('native input uses the unshifted DFT grid')
    if coefficients.ndim == 1:
        coefficients = coefficients[:, None]
    full = coefficients if mode == 'apply' else embed_new(coefficients)
    assert full.shape[0] == 3*problem.n and np.isfinite(full).all()
    binary, provenance = build_bridge(belyi_root)
    order = np.argsort(problem.centers, kind='stable')
    inverse = np.argsort(order)
    with tempfile.TemporaryDirectory(prefix='belyi-cover-') as temp:
        infile, outfile = Path(temp)/'input.txt', Path(temp)/'output.txt'
        with infile.open('w') as out:
            out.write(f'{digits} {eps_digits} {maxiter} {full.shape[1]} 2 {problem.count} 1\n')
            for center, length in enumerate((problem.n, 2*problem.n)):
                out.write(f'{length} 1 0 {np.count_nonzero(problem.centers == center)}\n')
            for x in problem.nodes[order]:
                out.write(f'{x.real:.17e} {x.imag:.17e} 1 0\n')
            for z in problem.weights:
                out.write(f'{z.real:.17e} {z.imag:.17e}\n')
            out.write(' '.join(str(int(i)+1) for i in inverse)+'\n')
            for col in full.T:
                for z in col:
                    out.write(f'{z.real:.17e} {z.imag:.17e}\n')
        started = time.monotonic()
        result = subprocess.run([str(binary), mode, str(infile), str(outfile), str(threads)],
                                capture_output=True, text=True, timeout=timeout)
        if result.returncode not in (0, 2) or not outfile.exists():
            raise RuntimeError(result.stdout+result.stderr)
        tokens = outfile.read_text().split()
        size, cols = map(int, tokens[:2])
        numbers = np.asarray([float(s) for s in tokens[2:]])
        values = numbers.reshape(cols, size, 2)
        output = (values[..., 0]+1j*values[..., 1]).T
        return output, {**provenance, 'exit_code': result.returncode,
                        'wall_seconds': time.monotonic()-started,
                        'stdout': result.stdout, 'stderr': result.stderr,
                        'arithmetic_decimal_digits': digits}


def side_audit(coefficients, geometry, radius, count=384, seed=810):
    rng = np.random.default_rng(seed)
    q, phase, delta = geometry.actions
    selected = np.resize(np.arange(len(q)), count)
    rng.shuffle(selected)
    qq, pp, dd = q[selected], phase[selected], delta[selected]
    midpoint = qq/(1+np.sqrt(dd))
    w = midpoint + 0.00002*(rng.random(count)-0.5)*np.exp(2j*np.pi*rng.random(count))
    v = pp*(w-qq)/(1-qq.conjugate()*w)
    derivative = pp*dd/(1-qq.conjugate()*w)**2
    keep = (abs(w) < radius) & (abs(v) < radius)
    w, v, derivative, selected = w[keep], v[keep], derivative[keep], selected[keep]
    def values(z):
        n = len(coefficients)//2
        x = (z/radius)**32
        a = np.polynomial.polynomial.polyval(x, coefficients[:n]).T*(z/radius)[:, None]**31
        b = np.polynomial.polynomial.polyval(x, coefficients[n:]).T*(z/radius)[:, None]**15
        f = np.empty((len(z), 3, coefficients.shape[1]), dtype=complex)
        f[:, geometry.fixed] = -2*a
        f[:, geometry.moving] = a+b
        f[:, geometry.partner] = a-b
        return f
    lhs, at_v = values(w), values(v)
    rhs = derivative[:, None, None]*at_v[np.arange(len(v))[:, None], geometry.images[selected]]
    scale = np.maximum(np.linalg.norm(lhs, axis=(0, 1)), np.linalg.norm(rhs, axis=(0, 1)))
    valid = scale > 1e-200
    defect = np.linalg.norm(lhs-rhs, axis=(0, 1))/np.maximum(scale, 1e-300)
    return {'relative_l2_by_column': [float(x) if ok else None for x, ok in zip(defect, valid)],
            'nonzero_columns': valid.tolist(), 'samples': len(w),
            'distinct_sides': len(set(selected.tolist()))}


def relative(a, b):
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a), np.linalg.norm(b), 1e-300))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument('--pilot', action='store_true')
    parser.add_argument('--native-solve-columns', type=int, default=0)
    parser.add_argument('--radius', type=float, default=0.99991)
    parser.add_argument('--belyi-root', default=os.environ.get('BELYI_ROOT', '/Users/musty/Belyi'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    geometry = Geometry()
    problem = make_problem(geometry, args.n, args.radius)
    rng = np.random.default_rng(81051)
    vectors = rng.normal(size=(2*args.n, 2))+1j*rng.normal(size=(2*args.n, 2))
    result, provenance = native(problem, vectors, belyi_root=args.belyi_root)
    agreement = relative(result, problem.apply_new(vectors))
    assert agreement < 1e-11, agreement
    old = rng.normal(size=(args.n, 2))+1j*rng.normal(size=(args.n, 2))
    full, full_provenance = native(problem, embed_old(old), 'apply', belyi_root=args.belyi_root)
    scalar_matrix, _ = scalar.sampled_operator(args.n, args.radius, geometry.actions,
                                               oversample=4, offset=0)
    old_agreement = relative(full[:args.n], scalar_matrix@old)
    assert old_agreement < 1e-10, old_agreement
    report = {'n': args.n, **problem.stats, 'native': provenance,
              'native_vs_numpy': agreement, 'old_component_vs_scalar': old_agreement,
              'status': 'operator adapter checked; no differential basis computed'}
    if args.pilot:
        matrix = problem.dense_new()
        size = len(matrix)
        if size <= 50:
            raise ValueError('pilot needs room for 48 directions and a spectral comparison')
        factors = lu_factor(matrix-np.eye(size))
        inverse = LinearOperator((size, size), matvec=lambda v: lu_solve(factors, v), dtype=complex)
        eigenvalues, eigenvectors = eigs(matrix, k=min(56, size-2), sigma=1, OPinv=inverse,
                                         v0=np.ones(size, dtype=complex), tol=1e-10)
        order = np.argsort(abs(eigenvalues-1))
        coefficients, _ = qr(eigenvectors[:, order[:48]], mode='economic')
        matrix_refine = np.eye(size)-matrix+coefficients@coefficients.conj().T
        factors_refine = lu_factor(matrix_refine)
        coefficients = lu_solve(factors_refine, coefficients)
        changed = make_problem(geometry, args.n, args.radius, oversample=3, offset=0.19)
        report['eigenvalue_distances'] = abs(eigenvalues[order]-1).tolist()
        report['finite_operator_defect'] = relative(problem.apply_new(coefficients), coefficients)
        report['changed_quadrature_defect'] = relative(changed.apply_new(coefficients), coefficients)
        report['side_audit'] = side_audit(coefficients, geometry, args.radius)
        report['status'] = '48 numerical candidate directions; inspect independent errors, not a certified basis'
        if args.native_solve_columns:
            refined, solve_report = native(problem, coefficients[:, :args.native_solve_columns],
                                           mode='solve', belyi_root=args.belyi_root, eps_digits=5,
                                           maxiter=64, timeout=180)
            report['native_solve'] = solve_report
            nonzero = bool(np.all(np.linalg.norm(refined, axis=0) > 1e-200))
            report['native_solve_nonzero'] = nonzero
            report['native_solve_finite_defect'] = relative(problem.apply_new(refined), refined) if nonzero else None
            report['native_solve_side_audit'] = side_audit(refined, geometry, args.radius)
        np.savez(args.output.with_suffix('.npz'), coefficients=coefficients, radius=args.radius)
    report['wall_seconds'] = time.monotonic()-started
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('native', 'native_solve', 'eigenvalue_distances')}, indent=2))


if __name__ == '__main__':
    main()
