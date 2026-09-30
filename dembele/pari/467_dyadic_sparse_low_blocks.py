"""D121 sparse block elimination of several positive moments.

Use the directed state ordering already measured by 464. Store block LU
factors rather than a dense inverse. All validation uses the original
transport equations and all sixteen frozen harmonic columns.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
s = importlib.util.spec_from_file_location('low', ROOT/'dembele/pari/464_dyadic_low_moment_block.py')
l = importlib.util.module_from_spec(s); s.loader.exec_module(l)


class Algebra:
    def __init__(self, ring): self.ring = ring

    def mul(self, a, b):
        n, inner, _ = a.shape
        assert b.shape[0] == inner and 8*inner*(self.ring.mod-1)**2 < 2**63
        m = b.shape[1]
        kernel = self.ring.matrix(a).transpose(0, 2, 1, 3).reshape(8*n, 8*inner)
        return ((kernel @ b.transpose(0, 2, 1).reshape(8*inner, m)) % self.ring.mod).reshape(n, 8, m).transpose(0, 2, 1)

    def action(self, a, x):
        n, inner, _ = a.shape
        assert 8*inner*(self.ring.mod-1)**2 < 2**63
        kernel = self.ring.matrix(a).transpose(0, 2, 1, 3).reshape(8*n, 8*inner)
        return ((kernel @ x.reshape(8*inner, -1)) % self.ring.mod).reshape(n, 8, -1)

    def inverse(self, a):
        r = self.ring; n = len(a)
        identity = np.zeros_like(a); identity[np.arange(n), np.arange(n), 0] = 1
        aug = np.concatenate((a.copy(), identity), axis=1)
        for k in range(n):
            aug[k] = r.mul(r.inverse_unit(aug[k, k]), aug[k])
            active = np.flatnonzero(np.any(aug[:, k], axis=1)); active = active[active != k]
            coefficients = aug[active, k].copy()
            product = np.einsum('iab,jb->ija', r.matrix(coefficients), aug[k]) % r.mod
            aug[active] = (aug[active]-product) % r.mod
        assert np.array_equal(aug[:, :n], identity)
        inverse = aug[:, n:]
        assert np.array_equal(self.mul(a, inverse), identity)
        return inverse


def coefficients(ring, pars, r, precision):
    # phi^n=(a*x+b)*phi^(n-1)/(1+c*x): independent of 459/463's
    # generating-function transport. Extra column P certifies the tail.
    matrices = ring.matrix(pars)
    A, B, C = matrices[:, :, 0], matrices[:, :, 1], matrices[:, :, 2]
    out = np.zeros((174, 2, r+1, precision+1, 8), dtype=np.int64)
    out[:, :, 0, 0, 0] = 1
    for n in range(1, r+1):
        out[:, :, n, 0] = np.einsum('ebij,ebj->ebi', B, out[:, :, n-1, 0]) % ring.mod
        for k in range(1, precision+1):
            out[:, :, n, k] = (
                np.einsum('ebij,ebj->ebi', B, out[:, :, n-1, k])
                +np.einsum('ebij,ebj->ebi', A, out[:, :, n-1, k-1])
                -np.einsum('ebij,ebj->ebi', C, out[:, :, n, k-1])) % ring.mod
    assert not np.any(out[:, :, :, precision])
    return out[:, :, 1:, :precision].copy()


def factor(blocks, order, algebra):
    blocks = {k:v.copy() for k,v in blocks.items()}
    diagonal, lower, upper = {}, {}, {}
    live = set(order); start = time.monotonic(); count = 0
    for step, k in enumerate(order):
        diagonal[k] = algebra.inverse(blocks[k, k])
        incoming = sorted(i for i in live if i != k and (i, k) in blocks)
        outgoing = sorted(j for j in live if j != k and (k, j) in blocks)
        for j in outgoing: upper[k, j] = blocks[k, j]
        for i in incoming:
            multiplier = algebra.mul(blocks[i, k], diagonal[k])
            lower[i, k] = multiplier
            for j in outgoing:
                product = algebra.mul(multiplier, blocks[k, j])
                if (i, j) in blocks: blocks[i, j] = (blocks[i, j]-product) % algebra.ring.mod
                else: blocks[i, j] = -product % algebra.ring.mod
                count += 1
            del blocks[i, k]
        for j in outgoing: del blocks[k, j]
        del blocks[k, k]; live.remove(k)
        if step % 30 == 0:
            print(f'SPARSE_LOW|r={len(diagonal[k])}; states={step+1}/174; seconds={time.monotonic()-start:.3f}', flush=True)
    assert not blocks
    return diagonal, lower, upper, {'factor_seconds':time.monotonic()-start, 'block_updates':count,
        'diagonal_inverse_blocks':len(diagonal), 'lower_blocks':len(lower), 'upper_blocks':len(upper)}


def solve(rhs, order, diagonal, lower, upper, algebra):
    b = rhs.copy(); x = np.empty_like(rhs)
    for k in order:
        for (i, j), a in lower.items():
            if j == k: b[i] = (b[i]-algebra.action(a, b[k])) % algebra.ring.mod
    for k in reversed(order):
        value = b[k].copy()
        for (i, j), a in upper.items():
            if i == k: value = (value-algebra.action(a, x[j])) % algebra.ring.mod
        x[k] = algebra.action(diagonal[k], value)
    return x


def build(r):
    assert r in (2, 4, 8, 16, 32, 64)
    start = time.monotonic(); ring = l.Ring(); algebra = Algebra(ring)
    saved = np.load(DATA/'dyadic_low_moment_block_d121.npz')
    params, targets = saved['params'], saved['targets']
    profile = json.loads((DATA/'dyadic_low_moment_block_d121.json').read_text())['graph_profile']
    order = profile['minimum_fill_state_order']
    then = time.monotonic(); coeff = coefficients(ring, params, r, 200)
    coefficient_seconds = time.monotonic()-then
    identity = np.zeros((r, r, 8), dtype=np.int64); identity[np.arange(r), np.arange(r), 0] = 1
    blocks = {(i, i):identity.copy() for i in range(174)}
    for e in range(174):
        for branch, target in enumerate(targets[e]):
            key = e, int(target)
            block = coeff[e, branch, :, 1:r+1]
            if key in blocks: blocks[key] = (blocks[key]-block) % ring.mod
            else: blocks[key] = -block % ring.mod
    diagonal, lower, upper, timing = factor(blocks, order, algebra)
    bank_path = DATA/'dyadic_precision200_d115.json'
    bank = json.loads(bank_path.read_text())
    moments = np.array(bank['state_moments_power_basis'], dtype=np.int64)[:, :200].transpose(0, 1, 3, 2)
    high = moments.copy(); high[:, 1:r+1] = 0
    rhs = np.zeros((174, r, 8, 16), dtype=np.int64)
    then = time.monotonic()
    for e in range(174):
        for branch, target in enumerate(targets[e]):
            rhs[e] = (rhs[e]+algebra.action(coeff[e, branch], high[target])) % ring.mod
    rhs_seconds = time.monotonic()-then
    then = time.monotonic(); answer = solve(rhs, order, diagonal, lower, upper, algebra)
    solve_seconds = time.monotonic()-then
    assert np.array_equal(answer, moments[:, 1:r+1])
    # Test an unrelated full-rank RHS to avoid merely checking one kernel.
    test = np.arange(174*r*8*2, dtype=np.int64).reshape(174, r, 8, 2) % ring.mod
    solved = solve(test, order, diagonal, lower, upper, algebra)
    residual = np.zeros_like(test)
    for (i, j), block in blocks.items(): residual[i] = (residual[i]+algebra.action(block, solved[j])) % ring.mod
    assert np.array_equal(residual, test)
    path = DATA/f'dyadic_sparse_low_r{r}_d121.npz'
    assert not path.exists()
    lk, uk = sorted(lower), sorted(upper)
    np.savez_compressed(path, P=np.array(200), r=np.array(r), order=np.array(order),
        diagonal=np.array([diagonal[i] for i in range(174)]), lower_keys=np.array(lk),
        lower=np.array([lower[k] for k in lk]), upper_keys=np.array(uk), upper=np.array([upper[k] for k in uk]))
    result = {'status':'pass', 'milestone':'D121', 'eliminated_positive_moments':r,
        'working_precision_pi':200, 'low_block_dimension':174*r,
        'coefficient_table_seconds':coefficient_seconds,
        'factorization':timing, 'sixteen_column_rhs_seconds':rhs_seconds,
        'sixteen_column_triangular_solve_seconds':solve_seconds,
        'actual_harmonic_columns_checked':16, 'actual_low_scalar_coefficients_checked':174*r*8*16,
        'unrelated_rhs_original_residual_checked':True,
        'unrelated_rhs_scalar_equations_checked':174*r*8*2,
        'factor_payload_bytes':sum(x.nbytes for x in list(diagonal.values())+list(lower.values())+list(upper.values())),
        'guaranteed_Schur_correction_gain_pi':r+1,
        'wall_seconds':time.monotonic()-start,
        'actual_moment_precision_increased':False, 'full_Schur_iteration_validated_for_this_r':False,
        'sources':[l.source(p) for p in [Path(__file__), Path(l.__file__),
            DATA/'dyadic_low_moment_block_d121.npz', DATA/'dyadic_low_moment_block_d121.json', bank_path, path]]}
    print('SPARSE_LOW_RESULT|'+json.dumps({k:v for k,v in result.items() if k!='sources'}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--moments', type=int, required=True)
    args = parser.parse_args(); out = DATA/f'dyadic_sparse_low_r{args.moments}_d121.json'
    assert not out.exists()
    out.write_text(json.dumps(build(args.moments), indent=2)+'\n')
    print('PASS|467_DYADIC_SPARSE_LOW_BLOCKS', flush=True)
