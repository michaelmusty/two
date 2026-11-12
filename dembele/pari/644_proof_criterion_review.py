"""D155 fixed proof-criterion review, transitive replay and completion.

Finite arithmetic and file authentication are checked here. The geometric
arguments and reconciliation of external theorem applications are prose
proofs in the bound report, not mechanically verified propositions.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dembele/data/computed'
OUT = DATA / 'proof_criterion_review_d155.json'
COMPLETION = DATA / 'proof_criterion_completion_d155.json'
LEDGER = DATA / 'proof_criterion_sources_d155.json'
REPORT = ROOT / 'dembele/certificates/proof-criterion-review-d155.md'
HELPER = ROOT / 'dembele/pari/641_dyadic_pilot_timing_review.py'
PATHS = {Path(__file__), HELPER}
CACHE = {}
DOCS = ['HANDOFF.md', 'CLAUDE.md', 'README.md', 'DECISIONS.md',
        'REFERENCES.md', 'dembele/README.md', 'dembele/pari/README.md']


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


prior = module(HELPER, 'd155_inherited_catalogue')


def raw_source(path):
    path = Path(path).resolve()
    if path not in CACHE:
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            while chunk := stream.read(1 << 20):
                digest.update(chunk)
        CACHE[path] = {'path': str(path), 'sha256': digest.hexdigest()}
    return CACHE[path]


def source(path):
    path = Path(path).resolve()
    PATHS.add(path)
    return raw_source(path)


def checked(refs):
    for ref in refs:
        assert raw_source(ref['path']) == ref, ref['path']


def read(stem):
    path = DATA / (stem+'.json')
    source(path)
    value = json.loads(path.read_text())
    assert value['status'] == 'pass', stem
    return value


def receipt(stem, driver, args=(), suffix='_attempt01'):
    obj = read(stem)
    row = read(stem+suffix+'.job')
    expected = source(ROOT/'dembele/pari'/driver)
    assert row['driver'] == expected
    assert row['command'] == ['python3', expected['path']]+list(args)
    assert row['status'] == 'pass' and row['exit_code'] == 0
    assert 0 < row['wall_seconds'] <= row['timeout_seconds'] == 180
    assert row['timeout_terminates_process_group'] and row['private_process_group'] > 0
    for ref in [row['driver'], row['log'], *row['sources']]:
        assert source(ref['path']) == ref
    lines = Path(row['log']['path']).read_text().splitlines()
    assert [json.loads(s.split('|', 1)[1]) for s in lines if s.startswith('PHASE_METADATA|')] == [source(DATA/(stem+'.json'))]
    assert any(s.startswith('PASS|'+driver[:3]+'_') for s in lines)
    if 'peak_rss_bytes' in obj:
        assert obj['peak_rss_bytes'] <= 2*(1 << 30)
    return row, source(DATA/(stem+suffix+'.job.json'))


def graph():
    parent = read('dyadic_pilot_timing_review_d154')
    checked(parent['sources'])
    assert parent['independent_finite_review_complete'] and len(parent['sources']) == 36
    assert not parent['next_column_or_stage_admitted']
    inherited = prior.graph()
    assert all(parent[k] == v for k, v in inherited.items())
    done = read('dyadic_pilot_timing_completion_d154')
    assert done['fixed_review'] == source(DATA/'dyadic_pilot_timing_review_d154.json')
    assert done['successful_bounded_jobs_this_continuation'] == 12573
    assert done['failed_bounded_jobs_this_continuation'] == 0
    for suffix, args in [('_attempt01', []), ('_recheck01', ['--check'])]:
        receipt('dyadic_pilot_timing_review_d154', HELPER.name, args, suffix)
    receipt('dyadic_pilot_timing_completion_d154', HELPER.name, ['--finish'])
    return {'D154_direct_bindings': 36, **inherited,
            'inherited_review': source(DATA/'dyadic_pilot_timing_review_d154.json')}


def inputs():
    packets = []
    for stem, driver in [('proof_criterion_bounds_d155', '642_proof_criterion_bounds.py'),
                         ('proof_criterion_controls_d155', '643_proof_criterion_controls.py')]:
        obj = read(stem)
        checked(obj['sources'])
        row, ref = receipt(stem, driver)
        packets.append(obj)
    bounds, controls = packets
    first = module(ROOT/'dembele/pari/642_proof_criterion_bounds.py', 'd155_bounds_replay')
    replay = first.calculate()
    assert all(bounds[k] == v for k, v in replay.items())
    second = module(ROOT/'dembele/pari/643_proof_criterion_controls.py', 'd155_controls_replay')
    assert second.rank_replay() == controls['rank_replays']
    assert second.independent_bounds() == controls['independent_uncollected_height_thresholds']
    assert second.failure_controls() == controls['failure_controls']
    assert bounds['conditional_two_order_target'] == 10480
    assert [r['minor_size'] for r in controls['rank_replays']] == [45, 45]
    assert not controls['rank_replay_candidate_equations_read']
    assert not controls['rank_replay_production_ball_arithmetic_imported']
    sample = next(s for s in bounds['thresholds'][1]['samples'] if s['P'] == 10480)
    margin = tuple(map(Q, sample['strict_margin_interval']))
    log2 = tuple(map(Q, bounds['log2_interval']))
    assert margin[0] > 3*log2[1]/16
    assert margin[1] < 4*log2[0]/16
    assert Q('0.1693677259') < margin[0] < margin[1] < Q('0.1693677260')
    assert (2*10480+3310-33, 2*10480+2784-296) == (24237, 23448)
    assert (2*10480+3310-66, 2*10480+2784-592) == (24204, 23152)
    candidate = read('cm_frame_curve_verification')
    checked(candidate['sources'])
    for job in candidate['jobs']:
        checked([job['script'], job['log']])
        assert job['status'] == 'pass' and job['exit_code'] == 0
    geometry = candidate['smoothness']
    assert geometry['smooth_over_Q'] and geometry['geometrically_integral_over_Q_and_F31']
    assert geometry['genus'] == 16 and geometry['canonical_embedding']
    assert sorted(geometry['free_basis_degrees']) == [0]+[1]*14+[2]*14+[3]
    design = read('dyadic_precision_design_d120')['precision_design']
    assert design['nonanchor_evaluation_Smith_beta'] == [0]*8+[35]*8
    assert design['raw_four_jet_error_beta_assumption'] == 'E=2*P+32'
    assert design['frame_change_error_beta'] == design['quadric_coarse_error_beta'] == 'E-296'
    assert design['additional_required_eta_error_beta_at_least'] == 'E'
    assert design['additional_required_beta_ring_precision_at_least'] == '2*P+64'
    return {'conditional_two_order_sufficient_P': 10480,
            'strict_thresholds_multiple_of_8': [10416, 10480, 10552],
            'actual_rank45_certificates_replayed_at_2_bits': [96, 160],
            'actual_matrix_entries_replayed_per_certificate': 6528,
            'P10480_order2_strict_margin_interval': list(map(str, margin)),
            'additional_uniform_beta_digit_loss_three_still_passes': True,
            'additional_uniform_beta_digit_loss_four_fails': True,
            'exact_order0_CM_quadric_values_replayed': 91,
            'candidate_scheme_certificate_authenticated': True,
            'uniform_precision_propagation_offsets_rechecked': True,
            'Zhao_7_4_factor_reconciled_in_companion_proof': True,
            'reconciliation_author_confirmed': False,
            'rank_dimension_argument_uses_Q_descent': True,
            'formal_verification_of_geometry_or_external_theorems': False}


def links(path, text, missing=()):
    results = []
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if link.startswith(('http://', 'https://', '#')):
            continue
        target = (path.parent/link.split('#', 1)[0]).resolve()
        assert target.is_file() or target in missing, (path, link)
        results.append(target)
    return results


def build():
    inherited = graph()
    print('D155_TRANSITIVE_GRAPH_PASS', flush=True)
    values = inputs()
    report_links = links(REPORT, REPORT.read_text(), (OUT, LEDGER, COMPLETION))
    external = [
        {'url': 'https://arxiv.org/pdf/2309.08886', 'version': 'v1, 16 September 2023',
         'location': 'Theorems 6.1, 7.3, 7.4; page 25 visually checked',
         'use': 'Ramified CM Hodge identity; factor reconciled in report, not author-confirmed.'},
        {'url': 'https://annals.math.princeton.edu/wp-content/uploads/annals-v187-n2-p04-p.pdf',
         'location': 'Theorem 1.1, Corollary 2.6, Theorems 2.7 and 4.7',
         'use': 'Averaged and nearby CM heights; structural integral Hodge system and its metric.',
         'excluded_application': 'CM-point theorems requiring disjoint finite ramification.'},
        {'url': 'https://arxiv.org/pdf/1810.02637', 'location': 'Formula (1.11) and section 12',
         'use': 'Stable curve Faltings lower bound and matching determinant metric.'},
        {'url': 'https://www.math.u-bordeaux.fr/~qliu/articles/modcove.pdf',
         'location': 'Proposition 4.4; Remark 4.5',
         'use': 'Extension to stable models; no extension claim for minimal regular models.'}]
    reports = sorted(set(p for p in report_links if p.suffix == '.md'))
    ledger = {'status': 'pass', 'milestone': 'D155',
              'scope': 'Conditional base-curve criterion; no new precision or cost experiment.',
              'external_sources': external,
              'external_sources_and_geometric_proofs_mechanically_verified': False,
              'inspected_reports': [source(p) for p in reports],
              'sources': [source(REPORT)]}
    with LEDGER.open('x') as stream:
        stream.write(json.dumps(ledger, indent=2)+'\n')
    source(LEDGER)
    return {'status': 'pass', 'milestone': 'D155',
            'independent_finite_review_complete': True, 'catalogue_graph_is_transitive': True,
            **inherited, **values,
            'full_sixteen_column_bank_precision_pi': 1600,
            'column0_precision_pi': 6400, 'column2_precision_pi': 3200,
            'actual_harmonic_precision_increased': False,
            'positive_exact_quadric_vanishing_proved': False,
            'candidate_identification_proved': False, 'field_polynomial_constructed': False,
            'new_precision_bank_or_pilot_admitted': False, 'all_caps_retained': True,
            'finite_rational_transfer_search_remains_parked': True,
            'report_local_links_checked': len(report_links),
            'sources': [source(p) for p in sorted(PATHS)]}


def finish():
    saved = read(OUT.stem)
    checked(saved['sources'])
    resources, refs = [], []
    for suffix, args in [('_attempt01', []), ('_recheck01', ['--check'])]:
        row, ref = receipt(OUT.stem, Path(__file__).name, args, suffix)
        refs.append(ref)
        measures = [json.loads(s.split('|', 1)[1]) for s in Path(row['log']['path']).read_text().splitlines()
                    if s.startswith('D155_REVIEW_RESOURCES|')]
        assert len(measures) == 1 and measures[0]['peak_rss_bytes'] < 2*(1 << 30)
        resources.append({'receipt_wall_seconds': row['wall_seconds'], **measures[0]})
    targets = []
    for name in DOCS:
        path = ROOT/name
        block = path.read_text().split('<!-- D155 proof criterion checkpoint -->', 1)[1].split('<!-- End D155 proof criterion checkpoint -->', 1)[0]
        assert all(s in block for s in ['10480', '0.169', 'source 645 is next unused'])
        targets.extend(links(path, block, (COMPLETION,)))
    assert len(targets) == 28
    result = {k: v for k, v in saved.items() if k not in ['sources', 'wall_seconds', 'peak_rss_bytes']}
    result.update(completed_at=datetime.now(timezone.utc).isoformat(), fixed_review=source(OUT),
                  report=source(REPORT), source_applicability_ledger=source(LEDGER),
                  review_receipts=refs, review_resources=resources,
                  successful_bounded_jobs_this_continuation=5, failed_bounded_jobs_this_continuation=0,
                  completion_job_receipt_path=str(DATA/'proof_criterion_completion_d155_attempt01.job.json'),
                  entry_documents_updated=DOCS, current_artifact_links_checked=len(targets),
                  direct_source_bindings=len(saved['sources']), next_unused_source=645,
                  entry_document_hashes_intentionally_not_frozen=True)
    with COMPLETION.open('x') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    assert all(path.is_file() for path in targets)


if __name__ == '__main__':
    assert __debug__
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--check', action='store_true')
    modes.add_argument('--finish', action='store_true')
    args = parser.parse_args()
    tick = time.monotonic()
    output = OUT
    if args.finish:
        finish()
        output = COMPLETION
    elif args.check:
        saved = read(OUT.stem)
        checked(saved['sources'])
        inherited = graph()
        values = inputs()
        assert all(saved[k] == v for k, v in (inherited | values).items())
    else:
        assert not OUT.exists()
        saved = build()
        saved.update(wall_seconds=time.monotonic()-tick,
                     peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024))
        assert saved['peak_rss_bytes'] <= 2*(1 << 30)
        with OUT.open('x') as stream:
            stream.write(json.dumps(saved, indent=2)+'\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform == 'darwin' else 1024)
    assert peak <= 2*(1 << 30)
    print('D155_REVIEW_RESOURCES|'+json.dumps({'wall_seconds': time.monotonic()-tick, 'peak_rss_bytes': peak}), flush=True)
    print('PHASE_METADATA|'+json.dumps(raw_source(output)), flush=True)
    print('PASS|644_PROOF_CRITERION_REVIEW', flush=True)
