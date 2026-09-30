"""D115: local balls at 448 beta digits, the CM frame, and two ratio orders.

Every division requires a certified nonzero denominator. Absolute beta-adic
errors propagate through all operations. Insufficient precision is an output,
not an equality or a claimed zero. Candidate coefficients enter only at the
final comparison, after construction of the actual rational residue frame.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('coarse',ROOT/'dembele/pari/415_dyadic_coarse_poisson.py')
coarse=importlib.util.module_from_spec(s);s.loader.exec_module(coarse)
R=coarse.CMring(448);Z=coarse.ZERO;O=coarse.ONE;INF=10**9

@lru_cache(None)
def beta_power(n):
    assert n>=0
    if n>=448:return Z
    z=O
    for _ in range(n):z=R.mul(z,coarse.BETA)
    return z

def divide_beta(x,n):
    for _ in range(n):
        assert x[0]%2==0
        c=x[0]//2
        x=R.normalize([(x[i+1] if i<15 else 0)-c*coarse.MP[i+1] for i in range(16)])
    return x

@lru_cache(maxsize=65536)
def unit_inverse(u):
    assert R.val(u)==0
    z=O
    for _ in range(9):z=R.mul(z,R.add(R.scale(O,2),R.scale(R.mul(u,z),-1)))
    assert R.mul(u,z)==O
    return z

class Ball:
    def __init__(self,u=Z,v=0,error=INF):
        u=R.normalize(u)
        if u==Z:self.u=Z;self.v=INF;self.error=error;return
        error=min(error,v+448);w=R.val(u)
        if v+w>=error:self.u=Z;self.v=INF;self.error=error;return
        self.u=divide_beta(u,w);self.v=v+w;self.error=error
    def known_nonzero(self):return self.v<self.error
    def lower(self):return min(self.v,self.error)
    def __neg__(self):return Ball(R.scale(self.u,-1),self.v if self.u!=Z else 0,self.error)
    def __add__(self,b):
        error=min(self.error,b.error)
        if self.u==Z:return Ball(b.u,b.v if b.u!=Z else 0,error)
        if b.u==Z:return Ball(self.u,self.v,error)
        v=min(self.v,b.v)
        u=R.add(R.mul(self.u,beta_power(self.v-v)),R.mul(b.u,beta_power(b.v-v)))
        return Ball(u,v,min(error,v+448))
    def __sub__(self,b):return self+(-b)
    def __mul__(self,b):
        error=min(self.error+b.lower(),b.error+self.lower())
        if self.u==Z or b.u==Z:return Ball(error=error)
        return Ball(R.mul(self.u,b.u),self.v+b.v,error)
    def inverse(self):
        assert self.known_nonzero(),('unresolved division',self.summary())
        return Ball(unit_inverse(self.u),-self.v,self.error-2*self.v)
    def __truediv__(self,b):return self*b.inverse()
    def __pow__(self,n):
        if n<0:return self.inverse()**(-n)
        z=Ball(O);x=self
        while n:
            if n&1:z=z*x
            x=x*x;n//=2
        return z
    def summary(self):return {'valuation_beta':self.v if self.known_nonzero() else None,'error_beta':self.error}
    def saved(self):return {'unit_beta':list(self.u),'beta_exponent':self.v if self.u!=Z else None,'error_beta':self.error}

ONE=Ball(O);TWO=Ball(R.scale(O,2));BETA=Ball(coarse.BETA)

def rational(q):
    q=Fraction(q)
    if not q:return Ball()
    n,d=q.numerator,q.denominator
    a=(abs(n)&-abs(n)).bit_length()-1;b=(d&-d).bit_length()-1
    u=R.scale(O,(n>>a)*pow(d>>b,-1,R.maximum))
    return Ball(u)*(TWO**(a-b))

def center(cs,error):
    z=Ball()
    for i,c in enumerate(cs):
        if Fraction(c):z=z+rational(c)*(BETA**i)
    return Ball(z.u,z.v if z.u!=Z else 0,min(z.error,error))

def dot(x,y):
    z=Ball()
    for a,b in zip(x,y):z=z+a*b
    return z

def multiply(a,b):return [[dot(row,col) for col in zip(*b)] for row in a]

def inverse(a):
    n=len(a);m=[row[:]+[ONE if i==j else Ball() for j in range(n)] for i,row in enumerate(a)]
    pivots=[]
    for k in range(n):
        candidates=[(m[i][k].v,i) for i in range(k,n) if m[i][k].known_nonzero()]
        if not candidates:return None,pivots,{'unresolved_column':k,'entries':[m[i][k].summary() for i in range(k,n)]}
        _,i=min(candidates);m[k],m[i]=m[i],m[k]
        pivot=m[k][k];pivots.append(pivot.summary());ip=pivot.inverse()
        m[k]=[x*ip for x in m[k]]
        for i in range(n):
            if i==k:continue
            c=m[i][k]
            m[i]=[x-c*y for x,y in zip(m[i],m[k])]
    inv=[row[n:] for row in m]
    residual=multiply(a,inv)
    assert all(not (x-(ONE if i==j else Ball())).known_nonzero() for i,row in enumerate(residual) for j,x in enumerate(row))
    return inv,pivots,None

def controls():
    for q in ['-3/8','7/16','4/3','17/9']:
        x=rational(q);assert not (x*x.inverse()-ONE).known_nonzero()
    x=center([0,0,2,1]+[0]*12,70)
    y=center([4,1]+[0]*14,60)
    assert not ((x/y)*y-x).known_nonzero()
    a=[[rational(2),ONE],[ONE,rational(4)]];ai,_,failed=inverse(a);assert failed is None
    assert not (ai[0][0]-rational('4/7')).known_nonzero()
    assert not (ai[0][1]-rational('-1/7')).known_nonzero()
    # An unknown ball may never become an invertible zero by normalization.
    assert not Ball(R.scale(O,4),0,32).known_nonzero()
    # f=1+u, a/f=2+3u+5u^2, b/f=7+11u+13u^2.
    # Reversion of t=3u+5u^2 gives b/f=7+(11/3)t-(16/27)t^2.
    f,a,b=map(rational,[1,2,7]);f1,a1,b1=map(rational,[1,5,18])
    f2,a2,b2=map(rational,[0,8,24])
    G=f*a1-a*f1;H=f*b1-b*f1
    second=f*f*(G*(f*b2-b*f2)-H*(f*a2-a*f2))/(G**3)
    assert not (second-rational('-16/27')).known_nonzero()

def calculations(path):
    controls();packet=json.loads(path.read_text())
    refpath=DATA/'dyadic_cm_matching_review_d112.json'
    frame=json.loads(refpath.read_text())['certificates']['roots_and_frame']
    errors=packet['coarse_error_beta']
    jets=[[[center(cs,errors[j]) for cs in row['coarse_coefficients_beta'][j]] for j in range(3)] for row in packet['CM_values']]
    result={'status':'pass','milestone':'D115','input_precision_pi':packet['working_precision_pi'],
            'anchor_nonvanishing_certified':any(x.known_nonzero() for x in jets[0][0]),
            'frame_computed':False,'candidate_identification_proved':False,'candidate_mismatch_certified':False}
    result['sources']=[coarse.source(x) for x in [Path(__file__),Path(coarse.__file__),path,refpath]]
    h=[];scales=[]
    for i,jet in enumerate(jets):
        good=[x.v for x in jet[0] if x.known_nonzero()]
        if not good:
            result['precision_obstruction']={'stage':'evaluation_row','CM_index':i};return result
        scale=BETA**min(good);scales.append(scale);h.append([x/scale for x in jet[0]])
    inv,pivots,failed=inverse(h[1:]);result['evaluation_pivots']=pivots
    if failed:result['precision_obstruction']={'stage':'evaluation_inverse',**failed};return result
    q=multiply([h[0]],inv)[0];result['frame_relation']=[x.saved() for x in q]
    if not all(x.known_nonzero() for x in q):
        result['precision_obstruction']={'stage':'frame_relation','entries':[x.summary() for x in q]};return result
    eta=[[center(cs,frame['rational_residue_frame_error_beta']) for cs in row] for row in frame['rational_residue_frame_values']]
    # q*H_nonanchor=H_W; sum eta_i=0, so these give the projective residue frame.
    weighted=[[x/q[i] for x in eta[i+1]] for i in range(16)]
    change=multiply(inv,weighted)
    actual=[multiply(jet,change) for jet in jets]
    for i in range(17):
        expected=[-x*scales[0] if i==0 else x*scales[i]/q[i-1] for x in eta[i]]
        assert all(not (x-y).known_nonzero() for x,y in zip(actual[i][0],expected))
    result['frame_computed']=True;result['change_of_basis']=[[x.saved() for x in row] for row in change]
    print('FRAME|all 17 residue rows enclosed; independent candidate data still unused',flush=True)
    candidate_path=DATA/'cm_ratio_jet_review_d106.json'
    candidate=json.loads(candidate_path.read_text())['candidate_comparison_packet']['candidate_ratio_Taylor_coefficients_orders_0_through_3']
    result['sources'].append(coarse.source(candidate_path))
    comparisons=[]
    for ci,jet in enumerate(actual):
        f=jet[0][0];gaussian=[f*jet[1][j]-jet[0][j]*jet[1][0] for j in range(16)]
        pivot=gaussian[1]
        if not pivot.known_nonzero():
            comparisons.append({'CM_index':ci,'pivot':pivot.summary(),'comparison_possible':False});continue
        tangent=[x/pivot for x in gaussian]
        second_difference=[f*jet[2][j]-jet[0][j]*jet[2][0] for j in range(16)]
        second=[f*f*(pivot*x-h*second_difference[1])/(pivot**3)
                for x,h in zip(second_difference,gaussian)]
        theta=eta[ci][0]+rational('2/17')
        orders=[]
        for n,actual_order in [(1,tangent),(2,second)]:
            expected=[]
            for cs in candidate[n]:
                v=Ball()
                for c in reversed(cs):v=v*theta+rational(c)
                expected.append(v)
            differences=[x-y for x,y in zip(actual_order,expected)]
            mismatches=[j for j,x in enumerate(differences) if x.known_nonzero()]
            orders.append({'order':n,'actual':[x.saved() for x in actual_order],
                 'candidate':[x.saved() for x in expected],'differences':[x.saved() for x in differences],
                 'minimum_error_beta':min(x.error for x in differences),'mismatch_coordinates':mismatches})
            result['candidate_mismatch_certified']|=bool(mismatches)
            print(f'COMPARISON|CM={ci}, order={n}, min beta error={min(x.error for x in differences)}, mismatches={mismatches}',flush=True)
        comparisons.append({'CM_index':ci,'comparison_possible':True,'pivot':pivot.summary(),'orders':orders})
    result['comparisons']=comparisons
    if not any(x['comparison_possible'] for x in comparisons):result['precision_obstruction']={'stage':'Gaussian_pivot'}
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args();assert not args.output.exists()
    result=calculations(args.input);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ['input_precision_pi','anchor_nonvanishing_certified','frame_computed','candidate_mismatch_certified','precision_obstruction']},indent=2),flush=True)
    print('PASS|427_DYADIC_SECOND_ORDER',flush=True)

if __name__=='__main__':main()
