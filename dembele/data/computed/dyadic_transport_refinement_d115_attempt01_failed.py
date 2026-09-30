"""D115: refine the existing splitting root and all saved transport centers."""
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('transport',ROOT/'dembele/pari/411_dyadic_moment_transports.py')
t=importlib.util.module_from_spec(s);s.loader.exec_module(t)

def main():
    previous=DATA/'dyadic_moment_transports_d113.json';p=json.loads(previous.read_text())
    split=t.rt.Splitting();oldx=split.x;old_error=split.error;split.refine();ex=t.Exact(split)
    assert t.r.val(t.r.sub(split.x,oldx))>=old_error
    def refine(row):
        X=(t.r.fm(row['matrix_constant']),t.r.fm(row['matrix_slope']))
        out=ex.normalize(X,row['determinant_valuation']);assert out is not None
        assert out['normalized_error_pi']>row['normalized_error_pi']
        assert out['constant_residue']==row['constant_residue']
        assert out['denominator_slope_valuation']==row['denominator_slope_valuation']
        assert t.r.mval(t.r.madd(t.r.fm(out['normalized_center']),t.r.mscale(t.r.fm(row['normalized_center']),t.r.neg(t.O))))>=row['normalized_error_pi']
        row.update(out)
    for row in p['transitions']:
        for child in row['children']:refine(child)
    for row in p['CM_charts']:refine(row)
    p['milestone']='D115';p['minimum_transition_error_pi']=min(c['normalized_error_pi'] for row in p['transitions'] for c in row['children'])
    p['minimum_CM_chart_error_pi']=min(c['normalized_error_pi'] for c in p['CM_charts'])
    p['pilot_maximum_working_precision_pi']=200
    p['root_refinement']={'old_error_pi':old_error,'new_error_pi':split.error,'old_center':t.a.fs(oldx),'new_center':t.a.fs(split.x),
                          'same_Hensel_branch_certified':True,'new_residual_valuation':t.r.val(t.r.add(t.r.mul(split.x,split.x),split.y2plus1))}
    p['sources']=[t.source(x) for x in [Path(__file__),Path(t.__file__),Path(t.rt.__file__),previous,DATA/'definite_dyadic_certificate_d109.json']]
    out=DATA/'dyadic_moment_transports_refined_d115.json';assert not out.exists()
    out.write_text(json.dumps(p,indent=2)+'\n')
    print(json.dumps({'root_error':split.error,'minimum_transition_error':p['minimum_transition_error_pi'],'minimum_CM_error':p['minimum_CM_chart_error_pi']}),flush=True)
    print('PASS|425_DYADIC_TRANSPORT_REFINEMENT',flush=True)

if __name__=='__main__':main()
