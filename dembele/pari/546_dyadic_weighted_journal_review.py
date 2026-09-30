"""D131 fixed finite review: weighted replay, journal recovery and actual correction."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
OUT=DATA/'dyadic_weighted_journal_review_d131.json'
PREFIX='dyadic_weighted_journal_review_d131'
s=importlib.util.spec_from_file_location('independent',ROOT/'dembele/pari/486_dyadic_precision400_independent.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
PATHS={Path(__file__),Path(r.__file__)};CACHE={}


def source(path):
    path=Path(path).resolve();PATHS.add(path)
    if path not in CACHE:CACHE[path]=r.source(path)
    return CACHE[path]


def checked(rows):
    for row in rows:assert source(row['path'])==row,row['path']


def read(stem):
    path=DATA/(stem+'.json');PATHS.add(path);p=json.loads(path.read_text());assert p['status']=='pass';return p


def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()


def envelope(path):
    PATHS.add(path);p=json.loads(path.read_text());assert set(p)=={'value','sha256'}
    assert hashlib.sha256(canonical(p['value'])).hexdigest()==p['sha256'];return p['value']


def sealed_stores():
    roots=sorted(p for p in DATA.glob('dyadic_rowjournal_*_d131') if p.is_dir())
    assert len(roots)==24,len(roots)
    total=history=retired=0;rows=[]
    for root in roots:
        assert not root.is_symlink()
        owner=envelope(root/'OWNER.json');assert owner['payloads_prospectively_transient_until_seal']
        assert owner['storage_source_sha256']==source(ROOT/'dembele/pari/543_dyadic_row_journal.py')['sha256']
        current=envelope(root/'CURRENT.json');seal=envelope(root/'SEALED.json')
        assert owner['cap_bytes']==2147483648
        assert seal['all_remaining_files_frozen'] and seal['history_payload_hashes_are_not_retained_source_hashes']
        assert seal['current_sha256']==hashlib.sha256(canonical(current)).hexdigest()
        assert not any((root/name).exists() for name in ('TXN.json','WAL.json','RETIRE.json','WORKSPACE.bin'))
        assert not list(root.glob('*.tmp')) and not list(root.glob('wal_*.bin'))
        for kind in ('state','aux'):
            d=current[kind];path=root/d['name'];assert path.parent==root and path.stat().st_size==d['row_bytes']*d['rows']==d['bytes']
            assert len(d['row_sha256'])==d['rows'] and source(path)['sha256']==d['sha256']
            with path.open('rb') as f:
                for sha in d['row_sha256']:
                    raw=f.read(d['row_bytes']);assert hashlib.sha256(raw).hexdigest()==sha
                assert not f.read(1)
            total+=d['bytes']
        for path in root.glob('history_*.json'):
            past=envelope(path);assert past['epoch']<current['epoch'];history+=1
        for path in root.glob('retired_*.json'):
            past=envelope(path);assert past['after_tag']==current['tag'] and not (root/past['name']).exists();retired+=1
        live={current[k]['name'] for k in ('state','aux')}
        assert {p.name for p in root.glob('*.bin')}==live
        files=list(root.iterdir());assert all(p.is_file() and not p.is_symlink() for p in files)
        assert sum(p.stat().st_size for p in files)<2147483648
        PATHS.update(files);rows.append({'namespace':root.name,'epoch':current['epoch'],'retained_payload_bytes':sum(current[k]['bytes'] for k in ('state','aux'))})
    assert total==101567858 and history==46 and retired==23,(total,history,retired)
    return {'sealed_namespaces':24,'current_payload_bytes':total,'historical_generation_records':history,
            'retired_correction_payload_records':retired,'all_current_payload_and_row_hashes_checked':True,
            'historical_overwritten_or_retired_payload_hashes_not_treated_as_retained_sources':True,
            'per_store_cap_bytes':2147483648,'aggregate_concurrent_store_cap_claimed':False,'stores':rows}


def direct_row(record,e,count,bits):
    width=(bits+7)//8;length=count*8*width
    with Path(record['path']).open('rb') as f:f.seek(e*length);raw=f.read(length)
    assert len(raw)==length
    return [tuple(int.from_bytes(raw[(k*8+i)*width:(k*8+i+1)*width],'little') for i in range(8)) for k in range(count)]


def independent_correction():
    prep=read('dyadic_weighted_P1600_col00_step01_prepared_d124')
    final=read('dyadic_weighted_P1600_col00_step01_d124')
    checked([prep['operator_input_file'],final['residual_file']])
    transport=read('dyadic_target_transports_d121');ring=r.Quotient(r.FP,800)
    checks=0
    for e in (0,83,173):
        totals={n:ring.zero for n in (1,2,33)}
        for ch in transport['transitions'][e]['children']:
            a,b,c=map(ring.norm,ch['normalized_center'][:3])
            values=direct_row(prep['operator_input_file'],ch['target_edge'],800,100)
            power=[ring.one]+[ring.zero]*799
            for n in range(1,34):
                new=[ring.mul(b,power[0])]
                for k in range(1,800):new.append(ring.sub(ring.add(ring.mul(b,power[k]),ring.mul(a,power[k-1])),ring.mul(c,new[-1])))
                power=new
                if n in totals:
                    v=ring.zero
                    for x,y in zip(power,values):v=ring.add(v,ring.mul(x,y))
                    totals[n]=ring.add(totals[n],v)
        own=direct_row(prep['operator_input_file'],e,800,100)
        assert totals[1]==own[1] and totals[2]==own[2]
        residual=direct_row(final['residual_file'],e,767,96)
        for i,v in enumerate(totals[33]):
            bit=max(0,(1600-33-i+7)//8)
            expected=(v<<100)% (1<<bit)
            assert expected==residual[33][i]<<104
        checks+=24
    return {'sampled_states':[0,83,173],'ordinary_powers_constructed_through':33,
            'checked_degrees':[1,2,33],'scalar_equations_checked':checks,
            'high_residual_and_low_equations_checked':True,'complete_operator_independently_recomputed':False}


def finite():
    a=read('dyadic_weighted_audit_aggregate_d131')['certificates']
    assert a['uniform_coordinate_comparisons']==a['weighted_coordinate_comparisons']==4454400
    assert a['CM_coordinate_comparisons']==870400 and a['weighted_fixed_point_certificate_replayed']
    for kind in ('states','cm'):
        p=read('dyadic_weighted_audit_'+kind+'_d131');assert p['production_arithmetic_not_imported']
        assert p['certificates']['scalar_equations_checked']==72
    small=read('dyadic_rowjournal_small_control_d131')['certificates']
    assert len(small['controls'])==19
    faults=[]
    for c in small['controls']:
        assert c['sealed'] and c['rows']==3 and c['final_direct_byte_comparisons']==162
        assert len(c['interruptions'])==1;faults.append(c['interruptions'][0]['fault'])
        assert c['interruptions'][0]['exit_code']==73 and c['interruptions'][0]['child_inherits_capped_process_group']
    assert len(set(faults))==19
    assert small['corruptions']['corruption_or_stale_WAL_rejections']==4
    assert small['corruptions']['bad_WAL_rejected_before_payload_write'] and small['corruptions']['repeated_recovery_idempotent']
    assert not small['power_loss_or_hardware_fault_testing_claimed']
    actual=read('dyadic_rowjournal_actual_control_d131')['certificates']
    target=read('dyadic_rowjournal_target_control_d131')['certificates']
    assert actual['actual_weighted_addition_scalar_checks']==2227200 and actual['final_direct_byte_comparisons']==41643768
    assert not actual['original_low_solve_and_operator_recomputed']
    assert target['final_direct_byte_comparisons']==18277080 and not target['full_target_bank_or_arithmetic_computed']
    inv=read('dyadic_rowjournal_inventory_control_d131')['certificates']
    assert inv['capacity_bytes']==2147483648 and inv['reserved_workspace_bytes']==67108864
    assert inv['prospective_layout_bytes_excluding_metadata']['sweep']==1217418840+2*375672960+67108864==2035873624
    assert inv['largest_reserved_occupancy_with_metadata']==2035873922<inv['capacity_bytes']
    assert inv['oversized_reservation_rejections']==1 and inv['rejected_file_not_created']
    assert inv['large_capacity_files_logically_reserved_but_not_filled_with_target_data']
    prep=read('dyadic_journal_arithmetic_prepare_d131')['certificates']
    assert prep['original_sparse_low_equation_scalars']==44544 and prep['factor_blocks_decoded']==1226 and prep['all_low_equations_zero']
    assert prep['complete_prepared_weighted_scalar_comparisons']==2227200 and prep['complete_correction_scalar_comparisons']==1113600
    fin=read('dyadic_journal_arithmetic_finish_d131')['certificates']
    assert fin['complete_actual_correction_recomputed'] and fin['original_low_solve_and_GMP_operator_both_recomputed']
    assert fin['before_pi']==800 and fin['after_pi']==833 and fin['all_states']==174
    seen=[];scalar=0
    current=fin['sealed_generation']
    for first in range(0,174,29):
        c=read(f'dyadic_journal_arithmetic_e{first:03d}_{first+28:03d}_d131')['certificates']
        assert c['first_state']==first and c['last_state']==first+28 and c['known_residual_lower_pi']==833
        for row in c['rows']:
            assert row['state']==len(seen) and row['sha256']==current['aux']['row_sha256'][len(seen)];seen.append(row)
        scalar+=c['new_residual_scalar_comparisons']
    assert len(seen)==174 and scalar==1067664
    independent=independent_correction()
    return {'weighted_replay':a,'process_interruption_children':22,'distinct_small_interruption_points':19,
            'corruption_and_stale_WAL_rejections':4,'power_loss_testing_claimed':False,
            'target_capacity_control':inv,'fresh_actual_correction':{
                'original_RHS_child_actions':348,'original_low_equation_scalars':44544,
                'GMP_original_correction_child_actions':348,'new_residual_scalar_comparisons':scalar,
                'residual_lower_before_pi':800,'residual_lower_after_pi':833,
                'independent_samples':independent},'actual_precision_increased':False}


def build():
    prior=read('dyadic_target_feasibility_review_d130');assert len(prior['sources'])==16142
    checked(prior['sources'])
    for stem in ('dyadic_target_feasibility_review_d130_attempt01','dyadic_target_feasibility_review_d130_recheck01'):
        p=read(stem+'.job');checked(p['sources']+[p['driver'],p['log']])
    read('dyadic_target_feasibility_completion_d130')
    certificates=finite();stores=sealed_stores()
    plans={'dyadic_weighted_replay_plan_d131':36,'dyadic_weighted_audit_plan_d131':3,
           'dyadic_rowjournal_plan_d131':3,'dyadic_journal_arithmetic_plan_d131':6}
    planned=set()
    for stem,count in plans.items():
        summary=read(stem+'_completed');checked([summary['plan'],summary['coordinator']])
        spec=json.loads(Path(summary['plan']['path']).read_text())
        assert summary['completed_jobs']==len(spec['jobs'])==count and 1<=summary['worker_limit']<=3
        for req,got in zip(spec['jobs'],summary['jobs']):
            assert req['stem']==got['stem'] and got['stem'] not in planned;planned.add(got['stem'])
            checked([got['receipt'],got['metadata']]);job=json.loads(Path(got['receipt']['path']).read_text())
            assert job['command']==['python3',str(ROOT/req['driver'])]+req['args']+['--output',req['stem']]
    jobs=[];categories=Counter();peaks=[];stems=set()
    for path in sorted(DATA.glob('*d131*')):
        if path.is_dir() or path.name.startswith(PREFIX) or path.name.startswith('dyadic_weighted_journal_completion_d131'):continue
        PATHS.add(path)
        if path.suffix=='.log':assert path.with_suffix('.job.json').exists()
        if path.suffix!='.json':continue
        packet=json.loads(path.read_text());checked([x for x in packet.get('sources',[]) if isinstance(x,dict) and 'sha256' in x])
        for field in ('peak_rss_bytes','maximum_child_process_peak_rss_bytes'):
            if field in packet:peaks.append(packet[field])
        if not path.name.endswith('.job.json'):continue
        assert packet['status']=='pass' and packet['exit_code']==0
        assert packet['timeout_seconds']==180 and packet['timeout_terminates_process_group']
        checked([packet['driver'],packet['log']]);command=packet['command'];stem=command[command.index('--output')+1]
        assert stem not in stems;stems.add(stem)
        metadata=DATA/(stem+'.json');read(stem)
        bindings=[json.loads(line.split('|',1)[1]) for line in Path(packet['log']['path']).read_text().splitlines() if line.startswith('PHASE_METADATA|')]
        assert bindings==[source(metadata)]
        name=Path(packet['driver']['path']).name;categories[name]+=1
        jobs.append({'receipt':path.name,'driver':name,'wall_seconds':packet['wall_seconds']})
    assert len(jobs)==54
    assert dict(categories)=={'541_dyadic_weighted_certificate.py':37,'542_dyadic_weighted_independent.py':3,
                              '544_dyadic_row_journal_controls.py':4,'545_dyadic_journal_arithmetic_control.py':10}
    assert stems-planned=={'dyadic_weighted_manifest_d131','dyadic_rowjournal_small_control_d131',
        'dyadic_journal_arithmetic_init_d131','dyadic_journal_arithmetic_prepare_d131',
        'dyadic_journal_arithmetic_begin_d131','dyadic_journal_arithmetic_finish_d131'}
    stats={'passed':54,'failed':0,'sum_wall_seconds':sum(x['wall_seconds'] for x in jobs),
           'maximum_wall_seconds':max(x['wall_seconds'] for x in jobs),'maximum_single_process_peak_rss_bytes':max(peaks)}
    ledger=read('dyadic_weighted_journal_sources_d131');assert ledger['execution_status']=='complete'
    for k,val in stats.items():assert abs(val-ledger['bounded_input_jobs'][k])<1e-6,k
    PATHS.add(ROOT/'dembele/certificates/dyadic-weighted-journal-d131.md')
    PATHS.add(ROOT/'dembele/pari/run_d131_batch.py')
    manifest=[source(p) for p in sorted(PATHS)]
    assert {(x['path'],x['sha256']) for x in prior['sources']}<={(x['path'],x['sha256']) for x in manifest}
    return {'status':'pass','milestone':'D131','independent_finite_review_complete':True,
            'production_arithmetic_not_imported_by_reviewer':True,'inherited_D130_hashes_preserved':16142,
            'finite_certificates':certificates,'sealed_storage_review':stores,
            'bounded_input_jobs':jobs,'input_job_categories':dict(categories),'input_job_statistics':stats,
            'actual_harmonic_precision_increased':False,'full_bank_precision_pi':800,
            'actual_column_precisions':{'0':3200,'1':1600},'candidate_identification_proved':False,
            'target_field_polynomial_constructed':False,'full_target_run_admitted':False,'sources':manifest}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    if args.check:
        result=json.loads(OUT.read_text());assert result['status']=='pass' and result['independent_finite_review_complete'];checked(result['sources'])
    else:
        assert not OUT.exists();result=build();OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'sources':len(result['sources']),'input_jobs':len(result['bounded_input_jobs'])}),flush=True)
    print('PASS|546_DYADIC_WEIGHTED_JOURNAL_REVIEW',flush=True)
