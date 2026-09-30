"""D122 capped lift phases using compiled products and a GMP final residual.

Reuse the frozen Schur implementation. A new column is accepted only after
the original complete operator has been reapplied with the older, separate
GMP polynomial backend. All fixed-width files and predecessor hashes remain
those of the D121 checkpoint protocol.
"""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('compiled',ROOT/'dembele/pari/477_dyadic_polynomial_kernel_control.py')
f=importlib.util.module_from_spec(s);s.loader.exec_module(f)


def run(args):
    l=f.l;original=l.p.Ring
    if args.phase!='verify':l.p.Ring=f.Ring
    try:result=l.run(args.phase,args.previous,args.column,args.output)
    finally:l.p.Ring=original
    result['milestone']='D122'
    result['polynomial_backend']='independent_previous_GMP' if args.phase=='verify' else 'FLINT_integer_interpolation'
    result['sources'] += [f.p.f.source(x) for x in [Path(__file__),Path(f.__file__),f.CSOURCE,f.LIBRARY,
        DATA/'dyadic_polynomial_kernel_control_d122.json',DATA/'dyadic_polynomial_target_d122.json']]
    if args.phase=='verify':result['certificate']['full_residual_uses_different_polynomial_backend_from_lift']=True
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=['seed','step','verify'],required=True)
    parser.add_argument('--previous');parser.add_argument('--column',type=int,default=1)
    parser.add_argument('--output',required=True);args=parser.parse_args()
    out=DATA/(args.output+'.json');assert not out.exists()
    out.write_text(json.dumps(run(args),indent=2)+'\n')
    print('PASS|478_DYADIC_COMPILED_LIFT',flush=True)
