"""D128 bounded P=3200 original-map actions, with two polynomial backends.

The extension control uses actual P=1600 inputs and checks old overlaps.
Full and low-RHS controls use deterministic dense synthetic inputs.
None certifies a new harmonic column or costs a complete P=3200 solve.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
s = importlib.util.spec_from_file_location('streamed', ROOT / 'dembele/pari/516_dyadic_factor_and_map_controls.py')
c = importlib.util.module_from_spec(s)
s.loader.exec_module(c)
q, h, b, a, w = c.q, c.h, c.b, c.a, c.w
P = 3200


def build(phase, first, last):
    assert 0 <= first <= last < 174 and last - first < 6
    control, _ = h.read('dyadic_adaptive_kernel_control_d124')
    for path in (Path(a.__file__), a.CSOURCE, a.LIBRARY):
        expected = [r for r in control['sources'] if Path(r['path']) == path]
        assert len(expected) == 1 and h.source(path) == expected[0]
        h.PATHS.add(path)
    targets, params, path = b.parameters(P)
    h.PATHS.add(path)
    source = None
    if phase == 'extend':
        packet, _ = h.read('dyadic_weighted_P1600_col00_verified_d124')
        source = q.StateReader(packet['state_file'], 1600, 200)
        masses, _ = h.read('dyadic_harmonic_certificate_d111')
    count = 1600 if phase == 'extend' else P
    rows = 33 if phase == 'rhs' else P
    rings = {'ADAPTIVE': a.Ring(400), 'GMP': q.p.Ring(400)}
    timings, sha = [], hashlib.sha256()
    old_checks = 0
    for e in range(first, last + 1):
        outputs = []
        for backend, ring in rings.items():
            start = time.monotonic()
            total = [b.ZERO] * rows
            preparation = application = 0.0
            for branch, child in enumerate(targets[e]):
                if phase == 'extend':
                    values = source.row(child)
                    values[0] = (masses['harmonic_basis'][0][child] & ring.mask,) + (0,) * 7
                else:
                    values = b.k.data(1, P, 400, f'D128-dense-state{child}')[0]
                    if phase == 'rhs':
                        values[1:33] = [b.ZERO] * 32
                pars = params[e][branch]
                assert q.l.value([[pars[2]]], P) >= 1
                assert q.l.value([[ring.add(pars[0], ring.neg(ring.mul(pars[1], pars[2])))]], P) >= 1
                tick = time.monotonic()
                plan = q.l.Plan(ring, *pars, count, rows)
                preparation += time.monotonic() - tick
                tick = time.monotonic()
                total = ring.padd(total, plan.apply(values))
                application += time.monotonic() - tick
                del plan, values
            timings.append({'state': e, 'backend': backend, 'prepare_seconds': preparation,
                'apply_seconds': application, 'total_seconds': time.monotonic() - start})
            outputs.append(total)
        assert outputs[0] == outputs[1]
        if phase == 'extend':
            mask = (1 << 200) - 1
            assert [tuple(v & mask for v in x) for x in outputs[0][:1600]] == source.row(e)
            old_checks += 1600 * 8
        sha.update(b.pack([outputs[0]], 400))
        print('P3200_TRANSPORT|' + json.dumps({'phase': phase, 'state': e,
            'ADAPTIVE_seconds': timings[-2]['total_seconds'], 'GMP_seconds': timings[-1]['total_seconds']}), flush=True)
        del outputs, total
    if source is not None:
        source.close()
    return {'phase': phase, 'working_precision_pi': P, 'first_state': first, 'last_state': last,
        'input_moment_count': count, 'output_moment_count': rows,
        'input_kind': 'actual_P1600_canonical_lift_with_exact_masses' if phase == 'extend' else 'deterministic_dense_synthetic',
        'known_positive_low_inputs_zeroed': phase == 'rhs',
        'complete_backend_scalar_comparisons': (last - first + 1) * rows * 8,
        'old_P1600_actual_scalar_overlaps': old_checks,
        'answers_sha256': sha.hexdigest(), 'state_timings': timings,
        'decoded_input_state_cache_capacity': 1, 'maximum_prepared_plans_held': 1,
        'complete_original_state_coverage': False, 'complete_larger_solve_costed': False,
        'actual_harmonic_precision_increased': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', required=True, choices=('extend', 'full', 'rhs'))
    parser.add_argument('--first', required=True, type=int)
    parser.add_argument('--last', required=True, type=int)
    args = parser.parse_args()
    out = DATA / f'dyadic_P3200_transport_{args.phase}_e{args.first:03d}_{args.last:03d}_d128.json'
    assert not out.exists()
    start = time.monotonic()
    cert = build(args.phase, args.first, args.last)
    h.PATHS.update([Path(__file__), Path(c.__file__), Path(q.__file__), Path(w.__file__),
        Path(h.__file__), Path(b.__file__), Path(a.__file__), a.CSOURCE, a.LIBRARY,
        Path(q.l.__file__), Path(q.p.__file__), Path(q.p.f.__file__),
        Path(b.k.__file__), b.k.CSOURCE, b.k.LIBRARY])
    result = {'status': 'pass', 'milestone': 'D128', 'certificates': cert,
        'wall_seconds': time.monotonic() - start, 'peak_rss_bytes': w.peak_rss(),
        'sources': [h.source(path) for path in sorted(h.PATHS)]}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('sources', 'certificates')}), flush=True)
    print('PASS|526_DYADIC_PRECISION3200_TRANSPORT_CONTROL', flush=True)
