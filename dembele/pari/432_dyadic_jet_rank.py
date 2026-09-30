"""D116: certify a Q2 rank lower bound from the actual degree-16-place jets."""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('series',ROOT/'dembele/pari/430_dyadic_ratio_series_review.py')
series=importlib.util.module_from_spec(s);s.loader.exec_module(series)
f=series.f
INF=10**9

def val(x):
    if not x:return INF
    n,d=abs(x.numerator),x.denominator
    return (n&-n).bit_length()-(d&-d).bit_length()

class Ball:
    def __init__(self,x=0,e=INF):
        x=Q(x);v=val(x);self.e=e
        if v>=e:self.x=Q(0);self.v=INF;return
        if e==INF:self.x=x;self.v=v;return
        unit=x/Q(2)**v;mod=2**(e-v)
        self.x=Q((unit.numerator*pow(unit.denominator,-1,mod))%mod)*Q(2)**v
        self.v=v
    def low(self):return min(self.v,self.e)
    def __add__(self,b):return Ball(self.x+b.x,min(self.e,b.e))
    def __neg__(self):return Ball(-self.x,self.e)
    def __sub__(self,b):return self+(-b)
    def __mul__(self,b):return Ball(self.x*b.x,min(self.e+b.low(),b.e+self.low()))
    def inverse(self):
        assert self.v<self.e
        return Ball(1/self.x,self.e-2*self.v)
    def saved(self):return [str(self.x),self.e]

def coefficients(ball):
    """In the Eisenstein basis, v_beta(sum c_i beta^i)=min(16*v2(c_i)+i)."""
    cs=list(map(Q,ball.u));v=ball.v if ball.u!=f.Z else 0
    while v>0:
        c=cs[-1];cs=[Q(0)]+cs[:-1]
        cs=[a-c*b for a,b in zip(cs,f.coarse.MP[:-1])];v-=1
    while v<0:
        c=-cs[0]/f.coarse.MP[0]
        cs=[(cs[i+1] if i<15 else Q(0))+c*f.coarse.MP[i+1] for i in range(16)];v+=1
    return [Ball(c,-((i-ball.error)//16)) for i,c in enumerate(cs)]

def actual_matrix():
    packet=json.loads((DATA/'dyadic_comparison200_d115.json').read_text())
    root=json.loads((DATA/'dyadic_cm_matching_review_d112.json').read_text())['certificates']['roots_and_frame']
    eta=[f.center(cs,root['rational_residue_frame_error_beta']) for cs in root['rational_residue_frame_values'][1]]
    r0=[a/eta[0] for a in eta]
    orders=packet['comparisons'][1]['orders']
    r1,r2=[[series.restore(x) for x in order['actual']] for order in orders]
    pairs=[(i,j) for i in range(16) for j in range(i,16)]
    rows=[[] for _ in range(48)]
    for i,j in pairs:
        jets=[r0[i]*r0[j],r0[i]*r1[j]+r1[i]*r0[j],r0[i]*r2[j]+r1[i]*r1[j]+r2[i]*r0[j]]
        for n,jet in enumerate(jets):
            for k,x in enumerate(coefficients(jet)):rows[16*n+k].append(x)
    return rows,pairs

def rank_certificate(matrix):
    a=[row[:] for row in matrix];m,n=len(a),len(a[0]);rr=list(range(m));cc=list(range(n));pivots=[]
    for k in range(min(m,n)):
        candidates=[(x.v,-(x.e-x.v),i,j) for i in range(k,m) for j in range(k,n)
                    if (x:=a[i][j]).v<x.e]
        if not candidates:break
        _,_,i,j=min(candidates)
        a[k],a[i]=a[i],a[k];rr[k],rr[i]=rr[i],rr[k]
        for row in a:row[k],row[j]=row[j],row[k]
        cc[k],cc[j]=cc[j],cc[k]
        pivot=a[k][k];pivots.append({'row':rr[k],'column':cc[k],'valuation':pivot.v,'error':pivot.e})
        inverse=pivot.inverse()
        for i in range(k+1,m):
            ratio=a[i][k]*inverse
            a[i][k]=Ball()
            for j in range(k+1,n):a[i][j]=a[i][j]-ratio*a[k][j]
    return {'rank_lower_bound':len(pivots),'pivots':pivots,
            'unused_rows':rr[len(pivots):],'unused_columns':cc[len(pivots):]}

def build():
    # Negative powers and boundary precision are tested in the full Eisenstein quotient.
    for exponent in [-19,-1,0,1,15,16,33]:
        x=f.BETA**exponent;cs=coefficients(x)
        reconstructed=f.Ball()
        for i,c in enumerate(cs):reconstructed=reconstructed+f.rational(c.x)*(f.BETA**i)
        assert not (x-reconstructed).known_nonzero()
    a,pairs=actual_matrix();certificate=rank_certificate(a)
    print('ACTUAL_J3_RANK|'+str(certificate['rank_lower_bound']),flush=True)
    return {'status':'pass','milestone':'D116','CM_index':1,
      'local_degree':16,'matrix_shape':[48,136],'monomial_pairs':pairs,
      'matrix_Q2_balls':[[x.saved() for x in row] for row in a],
      'certificate':certificate,'actual_J3_rank_45_certified':certificate['rank_lower_bound']==45,
      'candidate_identification_proved':False,'sources':[f.coarse.source(p) for p in [
        Path(__file__),Path(series.__file__),Path(f.__file__),DATA/'dyadic_comparison200_d115.json',
        DATA/'dyadic_cm_matching_review_d112.json']]}

if __name__=='__main__':
    result=build();out=DATA/'dyadic_jet_rank_d116.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|432_DYADIC_JET_RANK',flush=True)
