"""D117: final uniform CM disk and the scope of radius-only improvements."""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('budget',ROOT/'dembele/pari/447_cm_disk_vanishing_budget.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)

def build():
    projection=json.loads((DATA/'cm_projection_norm_gap_d117.json').read_text())
    original=json.loads((DATA/'cm_disk_vanishing_budget_d117.json').read_text())['budgets']
    # The exhaustive ball excludes every squared outlier in (4,64],
    # so equality in the following radius test is safe for open disks.
    assert projection['squared_absolute_value_search_upper']==64
    assert all(Q(x['squared_absolute_value_interval'][0])>64 for x in projection['eligible_single_outlier_elements'])
    rho2=Q(3,5);required=4*(1+rho2)**2/(1-rho2)**2
    assert required==64
    logrho=b.scale(b.log(1/rho2),Q(1,2));rows=[]
    for prior in original['thresholds']:
        n=prior['order'];pieces={k:tuple(map(Q,v)) for k,v in prior['upper_bound_pieces'].items()}
        pieces['disk_radius']=b.scale(logrho,480+2*n)
        total=b.plus(*pieces.values());optimistic=b.plus(*(v for k,v in pieces.items() if k!='disk_radius'))
        anchor=prior['certified_anchor_lower_beta'];achieved=prior['achieved_degree16_lower_beta']
        thresholds=[]
        for expression in (total,optimistic):
            lo=17*expression[0]/b.LOG2[1]-Q(anchor,16)
            hi=17*expression[1]/b.LOG2[0]-Q(anchor,16)
            N=hi.__floor__()+1;assert N-1<lo<hi<N;thresholds.append(N)
        row=dict(prior)
        row.update(upper_bound_expression_interval=list(map(str,total)),
                   upper_bound_pieces={k:list(map(str,v)) for k,v in pieces.items()},
                   degree16_sufficient_integral_jet_lower_beta=thresholds[0],
                   optimistic_radius_one_same_bound_threshold_beta=thresholds[1],
                   valuation_gap=thresholds[0]-achieved)
        rows.append(row)
    # This is a storage count for the present dense state representation,
    # not an impossibility bound on streaming or a new algorithm.
    storage=[]
    for P in (200,1000,10000,20000):
        entries=174*(3*P-1)*16
        storage.append({'working_pi_precision':P,'state_field_elements':entries,
                        'packed_state_bytes_at_P_bits_per_element':(entries*P+7)//8})
    assert storage[0]['state_field_elements']==1667616
    budgets={k:v for k,v in original.items() if k not in ('disk_radius','required_trace_for_disk','thresholds')}
    budgets.update(disk_radius_squared=str(rho2),strict_moving_projection_norm_lower=64,
                   required_projection_norm_for_open_disks=str(required),thresholds=rows)
    print('UNIFORM_DISK_BUDGET|'+json.dumps({'rho_squared':str(rho2),
          'thresholds':[r['degree16_sufficient_integral_jet_lower_beta'] for r in rows],
          'radius_one_limits':[r['optimistic_radius_one_same_bound_threshold_beta'] for r in rows]}),flush=True)
    return {'status':'pass','milestone':'D117','budgets':budgets,'dense_state_storage_examples':storage,
            'storage_examples_do_not_predict_precision_or_bound_other_algorithms':True,
            'actual_precision_increased':False,'positive_quadric_jet_exact_vanishing_proved':False,
            'candidate_identification_proved':False,'target_field_polynomial_constructed':False,
            'sources':[b.source(p) for p in [Path(__file__),Path(b.__file__),
                DATA/'cm_projection_norm_gap_d117.json',DATA/'cm_disk_vanishing_budget_d117.json',
                DATA/'cm_quadric_compound_bound_d116.json',DATA/'dyadic_precision200_d115.json']]}

if __name__=='__main__':
    result=build();out=DATA/'cm_uniform_disk_budget_d117.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print('PASS|449_CM_UNIFORM_DISK_BUDGET',flush=True)
