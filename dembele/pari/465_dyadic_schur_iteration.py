"""D121 full first-moment Schur iteration and original-residual control.

Recover one frozen P=200 harmonic column from its P=184 reduction. This
validates an algorithm, not a new increase of certified moment precision.
"""
import importlib.util
import json
from pathlib import Path
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'


def module(name, file):
    s = importlib.util.spec_from_file_location(name, ROOT/'dembele/pari'/file)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


l = module('low', '464_dyadic_low_moment_block.py')
g = module('transport', '463_dyadic_gmp_transport.py')


def build():
    start = time.monotonic(); full = l.Ring()
    binary = DATA/'dyadic_low_moment_block_d121.npz'
    saved = np.load(binary)
    params, targets, inverse = saved['params'], saved['targets'], saved['inverse']
    bank_path = DATA/'dyadic_precision200_d115.json'
    bank = json.loads(bank_path.read_text())
    truth = np.array(bank['state_moments_power_basis'], dtype=np.int64)[:, :200, 0, :]
    assert truth.shape == (174, 200, 8)
    small_cache = {}

    def low_solve(moment, ring):
        # Treat m1 as the eliminated variable, so its input coefficient is 0.
        bits = ring.bits
        if bits not in small_cache:
            pars = params % ring.mod
            delta = (pars[:, :, 0]-ring.mul(pars[:, :, 1], pars[:, :, 2])) % ring.mod
            cut = 8*bits
            weights = np.zeros((174, 2, cut, 8), dtype=np.int64)
            weights[:, :, 0] = pars[:, :, 1]
            value = delta.copy()
            for k in range(1, cut):
                if k >= 2: weights[:, :, k] = value
                value = ring.mul(value, -pars[:, :, 2] % ring.mod)
            assert not np.any(value)
            small_cache[bits] = ring.matrix(weights).transpose(0, 1, 3, 2, 4).reshape(174, 2, 8, 8*cut)
        operators = small_cache[bits]
        cut = 8*bits
        assert 8*cut*(ring.mod-1)**2 < 2**63
        rhs = np.zeros((174, 8, 1), dtype=np.int64)
        for e in range(174):
            for branch, target in enumerate(targets[e]):
                rhs[e, :, 0] = (rhs[e, :, 0]+operators[e, branch] @ moment[target, :cut].reshape(-1)) % ring.mod
        return ring.action(inverse % ring.mod, rhs)[:, :, 0]

    def apply(moment):
        gain = full.val(moment)
        if gain == 200:
            return np.zeros_like(moment), {'gain_pi':gain, 'zero_action':True}
        # Divide by the largest coefficientwise power of two justified by
        # the common pi-valuation. This division is exact in Z.
        shift = gain//8
        assert not np.any(moment & ((1 << shift)-1))
        bits = 25-shift
        cut = min(200, 8*bits)
        ring = g.Ring(bits)
        reduced = [[tuple(map(int, row)) for row in edge[:cut]] for edge in (moment >> shift)]
        pars = params % ring.mod
        answer = np.zeros_like(moment)
        then = time.monotonic()
        for e in range(174):
            total = [g.f.ZERO]*200
            for branch, target in enumerate(targets[e]):
                p = [tuple(map(int, x)) for x in pars[e, branch]]
                total = ring.padd(total, ring.transform(reduced[target], *p, 200))
            answer[e] = np.array(total, dtype=np.int64) << shift
        return answer, {'gain_pi':gain, 'coefficient_shift_bits':shift,
                        'input_cutoff_count':cut, 'active_modulus_bits':bits,
                        'wall_seconds':time.monotonic()-then}

    current = truth % (1 << 23)
    current[:, 0] = truth[:, 0]
    current[:, 1] = low_solve(current, full)
    assert full.val((current-truth) % full.mod) >= 184
    first, first_timing = apply(current)
    difference = (first-current) % full.mod
    assert not np.any(difference[:, :2])
    gains, timings = [], []
    while np.any(difference[:, 2:]):
        gain = full.val(difference[:, 2:])
        assert gain >= 184 and len(gains) < 8
        # Fill the low part of this Schur correction, preserving masses.
        shift = gain//8; bits = 25-shift
        assert not np.any(difference & ((1 << shift)-1))
        reduced = difference >> shift
        reduced[:, 1] = low_solve(reduced, l.Ring(bits))
        correction = reduced << shift
        current = (current+correction) % full.mod
        next_difference, timing = apply(correction)
        assert not np.any(next_difference[:, 0])
        next_difference[:, 1] = 0
        next_gain = full.val(next_difference[:, 2:])
        assert next_gain >= min(200, gain+2)
        gains.append({'before_pi':gain, 'after_pi':next_gain})
        timings.append(timing)
        difference = next_difference
        print('SCHUR_GAIN|'+json.dumps(gains[-1]), flush=True)
    assert np.array_equal(current, truth)
    # Reapply the ORIGINAL full operator, not the Schur recurrence.
    final, final_timing = apply(current)
    assert np.array_equal(final, current)
    result = {'status':'pass', 'milestone':'D121', 'eliminated_positive_moments':1,
        'working_precision_pi':200, 'seed_precision_pi':184,
        'harmonic_basis_column':0, 'state_equations_checked':174,
        'recovered_scalar_coefficients':174*200*8,
        'successive_Schur_correction_gains':gains,
        'expected_minimum_gain_per_step':2,
        'original_operator_final_residual_zero':True,
        'exact_overlap_with_entire_frozen_column':True,
        'first_full_action':first_timing, 'correction_actions':timings,
        'final_full_action':final_timing, 'wall_seconds':time.monotonic()-start,
        'no_dense_high_moment_operator_table_used':True,
        'actual_moment_precision_increased':False,
        'sources':[l.source(p) for p in [Path(__file__), Path(l.__file__), Path(g.__file__), binary,
            bank_path, DATA/'dyadic_low_moment_block_d121.json']]}
    print('SCHUR_CONTROL|'+json.dumps({k:v for k,v in result.items() if k!='sources'}), flush=True)
    return result


if __name__ == '__main__':
    out = DATA/'dyadic_schur_iteration_d121.json'
    assert not out.exists()
    out.write_text(json.dumps(build(), indent=2)+'\n')
    print('PASS|465_DYADIC_SCHUR_ITERATION', flush=True)
