"""D147 fixed review, transitive replay and completion of determinant investigation."""
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
OUT=DATA/'P1600_multiplication_review_d147.json';LEDGER=DATA/'P1600_multiplication_sources_d147.json'
REPORT=ROOT/'dembele/certificates/P1600-multiplication-determinant-d147.md'
HELPER=ROOT/'dembele/pari/616_P1600_intersection_review.py';PATHS={Path(__file__),HELPER}
spec=importlib.util.spec_from_file_location('d146_provenance',HELPER)
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
    inherited=prior.graph(parent['inherited_review']);assert len(parent['sources'])==42
    return {'D146_direct_bindings':42,**inherited}
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
def binary_rank(rows):
    basis={}
    for row in rows:
        x=row
        while x:
            bit=x.bit_length()-1
            if bit in basis:x^=basis[bit]
            else:basis[bit]=x;break
    return len(basis)


def build():
    tick=time.monotonic();parent_ref=source(DATA/'P1600_intersection_review_d146.json')
    inherited=graph(parent_ref);print('D147_TRANSITIVE_GRAPH_PASS',flush=True)
    completion=read('P1600_intersection_completion_d146')
    assert completion['fixed_review']==parent_ref and completion['successful_bounded_jobs']==5
    checked(completion['review_receipts'])
    for i,ref in enumerate(completion['review_receipts']):
        validate_job(json.loads(Path(ref['path']).read_text()),HELPER.name,parent_ref,[] if i==0 else ['--check'])
    final_parent_job=read('P1600_intersection_completion_d146_attempt01.job')
    validate_job(final_parent_job,HELPER.name,source(DATA/'P1600_intersection_completion_d146.json'),['--finish'])
    primary,first=receipt('P1600_multiplication_determinant_d147','617_P1600_multiplication_determinant.py')
    audit,second=receipt('P1600_multiplication_audit_d147','618_P1600_multiplication_audit.py')
    g=primary['graph'];vertices=g['vertices'];edges=list(map(tuple,g['edges']));C=g['cycle_basis_mod2']
    original=read('hyperellipticity_graph_review_d99')
    assert vertices==original['stable_vertices'] and edges==[(u,v) for u,v,_ in original['stable_edges']]
    assert len(C)==16 and all(len(c)==45 for c in C)
    assert binary_rank([sum(x<<i for i,x in enumerate(c)) for c in C])==16
    assert all(sum(c[e] for e,pair in enumerate(edges) if v in pair)%2==0 for c in C for v in vertices)
    pairs=g['monomial_pairs'];assert pairs==[[i,j] for i in range(16) for j in range(i,16)]
    products=[sum((C[i][e]*C[j][e])<<k for k,(i,j) in enumerate(pairs)) for e in range(45)]
    assert binary_rank(products)==45
    pivots=g['pivot_columns'];assert len(pivots)==45 and len(set(pivots))==45
    assert binary_rank([sum(((row>>j)&1)<<k for k,j in enumerate(pivots)) for row in products])==45
    assert g['one_edge_cuts']==g['two_edge_cuts']==[] and g['deletion_subsets_checked']==1035
    lookup={frozenset(pair):e for e,pair in enumerate(edges)}
    assert len(audit['cycle_pair_witnesses'])==45
    for e,w in enumerate(audit['cycle_pair_witnesses']):
        assert w['edge_index']==e and tuple(w['edge'])==edges[e];cyc=[]
        for p,c in zip(w['paths'],w['cycles']):
            assert len(p)==len(set(p)) and (p[0],p[-1])==edges[e]
            q={lookup[frozenset(pair)] for pair in zip(p,p[1:])}
            assert e not in q and sorted(q|{e})==c;cyc.append(q|{e})
        assert len(cyc)==2 and cyc[0]&cyc[1]=={e}
    assert audit['independent_surjectivity_rank']==45 and audit['dyadic_multiplication_cokernel_length']==0
    assert audit['cubic_two_edge_cut_control_rank']==11<12
    assert audit['block_Gram_identity_controls']==25 and audit['wrong_torsion_sign_rejected']
    assert len(primary['symmetric_metric_controls'])==5 and len(primary['cokernel_and_volume_controls'])==30
    assert primary['symmetric_metric_degree_correction_log2']=='60'
    assert primary['wrong_cokernel_sign_and_omission_rejected'] and primary['target_metric_rescaling_cancels']
    for row in primary['determinant_one_shear_controls']:
        assert row['frame_determinant']==row['intrinsic_quadric_norm_squared']==1
        assert row['coefficient_covolume_squared']==row['N']**2+2
    for key in ['known_height_constant_interval','residual_headroom_for_623_interval']:
        a,b=primary[key],audit[key];assert Q(a[0])<=Q(b[1]) and Q(b[0])<=Q(a[1])
    assert Q(audit['known_height_constant_interval'][1])<Q('44.411750955')
    assert Q(audit['residual_headroom_for_623_interval'][0])>Q('578.58824904')
    for packet in [primary,audit]:
        assert packet['ordinary_quadratic_differential_rank']==45
        assert packet['orbifold_weight4_rank']==72 and packet['elliptic_principal_parts_rank']==27
        assert packet['safe_sufficient_metric_residual_upper']=='578'
        assert not packet['metric_residual_at_most_578_proved']
        assert not packet['candidate_identification_proved'] and not packet['relation_height_at_most_623_proved']
        assert not packet['new_precision_bank_admitted']
    ledger={'status':'pass','milestone':'D147',
            'scope':'Normalize the actual canonical multiplication determinant and rational residue-frame comparison; prove dyadic surjectivity; identify remaining quantitative obligation.',
            'external_sources':[
             {'title':'Gerard Freixas i Montplet: Arithmetic Riemann-Roch and Hilbert-Samuel formulae for pointed stable curves',
              'url':'https://arxiv.org/pdf/0803.2366v1','location':'Theorem 4.5 at k=0,n=0 and Lemma 4.6 at k=1,n=0, pp. 16--17',
              'download_sha256':'00699147c57d623bf83e5bbb8fb9a85ab7d4084da86b361e1fdef537b4a507e6',
              'role':'Algebraic stable-coarse-curve isomorphism det(G)=det(E)^13 tensor O(-Delta). No isometry for our L2/quotient metrics is inferred; its discrepancy A_2 remains unevaluated.'},
             {'title':'Lee-Peng Teo: Resolvent Trace Formula and Determinants of n Laplacians',
              'url':'https://www.imath.kiev.ua/~sigma/2021/083/sigma21-083.pdf','location':'Sections 5--6, dimension formula and Theorem 6.2',
              'download_sha256':'2018d77e4701bde0654cec346b98eea3f4fca9669ea2e452bd5e21dd1166450b',
              'role':'The orbifold n=2 zero-mode space allows simple coarse poles at all elliptic points and has dimension 72. Direct substitution for the rank-45 ordinary bicanonical determinant is rejected. Local descent and the exact sequence are derived in the report.'}],
            'sources':[source(p) for p in [REPORT,ROOT/'dembele/certificates/hyperellipticity-review-d99.md',
              ROOT/'dembele/certificates/cm-residue-lattice-d102.md',ROOT/'dembele/certificates/cm-adjugate-height-d103.md',
              ROOT/'dembele/certificates/cm-rational-frame-jets-d106.md',ROOT/'dembele/certificates/cm-compound-height-d116.md',
              ROOT/'dembele/certificates/cm-finite-height-d118.md',ROOT/'dembele/certificates/cm-cartier-frame-d119.md',
              ROOT/'dembele/certificates/P1600-proof-gap-d141.md',ROOT/'dembele/certificates/P1600-two-height-routes-d142.md',
              ROOT/'dembele/certificates/P1600-elliptic-intersections-d146.md']],
            'geometric_application_and_height_identity_are_companion_derivations':True,
            'source_applicability_notes_are_mathematical_review_not_machine_verification':True,
            'dyadic_surjectivity_proved':True,'dyadic_multiplication_cokernel_length':0,
            'height_identity':'h_ext(I_2)=-4F-delta-60log(2)+R-t_mu, R=A_2+U_mu+Theta_frame',
            'safe_sufficient_metric_residual_upper':'578','metric_residual_at_most_578_proved':False,
            'Mumford_isometry_assumed':False,'orbifold_n2_direct_substitution_valid':False,
            'candidate_identification_proved':False,'relation_height_at_most_623_proved':False}
    assert not LEDGER.exists()
    with LEDGER.open('x') as f:f.write(json.dumps(ledger,indent=2)+'\n')
    source(LEDGER)
    for name in ['617_P1600_multiplication_determinant.py','618_P1600_multiplication_audit.py',Path(__file__).name]:
        p=ROOT/'dembele/pari'/name;source(p);ast.parse(p.read_text())
    return {'status':'pass','milestone':'D147','independent_finite_review_complete':True,
            'inherited_review':parent_ref,'catalogue_graph_is_transitive':True,**inherited,
            'completed_input_jobs':2,'preserved_failed_input_jobs':0,'input_receipts':[first,second],
            'actual_stable_fibre_multiplication_rank':45,'independent_cycle_pair_witnesses':45,
            'dyadic_multiplication_cokernel_length':0,'symmetric_metric_degree_correction_log2':'60',
            'height_identity':ledger['height_identity'],
            'known_height_constant_strict_upper':'44.411750955','safe_sufficient_metric_residual_upper':'578',
            'metric_residual_at_most_578_proved':False,'ordinary_quadratic_differential_rank':45,
            'orbifold_weight4_rank':72,'elliptic_principal_parts_rank':27,
            'orbifold_n2_direct_substitution_valid':False,'frame_determinant_alone_is_insufficient':True,
            'height_bound_at_most_623_proved':False,'height_bound_at_most_623_disproved':False,
            'best_current_proved_relation_height_upper':'83240',
            'positive_exact_quadric_vanishing_proved':False,'candidate_identification_proved':False,'field_polynomial_constructed':False,
            'actual_curve_spectral_calculation_started':False,'new_geodesic_census_started':False,
            'actual_harmonic_precision_increased':False,'next_precision_bank_admitted':False,
            'resource_caps_changed':False,'full_bank_precision_pi':1600,'column0_precision_pi':6400,
            'next_work':'Bound the actual residue-frame comparison Theta_frame and ordinary bicanonical quotient-metric combination A_2+U_mu, preserving joint cancellations, against R<=578. An orbifold n=2 route first requires its 27 elliptic principal parts and metric/lattice comparisons. Exact structural identification remains an alternative. Existing precision, spectral, level, Hecke and cubic pauses persist.',
            'wall_seconds':time.monotonic()-tick,'sources':[source(p) for p in sorted(PATHS)]}


def finish():
    saved=json.loads(OUT.read_text());checked(saved['sources']);review_ref=source(OUT);rows=[];resources=[]
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        path=DATA/('P1600_multiplication_review_d147_'+suffix+'.job.json');row=json.loads(path.read_text())
        validate_job(row,Path(__file__).name,review_ref,args);rows.append(source(path))
        logs=Path(row['log']['path']).read_text().splitlines()
        r=[json.loads(s.split('|',1)[1]) for s in logs if s.startswith('D147_REVIEW_RESOURCES|')]
        assert len(r)==1;resources.append({'receipt_wall_seconds':row['wall_seconds'],**r[0]})
    docs=['HANDOFF.md','CLAUDE.md','README.md','DECISIONS.md','REFERENCES.md','dembele/README.md','dembele/pari/README.md']
    links=[];output=DATA/'P1600_multiplication_completion_d147.json'
    for name in docs:
        path=ROOT/name;text=path.read_text()
        block=text.split('<!-- D147 multiplication determinant checkpoint -->',1)[1].split('<!-- D146 elliptic intersection',1)[0]
        assert 'R<=578' in block and 'source 620 is next unused' in block
        assert 'rank 45' in block and '72' in block and '27' in block
        for link in re.findall(r'\]\(([^)]+)\)',block):
            if link.startswith('http'):continue
            resolved=(path.parent/link).resolve();assert resolved==output or resolved.is_file(),(name,link);links.append(resolved)
    assert len(links)==28
    result={k:v for k,v in saved.items() if k not in ['sources','wall_seconds','peak_rss_bytes']}
    result.update({'completed_at':datetime.now(timezone.utc).isoformat(),'fixed_review':review_ref,
                   'report':source(REPORT),'source_applicability_ledger':source(LEDGER),'review_receipts':rows,'review_resources':resources,
                   'successful_bounded_jobs':5,'input_bounded_jobs':2,'review_bounded_jobs':2,'completion_bounded_jobs':1,'failed_bounded_jobs':0,
                   'completion_job_receipt_path':str(DATA/'P1600_multiplication_completion_d147_attempt01.job.json'),
                   'entry_documents_updated':docs,'current_artifact_links_checked':len(links),
                   'direct_source_bindings':len(saved['sources']),'next_unused_source':620,'entry_document_hashes_intentionally_not_frozen':True})
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
    print('D147_REVIEW_RESOURCES|'+json.dumps({'seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|619_P1600_MULTIPLICATION_REVIEW',flush=True)
