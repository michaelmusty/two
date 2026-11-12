"""D149 fixed review, transitive replay, index pricing and completion."""
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
OUT=DATA/'P1600_primitive_frame_review_d149.json';LEDGER=DATA/'P1600_primitive_frame_sources_d149.json'
REPORT=ROOT/'dembele/certificates/P1600-primitive-frame-limits-d149.md'
HELPER=ROOT/'dembele/pari/622_P1600_forward_frame_review.py';PATHS={Path(__file__),HELPER}
spec=importlib.util.spec_from_file_location('d148_provenance',HELPER)
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
    inherited=prior.graph(parent['inherited_review']);assert len(parent['sources'])==44
    return {'D148_direct_bindings':44,**inherited}
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


def price_dyadic_index():
    old=read('P1600_forward_frame_bound_d148')
    local=read('cm_cartier_frame_review_d119')['certificate']
    assert int(old['trace_gram_determinant'])==2**79
    assert local['model']['normalization_index_beta']==264 and local['residue_map_index_beta']==16
    # Trace-centered embedding determinant; 17 is a dyadic unit.
    eta_index=16*79//2;assert 2*eta_index==16*79
    dual_on_Z0=16*(8*16)-eta_index
    dual_on_ZA=dual_on_Z0-264
    determinant=dual_on_ZA+16
    assert (eta_index,dual_on_Z0,dual_on_ZA,determinant)==(632,1416,1152,1168)
    low=2*91*15;high=17*determinant-45*30
    assert (low,high)==(2730,18506)
    old_determinant=determinant+16*(278-48)
    old_low=2*91*245;old_high=17*old_determinant-45*490
    assert (old_determinant,old_low,old_high)==(4848,44590,60366)
    assert high-low==old_high-old_low==15776
    # log(2)=2 atanh(1/3); enclose the positive remaining geometric tail.
    N=12;log_lower=sum(Q(2,(2*k+1)*3**(2*k+1)) for k in range(N))
    log_upper=log_lower+Q(2,(2*N+1)*3**(2*N+1))/(1-Q(1,9))
    saving_coefficient=Q(high-low,16);assert saving_coefficient==986
    assert saving_coefficient*log_upper<684
    return {'eta_embedding_index_beta':eta_index,'dual_pairing_index_on_Z0_beta':dual_on_Z0,
            'dual_pairing_index_on_ZA_beta':dual_on_ZA,'primitive_forward_determinant_beta':determinant,
            'primitive_relation_index_beta_range':[low,high],
            'old_forward_determinant_beta':old_determinant,'old_relation_index_beta_range':[old_low,old_high],
            'additional_dyadic_saving_coefficient_log2':str(saving_coefficient),
            'log2_rational_interval':[str(log_lower),str(log_upper)],
            'additional_dyadic_saving_strict_upper':684,
            'extra_saving_actually_proved':False,'odd_prime_indices_bounded':False}


def build():
    tick=time.monotonic();parent_ref=source(DATA/'P1600_forward_frame_review_d148.json')
    inherited=graph(parent_ref);print('D149_TRANSITIVE_GRAPH_PASS',flush=True)
    completion=read('P1600_forward_frame_completion_d148')
    assert completion['fixed_review']==parent_ref and completion['successful_bounded_jobs']==5
    assert completion['failed_bounded_jobs']==1
    checked(completion['review_receipts'])
    for i,ref in enumerate(completion['review_receipts']):
        validate_job(json.loads(Path(ref['path']).read_text()),HELPER.name,parent_ref,[] if i==0 else ['--check'])
    final_parent_job=read('P1600_forward_frame_completion_d148_attempt01.job')
    validate_job(final_parent_job,HELPER.name,source(DATA/'P1600_forward_frame_completion_d148.json'),['--finish'])
    primary,first=receipt('P1600_primitive_frame_limits_d149','623_P1600_primitive_frame_limits.py')
    audit,second=receipt('P1600_primitive_frame_audit_d149','624_P1600_primitive_frame_audit.py')
    keys=['H_lower_interval','H_upper_interval','pencil_degree_lower_interval','pencil_degree_upper_interval',
          'pencil_degree_required_for_623_interval','primitive_true_relation_height_upper_interval',
          'optimistic_pencil_majorant_interval','field_term_removed_optimistic_majorant_interval']
    for key in keys:
        a,b=primary[key],audit[key];assert Q(a[0])<=Q(b[1]) and Q(b[0])<=Q(a[1])
    ranges={'H_lower_interval':(Q(335,1000),Q(336,1000)),
            'pencil_degree_lower_interval':(-56,-55),
            'pencil_degree_upper_interval':(Q(-412,1000),Q(-411,1000)),
            'pencil_degree_required_for_623_interval':(24,25),
            'primitive_true_relation_height_upper_interval':(15236,15237),
            'optimistic_pencil_majorant_interval':(5132,5133),
            'field_term_removed_optimistic_majorant_interval':(1162,1163)}
    for key,(a,b) in ranges.items():assert a<Q(audit[key][0])<=Q(audit[key][1])<b
    assert audit['independent_collected_budget_verified'] and audit['arbitrary_scalar_and_twist_height_invariance_verified']
    assert audit['odd_intersection_slack_identity_verified'] and audit['principal_part_norm_zero_beta']==2
    for row in audit['pencil_product_AMGM_controls']:
        values=list(map(Q,row));assert len(values)==17 and sum(values)==1
        product=Q(1)
        for z in values:product*=z
        assert product<=Q(1,17**17)
    one=primary['corank_one_control'];two=audit['direct_polynomial_substitution_control']
    assert one['field_characteristic']==31 and two['field_characteristic']==61
    assert one['section_dimension']==16 and one['multiplication_rank']==45 and one['evaluation_rank']==16
    for control in [one,two]:
        assert control['forward_rank']==15 and control['quadric_dimension']==91 and control['quadratic_image_rank']==91
        assert control['cofactor_product_zero'] and control['image_pivot_minor']!=0
        assert len(control['image_pivot_columns'])==91
    assert two['relation_plus_linear_factor_space_rank']==107
    assert not one['smooth_canonical_CM_curve_claimed']
    for packet in [primary,audit]:
        assert packet['primitive_forward_bound_equals_D148'] and packet['budget_difference_coefficient_log2']=='0'
        assert packet['primitive_scalar_valuation_beta']==278 and packet['primitive_forward_content_beta']==15
        assert packet['diagnostic_floors_are_not_actual_height_lower_bounds']
        assert packet['universal_cofactor_product_cancellation_disproved']
        assert not packet['actual_CM_specific_cancellation_disproved']
        assert not packet['pencil_degree_and_field_norm_refinements_alone_sufficient']
        assert not packet['target_proved'] and not packet['target_disproved']
        assert not packet['candidate_identification_proved'] and not packet['new_precision_bank_admitted']
        assert packet['best_current_proved_relation_height_upper']==15237
    price=price_dyadic_index()
    ledger={'status':'pass','milestone':'D149',
            'scope':'Assess the primitive forward pencil budget and universal cofactor cancellation, and price possible additional dyadic frame content without increasing precision.',
            'external_sources':[
             {'title':'Stacks Project, Lemma 44.3.1','url':'https://stacks.math.columbia.edu/tag/0B9D',
              'role':'Finite locally free divisors in the smooth relative curve locus are relative Cartier divisors; used through D119 actual local models.'},
             {'title':'Stacks Project, Section 109.19','url':'https://stacks.math.columbia.edu/tag/0E6N',
              'role':'Relative duality and the invertible relative dualizing sheaf for Gorenstein families; supports D119 principal-parts sequence, not the new numerical inequalities.'}],
            'sources':[source(p) for p in [REPORT,ROOT/'dembele/certificates/cm-residue-lattice-d102.md',
              ROOT/'dembele/certificates/cm-compound-height-d116.md',ROOT/'dembele/certificates/cm-finite-height-d118.md',
              ROOT/'dembele/certificates/cm-cartier-frame-d119.md',ROOT/'dembele/certificates/construction-reassessment-d120.md',
              ROOT/'dembele/certificates/P1600-joint-adjunction-RR-d144.md',
              ROOT/'dembele/certificates/P1600-elliptic-intersections-d146.md',
              ROOT/'dembele/certificates/P1600-forward-frame-bound-d148.md']],
            'new_geometric_and_metric_comparisons_are_companion_derivations':True,
            'finite_checks_do_not_mechanically_verify_geometric_proofs':True,
            'primitive_forward_upper_equals_D148':True,'best_current_proved_relation_height_upper':15237,
            'favorable_pencil_and_field_norm_majorant_strict_lower':1162,
            'diagnostic_floor_is_not_an_actual_relation_height_lower_bound':True,
            'dyadic_index_pricing':price,
            'CM_specific_exterior_cancellation_not_excluded':True,
            'target_623_proved':False,'target_623_disproved':False,'candidate_identification_proved':False}
    assert not LEDGER.exists()
    with LEDGER.open('x') as f:f.write(json.dumps(ledger,indent=2)+'\n')
    source(LEDGER)
    for name in ['623_P1600_primitive_frame_limits.py','624_P1600_primitive_frame_audit.py',Path(__file__).name]:
        p=ROOT/'dembele/pari'/name;source(p);ast.parse(p.read_text())
    return {'status':'pass','milestone':'D149','independent_finite_review_complete':True,
            'inherited_review':parent_ref,'catalogue_graph_is_transitive':True,**inherited,
            'completed_input_jobs':2,'preserved_failed_input_jobs':0,'input_receipts':[first,second],
            'primitive_forward_upper_equals_D148':True,'best_current_proved_relation_height_upper':15237,
            'pencil_degree_only_required_strict_lower':24,'pencil_degree_actual_strict_upper':'-0.411',
            'actual_CM_cotangent_height_strict_lower':'0.335',
            'favorable_pencil_majorant_strict_lower':5132,
            'favorable_pencil_and_field_norm_majorant_strict_lower':1162,
            'diagnostic_floors_are_not_actual_relation_height_lower_bounds':True,
            'universal_forward_cofactor_product_cancellation_disproved':True,
            'CM_specific_exterior_cancellation_not_excluded':True,'dyadic_index_pricing':price,
            'height_bound_at_most_623_proved':False,'height_bound_at_most_623_disproved':False,
            'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,'field_polynomial_constructed':False,
            'actual_curve_spectral_calculation_started':False,'new_geodesic_census_started':False,
            'actual_harmonic_precision_increased':False,'next_precision_bank_admitted':False,
            'resource_caps_changed':False,'full_bank_precision_pi':1600,'column0_precision_pi':6400,
            'next_work':'Audit the saved candidate-scheme, canonical-model and correspondence certificates for an exact automorphic identity or correspondence with a proved uniqueness implication that identifies the actual marked curve. Reuse established candidate checks; finite agreement and candidate height are insufficient. A new height approach must name additional actual-curve input beyond the closed normalization, pencil/field-norm and isolated dyadic-index repairs. Existing precision, spectral, level, Hecke and cubic pauses persist.',
            'wall_seconds':time.monotonic()-tick,'sources':[source(p) for p in sorted(PATHS)]}


def finish():
    saved=json.loads(OUT.read_text());checked(saved['sources']);review_ref=source(OUT);rows=[];resources=[]
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        path=DATA/('P1600_primitive_frame_review_d149_'+suffix+'.job.json');row=json.loads(path.read_text())
        validate_job(row,Path(__file__).name,review_ref,args);rows.append(source(path))
        logs=Path(row['log']['path']).read_text().splitlines()
        r=[json.loads(s.split('|',1)[1]) for s in logs if s.startswith('D149_REVIEW_RESOURCES|')]
        assert len(r)==1;resources.append({'receipt_wall_seconds':row['wall_seconds'],**r[0]})
    docs=['HANDOFF.md','CLAUDE.md','README.md','DECISIONS.md','REFERENCES.md','dembele/README.md','dembele/pari/README.md']
    links=[];output=DATA/'P1600_primitive_frame_completion_d149.json'
    for name in docs:
        path=ROOT/name;text=path.read_text()
        block=text.split('<!-- D149 primitive frame checkpoint -->',1)[1].split('<!-- D148 forward frame',1)[0]
        assert '15237' in block and 'source 626 is next unused' in block
        assert '1162' in block and '623' in block and '684' in block
        for link in re.findall(r'\]\(([^)]+)\)',block):
            if link.startswith('http'):continue
            resolved=(path.parent/link).resolve();assert resolved==output or resolved.is_file(),(name,link);links.append(resolved)
    assert len(links)==28
    result={k:v for k,v in saved.items() if k not in ['sources','wall_seconds','peak_rss_bytes']}
    result.update({'completed_at':datetime.now(timezone.utc).isoformat(),'fixed_review':review_ref,
                   'report':source(REPORT),'source_applicability_ledger':source(LEDGER),'review_receipts':rows,'review_resources':resources,
                   'successful_bounded_jobs':5,'input_bounded_jobs':2,'review_bounded_jobs':2,'completion_bounded_jobs':1,'failed_bounded_jobs':0,
                   'completion_job_receipt_path':str(DATA/'P1600_primitive_frame_completion_d149_attempt01.job.json'),
                   'entry_documents_updated':docs,'current_artifact_links_checked':len(links),
                   'direct_source_bindings':len(saved['sources']),'next_unused_source':626,'entry_document_hashes_intentionally_not_frozen':True})
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
        assert saved['dyadic_index_pricing']==price_dyadic_index()
    else:
        assert not OUT.exists();saved=build()
        saved['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        assert saved['peak_rss_bytes']<2*(1<<30)
        with OUT.open('x') as f:f.write(json.dumps(saved,indent=2)+'\n')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert peak<2*(1<<30)
    print('D149_REVIEW_RESOURCES|'+json.dumps({'seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|625_P1600_PRIMITIVE_FRAME_REVIEW',flush=True)
