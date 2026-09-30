"""D118 final section budget: corrected CM fibre and tropical Faltings term."""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('logs',ROOT/'dembele/pari/447_cm_disk_vanishing_budget.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)

def build():
    prior=json.loads((DATA/'cm_corrected_height_budget_d118.json').read_text())['budgets']
    tropical=json.loads((DATA/'cm_tropical_faltings_d118.json').read_text())
    theta=Q(tropical['dyadic_tropical_Faltings_contribution_coefficient_log2'])
    # h_Fal >= -16 log(pi)-8 log(2)+theta log(2), versus -16 log(2*pi).
    gain=8+theta;rows=[]
    pi=b.pi_interval();logpi=(b.log(pi[0])[0],b.log(pi[1])[1])
    hFal=b.plus(b.scale(logpi,-16),b.scale(b.LOG2,theta-8))
    for old in prior['thresholds']:
        n=old['order'];pieces={k:tuple(map(Q,v)) for k,v in old['upper_bound_pieces'].items()}
        pieces['frame_vector_and_Faltings_log2']=b.scale(b.LOG2,190-15*theta)
        total=b.plus(*pieces.values());ideal=b.plus(*(v for k,v in pieces.items() if k!='disk_radius'))
        A=old['certified_anchor_lower_beta'];Nactual=old['achieved_degree16_lower_beta'];targets=[]
        for iv in (total,ideal):
            lo=17*iv[0]/b.LOG2[1]-Q(A,16);hi=17*iv[1]/b.LOG2[0]-Q(A,16)
            N=hi.__floor__()+1;assert N-1<lo<hi<N;targets.append(N)
        row=dict(old);row.update(upper_bound_expression_interval=list(map(str,total)),
            upper_bound_pieces={k:list(map(str,v)) for k,v in pieces.items()},
            degree16_sufficient_integral_jet_lower_beta=targets[0],
            optimistic_radius_one_same_bound_threshold_beta=targets[1],valuation_gap=targets[0]-Nactual)
        rows.append(row)
    result={k:v for k,v in prior.items() if k not in ('total_upper_bound_formula','thresholds')}
    result.update(thresholds=rows,Faltings_lower_bound_interval=list(map(str,hFal)),
        tropical_Faltings_coefficient_log2=str(theta),
        total_upper_bound_formula='(240+n)*H_corrected+(190-15*theta)*log(2)+120*log(pi)+log(480*L)+log(C_n)+(240+n)*log(5/3)')
    print('ARITHMETIC_HEIGHT_BUDGET|'+json.dumps({'thresholds':[r['degree16_sufficient_integral_jet_lower_beta'] for r in rows],
          'radius_one_limits':[r['optimistic_radius_one_same_bound_threshold_beta'] for r in rows]}),flush=True)
    return {'status':'pass','milestone':'D118','budgets':result,
        'improvement_over_fibre_only_threshold_expression_beta':str(17*15*gain),
        'higher_intrinsic_jets_require_previous_exact_zeros':True,
        'actual_moment_precision_increased':False,'positive_quadric_jet_exact_vanishing_proved':False,
        'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
        'sources':[b.source(p) for p in [Path(__file__),Path(b.__file__),
            DATA/'cm_corrected_height_budget_d118.json',DATA/'cm_tropical_faltings_d118.json']]}

if __name__=='__main__':
    out=DATA/'cm_arithmetic_height_budget_d118.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n');print('PASS|454_CM_ARITHMETIC_HEIGHT_BUDGET',flush=True)
