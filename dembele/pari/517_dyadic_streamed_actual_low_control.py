"""D126 combine selective state reads, one prepared map, and streamed factors.

Recompute every low moment for two actual P=800 harmonic columns, or the
first actual P=1600 correction, and check the original sparse equations.
This validates the combined low solve without advancing precision.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
s = importlib.util.spec_from_file_location('controls', ROOT / 'dembele/pari/516_dyadic_factor_and_map_controls.py')
c = importlib.util.module_from_spec(s)
s.loader.exec_module(c)
q, h, b, a, w = c.q, c.h, c.b, c.a, c.w


def run(phase):
    control, _ = h.read('dyadic_adaptive_kernel_control_d124')
    for path in (Path(a.__file__), a.CSOURCE, a.LIBRARY):
        expected = [x for x in control['sources'] if Path(x['path']) == path]
        assert len(expected) == 1 and h.source(path) == expected[0]
        h.PATHS.add(path)
    readers = []
    if phase == 'harmonic':
        stems = ['dyadic_staged_P800_col00_verified_d123', 'dyadic_weighted_P800_col01_verified_d125']
        for stem in stems:
            packet, _ = h.read(stem)
            assert packet['certificate']['original_full_residual_zero']
            readers.append(q.StateReader(packet['state_file'], 800, 100))
        harmonic, _ = h.read('dyadic_harmonic_certificate_d111')
    else:
        stems = ['dyadic_weighted_P1600_col00_step01_prepared_d124']
        packet, _ = h.read(stems[0])
        assert packet['input_count'] == 800 and packet['correction_power_of_two_shift'] == 100
        readers.append(q.StateReader(packet['operator_input_file'], 800, 100))
    columns = len(readers)
    targets, params, path = b.parameters(800)
    h.PATHS.add(path)
    groups = {}
    for e in range(174):
        for branch, child in enumerate(targets[e]):
            groups.setdefault(params[e][branch], []).append((e, child))
    ring = a.Ring(100)
    totals = [[[b.ZERO] * 33 for _ in range(174)] for _ in readers]
    prepare_seconds = apply_seconds = 0.0
    tick = time.monotonic()
    for number, (pars, destinations) in enumerate(groups.items()):
        begin = time.monotonic()
        plan = q.l.Plan(ring, *pars, 800, 33)
        prepare_seconds += time.monotonic() - begin
        for col, reader in enumerate(readers):
            for e, child in destinations:
                values = reader.row(child)
                values[1:33] = [b.ZERO] * 32
                begin = time.monotonic()
                totals[col][e] = ring.padd(totals[col][e], plan.apply(values))
                apply_seconds += time.monotonic() - begin
                del values
        del plan
        if number % 55 == 0:
            print('STREAMED_ACTUAL_LOW|' + json.dumps({'maps': number + 1,
                'seconds': time.monotonic() - tick}), flush=True)
    rhs_seconds = time.monotonic() - tick
    rhs = [[[totals[col][e][k] for col in range(columns)] for k in range(1, 33)] for e in range(174)]
    del totals
    algebra = b.Algebra(100)
    factors = c.FactorReader(100)
    tick = time.monotonic()
    answer = factors.solve(rhs, algebra)
    solve_seconds = time.monotonic() - tick
    factors.close()
    assert factors.decoded_blocks == 1226
    checked = masses = 0
    for col, reader in enumerate(readers):
        for e in range(174):
            expected = reader.row(e, 33)
            mass = harmonic['harmonic_basis'][col][e] if phase == 'harmonic' else 0
            assert expected[0] == (mass & ring.mask,) + (0,) * 7
            masses += 1
            for k in range(32):
                assert answer[e][k][col] == expected[k + 1]
                checked += 8
        reader.close()
    tick = time.monotonic()
    for e in range(174):
        value = answer[e]
        for branch, child in enumerate(targets[e]):
            original = b.coefficients(params[e][branch], 32, algebra)
            value = algebra.sub(value, algebra.mul(original, answer[child]))
            del original
        assert value == rhs[e]
    return {'phase': phase, 'input_stems': stems, 'actual_columns': columns,
        'working_modulus_bits': 100, 'input_moments': 800, 'low_positive_moments': 32,
        'full_known_low_scalar_comparisons': checked, 'original_sparse_residual_scalar_checks': checked,
        'exact_masses_checked': masses, 'distinct_prepared_maps': len(groups),
        'maximum_prepared_maps_held': 1, 'maximum_decoded_input_states_held': 1,
        'maximum_decoded_factor_blocks_held': 1, 'factor_blocks_decoded': factors.decoded_blocks,
        'rhs_prepare_seconds': prepare_seconds, 'rhs_apply_seconds': apply_seconds,
        'rhs_seconds_including_selective_reads': rhs_seconds,
        'factor_read_decode_seconds': factors.read_seconds, 'solve_seconds_including_decode': solve_seconds,
        'original_sparse_residual_seconds': time.monotonic() - tick,
        'complete_original_high_residual_still_required_for_new_refinement': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', required=True, choices=('harmonic', 'correction'))
    args = parser.parse_args()
    out = DATA / f'dyadic_streamed_actual_low_{args.phase}_d126.json'
    assert not out.exists()
    start = time.monotonic()
    certificate = run(args.phase)
    h.PATHS.update([Path(__file__), Path(c.__file__), Path(q.__file__), Path(w.__file__),
        Path(h.__file__), Path(b.__file__), Path(b.k.__file__), b.k.CSOURCE, b.k.LIBRARY,
        Path(q.l.__file__), Path(q.p.__file__), Path(q.p.f.__file__)])
    result = {'status': 'pass', 'milestone': 'D126', 'certificates': certificate,
        'wall_seconds': time.monotonic() - start, 'peak_rss_bytes': w.peak_rss(),
        'actual_moment_precision_increased': False,
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|517_DYADIC_STREAMED_ACTUAL_LOW_CONTROL', flush=True)
