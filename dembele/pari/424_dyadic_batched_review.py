"""D115: static polynomial identities certify the batched operators and values."""
import argparse
from fractions import Fraction
import importlib.util
import json
from math import comb
from pathlib import Path
import time
import numpy as np
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('old',ROOT/'dembele/pari/416_dyadic_coarse_review.py')
old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
FP=[2,0,-16,0,20,0,-8,0]

def calculations(path,op_path):
    start=time.monotonic();p=json.loads(path.read_text());P=p['working_precision_pi'];mod=1<<(P//8)
    H=p['state_cutoff'];C=p['CM_cutoff'];assert [H,C]==[3*P-2,2*P-1]
    ops=np.load(op_path);assert int(ops['P'])==P
    transport=json.loads((DATA/'dyadic_moment_transports_d113.json').read_text())
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    def mul(x,y):
        v=[0]*15
        for i,a in enumerate(x):
            for j,b in enumerate(y):v[i+j]+=int(a)*int(b)
        for k in range(14,7,-1):
            for j,c in enumerate(FP):v[k-8+j]-=v[k]*c
        return [c%mod for c in v[:8]]
    eye=np.eye(8,dtype=np.int64)
    matrices=np.array([[mul(x,y) for y in eye] for x in eye]).transpose(0,2,1)
    def mat(x):return sum(int(c)*m for c,m in zip(x,matrices))%mod
    def params(row):
        assert row['normalized_error_pi']>=P
        return tuple(tuple(int((q:=Fraction(c)).numerator*pow(q.denominator,-1,mod)%mod) for c in x)
                   for x in row['normalized_center'][:3])
    def check(par,cs):
        cs=cs.astype(np.int64);A,B,D=map(mat,par)
        assert np.array_equal(cs[0,0],eye[0]) and not np.any(cs[0,1:])
        left=cs[1:].copy();left[:,1:]+=cs[1:,:-1]@D.T
        right=cs[:-1]@B.T;right[:,1:]+=cs[:-1,:-1]@A.T
        assert np.array_equal(left%mod,right%mod)
        # A unit perturbation fails this exact polynomial identity.
        assert not np.array_equal((left+1)%mod,right%mod)
    child=ops['child'];unique=sorted({params(c) for row in transport['transitions'] for c in row['children']})
    assert len(unique)==len(child)
    for par,cs in zip(unique,child):check(par,cs)
    cm=[row for row in transport['CM_charts'] if row['chart']=='A'];charts=ops['charts']
    for row,cs in zip(cm,charts):check(params(row),cs)
    print(f'OPERATOR_IDENTITIES|P={P}; all numerator/denominator polynomial identities pass; {time.monotonic()-start:.2f}s',flush=True)
    bank=np.array(p['state_moments_power_basis'],dtype=np.int64)
    assert bank.shape==(174,H+1,16,8) and np.all((0<=bank)&(bank<mod))
    assert 32*(H+1)*P*mod**2<2**63
    def transform(m):return np.stack([m@a.T for a in matrices],axis=1).reshape(len(m)*8,128)%mod
    transformed=[transform(m[:P]) for m in bank]
    for e,row in enumerate(transport['transitions']):
        rhs=np.zeros((H+1,128),dtype=np.int64)
        for j,c in enumerate(row['children']):
            index=int(ops['indices'][e,j]);target=int(ops['targets'][e,j])
            assert unique[index]==params(c) and target==c['target_edge']
            rhs=(rhs+child[index].reshape(H+1,P*8).astype(np.int64)@transformed[target])%mod
        assert np.array_equal(rhs.reshape(H+1,16,8),bank[e])
        assert all(row[0]==b[e]%mod and not np.any(row[1:]) for row,b in zip(bank[e,0],harmonic['harmonic_basis']))
    for ci,(row,cs) in enumerate(zip(cm,charts)):
        assert row['target_edge']==int(ops['CM_targets'][ci])
        rhs=(cs.reshape(C+1,(H+1)*8).astype(np.int64)@transform(bank[row['target_edge']]))%mod
        assert np.array_equal(rhs.reshape(C+1,16,8),np.array(p['CM_A_chart_moments'][ci]['moments_power_basis']))
    print(f'MOMENT_IDENTITIES|all states and CM transfers pass; {time.monotonic()-start:.2f}s',flush=True)
    M=old.FieldQuotient(p['arithmetic_precision_beta']);beta=old.BETA
    pi=M.add(M.scale(M.mul(beta,beta),-1),M.scale(old.MO,-2))
    q=M.add(M.norm(old.MP[1:]),M.scale(beta,-1));assert M.mul(beta,q)==pi
    qp=M.powers(q,C);embed=np.array(M.powers(pi,7),dtype=np.int64);errors=[2*P+32,2*P+48,2*P+32]
    assert p['coarse_error_beta']==errors
    kernels=[]
    for j in range(3):
        n=2*j+2;row=[old.MZ]
        for r in range(1,C+1):
            scalar=-sum(comb(n,i)*comb(n+r-i-1,r-i) for i in range(min(n,r)+1))
            assert scalar%(4 if j!=1 else 8)==0;row.append(M.scale(qp[r],scalar))
        kernels.append(row)
    for ci,chart in enumerate(p['CM_A_chart_moments']):
        moments=(np.array(chart['moments_power_basis'],dtype=np.int64)@embed)%M.mods
        for j in range(3):
            answer=np.zeros((16,16),dtype=np.int64)
            for r,c in enumerate(kernels[j]):answer+=M.matrix(c)@moments[r].T
            answer%=np.array(M.mods)[:,None]
            cs=answer.T.tolist();assert cs==p['CM_values'][ci]['coarse_coefficients_beta'][j]
            assert [v if (v:=M.val(x))<errors[j] else None for x in cs]==p['CM_values'][ci]['certified_valuations_beta'][j]
    prior=json.loads((DATA/'dyadic_coarse_review_d114.json').read_text());old.checked(prior['sources'])
    print('ANCHOR_VERIFIED|'+json.dumps(p['CM_values'][0]['certified_valuations_beta']),flush=True)
    print(f'REVIEW_FINISHED|{time.monotonic()-start:.2f}s',flush=True)
    return {'status':'pass','milestone':'D115','precision_pi':P,'all_operator_identities_verified':True,
      'all_state_residuals_and_CM_transfers_verified':True,'independent_coarse_kernel_expansion':True,
      'anchor_certified_valuations_beta':p['CM_values'][0]['certified_valuations_beta'],
      'D114_source_hashes_checked_unchanged':len(prior['sources']),
      'sources':[old.source(x) for x in [Path(__file__),Path(old.__file__),path,op_path,DATA/'dyadic_coarse_review_d114.json']]}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True)
    p.add_argument('--operators',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists();r=calculations(a.input,a.operators)
    a.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS|424_DYADIC_BATCHED_REVIEW',flush=True)

if __name__=='__main__':main()
