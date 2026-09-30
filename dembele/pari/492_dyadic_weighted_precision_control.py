"""D123 control weighted input precision against the actual P=800 column.

For fixed masses, the k-th positive input column of T is divisible by
pi^k. Thus T maps I_P={e:e_0=0, v(e_k)>=max(0,P-k)} to pi^P.
If Tx-x is in I_P, y=Tx has full original residual zero modulo pi^P.
This control assembles an input from earlier frozen Schur checkpoints,
packs only the required coordinate bits, and independently reconstructs
the full verified column with the older GMP polynomial backend. It is
not a newly implemented shrinking-band solver or a target-size cost.
"""
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('staged',ROOT/'dembele/pari/489_dyadic_staged_lift.py')
h=importlib.util.module_from_spec(s);s.loader.exec_module(h)


def bit_count(P,k,i):
    # The Eisenstein basis terms have distinct valuations modulo eight.
    return max(0,(P-k-i+7)//8)


def build():
    start=time.monotonic();P=800;R=32
    final,finalpath=h.read('dyadic_staged_P800_col00_verified_d123')
    assert final['certificate']['original_full_residual_zero']
    verified=h.state(final);compact=[[None]*P for _ in range(174)]
    assigned=[False]*P;selection=[];before=0;last_values=None
    for step in range(13):
        stem='dyadic_staged_P800_col00_'+('seed' if step==0 else f'step{step:02d}')+'_d123'
        packet,path=h.read(stem);u=packet['residual_lower_bound_pi']
        assert packet['kind']=='checkpoint' and u==400+33*step and u>before
        before=u;values=h.state(packet);last_values=values
        residual=h.binary(packet['residual_file'],174,P,P//8)
        assert all(x==h.ZERO for edge in residual for x in edge[:R+1])
        assert h.l.value(residual,P)==u
        ks=[k for k in range(R+1,P) if not assigned[k] and u+k>=P]
        for k in ks:
            assigned[k]=True
            masks=[(1<<bit_count(P,k,i))-1 for i in range(8)]
            for e in range(174):compact[e][k]=tuple(c&m for c,m in zip(values[e][k],masks))
        selection.append({'checkpoint':h.source(path),'residual_precision_pi':u,
            'first_selected_moment':min(ks) if ks else None,'last_selected_moment':max(ks) if ks else None,
            'selected_moments':len(ks)})
    # A zero low residual and an integral low-block inverse imply that
    # low errors have valuation >= u+R+1, now exceeding P.
    assert before+R+1>=P and all(assigned[R+1:])
    for e in range(174):
        assert last_values[e][:R+1]==verified[e][:R+1]
        compact[e][0]=last_values[e][0]
        for k in range(1,R+1):
            compact[e][k]=tuple(c&((1<<bit_count(P,k,i))-1) for i,c in enumerate(last_values[e][k]))
    selection.append({'checkpoint':selection[-1]['checkpoint'],'low_moments':[0,R],
        'low_error_lower_bound_pi':before+R+1,'selected_moments':R+1})
    # Full comparison uses the certified reference, not a valuation
    # sampled at a few states or degrees.
    checked=0
    for e in range(174):
        assert compact[e][0]==verified[e][0]
        for k in range(P):
            for i,c in enumerate(compact[e][k]):
                bits=bit_count(P,k,i);assert (c-verified[e][k][i])&((1<<bits)-1)==0
                checked+=1
    payload=bytearray()
    for edge in compact:
        for k,x in enumerate(edge):
            for i,c in enumerate(x):payload.extend(c.to_bytes((bit_count(P,k,i)+7)//8,'little'))
    pointer=0;unpacked=[]
    for e in range(174):
        edge=[]
        for k in range(P):
            row=[]
            for i in range(8):
                width=(bit_count(P,k,i)+7)//8
                row.append(int.from_bytes(payload[pointer:pointer+width],'little'));pointer+=width
            edge.append(tuple(row))
        unpacked.append(edge)
    assert pointer==len(payload) and unpacked==compact
    packing_seconds=time.monotonic()-start
    print(f'WEIGHTED_INPUT|bytes={len(payload)}; scalar checks={checked}; seconds={packing_seconds:.3f}',flush=True)
    engine=h.Engine(P);reconstructed=engine.apply(unpacked,0,173,'GMP')
    assert reconstructed==verified
    for e in range(174):
        assert reconstructed[e][0]==compact[e][0]
        for k in range(1,P):
            for i,c in enumerate(compact[e][k]):
                assert (reconstructed[e][k][i]-c)&((1<<bit_count(P,k,i))-1)==0
    path=DATA/'dyadic_weighted_precision_control_d123_input.bin';assert not path.exists()
    path.write_bytes(payload);file=h.source(path)
    h.PATHS.update([Path(__file__),Path(h.__file__)])
    full_bytes=Path(final['state_file']['path']).stat().st_size
    return {'status':'pass','milestone':'D123','working_precision_pi':P,'harmonic_basis_column':0,
        'weighted_ideal':'e_0=0; v_pi(e_k)>=max(0,P-k) for k>0',
        'coordinate_bit_count':'max(0,ceil((P-k-i)/8))',
        'full_weighted_reference_scalar_checks':checked,'full_reconstructed_scalar_checks':174*P*8,
        'original_operator_backend':'GMP','weighted_residual_condition_checked':True,
        'original_operator_reconstruction_equals_verified_column':True,
        'selection':selection,'last_required_baseline_correction':12,
        'last_baseline_uniform_residual_precision_pi':before,'low_error_bound_pi':before+R+1,
        'compact_input_bytes':len(payload),'uniform_input_bytes':full_bytes,
        'compact_to_uniform_byte_ratio':len(payload)/full_bytes,
        'packing_and_source_checks_seconds':packing_seconds,'operator_timings':engine.times,
        'checkpoint_files':[file],'frozen_reference_metadata':h.source(finalpath),
        'shrinking_band_solver_implemented':False,'full_sixteen_column_bank_precision_pi':400,
        'quadric_bounds_changed':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,'wall_seconds':time.monotonic()-start,
        'sources':[h.source(x) for x in sorted(h.PATHS)]}


if __name__=='__main__':
    out=DATA/'dyadic_weighted_precision_control_d123.json';assert not out.exists()
    result=build();out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['sources','selection','checkpoint_files']}),flush=True)
    print('PASS|492_DYADIC_WEIGHTED_PRECISION_CONTROL',flush=True)
