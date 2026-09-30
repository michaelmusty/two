"""D98: rigorous norm-ideal bound from the weight-four spectral transform.

The analytic proof is in nelson-spectral-ideal-d98.md. This evaluates its
explicit majorant, without assuming a signed lattice-counting estimate.
All interval endpoints use exact MPFR dyadics (the D93 correction).
"""
import importlib.util
import json
from math import comb, factorial
from pathlib import Path
from sage.all import QQ, PolynomialRing

spec = importlib.util.spec_from_file_location("kernel", Path(__file__).with_name("333_nelson_interval_sum.py"))
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)
RB, CB, PI, DATA = kernel.RB, kernel.CB, kernel.PI, kernel.DATA
DELTA = QQ(7)/64
PACKING = QQ(1795)/1792


def interval(value):
    return {"lower": str(value.lower().exact_rational()),
            "upper": str(value.upper().exact_rational()), "display": str(value)}


def ball(row):
    lo, hi = QQ(row["lower"]), QQ(row["upper"])
    value = RB((lo+hi)/2).add_error((hi-lo)/2)
    assert value.lower().exact_rational() <= lo <= hi <= value.upper().exact_rational()
    return value


def zeta(c):
    value = kernel.dedekind_zeta(CB(c))
    assert value.imag().contains_zero() and value.real().lower() > 1
    return value.real()


def tail(c, height):
    # Binet, 1<c<=2: |Gamma(c+it)|^14 <=
    # 8^7*exp(7/(6*c))*(2+t)^21*exp(-21*t).
    assert 1 < c <= 2
    polynomial = [QQ(1)]
    for _ in range(28):
        polynomial = kernel.polynomial_times(polynomial, 2, 1)
    polynomial = kernel.polynomial_times(polynomial, 3, 2)
    integral = sum(a*sum(QQ(comb(j, v)*height**(j-v)*factorial(v))/21**(v+1)
                         for v in range(j+1)) for j, a in enumerate(polynomial))
    value = 8**7*(RB(QQ(7)/(6*c))-21*height).exp()*RB(integral)
    return value, list(map(str, polynomial)), str(integral)


def algebra_checks():
    ring = PolynomialRing(QQ, names=("s", "mu"))
    s, mu = ring.gens()
    lam = mu*(1-mu)
    # Divide h_(s+2) by h_(s+1) using the Gamma recurrence.
    assert -(s+2)*(s-1)+(s+1-mu)*(s+mu) == lam+2
    # Discrete-series normalization: mu=2 is killed; mu=1 survives.
    one = PolynomialRing(QQ, "p").fraction_field()
    p = one.gen()
    d2 = -2/p+3/(p+1)
    d4 = 1/(p+1)
    assert d2 == (p-2)/(p*(p+1))
    q = PolynomialRing(QQ, "x")
    x = q.gen()
    # The first 17 Euler coefficients, including central contents.
    coeff = sum((e+1)**2*x**e for e in range(17))
    assert (coeff*(1-x)**3-(1+x)) % x**17 == 0
    return {"radial_transform": "4*pi*Gamma(p-mu)*Gamma(p+mu-1)/(Gamma(p+2)*Gamma(p-2))",
            "Mellin_transform_multiplier": "lambda+2", "lambda": "mu*(1-mu)",
            "D2_transform_over_4pi": str(d2), "D4_transform_over_4pi": str(d4),
            "D4_annihilated": True, "Euler_coefficients_checked": 17,
            "odd_squared_divisor_mass": "zeta_F(w)^4/zeta_F(2*w)*(1-2^(-w))^3/(1+2^(-w))"}


def main():
    output = DATA/"nelson_spectral_ideal_bound_d98.json"
    assert not output.exists()
    algebra = algebra_checks()
    contours = list(map(QQ, ["73/64", "75/64", "5/4", "21/16", "11/8", "23/16", "3/2", "13/8", "7/4", "2"]))
    denominator, height = 128, 16
    Z0 = (4*PI*PI)**8/2**62
    rows = []
    for c in contours:
        assert c > 1+DELTA
        cells, finite = [], QQ(0)
        for j in range(height*denominator):
            t = RB(QQ(2*j+1)/(2*denominator)).add_error(QQ(1)/(2*denominator))
            s = CB(c, t)
            upper = abs((2*s-1)*s.gamma()**14*s**7).upper().exact_rational()
            cells.append(str(upper))
            finite += upper/denominator
        vertical, polynomial, integral = tail(c, height)
        zet = zeta(2*c)
        cusp = (1+RB(2)**c)/(1-RB(2)**(-c-1))
        gamma = RB(c+4).gamma()*RB(c).gamma()
        constant = gamma*zet*cusp*(RB(finite)+vertical)/PI
        w = c-DELTA
        x = RB(2)**(-w)
        mass = zeta(w)**4/zeta(2*w)*(1-x)**3/(1+x)
        removed_prime = 4*RB(31)**(-w)
        omitted = mass-1-removed_prime
        assert omitted.lower() > 0
        scale = Z0**(-c)
        bound = PACKING*constant*scale*omitted
        rows.append({"contour": str(c), "norm_exponent": str(w),
                     "rectangle_upper_bounds": cells, "finite_integral_upper": str(finite),
                     "vertical_tail": interval(vertical), "tail_polynomial": polynomial,
                     "tail_integral_before_exponential": integral,
                     "zeta_2c": interval(zet), "cusp_factor": interval(cusp),
                     "gamma_comparison_factor": interval(gamma), "B_c": interval(constant),
                     "Z0_minus_c": interval(scale), "odd_squared_divisor_mass": interval(mass),
                     "removed_prime31_mass": interval(removed_prime), "omitted_mass": interval(omitted),
                     "uncomputed_ideal_S11_bound": interval(bound)})
        print("SPECTRAL_CONTOUR", c, "MASS", mass, "BOUND", bound, flush=True)
    best = min(rows, key=lambda row: QQ(row["uncomputed_ideal_S11_bound"]["upper"]))
    prior_path = DATA/"nelson_completed_majorant_d96.json"
    prime_path = DATA/"nelson_prime31_sum_d93_exact_d93.json"
    prior, prime = [json.loads(p.read_text()) for p in [prior_path, prime_path]]
    selected = prime["weighted_first_quartic_orbit"][prime["selected_root_index"]]["unit_plus_prime_families"]["1"]
    best_upper = QQ(best["uncomputed_ideal_S11_bound"]["upper"])
    two_family = ball(selected["absolute_error_bound"])
    total = RB(best_upper)+two_family
    partial = ball(selected["partial_sum"]["real"])
    enclosure = partial.add_error(total.upper())
    result = {"status": "pass: explicit spectral ideal bound; see proof and CM-anchor enclosure",
              "precision_bits": kernel.PRECISION, "mesh_denominator": denominator, "height": height,
              "Z0": interval(Z0), "pi": interval(PI), "finite_Hecke_exponent": str(DELTA),
              "positive_pretrace_bound": str(PACKING), "algebra": algebra, "rows": rows,
              "best_contour": best["contour"], "certified_omitted_S11_error_upper": str(best_upper),
              "two_saved_family_error": interval(two_family), "full_S11_error": interval(total),
              "selected_S11_partial_sum": interval(partial), "full_S11_enclosure": interval(enclosure),
              "improvement_over_D96": interval(RB(QQ(prior["certified_omitted_S11_error_upper"]))/best_upper),
              "CM_anchor_derivative_nonzero": not enclosure.contains_zero(),
              "global_kernel_identified_up_to_positive_scalar": True,
              "signed_infinite_counting_estimate_assumed": False,
              "new_quaternion_enumeration": False, "new_Hecke_data": False,
              "enumeration_expansion_justified": False,
              "sources": [kernel.source(p) for p in [Path(__file__), Path(kernel.__file__),
                          prior_path, prime_path, DATA/"nelson_signed_orbit_d97.json"]]}
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("BEST", best["contour"], "IMPROVEMENT", result["improvement_over_D96"]["display"], flush=True)
    print("PASS|368_nelson_spectral_ideal_bound")


if __name__ == "__main__":
    main()
