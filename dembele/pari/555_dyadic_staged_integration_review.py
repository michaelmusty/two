"""D132 independent finite review and admission of one staged P=6400 column.

No production arithmetic module is imported. Ordinary quotient recurrences
are sampled; complete comparisons use every retained reference coordinate.
"""
import argparse
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_staged_integration_review_d132.json';PREFIX=OUT.stem
s=importlib.util.spec_from_file_location('independent',ROOT/'dembele/pari/486_dyadic_precision400_independent.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
PATHS={Path(__file__),Path(r.__file__)};CACHE={}
def source(path):
    path=Path(path).resolve();PATHS.add(path)
    if path not in CACHE:CACHE[path]=r.source(path)
    return CACHE[path]
def canonical(d):return json.dumps(d,sort_keys=True,separators=(',',':')).encode()
def read(stem):
    p=DATA/(stem+'.json');PATHS.add(p);d=json.loads(p.read_text());assert d['status']=='pass';return d
def envelope(path):
    PATHS.add(path);d=json.loads(path.read_text());assert set(d)=={'value','sha256'}
    assert hashlib.sha256(canonical(d['value'])).hexdigest()==d['sha256'];return d['value']
def checked(records):
    for x in records:assert source(x['path'])==x,x['path']
def full_file(root,d):
    path=root/d['name'];assert path.stat().st_size==d['bytes']==d['rows']*d['row_bytes']
    assert source(path)['sha256']==d['sha256'] and len(d['row_sha256'])==d['rows']
    with path.open('rb') as f:
        for sha in d['row_sha256']:
            raw=f.read(d['row_bytes']);assert hashlib.sha256(raw).hexdigest()==sha
        assert not f.read(1)
def decode(path,e,count,bits,weighted=False):
    sizes=[[max(0,(count-k-i+7)//8) if weighted and k>32 else bits for i in range(8)] for k in range(count)]
    width=sum((n+7)//8 for row in sizes for n in row)
    with Path(path).open('rb') as f:f.seek(e*width);raw=f.read(width)
    assert len(raw)==width;at=0;values=[]
    for row in sizes:
        v=[]
        for n in row:
            size=(n+7)//8;x=int.from_bytes(raw[at:at+size],'little');at+=size;assert x<1<<n;v.append(x)
        values.append(tuple(v))
    return values
def inspect_store(name):
    root=DATA/name;owner=envelope(root/'OWNER.json');current=envelope(root/'CURRENT.json');seal=envelope(root/'SEALED.json')
    assert owner['storage_source_sha256']==source(ROOT/'dembele/pari/547_dyadic_staged_store.py')['sha256']
    assert owner['cap_bytes']==2147483648 and seal['all_remaining_files_frozen']
    assert seal['current_sha256']==hashlib.sha256(canonical(current)).hexdigest()
    assert not any((root/n).exists() for n in ('TXN.json','WAL.json','RETIRE.json','WORKSPACE.bin'))
    assert not list(root.glob('*.tmp')) and not list(root.glob('wal_*.bin'))
    live={current[k]['name'] for k in ('state','aux')}
    for kind in ('state','aux'):full_file(root,current[kind])
    for path in root.glob('pool_*.json'):
        d=envelope(path)
        if d.get('retired'):assert not (root/d['name']).exists()
        elif d.get('historical_after_state_update'):assert d['name']==current['state']['name']
        else:assert d['complete'];full_file(root,d);live.add(d['name'])
    assert {p.name for p in root.glob('*.bin')}==live
    history=[envelope(q) for q in sorted(root.glob('history_*.json'))]
    assert [x['epoch'] for x in history]==list(range(current['epoch']))
    tags={x['tag'] for x in history}|{current['tag']}
    retired=[envelope(q) for q in root.glob('retired_*.json')]
    for x in retired:assert x['after_tag'] in tags and not (root/x['name']).exists()
    archived=0
    for path in root.glob('archive_*.json'):
        d=envelope(path);assert d['external_records_remain_frozen'] and not d['arithmetic_payloads_removed']
        for item in d['items']:
            checked([item['external_metadata'],item['passing_receipt']]);external=json.loads(Path(item['external_metadata']['path']).read_text())
            original=canonical({'value':external,'sha256':hashlib.sha256(canonical(external)).hexdigest()})
            assert hashlib.sha256(original).hexdigest()==item['internal_sha256'] and len(original)==item['bytes']
            assert not (root/item['name']).exists();archived+=1
    PATHS.update(root.iterdir())
    return {'namespace':name,'epoch':current['epoch'],'payload_bytes':sum((root/n).stat().st_size for n in live),
            'history_records':len(history),'retirement_records':len(retired),'archived_duplicate_records':archived,
            'all_current_full_and_row_hashes_checked':True}
def recurrence(ring,pars,values,degrees):
    a,b,c=pars;power=[ring.one]+[ring.zero]*(len(values)-1);out={}
    for n in range(1,max(degrees)+1):
        row=[ring.mul(b,power[0])]
        for k in range(1,len(values)):row.append(ring.sub(ring.add(ring.mul(b,power[k]),ring.mul(a,power[k-1])),ring.mul(c,row[-1])))
        power=row
        if n in degrees:
            total=ring.zero
            for x,y in zip(power,values):total=ring.add(total,ring.mul(x,y))
            out[n]=total
    return out
def ordinary_samples():
    root=DATA/'dyadic_rowjournal_P800_col00_d132';cur=envelope(root/'CURRENT.json');transport=read('dyadic_target_transports_d121')
    ring=r.Quotient(r.FP,800);inputs=envelope(root/'INPUTS.json');ref=inputs['reference']['payload'];checked([ref])
    states=0
    for e in (0,83,173):
        total={n:ring.zero for n in (1,2,33)}
        for ch in transport['transitions'][e]['children']:
            values=decode(root/cur['state']['name'],ch['target_edge'],800,100,True)
            part=recurrence(ring,tuple(map(ring.norm,ch['normalized_center'][:3])),values,(1,2,33))
            for n in total:total[n]=ring.add(total[n],part[n])
        expected=decode(ref['path'],e,800,100)
        for n,x in total.items():assert x==expected[n];states+=8
    cmchecks=0;charts=[x for x in transport['CM_charts'] if x['chart']=='A']
    cm=envelope(root/'pool_CM.json')
    for ci in (0,8,16):
        chart=charts[ci];A,B,C=map(ring.norm,chart['normalized_center'][:3]);totals={n:ring.zero for n in (1,2,3)}
        for ch in transport['transitions'][chart['target_edge']]['children']:
            a,b,c=map(ring.norm,ch['normalized_center'][:3]);den=ring.add(ring.one,ring.mul(C,b));inv=ring.one
            for _ in range(10):inv=ring.mul(inv,ring.sub(ring.scale(ring.one,2),ring.mul(den,inv)))
            assert ring.mul(den,inv)==ring.one
            pars=(ring.mul(ring.add(ring.mul(A,a),ring.mul(B,c)),inv),ring.mul(ring.add(ring.mul(A,b),B),inv),ring.mul(ring.add(c,ring.mul(C,a)),inv))
            assert ring.value(pars[2])>=1 and ring.value(ring.sub(pars[0],ring.mul(pars[1],pars[2])))>=1
            values=decode(root/cur['state']['name'],ch['target_edge'],800,100,True)
            part=recurrence(ring,pars,values,(1,2,3))
            for n in totals:totals[n]=ring.add(totals[n],part[n])
        expected=decode(root/cm['name'],ci,1600,100)
        for n,x in totals.items():assert x==expected[n];cmchecks+=8
    lowroot=DATA/'dyadic_rowjournal_low1319_d132';low=envelope(lowroot/'pool_answer000_06.json');rhs=envelope(lowroot/'pool_rhs000.json')
    ring=r.Quotient(r.FP,10552);lowchecks=0
    for e in (0,83,173):
        own=decode(lowroot/low['name'],e,32,1319);totals={n:own[n-1] for n in (1,2)}
        for ch in transport['transitions'][e]['children']:
            values=[ring.zero]+decode(lowroot/low['name'],ch['target_edge'],32,1319)
            part=recurrence(ring,tuple(map(ring.norm,ch['normalized_center'][:3])),values,(1,2))
            for n in totals:totals[n]=ring.sub(totals[n],part[n])
        expected=decode(lowroot/rhs['name'],e,32,1319)
        for n,x in totals.items():assert x==expected[n-1];lowchecks+=8
    return {'ordinary_state_scalars':states,'ordinary_CM_scalars':cmchecks,'ordinary_1319bit_low_scalars':lowchecks,
            'sampled_not_complete_independent_operators':True}
def finite():
    base=(ROOT/'dembele/pari/548_dyadic_resumable_staged_driver.py').read_text()
    expected=base.replace('D132 separately capped, resumable weighted staged refinement phases.', 'D132 production staged phases with explicit prior-review provenance.')
    expected=expected.replace("prior=read('dyadic_weighted_journal_review_d131');known=", "prior=read(self.cfg.get('prior_review','dyadic_weighted_journal_review_d131'));known=")
    expected=expected.replace("q.name.startswith(('547_','548_'))", "q.name.startswith(('547_','554_'))")
    expected=expected.replace('PASS|548_DYADIC_RESUMABLE_STAGED_DRIVER','PASS|554_DYADIC_RESUMABLE_STAGED_PRODUCTION')
    assert expected==(ROOT/'dembele/pari/554_dyadic_resumable_staged_production.py').read_text()
    pilot=read('dyadic_staged_P800_col00_d132_completed');low=read('dyadic_staged_low1319_d132_completed')
    assert pilot['all_phases_complete'] and low['all_phases_complete']
    assert pilot['maximum_workers']==3 and low['maximum_workers']<=3
    assert len(pilot['interruption_controls'])==7 and len(low['metadata_archives'])==7
    stores=[inspect_store('dyadic_rowjournal_P800_col00_d132'),inspect_store('dyadic_rowjournal_low1319_d132')]
    assert stores[0]['epoch']==26 and stores[0]['history_records']==26 and stores[0]['retirement_records']==13
    assert stores[1]['archived_duplicate_records']==21
    root=DATA/'dyadic_rowjournal_P800_col00_d132';cur=envelope(root/'CURRENT.json');inputs=envelope(root/'INPUTS.json')
    ref=inputs['reference']['payload'];checked([ref]);scalar=0
    verify=envelope(root/'pool_verification.json')
    for e in range(174):
        expected=decode(ref['path'],e,800,100);actual=decode(root/cur['state']['name'],e,800,100,True)
        for k,(x,y) in enumerate(zip(expected,actual)):
            for i,(a,z) in enumerate(zip(x,y)):
                bits=100 if k<=32 else max(0,(800-k-i+7)//8);assert a%(1<<bits)==z;scalar+=1
        raw=b''.join(x.to_bytes(13,'little') for row in expected for x in row)
        with (root/verify['name']).open('rb') as f:f.seek(32*e);assert f.read(32)==hashlib.sha256(raw).digest()
    cm=envelope(root/'pool_CM.json');cmscalars=0
    for ci in range(17):
        actual=decode(root/cm['name'],ci,1600,100)
        ch=next(x for x in inputs['CM_chunks'] if x['first_chart']<=ci<=x['last_chart'])
        expected=decode(ch['file']['path'],ci-ch['first_chart'],6400,400)
        assert actual==[tuple(x% (1<<100) for x in row) for row in expected[:1600]];cmscalars+=1600*8
    coarse_records=[]
    for ci in range(17):
        for order,gain in enumerate((32,48,32,64)):
            d=read(f'dyadic_staged_P800_col00_d132_coarse_c{ci:02d}_o{order}')['certificates']
            assert d['chart']==ci and d['order']==order and d['error_beta']==1600+gain and d['old_overlap_checked'];coarse_records.append(d)
    old=read('dyadic_CM_P3200_col00_d129');ring=r.Quotient(r.MP,1664)
    for d in coarse_records:
        prior=old['CM_values'][d['chart']]['coarse_coefficients_beta'][d['order']]
        assert ring.value(ring.sub(ring.norm(d['coarse_value_beta']),ring.norm(prior)))>=d['error_beta']
    target=read('dyadic_staged_target_low_finish_d132')['certificates'];assert target['all_answer_bytes_match_D130']==7349760
    inv=read('dyadic_staged_lifetime_inventory_d132')['certificates']['schedules']
    assert [(x['precision_pi'],x['seed_precision_pi']) for x in inv]==[(800,400),(6400,3200),(10552,6400)]
    for d in inv:
        assert d['single_working_store'] and d['requires_duplicate_job_record_archival_after_each_sweep']
        assert max(x['total_bytes'] for x in d['phase_inventory'])==d['maximum_bound']['total_bytes']<2147483648
        assert d['margin_bytes']==2147483648-d['maximum_bound']['total_bytes']
        P=d['precision_pi'];W=174*sum((max(0,(P-k-i+7)//8)+7)//8 if k>32 else ((P//8+7)//8) for k in range(P) for i in range(8))
        assert W==d['weighted_bytes'] and d['CM_bytes']==17*2*P*8*((P//8+7)//8)
    fault=read('dyadic_staged_archive_interruption_d132')['certificates'];assert fault['intentional_child_exit']==73 and fault['records_removed_before_interruption']==1
    return {'full_known_P800_column_recomputed':True,'corrections':12,'weighted_scalar_comparisons':scalar,
            'uniform_original_output_digests_checked':174,'CM_scalar_comparisons':cmscalars,'coarse_values_checked':68,
            'target_1319_bit_solution_matches_D130':True,'intentional_interrupted_children':8,
            'stores':stores,'ordinary_samples':ordinary_samples(),'scratch_schedules':[{k:v for k,v in d.items() if k!='phase_inventory'} for d in inv],
            'no_new_harmonic_precision_in_controls':True,'power_loss_durability_claimed':False,
            'RAM_is_measured_admission_not_OS_hard_limit':True,'interrupted_child_RSS_not_separately_recorded':True}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');a=ap.parse_args()
    if a.check:
        d=json.loads(OUT.read_text());assert d['status']=='pass';checked(d['sources'])
        print('PASS|555_DYADIC_STAGED_INTEGRATION_REVIEW',flush=True);return
    assert not OUT.exists();prior=read('dyadic_weighted_journal_review_d131');checked(prior['sources'])
    jobs=[];categories=Counter()
    for path in sorted(DATA.glob('*d132*_attempt*.job.json')):
        if path.name.startswith(PREFIX):continue
        d=json.loads(path.read_text());assert d['status']=='pass' and d['exit_code']==0,path.name
        assert d['timeout_seconds']==180 and d['timeout_terminates_process_group'];checked([d['driver'],d['log']]+d.get('sources',[]))
        bindings=[json.loads(x.split('|',1)[1]) for x in Path(d['log']['path']).read_text().splitlines() if x.startswith('PHASE_METADATA|')]
        assert len(bindings)==1;checked(bindings);PATHS.add(path);categories[Path(d['driver']['path']).name]+=1
        jobs.append({'receipt':source(path),'wall_seconds':d['wall_seconds'],'driver':d['driver']['path']})
    cert=finite()
    for n in range(547,555):PATHS.add(next((ROOT/'dembele/pari').glob(str(n)+'_*.py')))
    for stem in ('dyadic_staged_integration_sources_d132','dyadic_staged_P800_col00_config_d132','dyadic_staged_low1319_config_d132','dyadic_staged_P6400_col00_config_d133'):
        read(stem)
    PATHS.add(ROOT/'dembele/certificates/dyadic-staged-integration-d132.md')
    result={'status':'pass','milestone':'D132','inherited_D131_hashes_preserved':len(prior['sources']),
            'independent_finite_review_complete':True,'production_arithmetic_not_imported':True,'certificates':cert,
            'passing_input_jobs':len(jobs),'failed_bounded_jobs':0,'input_categories':dict(categories),'input_jobs':jobs,
            'one_P6400_column_admitted_after_completed_review':True,'full_bank_launch_admitted':False,
            'actual_harmonic_precision_increased':False,'full_bank_precision_pi':800,'column_precisions':{'0':3200,'1':1600},
            'candidate_identification_proved':False,'field_polynomial_constructed':False,
            'sources':[source(x) for x in sorted(PATHS)]}
    OUT.write_text(json.dumps(result,indent=2)+'\n');print('D132_REVIEW_SOURCES|'+str(len(result['sources'])),flush=True)
    print('PASS|555_DYADIC_STAGED_INTEGRATION_REVIEW',flush=True)
if __name__=='__main__':main()
