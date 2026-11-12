"""D142 fixed review of both height routes and transitive D141 provenance."""
import argparse
import ast
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
OUT = DATA/'P1600_two_height_review_d142.json'
HELPER = ROOT/'dembele/pari/597_P1600_proof_gap_review.py'
PATHS = {Path(__file__), HELPER}
spec = importlib.util.spec_from_file_location('d141_provenance', HELPER)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return prior.prior.raw_source(path)


def checked(refs):
    for ref in refs:
        assert source(ref['path']) == ref, ref['path']


def read(stem):
    p = DATA/(stem+'.json')
    source(p)
    result = json.loads(p.read_text())
    assert result['status'] == 'pass'
    return result


def graph(ref):
    assert prior.prior.raw_source(ref['path']) == ref
    d141 = json.loads(Path(ref['path']).read_text())
    assert d141['status'] == 'pass' and d141['independent_finite_review_complete']
    for item in d141['sources']:
        assert prior.prior.raw_source(item['path']) == item, item['path']
    inherited = prior.graph(d141['inherited_review'])
    assert len(d141['sources']) == 48
    return {'D141_direct_bindings': 48, **inherited}


def validate_job(row, driver, output_ref, args=()):
    checked([row['driver'], row['log'], *row['sources']])
    assert row['driver'] == source(ROOT/'dembele/pari'/driver)
    assert row['command'] == ['python3', row['driver']['path']]+list(args)
    assert row['status'] == 'pass' and row['exit_code'] == 0
    assert 0 < row['wall_seconds'] < row['timeout_seconds'] == 180
    assert row['private_process_group'] > 0 and row['timeout_terminates_process_group']
    lines = Path(row['log']['path']).read_text().splitlines()
    marks = [json.loads(s.split('|', 1)[1]) for s in lines if s.startswith('PHASE_METADATA|')]
    assert marks == [output_ref]
    assert any(s.startswith('PASS|'+driver[:3]+'_') for s in lines)


def receipt(stem, driver):
    packet = read(stem)
    row = read(stem+'_attempt01.job')
    validate_job(row, driver, source(DATA/(stem+'.json')))
    checked(packet['sources'])
    peak = packet.get('conservative_peak_rss_bytes', packet['peak_rss_bytes'])
    assert peak < 2*(1 << 30)
    return packet, {'receipt': source(DATA/(stem+'_attempt01.job.json')),
                    'wall_seconds': row['wall_seconds'], 'conservative_peak_rss_bytes': peak}


def build():
    tick = time.monotonic()
    parent_ref = source(DATA/'P1600_proof_gap_review_d141.json')
    inherited = graph(parent_ref)
    print('D142_TRANSITIVE_GRAPH_PASS', flush=True)
    completion = read('P1600_proof_gap_completion_d141')
    assert completion['fixed_review'] == parent_ref and completion['successful_bounded_jobs'] == 4
    assert len(completion['review_receipts']) == 2
    checked(completion['review_receipts'])
    for i, ref in enumerate(completion['review_receipts']):
        validate_job(json.loads(Path(ref['path']).read_text()), HELPER.name, parent_ref, [] if i == 0 else ['--check'])
    diagnostic, diag_job = receipt('P1600_two_height_routes_d142', '598_P1600_two_height_routes.py')
    audit, audit_job = receipt('P1600_height_routes_audit_d142', '599_P1600_height_routes_audit.py')
    assert diagnostic['inherited_review'] == parent_ref
    assert diagnostic['new_joint_affine_ratio_height_integer_bounds'] == [871, 3532]
    assert diagnostic['true_relation_space_height_integer_upper'] == 83240
    assert diagnostic['without_Clifford_height_integer_upper'] == 149277
    assert diagnostic['actual_height_upper_bound_established']
    assert audit['exact_small_lattice_controls'] == 50
    assert audit['arb_precision_bits'] == 192 and audit['Dedekind_Euler_cutoff'] == 10000
    assert len(audit['row_selection_cases']) == 3
    assert [x['order'] for x in audit['cone_differences']] == [1, 2, 3, 32]
    assert Q(audit['independent_Faltings_upper_interval'][1]) < Q(30039246, 1000000)
    assert Q(audit['independent_Faltings_upper_interval'][0]) > 29
    assert Q(audit['independent_true_relation_space_upper_interval'][1]) < 83240
    assert Q(audit['independent_true_relation_space_upper_interval'][0]) > 83239
    assert Q(audit['formal_Faltings_shift_if_other_RR_ingredients_hold_interval'][1]) < -3
    assert Q(audit['residual_needed_for_Faltings_29_interval'][1]) < Q(320138, 1000)
    for value in (diagnostic, audit):
        for key in ('Faltings_lower_29_proved', 'height_bound_at_most_623_proved',
                    'candidate_identification_proved', 'corrected_global_RR_constant_certified'):
            assert value[key] is False
    assert not audit['RR_model_remainder_assumed_zero']
    ledger = read('P1600_two_height_sources_d142')
    checked(ledger['sources'])
    assert len(ledger['external_sources']) == 4
    assert ledger['source_applicability_notes_are_mathematical_review_not_machine_verification']
    for number in (598, 599, 600):
        paths = list((ROOT/'dembele/pari').glob(str(number)+'_P1600_*.py'))
        assert len(paths) == 1
        source(paths[0])
        ast.parse(paths[0].read_text())
    return {'status': 'pass', 'milestone': 'D142', 'independent_finite_review_complete': True,
            'inherited_review': parent_ref, 'catalogue_graph_is_transitive': True, **inherited,
            'completed_input_jobs': 2, 'preserved_failed_input_jobs': 0,
            'input_receipts': [diag_job, audit_job],
            'true_relation_space_height_upper_bound': 83240,
            'true_relation_space_height_is_not_proved_above_623': True,
            'height_bound_at_most_623_proved': False,
            'Faltings_upper_bound': '30.039246', 'Faltings_lower_29_proved': False,
            'RR_residual_320_138_would_suffice_under_comparison': True,
            'corrected_global_RR_constant_certified': False,
            'normalizer_finite_model_comparison_proved': False,
            'positive_exact_quadric_vanishing_proved': False,
            'candidate_identification_proved': False, 'field_polynomial_constructed': False,
            'actual_harmonic_precision_increased': False, 'next_precision_bank_admitted': False,
            'actual_curve_spectral_calculation_started': False,
            'resource_caps_changed': False, 'full_bank_precision_pi': 1600, 'column0_precision_pi': 6400,
            'next_work': 'Establish the finite Hodge-line comparison for the actual normalizer and the order-3/order-32 cotangent terms; assess the resulting analytic target before any numerical spectral work. The existing jet-height estimate does not reach 623; exact structural identification remains an alternative.',
            'wall_seconds': time.monotonic()-tick, 'sources': [source(p) for p in sorted(PATHS)]}


if __name__ == '__main__':
    assert __debug__
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    tick = time.monotonic()
    if args.check:
        saved = json.loads(OUT.read_text())
        assert saved['status'] == 'pass' and saved['independent_finite_review_complete']
        checked(saved['sources'])
        inherited = graph(saved['inherited_review'])
        assert all(saved[k] == v for k, v in inherited.items())
    else:
        assert not OUT.exists()
        saved = build()
        saved['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        assert saved['peak_rss_bytes'] < 2*(1 << 30)
        with OUT.open('x') as f:
            f.write(json.dumps(saved, indent=2)+'\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    assert peak < 2*(1 << 30)
    print('D142_REVIEW_RESOURCES|' + json.dumps({'seconds': time.monotonic()-tick, 'peak_rss_bytes': peak}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(OUT)), flush=True)
    print('PASS|600_P1600_TWO_HEIGHT_REVIEW', flush=True)
