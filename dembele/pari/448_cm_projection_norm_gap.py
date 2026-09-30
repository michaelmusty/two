"""D117: sharpen CM displacement using the integral CM projection lattice.

For alpha of norm one, x=alpha+beta*alpha*beta^-1 lies in O_M.
Its squared complex absolute values are at most four at the compact
places and equal 4*cosh(distance/2)^2 at the split place.
"""
from fractions import Fraction as Q
import importlib.util
import json
from math import isqrt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('trace_gap',ROOT/'dembele/pari/446_cm_arithmetic_trace_gap.py')
t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
MP=[2,0,64,0,336,0,672,0,660,0,352,0,104,0,16,0,1]

def polys():
    recurrence=[[2],[0,1]]
    for k in range(2,17):recurrence.append(t.add([0]+recurrence[-1],recurrence[-2]))
    assert recurrence[16]==MP
    basis=[[1]]+recurrence[1:16]
    traces=[16]
    for k in range(1,31):
        if k<=16:
            traces.append(-sum(MP[16-j]*traces[k-j] for j in range(1,k))-k*MP[16-k])
        else:traces.append(-sum(MP[16-j]*traces[k-j] for j in range(1,17)))
    gram=[[sum(x*y*(-1)**j*traces[i+j] for i,x in enumerate(a) for j,y in enumerate(b)) for b in basis] for a in basis]
    assert gram==[[(16 if i==0 else 32)*(i==j) for j in range(16)] for i in range(16)]
    assert 16*32**15==2**79
    parts=[]
    for k,p in enumerate(basis):
        assert all(c==0 for i,c in enumerate(p) if i%2!=k%2)
        part=[0]
        for c in reversed(p[k%2::2]):
            part=t.add(t.add(t.scale(part,-2),[0]+t.scale(part,-1)),[c])
        parts.append(part)
    return basis,gram,parts

def vectors(bound):
    def tail(prefix,left):
        if len(prefix)==16:yield prefix;return
        for a in range(-isqrt(left//2),isqrt(left//2)+1):yield from tail(prefix+[a],left-2*a*a)
    for a in range(-isqrt(bound),isqrt(bound)+1):yield from tail([a],bound-a*a)

def square(a,b):
    return (0 if a<=0<=b else min(a*a,b*b)),max(a*a,b*b)

def build():
    prior=json.loads((DATA/'cm_arithmetic_trace_gap_d117.json').read_text())
    roots=[tuple(map(Q,row)) for row in prior['real_root_intervals']]
    basis,gram,parts=polys();unit=2**96;normunit=unit**3
    embeddings=[]
    for a,b in roots:
        values=[]
        for polynomial in parts:
            lo,hi=t.interval_poly(polynomial,(a,b));values.append(((lo*unit).__floor__(),(hi*unit).__ceil__()))
        embeddings.append((values,((a+2)*unit).__floor__(),((b+2)*unit).__ceil__()))
    cap=64;bound=(28+cap)//8;assert bound==11
    count=0;eligible=[];boundary=[]
    for coefficients in vectors(bound):
        count+=1;active=[(j,c) for j,c in enumerate(coefficients) if c]
        outliers=[];values=[];ambiguous=False
        for ei,(entries,blo,bhi) in enumerate(embeddings):
            real=[0,0];imag=[0,0]
            for j,c in active:
                lo,hi=entries[j]
                if c<0:lo,hi=hi,lo
                target=imag if j%2 else real;target[0]+=c*lo;target[1]+=c*hi
            rlo,rhi=square(*real);ilo,ihi=square(*imag)
            lo=rlo*unit+blo*ilo;hi=rhi*unit+bhi*ihi
            assert 0<=lo<=hi
            if lo<=4*normunit<=hi:
                ambiguous=True;break
            values.append((lo,hi))
            if lo>4*normunit:outliers.append(ei)
            if len(outliers)>1:break
        if ambiguous:
            # Independently reduce x*conjugate(x); constant norm four is
            # harmless, whereas an unresolved nonconstant boundary is rejected.
            x=[0]
            for j,c in active:x=t.add(x,t.scale(basis[j],c))
            product=[0]*(2*len(x)-1)
            for i,a in enumerate(x):
                for j,b in enumerate(x):product[i+j]+=a*b*(-1)**j
            norm=t.remainder(product,MP);assert norm==[4]
            boundary.append(coefficients);continue
        if len(outliers)!=1 or len(values)!=8:continue
        ei=outliers[0];lo,hi=values[ei]
        eligible.append({'coefficients_in_CM_trace_basis':coefficients,'outlier_embedding_index':ei,
                         'squared_absolute_value_interval':[str(Q(lo,normunit)),str(Q(hi,normunit))]})
    eligible.sort(key=lambda row:Q(row['squared_absolute_value_interval'][0]))
    lower=min([Q(cap)]+[Q(row['squared_absolute_value_interval'][0]) for row in eligible])
    tests=[]
    for rho in [Q(1,2),Q(3,5),Q(2,3),Q(7,10),Q(3,4),Q(4,5)]:
        required=4*(1+rho*rho)**2/(1-rho*rho)**2
        tests.append({'disk_radius':str(rho),'required_projection_norm':str(required),'certified':required<lower})
    print('CM_PROJECTION_GAP|'+json.dumps({'vectors':count,'eligible':len(eligible),'norm_lower':str(lower),'radii':tests}),flush=True)
    return {'status':'pass','milestone':'D117','CM_polynomial_ascending':MP,
       'CM_trace_basis_polynomials':basis,'Hermitian_trace_Gram_matrix':gram,
       'CM_discriminant':2**79,'real_root_intervals':prior['real_root_intervals'],
       'squared_absolute_value_search_upper':cap,'weighted_integer_norm_bound':bound,
       'vectors_enumerated':count,'constant_norm_four_vectors':boundary,
       'eligible_single_outlier_elements':eligible,'uniform_moving_projection_squared_norm_lower':str(lower),
       'disk_radius_tests':tests,'projection_and_geometric_implication_in_companion_proof':True,
       'quaternion_integrality_sufficiency_claimed':False,'candidate_identification_proved':False,
       'target_field_polynomial_constructed':False,'sources':[t.source(p) for p in [Path(__file__),Path(t.__file__),
           DATA/'cm_arithmetic_trace_gap_d117.json',DATA/'cm_intrinsic_height_d104.json',
           ROOT/'dembele/certificates/cm-frame-arithmetic-d105.md']]}

if __name__=='__main__':
    result=build();out=DATA/'cm_projection_norm_gap_d117.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|448_CM_PROJECTION_NORM_GAP',flush=True)
