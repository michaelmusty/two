"""D108 conditional dyadic moment-to-jet interface and exact controls.

No arithmetic Shimura cocycle or its moments are computed here. Controls
use an explicitly synthetic three-atom measure in the actual CM field.
The proof supplies uniform tail bounds, including ramification at 2.
"""
import hashlib
import json
from math import comb
from pathlib import Path
from sage.all import QQ, NumberField, PolynomialRing, PowerSeriesRing

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    output = DATA/"dyadic_poisson_jet_interface_d108.json"
    assert not output.exists(), "Preserve completed artifacts."
    ring = PolynomialRing(QQ, "x"); x = ring.gen()
    Fpoly = x**8-8*x**6+20*x**4-16*x**2+2
    Mpoly = Fpoly(-x*x-2)
    assert Mpoly.degree() == 16 and Mpoly[0] % 4 == 2
    assert all(c % 2 == 0 for c in list(Mpoly)[:-1])
    assert Fpoly[0] % 4 == 2 and all(c % 2 == 0 for c in list(Fpoly)[:-1])
    CM = NumberField(Mpoly, "beta"); beta = CM.gen()
    pi = -beta*beta-2
    assert Fpoly(pi) == 0 and beta*beta == -2-pi
    def val(y):
        y = CM(y)
        if not y:
            return None
        # Eisenstein power basis: summands have distinct valuations mod 16.
        return min(QQ(16*c.valuation(2)+i)/2 for i,c in enumerate(y.list()) if c)
    def at_least(y, bound):
        v = val(y)
        return v is None or v >= bound
    assert val(2) == 8 and val(pi) == 1 and val(beta) == QQ(1)/2
    assert val(beta-1) == 0
    # All three charts are represented, and the total synthetic mass is zero.
    atoms = [(pi, CM(1)), (1+pi, CM(-2)), (1/pi, CM(1))]
    series = PowerSeriesRing(CM, "w", default_prec=9); w = series.gen()
    z = beta*(1+w)/(1-w)
    phi = sum(weight/(z-t) for t,weight in atoms)*2*beta/(1-w)**2
    exact_f = [sum((-1)**k*weight/(beta-t)**(k+1) for t,weight in atoms) for k in range(6)]
    exact_coarse = [phi[2*j+1]/2 for j in range(3)]
    # The odd part of phi(w)dw is the invariant differential; u=w^2.
    assert [sum(beta*(2*beta)**k*comb(2*j+2,k+1)*exact_f[k]
                for k in range(2*j+2)) for j in range(3)] == exact_coarse
    def truncated(k, J, A, B, C, wrong_infinity=False):
        value = (-1)**k*beta**(-k-1)*sum(comb(k+r,r)*(pi/beta)**r*A[r] for r in range(J+1))
        value += (-1)**k*(beta-1)**(-k-1)*sum(comb(k+r,r)*(pi/(beta-1))**r*B[r] for r in range(J+1))
        infinite = pi**(k+1)*sum(comb(k+r,r)*(beta*pi)**r*C[k+r+1] for r in range(J-k))
        return value+infinite if wrong_infinity else value-infinite
    rows = []
    for J,d,P in [(7,0,4),(15,0,8),(15,3,7),(31,0,16)]:
        scalar = beta**(-2*d)
        A = [scalar]*(J+1); B = [-2*scalar]*(J+1); C = [scalar]*(J+1)
        approx = [truncated(k,J,A,B,C) for k in range(6)]
        perturbed = [truncated(k,J,[v+beta**(2*P) for v in A],B,C) for k in range(6)]
        errors, noisy_errors = [], []
        for k in range(6):
            bound = QQ(J-k)/2-d
            noisy_bound = min(bound, P-QQ(k+1)/2)
            error = scalar*exact_f[k]-approx[k]
            noisy_error = scalar*exact_f[k]-perturbed[k]
            assert at_least(error,bound) and at_least(noisy_error,noisy_bound)
            errors.append(str(val(error))); noisy_errors.append(str(val(noisy_error)))
        coarse = [sum(beta*(2*beta)**k*comb(2*j+2,k+1)*perturbed[k]
                      for k in range(2*j+2)) for j in range(3)]
        target_bound = min(QQ(J+1)/2-d,P)
        coarse_errors = [scalar*exact_coarse[j]-coarse[j] for j in range(3)]
        assert all(at_least(err,target_bound) for err in coarse_errors)
        wrong = truncated(0,J,A,B,C,wrong_infinity=True)
        assert not at_least(scalar*exact_f[0]-wrong, QQ(J)/2-d)
        rows.append({"highest_moment_index": J, "measure_denominator_exponent": d,
                     "input_moment_absolute_precision": P,
                     "Taylor_tail_valuations": errors,
                     "Taylor_with_moment_error_valuations": noisy_errors,
                     "coarse_coefficient_error_valuations": list(map(lambda e:str(val(e)),coarse_errors)),
                     "proved_coarse_lower_bound": str(target_bound),
                     "wrong_infinity_sign_rejected": True})
    matrix = [[str(beta*(2*beta)**k*comb(2*j+2,k+1)) if k<=2*j+1 else "0"
               for k in range(6)] for j in range(3)]
    result = {"status": "pass", "milestone": "D108",
              "F_polynomial_ascending": list(map(str,Fpoly.list())),
              "CM_polynomial_ascending": list(map(str,Mpoly.list())),
              "both_polynomials_Eisenstein_at_2": True,
              "valuation_normalization": "v(pi)=1, v(2)=8, v(beta)=1/2",
              "three_boundary_charts": ["t=pi*x", "t=1+pi*x", "t=1/(pi*x), x=0 means infinity"],
              "measure_bound_hypothesis": "v(mu(B))>=-d for every compact open ball",
              "Taylor_error_lower_bound": "min((J-k)/2-d,P-(k+1)/2)",
              "coarse_parameter": "w=(z-beta)/(z+beta); u=w^2",
              "coarse_formula": "g_j=beta*sum_(k=0)^(2j+1) (2*beta)^k*binomial(2j+2,k+1)*f_k",
              "coarse_error_lower_bound": "min((J+1)/2-d,P)",
              "coarse_orders_checked": [0,1,2], "ordinary_Taylor_orders_checked": list(range(6)),
              "minimum_highest_moment_index_for_formula": 5,
              "coarse_transformation_matrix": matrix, "synthetic_measure_controls": rows,
              "actual_CM_coordinate_global_identification_proved": False,
              "actual_Shimura_cocycle_computed": False, "actual_moments_computed": False,
              "actual_Shimura_jet_evaluated": False,
              "scope": "Conditional certified local evaluator once actual bounded harmonic-measure moments and a matched dyadic CM embedding are supplied. Controls are synthetic, not Shimura data.",
              "sources": [source(Path(__file__)), source(DATA/"cm_orbit.json")]}
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"pass","synthetic_controls":len(rows),
                      "coarse_error_bound":result["coarse_error_lower_bound"],
                      "actual_Shimura_jet_evaluated":False}),flush=True)
    print("PASS|D108_DYADIC_POISSON_INTERFACE",flush=True)


if __name__ == "__main__":
    main()
