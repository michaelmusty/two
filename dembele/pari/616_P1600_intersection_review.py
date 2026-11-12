"""D146 fixed review, transitive replay and completion of the intersection bound."""
import argparse
import ast
from datetime import datetime,timezone
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'P1600_intersection_review_d146.json';LEDGER=DATA/'P1600_intersection_sources_d146.json'
REPORT=ROOT/'dembele/certificates/P1600-elliptic-intersections-d146.md'
HELPER=ROOT/'dembele/pari/613_P1600_spectral_review.py';PATHS={Path(__file__),HELPER}
spec=importlib.util.spec_from_file_location('d145_provenance',HELPER)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)


def raw_source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def source(path):
    p=Path(path).resolve();PATHS.add(p);return raw_source(p)
def checked(refs):
    for ref in refs:assert source(ref['path'])==ref,ref['path']
def read(stem):
    p=DATA/(stem+'.json');source(p);r=json.loads(p.read_text());assert r['status']=='pass';return r
def graph(ref):
    assert raw_source(ref['path'])==ref;parent=json.loads(Path(ref['path']).read_text())
    assert parent['status']=='pass' and parent['independent_finite_review_complete']
    for item in parent['sources']:assert raw_source(item['path'])==item,item['path']
    inherited=prior.graph(parent['inherited_review']);assert len(parent['sources'])==41
    return {'D145_direct_bindings':41,**inherited}
def validate_job(row,driver,output_ref,args=()):
    checked([row['driver'],row['log'],*row['sources']])
    assert row['driver']==source(ROOT/'dembele/pari'/driver)
    assert row['command']==['python3',row['driver']['path']]+list(args)
    assert row['status']=='pass' and row['exit_code']==0
    assert 0<row['wall_seconds']<row['timeout_seconds']==180
    assert row['private_process_group']>0 and row['timeout_terminates_process_group']
    lines=Path(row['log']['path']).read_text().splitlines()
    marks=[json.loads(s.split('|',1)[1]) for s in lines if s.startswith('PHASE_METADATA|')]
    assert marks==[output_ref] and any(s.startswith('PASS|'+driver[:3]+'_') for s in lines)
def receipt(stem,driver):
    packet=read(stem);jobstem=stem+'_attempt01.job';row=read(jobstem)
    validate_job(row,driver,source(DATA/(stem+'.json')));checked(packet['sources'])
    peak=packet['conservative_peak_rss_bytes'];assert peak<2*(1<<30)
    return packet,{'receipt':source(DATA/(jobstem+'.json')),'wall_seconds':row['wall_seconds'],'conservative_peak_rss_bytes':peak}


def build():
    tick=time.monotonic();parent_ref=source(DATA/'P1600_spectral_review_d145.json')
    inherited=graph(parent_ref);print('D146_TRANSITIVE_GRAPH_PASS',flush=True)
    completion=read('P1600_spectral_completion_d145')
    assert completion['fixed_review']==parent_ref and completion['successful_bounded_jobs']==7
    checked(completion['review_receipts'])
    for i,ref in enumerate(completion['review_receipts']):
        validate_job(json.loads(Path(ref['path']).read_text()),HELPER.name,parent_ref,[] if i==0 else ['--check'])
    final_parent_job=read('P1600_spectral_completion_d145_attempt01.job')
    validate_job(final_parent_job,HELPER.name,source(DATA/'P1600_spectral_completion_d145.json'),['--finish'])
    primary,first=receipt('P1600_elliptic_intersections_d146','614_P1600_elliptic_intersections.py')
    audit,second=receipt('P1600_intersection_audit_d146','615_P1600_intersection_audit.py')
    assert primary['field_discriminant']==str(2**31) and primary['prime3_inert_degree']==8
    assert primary['order6_normalizer_square_conditions_both_rejected']
    assert primary['cyclic3_and_symmetric3_rational_controls'] and audit['different_product_controls_independent']
    assert primary['cyclic3_branch_difference_square']==primary['symmetric3_branch_difference']=='-27'
    assert primary['controls_are_examples_not_a_claim_all_actions_have_these_coordinates']
    assert primary['dyadic_same_component_pairs']==13 and primary['dyadic_order3_pairs_separated_by_tame_reduction']==4
    assert primary['order3_row_sum_bounds_in_v3']==['1','3/2'] and primary['odd_pair_cost_bounds_log3']==['18','45']
    assert [r['ratio'] for r in primary['pair_to_row_weights']]==['2','10/3']
    assert audit['factorial_valuation_negative_control_rejected'] and audit['pair_cost_two_sided_linear_identities_verified']
    assert audit['individual_dyadic_marks_and_tails_replayed'] and audit['dyadic_combined_log2_coefficient']=='1193197/6144'
    for key in ['joint_Psi_plus_I_lower_interval','joint_Psi_plus_I_upper_interval','Faltings_upper_interval']:
        a,b=primary[key],audit[key];assert Q(a[0])<=Q(b[1]) and Q(b[0])<=Q(a[1])
    assert Q(audit['joint_Psi_plus_I_lower_interval'][0])>48
    assert Q(audit['joint_Psi_plus_I_upper_interval'][1])<79
    assert Q(audit['Faltings_upper_interval'][1])<Q('4.2')<29
    assert audit['all_three_D141_Faltings_only_critical_targets_excluded']
    for packet in [primary,audit]:
        assert packet['Faltings_lower_29_disproved']
        assert not packet['candidate_identification_proved'] and not packet['relation_height_at_most_623_proved']
        assert not packet['new_precision_bank_admitted']
    ledger={'status':'pass','milestone':'D146',
            'scope':'Bound all omitted elliptic intersections and close the Faltings-only repair of the existing P1600 jet criterion.',
            'external_sources':[
             {'title':'Xinyi Yuan: Modular Heights of Quaternionic Shimura Curves',
              'url':'https://arxiv.org/pdf/2205.13995v3','location':'Proposition 4.1 and proof, pp. 54--56; section 4.1',
              'download_sha256':'7dbf684fa65122ba3a15364079b6c3b1c7fdc2893bf2114a55ca9b448090762c',
              'role':'Smooth maximal-level quotients, special-fibre compatibility, no vertical generic inertia, Hodge/orbifold comparison, and nearby-quaternion local stabilizers. Normalizer extension and intersection bounds are proved in our companion report.'},
             {'title':'The Stacks Project: A formula for the different',
              'url':'https://stacks.math.columbia.edu/tag/0BWB','location':'Example 49.12.5 and Lemma 49.12.6',
              'role':'Monogenic derivative and differential descriptions of the different. Applied to the finite flat smooth formal disk quotient; the orbit product and fixed-section estimate are derived in the report.'}],
            'sources':[source(p) for p in [REPORT,ROOT/'dembele/certificates/P1600-proof-gap-d141.md',
              ROOT/'dembele/certificates/P1600-two-height-routes-d142.md',ROOT/'dembele/certificates/P1600-finite-model-cotangents-d143.md',
              ROOT/'dembele/certificates/P1600-joint-adjunction-RR-d144.md',ROOT/'dembele/certificates/P1600-spectral-feasibility-d145.md',
              ROOT/'dembele/certificates/cm-intrinsic-height-d104.md',ROOT/'dembele/certificates/cm-finite-height-d118.md',
              ROOT/'dembele/certificates/cm-cartier-frame-d119.md']],
            'source_applicability_notes_are_mathematical_review_not_machine_verification':True,
            'normalizer_local_group_and_all_prime_arguments_are_our_derivations':True,
            'no_new_CM_coordinates_or_canonical_lift_formula_assumed':True,
            'RR_and_CM_normalizations_retain_prior_documented_source_reconciliations':True,
            'safe_joint_strict_bounds':['48','79'],'safe_Faltings_strict_upper':'4.2',
            'Faltings_lower_29_disproved':True,'candidate_identification_proved':False,
            'relation_height_at_most_623_proved':False}
    assert not LEDGER.exists()
    with LEDGER.open('x') as f:f.write(json.dumps(ledger,indent=2)+'\n')
    source(LEDGER)
    for name in ['614_P1600_elliptic_intersections.py','615_P1600_intersection_audit.py',Path(__file__).name]:
        p=ROOT/'dembele/pari'/name;source(p);ast.parse(p.read_text())
    return {'status':'pass','milestone':'D146','independent_finite_review_complete':True,
            'inherited_review':parent_ref,'catalogue_graph_is_transitive':True,**inherited,
            'completed_input_jobs':2,'preserved_failed_input_jobs':0,'input_receipts':[first,second],
            'all_dyadic_intersections_on_Q_accounted_for':True,'elliptic_intersections_away_from_2_and_3_vanish':True,
            'wild_local_groups_at_3':['C3','S3'],'odd_pair_cost_bounds_log3':['18','45'],
            'safe_joint_strict_bounds':['48','79'],'safe_Faltings_strict_upper':'4.2',
            'Faltings_lower_29_disproved':True,'all_three_D141_Faltings_only_critical_targets_excluded':True,
            'RR_and_CM_normalizations_retain_prior_documented_source_reconciliations':True,
            'height_bound_at_most_623_proved':False,'height_bound_at_most_623_disproved':False,
            'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,'field_polynomial_constructed':False,
            'actual_curve_spectral_calculation_started':False,'new_geodesic_census_started':False,
            'actual_harmonic_precision_increased':False,'next_precision_bank_admitted':False,
            'resource_caps_changed':False,'full_bank_precision_pi':1600,'column0_precision_pi':6400,
            'next_work':'Investigate the actual relation-space exterior height target 623 via the determinant of the canonical multiplication sequence in the fixed rational residue frame, retaining integral indices and quotient metrics. Exact structural identification remains an alternative. The Faltings-only P1600 repair is ruled out; existing precision, spectral, level, Hecke and cubic pauses persist.',
            'wall_seconds':time.monotonic()-tick,'sources':[source(p) for p in sorted(PATHS)]}


def finish():
    saved=json.loads(OUT.read_text());checked(saved['sources']);review_ref=source(OUT);rows=[];resources=[]
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        path=DATA/('P1600_intersection_review_d146_'+suffix+'.job.json');row=json.loads(path.read_text())
        validate_job(row,Path(__file__).name,review_ref,args);rows.append(source(path))
        logs=Path(row['log']['path']).read_text().splitlines()
        r=[json.loads(s.split('|',1)[1]) for s in logs if s.startswith('D146_REVIEW_RESOURCES|')]
        assert len(r)==1;resources.append({'receipt_wall_seconds':row['wall_seconds'],**r[0]})
    docs=['HANDOFF.md','CLAUDE.md','README.md','DECISIONS.md','REFERENCES.md','dembele/README.md','dembele/pari/README.md']
    links=[];output=DATA/'P1600_intersection_completion_d146.json'
    for name in docs:
        path=ROOT/name;text=path.read_text()
        block=text.split('<!-- D146 elliptic intersection checkpoint -->',1)[1].split('<!-- D145 spectral feasibility',1)[0]
        assert 'h_Fal(C)<4.2' in block and 'source 617 is next unused' in block
        for link in re.findall(r'\]\(([^)]+)\)',block):
            if link.startswith('http'):continue
            resolved=(path.parent/link).resolve();assert resolved==output or resolved.is_file(),(name,link);links.append(resolved)
    assert len(links)==28
    result={k:v for k,v in saved.items() if k not in ['sources','wall_seconds','peak_rss_bytes']}
    result.update({'completed_at':datetime.now(timezone.utc).isoformat(),'fixed_review':review_ref,
                   'report':source(REPORT),'source_applicability_ledger':source(LEDGER),'review_receipts':rows,'review_resources':resources,
                   'successful_bounded_jobs':5,'input_bounded_jobs':2,'review_bounded_jobs':2,'completion_bounded_jobs':1,'failed_bounded_jobs':0,
                   'completion_job_receipt_path':str(DATA/'P1600_intersection_completion_d146_attempt01.job.json'),
                   'entry_documents_updated':docs,'current_artifact_links_checked':len(links),
                   'direct_source_bindings':len(saved['sources']),'next_unused_source':617,'entry_document_hashes_intentionally_not_frozen':True})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    assert all(p.is_file() for p in links);return output


if __name__=='__main__':
    assert __debug__;ap=argparse.ArgumentParser(description=__doc__);group=ap.add_mutually_exclusive_group()
    group.add_argument('--check',action='store_true');group.add_argument('--finish',action='store_true');args=ap.parse_args()
    tick=time.monotonic();output=OUT
    if args.finish:output=finish()
    elif args.check:
        saved=json.loads(OUT.read_text());assert saved['status']=='pass' and saved['independent_finite_review_complete']
        checked(saved['sources']);inherited=graph(saved['inherited_review']);assert all(saved[k]==v for k,v in inherited.items())
    else:
        assert not OUT.exists();saved=build()
        saved['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        assert saved['peak_rss_bytes']<2*(1<<30)
        with OUT.open('x') as f:f.write(json.dumps(saved,indent=2)+'\n')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert peak<2*(1<<30)
    print('D146_REVIEW_RESOURCES|'+json.dumps({'seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|616_P1600_INTERSECTION_REVIEW',flush=True)
