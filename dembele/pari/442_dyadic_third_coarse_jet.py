"""D116: a fourth coarse coefficient from the frozen precision-200 moment bank.

No moments, transport centers, or earlier artifacts are changed. The direct
expansion of twice the A-kernel independently reproduces orders zero to two.
"""
import importlib.util
import json
from math import comb
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('base',ROOT/'dembele/pari/415_dyadic_coarse_poisson.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)

def coefficient(n,r):
    # [X^r](1-((1+X)/(1-X))^n), expanded using (1+2X/(1-X))^n.
    return -sum(2**k*comb(n,k)*comb(r-1,k-1) for k in range(1,min(n,r)+1)) if r else 0

def calculations():
    path=DATA/'dyadic_precision200_d115.json';old=json.loads(path.read_text())
    P=old['working_precision_pi'];C=old['CM_cutoff'];assert [P,C]==[200,399]
    precision=448;ring=b.CMring(precision)
    pi=ring.add(ring.scale(ring.mul(b.BETA,b.BETA),-1),ring.scale(b.ONE,-2))
    q=ring.add(ring.normalize(b.MP[1:]),ring.scale(b.BETA,-1))
    assert ring.mul(b.BETA,q)==pi and ring.val(q)==1
    powers=ring.powers(q,C);embed=np.array(ring.powers(pi,7),dtype=np.int64)
    assert 16*ring.maximum**2+ring.maximum<2**63
    assert 8*(1<<(P//8))*ring.maximum<2**63
    kernels=[];gains=[];errors=[]
    for j in range(4):
        n=2*j+2
        v2=lambda x:(x&-x).bit_length()-1
        gain=16*min(k+v2(comb(n,k)) for k in range(1,n+1));gains.append(gain)
        row=[ring.scale(powers[r],coefficient(n,r)) for r in range(C+1)]
        assert row[0]==b.ZERO and all(ring.val(x)>=min(precision,r+gain) for r,x in enumerate(row[1:],1))
        kernels.append(row)
        # Every retained coefficient has valuation >= gain+1. The omitted
        # tail starts at C+1 and moments are integral. Use a conservative bound.
        errors.append(min(precision,2*P+gain,C+1+gain))
    assert gains==[32,48,32,64] and errors==[432,448,432,448]
    results=[];counts=[0]*4;overlap=0
    for ci,chart in enumerate(old['CM_A_chart_moments']):
        assert chart['CM_index']==ci and chart['error_pi']==P and chart['chart']=='A'
        moments=(np.array(chart['moments_power_basis'],dtype=np.int64)@embed)%ring.mods
        values=[];valuations=[]
        for j in range(4):
            answer=np.zeros((16,16),dtype=np.int64)
            for r,c in enumerate(kernels[j]):
                if c!=b.ZERO:answer=(answer+ring.matrix(c)@moments[r].T)%ring.mods[:,None]
            rows=answer.T.tolist();values.append(rows)
            vs=[ring.val(x) for x in rows]
            valuations.append([v if v<errors[j] else None for v in vs]);counts[j]+=sum(v<errors[j] for v in vs)
            if j<3:
                for x,y in zip(rows,old['CM_values'][ci]['coarse_coefficients_beta'][j]):
                    assert ring.val(ring.add(x,ring.scale(y,-1)))>=old['coarse_error_beta'][j]
                    overlap+=1
        results.append({'CM_index':ci,'coarse_coefficients_beta':values,'error_beta':errors,
                        'certified_valuations_beta':valuations})
    print('THIRD_COARSE_JET|beta error 448; nonzero counts '+str(counts)+'; old coefficients checked '+str(overlap),flush=True)
    return {'status':'pass','milestone':'D116','working_precision_pi':P,'CM_cutoff':C,
       'arithmetic_precision_beta':precision,'coarse_orders':[0,1,2,3],
       'coarse_parameter':'u=((z-beta)/(z+beta))^2','twice_A_kernel_gains_beta':gains,
       'coarse_error_beta':errors,'CM_values':results,'nonzero_entries_by_coarse_order':counts,
       'old_coarse_coefficients_checked':overlap,'third_actual_coarse_jet_computed':True,
       'moment_precision_increased':False,'candidate_identification_proved':False,
       'target_field_polynomial_constructed':False,
       'sources':[b.source(x) for x in [Path(__file__),Path(b.__file__),path,
                   ROOT/'dembele/certificates/dyadic-coarse-d114.md']]}

if __name__=='__main__':
    result=calculations();out=DATA/'dyadic_third_coarse_jet_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('PASS|442_DYADIC_THIRD_COARSE_JET',flush=True)
