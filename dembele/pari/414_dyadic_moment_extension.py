"""D114: solve low moments modulo pi^16, then recover high rows and CM moments.

Frozen D113 bit-plane arithmetic is used only within its certified P<=16
range. The finite contracting equations use columns 0,...,15; rows through
46 are recovered from that solution. CM moments through 31 have error 16.
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
spec=importlib.util.spec_from_file_location('d113',ROOT/'dembele/pari/412_dyadic_moment_pilot.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
r=old.r;source,checked=old.source,old.checked
P,LOW,HIGH,CM=16,15,46,31
R=old.Ring(1,P);V=old.Ring(16,P);ZERO=(0,0);ONE=(1,0)

def params(row):return tuple(R.encode([r.f(x)]) for x in row['normalized_center'][:3])

@lru_cache(None)
def powers(p,degree,cutoff):
    a,b,c=p;delta=R.add(a,R.neg(R.smul(b,c)));phi=[b,delta]
    for _ in range(2,cutoff+1):phi.append(R.neg(R.smul(c,phi[-1])))
    rows=[[ONE]+[ZERO]*cutoff]
    for _ in range(degree):
        nxt=[ZERO]*(cutoff+1)
        for i,u in enumerate(rows[-1]):
            if u!=ZERO:
                for k,v in enumerate(phi[:cutoff+1-i]):
                    if v!=ZERO:nxt[i+k]=R.add(nxt[i+k],R.smul(u,v))
        rows.append(nxt)
    return rows

def calculations():
    packet=json.loads((DATA/'dyadic_moment_transports_d113.json').read_text())
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    previous=json.loads((DATA/'dyadic_moment_pilot_d113.json').read_text())
    m0=[V.encode([[b[e]]+[0]*7 for b in harmonic['harmonic_basis']]) for e in range(174)]
    ops=[]
    for row in packet['transitions']:
        children=[]
        for child in row['children']:
            assert child['normalized_error_pi']>=P
            cs=powers(params(child),HIGH,LOW)
            assert all(R.val(cs[n][k])>=k for n in range(1,HIGH+1) for k in range(1,LOW+1))
            children.append((child['target_edge'],[[(k,c) for k,c in enumerate(row) if c!=ZERO] for row in cs]))
        ops.append(children)
    def evaluate(m,e,n):
        z=ZERO
        for f,rows in ops[e]:
            for k,c in rows[n]:z=V.add(z,V.smul(c,m[f][k]))
        return z
    def step(m):return [[m0[e]]+[evaluate(m,e,n) for n in range(1,LOW+1)] for e in range(174)]
    m=[[z]+[ZERO]*LOW for z in m0];gains=[]
    for iteration in range(1,P+1):
        new=step(m)
        gain=min(V.val(V.add(x,V.neg(y))) for row,prev in zip(new,m) for x,y in zip(row[1:],prev[1:]))
        assert gain>=iteration-1;gains.append(gain);m=new
    assert step(m)==m
    high=[row+[evaluate(m,e,n) for n in range(LOW+1,HIGH+1)] for e,row in enumerate(m)]
    # Project to the earlier precision, with independent old output as oracle.
    V12=old.Ring(16,12)
    for e,row in enumerate(high):
        for n,z in enumerate(row[:12]):
            assert V12.decode((z[0],z[1]&V12.highmask))==previous['state_moments_power_basis'][e][n]
    print('STATE_MOMENTS|16 low-degree iterations; rows through 46; all D113 overlaps agree',flush=True)
    charts=[];nonzero=anchor=0
    for chart in packet['CM_charts']:
        assert chart['normalized_error_pi']>=P
        cs=powers(params(chart),CM,HIGH);moments=[]
        for n,row in enumerate(cs):
            z=ZERO
            for k,c in enumerate(row):
                assert R.val(c)>=min(P,max(0,k-n))
                if c!=ZERO:z=V.add(z,V.smul(c,high[chart['target_edge']][k]))
            moments.append(V.decode(z))
            if n:
                count=sum(R.val(R.encode([x]))<P for x in moments[-1]);nonzero+=count
                if chart['CM_index']==0:anchor+=count
        exact=chart['zeroth_moments']
        assert moments[0]==V.decode(V.encode([[x]+[0]*7 for x in exact]))
        charts.append({'CM_index':chart['CM_index'],'chart':chart['chart'],
                       'moments_power_basis':moments,'error_pi':P,'zeroth_moments_exact':exact})
    print(f'CM_MOMENTS|degrees 0..31 modulo pi^16; positive nonzero {nonzero}; anchor {anchor}',flush=True)
    return {'status':'pass','milestone':'D114','working_precision_pi':P,'low_cutoff':LOW,
            'state_cutoff':HIGH,'CM_cutoff':CM,'iterations':P,
            'successive_difference_lower_bounds_pi':gains,
            'state_moments_power_basis':[[V.decode(z) for z in row] for row in high],
            'CM_chart_moments':charts,'CM_positive_nonzero_entries':nonzero,
            'anchor_positive_nonzero_entries':anchor,'D113_overlap_checked':True,
            'actual_coarse_differential_coefficients_computed':False,
            'sources':[source(p) for p in [Path(__file__),Path(old.__file__),
              DATA/'dyadic_moment_transports_d113.json',DATA/'dyadic_harmonic_certificate_d111.json',
              DATA/'dyadic_moment_pilot_d113.json']]}

def main():
    out=DATA/'dyadic_moment_extension_d114.json';assert not out.exists()
    result=calculations();out.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS|414_DYADIC_MOMENT_EXTENSION',flush=True)

if __name__=='__main__':main()
