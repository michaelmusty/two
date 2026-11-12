"""D141 fixed review, including complete transitive D140 provenance.

Finite arithmetic is independently audited by source 596. This review
binds that audit, the two diagnosed failures, proof and source ledger,
while explicitly retaining all unproved geometric-height hypotheses.
"""
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
OUT = DATA/'P1600_proof_gap_review_d141.json'
HELPER = ROOT/'dembele/pari/592_dyadic_P1600_recognition_review.py'
PATHS = {Path(__file__), HELPER, ROOT/'dembele/certificates/P1600-proof-gap-d141.md'}
spec = importlib.util.spec_from_file_location('d140_provenance', HELPER)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return prior.raw_source(path)


def checked(refs):
    for ref in refs:
        assert source(ref['path']) == ref, ref['path']


def read(stem, status='pass'):
    path = DATA/(stem+'.json')
    source(path)
    result = json.loads(path.read_text())
    assert result['status'] == status, stem
    return result


def graph(ref):
    assert prior.raw_source(ref['path']) == ref
    d140 = json.loads(Path(ref['path']).read_text())
    assert d140['status'] == 'pass' and d140['recognition_complete']
    assert d140['same_saturated_integer_lattice_as_candidate']
    for item in d140['sources']:
        assert prior.raw_source(item['path']) == item, item['path']
    inherited = prior.inherited_graph(d140['inherited_review'])
    assert len(d140['sources']) == 80
    return {'D140_direct_bindings': 80, **inherited}


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
    assert packet['peak_rss_bytes'] < 2*(1 << 30)
    return packet, {'receipt': source(DATA/(stem+'_attempt01.job.json')),
                    'wall_seconds': row['wall_seconds'], 'peak_rss_bytes': packet['peak_rss_bytes']}


def failed_receipts():
    specs = [('P1600_proof_gap_diagnostics_d141', '593_P1600_proof_gap_diagnostics.py',
              'assert candidate_covolume_upper <= threshold'),
             ('P1600_proof_gap_audit_d141', '595_P1600_proof_gap_audit.py',
              "AttributeError: 'float' object has no attribute 'denominator'")]
    refs = []
    for stem, driver, reason in specs:
        row = read(stem+'_attempt01.job', 'failed')
        checked([row['driver'], row['log'], row['failed_driver_snapshot'], *row['sources']])
        assert row['driver'] == source(ROOT/'dembele/pari'/driver)
        assert row['driver']['sha256'] == row['failed_driver_snapshot']['sha256']
        assert row['command'] == ['python3', row['driver']['path']]
        assert row['exit_code'] == 1 and 0 < row['wall_seconds'] < row['timeout_seconds'] == 180
        assert row['private_process_group'] > 0 and row['timeout_terminates_process_group']
        text = Path(row['log']['path']).read_text()
        assert reason in text and 'PHASE_METADATA|' not in text
        assert not (DATA/(stem+'.json')).exists()
        refs.append(source(DATA/(stem+'_attempt01.job.json')))
    return refs


def build():
    tick = time.monotonic()
    parent_ref = source(DATA/'dyadic_P1600_recognition_review_d140.json')
    inherited = graph(parent_ref)
    print('D141_TRANSITIVE_GRAPH_PASS', flush=True)
    completion = read('dyadic_P1600_recognition_completion_d140')
    assert completion['fixed_review'] == parent_ref and completion['successful_bounded_jobs'] == 13
    assert len(completion['review_receipts']) == 2
    checked(completion['review_receipts'])
    for i, ref in enumerate(completion['review_receipts']):
        validate_job(json.loads(Path(ref['path']).read_text()), HELPER.name, parent_ref, [] if i == 0 else ['--check'])
    failed = failed_receipts()
    diagnostic, diag_job = receipt('P1600_proof_gap_diagnostics_r2_d141', '594_P1600_proof_gap_diagnostics_revision.py')
    audit, audit_job = receipt('P1600_proof_gap_audit_r2_d141', '596_P1600_proof_gap_audit_revision.py')
    assert diagnostic['inherited_review'] == parent_ref
    assert audit['controls'] == {'coefficient_matrices_enumerated': 6561, 'nonzero_wedges': 6240,
                                  'outside_wedges_checked': 6192, 'strict_boundary_rejected': True}
    for summary in audit['exterior_review']:
        assert summary['training_2_bits'] in (96, 160)
        assert summary['independently_replayed_Gram_minors'] == list(range(1, 92))
        assert summary['outside_count_cases_checked'] == 45
    assert audit['height_review']['new_integer_targets'] == [28, 28, 29]
    assert audit['height_review']['uncollected_Faltings_expression_checked']
    assert audit['height_review']['historical_D120_exclusion_preserved']
    assert audit['height_review']['no_geometric_height_hypothesis_established']
    exts = diagnostic['exterior_lattice_certificates']
    assert [x['training_2_bits'] for x in exts] == [96, 160]
    assert Q(exts[1]['sufficient_strict_log_covolume_interval'][0]) > 623
    assert [x['candidate_covolume_upper_within_max_Pluecker_threshold'] for x in exts] == [False, True]
    budgets = diagnostic['section_budget_diagnostics']
    assert budgets['recognized_basis_max_coefficient_l1'] == {'96': 30460, '160': 29299}
    assert [x['Faltings_sufficient_integer_lower_bound'] for x in budgets['rows']] == [28, 28, 29]
    assert [x['recognized_basis_uniform_sufficient_beta'] for x in budgets['rows']] == [25146, 25260, 25367]
    assert [x['unit_cost_and_radius_one_optimistic_sufficient_beta'] for x in budgets['rows']] == [21874, 21976, 22070]
    assert budgets['Faltings_lower_29_proved'] is False and budgets['either_hypothesis_proved'] is False
    for value in (diagnostic, audit):
        for key in ('candidate_identification_proved', 'true_ideal_height_bound_proved', 'actual_harmonic_precision_increased'):
            assert value[key] is False
    ledger = read('P1600_proof_gap_sources_d141')
    checked(ledger['sources'])
    assert len(ledger['external_sources']) == 5
    assert ledger['source_applicability_notes_are_mathematical_review_not_machine_verification']
    for key in ('candidate_identification_proved', 'Faltings_lower_29_proved', 'true_ideal_height_bound_proved'):
        assert ledger[key] is False
    for path in sorted((ROOT/'dembele/pari').glob('59[3-7]_P1600_proof_gap_*.py')):
        source(path)
        ast.parse(path.read_text())
    return {'status': 'pass', 'milestone': 'D141', 'independent_finite_review_complete': True,
            'inherited_review': parent_ref, 'catalogue_graph_is_transitive': True, **inherited,
            'completed_input_jobs': 2, 'preserved_failed_input_jobs': 2,
            'input_receipts': [diag_job, audit_job], 'preserved_failed_receipts': failed,
            'exterior_log_height_623_would_identify_quadratic_space': True,
            'Faltings_lower_29_would_suffice_at_P1600': True,
            'Faltings_critical_intervals': [x['Faltings_strict_critical_value_interval'] for x in budgets['rows']],
            'true_ideal_height_bound_proved': False, 'Faltings_lower_29_proved': False,
            'positive_exact_quadric_vanishing_proved': False, 'candidate_identification_proved': False,
            'field_polynomial_constructed': False, 'actual_harmonic_precision_increased': False,
            'next_precision_bank_admitted': False, 'resource_caps_changed': False,
            'full_bank_precision_pi': 1600, 'column0_precision_pi': 6400,
            'published_modular_height_is_not_used_as_Faltings_height': True,
            'orbifold_cone_constant_reconciliation_remains_required': True,
            'next_work': 'Derive a corrected arithmetic Riemann-Roch comparison for the actual normalizer curve, retaining the finite-model, elliptic-fibre, metric and analytic terms; assess whether it can prove h_Fal above 28.084618 before any numerical spectral work. A true relation-space height bound at most 623 is the alternative.',
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
        saved['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
        assert saved['peak_rss_bytes'] < 2*(1 << 30)
        with OUT.open('x') as f:
            f.write(json.dumps(saved, indent=2)+'\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    assert peak < 2*(1 << 30)
    print('D141_REVIEW_RESOURCES|' + json.dumps({'seconds': time.monotonic()-tick, 'peak_rss_bytes': peak}), flush=True)
    print('PHASE_METADATA|' + json.dumps(source(OUT)), flush=True)
    print('PASS|597_P1600_PROOF_GAP_REVIEW', flush=True)
