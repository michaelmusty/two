"""D125 assemble sixteen independently verified columns and their CM jets."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'


def source(path):
    path=Path(path).resolve();h=hashlib.sha256()
    with path.open('rb') as f:
        while buf:=f.read(1<<20):h.update(buf)
    return {'path':str(path),'sha256':h.hexdigest()}


def build():
    paths=[Path(__file__)];columns=[];packets=[];verified=set()
    for column in range(16):
        state=DATA/('dyadic_staged_P800_col00_verified_d123.json' if column==0 else
                    f'dyadic_weighted_P800_col{column:02d}_verified_d125.json')
        cm=DATA/('dyadic_staged_CM_P800_col00_d123.json' if column==0 else
                 f'dyadic_direct_CM_P800_col{column:02d}_d125.json')
        a=json.loads(state.read_text());c=json.loads(cm.read_text())
        assert a['status']==c['status']=='pass' and a['harmonic_basis_column']==c['harmonic_basis_column']==column
        assert a['working_precision_pi']==c['working_precision_pi']==800
        assert a['certificate']['original_full_residual_zero'] and a['residual_lower_bound_pi']==800
        assert c['coarse_error_beta']==[1632,1648,1632,1664] and len(c['CM_values'])==17
        if column:assert a['certificate']['full_residual_uses_different_polynomial_backend_from_lift']
        paths += [state,cm]
        for row in a['checkpoint_files']+c['checkpoint_files']+c['sources']:
            key=(row['path'],row['sha256'])
            if key not in verified:assert source(row['path'])==row;verified.add(key)
            paths.append(Path(row['path']))
        columns.append({'harmonic_basis_column':column,'verified_state_metadata':source(state),
            'CM_metadata':source(cm),'state_binary':a['checkpoint_files'][0],
            'original_full_residual_zero':True,'working_precision_pi':800})
        packets.append(c)
    values=[]
    for ci in range(17):
        values.append({'CM_index':ci,'coarse_coefficients_beta':[
            [packets[column]['CM_values'][ci]['coarse_coefficients_beta'][order] for column in range(16)]
            for order in range(4)],'certified_valuations_beta':[
            [packets[column]['CM_values'][ci]['certified_valuations_beta'][order] for column in range(16)]
            for order in range(4)]})
    result={'status':'pass','milestone':'D125','working_precision_pi':800,'harmonic_basis_columns':16,
        'low_state_cutoff':799,'CM_cutoff':1599,'direct_CM_columns':list(range(1,16)),
        'reused_column_zero_from_D123':True,
        'coefficient_modulus_bits':100,'binary_coefficient_width_bytes':13,'state_columns':columns,
        'coarse_orders':[0,1,2,3],'coarse_error_beta':[1632,1648,1632,1664],
        'arithmetic_precision_beta':1664,'CM_values':values,
        'complete_original_residual_scalar_checks':174*800*16*8,'CM_moment_scalar_coefficients':17*1600*16*8,
        'old_coarse_values_checked':17*4*16,'full_sixteen_column_bank_refined':True,
        'candidate_identification_proved':False,'sources':[source(x) for x in sorted(set(paths))]}
    print('COMPLETE_P800_BANK|16 columns; 17817600 original state coefficients; 1088 coarse values',flush=True)
    return result


if __name__=='__main__':
    out=DATA/'dyadic_precision800_d125.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n');print('PASS|507_DYADIC_COMPLETE_PRECISION800_BANK',flush=True)
