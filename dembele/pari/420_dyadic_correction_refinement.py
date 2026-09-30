"""D115: refine only the contracting correction to the known moment bank.

Packed integers perform exact scalar/vector polynomial products. Guard bits
prevent carries between lanes; the full defining polynomial is always reduced.
Only the low moment system is iterated, then higher rows are recovered once.
This source computes enclosures, not candidate identification.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
FP=(2,0,-16,0,20,0,-8,0,1)

def module(number,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'dembele/pari'/number)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result

base=module('415_dyadic_coarse_poisson.py','coarse_d114')
source=base.source

class PackedRing:
    def __init__(self,precision,width=1):
        assert precision%8==0 and 8<=precision<=152
        self.precision=precision;self.width=width;self.bits=precision//8
        self.mod=1<<self.bits
        self.slot=2*self.bits+16;self.stride=self.slot*width
        self.units=sum(1<<(j*self.slot) for j in range(width))
        self.blockmask=(self.mod-1)*self.units
        self.mask=sum(self.blockmask<<(i*self.stride) for i in range(8))
        self.bias=64*self.mod*self.units
        self.negbias=sum(self.mod*self.units<<(i*self.stride) for i in range(8))
    def encode(self,rows):
        assert len(rows)==self.width and all(len(x)==8 for x in rows)
        z=0
        for j,row in enumerate(rows):
            for i,c in enumerate(row):
                c=Fraction(c);assert c.denominator%2
                v=c.numerator*pow(c.denominator,-1,self.mod)%self.mod
                z|=v<<((i*self.width+j)*self.slot)
        return z
    def decode(self,z):
        return [[(z>>((i*self.width+j)*self.slot))&(self.mod-1) for i in range(8)] for j in range(self.width)]
    def add(self,x,y):return (x+y)&self.mask
    def neg(self,x):return (self.negbias-x)&self.mask
    def reduce(self,z):
        v=[(z>>(i*self.stride))&self.blockmask for i in range(15)]
        for k in range(14,7,-1):
            c=v[k]
            if c:
                for j in (0,2,4,6):
                    v[k-8+j]=(v[k-8+j]+self.bias-c*FP[j])&self.blockmask
        return sum(v[i]<<(i*self.stride) for i in range(8))
    def mul(self,x,y):
        assert self.width==1
        return self.reduce(x*y)
    def dot(self,terms):
        # At most 2P terms, each coefficient sums at most 8 products <2^(2m).
        # The 16 guard bits suffice since 16P<2^16 throughout the allowed range.
        return self.reduce(sum(c*v for c,v in terms))
    def val(self,z):
        for v in range(self.precision):
            if z&(self.units<<((v%8)*self.stride+v//8)):return v
        return self.precision
    @lru_cache(None)
    def scalar(self,cs):
        return sum(int(c)%self.mod<<(i*self.stride) for i,c in enumerate(cs))

def validate(R,V):
    # Independent ordinary signed convolution, including the nonzero pi^4 term.
    def ordinary(x,y):
        v=[0]*15
        for i,a in enumerate(x):
            for j,b in enumerate(y):v[i+j]+=a*b
        for k in range(14,7,-1):
            for j in range(8):v[k-8+j]-=v[k]*FP[j]
        return [x%R.mod for x in v[:8]]
    vectors=[[((j+3)*(i+5)**2+7*i)%R.mod for i in range(8)] for j in range(16)]
    for k in range(8):
        c=[int(i==k) for i in range(8)]
        actual=V.decode(V.dot([(V.scalar(tuple(c)),V.encode(vectors))]))
        assert actual==[ordinary(c,x) for x in vectors]
    terms=[];expected=[[0]*8 for _ in range(16)]
    for k in range(2*R.precision):
        c=[(k+3*i+1)%R.mod for i in range(8)]
        terms.append((V.scalar(tuple(c)),V.encode(vectors)))
        for j,x in enumerate(vectors):expected[j]=[(a+b)%R.mod for a,b in zip(expected[j],ordinary(c,x))]
    assert V.decode(V.dot(terms))==expected
    pi=R.encode([[0,1,0,0,0,0,0,0]]);z=1
    for _ in range(8):z=R.mul(z,pi)
    assert R.decode(z)[0]==[(-c)%R.mod for c in FP[:8]]
    assert V.add(V.encode(vectors),V.neg(V.encode(vectors)))==0

def calculations(P,seed_path):
    start=time.monotonic();R=PackedRing(P);V=PackedRing(P,16);validate(R,V)
    low=P-1;cmmax=2*P-1;high=3*P-2
    packet=json.loads((DATA/'dyadic_moment_transports_d113.json').read_text())
    harmonic=json.loads((DATA/'dyadic_harmonic_certificate_d111.json').read_text())
    seed=json.loads(seed_path.read_text());oldP=seed['working_precision_pi']
    assert oldP<P and len(seed['state_moments_power_basis'][0])>low
    m0=[V.encode([[b[e]]+[0]*7 for b in harmonic['harmonic_basis']]) for e in range(174)]
    def params(row):return tuple(R.encode([x]) for x in row['normalized_center'][:3])
    @lru_cache(None)
    def powers(p,degree,cutoff):
        a,b,c=p;rows=[[1]+[0]*cutoff]
        # (1+cx)phi^(n+1)=(b+ax)phi^n, independent of previous bit-plane code.
        for _ in range(degree):
            prev=rows[-1];row=[]
            for k in range(cutoff+1):
                z=R.mul(b,prev[k])
                if k:z=R.add(z,R.add(R.mul(a,prev[k-1]),R.neg(R.mul(c,row[k-1]))))
                row.append(z)
            rows.append(row)
        return rows
    @lru_cache(None)
    def lift(c):return V.scalar(tuple(R.decode(c)[0]))
    ops=[]
    for tr in packet['transitions']:
        children=[]
        for child in tr['children']:
            assert child['normalized_error_pi']>=P
            cs=powers(params(child),high,low)
            assert all(R.val(c)>=k for row in cs for k,c in enumerate(row) if k)
            children.append((child['target_edge'],[[(k,lift(c)) for k,c in enumerate(row) if c] for row in cs]))
        ops.append(children)
    print(f'OPERATORS|P={P} built in {time.monotonic()-start:.2f}s',flush=True)
    def evaluate(m,e,n):
        return V.dot((c,m[f][k]) for f,rows in ops[e] for k,c in rows[n])
    def step(m):return [[m0[e]]+[evaluate(m,e,n) for n in range(1,low+1)] for e in range(174)]
    m=[[V.encode(x) for x in row[:low+1]] for row in seed['state_moments_power_basis']]
    # Zeroth masses are exact input, not variables of the contracting operator.
    # Their arbitrary lifts modulo the seed precision must be replaced first.
    for e in range(174):m[e][0]=m0[e]
    first=step(m)
    correction=[[V.add(x,V.neg(y)) for x,y in zip(row,prev)] for row,prev in zip(first,m)]
    gains=[]
    for iteration in range(oldP,P):
        gain=min(V.val(x) for row in correction for x in row)
        assert gain>=iteration and all(row[0]==0 for row in correction)
        gains.append(gain)
        m=[[V.add(x,y) for x,y in zip(row,diff)] for row,diff in zip(m,correction)]
        if iteration+1<P:
            # Every correction has valuation >=gain; columns k>=P-gain vanish.
            correction=[[0]+[V.dot((c,correction[f][k]) for f,rows in ops[e]
                           for k,c in rows[n] if 0<k<P-gain)
                           for n in range(1,low+1)] for e in range(174)]
    assert step(m)==m
    full=[row+[evaluate(m,e,n) for n in range(low+1,high+1)] for e,row in enumerate(m)]
    bank=[[V.decode(z) for z in row] for row in full]
    mask=(1<<(oldP//8))-1
    for e,row in enumerate(seed['state_moments_power_basis']):
        for n,values in enumerate(row):assert [[c&mask for c in x] for x in bank[e][n]]==values
    print(f'STATES|P={P}, seed {oldP}, gains {gains}, all overlaps pass; {time.monotonic()-start:.2f}s',flush=True)
    charts=[]
    for chart in packet['CM_charts']:
        if chart['chart']!='A':continue
        assert chart['normalized_error_pi']>=P
        cs=powers(params(chart),cmmax,high)
        rows=[]
        for n,row in enumerate(cs):
            assert all(R.val(c)>=min(P,max(0,k-n)) for k,c in enumerate(row))
            z=V.dot((lift(c),full[chart['target_edge']][k]) for k,c in enumerate(row) if c)
            rows.append(V.decode(z))
        assert rows[0]==V.decode(V.encode([[x]+[0]*7 for x in chart['zeroth_moments']]))
        charts.append({'CM_index':chart['CM_index'],'chart':'A','moments_power_basis':rows,'error_pi':P})
    print(f'CM|17 A charts through degree {cmmax}; {time.monotonic()-start:.2f}s',flush=True)
    import numpy as np
    precision=2*P+48;CM=base.CMring(precision);kernels,pi=base.kernel_bank(CM,cmmax)
    errors=[2*P+32,2*P+48,2*P+32];embedding=np.array(CM.powers(pi,7),dtype=np.int64)
    results=[]
    # Bound each accumulated integer product before any NumPy int64 operation.
    assert 32*(cmmax+1)*16*int(max(CM.mods))**2<2**63
    for ci,chart in enumerate(charts):
        moments=(np.array(chart['moments_power_basis'],dtype=np.int64)@embedding)%CM.mods
        vals=[];valuations=[]
        for j in range(3):
            answer=np.zeros((16,16),dtype=np.int64)
            for degree,c in enumerate(kernels[j][0]):
                c=CM.scale(c,2)
                if c!=base.ZERO:answer+=CM.matrix(c)@moments[degree].T
            answer%=CM.mods[:,None];coeffs=answer.T.tolist();vals.append(coeffs)
            valuations.append([v if (v:=CM.val(x))<errors[j] else None for x in coeffs])
        results.append({'CM_index':ci,'coarse_coefficients_beta':vals,'certified_valuations_beta':valuations,'error_beta':errors})
    oldcoarse=json.loads((DATA/'dyadic_coarse_review_d114.json').read_text())['certificates']['Poisson']
    for row,old in zip(results,oldcoarse['symmetry_refined_CM_values']):
        for j in range(3):
            for x,y in zip(row['coarse_coefficients_beta'][j],old['coarse_coefficients_beta'][j]):
                assert CM.val(CM.add(x,CM.scale(y,-1)))>=oldcoarse['symmetry_refined_errors_beta'][j]
    print('ANCHOR|'+json.dumps(results[0]['certified_valuations_beta']),flush=True)
    print(f'COARSE|errors beta={errors}; total {time.monotonic()-start:.2f}s',flush=True)
    return {'status':'pass','milestone':'D115','working_precision_pi':P,'low_cutoff':low,'state_cutoff':high,
            'CM_cutoff':cmmax,'seed_precision_pi':oldP,'successive_difference_lower_bounds_pi':gains,
            'state_moments_power_basis':bank,'CM_A_chart_moments':charts,'coarse_error_beta':errors,
            'arithmetic_precision_beta':precision,'CM_values':results,
            'anchor_nonvanishing_certified':any(v is not None for v in results[0]['certified_valuations_beta'][0]),
            'rational_frame_computed':False,'candidate_identification_proved':False,
            'sources':[source(x) for x in [Path(__file__),Path(base.__file__),seed_path,
              DATA/'dyadic_moment_transports_d113.json',DATA/'dyadic_harmonic_certificate_d111.json',
              DATA/'dyadic_coarse_review_d114.json']]}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--precision',type=int,required=True)
    parser.add_argument('--seed',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();assert not args.output.exists()
    result=calculations(args.precision,args.seed)
    args.output.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('PASS|420_DYADIC_CORRECTION',flush=True)

if __name__=='__main__':main()
