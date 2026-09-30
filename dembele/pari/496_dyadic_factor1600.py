"""D124 factor the P=1600 r=32 low block, preserving every P=800 coefficient."""
import argparse
import importlib.util
import json
from pathlib import Path
import time
import resource
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('low',ROOT/'dembele/pari/472_dyadic_multiprecision_low_factor.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
ZERO,ONE=b.ZERO,b.ONE


def build(P,stem):
    assert P==1600
    start=time.monotonic();r=32;algebra=b.Algebra(P//8)
    targets,params,transport=b.parameters(P)
    oldpath=DATA/'dyadic_sparse_low_r32_d121.npz';old=np.load(oldpath);order=old['order'].tolist()
    oldD=old['diagonal'];oldL={tuple(k):v for k,v in zip(old['lower_keys'].tolist(),old['lower'])}
    oldU={tuple(k):v for k,v in zip(old['upper_keys'].tolist(),old['upper'])}
    def oldcheck(a,expected):
        assert np.array_equal(np.array(b.reduce(a,(1<<25)-1),dtype=np.int64),expected)
    identity=algebra.identity(r);zero=[[ZERO]*r for _ in range(r)]
    original={(i,i):identity for i in range(174)};cache={}
    for e in range(174):
        for branch,j in enumerate(targets[e]):
            pars=params[e][branch]
            if pars not in cache:cache[pars]=b.coefficients(pars,r,algebra)
            original[e,j]=algebra.sub(original.get((e,j),zero),cache[pars])
    coefficient_seconds=time.monotonic()-start
    blocks=dict(original);live=set(order);D,L,U={},{},{};updates=0
    for step,pivot in enumerate(order):
        seed=[[tuple(map(int,x)) for x in row] for row in oldD[pivot]]
        D[pivot]=algebra.inverse_from_seed(blocks[pivot,pivot],seed);oldcheck(D[pivot],oldD[pivot])
        incoming=sorted(i for i in live if i!=pivot and (i,pivot) in blocks)
        outgoing=sorted(j for j in live if j!=pivot and (pivot,j) in blocks)
        for j in outgoing:U[pivot,j]=blocks[pivot,j];oldcheck(U[pivot,j],oldU[pivot,j])
        for i in incoming:
            multiplier=algebra.mul(blocks[i,pivot],D[pivot]);L[i,pivot]=multiplier;oldcheck(multiplier,oldL[i,pivot])
            for j in outgoing:
                blocks[i,j]=algebra.sub(blocks.get((i,j),zero),algebra.mul(multiplier,blocks[pivot,j]));updates+=1
            del blocks[i,pivot]
        for j in outgoing:del blocks[pivot,j]
        del blocks[pivot,pivot];live.remove(pivot)
        if step%30==0 or step==173:print(f'STAGED_FACTOR|P={P}; pivots={step+1}; updates={updates}; seconds={time.monotonic()-start:.3f}',flush=True)
    assert not blocks and updates==2246
    factor_seconds=time.monotonic()-start-coefficient_seconds
    keys=[['D',i,i] for i in range(174)]+[['L',i,j] for i,j in sorted(L)]+[['U',i,j] for i,j in sorted(U)]
    def block(kind,i,j):return D[i] if kind=='D' else (L if kind=='L' else U)[i,j]
    priorpath=DATA/'dyadic_low_factor_P800_r32_d123.json';prior=json.loads(priorpath.read_text())
    priorbin=priorpath.with_suffix('.bin');assert prior['binary_block_order']==keys and prior['order']==order
    with priorbin.open('rb') as f:
        for kind,i,j in keys:
            expected=b.unpack(f.read(r*r*8*13),r,r,100)
            assert b.reduce(block(kind,i,j),(1<<100)-1)==expected
        assert not f.read()
    then=time.monotonic();rhs=[b.k.data(r,2,algebra.bits,f'D124-P{P}-state{i}') for i in range(174)]
    answer=b.solve(rhs,order,D,L,U,algebra)
    residual=[[[ZERO]*2 for _ in range(r)] for _ in range(174)]
    for (i,j),a in original.items():residual[i]=algebra.add(residual[i],algebra.mul(a,answer[j]))
    assert residual==rhs
    residual_seconds=time.monotonic()-then
    binary=DATA/(stem+'.bin');assert not binary.exists()
    with binary.open('wb') as f:
        for kind,i,j in keys:f.write(b.pack(block(kind,i,j),algebra.bits))
    width=(algebra.bits+7)//8;assert binary.stat().st_size==len(keys)*r*r*8*width
    return {'status':'pass','milestone':'D124','working_precision_pi':P,'eliminated_positive_moments':r,
        'modulus_bits':algebra.bits,'order':order,'binary_block_order':keys,'binary_coefficient_width_bytes':width,
        'binary_payload_bytes':binary.stat().st_size,'block_updates':updates,'all_P800_factor_coefficients_agree':True,
        'diagonal_inverse_products_checked':174,'unrelated_rhs_columns':2,'original_sparse_residual_checked':True,
        'original_scalar_equations_checked':174*r*8*2,'coefficient_seconds':coefficient_seconds,
        'factor_seconds':factor_seconds,'solve_and_residual_seconds':residual_seconds,
        'wall_seconds':time.monotonic()-start,'actual_moment_precision_increased':False,
        'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        'sources':[b.p.f.source(x) for x in [Path(__file__),Path(b.__file__),Path(b.p.__file__),Path(b.k.__file__),
            b.k.LIBRARY,transport,oldpath,priorpath,priorbin,binary]]}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--precision',type=int,default=1600)
    args=parser.parse_args();stem=f'dyadic_low_factor_P{args.precision}_r32_d124';out=DATA/(stem+'.json')
    assert not out.exists();result=build(args.precision,stem);out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['sources','order','binary_block_order']}),flush=True)
    print('PASS|496_DYADIC_FACTOR1600',flush=True)
