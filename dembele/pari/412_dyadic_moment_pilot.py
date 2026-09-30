"""D113 bounded positive-moment pilot via the finite contracting equations.

The pilot works modulo pi^12, retaining moments 0,...,11 on 174 states,
for all sixteen actual harmonic measures. CM moments 1,2,3 have respective
error lower bounds 11,10,9. Two bit planes implement O_K/(pi^12).
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
spec=importlib.util.spec_from_file_location('transport',ROOT/'dembele/pari/411_dyadic_moment_transports.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
r=t.r;source,checked=r.source,r.checked
P,J,CM_DEGREE=12,11,3

class Ring:
    """Parallel vectors over O_K/(pi^P), 8<=P<=16, with pi^8=-2.

    The discarded terms of the true F polynomial have valuation >=20.
    Low/high bits give coefficients modulo 2/4 in the power basis of pi.
    """
    def __init__(self,width=1,precision=P):
        assert 8<=precision<=16
        self.width=width;self.precision=precision
        self.lowmask=(1<<(8*width))-1
        self.highmask=(1<<((precision-8)*width))-1
        self.slotmask=(1<<width)-1
    def add(self,x,y):
        return x[0]^y[0],(x[1]^y[1]^(x[0]&y[0]))&self.highmask
    def neg(self,x):return x[0],(x[1]^x[0])&self.highmask
    def shift(self,x):
        return ((x[0]<<self.width)&self.lowmask,
                ((x[1]<<self.width)^(x[0]>>(7*self.width)))&self.highmask)
    def smul(self,c,x):
        lo,hi=c;v,w=x;z,h=0,0
        for j in range(8):
            if (lo>>j)&1:h^=w^(z&v);z^=v
            if (hi>>j)&1:h^=v
            v,w=(v<<self.width)&self.lowmask,((w<<self.width)^(v>>(7*self.width)))&self.highmask
        return z,h&self.highmask
    def encode(self,rows):
        assert len(rows)==self.width
        lo=hi=0
        for n,row in enumerate(rows):
            assert len(row)==8
            for i,c in enumerate(row):
                mod=4 if i<self.precision-8 else 2
                c=r.Q(c);assert c.denominator%2
                z=c.numerator*pow(c.denominator,-1,mod)%mod
                lo|=(z&1)<<(i*self.width+n)
                hi|=(z>>1)<<(i*self.width+n)
        return lo,hi
    def decode(self,x):
        return [[((x[0]>>(i*self.width+n))&1)+2*((x[1]>>(i*self.width+n))&1)
                 for i in range(8)] for n in range(self.width)]
    def val(self,x):
        def first(n):return ((n&-n).bit_length()-1)//self.width
        return min(first(x[0]) if x[0] else self.precision,
                   8+first(x[1]) if x[1] else self.precision)

R=Ring();V=Ring(16);ZERO=(0,0);ONE=(1,0)

def center(row):return tuple(R.encode([r.f(v)]) for v in row['normalized_center'][:3])

@lru_cache(None)
def powers(params,degree,truncation):
    a,b,c=params;delta=R.add(a,R.neg(R.smul(b,c)))
    phi=[b,delta]
    for _ in range(2,truncation+1):phi.append(R.neg(R.smul(c,phi[-1])))
    result=[[ONE]+[ZERO]*truncation]
    for _ in range(degree):
        nxt=[ZERO]*(truncation+1)
        for i,u in enumerate(result[-1]):
            if u!=ZERO:
                for k,v in enumerate(phi[:truncation+1-i]):
                    if v!=ZERO:nxt[i+k]=R.add(nxt[i+k],R.smul(u,v))
        result.append(nxt)
    return tuple(tuple(row) for row in result)

def validation():
    basis=[tuple(r.Q(i==j) for i in range(8)) for j in range(8)]
    for x in basis:
        for y in basis:
            assert R.smul(R.encode([x]),R.encode([y]))==R.encode([r.mul(x,y)])
    assert R.encode([r.scale(r.ONE,2)])==(0,1) and R.val((0,1))==8
    for n in range(16):
        rows=[[0]*8 for _ in range(16)];rows[n]=[3,1,2,3,0,1,1,0]
        x=V.encode(rows);assert V.add(x,V.neg(x))==ZERO
        for y in basis:
            assert V.decode(V.smul(R.encode([y]),x))==V.decode(V.encode([r.mul(y,tuple(map(r.Q,z))) for z in rows]))

def calculations():
    validation()
    packet=json.loads((DATA/'dyadic_moment_transports_d113.json').read_text())
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    m0=[V.encode([[harmonic['harmonic_basis'][n][e]]+[0]*7 for n in range(16)]) for e in range(174)]
    operators=[]
    for row in packet['transitions']:
        children=[]
        for child in row['children']:
            assert child['normalized_error_pi']>=P and child['determinant_valuation']==1
            coef=powers(center(child),J,J)
            assert all(R.val(coef[n][k])>=min(k,P) for n in range(1,J+1) for k in range(1,J+1))
            children.append((child['target_edge'],[[ (k,c) for k,c in enumerate(cs) if c!=ZERO] for cs in coef]))
        operators.append(children)
    def step(m):
        out=[]
        for e,children in enumerate(operators):
            rows=[m0[e]]
            for n in range(1,J+1):
                v=ZERO
                for f,coef in children:
                    for k,c in coef[n]:v=V.add(v,V.smul(c,m[f][k]))
                rows.append(v)
            out.append(rows)
        return out
    m=[[x]+[ZERO]*J for x in m0];gains=[]
    for iteration in range(1,P+1):
        new=step(m)
        gain=min(V.val(V.add(x,V.neg(y))) for row,old in zip(new,m) for x,y in zip(row[1:],old[1:]))
        assert gain>=iteration-1;gains.append(gain);m=new
    assert step(m)==m
    bad=[row[:] for row in m];bad[0][1]=V.add(bad[0][1],(1,0))
    assert step(bad)!=bad
    print(f'MOMENTS|174 states x 16 measures x degrees 0..{J}; precision pi^{P}; gains {gains}',flush=True)
    charts=[];nonzero=0;anchor_nonzero=0
    for chart in packet['CM_charts']:
        coef=powers(center(chart),CM_DEGREE,J);f=chart['target_edge'];rows=[]
        for degree in range(CM_DEGREE+1):
            z=ZERO
            for k,c in enumerate(coef[degree]):
                if c!=ZERO:z=V.add(z,V.smul(c,m[f][k]))
            rows.append(V.decode(z))
            if degree:
                err=min(P,J+1-degree)
                for vec in rows[-1]:
                    if R.val(R.encode([vec]))<err:
                        nonzero+=1
                        if chart['CM_index']==0:anchor_nonzero+=1
        assert rows[0]==V.decode(V.encode([[v]+[0]*7 for v in chart['zeroth_moments']]))
        charts.append({'CM_index':chart['CM_index'],'chart':chart['chart'],
                       'moments_power_basis':rows,'positive_degree_errors_pi':[J,J-1,J-2],
                       'zeroth_moments_exact':chart['zeroth_moments']})
    assert nonzero>0
    print(f'CM_MOMENTS|51 charts, degrees 1..3, errors 11/10/9; {nonzero} certified nonzero entries; anchor {anchor_nonzero}',flush=True)
    return {'status':'pass','milestone':'D113','working_precision_pi':P,'state_maximum_degree':J,
            'iterations':P,'successive_difference_lower_bounds_pi':gains,
            'state_moments_power_basis':[[V.decode(z) for z in row] for row in m],
            'CM_chart_moments':charts,'certified_nonzero_positive_CM_entries':nonzero,
            'anchor_certified_nonzero_positive_entries':anchor_nonzero,
            'truncated_fixed_point_residual_zero':True,'altered_positive_moment_rejected':True,
            'actual_positive_degree_moments_computed':True,'actual_Shimura_tangent_or_jet_evaluated':False,
            'actual_harmonic_to_residue_frame_change_computed':False,
            'sources':[source(p) for p in [Path(__file__),Path(t.__file__),DATA/'dyadic_moment_transports_d113.json',
                                          DATA/'dyadic_harmonic_certificate_d111.json']]}

def main():
    out=DATA/'dyadic_moment_pilot_d113.json';assert not out.exists()
    result=calculations();out.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS|412_DYADIC_MOMENT_PILOT',flush=True)

if __name__=='__main__':main()
