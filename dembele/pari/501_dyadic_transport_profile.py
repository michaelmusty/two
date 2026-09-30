"""D124 profile actual low-row transports, with independent-backend controls."""
import cProfile
import importlib.util
import json
from pathlib import Path
import pstats
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('weighted',ROOT/'dembele/pari/497_dyadic_weighted_chunks.py')
w=importlib.util.module_from_spec(s);s.loader.exec_module(w);h=w.h


def build():
    start=time.monotonic();packet,path=h.read('dyadic_weighted_P1600_col00_step01_prepared_d124')
    P=packet['working_precision_pi'];assert P==1600
    values=w.scaled_values(packet['operator_input_file'],174,packet['input_count'],P,packet['correction_power_of_two_shift'])
    engine=w.Engine(P);states=(0,17,61,98,173);answers={};profile=cProfile.Profile()
    begin=time.monotonic()
    for e in states:
        answer,_=profile.runcall(engine.apply_rows,values,33,e,e,'FLINT')
        assert answer[0]==values[e][:33];answers[e]=answer
    profiled_seconds=time.monotonic()-begin
    begin=time.monotonic()
    for e in states:
        answer,_=engine.apply_rows(values,33,e,e,'GMP');assert answer==answers[e]
    independent_seconds=time.monotonic()-begin
    entries=[]
    for (file,line,fn),(primitive,calls,self_seconds,total_seconds,callers) in pstats.Stats(profile).stats.items():
        entries.append({'file':file,'line':line,'function':fn,'calls':calls,
            'self_seconds':self_seconds,'cumulative_seconds':total_seconds})
    entries.sort(key=lambda row:row['self_seconds'],reverse=True)
    h.PATHS.update([Path(__file__),Path(w.__file__)])
    return {'status':'pass','milestone':'D124','working_precision_pi':P,'actual_input_precision_pi':800,
        'profiled_states':list(states),'output_moments':33,'original_low_equation_scalar_checks':len(states)*33*8,
        'older_GMP_backend_scalar_comparisons':len(states)*33*8,
        'profiled_FLINT_seconds':profiled_seconds,'unprofiled_GMP_seconds':independent_seconds,
        'timing_caveat':'Profiling overhead is included only in the FLINT figure; these are not speed-comparison timings.',
        'top_functions_by_self_time':entries[:25],'top_functions_by_cumulative_time':sorted(entries,key=lambda row:row['cumulative_seconds'],reverse=True)[:20],
        'input_metadata':h.source(path),'wall_seconds':time.monotonic()-start,'peak_rss_bytes':w.peak_rss(),
        'no_new_harmonic_column':True,'sources':[h.source(path) for path in sorted(h.PATHS)]}


if __name__=='__main__':
    out=DATA/'dyadic_transport_profile_d124.json';assert not out.exists()
    result=build();out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['sources','top_functions_by_cumulative_time']}),flush=True)
    print('PASS|501_DYADIC_TRANSPORT_PROFILE',flush=True)
