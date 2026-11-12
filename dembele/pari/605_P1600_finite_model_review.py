"""D143 fixed review: CM constants, dyadic model and full D142 provenance."""
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
OUT = DATA/'P1600_finite_model_review_d143.json'
HELPER = ROOT/'dembele/pari/600_P1600_two_height_review.py'
PATHS = {Path(__file__), HELPER}
spec = importlib.util.spec_from_file_location('d142_provenance', HELPER)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def raw_source(path):
    path = Path(path).resolve()
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return raw_source(path)


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
    assert raw_source(ref['path']) == ref
    parent = json.loads(Path(ref['path']).read_text())
    assert parent['status'] == 'pass' and parent['independent_finite_review_complete']
    for item in parent['sources']:
        assert raw_source(item['path']) == item, item['path']
    inherited = prior.graph(parent['inherited_review'])
    assert len(parent['sources']) == 38
    return {'D142_direct_bindings': 38, **inherited}


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
    peak = packet['conservative_peak_rss_bytes']
    assert peak < 2*(1 << 30)
    return packet, {'receipt': source(DATA/(stem+'_attempt01.job.json')),
                    'wall_seconds': row['wall_seconds'], 'conservative_peak_rss_bytes': peak}


def overlaps(a,b):
    return Q(a[0]) <= Q(b[1]) and Q(b[0]) <= Q(a[1])


def build():
    tick = time.monotonic()
    parent_ref = source(DATA/'P1600_two_height_review_d142.json')
    inherited = graph(parent_ref)
    print('D143_TRANSITIVE_GRAPH_PASS', flush=True)
    completion = read('P1600_two_height_completion_d142')
    assert completion['fixed_review'] == parent_ref and completion['successful_bounded_jobs'] == 4
    checked(completion['review_receipts'])
    for i, ref in enumerate(completion['review_receipts']):
        validate_job(json.loads(Path(ref['path']).read_text()), HELPER.name, parent_ref, [] if i == 0 else ['--check'])
    names = [
        ('P1600_elliptic_heights_d143','601_P1600_elliptic_heights.py'),
        ('P1600_elliptic_height_audit_d143','602_P1600_elliptic_height_audit.py'),
        ('P1600_dyadic_model_diagnostic_d143','603_P1600_dyadic_model_diagnostic.py'),
        ('P1600_dyadic_model_audit_d143','604_P1600_dyadic_model_audit.py')]
    packets, receipts = [], []
    for stem, driver in names:
        packet, job = receipt(stem, driver)
        packets.append(packet); receipts.append(job)
    heights, height_audit, model, model_audit = packets
    assert heights['arb_precision_bits'] == 192 and height_audit['arb_precision_bits'] == 224
    assert height_audit['independent_primitive_character_construction']
    assert height_audit['independent_number_field_discriminants']
    assert [row['elliptic_order'] for row in heights['CM_heights']] == [3,32]
    for a,b in zip(heights['CM_heights'],height_audit['CM_fields']):
        assert a['conductors'] == b['primitive_conductors']
        assert a['CM_field_discriminant'] == b['field_discriminant']
        for ka,kb in [('finite_L_log_derivative_interval','L_log_derivative_interval'),
                      ('absolute_Hodge_height_interval','Hodge_height_interval'),
                      ('cotangent_height_upper_interval','cotangent_upper_interval')]:
            assert overlaps(a[ka],b[kb])
    assert height_audit['strict_upper_bounds'] == {'H3':'987/250','H32':'24843/250','Psi':'82423/500','remaining_target':'60623/125'}
    assert Q(height_audit['total_cotangent_upper_interval'][1]) < Q(82423,500)
    assert [r['order'] for r in height_audit['changed_frame_jet_controls']] == [2,3,32]
    assert model['all_component_degree_identities_hold']
    assert model['component_degree_defects'] == ['0']*58
    assert model['Hodge_degree'] == model['orbifold_degree'] == '1455/32'
    expected = [12,15,8,18,25,5,2,2,1,1]+[0]*48
    assert [r['different_coefficient'] for r in model['components']] == expected
    assert model_audit['independent_grounded_Laplacian_solution'] == list(map(str,expected))
    n3 = [0]*58
    n3[0] = 1
    for j in range(34,38):
        n3[j] = 2
    assert model_audit['order3_points_by_component'] == n3
    assert sum(len(row['local_terms']) for row in model['components']) == 106
    assert all(t['difference_valuation_b'] < t['certified_error_lower']
               for row in model['components'] for t in row['local_terms'])
    assert model['different_graph_energy'] == '339/16'
    assert model_audit['coarse_correction_coefficient_b'] == '-153/4'
    assert model_audit['tail_correction_coefficient_b'] == '16955/768'
    assert model_audit['minimal_regular_model_correction_coefficient_b'] == '-12421/768'
    assert model_audit['E_model_coefficient_log2'] == '-12421/6144'
    assert overlaps(model['E_model_candidate_interval'],model_audit['E_model_interval'])
    assert Q(model_audit['E_model_interval'][1]) < 0
    assert model_audit['E_model_computed'] and model_audit['E_model_sign_proved']
    assert model_audit['delta_other'] == 0 and model_audit['good_reduction_away_from_2']
    assert model_audit['safe_sufficient_negative_target'] == '-97277/200'
    assert model_audit['equivalent_sufficient_log_CZ_plus_I_over6_upper'] == '-97277/1200'
    assert Q(model_audit['sufficient_I_plus_spectral_upper_target_interval'][0]) > -Q(97277,200)
    for packet in packets:
        assert not packet['Faltings_lower_29_proved'] and not packet['candidate_identification_proved']
    ledger = read('P1600_finite_model_sources_d143')
    checked(ledger['sources'])
    assert len(ledger['external_sources']) == 6
    assert ledger['source_applicability_notes_are_mathematical_review_not_machine_verification']
    assert ledger['normalizer_finite_model_comparison_proved'] and ledger['elliptic_cotangent_bounds_proved']
    assert not ledger['corrected_global_RR_constant_certified'] and not ledger['full_intersection_upper_bound_proved']
    for driver in [name for stem,name in names]+[Path(__file__).name]:
        p = ROOT/'dembele/pari'/driver
        source(p); ast.parse(p.read_text())
    return {'status':'pass','milestone':'D143','independent_finite_review_complete':True,
            'inherited_review':parent_ref,'catalogue_graph_is_transitive':True,**inherited,
            'completed_input_jobs':4,'preserved_failed_input_jobs':0,'input_receipts':receipts,
            'normalizer_finite_model_comparison_proved':True,'E_model_coefficient_log2':'-12421/6144',
            'elliptic_cotangent_bounds_proved':True,'cotangent_strict_upper_bounds':{'H3':'3.948','H32':'99.372','Psi':'164.846'},
            'good_reduction_away_from_2':True,'delta_other':0,
            'sufficient_I_plus_6_log_CZ_upper_bound_under_corrected_RR':'-486.385',
            'full_intersection_upper_bound_proved':False,'corrected_global_RR_constant_certified':False,
            'Faltings_lower_29_proved':False,'height_bound_at_most_623_proved':False,
            'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,
            'field_polynomial_constructed':False,'actual_harmonic_precision_increased':False,
            'next_precision_bank_admitted':False,'actual_curve_spectral_calculation_started':False,
            'resource_caps_changed':False,'full_bank_precision_pi':1600,'column0_precision_pi':6400,
            'next_work':'Bound the full elliptic-section intersection term and reconcile the complete corrected global RR constant; assess a certified analytic inequality against I+6 average(log(C_corrected Zprime(1))) <= -486.385. No new spectral or precision-bank job is admitted. Exact structural identification remains an alternative.',
            'wall_seconds':time.monotonic()-tick,'sources':[source(p) for p in sorted(PATHS)]}


if __name__ == '__main__':
    assert __debug__
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true')
    args = ap.parse_args()
    tick = time.monotonic()
    if args.check:
        saved = json.loads(OUT.read_text())
        assert saved['status'] == 'pass' and saved['independent_finite_review_complete']
        checked(saved['sources'])
        inherited = graph(saved['inherited_review'])
        assert all(saved[k] == v for k,v in inherited.items())
    else:
        assert not OUT.exists()
        saved = build()
        saved['peak_rss_bytes'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
        assert saved['peak_rss_bytes'] < 2*(1 << 30)
        with OUT.open('x') as f:
            f.write(json.dumps(saved,indent=2)+'\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    assert peak < 2*(1 << 30)
    print('D143_REVIEW_RESOURCES|'+json.dumps({'seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(source(OUT)),flush=True)
    print('PASS|605_P1600_FINITE_MODEL_REVIEW',flush=True)
