"""D116: complementary-minor cancellation and sharper actual jet height bounds."""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'

def source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def det(a):
    if not a:return 1
    a=[list(map(Q,row)) for row in a];value=Q(1)
    for k in range(len(a)):
        i=next((i for i in range(k,len(a)) if a[i][k]),None)
        if i is None:return 0
        if i!=k:a[k],a[i]=a[i],a[k];value=-value
        pivot=a[k][k];value*=pivot
        for i in range(k+1,len(a)):
            ratio=a[i][k]/pivot
            for j in range(k+1,len(a)):a[i][j]-=ratio*a[k][j]
    assert value.denominator==1;return value.numerator

def minor(a,I,J):return det([[a[i][j] for j in J] for i in I])

def adj(a):
    n=len(a)
    return [[(-1)**(i+j)*minor(a,[x for x in range(n) if x!=j],
                                  [x for x in range(n) if x!=i]) for j in range(n)] for i in range(n)]

def controls():
    count=0;dets=[]
    for n in range(3,7):
        base=[[((i+2)*(j+3)+i*j*j)%11-5+(29 if i==j else 0) for j in range(n)] for i in range(n)]
        for singular in [False,True]:
            a=[[2**i*x for x in row] for i,row in enumerate(base)]
            if singular:a[-1]=a[0][:]
            d=det(a);dets.append(d);ad=adj(a)
            assert (d==0)==singular
            for k in range(1,4):
                sets=list(combinations(range(n),k))
                for I in sets:
                    for J in sets:
                        complement=(-1)**(sum(I)+sum(J))*minor(a,[x for x in range(n) if x not in J],
                                                                              [x for x in range(n) if x not in I])
                        assert minor(ad,I,J)==d**(k-1)*complement
                        count+=1
    # B=G*H'-H*G'=f*Wr(f,a,b); all values are independent formal derivatives.
    wronskians=0
    for seed in range(1,21):
        rows=[[((seed+3)*(i+2)*(j+1)+i+2*j)%19-9 for j in range(3)] for i in range(3)]
        f,a,b=rows[0];fp,ap,bp=rows[1];fpp,app,bpp=rows[2]
        G=f*ap-a*fp;H=f*bp-b*fp
        Gp=f*app-a*fpp;Hp=f*bpp-b*fpp
        assert G*Hp-H*Gp==f*det(rows);wronskians+=1
    # A diagonal nonunit example rejects one extra cancellation factor.
    a=[[0]*4 for _ in range(4)]
    for i,x in enumerate([2,3,5,7]):a[i][i]=x
    assert minor(adj(a),(0,1),(0,1))==det(a)*35
    assert minor(adj(a),(0,1),(0,1))!=det(a)**2*35
    return {'complementary_minor_identities_checked':count,'matrix_determinants':dets,
            'singular_and_nonunit_controls':True,'Wronskian_identities_checked':wronskians,
            'extra_determinant_cancellation_rejected':True}

def budgets():
    x=Q(1,3);n=64
    lo=2*sum(x**(2*k+1)/Q(2*k+1) for k in range(n))
    hi=lo+2*x**(2*n+1)/(Q(2*n+1)*(1-x*x))
    g=16;H=Q(41,10);B=20;V=35
    norm_exponents=[]
    for k,rounding in [(1,4),(2,8),(3,11)]:
        assert comb(g,k)*g**k<=2**(2*rounding)
        norm_exponents.append((g-k)*(g+1)*B+k*V+rounding)
    assert norm_exponents==[5139,4838,4536]
    gaussian=norm_exponents[1]+60
    fvalue=norm_exponents[0]+20
    wronskian=norm_exponents[2]+120
    delta=g*(g+1)*B
    numerator=3*fvalue+wronskian
    denominator=1+delta+3*gaussian
    assert [gaussian,fvalue,wronskian,delta,numerator,denominator]==[4898,5159,4656,5440,20133,20135]
    line_coefficients=[(3+(g-2)*(g+1),g-1),(9+(4*g-6)*(g+1),4*g-2)]
    assert line_coefficients==[(241,15),(995,62)]
    rows=[]
    for order,((hcoeff,fcoeff),norm,candidate) in enumerate(zip(line_coefficients,[gaussian,max(numerator,denominator)],[677,1947]),1):
        alpha=hcoeff*H;beta=norm+48*fcoeff
        actual_lo=alpha+beta*lo;actual_hi=alpha+beta*hi
        ceiling=actual_hi.numerator//actual_hi.denominator+1
        assert ceiling-1<actual_lo<actual_hi<ceiling
        row={'order':order,'coefficient_of_H_CM':hcoeff,'negative_coefficient_of_h_Fal':fcoeff,
             'section_norm_binary_exponent':norm,'actual_height_bound_alpha':str(alpha),
             'actual_height_bound_beta_log2':beta,'actual_height_strict_integer_upper':ceiling,
             'candidate_height_upper':candidate,'difference_height_bound_alpha':str(alpha+candidate),
             'difference_height_bound_beta_log2':beta+1}
        for name,m in [('rational_anchor_only',272),('degree16_place_only',17),('both_places_uniform_beta_error',16)]:
            low=m*(beta+1)+m*(alpha+candidate)/hi
            high=m*(beta+1)+m*(alpha+candidate)/lo
            threshold=high.numerator//high.denominator+1
            assert threshold-1<low<high<threshold
            row[name]={'sufficient_beta_error':threshold,'sufficient_integer_pi_error':(threshold+1)//2}
        rows.append(row)
    return {'log2_lower':str(lo),'log2_upper':str(hi),
      'reduced_exterior_section_norm_exponents':norm_exponents,
      'Gaussian_value_exponent':gaussian,'first_section_value_exponent':fvalue,
      'third_Wronskian_exponent':wronskian,'frame_determinant_exponent':delta,
      'second_ratio_numerator_denominator_exponents':[numerator,denominator],
      'thresholds':rows,'bounds_are_sufficient_not_necessary':True}

def build():
    control=controls();budget=budgets()
    return {'status':'pass','milestone':'D116','controls':control,'height_budgets':budget,
      'common_determinant_factors_removed_by_integral_polynomial_identities':True,
      'actual_precision_increased':False,'candidate_identification_proved':False,
      'target_field_polynomial_constructed':False,'sources':[source(p) for p in [Path(__file__),
        ROOT/'dembele/certificates/cm-adjugate-height-d103.md',
        ROOT/'dembele/certificates/cm-intrinsic-height-d104.md',
        ROOT/'dembele/certificates/cm-rational-frame-jets-d106.md',
        DATA/'cm_ratio_jet_review_d106.json',DATA/'dyadic_strategy_review_d115.json']]}

if __name__=='__main__':
    result=build();out=DATA/'cm_compound_height_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['height_budgets']['thresholds'],indent=2),flush=True)
    print('PASS|433_CM_COMPOUND_HEIGHT',flush=True)
