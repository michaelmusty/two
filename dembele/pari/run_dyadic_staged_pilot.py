"""Resume the D123 single-column pilot; every mathematical phase is capped.

This outer coordinator runs at most three disjoint state chunks at once.
It skips only successful saved receipts, never overwrites them, and stops
on failed or incomplete receipts rather than blindly retrying a command.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
DRIVER='dembele/pari/489_dyadic_staged_lift.py';WRAPPER='dembele/pari/run_dyadic_capped.py'
MARKER='PASS|489_DYADIC_STAGED_LIFT'


def source(path):
    path=Path(path).resolve();h=hashlib.sha256()
    with path.open('rb') as f:
        while data:=f.read(1<<20):h.update(data)
    return {'path':str(path),'sha256':h.hexdigest()}


def job(phase,stem,extra):
    receipt=DATA/(stem+'_attempt01.job.json');log=DATA/(stem+'_attempt01.log');out=DATA/(stem+'.json')
    if not receipt.exists():
        assert not log.exists() and not out.exists(),('incomplete phase needs inspection',stem)
        command=['python3',WRAPPER,DRIVER,stem+'_attempt01',MARKER,'--phase',phase,'--output',stem]+extra
        completed=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        if completed.returncode:
            print(completed.stdout+completed.stderr,flush=True)
            raise RuntimeError('bounded phase failed: '+stem)
    saved=json.loads(receipt.read_text());assert saved['status']=='pass' and saved['exit_code']==0
    assert saved['timeout_seconds']==180 and saved['timeout_terminates_process_group']
    assert source(saved['driver']['path'])==saved['driver'] and source(saved['log']['path'])==saved['log']
    packet=json.loads(out.read_text());assert packet['status']=='pass' and packet['phase']==phase
    print('PILOT_PHASE|'+json.dumps({'stem':stem,'seconds':saved['wall_seconds'],
        'residual_pi':packet.get('residual_lower_bound_pi')}),flush=True)
    return packet,receipt


def main(P,column,chunk_size,workers):
    start=time.monotonic();base=f'dyadic_staged_P{P}_col{column:02d}';jobs=[]
    summary=DATA/f'dyadic_staged_pilot_P{P}_col{column:02d}_d123.json'
    assert not summary.exists(), 'pilot already complete; inspect its saved result'
    seed='dyadic_actual_P400_col0_verified_d121' if column==0 else f'dyadic_actual_P400_col{column:02d}_verified_d122'
    def one(phase,stem,args):
        packet,receipt=job(phase,stem,args);jobs.append(receipt);return packet
    def sweep(previous,prefix,backend='FLINT'):
        items=[(first,min(first+chunk_size-1,173)) for first in range(0,174,chunk_size)]
        def run(item):
            first,last=item;stem=f'{prefix}_e{first:03d}_{last:03d}'
            return job('sweep',stem,['--previous',previous,'--first',str(first),'--last',str(last),'--backend',backend])
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for _,receipt in pool.map(run,items):jobs.append(receipt)
    init=base+'_input_d123';one('init',init,['--precision',str(P),'--seed',seed])
    extended=base+'_extend_d123';sweep(init,extended)
    low=base+'_seed_low_d123';one('seed-low',low,['--previous',init,'--chunks',extended])
    prefix=base+'_seed_operator_d123';sweep(low,prefix)
    previous=base+'_seed_d123';packet=one('finish-seed',previous,['--previous',low,'--chunks',prefix])
    step=0
    while packet['residual_lower_bound_pi']<P:
        step+=1;assert step<=((P-400+32)//33)+1
        prepared=base+f'_step{step:02d}_prepared_d123'
        one('prepare-step',prepared,['--previous',previous])
        prefix=base+f'_step{step:02d}_operator_d123';sweep(prepared,prefix)
        previous=base+f'_step{step:02d}_d123'
        packet=one('finish-step',previous,['--previous',prepared,'--chunks',prefix])
    prefix=base+'_verify_operator_d123';sweep(previous,prefix,'GMP')
    verified=base+'_verified_d123';packet=one('finish-verify',verified,['--previous',previous,'--chunks',prefix])
    assert packet['certificate']['original_full_residual_zero'] and packet['actual_moment_precision_increased']
    rows=[json.loads(path.read_text()) for path in jobs]
    result={'status':'pass','milestone':'D123','precision_pi':P,'harmonic_basis_column':column,
        'chunk_size':chunk_size,'concurrent_chunk_workers':workers,'correction_steps':step,
        'correction_history':packet['correction_history'],'verified_checkpoint':source(DATA/(verified+'.json')),
        'completed_phases':len(jobs),'sum_recorded_phase_seconds':sum(x['wall_seconds'] for x in rows),
        'maximum_phase_seconds':max(x['wall_seconds'] for x in rows),'coordinator_wall_seconds':time.monotonic()-start,
        'each_mathematical_phase_has_180_second_process_group_cap':True,
        'sources':[source(path) for path in [Path(__file__),ROOT/DRIVER,ROOT/WRAPPER,*jobs]]}
    summary.write_text(json.dumps(result,indent=2)+'\n')
    print('PILOT_COMPLETE|'+json.dumps({k:v for k,v in result.items() if k!='sources'}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--precision',type=int,default=800)
    parser.add_argument('--column',type=int,default=0);parser.add_argument('--chunk-size',type=int,default=29)
    parser.add_argument('--workers',type=int,default=3);args=parser.parse_args()
    assert 0<=args.column<16 and 1<=args.chunk_size<=174 and 1<=args.workers<=3
    main(args.precision,args.column,args.chunk_size,args.workers)
