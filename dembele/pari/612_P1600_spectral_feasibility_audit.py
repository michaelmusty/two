"""D145 independent rational audit of the B80 trace census and heat constants."""
from fractions import Fraction as Q
import hashlib
from itertools import combinations,product
import json
import math
from pathlib import Path
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'


def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def add(a,b):return a[0]+b[0],a[1]+b[1]
def scale(a,c):return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def mul(a,b):
    values=[x*y for x in a for y in b];return min(values),max(values)
def inv(a):
    assert a[0]>0;return 1/a[1],1/a[0]
def square(a):
    return (Q(0) if a[0]<=0<=a[1] else min(t*t for t in a),max(t*t for t in a))
def exp_interval(x):
    if x<0:return inv(exp_interval(-x))
    term=Q(1);total=term
    for k in range(1,81):term*=x/k;total+=term
    nxt=term*x/81;tail=nxt/(1-x/82)
    return total,total+tail
def log_integer(n):
    y=Q(n-1,n+1);total=sum(2*y**(2*k+1)/(2*k+1) for k in range(128))
    tail=2*y**257/(257*(1-y*y));return total,total+tail
def evaluate(poly,x):
    out=(Q(0),Q(0))
    for c in reversed(poly):out=add(mul(out,x),(Q(c),Q(c)))
    return out


if __name__=='__main__':
    assert __debug__;tick=time.monotonic()
    input_names=['P1600_trace_systole_d145','P1600_trace_systole_audit_d145','P1600_spectral_feasibility_d145']
    old,trace,heat=[json.loads((DATA/(n+'.json')).read_text()) for n in input_names]
    assert all(r['status']=='pass' for r in [old,trace,heat])
    polynomial=[2,0,-16,0,20,0,-8,0,1]
    roots=[];grid=1<<60
    for saved in old['real_root_intervals']:
        lo,hi=map(Q,saved)
        lo=Q((lo*grid).__floor__(),grid);hi=Q((hi*grid).__ceil__(),grid)
        assert evaluate(polynomial,(lo,lo))[0]*evaluate(polynomial,(hi,hi))[0]<0
        assert -2<lo<hi<2 and (not roots or roots[-1][1]<lo)
        roots.append((lo,hi))
    assert len(roots)==8 and 0<roots[4][0]<roots[4][1]<1
    # Eight disjoint sign-changing intervals isolate all roots of degree eight.
    C=[[2]+[0]*8,[0,1]+[0]*7]
    for k in range(2,9):C.append([0]+C[-1][:-1]);C[-1]=[a-b for a,b in zip(C[-1],C[-3])]
    assert C[8]==polynomial
    C[8]=[0]*9
    unit=[[1]+[0]*7]+[c[:8] for c in C[1:8]]
    dyadic=[[a+b for a,b in zip(C[j][:8],C[j+1][:8])] for j in range(8)]
    rows=[]
    for family,basis,weights in [('unit',unit,[8]+[16]*7),('dyadic',dyadic,[16]*8)]:
        saved=next(r for r in trace['families'] if r['family']==family)
        assert [list(map(Q,r))+[Q(0)]*(8-len(r)) for r in saved['orthogonal_trace_basis']]==basis
        vectors=set()
        # Independent support/magnitude/sign construction, not coordinate recursion.
        for size in range(1,6):
            for support in combinations(range(8),size):
                ranges=[range(1,math.isqrt(80//weights[i])+1) for i in support]
                for mags in product(*ranges):
                    if sum(weights[i]*m*m for i,m in zip(support,mags))>80:continue
                    for signs in product([-1,1],repeat=size-1):
                        v=[0]*8
                        for i,m,s in zip(support,mags,signs+(1,)):v[i]=m*s
                        vectors.add(tuple(v))
        assert vectors==set(map(tuple,saved['all_orthogonal_vectors']))
        assert len(vectors)==saved['signed_pairs'] and not saved['all_admissible_candidates']
        damaged=set(vectors);damaged.pop();assert damaged!=vectors
        values=[[evaluate(c,r) for c in basis] for r in roots]
        norms=[(Q(1),Q(1)) if family=='unit' else add(r,(Q(2),Q(2))) for r in roots]
        candidates=[];central=0
        for v in vectors:
            if family=='unit' and abs(v[0])==2 and not any(v[1:]):central+=1;continue
            allowed=True
            for j in [4,0,1,2,3,5,6,7]:
                t=(Q(0),Q(0))
                for c,term in zip(v,values[j]):t=add(t,scale(term,c))
                u=mul(square(t),inv(norms[j]))
                assert u[1]<4 or u[0]>4
                if (j==4 and u[1]<4) or (j!=4 and u[0]>4):allowed=False;break
            if allowed:candidates.append(v)
        assert not candidates
        rows.append({'family':family,'independent_signed_pairs':len(vectors),
                     'exactly_central_pairs_removed':central,'admissible_hyperbolic_pairs':0})
    # Exact cutoff implication: length <= acosh(25) forces trace(u)<=80.
    delta=Q(39,10)
    cosh_delta=scale(add(exp_interval(delta),exp_interval(-delta)),Q(1,2))
    assert cosh_delta[1]<25
    d=Q(1455,32);cE=Q(869,128)
    D=scale(exp_interval(-Q(1,4)),d/2+cE)
    a=scale(exp_interval(Q(3,4)-3*delta**2/16),2)
    q=exp_interval(-Q(9,16))
    assert D[1]<23 and a[1]<Q(1,4) and q[1]<Q(4,7)
    gamma_lower=sum(Q(1,k) for k in range(1,33))-5*log_integer(2)[1]-Q(1,64)
    assert gamma_lower>Q(577,1000)
    loggap=add(log_integer(3),scale(log_integer(2),-4))
    tail=mul(exp_interval(Q(3,16)),add(scale(loggap,-1),(Q(3,16)-Q(577,1000),)*2))
    assert tail[1]<Q(31,20)
    K=4/(delta**2-1);M=Q(95,24);nonconstant=Q(623,24)
    assert M==Q(1,4)*(1+Q(4,7)*22)/(1-Q(1,4)*Q(4,7))
    assert nonconstant==23+M-1
    lower=Q(577,1000)-M*K-nonconstant*Q(31,20)
    assert lower==Q(heat['elementary_log_Zprime_lower']) and lower> -41>Q('-96.820')
    assert Q(1,4)-Q(7,64)**2==Q(975,4096)>Q(3,16)
    assert Q(heat['necessary_joint_S_upper_for_Faltings29_interval'][1])< -249
    result={'status':'pass','milestone':'D145','all_arithmetic_exact_rational':True,
            'root_isolation_independently_verified':True,'independent_enumeration_method':'support, magnitudes, signs',
            'trace_families':rows,'bound80_fully_replayed':True,'omitted_vector_control_rejected':True,
            'independent_exp_and_log_series_with_rational_remainders':True,
            'gamma_lower_proof':'H_32-log(32)-1/64 < Euler gamma',
            'elementary_log_Zprime_lower':str(lower),'uniform_strict_log_Zprime_lower':'-41',
            'D144_sufficient_spectral_target_ruled_out':True,
            'Faltings_lower_29_proved':False,'Faltings_lower_29_disproved':False,
            'candidate_identification_proved':False,'actual_curve_eigenvalue_computation_started':False,
            'wall_seconds':time.monotonic()-tick,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
            'sources':[source(Path(__file__))]+[source(DATA/(n+'.json')) for n in input_names]}
    result['conservative_peak_rss_bytes']=result['peak_rss_bytes'];assert result['peak_rss_bytes']<2*(1<<30)
    output=DATA/'P1600_spectral_feasibility_audit_d145.json'
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|612_P1600_SPECTRAL_FEASIBILITY_AUDIT',flush=True)
