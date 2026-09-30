"""D97: rigorous transfer constants for a future signed counting bound.

If |P_N(A)| <= M*(A/N)^theta for every A >= T=25600, integration
by parts bounds the omitted family by boundary_N + M*J_(N,theta).
This computes upper bounds for J, including the infinite analytic tail.
It does NOT prove the required inequality for P_N. No fitted constant
is used to replace an actual error bound.
"""
from fractions import Fraction as Q
import importlib.util
import json
from math import factorial
from pathlib import Path
import time

spec = importlib.util.spec_from_file_location("scalar", Path(__file__).with_name("360_nelson_completed_scalar_blocks.py"))
scalar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scalar)
kernel, RB, PI, DATA = scalar.kernel, scalar.RB, scalar.PI, scalar.DATA
ball, interval = scalar.ball, scalar.interval
T, U = 25600, 2**72
THETAS = [Q(1, 2), Q(2, 3), Q(3, 4), Q(7, 8)]


def box(row):
    return Q(row["lower"]), Q(row["upper"])


def polynomial_bound(coefficients):
    """Supremum of |p'-p| on [-3/8,3/8], by rational intervals."""
    total = Q(0)
    for m, row in enumerate(coefficients):
        lo, hi = box(row)
        dl, dh = box(coefficients[m+1]) if m+1 < len(coefficients) else (Q(0), Q(0))
        total += max(abs((m+1)*dl-hi), abs((m+1)*dh-lo))*Q(3, 8)**m
    return total


def far_constants():
    values = {}
    for label, shifts in [("H", [1, 2]), ("Q", [2, 3])]:
        p = list(map(Q, kernel.gamma_majorant(4, 3)))
        for shift in shifts:
            p = kernel.polynomial_times(p, 4+shift, 1)
        integral = sum(v*Q(factorial(j), 24**(j+1)) for j, v in enumerate(p))
        constant = Q(8, 7)**8*Q(544, 31)*integral/3
        values[label] = {"polynomial": list(map(str, p)), "integral": str(integral), "constant_upper": str(constant)}
    return values


def polynomial_value(coefficients, x):
    value = RB(0)
    for row in reversed(coefficients):
        value = value*x+ball(row)
    return value


def main():
    started = time.monotonic()
    output = DATA/"nelson_signed_tail_transfer_d97.json"
    assert not output.exists()
    paths = [DATA/"nelson_completed_scalar_blocks_d96.json", DATA/"nelson_signed_orbit_blocks_d97.json"]
    blocks, signed = [json.loads(p.read_text()) for p in paths]
    h = ball(blocks["log_half_width"])
    assert h.upper() < RB(3)/8
    hlow = box(blocks["log_half_width"])[0]
    Z0 = (4*PI*PI)**8/2**62
    far = far_constants()
    records = []
    totals = {(N, theta): RB(0) for N in [1, 31] for theta in THETAS}
    for b in blocks["blocks"]:
        j = b["index"]
        if int(b["A_upper"]) <= T or int(b["A_lower"]) >= U:
            continue
        lower, upper = max(T, 2**j), min(U, 2**(j+1))
        e3, e4, e5 = [kernel.quadrature_error(Z0*2**j, k, kernel.STEP_DENOMINATOR)[0] for k in [3, 4, 5]]
        analytic = {"H": 4*e3+6*e4+e5, "Q": RB(2).sqrt()*(4*e4+e5)}
        bounds = {}
        for label in ["H", "Q"]:
            row = b["kernels"][label]
            polynomial = polynomial_bound(row["finite_Taylor_coefficients"])
            remainder = (32/hlow+1)*box(row["exponential_remainder_bound"])[1]
            bound = polynomial+remainder+Q(analytic[label].upper().exact_rational())
            bounds[label] = {"polynomial_absolute_bound": str(polynomial),
                             "Taylor_derivative_and_value_remainder_upper": str(remainder),
                             "analytic_derivative_and_value_error": interval(analytic[label]),
                             "total_upper": str(bound)}
        center_low = box(b["A_center"])[0]
        terms = []
        for N in [1, 31]:
            envelope = Q(bounds["H"]["total_upper"])+N/center_low*Q(bounds["Q"]["total_upper"])
            for theta in THETAS:
                integral = RB(N)**(-theta)*(RB(lower)**(theta-1)-RB(upper)**(theta-1))/(1-theta)
                term = RB(envelope)*integral
                assert term.lower() > 0
                totals[N, theta] += term
                terms.append({"norm": N, "theta": str(theta), "radial_integral": interval(integral),
                              "derivative_envelope_upper": str(envelope), "contribution": interval(term)})
        records.append({"index": j, "lower": lower, "upper": upper, "bounds": bounds, "terms": terms})
    assert len(records) == 58 and records[0]["lower"] == T and records[-1]["upper"] == U
    point_block = blocks["blocks"][14]
    center = ball(point_block["A_center"])
    x = (RB(T)/center).log()
    assert abs(x).upper() < h.lower()
    point_values = {}
    for label in ["H", "Q"]:
        row = point_block["kernels"][label]
        error = ball(row["exponential_remainder_bound"])+ball(row["quadrature_error_bound"])
        point_values[label] = polynomial_value(row["finite_Taylor_coefficients"], x).add_error(error.upper())
    families = []
    for family in signed["families"]:
        N = family["norm"]
        f = (point_values["H"]+N/center*point_values["Q"])/T
        phase = ball(family["cutoffs"][-1]["signed_phase_sum"])
        boundary = abs(phase*f)
        transfers = []
        for theta in THETAS:
            far_H, far_Q = [RB(Q(far[k]["constant_upper"])) for k in ["H", "Q"]]
            tail = Z0**(-4)*RB(N)**(-theta)*(far_H*RB(U)**(theta-5)/(5-theta)+N*far_Q*RB(U)**(theta-6)/(6-theta))
            total = totals[N, theta]+tail
            transfers.append({"theta": str(theta), "finite_integral_upper_enclosure": interval(totals[N, theta]),
                              "far_integral_upper_enclosure": interval(tail), "J_upper_enclosure": interval(total)})
        families.append({"label": family["label"], "norm": N, "f_at_T": interval(f),
                         "signed_count_at_T": interval(phase), "boundary_absolute": interval(boundary),
                         "transfers": transfers})
        print("TRANSFER", N, "boundary", boundary, {v["theta"]: v["J_upper_enclosure"]["display"] for v in transfers}, flush=True)
    result = {"status": "pass: certified conditional tail-transfer constants; signed-count premise remains unproved",
              "T": T, "U": str(U), "theta_values": list(map(str, THETAS)), "Z0": interval(Z0),
              "derivative_identity": "f_N'(A)=(2*K3-4*K4+K5)/A^2+N*(2*K4-K5)/A^3",
              "premise": "for every A>=T, |P_N(A)|<=M*(A/N)^theta; P_N sums phases over the whole ideal family",
              "conclusion": "|tail_N(T)|<=boundary_absolute+M*J_upper",
              "far_contour": 4, "far_constants": far, "blocks": records, "families": families,
              "premise_proved": False, "finite_observed_constants_extrapolated": False,
              "actual_error_bound_improved": False, "CM_anchor_derivative_nonzero": False,
              "sources": [kernel.source(p) for p in [Path(__file__), Path(scalar.__file__), Path(kernel.__file__)]+paths]}
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS|364_nelson_signed_tail_transfer", round(time.monotonic()-started, 3), flush=True)


if __name__ == "__main__":
    main()
