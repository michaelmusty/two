"""D124 resumable weighted P=1600 pilot; each mathematical phase is capped."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
DRIVER='dembele/pari/497_dyadic_weighted_chunks.py';WRAPPER='dembele/pari/run_dyadic_capped.py'


def source(path):
    path=Path(path).resolve();sha=hashlib.sha256()
    with path.open('rb') as file:
        while block:=file.read(1<<20):sha.update(block)
    return {'path':str(path),'sha256':sha.hexdigest()}


def main(workers,chunk):
    start=time.monotonic();P=1600;base='dyadic_weighted_P1600_col00';jobs=[]
    summary=DATA/'dyadic_weighted_pilot_P1600_col00_d124.json';assert not summary.exists()
    def job(phase,stem,extra):
        receipt=DATA/(stem+'_attempt01.job.json');log=DATA/(stem+'_attempt01.log');out=DATA/(stem+'.json')
        cmd=['python3',WRAPPER,DRIVER,stem+'_attempt01','PASS|497_DYADIC_WEIGHTED_CHUNKS',
            '--phase',phase,'--output',stem]+extra
        resumed=receipt.exists()
        if not resumed:
            assert not log.exists() and not out.exists(),('inspect incomplete phase before resuming',stem)
            completed=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
            if completed.returncode:print(completed.stdout+completed.stderr,flush=True);raise RuntimeError(stem)
        row=json.loads(receipt.read_text());assert row['status']=='pass' and row['exit_code']==0
        assert row['timeout_seconds']==180 and row['timeout_terminates_process_group']
        assert row['command']==['python3',str(ROOT/DRIVER)]+cmd[5:]
        assert source(row['driver']['path'])==row['driver'] and source(row['log']['path'])==row['log']
        packet=json.loads(out.read_text());assert packet['status']=='pass' and packet['phase']==phase
        print('WEIGHTED_PILOT_PHASE|'+json.dumps({'stem':stem,'seconds':row['wall_seconds'],
            'peak_rss_bytes':packet['peak_rss_bytes'],'precision_pi':packet.get('weighted_residual_lower_bound_pi'),
            'active_moments':packet.get('active_moment_count'),'resumed':resumed}),flush=True)
        return packet,receipt,out,resumed
    def one(phase,stem,extra):
        packet,receipt,out,resumed=job(phase,stem,extra);jobs.append((receipt,out,resumed));return packet
    def sweep(previous,prefix,purpose):
        ranges=[(first,min(first+chunk-1,173)) for first in range(0,174,chunk)]
        def run(bounds):
            first,last=bounds
            return job('sweep',f'{prefix}_e{first:03d}_{last:03d}',
                ['--previous',previous,'--purpose',purpose,'--first',str(first),'--last',str(last)])
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for packet,receipt,out,resumed in pool.map(run,ranges):jobs.append((receipt,out,resumed))
    initial=base+'_input_d124'
    one('init',initial,['--precision','1600','--seed','dyadic_staged_P800_col00_verified_d123'])
    extension=base+'_extend_d124';sweep(initial,extension,'extend')
    seed=base+'_seed_assembled_d124';one('seed-assemble',seed,['--previous',initial,'--chunks',extension])
    rhs=base+'_seed_rhs_d124';sweep(seed,rhs,'seed-low-rhs')
    low=base+'_seed_low_d124';one('seed-low-finish',low,['--previous',seed,'--chunks',rhs])
    prefix=base+'_seed_operator_d124';sweep(low,prefix,'seed-residual')
    previous=base+'_seed_d124';packet=one('finish-seed',previous,['--previous',low,'--chunks',prefix])
    step=0
    while packet['active_moment_count']>33:
        step+=1;assert step<=24
        prepared=base+f'_step{step:02d}_prepared_d124';one('prepare-step',prepared,['--previous',previous])
        prefix=base+f'_step{step:02d}_operator_d124';sweep(prepared,prefix,'correction')
        previous=base+f'_step{step:02d}_d124';packet=one('finish-step',previous,['--previous',prepared,'--chunks',prefix])
    prefix=base+'_reconstruct_operator_d124';sweep(previous,prefix,'reconstruct')
    reconstructed=base+'_reconstructed_d124'
    one('finish-reconstruct',reconstructed,['--previous',previous,'--chunks',prefix])
    prefix=base+'_verify_operator_d124';sweep(reconstructed,prefix,'verify')
    verified=base+'_verified_d124';packet=one('finish-verify',verified,['--previous',reconstructed,'--chunks',prefix])
    assert packet['certificate']['original_full_residual_zero'] and packet['actual_moment_precision_increased']
    rows=[json.loads(receipt.read_text()) for receipt,_,_ in jobs]
    outputs=[json.loads(out.read_text()) for _,out,_ in jobs]
    files={file['path'] for row in outputs for file in row['checkpoint_files']}
    result={'status':'pass','milestone':'D124','working_precision_pi':P,'harmonic_basis_column':0,
        'concurrent_chunk_workers':workers,'chunk_size':chunk,'completed_phases':len(jobs),'correction_steps':step,
        'correction_history':packet['correction_history'],'verified_checkpoint':source(DATA/(verified+'.json')),
        'sum_recorded_phase_seconds':sum(row['wall_seconds'] for row in rows),
        'maximum_phase_seconds':max(row['wall_seconds'] for row in rows),
        'maximum_single_phase_peak_rss_bytes':max(row['peak_rss_bytes'] for row in outputs),
        'coordinator_current_invocation_wall_seconds':time.monotonic()-start,
        'phases_resumed_from_prior_invocations':sum(resumed for _,_,resumed in jobs),
        'distinct_checkpoint_payload_bytes':sum(Path(file).stat().st_size for file in files),
        'full_sixteen_column_bank_precision_pi':400,'full_P10552_solve_costed':False,
        'sources':[source(path) for path in [Path(__file__),ROOT/DRIVER,ROOT/WRAPPER,*[r for r,_,_ in jobs]]]}
    summary.write_text(json.dumps(result,indent=2)+'\n')
    print('WEIGHTED_PILOT_COMPLETE|'+json.dumps({k:v for k,v in result.items() if k!='sources'}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--chunk-size',type=int,default=29);args=parser.parse_args()
    assert 1<=args.workers<=3 and 1<=args.chunk_size<=29
    main(args.workers,args.chunk_size)
