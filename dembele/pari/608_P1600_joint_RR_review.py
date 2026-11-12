"""D144 fixed review: joint adjunction, compact normalization and D143 provenance."""
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

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'dembele/data/computed'
OUT=DATA/'P1600_joint_RR_review_d144.json'
HELPER=ROOT/'dembele/pari/605_P1600_finite_model_review.py'
PATHS={Path(__file__),HELPER}
spec=importlib.util.spec_from_file_location('d143_provenance',HELPER)
prior=importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def raw_source(path):
    p=Path(path).resolve()
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}


def source(path):
    p=Path(path).resolve();PATHS.add(p)
    return raw_source(p)


def checked(refs):
    for ref in refs:
        assert source(ref['path'])==ref,ref['path']


def read(stem):
    p=DATA/(stem+'.json');source(p)
    result=json.loads(p.read_text())
    assert result['status']=='pass'
    return result


def graph(ref):
    assert raw_source(ref['path'])==ref
    parent=json.loads(Path(ref['path']).read_text())
    assert parent['status']=='pass' and parent['independent_finite_review_complete']
    for item in parent['sources']:
        assert raw_source(item['path'])==item,item['path']
    inherited=prior.graph(parent['inherited_review'])
    assert len(parent['sources'])==46
    return {'D143_direct_bindings':46,**inherited}


def validate_job(row,driver,output_ref,args=()):
    checked([row['driver'],row['log'],*row['sources']])
    assert row['driver']==source(ROOT/'dembele/pari'/driver)
    assert row['command']==['python3',row['driver']['path']]+list(args)
    assert row['status']=='pass' and row['exit_code']==0
    assert 0<row['wall_seconds']<row['timeout_seconds']==180
    assert row['private_process_group']>0 and row['timeout_terminates_process_group']
    lines=Path(row['log']['path']).read_text().splitlines()
    marks=[json.loads(s.split('|',1)[1]) for s in lines if s.startswith('PHASE_METADATA|')]
    assert marks==[output_ref]
    assert any(s.startswith('PASS|'+driver[:3]+'_') for s in lines)


def receipt(stem,driver,attempt):
    packet=read(stem)
    row=read(stem+'_'+attempt+'.job')
    validate_job(row,driver,source(DATA/(stem+'.json')))
    checked(packet['sources'])
    peak=packet['conservative_peak_rss_bytes']
    assert peak<2*(1<<30)
    return packet,{'receipt':source(DATA/(stem+'_'+attempt+'.job.json')),
                   'wall_seconds':row['wall_seconds'],'conservative_peak_rss_bytes':peak}


def overlaps(a,b):
    return Q(a[0])<=Q(b[1]) and Q(b[0])<=Q(a[1])


def build():
    tick=time.monotonic()
    parent_ref=source(DATA/'P1600_finite_model_review_d143.json')
    inherited=graph(parent_ref)
    print('D144_TRANSITIVE_GRAPH_PASS',flush=True)
    completion=read('P1600_finite_model_completion_d143')
    assert completion['fixed_review']==parent_ref and completion['successful_bounded_jobs']==6
    checked(completion['review_receipts'])
    for i,ref in enumerate(completion['review_receipts']):
        validate_job(json.loads(Path(ref['path']).read_text()),HELPER.name,parent_ref,[] if i==0 else ['--check'])
    primary,first=receipt('P1600_joint_adjunction_d144','606_P1600_joint_adjunction.py','attempt01')
    audit,second=receipt('P1600_adjunction_RR_audit_d144','607_P1600_adjunction_RR_audit.py','attempt02')
    bad_path=DATA/'P1600_adjunction_RR_audit_d144_attempt01.job.json'
    source(bad_path);bad=json.loads(bad_path.read_text())
    assert bad['status']=='failed' and bad['exit_code']==1 and bad['wall_seconds']<180
    assert bad['private_process_group']>0 and bad['timeout_terminates_process_group']
    checked([bad['failed_driver_snapshot'],bad['log'],*bad['sources']])
    assert bad['driver']['sha256']==bad['failed_driver_snapshot']['sha256']
    old=Path(bad['failed_driver_snapshot']['path']).read_text()
    new=(ROOT/'dembele/pari/607_P1600_adjunction_RR_audit.py').read_text()
    assert old.replace('drops[17]==28','drops[17]==20')==new
    assert 'AssertionError' in Path(bad['log']['path']).read_text()
    assert primary['arb_precision_bits']==192 and audit['arb_precision_bits']==224
    assert primary['joint_adjunction_symbolic_identity']
    assert primary['weighted_vertical_coefficient_log2']=='27799/256'
    assert primary['tail_total_length_b']=='48'
    assert primary['tail_joint_correction_coefficient_log2']==audit['independent_tail_joint_correction_coefficient_log2']=='-19909/6144'
    assert primary['anchor_intersection_on_Q_b']=='32'
    assert primary['anchor_intersection_on_minimal_regular_b']=='68'
    assert primary['ordinary_intersection_on_Q_b']=='33/2'
    assert primary['known_dyadic_pair_cost_coefficient_log2']=='659/8'
    assert primary['prime3_pair_cost_coefficient_log3']=='12'
    assert audit['individual_mark_tail_replay'] and audit['marked_points']==27 and audit['unordered_pair_slots']==351
    assert audit['all_17_D118_dyadic_contents_reconstructed']
    assert audit['dyadic_contents_beta']==['280']+['17']*16
    for row in primary['prime3_pair_inequalities']:
        assert Q(row['cost'])>=Q(row['twice_row_weight'])
    for flag in ['universal_variable_cut_cancellation','boundary_anomaly_derived_from_radial_terms',
                 'Deligne_pairing_topological_sign_checked','universal_Gamma_cancellation_checked']:
        assert audit[flag]
    assert [r['order'] for r in audit['Teo_n1_spectral_controls']]==[1,2,3,4,5,8,16,32,64]
    assert all(r['overlaps_final_FvP_8_1'] for r in audit['Teo_n1_spectral_controls'])
    for ka,kb in [('joint_Psi_plus_I_upper_interval','independent_joint_upper_interval'),
                  ('signature_log_C_interval','independent_log_C_interval'),
                  ('Faltings_lower_affine_baseline_interval','independent_affine_Faltings_baseline_interval'),
                  ('sufficient_average_log_Zprime_for_Faltings29_interval','independent_sufficient_log_Zprime_target_interval')]:
        assert overlaps(primary[ka],audit[kb])
    assert Q(audit['independent_joint_upper_interval'][1])<Q('85.172')
    assert Q(audit['independent_affine_Faltings_baseline_interval'][0])>Q('-19.410')
    assert Q(audit['independent_sufficient_log_Zprime_target_interval'][0])>Q('-96.820')
    assert Q(audit['implied_average_log_Zprime_lower_interval'][0])>Q('-98.900')
    ledger=read('P1600_joint_RR_sources_d144')
    checked(ledger['sources'])
    assert len(ledger['external_sources'])==3
    assert ledger['source_applicability_notes_are_mathematical_review_not_machine_verification']
    assert ledger['joint_Psi_plus_I_upper_bound_proved'] and ledger['corrected_global_RR_constant_certified']
    assert ledger['corrections_are_our_derivations_not_author_confirmed']
    assert not ledger['full_intersection_upper_bound_proved']
    for packet in [primary,audit,ledger]:
        assert not packet['Faltings_lower_29_proved'] and not packet['candidate_identification_proved']
    for name in ['606_P1600_joint_adjunction.py','607_P1600_adjunction_RR_audit.py',Path(__file__).name]:
        p=ROOT/'dembele/pari'/name;source(p);ast.parse(p.read_text())
    return {'status':'pass','milestone':'D144','independent_finite_review_complete':True,
            'inherited_review':parent_ref,'catalogue_graph_is_transitive':True,**inherited,
            'completed_input_jobs':2,'preserved_failed_input_jobs':1,'input_receipts':[first,second],
            'preserved_failed_receipt':source(bad_path),
            'joint_Psi_plus_I_upper_bound_proved':True,'joint_strict_upper':'85.172',
            'full_intersection_upper_bound_proved':False,'corrected_global_RR_constant_certified':True,
            'RR_scope':'compact orbifolds, with the companion derivation',
            'source_corrections_are_our_derivations_not_author_confirmed':True,
            'signature_log_C_formula':'15log(pi)+(5081/192)log2+log3-485/64',
            'Faltings_lower_affine_formula':'hFal > -19.410 - average(log Zprime(1))/2',
            'safe_sufficient_average_log_Zprime_target_for_Faltings29':'-96.820',
            'safe_implied_average_log_Zprime_lower':'-98.900',
            'Faltings_lower_29_proved':False,'height_bound_at_most_623_proved':False,
            'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,
            'field_polynomial_constructed':False,'actual_harmonic_precision_increased':False,
            'next_precision_bank_admitted':False,'actual_curve_spectral_calculation_started':False,
            'resource_caps_changed':False,'full_bank_precision_pi':1600,'column0_precision_pi':6400,
            'next_work':'Derive and assess a certified analytic route to average(log Zprime(1)) <= -96.820 before admitting actual-curve numerical spectral work. Exact structural identification remains an alternative. Existing precision, spectral, level, Hecke and cubic pauses persist.',
            'wall_seconds':time.monotonic()-tick,'sources':[source(p) for p in sorted(PATHS)]}


if __name__=='__main__':
    assert __debug__
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args();tick=time.monotonic()
    if args.check:
        saved=json.loads(OUT.read_text())
        assert saved['status']=='pass' and saved['independent_finite_review_complete']
        checked(saved['sources'])
        inherited=graph(saved['inherited_review'])
        assert all(saved[k]==v for k,v in inherited.items())
    else:
        assert not OUT.exists()
        saved=build()
        saved['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        assert saved['peak_rss_bytes']<2*(1<<30)
        with OUT.open('x') as f:f.write(json.dumps(saved,indent=2)+'\n')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    assert peak<2*(1<<30)
    print('D144_REVIEW_RESOURCES|'+json.dumps({'seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(source(OUT)),flush=True)
    print('PASS|608_P1600_JOINT_RR_REVIEW',flush=True)
