"""D122 control and benchmark compiled arbitrary-precision polynomial transport."""
import argparse
import ctypes as C
import importlib.util
import json
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('lift',ROOT/'dembele/pari/473_dyadic_actual_precision_lift.py')
l=importlib.util.module_from_spec(s);s.loader.exec_module(l)
p=l.p;b=l.b
CSOURCE=ROOT/'dembele/pari/476_dyadic_polynomial_kernel.c'
LIBRARY=DATA/'dyadic_polynomial_kernel_d122.dylib'


class Kernel:
    def __init__(self):
        self.lib=C.CDLL(str(LIBRARY));self.fn=self.lib.dembele_poly_mul
        self.fn.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p,C.c_long,C.c_long,C.c_long,C.c_ulong]
        self.fn.restype=C.c_int
    def multiply(self,a,b,bits,length):
        width=(bits+7)//8
        left=b''.join(int(c).to_bytes(width,'little') for row in a for c in row)
        right=b''.join(int(c).to_bytes(width,'little') for row in b for c in row)
        out=C.create_string_buffer(length*8*width)
        assert self.fn(out,left,right,len(a),len(b),length,bits)==0
        raw=out.raw
        return [tuple(int.from_bytes(raw[(8*i+j)*width:(8*i+j+1)*width],'little') for j in range(8))
                for i in range(length)]


class Ring(p.Ring):
    def __init__(self,bits):super().__init__(bits);self.kernel=Kernel();self.compiled_products=0
    def pmul(self,a,b,limit=None):
        if not a or not b:return []
        if limit is not None:a,b=a[:limit],b[:limit]
        length=len(a)+len(b)-1
        if limit is not None:length=min(length,limit)
        if length<24:return super().pmul(a,b,limit)
        self.compiled_products+=1
        return self.kernel.multiply(a,b,self.bits,length)


def build(target):
    paths=[Path(__file__),CSOURCE,Path(l.__file__),Path(p.__file__)]
    if not target:
        assert not LIBRARY.exists()
        snapshot=DATA/'dyadic_polynomial_kernel_d122_build_source.c';assert not snapshot.exists()
        snapshot.write_bytes(CSOURCE.read_bytes())
        command=['clang','-O3','-dynamiclib','-Wall','-Wextra','-Werror','-I/opt/homebrew/include',
                 '-L/opt/homebrew/lib','-Wl,-rpath,/opt/homebrew/lib',str(CSOURCE),'-o',str(LIBRARY),'-lflint','-lgmp']
        done=subprocess.run(command,capture_output=True,text=True,check=False)
        print(done.stdout+done.stderr,flush=True);assert done.returncode==0
        paths.append(snapshot)
    kernel=Kernel();controls=[]
    for bits in (3,25,50,1319,1536):
        a=b.k.data(1,5,bits,'poly-A')[0];bb=b.k.data(1,7,bits,'poly-B')[0]
        expected=p.f.slow_product(a,bb,1<<bits)
        for length in (1,9,11):assert kernel.multiply(a,bb,bits,length)==expected[:length]
        controls.append({'bits':bits,'lengths':[1,9,11]})
    products=[]
    for bits in (50,1319):
        a=b.k.data(1,193,bits,'long-A')[0];bb=b.k.data(1,257,bits,'long-B')[0]
        then=time.monotonic();got=kernel.multiply(a,bb,bits,320);elapsed=time.monotonic()-then
        assert got==p.Ring(bits).pmul(a,bb,320)
        products.append({'bits':bits,'input_lengths':[193,257],'output_length':320,'seconds':elapsed})
    timings=[]
    for P in ([10552] if target else [200,400,1600]):
        ring=Ring(P//8);pi=(0,1)+(0,)*6
        unit=tuple((ring.mod-7-19*j)&ring.mask for j in range(8))
        bb=tuple((ring.mod-3-11*j)&ring.mask for j in range(8))
        c=ring.mul(pi,unit);a=ring.add(pi,ring.mul(bb,c))
        values=[tuple((ring.mod-1-17*i-31*j)&ring.mask for j in range(8)) for i in range(P)]
        then=time.monotonic();plan=l.Plan(ring,a,bb,c,P,P);prepared=time.monotonic()-then
        then=time.monotonic();answer=plan.apply(values);elapsed=time.monotonic()-then
        small=p.Ring(25)
        assert [tuple(x&small.mask for x in row) for row in answer[:200]]==l.Plan(small,
            *[tuple(x&small.mask for x in row) for row in (a,bb,c)],200,200).apply([
                tuple(x&small.mask for x in row) for row in values[:200]])
        if not target:
            assert answer==l.Plan(p.Ring(P//8),a,bb,c,P,P).apply(values)
        timing={'synthetic_P':P,'prepare_seconds':prepared,'apply_seconds':elapsed,
            'compiled_products':ring.compiled_products}
        timings.append(timing);print('COMPILED_POLYNOMIAL_TRANSPORT|'+json.dumps(timing),flush=True)
    actual=[]
    if not target:
        _,state,_,statepath=l.checkpoint('dyadic_actual_P400_col0_verified_d121');paths.append(statepath)
        targets,params,transpath=b.parameters(400);paths.append(transpath);ring=Ring(50)
        for edge in (0,17,61,98,173):
            total=[b.ZERO]*400
            for branch,j in enumerate(targets[edge]):
                total=ring.padd(total,l.Plan(ring,*params[edge][branch],400,400).apply(state[j]))
            assert total==state[edge];actual.append(edge)
    paths += [LIBRARY,Path('/opt/homebrew/include/flint/fmpz_mod_poly.h'),
        Path('/opt/homebrew/lib/libflint.dylib').resolve(),Path('/opt/homebrew/lib/libgmp.dylib').resolve()]
    return {'status':'pass','milestone':'D122','small_product_controls':controls,
        'large_product_comparisons_with_GMP':products,'synthetic_transports':timings,
        'actual_P400_original_state_equations_checked':actual,'actual_new_moments_computed':False,
        'sources':[p.f.source(x) for x in paths]}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--target',action='store_true');args=parser.parse_args()
    out=DATA/('dyadic_polynomial_target_d122.json' if args.target else 'dyadic_polynomial_kernel_control_d122.json')
    assert not out.exists();out.write_text(json.dumps(build(args.target),indent=2)+'\n')
    print('PASS|477_DYADIC_POLYNOMIAL_KERNEL_CONTROL',flush=True)
