"""D138 recover the actual residue frame from the completed P=1600 bank.

Only actual harmonic jets and the refined algebraic CM values enter this
step. Candidate quadrics are tested in a separate subsequent calculation.
"""
import importlib.util
import json
from pathlib import Path
import time
import resource
import sys

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('balls',ROOT/'dembele/pari/570_dyadic_precision1600_balls.py')
f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
t=importlib.util.spec_from_file_location('provenance',ROOT/'dembele/pari/569_dyadic_complete_precision1600_bank.py')
provenance=importlib.util.module_from_spec(t);t.loader.exec_module(provenance)


def build():
    begin=time.monotonic();path=DATA/'dyadic_precision1600_bank_d138.json';packet=json.loads(path.read_text())
    etapath=DATA/'dyadic_CM_frame_beta21168_d122.json';frame=json.loads(etapath.read_text())
    assert packet['working_precision_pi']==1600 and packet['coarse_error_beta']==[3232,3248,3232,3264]
    assert packet['full_sixteen_column_bank_refined'] and frame['all_original_Hensel_branches_preserved']
    errors=packet['coarse_error_beta']
    jets=[[[f.center(cs,errors[n]) for cs in row['coarse_coefficients_beta'][n]] for n in range(4)] for row in packet['CM_values']]
    h=[];scales=[];fibres=[]
    for i,jet in enumerate(jets):
        vals=[x.v for x in jet[0] if x.known_nonzero()];assert vals
        v=min(vals);assert v==(296 if i==0 else 33)
        fibres.append(v);scale=f.BETA**v;scales.append(scale);h.append([x/scale for x in jet[0]])
    inv,pivots=f.inverse(h[1:]);q=f.multiply([h[0]],inv)[0]
    assert all(x.known_nonzero() and x.v==-35 for x in q)
    # Centers are reduced into the working ring; never attach an input's
    # larger advertised precision to digits discarded by that reduction.
    etaerror=min(f.PRECISION,frame['rational_residue_frame_error_beta'])
    eta=[[f.center(cs,etaerror) for cs in row] for row in frame['rational_residue_frame_values']]
    weighted=[[x/q[i] for x in eta[i+1]] for i in range(16)]
    change=f.multiply(inv,weighted);actual=[f.multiply(jet,change) for jet in jets]
    assert min(x.lower() for row in change for x in row)>=0
    for i in range(17):
        expected=[-x*scales[0] if i==0 else x*scales[i]/q[i-1] for x in eta[i]]
        assert all(not(x-y).known_nonzero() for x,y in zip(actual[i][0],expected))
    oldpath=DATA/'dyadic_comparison200_d115.json';old=json.loads(oldpath.read_text())
    for row,saved in zip(change,old['change_of_basis']):
        for x,y in zip(row,saved):assert not(x-f.restore(y)).known_nonzero()
    priorpath=DATA/'dyadic_residue_frame800_d125.json';prior=json.loads(priorpath.read_text())
    for row,saved in zip(change,prior['change_of_basis']):
        for x,y in zip(row,saved):assert not(x-f.restore(y)).known_nonzero()
    for jet,priorrow in zip(actual,prior['CM_values']):
        for row,saved in zip(jet,priorrow['actual_residue_frame_coarse_jets']):
            for x,y in zip(row,saved):assert not(x-f.restore(y)).known_nonzero()
    gaussian=[]
    for i,jet in enumerate(actual):
        G=jet[0][0]*jet[1][1]-jet[0][1]*jet[1][0]
        gaussian.append({'CM_index':i,**G.summary(),'lower_beta':G.lower()})
    result={'status':'pass','milestone':'D138','working_precision_pi':1600,'arithmetic_precision_beta':f.PRECISION,
        'coarse_error_beta':errors,'eta_input_error_beta':frame['rational_residue_frame_error_beta'],
        'eta_working_error_beta':etaerror,'canonical_fibre_valuations_beta':fibres,
        'evaluation_inverse_pivots':pivots,'frame_relation':[x.saved() for x in q],
        'change_of_basis':[[x.saved() for x in row] for row in change],
        'minimum_change_entry_error_beta':min(x.error for row in change for x in row),
        'CM_values':[{'CM_index':i,'actual_residue_frame_coarse_jets':[[x.saved() for x in row] for row in jet]}
                     for i,jet in enumerate(actual)],
        'leading_frame_rows_checked':17,'old_change_entries_compared':256,'P800_change_entries_compared':256,'P800_actual_jet_overlaps':1088,'Gaussian_G12':gaussian,
        'W_Gaussian_known_nonzero':gaussian[0]['valuation_beta'] is not None,
        'W_Gaussian_inverted':False,'candidate_data_used':False,'candidate_identification_proved':False,
        'wall_seconds':time.monotonic()-begin,
        'sources':[provenance.source(x) for x in [Path(__file__),Path(f.__file__),Path(provenance.__file__),path,etapath,oldpath,priorpath]]}
    print('P1600_RESIDUE_FRAME|'+json.dumps({k:result[k] for k in ['minimum_change_entry_error_beta',
        'W_Gaussian_known_nonzero','wall_seconds']}),flush=True)
    result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    assert result['peak_rss_bytes']<=2*(1<<30)
    return result


if __name__=='__main__':
    out=DATA/'dyadic_residue_frame1600_d138.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n')
    print('PHASE_METADATA|'+json.dumps(provenance.source(out)),flush=True)
    print('PASS|571_DYADIC_PRECISION1600_RESIDUE_FRAME',flush=True)
