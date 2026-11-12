"""D138 arbitrary-integer beta arithmetic and explicit valuation balls.

The ball interface follows frozen 427, with dynamic ring precision and
integer scaling that avoids a field product for integral quadric entries.
"""
from fractions import Fraction
from functools import lru_cache
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
MP=(2,0,64,0,336,0,672,0,660,0,352,0,104,0,16,0,1)
ZERO=(0,)*16;ONE=(1,)+(0,)*15;BETACOORD=(0,1)+(0,)*14;INF=10**9


class Ring:
    def __init__(self,precision):
        assert precision>0 and precision%16==0
        self.precision=precision;self.bits=precision//16;self.mod=1<<self.bits;self.mask=self.mod-1
    def normalize(self,x):return tuple(int(c)&self.mask for c in x)
    def add(self,a,b):return tuple((x+y)&self.mask for x,y in zip(a,b))
    def scale(self,a,n):return tuple((x*n)&self.mask for x in a)
    def mul(self,a,b):
        if a==ZERO or b==ZERO:return ZERO
        if a==ONE:return b
        if b==ONE:return a
        if not any(a[1:]):return self.scale(b,a[0])
        if not any(b[1:]):return self.scale(a,b[0])
        out=[0]*31
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):out[i+j]+=x*y
        for d in range(30,15,-1):
            if out[d]:
                for j in range(0,16,2):out[d-16+j]-=out[d]*MP[j]
        return tuple(x&self.mask for x in out[:16])
    def value(self,x):
        return min([self.precision]+[16*((c&-c).bit_length()-1)+i for i,c in enumerate(x) if c])
    def divide_beta(self,x,n):
        for _ in range(n):
            assert x[0]%2==0
            half=x[0]//2
            x=tuple(((x[i+1] if i<15 else 0)-half*MP[i+1])&self.mask for i in range(16))
        return x
    def unit_inverse(self,x):
        assert self.value(x)==0
        z=ONE;two=self.scale(ONE,2)
        for _ in range((self.precision-1).bit_length()):
            z=self.mul(z,self.add(two,self.scale(self.mul(x,z),-1)))
        assert self.mul(x,z)==ONE
        return z
    def rational_integral(self,row,shift=0):
        result=[]
        for c in row:
            q=Fraction(c)*(1<<shift);assert q.denominator&1
            result.append(q.numerator*pow(q.denominator,-1,self.mod)&self.mask)
        return tuple(result)


PRECISION=4096;R=Ring(PRECISION)


@lru_cache(None)
def beta_power(n):
    assert n>=0
    if n>=PRECISION:return ZERO
    ans=ONE;x=BETACOORD
    while n:
        if n&1:ans=R.mul(ans,x)
        x=R.mul(x,x);n//=2
    return ans


@lru_cache(maxsize=65536)
def unit_inverse(x):return R.unit_inverse(x)


class Ball:
    def __init__(self,u=ZERO,v=0,error=INF):
        u=R.normalize(u)
        if u==ZERO:self.u=ZERO;self.v=INF;self.error=error;return
        error=min(error,v+PRECISION);w=R.value(u)
        if v+w>=error:self.u=ZERO;self.v=INF;self.error=error;return
        self.u=R.divide_beta(u,w);self.v=v+w;self.error=error
    def known_nonzero(self):return self.v<self.error
    def lower(self):return min(self.v,self.error)
    def __neg__(self):return Ball(R.scale(self.u,-1),self.v if self.u!=ZERO else 0,self.error)
    def __add__(self,other):
        error=min(self.error,other.error)
        if self.u==ZERO:return Ball(other.u,other.v if other.u!=ZERO else 0,error)
        if other.u==ZERO:return Ball(self.u,self.v,error)
        v=min(self.v,other.v)
        u=R.add(R.mul(self.u,beta_power(self.v-v)),R.mul(other.u,beta_power(other.v-v)))
        return Ball(u,v,min(error,v+PRECISION))
    def __sub__(self,other):return self+(-other)
    def __mul__(self,other):
        error=min(self.error+other.lower(),other.error+self.lower())
        if self.u==ZERO or other.u==ZERO:return Ball(error=error)
        return Ball(R.mul(self.u,other.u),self.v+other.v,error)
    def scale_integer(self,c):
        assert isinstance(c,int)
        if c==0:return Ball()
        gain=16*((abs(c)&-abs(c)).bit_length()-1)
        return Ball(R.scale(self.u,c),self.v if self.u!=ZERO else 0,self.error+gain)
    def inverse(self):
        assert self.known_nonzero(),('unresolved division',self.summary())
        return Ball(unit_inverse(self.u),-self.v,self.error-2*self.v)
    def __truediv__(self,other):return self*other.inverse()
    def __pow__(self,n):
        if n<0:return self.inverse()**(-n)
        ans=Ball(ONE);x=self
        while n:
            if n&1:ans=ans*x
            x=x*x;n//=2
        return ans
    def summary(self):return {'valuation_beta':self.v if self.known_nonzero() else None,'error_beta':self.error}
    def saved(self):return {'unit_beta':list(self.u),'beta_exponent':self.v if self.u!=ZERO else None,'error_beta':self.error}


BETA=Ball(BETACOORD);TWO=Ball(R.scale(ONE,2))


def rational(q):
    q=Fraction(q)
    if not q:return Ball()
    n,d=q.numerator,q.denominator
    a=(abs(n)&-abs(n)).bit_length()-1;b=(d&-d).bit_length()-1
    u=R.scale(ONE,(n>>a)*pow(d>>b,-1,R.mod))
    return Ball(u)*(TWO**(a-b))


def center(row,error):
    if all(Fraction(c).denominator==1 for c in row):return Ball(tuple(int(c) for c in row),error=error)
    z=Ball()
    for i,c in enumerate(row):
        if Fraction(c):z=z+rational(c)*(BETA**i)
    return Ball(z.u,z.v if z.u!=ZERO else 0,min(error,z.error))


def restore(row):return Ball(tuple(row['unit_beta']),row['beta_exponent'] or 0,row['error_beta'])
def dot(a,b):
    out=Ball()
    for x,y in zip(a,b):out=out+x*y
    return out
def multiply(a,b):return [[dot(row,col) for col in zip(*b)] for row in a]


def inverse(a):
    n=len(a);ident=Ball(ONE)
    rows=[row[:]+[ident if i==j else Ball() for j in range(n)] for i,row in enumerate(a)]
    pivots=[]
    for k in range(n):
        choices=[(rows[i][k].v,i) for i in range(k,n) if rows[i][k].known_nonzero()]
        assert choices,('unresolved inverse column',k)
        _,i=min(choices);rows[k],rows[i]=rows[i],rows[k]
        pivots.append(rows[k][k].summary());ip=rows[k][k].inverse()
        rows[k]=[x*ip for x in rows[k]]
        for i in range(n):
            if i!=k:
                c=rows[i][k];rows[i]=[x-c*y for x,y in zip(rows[i],rows[k])]
    inv=[row[n:] for row in rows];check=multiply(a,inv)
    assert all(not(x-(ident if i==j else Ball())).known_nonzero() for i,row in enumerate(check) for j,x in enumerate(row))
    return inv,pivots


def controls():
    s=importlib.util.spec_from_file_location('old',ROOT/'dembele/pari/427_dyadic_second_order_comparison.py')
    old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
    for i in range(8):
        x=tuple((R.mod-17-13*i-19*j)&R.mask for j in range(16))
        y=tuple((R.mod-23-11*i-31*j)&R.mask for j in range(16))
        assert tuple(c%old.R.maximum for c in R.mul(x,y))==old.R.mul(old.R.normalize(x),old.R.normalize(y))
    for q in ('-3/8','7/16','4/3','17/9'):
        x=rational(q);assert not(x*x.inverse()-Ball(ONE)).known_nonzero()
        for c in (-8,-1,1,3,16):assert not(x.scale_integer(c)-x*rational(c)).known_nonzero()
    a=[[rational(2),Ball(ONE)],[Ball(ONE),rational(4)]];ai,_=inverse(a)
    assert not(ai[0][0]-rational('4/7')).known_nonzero()
    assert not(ai[0][1]-rational('-1/7')).known_nonzero()
    unresolved=Ball(R.scale(ONE,4),error=32);assert not unresolved.known_nonzero()
    try:unresolved.inverse()
    except AssertionError:pass
    else:raise AssertionError('unknown ball inverted')
    return {'ring_precision_beta':PRECISION,'independent_ring_products_checked':8,
        'integral_scalings_compared_with_field_products':20,'inverse_residual_checked':True,
        'unknown_ball_inverse_rejected':True,'sources':[old.coarse.source(x) for x in [Path(__file__),Path(old.__file__)]]}


if __name__=='__main__':
    out=DATA/'dyadic_precision1600_balls_d138.json';assert not out.exists()
    tick=time.monotonic();result={'status':'pass','milestone':'D138',**controls()}
    result['wall_seconds']=time.monotonic()-tick;result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    assert result['peak_rss_bytes']<=2*(1<<30)
    out.write_text(json.dumps(result,indent=2)+'\n')
    import hashlib
    print('PHASE_METADATA|'+json.dumps({'path':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}),flush=True)
    print('PASS|570_DYADIC_PRECISION1600_BALLS',flush=True)
