"""D121 full sparse-block Schur controls with precision-aware corrections."""
import argparse
import importlib.util
import json
from pathlib import Path
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'


def module(name, filename):
    s = importlib.util.spec_from_file_location(name, ROOT/'dembele/pari'/filename)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


b = module('blocks', '467_dyadic_sparse_low_blocks.py')
p = module('prepared', '466_dyadic_prepared_transport.py')


def build(r):
    assert r in (8, 32, 64)
    begin = time.monotonic(); full = b.l.Ring()
    state = np.load(DATA/'dyadic_low_moment_block_d121.npz')
    params, targets = state['params'], state['targets']
    path = DATA/f'dyadic_sparse_low_r{r}_d121.npz'
    fact = np.load(path)
    order = fact['order'].tolist()
    baseD, baseL, baseU = fact['diagonal'], fact['lower'], fact['upper']
    lk, uk = fact['lower_keys'].tolist(), fact['upper_keys'].tolist()
    bank_path = DATA/'dyadic_precision200_d115.json'
    bank = json.loads(bank_path.read_text())
    truth = np.array(bank['state_moments_power_basis'], dtype=np.int64)[:, :200, 0, :]
    del bank
    low_times = []

    def low_solve(moment, bits):
        cut = 8*bits
        # All nonmass input moments here have indices >=r+1. If they lie
        # beyond the contraction cutoff their contribution is exactly zero.
        if not np.any(moment[:, 0]) and cut <= r+1:
            return np.zeros((174, r, 8), dtype=np.int64)
        ring = b.l.Ring(bits); alg = b.Algebra(ring); start = time.monotonic()
        mask = ring.mod-1
        D = baseD if bits == 25 else baseD & mask
        L = baseL if bits == 25 else baseL & mask
        U = baseU if bits == 25 else baseU & mask
        diagonal = {i:D[i] for i in range(174)}
        lower = {tuple(key):L[i] for i, key in enumerate(lk)}
        upper = {tuple(key):U[i] for i, key in enumerate(uk)}
        coefficient = b.coefficients(ring, params & mask, r, cut)
        rhs = np.zeros((174, r, 8, 1), dtype=np.int64)
        indices = [0]+list(range(r+1, cut))
        for e in range(174):
            for branch, j in enumerate(targets[e]):
                rhs[e] = (rhs[e]+alg.action(coefficient[e, branch][:, indices], moment[j, indices, :, None])) & mask
        solved = b.solve(rhs, order, diagonal, lower, upper, alg)[:, :, :, 0]
        low_times.append({'modulus_bits':bits, 'input_indices_used':len(indices), 'wall_seconds':time.monotonic()-start})
        return solved

    def apply(moment):
        gain = full.val(moment)
        if gain == 200: return np.zeros_like(moment), {'gain_pi':gain, 'zero_action':True}
        shift = gain//8; bits = 25-shift; cut = 8*bits
        assert not np.any(moment & ((1 << shift)-1))
        reduced = moment >> shift
        if not np.any(reduced[:, :cut]):
            return np.zeros_like(moment), {'gain_pi':gain, 'input_cutoff_count':cut,
                'zero_action_by_contraction_cutoff':True}
        ring = p.Ring(bits)
        values = [[tuple(map(int, row)) for row in edge[:cut]] for edge in reduced]
        pars = params & ring.mask
        result = np.zeros_like(moment); start = time.monotonic(); plans = {}
        for e in range(174):
            total = [p.f.ZERO]*200
            for branch, j in enumerate(targets[e]):
                key = tuple(tuple(map(int, x)) for x in pars[e, branch])
                if key not in plans: plans[key] = p.Plan(ring, *key, cut, 200)
                total = ring.padd(total, plans[key].apply(values[j]))
            result[e] = np.array(total, dtype=np.int64) << shift
        return result, {'gain_pi':gain, 'active_modulus_bits':bits, 'input_cutoff_count':cut,
            'distinct_plans':len(plans), 'wall_seconds':time.monotonic()-start}

    seed = 64 if r >= 32 else 168
    current = truth % (1 << (seed//8)); current[:, 0] = truth[:, 0]
    current[:, 1:r+1] = low_solve(current, 25)
    assert full.val((current-truth) % full.mod) >= seed
    initial, initial_time = apply(current)
    difference = (initial-current) % full.mod
    assert not np.any(difference[:, :r+1])
    gains, action_times = [], []
    while np.any(difference[:, r+1:]):
        gain = full.val(difference[:, r+1:])
        assert gain >= seed and len(gains) < (200-seed+r)//(r+1)
        shift = gain//8; bits = 25-shift
        assert not np.any(difference & ((1 << shift)-1))
        reduced = difference >> shift
        reduced[:, 1:r+1] = low_solve(reduced, bits)
        correction = reduced << shift
        current = (current+correction) % full.mod
        difference, timing = apply(correction)
        assert not np.any(difference[:, 0])
        difference[:, 1:r+1] = 0
        after = full.val(difference[:, r+1:])
        assert after >= min(200, gain+r+1)
        gains.append({'before_pi':gain, 'after_pi':after}); action_times.append(timing)
        print('BLOCK_SCHUR_GAIN|'+json.dumps({'r':r, **gains[-1]}), flush=True)
    assert np.array_equal(current, truth)
    checked, final_time = apply(current)
    assert np.array_equal(checked, current)
    result = {'status':'pass', 'milestone':'D121', 'eliminated_positive_moments':r,
        'working_precision_pi':200, 'seed_precision_pi':seed, 'harmonic_basis_column':0,
        'successive_correction_gains':gains, 'minimum_correction_gain_pi':r+1,
        'original_operator_final_residual_zero':True,
        'entire_frozen_column_recovered':True, 'scalar_coefficients_checked':174*200*8,
        'initial_action':initial_time, 'correction_actions':action_times, 'final_action':final_time,
        'low_block_solves':low_times, 'wall_seconds':time.monotonic()-begin,
        'actual_moment_precision_increased':False,
        'sources':[b.l.source(x) for x in [Path(__file__), Path(b.__file__), Path(p.__file__),
            path, DATA/f'dyadic_sparse_low_r{r}_d121.json', DATA/'dyadic_low_moment_block_d121.npz', bank_path]]}
    print('BLOCK_SCHUR_CONTROL|'+json.dumps({k:v for k,v in result.items() if k!='sources'}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--moments', type=int, required=True)
    args = parser.parse_args(); out = DATA/f'dyadic_block_schur_r{args.moments}_d121.json'
    assert not out.exists()
    out.write_text(json.dumps(build(args.moments), indent=2)+'\n')
    print('PASS|468_DYADIC_BLOCK_SCHUR_ITERATION', flush=True)
