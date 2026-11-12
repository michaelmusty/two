"""D138 assemble the reviewed sixteen-column bank at common precision P1600.

Higher-precision column zero is reduced explicitly. Weighted state
certificates retain their actual scope; no uniform state binary is invented.
"""
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
PATHS={Path(__file__)};CACHE={};P=1600;ERRORS=[3232,3248,3232,3264];BETA=3264

def source(path):
    path=Path(path).resolve();PATHS.add(path)
    if path not in CACHE:
        h=hashlib.sha256()
        with path.open('rb') as f:
            while raw:=f.read(1<<20):h.update(raw)
        CACHE[path]={'path':str(path),'sha256':h.hexdigest()}
    return CACHE[path]

def read(stem):
    p=DATA/(stem+'.json');PATHS.add(p);v=json.loads(p.read_text());assert v['status']=='pass',stem;return v

def build():
    start=time.monotonic();admission=read('dyadic_checkpoint_admission_r2_d137')
    assert admission['P1600_checkpoint_admitted']
    prior=source(DATA/'dyadic_checkpoint_admission_r2_d137.json')
    known={r['path']:r['sha256'] for r in admission['sources']}
    summary=read('dyadic_checkpoint_columns_completed_r2_d137')
    assert summary['all_fourteen_new_columns_independently_reviewed'] and summary['prior_admission']==prior
    assert len(summary['columns'])==14 and summary['higher_precision_bank_not_launched']
    reviewed=[]
    for col,ref in zip(range(2,16),summary['columns']):
        assert source(ref['path'])==ref;done=read(Path(ref['path']).stem)
        assert done['column']==col and done['prior_admission']==prior
        rev=done['fixed_review'];assert source(rev['path'])==rev;r=read(Path(rev['path']).stem)
        assert r['independent_finite_review_complete'] and r['incremental_provenance'] and r['prior_fixed_review']==prior
        assert r['working_precision_pi']==P and r['harmonic_basis_column']==col and r['failed_bounded_input_jobs']==0
        for item in r['sources']:
            if item['path'] in known:assert known[item['path']]==item['sha256']
            known[item['path']]=item['sha256']
        reviewed.append(rev)
    columns=[];packets=[];old=read('dyadic_precision800_d125');overlaps=0
    # Independent quotient arithmetic is used only for the complete old
    # coarse overlaps. The assembly itself is an exact byte/integer map.
    import importlib.util
    spec=importlib.util.spec_from_file_location('quotient',ROOT/'dembele/pari/486_dyadic_precision400_independent.py')
    q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q);source(q.__file__)
    ring=q.Quotient(q.MP,BETA);mod=1<<(BETA//16)
    for col in range(16):
        state_stem='dyadic_staged_P6400_col00_d133_seal' if col==0 else 'dyadic_rolling_P1600_col01_verified_d127' if col==1 else f'dyadic_staged_P1600_col{col:02d}_r2_d137_seal'
        cm_stem='dyadic_CM_P6400_col00_d136' if col==0 else 'dyadic_rolling_CM_P1600_col01_d127' if col==1 else f'dyadic_CM_P1600_col{col:02d}_r2_d137'
        state=read(state_stem);cm=read(cm_stem);sp=source(DATA/(state_stem+'.json'));cp=source(DATA/(cm_stem+'.json'))
        for ref in (sp,cp):assert known[ref['path']]==ref['sha256']
        inputP=6400 if col==0 else 1600
        assert state['working_precision_pi']==cm['working_precision_pi']==inputP
        assert state['harmonic_basis_column']==cm['harmonic_basis_column']==col
        weighted=state.get('weighted_input',False)
        assert state['certificate']['original_weighted_fixed_point'] if weighted else state['certificate']['original_full_residual_zero']
        assert cm['verified_state_metadata']==sp
        assert cm['coarse_error_beta']==[2*inputP+g for g in (32,48,32,64)]
        binary=state['state_file'];assert source(binary['path'])==binary and known[binary['path']]==binary['sha256']
        for ref in cm['checkpoint_files']:
            assert source(ref['path'])==ref and known[ref['path']]==ref['sha256']
        values=[]
        for ci in range(17):
            coefficients=[]
            for order in range(4):
                row=[x%mod for x in cm['CM_values'][ci]['coarse_coefficients_beta'][order]]
                assert len(row)==16
                before=old['CM_values'][ci]['coarse_coefficients_beta'][order][col]
                assert ring.value(ring.sub(tuple(row),ring.norm(before)))>=old['coarse_error_beta'][order]
                overlaps+=1;coefficients.append(row)
            values.append(coefficients)
        packets.append(values)
        columns.append({'harmonic_basis_column':col,'verified_state_metadata':sp,'CM_metadata':cp,
                        'state_binary':binary,'source_precision_pi':inputP,'working_precision_pi':P,
                        'state_equation_certificate_kind':'original_weighted_fixed_point' if weighted else 'original_full_residual_zero',
                        'weighted_state_representation':weighted,'CM_centers_reduced_to_beta_precision':BETA})
    values=[{'CM_index':ci,'coarse_coefficients_beta':[[packets[col][ci][order] for col in range(16)] for order in range(4)]} for ci in range(17)]
    assert overlaps==1088
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);assert peak<=2*(1<<30)
    result={'status':'pass','milestone':'D138','working_precision_pi':P,'harmonic_basis_columns':16,
            'state_columns':columns,'coarse_orders':[0,1,2,3],'coarse_error_beta':ERRORS,
            'arithmetic_precision_beta':BETA,'CM_values':values,'full_sixteen_column_bank_refined':True,
            'common_precision_original_equation_scalar_coverage':174*P*16*8,
            'equation_scope':'Authenticated original weighted equations for columns 0 and 2-15; inherited uniform full residual for column 1; independent original-operator audits are samples.',
            'CM_moment_scalar_coefficients':17*2*P*16*8,'old_coarse_values_checked':overlaps,
            'prior_admission':prior,'column_review_roots':reviewed,'higher_precision_column_zero_reduced_explicitly':True,
            'new_state_or_CM_binary_written':False,'candidate_identification_proved':False,'field_polynomial_constructed':False,
            'wall_seconds':time.monotonic()-start,'peak_rss_bytes':peak,'sources':[source(p) for p in sorted(PATHS)]}
    print('COMMON_P1600_BANK|16 reviewed columns; 1088 complete old coarse overlaps',flush=True)
    return result

if __name__=='__main__':
    out=DATA/'dyadic_precision1600_bank_d138.json';assert not out.exists()
    with out.open('x') as f:f.write(json.dumps(build(),indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(source(out)),flush=True)
    print('PASS|569_DYADIC_COMPLETE_PRECISION1600_BANK',flush=True)
