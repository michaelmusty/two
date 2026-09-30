"""D124 control a compiled small-product path and measure actual transports."""
import argparse
import ctypes as C
import importlib.util
import json
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('weighted',ROOT/'dembele/pari/497_dyadic_weighted_chunks.py')
w=importlib.util.module_from_spec(s);s.loader.exec_module(w);h=w.h;b=w.b;p=w.p;f=w.f
CSOURCE=ROOT/'dembele/pari/502_dyadic_small_polynomial_kernel.c'
LIBRARY=DATA/'dyadic_adaptive_polynomial_kernel_d124.dylib'


class Kernel(f.Kernel):
    def __init__(self):
        self.lib=C.CDLL(str(LIBRARY));self.fn=self.lib.dembele_adaptive_poly_mul
        self.fn.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p,C.c_long,C.c_long,C.c_long,C.c_ulong];self.fn.restype=C.c_int


class Ring(p.Ring):
    def __init__(self,bits):super().__init__(bits);self.kernel=Kernel()
    def pmul(self,a,b,limit=None):
        if not a or not b:return []
        if limit is not None:a,b=a[:limit],b[:limit]
        length=len(a)+len(b)-1
        if limit is not None:length=min(length,limit)
        return self.kernel.multiply(a,b,self.bits,length)


def controls():
    assert not LIBRARY.exists()
    snapshot=DATA/'dyadic_adaptive_polynomial_build_source_d124.c';assert not snapshot.exists();snapshot.write_bytes(CSOURCE.read_bytes())
    command=['clang','-O3','-dynamiclib','-Wall','-Wextra','-Werror','-I/opt/homebrew/include',
        '-L/opt/homebrew/lib','-Wl,-rpath,/opt/homebrew/lib',str(CSOURCE),'-o',str(LIBRARY),'-lflint','-lgmp']
    done=subprocess.run(command,capture_output=True,text=True);print(done.stdout+done.stderr,flush=True);assert done.returncode==0
    h.PATHS.add(snapshot);kernel=Kernel();products=0
    for bits in (1,3,25,50,100,200,1319,1536):
        for na,nb in ((1,1),(1,7),(7,11),(13,13),(23,23),(31,37)):
            left=b.k.data(1,na,bits,'adaptive-left')[0];right=b.k.data(1,nb,bits,'adaptive-right')[0]
            expected=p.f.slow_product(left,right,1<<bits)
            for length in sorted({1,min(23,na+nb-1),min(24,na+nb-1),na+nb-1}):
                assert kernel.multiply(left,right,bits,length)==expected[:length];products+=1
    # Worst-case packed carries, zero products and truncation at each boundary.
    for bits in (3,100,1319):
        maximum=((1<<bits)-1,)*8
        for na,nb in ((2,3),(12,13),(23,23)):
            left=[maximum]*na;right=[maximum]*nb;expected=p.f.slow_product(left,right,1<<bits)
            for length in (1, min(23,na+nb-1),na+nb-1):
                assert kernel.multiply(left,right,bits,length)==expected[:length];products+=1
            assert kernel.multiply(left,[b.ZERO]*nb,bits,min(23,na+nb-1))==[b.ZERO]*min(23,na+nb-1);products+=1
    # Real low equations and full state equations; profile-free fair timings.
    timings=[];actual=0
    for P,stem,nc,rows,shift in [(800,'dyadic_staged_P800_col00_verified_d123',800,800,0),
        (1600,'dyadic_weighted_P1600_col00_step01_prepared_d124',800,33,100)]:
        packet,_=h.read(stem);file=packet['state_file'] if shift==0 else packet['operator_input_file']
        values=w.scaled_values(file,174,nc,P,shift);bitcount=P//8-shift
        reduced=[[tuple(c>>shift for c in x) for x in edge] for edge in values]
        targets,params,parampath=b.parameters(P);h.PATHS.add(parampath);answers=[]
        for cls in (f.Ring,Ring,p.Ring):
            ring=cls(bitcount);begin=time.monotonic();out=[]
            for e in (0,17,61,98,173):
                total=[b.ZERO]*rows
                for branch,j in enumerate(targets[e]):
                    pars=[tuple(c&ring.mask for c in x) for x in params[e][branch]]
                    total=ring.padd(total,w.l.Plan(ring,*pars,nc,rows).apply(reduced[j]))
                assert total==reduced[e][:rows];out.append(total)
            answers.append(out);timings.append({'working_P':P,'input_valuation_pi':8*shift,'input_count':nc,
                'output_count':rows,'backend':cls.__module__+'.'+cls.__name__,'seconds':time.monotonic()-begin})
        assert answers[0]==answers[1]==answers[2];actual+=5*rows*8
    return {'independent_small_products_checked':products,'bits_checked':[1,3,25,50,100,200,1319,1536],
        'actual_original_equation_scalar_checks':actual,'unprofiled_actual_timings':timings}


def target():
    controlpath=DATA/'dyadic_adaptive_kernel_control_d124.json';control=json.loads(controlpath.read_text());assert control['status']=='pass'
    h.PATHS.add(controlpath)
    expected=[x for x in control['sources'] if Path(x['path'])==LIBRARY];assert len(expected)==1 and h.source(LIBRARY)==expected[0]
    P=10552;answers=[];timings=[]
    for cls in (Ring,p.Ring):
        ring=cls(P//8);pi=(0,1)+(0,)*6
        unit=tuple((ring.mod-7-19*j)&ring.mask for j in range(8));bv=tuple((ring.mod-3-11*j)&ring.mask for j in range(8))
        c=ring.mul(pi,unit);a=ring.add(pi,ring.mul(bv,c))
        values=[tuple((ring.mod-1-17*i-31*j)&ring.mask for j in range(8)) for i in range(P)]
        begin=time.monotonic();plan=w.l.Plan(ring,a,bv,c,P,P);prepare=time.monotonic()-begin
        begin=time.monotonic();answer=plan.apply(values);elapsed=time.monotonic()-begin;answers.append(answer)
        timings.append({'backend':cls.__module__+'.'+cls.__name__,'prepare_seconds':prepare,'apply_seconds':elapsed})
        print('ADAPTIVE_TARGET|'+json.dumps(timings[-1]),flush=True)
    assert answers[0]==answers[1]
    return {'synthetic_target_P':P,'complete_scalar_comparisons':P*8,'timings':timings,
        'actual_harmonic_precision_increased':False,'complete_target_size_solve_costed':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--target',action='store_true');args=parser.parse_args()
    out=DATA/('dyadic_adaptive_target_d124.json' if args.target else 'dyadic_adaptive_kernel_control_d124.json')
    assert not out.exists();start=time.monotonic();certificate=target() if args.target else controls()
    h.PATHS.update([Path(__file__),Path(w.__file__),CSOURCE,f.CSOURCE,LIBRARY,
        Path('/opt/homebrew/include/gmp.h'),Path('/opt/homebrew/include/flint/fmpz_mod_poly.h'),
        Path('/opt/homebrew/lib/libflint.dylib').resolve(),Path('/opt/homebrew/lib/libgmp.dylib').resolve()])
    result={'status':'pass','milestone':'D124','phase':'target' if args.target else 'controls','certificates':certificate,
        'wall_seconds':time.monotonic()-start,'peak_rss_bytes':w.peak_rss(),
        'production_P1600_lift_not_modified':True,'sources':[h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='sources'}),flush=True)
    print('PASS|503_DYADIC_ADAPTIVE_KERNEL_CONTROL',flush=True)
