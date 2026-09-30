"""D115 exact local product-formula thresholds for the D106 comparison."""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'dembele/data/computed'
s=importlib.util.spec_from_file_location('review',ROOT/'dembele/pari/416_dyadic_coarse_review.py')
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)

def main():
    N=64;x=Q(1,3)
    lo=2*sum(x**(2*k+1)/Q(2*k+1) for k in range(N))
    hi=lo+2*x**(2*N+1)/(Q(2*N+1)*(1-x*x))
    rows=[]
    for n,B in enumerate([Q(111817,10),Q(334657,10),Q(557517,10)],1):
        row={'order':n,'difference_height_upper':str(B)}
        for name,multiplier in [('rational_anchor_only',272),('degree16_place_only',17),('both_places_uniform_beta_error',16)]:
            lower=multiplier*B/hi;upper=multiplier*B/lo
            assert lower.numerator//lower.denominator==upper.numerator//upper.denominator
            bound=upper.numerator//upper.denominator+1
            assert bound*lo>multiplier*B
            row[name]={'sufficient_beta_error':bound,'sufficient_integer_pi_error':(bound+1)//2}
        rows.append(row)
    result={'status':'pass','milestone':'D115','field_degree':17,'dyadic_local_degrees':[1,16],
      'normalizations':{'v_beta_2':16,'v_pi_2':8},'log2_lower':str(lo),'log2_upper':str(hi),
      'thresholds':rows,'thresholds_are_sufficient_not_necessary':True,
      'finite_precision_matching_below_threshold_proves_equality':False,
      'sources':[r.source(p) for p in [Path(__file__),DATA/'cm_ratio_jet_review_d106.json',
                     DATA/'dyadic_cm_matching_review_d112.json']]}
    out=DATA/'dyadic_exactness_budget_d115.json';assert not out.exists()
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(rows,indent=2),flush=True)
    print('PASS|423_DYADIC_EXACTNESS',flush=True)

if __name__=='__main__':main()
