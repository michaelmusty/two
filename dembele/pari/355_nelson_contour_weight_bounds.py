"""D94: rigorous fractional-contour and polynomial-weight cost probes.

For W(s)=(2s-1)*(1-s*(s-1)/r)^m, H=(1+W)/2 is an admissible
polynomial in Nelson's residue identity. Nonzero m changes each finite
family; its bounds must not be combined with D93's original partial sums.
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


def interval(value):
    return {"lower": str(value.lower().exact_rational()),
            "upper": str(value.upper().exact_rational()), "display": str(value)}


def ball(row):
    lo, hi = QQ(row["lower"]), QQ(row["upper"])
    value = RB((lo + hi) / 2).add_error((hi - lo) / 2)
    assert value.lower().exact_rational() <= lo <= hi <= value.upper().exact_rational()
    return value


def multiply(p, q):
    out = [QQ(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def tail_polynomial(c, k, shift, m, r):
    # Binet bounds Gamma(c+it)^16 by
    # 8^8*exp(4/(3*c))*(2+t)^24*exp(-24*t), 3/2<c<=2.
    # The seven s factors, rising factorial, and W give this polynomial.
    assert QQ(3)/2 < c <= 2
    p = [QQ(1)]
    for _ in range(31):
        p = kernel.polynomial_times(p, 2, 1)
    for j in range(k):
        p = kernel.polynomial_times(p, 2 + j, 1)
    p = kernel.polynomial_times(p, 3, 2)
    p = kernel.polynomial_times(p, 2 + shift, 1)
    # On c+it, |1-s(s-1)/r| <= 1+((2+t)*(1+t))/r.
    for _ in range(m):
        p = multiply(p, [1 + 2/r, 3/r, 1/r])
    return p


def vertical_tail(c, k, shift, m, r):
    p = tail_polynomial(c, k, shift, m, r)
    h = 16
    integral = sum(coefficient * sum(QQ(comb(j, v) * h**(j-v) * factorial(v)) / 24**(v+1)
                                    for v in range(j+1)) for j, coefficient in enumerate(p))
    value = 8**8 * (RB(QQ(4)/(3*c)) - 24*h).exp() * RB(integral)
    return value, list(map(str, p)), str(integral)


def zeta(x):
    value = kernel.dedekind_zeta(CB(x))
    assert value.imag().contains_zero() and value.real().lower() > 1
    return value.real()


def divisor_mass(s):
    assert s > 2
    x = RB(2)**(-s)
    local = (1 - 2*x*x)/((1-x)**2 * (1-2*x)**2)
    return zeta(s)**2 * zeta(s-1)**2 / zeta(2*s-1) / local


def main():
    output = DATA / "nelson_contour_weight_bounds_d94.json"
    assert not output.exists()
    R = PolynomialRing(QQ, "s")
    s = R.gen()
    contours = [QQ(3)/2 + QQ(1)/d for d in [128, 64, 32, 16, 8, 4, 2]]
    powers = [0, 1, 2, 4]
    denominator, height = 128, 16
    Z0 = (4*PI*PI)**8 / 2**62
    rows = []
    for c in contours:
        r = c*(c-1)
        totals = {(m, a, j): RB(0) for m in powers for a in [1, 3, 5] for j in [2, a+2]}
        for h in range(height * denominator):
            t = RB(QQ(2*h+1)/(2*denominator)).add_error(QQ(1)/(2*denominator))
            z = CB(c, t)
            base = abs((2*z-1) * z.gamma()**16 * z**7)
            weight = abs(1 - z*(z-1)/r)
            rising = CB(1)
            for k in range(1, 8):
                rising *= z+k-1
                if k in [3, 5, 7]:
                    a = k-2
                    for j in [2, a+2]:
                        term = base * abs(rising*(z+j))
                        for m in powers:
                            totals[m, a, j] += RB((term*weight**m).upper()) / denominator
        factor = zeta(2*c) * (1+RB(2)**c)/(1-RB(2)**(-c-1)) / PI
        mass = divisor_mass(c+QQ(1)/2)
        omitted = mass-1-64*RB(31)**(-c-QQ(1)/2)
        orbit = 1/(1-RB(QQ(2)/9)**c)
        assert omitted.lower() > 0
        for m in powers:
            W = (2*s-1)*(1-s*(s-1)/r)**m
            H = (1+W)/2
            assert W(1-s) == -W and H(0) == 0 and H(1) == 1
            constants, errors = {}, {}
            for a in [1, 3, 5]:
                constants[str(a)] = {}
                bsum = RB(0)
                for j in [2, a+2]:
                    tail, polynomial, integral = vertical_tail(c, a+2, j, m, r)
                    value = factor*(totals[m, a, j]+tail)
                    constants[str(a)][str(j)] = {"bound": interval(value), "vertical_tail": interval(tail),
                                                "tail_polynomial": polynomial, "tail_integral_before_exponential": integral}
                    bsum += RB(value.upper())
                error = Z0**(-c) * bsum * orbit * omitted
                errors[str(a)] = interval(error)
            rows.append({"contour": str(c), "weight_power": m, "weight_parameter": str(r),
                         "W_coefficients": list(map(str, W.list())), "H_coefficients": list(map(str, H.list())),
                         "divisor_mass": interval(mass), "omitted_divisor_mass": interval(omitted),
                         "whole_orbit_moment": interval(orbit), "constants": constants,
                         "all_uncomputed_norm_ideal_bounds": errors,
                         "can_use_D93_partial_sums": m == 0})
        print("CONTOUR", c, [(m, rows[-4+i]["all_uncomputed_norm_ideal_bounds"]["1"]["display"]) for i, m in enumerate(powers)], flush=True)
    best = {}
    for m in powers:
        best[str(m)] = {str(a): min((row for row in rows if row["weight_power"] == m),
                                    key=lambda row: QQ(row["all_uncomputed_norm_ideal_bounds"][str(a)]["upper"]))["contour"]
                       for a in [1, 3, 5]}
    result = {"status": "pass: rigorous contour/weight majorants; no new CM evaluation",
              "Z0": interval(Z0), "precision_bits": kernel.PRECISION, "mesh_denominator": denominator,
              "vertical_height": height, "rows": rows, "best_contours_by_weight_power": best,
              "nonzero_weight_requires_new_partial_sums": True,
              "global_test_vector_identified": False, "Shimura_derivative_computed": False,
              "sources": [kernel.source(p) for p in [Path(__file__), Path(kernel.__file__),
                          DATA/"nelson_prime31_exact_d93.json", DATA/"nelson_all_ideal_bounds_d93_exact_d93.json"]]}
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS|355_nelson_contour_weight_bounds")


if __name__ == "__main__":
    main()
