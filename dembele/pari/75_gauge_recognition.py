"""Bounded, explicitly tentative recognition tests for normalized CM jets.

Extra mpmath working precision is only for exact field embeddings; input
jet accuracy is limited by two independent numerical truncations.
"""
from fractions import Fraction
import json
from pathlib import Path
import mpmath as mp

DATA=Path(__file__).resolve().parents[1]/'data/computed'


def main():
    mp.mp.dps=50
    source=json.loads((DATA/'canonical_gauge.json').read_text())
    b=2*mp.cos(7*mp.pi/16)
    field_vector=[b**i for i in range(8)]
    results=[]
    for entry in source['nontrivial_normalized_jet_samples']:
        y=mp.mpf(str(entry['value']))
        discrepancy=mp.mpf(str(entry['truncation_difference']))
        # This tolerance is empirical, not a certified error enclosure.
        tolerance=max(mp.mpf('1e-11'),10*discrepancy)
        rational=Fraction(entry['value']).limit_denominator(1000)
        rational_error=abs(y-mp.mpf(rational.numerator)/rational.denominator)
        relation=mp.pslq(mp.matrix(field_vector+[y]),tol=tolerance,
                         maxcoeff=4,maxsteps=2000)
        candidate=None
        if relation is not None and relation[-1]!=0:
            value=-sum(relation[i]*field_vector[i] for i in range(8))/relation[-1]
            candidate={'relation':[int(v) for v in relation],
                       'absolute_residual':float(abs(y-value)),
                       'status':'tentative only; requires higher precision and exact validation'}
        results.append({**entry,'empirical_tolerance':float(tolerance),
                        'nearest_rational_denominator_at_most_1000':str(rational),
                        'rational_absolute_residual':float(rational_error),
                        'rational_within_empirical_tolerance':bool(rational_error<tolerance),
                        'field_height_at_most_4_candidate':candidate})
    report={'status':'recognition pilot only; no exact coefficient or number-field model certified',
            'field_hypothesis':'Q(2 cos(7 pi/16)); containment is not established by this search',
            'rational_denominator_bound':1000,'field_relation_height_bound':4,
            'results':results}
    text=json.dumps(report,indent=2)
    (DATA/'gauge_recognition.json').write_text(text+'\n')
    (DATA/'gauge_recognition.out').write_text(text+'\n')
    print(text)


if __name__=='__main__':
    main()
