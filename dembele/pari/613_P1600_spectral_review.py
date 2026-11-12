"""D145 fixed review, replay and checkpoint completion under the capped wrapper."""
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
OUT=DATA/'P1600_spectral_review_d145.json'
LEDGER=DATA/'P1600_spectral_sources_d145.json'
REPORT=ROOT/'dembele/certificates/P1600-spectral-feasibility-d145.md'
HELPER=ROOT/'dembele/pari/608_P1600_joint_RR_review.py'
PATHS={Path(__file__),HELPER}
spec=importlib.util.spec_from_file_location('d144_provenance',HELPER)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)


def raw_source(path):
    p=Path(path).resolve();return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def source(path):
    p=Path(path).resolve();PATHS.add(p);return raw_source(p)
def checked(refs):
    for ref in refs:assert source(ref['path'])==ref,ref['path']
def read(stem):
    p=DATA/(stem+'.json');source(p);result=json.loads(p.read_text());assert result['status']=='pass';return result
def graph(ref):
    assert raw_source(ref['path'])==ref
    parent=json.loads(Path(ref['path']).read_text())
    assert parent['status']=='pass' and parent['independent_finite_review_complete']
    for item in parent['sources']:assert raw_source(item['path'])==item,item['path']
    inherited=prior.graph(parent['inherited_review']);assert len(parent['sources'])==40
    return {'D144_direct_bindings':40,**inherited}
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
def receipt(stem,driver):
    packet=read(stem);jobstem=stem+'_attempt01.job';row=read(jobstem)
    validate_job(row,driver,source(DATA/(stem+'.json')));checked(packet['sources'])
    peak=packet['conservative_peak_rss_bytes'];assert peak<2*(1<<30)
    return packet,{'receipt':source(DATA/(jobstem+'.json')),'wall_seconds':row['wall_seconds'],
                   'conservative_peak_rss_bytes':peak}


def build():
    tick=time.monotonic();parent_ref=source(DATA/'P1600_joint_RR_review_d144.json')
    inherited=graph(parent_ref);print('D145_TRANSITIVE_GRAPH_PASS',flush=True)
    completion=read('P1600_joint_RR_completion_d144')
    assert completion['fixed_review']==parent_ref and completion['successful_bounded_jobs']==4
    checked(completion['review_receipts'])
    for i,ref in enumerate(completion['review_receipts']):
        validate_job(json.loads(Path(ref['path']).read_text()),HELPER.name,parent_ref,[] if i==0 else ['--check'])
    packets=[];receipts=[]
    for stem,driver in [('P1600_trace_systole_d145','609_P1600_trace_systole.py'),
                        ('P1600_trace_systole_audit_d145','610_P1600_trace_systole_audit.py'),
                        ('P1600_spectral_feasibility_d145','611_P1600_spectral_feasibility.py'),
                        ('P1600_spectral_feasibility_audit_d145','612_P1600_spectral_feasibility_audit.py')]:
        packet,row=receipt(stem,driver);packets.append(packet);receipts.append(row)
        ast.parse((ROOT/'dembele/pari'/driver).read_text())
    initial,trace,heat,audit=packets
    assert initial['field_discriminant']==str(2**31) and initial['split_root_index_zero_based']==4
    assert [r['enumerated_sign_pairs'] for r in initial['families']]==[149,64]
    assert all(not r['admissible_trace_candidates'] for r in initial['families'])
    assert trace['complete_D145_bound40_replayed'] and trace['exact_integer_enumeration']
    assert [r['signed_pairs'] for r in trace['families']]==[2229,1864]
    assert all(not r['all_admissible_candidates'] for r in trace['families'])
    assert [r['gram_diagonal'] for r in trace['families']]==[[8]+[16]*7,[16]*8]
    assert [r['basis_index_in_OF'] for r in trace['families']]==['1','2']
    assert Q(trace['normalizer_systole_lower_rational'])>Q(39,10)
    assert audit['all_arithmetic_exact_rational'] and audit['bound80_fully_replayed']
    assert audit['root_isolation_independently_verified'] and audit['omitted_vector_control_rejected']
    assert audit['independent_exp_and_log_series_with_rational_remainders']
    assert [r['independent_signed_pairs'] for r in audit['trace_families']]==[2229,1864]
    assert all(r['admissible_hyperbolic_pairs']==0 for r in audit['trace_families'])
    assert heat['spectral_gap_used']=='3/16' and heat['Blomer_Brumley_gap']=='975/4096'
    assert heat['elliptic_heat_zero_bound']=='869/128' and heat['times']==['1','4']
    assert heat['small_time_integral_multiplier_upper']=='400/1421'
    assert heat['elementary_log_Zprime_lower']==audit['elementary_log_Zprime_lower']=='-695255321/17052000'
    assert Q(heat['elementary_log_Zprime_lower'])> -41>Q('-96.820')
    assert Q(heat['refined_log_Zprime_lower_interval'][0])>Q(heat['elementary_log_Zprime_lower'])
    assert Q(heat['necessary_joint_S_upper_for_Faltings29_interval'][1])< -249
    for packet in [heat,audit]:
        assert packet['D144_sufficient_spectral_target_ruled_out']
        assert not packet['Faltings_lower_29_proved'] and not packet['Faltings_lower_29_disproved']
        assert not packet['candidate_identification_proved'] and not packet['actual_curve_eigenvalue_computation_started']
    ledger={'status':'pass','milestone':'D145',
            'scope':'Uniform spectral lower bound refutes the D144 sufficient target; the Faltings height and identification remain undecided.',
            'external_sources':[
             {'title':'Garbin and Jorgenson: Heat kernel asymptotics on sequences of elliptically degenerating Riemann surfaces',
              'url':'https://www.jstage.jst.go.jp/article/kodaimath/43/1/43_84/_pdf',
              'location':'Kodai Math. J. 43 (2020), 84--128, Remark 2.7 and equations (2.7)--(2.8), p. 101',
              'download_sha256':'5b69c4e4b5ef4294ecc31679e05b0e10758cbb83b7bbee176a24bd36a797e38c',
              'role':'Compact scalar heat decomposition into positive identity, elliptic and hyperbolic terms. The two-time comparison, elementary tails, and Zprime lower bound are our derivations.'},
             {'title':'Blomer and Brumley: On the Ramanujan conjecture over number fields',
              'url':'https://annals.math.princeton.edu/wp-content/uploads/annals-v174-n1-p18-p.pdf',
              'location':'Annals of Mathematics 174 (2011), 581--605, Definition 1 and Theorem 1, pp. 582--583',
              'download_sha256':'187908253723fccc383ce36079178479e931e2bf61adbcde7bd177ceb7d84868',
              'role':'Exponent 7/64 at every place, applied at the split real place after quaternionic Jacquet--Langlands transfer; constants separated; normalizer spectrum is a subspace.'}],
            'sources':[source(p) for p in [REPORT,ROOT/'dembele/certificates/marked-descent.md',
              ROOT/'dembele/certificates/nelson-norm-one-control-d92.md',ROOT/'dembele/certificates/nelson-global-identification-d95.md',
              ROOT/'dembele/certificates/nelson-spectral-ideal-d98.md',ROOT/'dembele/certificates/P1600-joint-adjunction-RR-d144.md']],
            'source_applicability_notes_are_mathematical_review_not_machine_verification':True,
            'trace_normalization_and_conjugate_uniformity_proved_in_companion_report':True,
            'spectral_lower_bound_independent_of_D144_RR_corrections':True,
            'uniform_strict_log_Zprime_lower':'-41','D144_sufficient_spectral_target_ruled_out':True,
            'safe_necessary_joint_S_upper_for_Faltings29':'-249',
            'Faltings_lower_29_proved':False,'Faltings_lower_29_disproved':False,'candidate_identification_proved':False}
    assert not LEDGER.exists()
    with LEDGER.open('x') as f:f.write(json.dumps(ledger,indent=2)+'\n')
    source(LEDGER);ast.parse(Path(__file__).read_text())
    return {'status':'pass','milestone':'D145','independent_finite_review_complete':True,
            'inherited_review':parent_ref,'catalogue_graph_is_transitive':True,**inherited,
            'completed_input_jobs':4,'preserved_failed_input_jobs':0,'input_receipts':receipts,
            'normalizer_systole_strict_lower':'acosh(25)>39/10','necessary_trace_pairs_checked':4093,
            'trace_candidates_are_not_asserted_to_embed':True,'spectral_gap_used':'3/16',
            'uniform_strict_log_Zprime_lower':'-41','D144_sufficient_spectral_target_ruled_out':True,
            'spectral_lower_bound_independent_of_D144_RR_corrections':True,
            'safe_necessary_joint_S_upper_for_Faltings29':'-249',
            'Faltings_lower_29_proved':False,'Faltings_lower_29_disproved':False,
            'height_bound_at_most_623_proved':False,'positive_exact_quadric_vanishing_proved':False,
            'candidate_identification_proved':False,'field_polynomial_constructed':False,
            'actual_curve_spectral_calculation_started':False,'new_geodesic_census_started':False,
            'actual_harmonic_precision_increased':False,'next_precision_bank_admitted':False,
            'resource_caps_changed':False,'full_bank_precision_pi':1600,'column0_precision_pi':6400,
            'next_work':'Assess the omitted geometric intersection terms using saved derivative contents and local constraints against the necessary S<-249 condition. The D144 spectral upper target is false. Exact structural identification remains an alternative; existing precision, spectral, level, Hecke and cubic pauses persist.',
            'wall_seconds':time.monotonic()-tick,'sources':[source(p) for p in sorted(PATHS)]}


def finish():
    saved=json.loads(OUT.read_text());checked(saved['sources'])
    review_ref=source(OUT);rows=[];resources=[]
    for suffix,args in [('attempt01',[]),('recheck01',['--check'])]:
        path=DATA/('P1600_spectral_review_d145_'+suffix+'.job.json')
        row=json.loads(path.read_text());validate_job(row,Path(__file__).name,review_ref,args)
        rows.append(source(path))
        logs=Path(row['log']['path']).read_text().splitlines()
        r=[json.loads(s.split('|',1)[1]) for s in logs if s.startswith('D145_REVIEW_RESOURCES|')]
        assert len(r)==1;resources.append({'receipt_wall_seconds':row['wall_seconds'],**r[0]})
    docs=['HANDOFF.md','CLAUDE.md','README.md','DECISIONS.md','REFERENCES.md','dembele/README.md','dembele/pari/README.md']
    links=[];output=DATA/'P1600_spectral_completion_d145.json'
    for name in docs:
        path=ROOT/name;text=path.read_text()
        block=text.split('<!-- D145 spectral feasibility checkpoint -->',1)[1].split('<!-- D144 joint adjunction',1)[0]
        assert 'log Zprime(1)) > -41' in block and 'source 614 is next unused' in block
        for link in re.findall(r'\]\(([^)]+)\)',block):
            if link.startswith('http'):continue
            resolved=(path.parent/link).resolve()
            assert resolved==output or resolved.is_file(),(name,link)
            links.append(resolved)
    assert len(links)==28
    result={k:v for k,v in saved.items() if k not in ['sources','wall_seconds','peak_rss_bytes']}
    result.update({'completed_at':datetime.now(timezone.utc).isoformat(),'fixed_review':review_ref,
                   'report':source(REPORT),'source_applicability_ledger':source(LEDGER),
                   'review_receipts':rows,'review_resources':resources,
                   'successful_bounded_jobs':7,'input_bounded_jobs':4,'review_bounded_jobs':2,
                   'completion_bounded_jobs':1,'failed_bounded_jobs':0,
                   'completion_job_receipt_path':str(DATA/'P1600_spectral_completion_d145_attempt01.job.json'),
                   'entry_documents_updated':docs,'current_artifact_links_checked':len(links),
                   'direct_source_bindings':len(saved['sources']),'next_unused_source':614,
                   'entry_document_hashes_intentionally_not_frozen':True})
    with output.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    assert all(p.is_file() for p in links)
    return output


if __name__=='__main__':
    assert __debug__
    ap=argparse.ArgumentParser(description=__doc__);group=ap.add_mutually_exclusive_group()
    group.add_argument('--check',action='store_true');group.add_argument('--finish',action='store_true')
    args=ap.parse_args();tick=time.monotonic();output=OUT
    if args.finish:output=finish()
    elif args.check:
        saved=json.loads(OUT.read_text());assert saved['status']=='pass' and saved['independent_finite_review_complete']
        checked(saved['sources']);inherited=graph(saved['inherited_review'])
        assert all(saved[k]==v for k,v in inherited.items())
    else:
        assert not OUT.exists();saved=build()
        saved['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        assert saved['peak_rss_bytes']<2*(1<<30)
        with OUT.open('x') as f:f.write(json.dumps(saved,indent=2)+'\n')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert peak<2*(1<<30)
    print('D145_REVIEW_RESOURCES|'+json.dumps({'seconds':time.monotonic()-tick,'peak_rss_bytes':peak}),flush=True)
    print('PHASE_METADATA|'+json.dumps(source(output)),flush=True)
    print('PASS|613_P1600_SPECTRAL_REVIEW',flush=True)
