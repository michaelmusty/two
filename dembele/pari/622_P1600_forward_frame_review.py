"""D148 fixed review, transitive replay and completion of the joint height bound."""
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
OUT=DATA/'P1600_forward_frame_review_d148.json';LEDGER=DATA/'P1600_forward_frame_sources_d148.json'
REPORT=ROOT/'dembele/certificates/P1600-forward-frame-bound-d148.md'
HELPER=ROOT/'dembele/pari/619_P1600_multiplication_review.py';PATHS={Path(__file__),HELPER}
spec=importlib.util.spec_from_file_location('d147_provenance',HELPER)
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
    return {'D147_direct_bindings':41,**inherited}
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
def receipt(stem,driver,attempt='attempt01'):
    packet=read(stem);jobstem=stem+'_'+attempt+'.job';row=read(jobstem)
    validate_job(row,driver,source(DATA/(stem+'.json')));checked(packet['sources'])
    peak=packet['conservative_peak_rss_bytes'];assert peak<2*(1<<30)
    return packet,{'receipt':source(DATA/(jobstem+'.json')),'wall_seconds':row['wall_seconds'],'conservative_peak_rss_bytes':peak}


def build():
    tick=time.monotonic();parent_ref=source(DATA/'P1600_multiplication_review_d147.json')
    inherited=graph(parent_ref);print('D148_TRANSITIVE_GRAPH_PASS',flush=True)
    completion=read('P1600_multiplication_completion_d147')
    assert completion['fixed_review']==parent_ref and completion['successful_bounded_jobs']==5
    assert completion['failed_bounded_jobs']==1
    checked(completion['review_receipts'])
    for i,ref in enumerate(completion['review_receipts']):
        validate_job(json.loads(Path(ref['path']).read_text()),HELPER.name,parent_ref,[] if i==0 else ['--check'])
    final_parent_job=read('P1600_multiplication_completion_d147_attempt01.job')
    validate_job(final_parent_job,HELPER.name,source(DATA/'P1600_multiplication_completion_d147.json'),['--finish'])
    primary,first=receipt('P1600_forward_frame_bound_d148','620_P1600_forward_frame_bound.py')
    audit,second=receipt('P1600_forward_frame_audit_d148','621_P1600_forward_frame_audit.py','attempt02')
    assert primary['trace_gram_determinant']==str(2**79) and primary['trace_dual_clearing_integer']==32
    assert primary['trace_dual_pairing_with_eta_is_identity'] and audit['independent_Newton_power_trace_dual_verified']
    bounds=[sum(abs(Q(c))*4**k for k,c in enumerate(row)) for row in primary['scaled_trace_dual_power_coordinates']]
    assert bounds==list(map(Q,primary['dual_root_majorants'])) and len(bounds)==16
    D2=sum(z*z for z in bounds)
    assert D2==Q(primary['sum_squared_dual_root_majorants'])==Q(audit['sum_squared_dual_root_majorants'])
    assert Q(primary['Rouche_left'])<Q(primary['Rouche_right'])==4**17
    assert primary['root_radius']==4
    assert [x['ranks'] for x in primary['filtration_rank_cases']]==[[17,15,13],[17,16,12],[17,17,11]]
    assert audit['exterior_norm_cases']==83 and len(audit['symmetric_and_exterior_content_controls'])==4
    for row in audit['symmetric_and_exterior_content_controls']:
        assert int(row['image_index'])==row['prime']**(2*row['frame_content']*row['kernel_rank'])
    for key in ['true_relation_height_upper_interval','combined_R_minus_t_upper_interval','field_size_removed_majorant_interval']:
        a,b=primary[key],audit[key];assert Q(a[0])<=Q(b[1]) and Q(b[0])<=Q(a[1])
    assert 15236<Q(audit['true_relation_height_upper_interval'][0])
    assert Q(audit['true_relation_height_upper_interval'][1])<15237
    assert Q(audit['combined_R_minus_t_upper_interval'][1])<15193
    assert 11266<Q(audit['field_size_removed_majorant_interval'][0])
    assert Q(audit['field_size_removed_majorant_interval'][1])<11267
    for packet in [primary,audit]:
        assert packet['safe_true_relation_height_upper']==15237
        assert packet['worst_filtration_ranks']==[17,15,13]
        assert Q(packet['dyadic_frame_content_coefficient_log2'])==Q(22295,8)
        assert packet['majorant_floor_is_not_an_actual_height_lower_bound']
        assert not packet['target_proved'] and not packet['target_disproved']
        assert not packet['candidate_identification_proved'] and not packet['new_precision_bank_admitted']
        assert not packet['spectral_n2_determinant_used']
    failed_path=DATA/'P1600_forward_frame_audit_d148_attempt01.job.json'
    failed=json.loads(failed_path.read_text());source(failed_path)
    assert failed['status']=='failed' and failed['exit_code']==1
    assert 0<failed['wall_seconds']<failed['timeout_seconds']==180
    assert failed['private_process_group']>0 and failed['timeout_terminates_process_group']
    checked([failed['log'],failed['failed_driver_snapshot'],*failed['sources']])
    assert failed['driver']['sha256']==failed['failed_driver_snapshot']['sha256']
    failed_log=Path(failed['log']['path']).read_text()
    assert 'NotImplementedError' in failed_log and 'QQ(2*i+3,3)' in failed_log
    ledger={'status':'pass','milestone':'D148',
            'scope':'Bound the actual relation-space height jointly using the leading-jet filtration of the multiplication image and an integral forward residue-frame map.',
            'external_sources':[
             {'title':'Aaron Bertram: Special Divisors',
              'url':'https://www.math.utah.edu/~bertram/6180/Special.pdf','location':'Clifford theorem and equality criterion, pp. 3--4',
              'role':'On the already nonhyperelliptic genus-16 curve, the degree-four line 2D-K has at most two sections. Combined with RR and the inherited actual rank-45 jet map, this gives the filtration ranks 17,k,28-k with 15<=k<=17.'}],
            'sources':[source(p) for p in [REPORT,ROOT/'dembele/certificates/cm-residue-lattice-d102.md',
              ROOT/'dembele/certificates/cm-adjugate-height-d103.md',ROOT/'dembele/certificates/cm-rational-frame-jets-d106.md',
              ROOT/'dembele/certificates/cm-compound-height-d116.md',ROOT/'dembele/certificates/cm-disk-and-exactness-d117.md',
              ROOT/'dembele/certificates/cm-finite-height-d118.md',ROOT/'dembele/certificates/cm-cartier-frame-d119.md',
              ROOT/'dembele/certificates/P1600-proof-gap-d141.md',ROOT/'dembele/certificates/P1600-two-height-routes-d142.md',
              ROOT/'dembele/certificates/P1600-multiplication-determinant-d147.md']],
            'geometric_filtration_and_joint_height_bound_are_companion_derivations':True,
            'source_applicability_notes_are_mathematical_review_not_machine_verification':True,
            'actual_relation_height_strict_upper':15237,'effective_R_minus_t_strict_upper':15193,
            'field_size_removed_majorant_strict_lower':11266,
            'majorant_floor_is_not_an_actual_height_lower_bound':True,
            'unknown_odd_multiplication_indices_not_assumed_zero':True,
            'horizontal_CM_order_not_replaced_by_abstract_field_order':True,
            'target_623_proved':False,'target_623_disproved':False,'candidate_identification_proved':False}
    assert not LEDGER.exists()
    with LEDGER.open('x') as f:f.write(json.dumps(ledger,indent=2)+'\n')
    source(LEDGER)
    for name in ['620_P1600_forward_frame_bound.py','621_P1600_forward_frame_audit.py',Path(__file__).name]:
        p=ROOT/'dembele/pari'/name;source(p);ast.parse(p.read_text())
    return {'status':'pass','milestone':'D148','independent_finite_review_complete':True,
            'inherited_review':parent_ref,'catalogue_graph_is_transitive':True,**inherited,
            'completed_input_jobs':2,'preserved_failed_input_jobs':1,'input_receipts':[first,second],
            'failed_audit_receipt':source(failed_path),
            'failed_audit_reason':'A two-argument Sage QQ call in an exterior-norm control raised NotImplementedError. Replaced with exact rational division; dual-field and height calculations passed unchanged.',
            'previous_relation_height_upper':83240,'best_current_proved_relation_height_upper':15237,
            'effective_R_minus_t_strict_upper':15193,'worst_filtration_ranks':[17,15,13],
            'field_size_removed_majorant_strict_lower':11266,'majorant_floor_is_not_an_actual_height_lower_bound':True,
            'field_vector_norm_refinement_alone_cannot_reach_623_in_this_majorant':True,
            'height_bound_at_most_623_proved':False,'height_bound_at_most_623_disproved':False,
            'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,'field_polynomial_constructed':False,
            'actual_curve_spectral_calculation_started':False,'new_geodesic_census_started':False,
            'actual_harmonic_precision_increased':False,'next_precision_bank_admitted':False,
            'resource_caps_changed':False,'full_bank_precision_pi':1600,'column0_precision_pi':6400,
            'next_work':'Assess a relation-specific exterior comparison or a primitive principal-parts pencil comparison that avoids the full rank-91 ambient cofactor-frame majorant. Any cancellation must apply to the actual relation space and retain D119 horizontal-order/global-normalization data. Field-vector norm refinement alone cannot reach 623 in the present bound. Exact structural identification remains an alternative; existing precision, spectral, level, Hecke and cubic pauses persist.',
            'wall_seconds':time.monotonic()-tick,'sources':[source(p) for p in sorted(PATHS)]}


def finish():
    saved=json.loads(OUT.read_text());checked(saved['sources']);review_ref=source(OUT);rows=[];resources=[]
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        path=DATA/('P1600_forward_frame_review_d148_'+suffix+'.job.json');row=json.loads(path.read_text())
        validate_job(row,Path(__file__).name,review_ref,args);rows.append(source(path))
        logs=Path(row['log']['path']).read_text().splitlines()
        r=[json.loads(s.split('|',1)[1]) for s in logs if s.startswith('D148_REVIEW_RESOURCES|')]
        assert len(r)==1;resources.append({'receipt_wall_seconds':row['wall_seconds'],**r[0]})
    docs=['HANDOFF.md','CLAUDE.md','README.md','DECISIONS.md','REFERENCES.md','dembele/README.md','dembele/pari/README.md']
    links=[];output=DATA/'P1600_forward_frame_completion_d148.json'
    for name in docs:
        path=ROOT/name;text=path.read_text()
        block=text.split('<!-- D148 forward frame checkpoint -->',1)[1].split('<!-- D147 multiplication determinant',1)[0]
        assert '15237' in block and 'source 623 is next unused' in block
        assert '11266' in block and '623' in block
        for link in re.findall(r'\]\(([^)]+)\)',block):
            if link.startswith('http'):continue
            resolved=(path.parent/link).resolve();assert resolved==output or resolved.is_file(),(name,link);links.append(resolved)
    assert len(links)==28
    result={k:v for k,v in saved.items() if k not in ['sources','wall_seconds','peak_rss_bytes']}
    result.update({'completed_at':datetime.now(timezone.utc).isoformat(),'fixed_review':review_ref,
                   'report':source(REPORT),'source_applicability_ledger':source(LEDGER),'review_receipts':rows,'review_resources':resources,
                   'successful_bounded_jobs':5,'input_bounded_jobs':2,'review_bounded_jobs':2,'completion_bounded_jobs':1,'failed_bounded_jobs':1,
                   'completion_job_receipt_path':str(DATA/'P1600_forward_frame_completion_d148_attempt01.job.json'),
                   'entry_documents_updated':docs,'current_artifact_links_checked':len(links),
                   'direct_source_bindings':len(saved['sources']),'next_unused_source':623,'entry_document_hashes_intentionally_not_frozen':True})
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
    print('D148_REVIEW_RESOURCES|'+json.dumps({'seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|622_P1600_FORWARD_FRAME_REVIEW',flush=True)
