"""D123 independent recurrence, seed-tail and CM checks for the P=800 pilot."""
import importlib.util
import json
from math import comb
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('independent',ROOT/'dembele/pari/486_dyadic_precision400_independent.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
PATHS={Path(__file__),Path(r.__file__)}


def read(stem):
    path=DATA/(stem+'.json');PATHS.add(path);packet=json.loads(path.read_text());assert packet['status']=='pass'
    for row in packet.get('checkpoint_files',[]):assert r.source(row['path'])==row;PATHS.add(Path(row['path']))
    return packet


def binary(path,nr,nc,P):
    path=Path(path);PATHS.add(path);raw=path.read_bytes();width=(P//8+7)//8
    assert len(raw)==nr*nc*8*width
    return [[tuple(int.from_bytes(raw[((e*nc+k)*8+i)*width:((e*nc+k)*8+i+1)*width],'little') for i in range(8))
        for k in range(nc)] for e in range(nr)]


def recurrence(ring,maps,moments,state,degrees,count):
    totals={n:ring.zero for n in degrees}
    for child in maps[state]['children']:
        a,b,c=[ring.norm(row) for row in child['normalized_center'][:3]]
        power=[ring.one]+[ring.zero]*(count-1)
        for n in range(1,max(degrees)+1):
            new=[ring.mul(b,power[0])]
            for k in range(1,count):
                new.append(ring.sub(ring.add(ring.mul(b,power[k]),ring.mul(a,power[k-1])),ring.mul(c,new[-1])))
            power=new
            if n in degrees:
                value=ring.zero
                for x,y in zip(power,moments[child['target_edge']][:count]):value=ring.add(value,ring.mul(x,y))
                totals[n]=ring.add(totals[n],value)
    return totals


def build():
    start=time.monotonic();P=800
    packet=read('dyadic_staged_P800_col00_verified_d123');assert packet['actual_moment_precision_increased']
    assert packet['working_precision_pi']==P and packet['harmonic_basis_column']==0
    assert packet['certificate']['original_full_residual_zero']
    assert packet['certificate']['full_residual_uses_different_polynomial_backend_from_lift']
    values=binary(packet['state_file']['path'],174,P,P)
    residual=Path(packet['residual_file']['path']);PATHS.add(residual)
    raw=residual.read_bytes();assert len(raw)==174*P*8*13 and not any(raw)
    old=read('dyadic_actual_P400_col0_verified_d121')
    seed=binary(old['checkpoint_files'][0]['path'],174,400,400);mask=(1<<50)-1
    assert [[tuple(x&mask for x in row) for row in edge[:400]] for edge in values]==seed
    maps=read('dyadic_target_transports_d121')['transitions'];ring=r.Quotient(r.FP,P)
    checked=0
    for e in (0,17,61,98,173):
        totals=recurrence(ring,maps,values,e,(1,2,33,64),P)
        for n,x in totals.items():assert x==values[e][n];checked+=8
    # Independently test the newly reconstructed high seed moments, using
    # only the old low bank and ordinary coefficient recurrence.
    small=r.Quotient(r.FP,400);tail=recurrence(small,maps,seed,0,(400,599,799),400)
    for n,x in tail.items():assert x==tuple(c&mask for c in values[0][n])
    print(f'P800_INDEPENDENT_STATES|sampled scalars={checked}; high seed scalars=24; seconds={time.monotonic()-start:.3f}',flush=True)
    factor=read('dyadic_low_factor_P800_r32_d123')
    assert factor['all_P400_factor_coefficients_agree'] and factor['original_sparse_residual_checked']
    assert factor['unrelated_rhs_columns']==2 and factor['diagonal_inverse_products_checked']==174
    cm=read('dyadic_staged_CM_P800_col00_d123')
    assert cm['coarse_error_beta']==[1632,1648,1632,1664] and cm['CM_cutoff']==1599
    moments=binary(cm['checkpoint_files'][0]['path'],17,1600,P)
    qring=r.Quotient(r.MP,1664)
    pi=qring.sub(qring.scale(qring.one,-2),qring.mul(qring.beta,qring.beta))
    q=qring.sub(tuple(r.MP[1:]),qring.beta);assert qring.mul(q,qring.beta)==pi
    powers=[qring.one]
    for _ in range(7):powers.append(qring.mul(powers[-1],pi))
    kernels=[]
    for order in range(4):
        n=2*order+2
        kernels.append([0]+[-sum(comb(n,i)*comb(n+k-i-1,k-i) for i in range(min(n,k)+1)) for k in range(1,1600)])
    coarse=0
    for ci,chart in enumerate(moments):
        embedded=[]
        for row in chart:
            x=qring.zero
            for c,a in zip(row,powers):x=qring.add(x,qring.scale(a,c))
            embedded.append(x)
        for order,cs in enumerate(kernels):
            x=qring.zero
            for c,a in reversed(list(zip(cs,embedded))):x=qring.add(qring.mul(x,q),qring.scale(a,c))
            assert x==tuple(cm['CM_values'][ci]['coarse_coefficients_beta'][order]);coarse+=1
    pilot=read('dyadic_staged_pilot_P800_col00_d123')
    assert pilot['correction_history']==packet['correction_history']
    assert pilot['correction_steps']==len(packet['correction_history'])==13
    before=400
    for step in packet['correction_history']:
        assert step['before_pi']==before and step['after_pi']>=min(P,before+33)
        before=step['after_pi']
    assert before==P and coarse==68
    # Independently inventory each sweep's ranges and single input hash.
    sweeps={}
    for path in DATA.glob('dyadic_staged_P800_col00_*_e[0-9][0-9][0-9]_[0-9][0-9][0-9].json'):
        row=read(path.stem);key=(row['input_metadata']['path'],row['backend'])
        assert r.source(row['input_metadata']['path'])==row['input_metadata']
        sweeps.setdefault(key,[]).append((row['first_state'],row['last_state']))
    assert len(sweeps)==16
    for rows in sweeps.values():
        cursor=0
        for first,last in sorted(rows):assert first==cursor and last>=first;cursor=last+1
        assert cursor==174
    return {'status':'pass','milestone':'D123','actual_harmonic_columns_refined_to_P800':1,
        'working_precision_pi':P,'full_sixteen_column_bank_precision_pi':400,
        'frozen_P400_low_scalar_overlaps_checked':174*400*8,'production_original_residual_scalar_checks':174*P*8,
        'independent_original_recurrence_scalar_checks':checked,'independent_high_seed_scalar_checks':24,
        'high_seed_degrees_checked':[400,599,799],'independent_coarse_values_checked':coarse,
        'coarse_error_beta':[1632,1648,1632,1664],'complete_disjoint_sweeps_checked':len(sweeps),
        'all_thirteen_correction_gains_checked':True,'W_Gaussian_or_quadric_bounds_changed':False,
        'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
        'wall_seconds':time.monotonic()-start,'sources':[r.source(x) for x in sorted(PATHS)]}


if __name__=='__main__':
    out=DATA/'dyadic_staged_pilot_independent_d123.json';assert not out.exists()
    result=build();out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='sources'}),flush=True)
    print('PASS|491_DYADIC_STAGED_PILOT_INDEPENDENT',flush=True)
