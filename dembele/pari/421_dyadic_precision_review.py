"""D115 independent ordinary-integer replay of higher precision moment banks."""
import argparse
from fractions import Fraction
from functools import lru_cache
import importlib.util
import json
from math import comb
from pathlib import Path
import time
import numpy as np
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('review114',ROOT/'dembele/pari/416_dyadic_coarse_review.py')
old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
FP=np.array([2,0,-16,0,20,0,-8,0],dtype=np.int64)

def calculations(path):
    start=time.monotonic();p=json.loads(path.read_text());P=p['working_precision_pi'];mod=1<<(P//8)
    H=p['state_cutoff'];C=p['CM_cutoff'];low=p['low_cutoff']
    assert [low,H,C]==[P-1,3*P-2,2*P-1]
    assert 32*(H+1)*P*mod**2<2**63
    packet=json.loads((DATA/'dyadic_moment_transports_d113.json').read_text())
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    def norm(x):return np.asarray(x,dtype=np.int64)%mod
    def enc(x):return norm([int((q:=Fraction(c)).numerator*pow(q.denominator,-1,mod)%mod) for c in x])
    def mul(x,y):
        z=np.convolve(x,y)%mod
        for k in range(14,7,-1):z[k-8:k]=(z[k-8:k]-z[k]*FP)%mod
        return z[:8]
    basis=np.eye(8,dtype=np.int64)
    matrices=np.array([[mul(x,y) for y in basis] for x in basis]).transpose(0,2,1)
    def matrix(x):return np.tensordot(x,matrices,axes=1)%mod
    def params(row):return tuple(tuple(enc(x)) for x in row['normalized_center'][:3])
    @lru_cache(None)
    def powers(par,degree,cutoff):
        a,b,c=[np.array(x,dtype=np.int64) for x in par];A,B,D=map(matrix,[a,b,c])
        out=np.zeros((degree+1,cutoff+1,8),dtype=np.int64);out[0,0,0]=1
        for n in range(1,degree+1):
            out[n,0]=(B@out[n-1,0])%mod
            for k in range(1,cutoff+1):out[n,k]=(B@out[n-1,k]+A@out[n-1,k-1]-D@out[n,k-1])%mod
        # Separate binomial numerator/denominator samples validate the recurrence.
        def xp(x,n):
            z=basis[0]
            for _ in range(n):z=mul(z,x)
            return z
        for n in sorted({1,2,degree}):
            for k in sorted({0,1,min(3,cutoff),cutoff}):
                z=np.zeros(8,dtype=np.int64)
                for i in range(min(n,k)+1):
                    term=mul(mul(xp(a,i),xp(b,n-i)),xp(c,k-i))
                    z=(z+(comb(n,i)*comb(n+k-i-1,k-i)*(-1)**(k-i)%mod)*term)%mod
                assert np.array_equal(z,out[n,k])
        return out
    bank=np.array(p['state_moments_power_basis'],dtype=np.int64).transpose(0,1,3,2)
    assert bank.shape==(174,H+1,8,16) and np.all((0<=bank)&(bank<mod))
    def transformed(m):
        return np.einsum('iab,kbc->kiac',matrices,m).reshape(len(m)*8,128)%mod
    tbank=[transformed(m[:P]) for m in bank]
    for e,row in enumerate(packet['transitions']):
        rhs=np.zeros((H+1,128),dtype=np.int64)
        for child in row['children']:
            assert child['normalized_error_pi']>=P
            cs=powers(params(child),H,P)
            assert np.all(cs[:,P]==0)
            rhs=(rhs+cs[:,:P].reshape(H+1,P*8)@tbank[child['target_edge']])%mod
        assert np.array_equal(rhs.reshape(H+1,8,16),bank[e]),('state',e)
        mass=np.zeros((8,16),dtype=np.int64);mass[0]=[b[e]%mod for b in harmonic['harmonic_basis']]
        assert np.array_equal(bank[e,0],mass)
    print(f'STATE_REVIEW|P={P}; {174*(H+1)*16} entries; {time.monotonic()-start:.2f}s',flush=True)
    cmrows=[x for x in packet['CM_charts'] if x['chart']=='A']
    for cm,saved in zip(cmrows,p['CM_A_chart_moments']):
        cs=powers(params(cm),C,H)
        rhs=(cs.reshape(C+1,(H+1)*8)@transformed(bank[cm['target_edge']]))%mod
        assert np.array_equal(rhs.reshape(C+1,8,16),np.array(saved['moments_power_basis']).transpose(0,2,1))
    print(f'CM_REVIEW|all 17 A charts; {time.monotonic()-start:.2f}s',flush=True)
    M=old.FieldQuotient(p['arithmetic_precision_beta']);beta=old.BETA
    pi=M.add(M.scale(M.mul(beta,beta),-1),M.scale(old.MO,-2))
    q=M.add(M.norm(old.MP[1:]),M.scale(beta,-1));assert M.mul(beta,q)==pi
    qp=M.powers(q,C);embed=np.array(M.powers(pi,7),dtype=np.int64)
    kernels=[]
    for j in range(3):
        n=2*j+2;row=[old.MZ]
        for r in range(1,C+1):
            scalar=-sum(comb(n,i)*comb(n+r-i-1,r-i) for i in range(min(n,r)+1))
            assert scalar%(4 if j!=1 else 8)==0
            row.append(M.scale(qp[r],scalar))
        kernels.append(row)
    errors=[2*P+32,2*P+48,2*P+32];assert p['coarse_error_beta']==errors
    for ci,chart in enumerate(p['CM_A_chart_moments']):
        moments=(np.array(chart['moments_power_basis'],dtype=np.int64)@embed)%M.mods
        for j in range(3):
            answer=np.zeros((16,16),dtype=np.int64)
            for r,c in enumerate(kernels[j]):answer+=M.matrix(c)@moments[r].T
            answer%=np.array(M.mods)[:,None]
            assert answer.T.tolist()==p['CM_values'][ci]['coarse_coefficients_beta'][j]
    earlier=json.loads((DATA/'dyadic_coarse_review_d114.json').read_text());old.checked(earlier['sources'])
    print(f'COARSE_REVIEW|independent numerator/binomial kernels; all values agree; {time.monotonic()-start:.2f}s',flush=True)
    return {'status':'pass','milestone':'D115','precision_pi':P,'state_entries':174*(H+1)*16,'CM_A_entries':17*(C+1)*16,
         'independent_state_residuals_and_CM_transfers':True,'independent_coarse_kernel_expansion':True,
         'D114_source_hashes_checked_unchanged':len(earlier['sources']),
         'sources':[old.source(x) for x in [Path(__file__),Path(old.__file__),path,DATA/'dyadic_coarse_review_d114.json']]}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();assert not a.output.exists()
    result=calculations(a.input);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS|421_DYADIC_PRECISION_REVIEW',flush=True)

if __name__=='__main__':main()
