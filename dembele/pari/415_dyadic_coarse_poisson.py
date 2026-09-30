"""D114 actual harmonic-differential coarse coefficients in the matched CM charts.

Combine the D108 formulas before evaluation so all moment coefficients are
integral. Exact arithmetic modulo beta^80 supplies g0,g1,g2; the analytic
and moment error bounds are beta^48, beta^64, beta^48 respectively.
No ratio normalization or harmonic-to-residue basis change is performed.
"""
from functools import lru_cache
import importlib.util
import json
from math import comb
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
spec=importlib.util.spec_from_file_location('transport',ROOT/'dembele/pari/411_dyadic_moment_transports.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
source,checked=t.source,t.checked
MP=[2,0,64,0,336,0,672,0,660,0,352,0,104,0,16,0,1]
ZERO=(0,)*16;ONE=(1,)+(0,)*15;BETA=(0,1)+(0,)*14

class CMring:
    def __init__(self,precision=80):
        self.precision=precision
        self.mods=np.array([1<<max(0,(precision-i+15)//16) for i in range(16)],dtype=np.int64)
        self.maximum=int(max(self.mods));self.poly=np.array(MP[:-1],dtype=np.int64)
    def normalize(self,x):return tuple(int(c)%int(m) for c,m in zip(x,self.mods))
    def add(self,x,y):return self.normalize([a+b for a,b in zip(x,y)])
    def scale(self,x,n):return self.normalize([int(c)*int(n) for c in x])
    def mul(self,x,y):
        out=np.convolve(x,y)%self.maximum
        for k in range(30,15,-1):
            if out[k]:out[k-16:k]=(out[k-16:k]-int(out[k])*self.poly)%self.maximum
        return self.normalize(out[:16])
    def powers(self,x,n):
        p=[ONE]
        for _ in range(n):p.append(self.mul(p[-1],x))
        return p
    def val(self,x):
        return min((16*((int(c)&-int(c)).bit_length()-1)+i for i,c in enumerate(x) if c),default=self.precision)
    @lru_cache(None)
    def matrix(self,x):
        return np.array([self.mul(x,tuple(int(i==j) for i in range(16))) for j in range(16)],dtype=np.int64).T

def kernel_bank(R,cutoff):
    beta=BETA;pi=R.add(R.scale(R.mul(beta,beta),-1),R.scale(ONE,-2))
    # The exact integral identity beta*qA=pi avoids dividing an approximate value.
    qA=R.normalize(MP[1:]);qA=R.add(qA,R.scale(beta,-1))
    assert R.mul(beta,qA)==pi
    bp=R.powers(beta,R.precision);inv=ZERO
    for x in bp[:-1]:inv=R.add(inv,R.scale(x,-1))
    assert bp[-1]==ZERO and R.mul(R.add(beta,R.scale(ONE,-1)),inv)==ONE
    qB=R.mul(pi,inv);qC=R.mul(beta,pi);ratio=R.scale(R.mul(beta,inv),-2)
    Ap,Bp,Cp=R.powers(qA,cutoff),R.powers(qB,cutoff),R.powers(qC,cutoff)
    rp=R.powers(ratio,5);pref=R.mul(beta,inv);bank=[]
    for j in range(3):
        n=2*j+2;rows=[[],[],[]]
        for degree in range(cutoff+1):
            sa=sum((-2)**k*comb(n,k+1)*comb(k+degree,degree) for k in range(n))
            rows[0].append(R.scale(Ap[degree],sa))
            acc=ZERO
            for k in range(n):acc=R.add(acc,R.scale(rp[k],comb(n,k+1)*comb(k+degree,degree)))
            rows[1].append(R.mul(R.mul(pref,Bp[degree]),acc))
            sc=-sum(2**k*comb(n,k+1)*comb(degree-1,k) for k in range(min(n-1,degree-1)+1)) if degree else 0
            rows[2].append(R.scale(Cp[degree],sc))
        bank.append(rows)
    return bank,pi

def calculations():
    packet=json.loads((DATA/'dyadic_moment_extension_d114.json').read_text())
    interface=json.loads((DATA/'dyadic_poisson_jet_interface_d108.json').read_text())
    assert [int(x) for x in interface['CM_polynomial_ascending']]==MP
    assert packet['working_precision_pi']==16 and packet['CM_cutoff']==31
    ring=CMring(80);kernels,pi=kernel_bank(ring,31)
    assert ring.val(BETA)==1 and ring.val(pi)==2 and ring.val(ring.scale(ONE,2))==16
    # Stronger D108 bounds retain the exact binomial coefficient valuation.
    def v2(n):return (n&-n).bit_length()-1
    errors=[];gains=[]
    for j in range(3):
        term_gains=[16*(k+v2(comb(2*j+2,k+1))) for k in range(2*j+2)]
        gains.append(term_gains);errors.append(32+min(term_gains))
    assert errors==[48,64,48]
    embed=np.array(ring.powers(pi,7),dtype=np.int64)
    moments=[]
    for index,row in enumerate(packet['CM_chart_moments']):
        assert row['CM_index']==index//3 and row['chart']==['A','B','C'][index%3] and row['error_pi']==16
        # degree x measure x beta power, then transpose for column evaluation.
        moments.append((np.array(row['moments_power_basis'],dtype=np.int64)@embed)%ring.mods)
    moments=np.array(moments).reshape(17,3,32,16,16).transpose(0,1,2,4,3)
    results=[];allcounts=[0]*3
    for ci in range(17):
        values=[];valuations=[];lower=[]
        for j in range(3):
            answer=np.zeros((16,16),dtype=np.int64)
            for chart in range(3):
                for degree,c in enumerate(kernels[j][chart]):
                    if c!=ZERO:answer+=ring.matrix(c)@moments[ci,chart,degree]
            answer%=ring.mods[:,None];rows=answer.T.tolist();values.append(rows)
            vs=[ring.val(row) for row in rows]
            valuations.append([v if v<errors[j] else None for v in vs])
            lower.append([min(v,errors[j]) for v in vs]);allcounts[j]+=sum(v<errors[j] for v in vs)
        results.append({'CM_index':ci,'coarse_coefficients_beta':values,'error_beta':errors,
                        'certified_valuations_beta':valuations,'valuation_lower_bounds_beta':lower})
    anchor=results[0]['certified_valuations_beta'][0]
    available=[(v,i) for i,v in enumerate(anchor) if v is not None]
    chosen=min(available) if available else None
    witness=None if chosen is None else {'harmonic_basis_index':chosen[1],'valuation_beta':chosen[0],
                                        'absolute_error_beta':errors[0],
                                        'relative_precision_beta':errors[0]-chosen[0],
                                        'division_performed':False}
    print(f'COARSE|actual g0/g1/g2 at 17 CM points; beta-error {errors}; nonzero entries {allcounts}',flush=True)
    print('ANCHOR|'+json.dumps(witness),flush=True)
    return {'status':'pass','milestone':'D114','arithmetic_precision_beta':80,
            'CM_moment_precision_pi':16,'CM_moment_cutoff':31,'coarse_parameter':'u=((z-beta)/(z+beta))^2',
            'coarse_orders':[0,1,2],'kernel_coefficients_beta':kernels,
            'binomial_error_gains_beta':gains,'coarse_error_beta':errors,'coarse_error_pi':[24,32,24],
            'CM_values':results,'nonzero_entries_by_coarse_order':allcounts,
            'anchor_nonvanishing_witness':witness,
            'actual_harmonic_coarse_differential_2jet_computed':True,
            'actual_rational_frame_ratio_jet_computed':False,
            'actual_harmonic_to_residue_frame_change_computed':False,
            'Gaussian_pivot_certified':False,'candidate_identification_proved':False,
            'target_field_polynomial_constructed':False,
            'sources':[source(p) for p in [Path(__file__),Path(t.__file__),
                DATA/'dyadic_moment_extension_d114.json',DATA/'dyadic_poisson_jet_interface_d108.json']]}

def main():
    out=DATA/'dyadic_coarse_poisson_d114.json';assert not out.exists()
    result=calculations();out.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS|415_DYADIC_COARSE_POISSON',flush=True)

if __name__=='__main__':main()
