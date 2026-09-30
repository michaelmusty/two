"""D121 build, independently test and price the multiprecision block kernel."""
import ctypes as C
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
s = importlib.util.spec_from_file_location('reference', ROOT/'dembele/pari/459_dyadic_mobius_transform.py')
f = importlib.util.module_from_spec(s); s.loader.exec_module(f)
CSOURCE = ROOT/'dembele/pari/469_dyadic_block_kernel.c'
LIBRARY = DATA/'dyadic_block_kernel_d121.dylib'


class Kernel:
    def __init__(self):
        self.lib = C.CDLL(str(LIBRARY))
        self.fn = self.lib.dembele_block_mul
        self.fn.argtypes = [C.c_void_p, C.c_void_p, C.c_void_p, C.c_long, C.c_long, C.c_long, C.c_ulong]
        self.fn.restype = C.c_int
        self.lib.dembele_flint_version.restype = C.c_char_p
        self.version = self.lib.dembele_flint_version().decode()

    def multiply(self, a, b, bits):
        nr, nk, nc = len(a), len(b), len(b[0])
        assert len(a[0]) == nk
        width = (bits+7)//8
        def pack(matrix):
            return b''.join(int(c).to_bytes(width,'little') for row in matrix for x in row for c in x)
        ab, bb = pack(a), pack(b)
        out = C.create_string_buffer(nr*nc*8*width)
        status = self.fn(out, ab, bb, nr, nk, nc, bits)
        assert status == 0
        raw = out.raw
        return [[tuple(int.from_bytes(raw[((i*nc+j)*8+u)*width:((i*nc+j)*8+u+1)*width],'little')
                       for u in range(8)) for j in range(nc)] for i in range(nr)]


def data(nr, nc, bits, label):
    width=(bits+7)//8; mask=(1 << bits)-1
    return [[tuple(int.from_bytes(hashlib.shake_256(f'{label}:{i}:{j}:{u}'.encode()).digest(width),'little') & mask
                   for u in range(8)) for j in range(nc)] for i in range(nr)]


def reference_entry(a, b, i, j, bits):
    mod = 1 << bits; total = [0]*8
    for k in range(len(b)):
        value = f.slow_product([a[i][k]], [b[k][j]], mod)[0]
        total = [(x+y) % mod for x,y in zip(total,value)]
    return tuple(total)


def build():
    assert not LIBRARY.exists()
    snapshot=DATA/'dyadic_block_kernel_d121_build_source.c'; assert not snapshot.exists()
    snapshot.write_bytes(CSOURCE.read_bytes())
    command=['clang','-O3','-dynamiclib','-Wall','-Wextra','-Werror',
             '-I/opt/homebrew/include','-L/opt/homebrew/lib','-Wl,-rpath,/opt/homebrew/lib',
             str(CSOURCE),'-o',str(LIBRARY),'-lflint','-lgmp']
    done=subprocess.run(command,capture_output=True,text=True,check=False)
    print(done.stdout+done.stderr,flush=True); assert done.returncode == 0
    kernel=Kernel(); tests=[]
    for bits in (3,25,200,1319,1536):
        a,b=data(3,4,bits,'A'),data(4,2,bits,'B')
        answer=kernel.multiply(a,b,bits)
        expected=[[reference_entry(a,b,i,j,bits) for j in range(2)] for i in range(3)]
        assert answer == expected
        tests.append({'bits':bits,'entries':6,'rectangular_shape':[3,4,2]})
    # Exercise every pair of b-basis vectors, including maximum-degree
    # terms, at a modulus where the eleven interpolation guard bits matter.
    eye=[tuple(int(i==j) for i in range(8)) for j in range(8)]
    a=[[x] for x in eye]; b=[eye]
    assert kernel.multiply(a,b,3) == [[f.slow_product([x],[y],8)[0] for y in eye] for x in eye]
    rows=[]
    for n,bits in ((8,25),(32,200),(32,1319),(64,1319)):
        a,b=data(n,n,bits,'dense-A'),data(n,n,bits,'dense-B')
        start=time.monotonic(); answer=kernel.multiply(a,b,bits); elapsed=time.monotonic()-start
        for i,j in ((0,0),(n//2,n//3),(n-1,n-1)):
            assert answer[i][j] == reference_entry(a,b,i,j,bits)
        row={'size':n,'modulus_bits':bits,'wall_seconds_including_binary_conversion':elapsed,
             'independent_full_dot_products_checked':3}
        rows.append(row);print('MULTIPRECISION_BLOCK|'+json.dumps(row),flush=True)
    paths=[Path(__file__),CSOURCE,snapshot,LIBRARY,Path(f.__file__),
        Path('/opt/homebrew/lib/libflint.dylib').resolve(),Path('/opt/homebrew/lib/libgmp.dylib').resolve()]
    paths += [Path('/opt/homebrew/include/flint')/name for name in ['fmpz.h','fmpz_mod.h','fmpz_mod_mat.h','flint.h']]
    return {'status':'pass','milestone':'D121','FLINT_version':kernel.version,
        'compile_command':command,'finite_difference_guard_bits':11,
        'multiprecision_rectangular_controls':tests,'field_basis_pair_products_checked':64,
        'benchmarks':rows,'fixed_width_multiplication_used':False,
        'even_ring_elements_inverted':False,'actual_moment_precision_increased':False,
        'full_high_precision_low_block_factorization_done':False,
        'sources':[f.source(p) for p in paths]}


if __name__=='__main__':
    out=DATA/'dyadic_block_kernel_control_d121.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n')
    print('PASS|470_DYADIC_BLOCK_KERNEL_CONTROL',flush=True)
