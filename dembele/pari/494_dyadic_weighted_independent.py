"""D123 independent audit of the weighted lattice and shrinking pilot.

Only source 486's separate integer quotient arithmetic is imported.
Variable-width inputs are decoded here, then compared by pi-valuations
with every frozen uniform checkpoint. Original coefficients are obtained
by ordinary rational-series recurrence, not production transport plans.
"""
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('independent',ROOT/'dembele/pari/486_dyadic_precision400_independent.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
PATHS={Path(__file__),Path(r.__file__)};P=800;R=32


def read(stem):
    path=DATA/(stem+'.json');PATHS.add(path);row=json.loads(path.read_text());assert row['status']=='pass'
    for file in row.get('checkpoint_files',[]):assert r.source(file['path'])==file;PATHS.add(Path(file['path']))
    return row


def raw_file(file):
    path=Path(file['path']);assert r.source(path)==file;PATHS.add(path);return path.read_bytes()


def uniform(file,nr,nc,bits):
    raw=raw_file(file);width=(bits+7)//8;assert len(raw)==nr*nc*8*width
    result=[];offset=0
    for e in range(nr):
        edge=[]
        for k in range(nc):
            row=[]
            for i in range(8):
                c=int.from_bytes(raw[offset:offset+width],'little');assert c<1<<bits
                row.append(c);offset+=width
            edge.append(tuple(row))
        result.append(edge)
    return result


def weighted(file,full_low):
    raw=raw_file(file);offset=0;result=[]
    for e in range(174):
        edge=[]
        for k in range(P):
            precision=P if full_low and k<=R else P-k;row=[]
            for i in range(8):
                needed=max(0,-((i-precision)//8));width=-(-needed//8)
                c=int.from_bytes(raw[offset:offset+width],'little');offset+=width
                assert c<1<<needed;row.append(c)
            edge.append(tuple(row))
        result.append(edge)
    assert offset==len(raw);return result


def compare(ring,small,large,full_low):
    count=0
    for e,edge in enumerate(small):
        for k,x in enumerate(edge):
            target=P if full_low and k<=R else P-k
            assert ring.value(ring.sub(x,large[e][k]))>=target,(e,k,target)
            count+=8
    return count


def recurrence(ring,maps,values,state,degrees):
    answer={n:ring.zero for n in degrees}
    for child in maps[state]['children']:
        a,b,c=[ring.norm(x) for x in child['normalized_center'][:3]]
        power=[ring.one]+[ring.zero]*(P-1)
        for n in range(1,max(degrees)+1):
            new=[ring.mul(b,power[0])]
            for k in range(1,P):
                new.append(ring.sub(ring.add(ring.mul(b,power[k]),ring.mul(a,power[k-1])),ring.mul(c,new[-1])))
            power=new
            if n in degrees:
                value=ring.zero
                for coefficient,moment in zip(power,values[child['target_edge']]):value=ring.add(value,ring.mul(coefficient,moment))
                answer[n]=ring.add(answer[n],value)
    return answer


def build():
    start=time.monotonic();ring=r.Quotient(r.FP,P)
    maps=read('dyadic_target_transports_d121')['transitions'];mapchecks=0
    for state in maps:
        for child in state['children']:
            assert child['normalized_error_pi']>=P
            a,b,c=[ring.norm(x) for x in child['normalized_center'][:3]]
            assert ring.value(c)>=1 and ring.value(ring.sub(a,ring.mul(b,c)))>=1
            mapchecks+=1
    assert mapchecks==348
    reference=read('dyadic_staged_P800_col00_verified_d123')
    values=uniform(reference['state_file'],174,P,P//8)
    control=read('dyadic_weighted_precision_control_d123')
    compact=weighted(control['checkpoint_files'][0],False)
    early_count=compare(ring,compact,values,False)
    assert all(a[0]==b[0] for a,b in zip(compact,values))
    state_count=residual_count=0;band_counts=[]
    for step in range(13):
        suffix=('seed' if step==0 else f'step{step:02d}')+'_d123'
        packet=read('dyadic_shrinking_P800_col00_'+suffix)
        old=read('dyadic_staged_P800_col00_'+suffix)
        u=400+33*step;count=max(R+1,P-u);band_counts.append(count)
        assert packet['weighted_residual_lower_bound_pi']==u and packet['active_moment_count']==count
        assert packet['correction_steps']==step and old['residual_lower_bound_pi']==u
        compact=weighted(packet['state_file'],True)
        baseline=uniform(old['state_file'],174,P,P//8)
        state_count+=compare(ring,compact,baseline,True)
        assert all(a[0]==b[0] for a,b in zip(compact,baseline))
        shift=packet['residual_power_of_two_shift'];bits=packet['residual_modulus_bits']
        assert shift==u//8 and bits==P//8-shift
        residual=uniform(packet['residual_file'],174,count,bits)
        residual=[[tuple(c<<shift for c in x) for x in edge] for edge in residual]
        for edge in residual:
            assert all(x==ring.zero for x in edge[:R+1])
            assert all(ring.value(x)>=u for x in edge)
        original=uniform(old['residual_file'],174,P,P//8)
        residual_count+=compare(ring,residual,original,True)
    assert band_counts==[400,367,334,301,268,235,202,169,136,103,70,37,33]
    assert all(x==ring.zero for edge in residual for x in edge)
    full=read('dyadic_shrinking_P800_col00_verified_d123')
    output=uniform(full['checkpoint_files'][0],174,P,P//8);assert output==values
    assert full['weighted_residual_condition_checked'] and full['full_precision_reconstruction_equals_verified_column']
    assert full['correction_steps']==12
    final_weighted=compare(ring,compact,output,True)
    harmonic=read('dyadic_harmonic_certificate_d111')['harmonic_basis'][0]
    for e,mass in enumerate(harmonic):assert compact[e][0]==output[e][0]==(mass&ring.mask,)+(0,)*7
    print(f'WEIGHTED_INDEPENDENT|states={state_count}; residuals={residual_count}; seconds={time.monotonic()-start:.3f}',flush=True)
    sampled=0
    for e in (0,61,173):
        for degree,value in recurrence(ring,maps,compact,e,(1,2,33,64)).items():
            assert value==output[e][degree];sampled+=8
    pilot=read('dyadic_shrinking_pilot_d123')
    assert pilot['completed_phases']==14 and pilot['correction_steps']==12
    return {'status':'pass','milestone':'D123','working_precision_pi':P,
        'child_maps_with_integral_column_divisibility_checked':mapchecks,
        'early_compact_input_scalar_checks':early_count,
        'all_thirteen_shrinking_state_scalar_checks':state_count,
        'all_thirteen_active_residual_scalar_checks':residual_count,
        'active_moment_counts':band_counts,'exact_harmonic_masses_checked':174,
        'full_uniform_reconstruction_scalar_checks':174*P*8,
        'final_weighted_residual_scalar_checks':final_weighted,
        'independent_original_recurrence_from_weighted_input_scalar_checks':sampled,
        'production_arithmetic_not_imported':True,'shrinking_correction_stage_passes':True,
        'uses_existing_P800_seed':True,'full_sixteen_column_bank_precision_pi':400,
        'quadric_bounds_changed':False,'candidate_identification_proved':False,
        'target_field_polynomial_constructed':False,'wall_seconds':time.monotonic()-start,
        'sources':[r.source(path) for path in sorted(PATHS)]}


if __name__=='__main__':
    out=DATA/'dyadic_weighted_independent_d123.json';assert not out.exists()
    result=build();out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='sources'}),flush=True)
    print('PASS|494_DYADIC_WEIGHTED_INDEPENDENT',flush=True)
