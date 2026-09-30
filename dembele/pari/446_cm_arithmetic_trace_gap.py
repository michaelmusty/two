"""D117: an exact trace-lattice gap for arithmetic CM displacements.

The search is in the eight-dimensional integer ring of Q(zeta_32)^+,
not a quaternion-group or class census. The geometric implication is
proved in the companion report. All root and trace comparisons are exact.
"""
from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
FP=[2,0,-16,0,20,0,-8,0,1]

def source(p):
    p=Path(p).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a

def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def scale(a,c):return trim([c*x for x in a])

def remainder(a,b):
    a=list(map(Q,a));b=list(map(Q,b))
    while len(a)>=len(b) and any(a):
        shift=len(a)-len(b);c=a[-1]/b[-1]
        for i,x in enumerate(b):a[i+shift]-=c*x
        a=trim(a)
    return a

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return remainder(c,FP)

def eval_poly(p,x):
    y=0
    for c in reversed(p):y=y*x+c
    return y

def sturm_roots(bits=72):
    sequence=[list(map(Q,FP)),[Q(i)*FP[i] for i in range(1,9)]]
    while len(sequence[-1])>1:sequence.append(scale(remainder(sequence[-2],sequence[-1]),-1))
    def variations(x):
        signs=[(v>0)-(v<0) for p in sequence if (v:=eval_poly(p,x))]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    pending=[(Q(-2),Q(2))];roots=[]
    while pending:
        a,b=pending.pop();n=variations(a)-variations(b)
        if not n:continue
        if n==1 and b-a<=Q(1,2**bits):roots.append((a,b));continue
        mid=(a+b)/2;assert eval_poly(FP,mid)!=0
        pending.extend([(a,mid),(mid,b)])
    roots.sort();assert len(roots)==8
    assert all(variations(a)-variations(b)==1 for a,b in roots)
    return roots

def interval_mul(a,b):
    values=[x*y for x in a for y in b];return min(values),max(values)

def interval_poly(p,x):
    out=(Q(0),Q(0))
    for c in reversed(p):
        a,b=interval_mul(out,x);out=(a+c,b+c)
    return out

def trace(a):
    return sum((p[i] if i<len(p) else 0) for i in range(8)
               for p in [mul(a,[0]*i+[1])])

def trace_basis():
    cheb=[[2],[0,1]]
    for k in range(2,8):cheb.append(add([0]+cheb[-1],scale(cheb[-2],-1)))
    basis=[[1]]+cheb[1:]
    gram=[[trace(mul(a,b)) for b in basis] for a in basis]
    assert gram==[[Q((8 if i==0 else 16)*(i==j)) for j in range(8)] for i in range(8)]
    # Monic triangular change from 1,b,...,b^7; determinant one.
    assert all(len(p)==i+1 and p[-1]==1 for i,p in enumerate(basis))
    assert 8*16**7==2**31
    return basis,[[int(x) for x in row] for row in gram]

def vectors(bound):
    def tail(prefix,left):
        if len(prefix)==8:yield prefix;return
        for a in range(-isqrt(left//2),isqrt(left//2)+1):
            yield from tail(prefix+[a],left-2*a*a)
    for a in range(-isqrt(bound),isqrt(bound)+1):yield from tail([a],bound-a*a)

def build():
    basis,gram=trace_basis();roots=sturm_roots();shift=96;unit=2**shift
    intervals=[]
    for root in roots:
        row=[]
        for polynomial in basis:
            a,b=interval_poly(polynomial,root)
            row.append(((a*unit).__floor__(),(b*unit).__ceil__()))
        intervals.append(row)
    cap=8;bound=(cap*cap+7*4)//8;assert bound==11
    count=0;eligible=[]
    for a in vectors(bound):
        count+=1
        if not any(a[1:]):continue
        values=[]
        for row in intervals:
            lo=sum(c*(x if c>=0 else y) for c,(x,y) in zip(a,row))
            hi=sum(c*(y if c>=0 else x) for c,(x,y) in zip(a,row))
            # A nonconstant field element cannot have a conjugate exactly +/-2.
            assert not lo<=2*unit<=hi and not lo<=-2*unit<=hi
            values.append((lo,hi))
        outside=[i for i,(lo,hi) in enumerate(values) if lo>2*unit or hi< -2*unit]
        if len(outside)!=1:continue
        i=outside[0];lo,hi=values[i]
        if lo<=2*unit:continue
        eligible.append({'coefficients_in_trace_basis':a,'outlier_embedding_index':i,
                         'outlier_interval':[str(Q(lo,unit)),str(Q(hi,unit))]})
    eligible.sort(key=lambda row:Q(row['outlier_interval'][0]))
    lower=min([Q(cap)]+[Q(row['outlier_interval'][0]) for row in eligible])
    choices=[]
    for rho in [Q(1,4),Q(1,3),Q(3,8),Q(2,5),Q(5,12),Q(3,7),Q(4,9),Q(1,2)]:
        required=2*(1+6*rho*rho+rho**4)/(1-rho*rho)**2
        choices.append({'disk_radius':str(rho),'trace_required_for_disjoint_translates':str(required),
                        'certified':required<lower})
    assert any(x['certified'] for x in choices)
    print('TRACE_GAP|'+json.dumps({'vectors':count,'eligible':len(eligible),'trace_lower':str(lower),'radii':choices}),flush=True)
    return {'status':'pass','milestone':'D117','field_polynomial_ascending':FP,
       'trace_basis_polynomials':basis,'trace_Gram_matrix':gram,'field_discriminant':2**31,
       'real_root_intervals':[[str(a),str(b)] for a,b in roots],
       'trace_search_upper':cap,'weighted_integer_norm_bound':bound,'vectors_enumerated':count,
       'eligible_single_positive_outlier_elements':eligible,'uniform_hyperbolic_trace_lower':str(lower),
       'disk_radius_tests':choices,'geometric_displacement_implication_in_companion_proof':True,
       'actual_CM_minimum_displacement_computed':False,'candidate_identification_proved':False,
       'target_field_polynomial_constructed':False,'sources':[source(p) for p in [Path(__file__),
          ROOT/'dembele/certificates/cm-adjugate-height-d103.md',
          ROOT/'dembele/data/computed/cm_intrinsic_height_d104.json',
          ROOT/'dembele/data/computed/cm_arithmetic_identification_review_d116.json']]}

if __name__=='__main__':
    result=build();out=DATA/'cm_arithmetic_trace_gap_d117.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|446_CM_ARITHMETIC_TRACE_GAP',flush=True)
