"""D121 actual multiprecision sparse low-moment factorization.

Blocks use arbitrary Python integers and the independently controlled FLINT
kernel. Only old P=200 comparison data use NumPy. Binary storage contains
fixed-width unsigned coefficients, not executable serialization.
"""
import argparse
from fractions import Fraction
import importlib.util
import json
from math import comb
from pathlib import Path
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'


def module(name, filename):
    s = importlib.util.spec_from_file_location(name, ROOT/'dembele/pari'/filename)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


p = module('prepared', '466_dyadic_prepared_transport.py')
k = module('block_kernel', '470_dyadic_block_kernel_control.py')
ZERO, ONE = p.f.ZERO, p.f.ONE


def pack(a, bits):
    width = (bits+7)//8
    return b''.join(int(c).to_bytes(width, 'little') for row in a for x in row for c in x)


def unpack(raw, nr, nc, bits):
    width = (bits+7)//8
    assert len(raw) == nr*nc*8*width
    return [[tuple(int.from_bytes(raw[((i*nc+j)*8+u)*width:((i*nc+j)*8+u+1)*width], 'little')
                   for u in range(8)) for j in range(nc)] for i in range(nr)]


def reduce(a, mask):
    return [[tuple(c & mask for c in x) for x in row] for row in a]


class Algebra:
    def __init__(self, bits):
        self.bits, self.mask = bits, (1 << bits)-1
        self.ring, self.kernel = p.Ring(bits), k.Kernel()

    def mul(self, a, b): return self.kernel.multiply(a, b, self.bits)

    def sub(self, a, b):
        return [[tuple((u-v) & self.mask for u,v in zip(x,y)) for x,y in zip(ar,br)] for ar,br in zip(a,b)]

    def add(self, a, b):
        return [[tuple((u+v) & self.mask for u,v in zip(x,y)) for x,y in zip(ar,br)] for ar,br in zip(a,b)]

    def identity(self, n): return [[ONE if i==j else ZERO for j in range(n)] for i in range(n)]

    def inverse_from_seed(self, a, seed):
        z = seed; bits = 25; ident = self.identity(len(a))
        while bits < self.bits:
            bits = min(self.bits, 2*bits); stage = Algebra(bits)
            aa = reduce(a, stage.mask)
            z = stage.mul(z, stage.sub(stage.add(ident, ident), stage.mul(aa,z)))
        assert self.mul(a,z) == ident
        return z


def parameters(P):
    path = DATA/'dyadic_target_transports_d121.json'
    packet = json.loads(path.read_text()); mask = (1 << (P//8))-1
    targets, params = [], []
    for row in packet['transitions']:
        targets.append([c['target_edge'] for c in row['children']]); pars=[]
        for c in row['children']:
            assert c['normalized_error_pi'] >= P
            pars.append(tuple(tuple(int(x) & mask for x in a) for a in c['normalized_center'][:3]))
        params.append(pars)
    return targets, params, path


def coefficients(pars, r, algebra):
    # phi=b+delta*x/(1+c*x). The positive coefficient matrix factors
    # H[n,j]=binom(n,j)b^(n-j)delta^j and B[j,k]=binom(k-1,j-1)(-c)^(k-j).
    a,b,c = pars; ring = algebra.ring
    delta = ring.add(a, ring.neg(ring.mul(b,c)))
    powers = []
    for value in (b, delta, ring.neg(c)):
        row = [ONE]
        for _ in range(r): row.append(ring.mul(row[-1],value))
        powers.append(row)
    bp, dp, cp = powers
    def scale(a,n): return tuple((x*n) & ring.mask for x in a)
    H = [[scale(ring.mul(bp[n-j],dp[j]),comb(n,j)) if j<=n else ZERO
          for j in range(1,r+1)] for n in range(1,r+1)]
    B = [[scale(cp[k-j],comb(k-1,j-1)) if j<=k else ZERO
          for k in range(1,r+1)] for j in range(1,r+1)]
    return algebra.mul(H,B)


def solve(rhs, order, D, L, U, algebra):
    b = list(rhs); x = [None]*len(rhs)
    for k in order:
        for (i,j),a in L.items():
            if j==k: b[i] = algebra.sub(b[i],algebra.mul(a,b[k]))
    for k in reversed(order):
        value = b[k]
        for (i,j),a in U.items():
            if i==k: value = algebra.sub(value,algebra.mul(a,x[j]))
        x[k] = algebra.mul(D[k],value)
    return x


def build(P, r):
    assert P >= 200 and P <= 10552 and P % 8 == 0 and r in (8,32,64)
    start = time.monotonic(); algebra = Algebra(P//8)
    targets, params, transport_path = parameters(P)
    old_path = DATA/f'dyadic_sparse_low_r{r}_d121.npz'
    old = np.load(old_path); order = old['order'].tolist()
    oldD, oldL, oldU = old['diagonal'], old['lower'], old['upper']
    oldL = {tuple(key):v for key,v in zip(old['lower_keys'].tolist(),oldL)}
    oldU = {tuple(key):v for key,v in zip(old['upper_keys'].tolist(),oldU)}
    def oldcheck(a,b): assert np.array_equal(np.array(reduce(a,(1 << 25)-1),dtype=np.int64),b)
    identity = algebra.identity(r)
    zero = [[ZERO]*r for _ in range(r)]
    original = {(i,i):identity for i in range(174)}; cache={}
    for e in range(174):
        for branch,j in enumerate(targets[e]):
            pars = params[e][branch]
            if pars not in cache: cache[pars] = coefficients(pars,r,algebra)
            key=e,j; original[key] = algebra.sub(original.get(key,zero),cache[pars])
    coefficient_seconds = time.monotonic()-start
    print(f'MP_LOW_COEFFICIENTS|P={P}; r={r}; maps={len(cache)}; seconds={coefficient_seconds:.3f}',flush=True)
    blocks=dict(original); live=set(order); D,L,U={},{},{}; updates=0
    for step,pivot in enumerate(order):
        seed=[[tuple(map(int,x)) for x in row] for row in oldD[pivot]]
        D[pivot] = algebra.inverse_from_seed(blocks[pivot,pivot],seed)
        oldcheck(D[pivot],oldD[pivot])
        incoming=sorted(i for i in live if i!=pivot and (i,pivot) in blocks)
        outgoing=sorted(j for j in live if j!=pivot and (pivot,j) in blocks)
        for j in outgoing:
            U[pivot,j]=blocks[pivot,j]; oldcheck(U[pivot,j],oldU[pivot,j])
        for i in incoming:
            multiplier=algebra.mul(blocks[i,pivot],D[pivot]); L[i,pivot]=multiplier
            oldcheck(multiplier,oldL[i,pivot])
            for j in outgoing:
                product=algebra.mul(multiplier,blocks[pivot,j])
                blocks[i,j]=algebra.sub(blocks.get((i,j),zero),product); updates+=1
            del blocks[i,pivot]
        for j in outgoing: del blocks[pivot,j]
        del blocks[pivot,pivot]; live.remove(pivot)
        if step % 25 == 0 or step==173:
            print(f'MP_LOW_FACTOR|P={P}; states={step+1}/174; updates={updates}; seconds={time.monotonic()-start:.3f}',flush=True)
    assert not blocks and updates==2246
    factor_seconds=time.monotonic()-start-coefficient_seconds
    # Two unrelated right-hand sides, checked in the original sparse matrix.
    rhs=[k.data(r,2,algebra.bits,f'actual-P{P}-state{i}') for i in range(174)]
    then=time.monotonic(); answer=solve(rhs,order,D,L,U,algebra)
    residual=[[[ZERO]*2 for _ in range(r)] for _ in range(174)]
    for (i,j),block in original.items():
        residual[i]=algebra.add(residual[i],algebra.mul(block,answer[j]))
    assert residual==rhs
    residual_seconds=time.monotonic()-then
    binary=DATA/f'dyadic_low_factor_P{P}_r{r}_d121.bin'; assert not binary.exists()
    keys=[['D',i,i] for i in range(174)]+[['L',i,j] for i,j in sorted(L)]+[['U',i,j] for i,j in sorted(U)]
    with binary.open('wb') as out:
        for kind,i,j in keys: out.write(pack(D[i] if kind=='D' else (L if kind=='L' else U)[i,j],algebra.bits))
    assert binary.stat().st_size==len(keys)*r*r*8*((algebra.bits+7)//8)
    result={'status':'pass','milestone':'D121','working_precision_pi':P,'eliminated_positive_moments':r,
        'modulus_bits':algebra.bits,'order':order,'binary_block_order':keys,
        'binary_coefficient_width_bytes':(algebra.bits+7)//8,'binary_payload_bytes':binary.stat().st_size,
        'block_updates':updates,'all_P200_factor_coefficients_agree':True,
        'diagonal_inverse_products_checked':174,'unrelated_rhs_columns':2,
        'original_sparse_residual_checked':True,'original_scalar_equations_checked':174*r*8*2,
        'coefficient_seconds':coefficient_seconds,'factor_seconds':factor_seconds,
        'solve_and_residual_seconds':residual_seconds,'wall_seconds':time.monotonic()-start,
        'actual_moment_precision_increased':False,
        'sources':[p.f.source(x) for x in [Path(__file__),Path(p.__file__),Path(k.__file__),
            k.LIBRARY,transport_path,old_path,binary]]}
    print('MP_LOW_RESULT|'+json.dumps({x:y for x,y in result.items() if x not in ('sources','order','binary_block_order')}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--precision',type=int,default=400);parser.add_argument('--moments',type=int,default=32)
    args=parser.parse_args();out=DATA/f'dyadic_low_factor_P{args.precision}_r{args.moments}_d121.json'
    assert not out.exists();out.write_text(json.dumps(build(args.precision,args.moments),indent=2)+'\n')
    print('PASS|472_DYADIC_MULTIPRECISION_LOW_FACTOR',flush=True)
