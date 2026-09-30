"""D118: subtract the proved dyadic Hodge/ramification correction."""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('logs',ROOT/'dembele/pari/447_cm_disk_vanishing_budget.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)

def build():
    prior=json.loads((DATA/'cm_uniform_disk_budget_d117.json').read_text())['budgets']
    correction=json.loads((DATA/'cm_composite_differential_d118.json').read_text())
    c=Q(correction['normalized_dyadic_finite_zero_degree_coefficient_log2'])
    hodge=Q(prior['saved_Hodge_height_upper'])
    H=b.plus((2*hodge,2*hodge),b.scale(b.LOG2,1-c));assert H[1]<Q(8,3)
    rows=[]
    for r in prior['thresholds']:
        n=r['order'];pieces={k:tuple(map(Q,v)) for k,v in r['upper_bound_pieces'].items()}
        pieces['CM_fibre_degree']=b.scale(H,240+n)
        total=b.plus(*pieces.values());ideal=b.plus(*(v for k,v in pieces.items() if k!='disk_radius'))
        anchor=r['certified_anchor_lower_beta'];actual=r['achieved_degree16_lower_beta'];targets=[]
        for expression in (total,ideal):
            lo=17*expression[0]/b.LOG2[1]-Q(anchor,16)
            hi=17*expression[1]/b.LOG2[0]-Q(anchor,16)
            N=hi.__floor__()+1;assert N-1<lo<hi<N;targets.append(N)
        # Sensitivity: remaining height improvement needed if ONLY h_Fal
        # is changed and all other inputs and measured valuations are fixed.
        finite=b.scale(b.LOG2,Q(16*actual+anchor,272))
        pi=b.pi_interval();logpi=(b.log(pi[0])[0],b.log(pi[1])[1])
        old_faltings_lower=b.scale(b.plus(b.LOG2,logpi),-16)
        needed=b.plus(old_faltings_lower,b.scale(b.plus(total,b.scale(finite,-1)),Q(1,15)))
        row=dict(r)
        row.update(upper_bound_expression_interval=list(map(str,total)),
                   upper_bound_pieces={k:list(map(str,v)) for k,v in pieces.items()},
                   degree16_sufficient_integral_jet_lower_beta=targets[0],
                   optimistic_radius_one_same_bound_threshold_beta=targets[1],
                   valuation_gap=targets[0]-actual,
                   h_Fal_lower_bound_needed_if_only_that_input_changes_interval=list(map(str,needed)),
                   h_Fal_lower_bound_needed_sufficient_integer=needed[1].__floor__()+1)
        rows.append(row)
    packet={k:v for k,v in prior.items() if k not in ('coarse_CM_fibre_height_upper_interval','thresholds','total_upper_bound_formula')}
    packet.update(coarse_CM_fibre_height_upper_interval=list(map(str,H)),
                  coarse_CM_fibre_height_upper_formula='2*h_L_upper-(35/34)*log(2)',
                  total_upper_bound_formula='(240+n)*H_corrected+310*log(2)+120*log(pi)+log(480*L)+log(C_n)+(240+n)*log(5/3)',
                  dyadic_height_correction_coefficient_log2=str(c),thresholds=rows)
    print('CORRECTED_HEIGHT_BUDGET|'+json.dumps({'thresholds':[r['degree16_sufficient_integral_jet_lower_beta'] for r in rows],
          'radius_one_limits':[r['optimistic_radius_one_same_bound_threshold_beta'] for r in rows],
          'h_Fal_only_sufficient_integers':[r['h_Fal_lower_bound_needed_sufficient_integer'] for r in rows]}),flush=True)
    return {'status':'pass','milestone':'D118','budgets':packet,
            'h_Fal_sensitivity_is_not_a_proved_lower_bound':True,
            'dyadic_combined_fibre_correction_fully_accounted_for':True,
            'higher_intrinsic_jets_require_previous_exact_zeros':True,
            'actual_moment_precision_increased':False,'positive_quadric_jet_exact_vanishing_proved':False,
            'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
            'sources':[b.source(p) for p in [Path(__file__),Path(b.__file__),
                DATA/'cm_composite_differential_d118.json',DATA/'cm_uniform_disk_budget_d117.json']]}

if __name__=='__main__':
    out=DATA/'cm_corrected_height_budget_d118.json';assert not out.exists()
    out.write_text(json.dumps(build(),indent=2)+'\n');print('PASS|452_CM_CORRECTED_HEIGHT_BUDGET',flush=True)
