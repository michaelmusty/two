"""D121 propagate the certified P=400 column to all CM points and four jets.

Only the state rows needed by the seventeen A charts are extended. The
CM coefficient ring uses arbitrary integers; no int64 products are used.
"""
import importlib.util
import json
from math import comb
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('lift',ROOT/'dembele/pari/473_dyadic_actual_precision_lift.py')
l=importlib.util.module_from_spec(s);s.loader.exec_module(l)
b,p=l.b,l.p
MP=[2,0,64,0,336,0,672,0,660,0,352,0,104,0,16,0,1]
ZERO=(0,)*16;ONE=(1,)+(0,)*15;BETA=(0,1)+(0,)*14


class Ring:
    def __init__(self,precision=864):
        assert precision%16==0
        self.precision=precision;self.mod=1<<(precision//16);self.mask=self.mod-1
    def add(self,a,b):return tuple((x+y)&self.mask for x,y in zip(a,b))
    def scale(self,a,n):return tuple((n*x)&self.mask for x in a)
    def mul(self,a,b):
        z=[0]*31
        for i,x in enumerate(a):
            for j,y in enumerate(b):z[i+j]+=x*y
        for k in range(30,15,-1):
            for j in range(0,16,2):z[k-16+j]-=z[k]*MP[j]
        return tuple(x&self.mask for x in z[:16])
    def powers(self,x,n):
        out=[ONE]
        for _ in range(n):out.append(self.mul(out[-1],x))
        return out
    def value(self,x):
        return min([self.precision]+[16*((c&-c).bit_length()-1)+i for i,c in enumerate(x) if c])


def coefficient(n,r):
    return -sum((1<<k)*comb(n,k)*comb(r-1,k-1) for k in range(1,min(n,r)+1)) if r else 0


def build():
    begin=time.monotonic();P=400;H=3*P-2;C=2*P-1;column=0
    previous='dyadic_actual_P400_col0_verified_d121'
    saved,state,_,statepath=l.checkpoint(previous)
    assert saved['actual_moment_precision_increased']
    packet=json.loads((DATA/'dyadic_target_transports_d121.json').read_text())
    charts=[row for row in packet['CM_charts'] if row['chart']=='A'];assert len(charts)==17
    targets,params,transportpath=b.parameters(P);ring=p.Ring(P//8)
    required=sorted({row['target_edge'] for row in charts});extended={};plans={}
    bankpath=DATA/'dyadic_precision200_d115.json';old=json.loads(bankpath.read_text());mask=(1<<25)-1
    for e in required:
        total=[b.ZERO]*(H+1)
        for branch,j in enumerate(targets[e]):
            pars=params[e][branch]
            if pars not in plans:plans[pars]=l.Plan(ring,*pars,P,H+1)
            total=ring.padd(total,plans[pars].apply(state[j]))
        assert total[:P]==state[e]
        assert [tuple(c&mask for c in row) for row in total[:599]]==[
            tuple(m[column]) for m in old['state_moments_power_basis'][e]]
        extended[e]=total
    print(f'ACTUAL_CM_STATES|{len(required)} target states extended through {H}; seconds={time.monotonic()-begin:.3f}',flush=True)
    values=[]
    for ci,row in enumerate(charts):
        assert row['CM_index']==ci and row['normalized_error_pi']>=P
        pars=[tuple(int(c)&ring.mask for c in a) for a in row['normalized_center'][:3]]
        got=l.Plan(ring,*pars,H+1,C+1).apply(extended[row['target_edge']])
        assert got[0]==(row['zeroth_moments'][column]&ring.mask,)+(0,)*7
        assert [tuple(c&mask for c in a) for a in got[:400]]==[
            tuple(m[column]) for m in old['CM_A_chart_moments'][ci]['moments_power_basis']]
        values.append(got)
        if ci%4==0:print(f'ACTUAL_CM_CHARTS|{ci+1}/17; seconds={time.monotonic()-begin:.3f}',flush=True)
    # Independent arithmetic controls against the previously bounded ring.
    coarse=b.module('old_coarse','415_dyadic_coarse_poisson.py')
    cm=Ring();oldring=coarse.CMring(448)
    for i in range(5):
        x=tuple((cm.mod-1-19*i-31*j)&cm.mask for j in range(16))
        y=tuple((cm.mod-7-13*i-17*j)&cm.mask for j in range(16))
        expected=oldring.mul(oldring.normalize(x),oldring.normalize(y))
        assert tuple(c%oldring.maximum for c in cm.mul(x,y))==expected
    pi=cm.add(cm.scale(cm.mul(BETA,BETA),-1),cm.scale(ONE,-2))
    powers=cm.powers(pi,8);relation=ZERO
    for n,c in enumerate([2,0,-16,0,20,0,-8,0,1]):relation=cm.add(relation,cm.scale(powers[n],c))
    assert relation==ZERO and cm.value(pi)==2
    q=cm.add(tuple(MP[1:]),cm.scale(BETA,-1));assert cm.mul(BETA,q)==pi and cm.value(q)==1
    qp=cm.powers(q,C);kernels=[];errors=[];gains=[]
    for order in range(4):
        n=2*order+2
        gain=16*min(k+(comb(n,k)&-comb(n,k)).bit_length()-1 for k in range(1,n+1))
        row=[cm.scale(qp[r],coefficient(n,r)) for r in range(C+1)]
        assert all(cm.value(x)>=min(cm.precision,r+gain) for r,x in enumerate(row))
        kernels.append(row);gains.append(gain);errors.append(min(cm.precision,2*P+gain,C+1+gain))
    assert gains==[32,48,32,64] and errors==[832,848,832,864]
    jetpath=DATA/'dyadic_third_coarse_jet_d116.json';oldjets=json.loads(jetpath.read_text());results=[]
    for ci,moments in enumerate(values):
        embedded=[]
        for m in moments:
            x=ZERO
            for c,a in zip(m,powers):x=cm.add(x,cm.scale(a,c))
            embedded.append(x)
        jets=[];valuations=[]
        for order,kernel in enumerate(kernels):
            value=ZERO
            for a,m in zip(kernel,embedded):value=cm.add(value,cm.mul(a,m))
            prior=tuple(oldjets['CM_values'][ci]['coarse_coefficients_beta'][order][column])
            assert cm.value(cm.add(value,cm.scale(prior,-1)))>=oldjets['coarse_error_beta'][order]
            jets.append(list(value));v=cm.value(value);valuations.append(v if v<errors[order] else None)
        results.append({'CM_index':ci,'coarse_coefficients_beta':jets,'certified_valuations_beta':valuations})
    chartfile=DATA/'dyadic_actual_CM_P400_col0_d121_moments.bin';assert not chartfile.exists()
    chartfile.write_bytes(b.pack(values,P//8))
    paths=[Path(__file__),Path(l.__file__),Path(coarse.__file__),statepath,transportpath,bankpath,jetpath,chartfile]
    paths += [Path(x['path']) for x in saved['checkpoint_files']]
    result={'status':'pass','milestone':'D121','harmonic_basis_column':column,'working_precision_pi':P,
        'state_cutoff':H,'CM_cutoff':C,'extended_target_states':required,'CM_charts_checked':17,
        'CM_moment_scalar_coefficients':17*(C+1)*8,'coarse_orders':[0,1,2,3],
        'arithmetic_precision_beta':cm.precision,'kernel_gains_beta':gains,'coarse_error_beta':errors,
        'CM_values':results,'old_coarse_values_checked':68,'independent_ring_products_checked':5,
        'old_CM_moment_scalar_coefficients_checked':17*400*8,
        'actual_moment_precision_increased':True,'actual_harmonic_columns_refined':1,
        'full_sixteen_column_bank_precision_pi':200,'candidate_identification_proved':False,
        'wall_seconds':time.monotonic()-begin,'sources':[p.f.source(x) for x in paths]}
    print('ACTUAL_CM_RESULT|'+json.dumps({k:v for k,v in result.items() if k not in ('sources','CM_values')}),flush=True)
    return result


if __name__=='__main__':
    out=DATA/'dyadic_actual_CM_P400_col0_d121.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n');print('PASS|475_DYADIC_ACTUAL_CM_COLUMN',flush=True)
