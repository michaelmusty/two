"""D115 batched full-polynomial refinement in separately bounded phases.

The operators and their application are separate jobs, each retaining the
180-second cap. NumPy carries bounded integers only; no numerical tolerance.
"""
import argparse
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import time
import numpy as np
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('base',ROOT/'dembele/pari/415_dyadic_coarse_poisson.py')
base=importlib.util.module_from_spec(s);s.loader.exec_module(base)
FP=np.array([2,0,-16,0,20,0,-8,0],dtype=np.int64)

def ring(P):
    assert P%8==0 and 16<=P<=152
    mod=1<<(P//8)
    def mul(x,y):
        out=np.convolve(x,y)%mod
        for k in range(14,7,-1):out[k-8:k]=(out[k-8:k]-out[k]*FP)%mod
        return out[:8]
    eye=np.eye(8,dtype=np.int64)
    matrices=np.array([[mul(x,y) for y in eye] for x in eye]).transpose(0,2,1)
    return mod,matrices

def operators(P,path):
    start=time.monotonic();mod,matrices=ring(P);H=3*P-2;C=2*P-1
    packet=json.loads((DATA/'dyadic_moment_transports_d113.json').read_text())
    def params(row):
        assert row['normalized_error_pi']>=P
        return tuple(tuple(int((q:=Fraction(c)).numerator*pow(q.denominator,-1,mod)%mod) for c in x)
                     for x in row['normalized_center'][:3])
    unique=sorted({params(c) for row in packet['transitions'] for c in row['children']})
    lookup={p:i for i,p in enumerate(unique)}
    targets=np.array([[c['target_edge'] for c in row['children']] for row in packet['transitions']])
    indices=np.array([[lookup[params(c)] for c in row['children']] for row in packet['transitions']])
    cm=[row for row in packet['CM_charts'] if row['chart']=='A']
    def powers(pars,degree,cutoff):
        count=len(pars);par=np.array(pars,dtype=np.int64)
        M=np.einsum('eri,ijk->erjk',par,matrices)%mod;A,B,D=M[:,0],M[:,1],M[:,2]
        dtype=np.uint16 if mod<=65536 else np.uint32
        out=np.zeros((count,degree+1,cutoff+1,8),dtype=dtype);out[:,0,0,0]=1
        for n in range(1,degree+1):
            out[:,n,0]=np.einsum('eij,ej->ei',B,out[:,n-1,0])%mod
            for k in range(1,min(cutoff,n+P-1)+1):
                out[:,n,k]=(np.einsum('eij,ej->ei',B,out[:,n-1,k])
                             +np.einsum('eij,ej->ei',A,out[:,n-1,k-1])
                             -np.einsum('eij,ej->ei',D,out[:,n,k-1]))%mod
        return out
    child=powers(unique,H,P)
    assert not np.any(child[:,:,P]);child=child[:,:,:P].copy()
    print(f'CHILD_OPERATORS|P={P}, unique={len(unique)}, seconds={time.monotonic()-start:.2f}',flush=True)
    charts=powers([params(c) for c in cm],C,H)
    assert not path.exists()
    np.savez_compressed(path,P=np.array(P),child=child,targets=targets,indices=indices,
                        charts=charts,CM_targets=np.array([c['target_edge'] for c in cm]))
    print(f'OPERATORS_SAVED|{path.name}, seconds={time.monotonic()-start:.2f}',flush=True)

def solve(P,op_path,seed_path,out_path):
    start=time.monotonic();mod,matrices=ring(P);H=3*P-2;C=2*P-1
    ops=np.load(op_path);assert int(ops['P'])==P
    child=ops['child'];indices=ops['indices'];targets=ops['targets']
    seed=json.loads(seed_path.read_text());oldP=seed['working_precision_pi']
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    m=np.array(seed['state_moments_power_basis'],dtype=np.int64).transpose(0,1,3,2)[:,:P].copy()
    assert m.shape==(174,P,8,16)
    mass=np.zeros((174,8,16),dtype=np.int64);mass[:,0,:]=np.array(harmonic['harmonic_basis']).T%mod
    m[:,0]=mass
    assert 32*(H+1)*P*mod**2<2**63
    def transformed(bank):return np.einsum('iab,ekbc->ekiac',matrices,bank)%mod
    def apply(bank,rows,cut):
        if cut==0:return np.zeros((174,rows,8,16),dtype=np.int64)
        bm=transformed(bank[:,:cut]).reshape(174,cut*8,128)
        out=np.zeros((174,rows,128),dtype=np.int64)
        for e in range(174):
            for branch in range(2):
                cs=child[indices[e,branch],:rows,:cut].reshape(rows,cut*8).astype(np.int64)
                out[e]=(out[e]+cs@bm[targets[e,branch]])%mod
        return out.reshape(174,rows,8,16)
    def valuation(bank):
        for v in range(P):
            if np.any(bank[:,:,v%8]&(1<<(v//8))):return v
        return P
    first=apply(m,P,P);first[:,0]=mass;delta=(first-m)%mod;gains=[]
    for iteration in range(oldP,P):
        gain=valuation(delta);assert gain>=iteration and not np.any(delta[:,0]);gains.append(gain)
        m=(m+delta)%mod
        if iteration+1<P:delta=apply(delta,P,max(0,P-gain));delta[:,0]=0
    assert np.array_equal(apply(m,P,P),m)
    full=apply(m,H+1,P)
    old=np.array(seed['state_moments_power_basis']).transpose(0,1,3,2)
    assert np.array_equal(full[:,:old.shape[1]]% (1<<(oldP//8)),old)
    print(f'STATES|P={P}, gains={gains}, residual and overlap pass; seconds={time.monotonic()-start:.2f}',flush=True)
    tbank=transformed(full).reshape(174,(H+1)*8,128);charts=[]
    for ci,cs in enumerate(ops['charts']):
        row=(cs.reshape(C+1,(H+1)*8).astype(np.int64)@tbank[ops['CM_targets'][ci]])%mod
        charts.append({'CM_index':ci,'chart':'A','moments_power_basis':row.reshape(C+1,8,16).transpose(0,2,1).tolist(),'error_pi':P})
    precision=2*P+48;M=base.CMring(precision);kernels,pi=base.kernel_bank(M,C)
    errors=[2*P+32,2*P+48,2*P+32];embed=np.array(M.powers(pi,7),dtype=np.int64)
    assert 32*(C+1)*16*int(max(M.mods))**2<2**63
    results=[]
    for ci,chart in enumerate(charts):
        moments=(np.array(chart['moments_power_basis'],dtype=np.int64)@embed)%M.mods
        values=[];vals=[]
        for j in range(3):
            answer=np.zeros((16,16),dtype=np.int64)
            for r,c in enumerate(kernels[j][0]):answer+=M.matrix(M.scale(c,2))@moments[r].T
            answer%=M.mods[:,None];cs=answer.T.tolist();values.append(cs)
            vals.append([v if (v:=M.val(x))<errors[j] else None for x in cs])
        results.append({'CM_index':ci,'coarse_coefficients_beta':values,'certified_valuations_beta':vals,'error_beta':errors})
    for row,oldrow in zip(results,seed['CM_values']):
        for j in range(3):
            for x,y in zip(row['coarse_coefficients_beta'][j],oldrow['coarse_coefficients_beta'][j]):
                assert M.val(M.add(x,M.scale(y,-1)))>=seed['coarse_error_beta'][j]
    print('ANCHOR|'+json.dumps(results[0]['certified_valuations_beta']),flush=True)
    result={'status':'pass','milestone':'D115','working_precision_pi':P,'low_cutoff':P-1,'state_cutoff':H,'CM_cutoff':C,
        'seed_precision_pi':oldP,'successive_difference_lower_bounds_pi':gains,
        'state_moments_power_basis':full.transpose(0,1,3,2).tolist(),'CM_A_chart_moments':charts,
        'coarse_error_beta':errors,'arithmetic_precision_beta':precision,'CM_values':results,
        'anchor_nonvanishing_certified':any(v is not None for v in results[0]['certified_valuations_beta'][0]),
        'rational_frame_computed':False,'candidate_identification_proved':False,
        'sources':[base.source(x) for x in [Path(__file__),Path(base.__file__),op_path,seed_path,
            DATA/'dyadic_moment_transports_d113.json',DATA/'dyadic_harmonic_certificate_d111.json']]}
    assert not out_path.exists();out_path.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(f'SOLVED|P={P}, seconds={time.monotonic()-start:.2f}',flush=True)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=['operators','solve'],required=True)
    p.add_argument('--precision',type=int,required=True);p.add_argument('--operators',type=Path,required=True)
    p.add_argument('--seed',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    if a.phase=='operators':operators(a.precision,a.operators)
    else:solve(a.precision,a.operators,a.seed,a.output)
    print('PASS|422_DYADIC_BATCHED',flush=True)

if __name__=='__main__':main()
