"""D96: Taylor enclosures of the completed S11 scalar kernels.

The finite trapezoidal rule is expanded in log(A), before taking any
absolute values. A complex exponential remainder and the D91 analytic
quadrature error make each whole dyadic block rigorous. No quaternion
or Hecke enumeration is performed here.
"""
import importlib.util
import json
from math import factorial
from pathlib import Path
import time
from sage.all import QQ

spec = importlib.util.spec_from_file_location("kernel", Path(__file__).with_name("333_nelson_interval_sum.py"))
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)
RB, CB, PI, DATA = kernel.RB, kernel.CB, kernel.PI, kernel.DATA
ORDER = 32
BLOCKS = 96


def interval(value):
    return {"lower": str(value.lower().exact_rational()),
            "upper": str(value.upper().exact_rational()), "display": str(value)}


def ball(row):
    lo, hi = QQ(row["lower"]), QQ(row["upper"])
    value = RB((lo+hi)/2).add_error((hi-lo)/2)
    assert value.lower().exact_rational() <= lo <= hi <= value.upper().exact_rational()
    return value


def main():
    output = DATA / "nelson_completed_scalar_blocks_d96.json"
    assert not output.exists()
    started = time.monotonic()
    prior_path = DATA / "nelson_interval_sum_d91_exact_d93.json"
    prior = json.loads(prior_path.read_text())
    Z0 = (4*PI*PI)**8 / 2**62
    log2, sqrt2 = RB(2).log(), RB(2).sqrt()
    h = log2/2
    nodes = []
    remainders = [RB(0), RB(0)]
    point_sums = [RB(0), RB(0)]
    for j in range(kernel.HEIGHT*kernel.STEP_DENOMINATOR+1):
        s = CB(2, QQ(j)/kernel.STEP_DENOMINATOR)
        two_s = (s*log2).exp()
        base = (2*s-1)*s.gamma()**16*s**7*kernel.dedekind_zeta(2*s)*(1+two_s)/(1-1/(2*two_s))
        base *= s*(s+1)*(s+2)
        weight = QQ(1 if j == 0 else 2)/kernel.STEP_DENOMINATOR
        # H=K3-K4 has multiplier -(s+2); Q=e^-x K4(A_center e^x).
        factors = [-base*(s+2)*weight/(2*PI), base*(s+3)*weight/(2*PI)]
        polynomials = []
        for which, factor in enumerate(factors):
            exponent = -s-which
            coefficients = [factor]
            for m in range(1, ORDER):
                coefficients.append(coefficients[-1]*exponent/m)
            polynomials.append(coefficients)
            remainders[which] += abs(factor)*abs(exponent)**ORDER
            point_sums[which] += (factor*(-s*Z0.log()).exp()).real()
        nodes.append((s, polynomials))
    remainders = [value*h**ORDER/factorial(ORDER)*((2+i)*h).exp()
                  for i, value in enumerate(remainders)]
    print("COMPLETED_NODES", len(nodes), "elapsed", round(time.monotonic()-started, 2), flush=True)

    # A=1 is an independent comparison against the corrected D93 replay.
    old_identity = next(row for row in prior["kernels"] if row["majorant_field_element"] == ["1"]+["0"]*7)
    old_values = {row["k"]: ball(row["value"]) for row in old_identity["values"]}
    e3 = kernel.quadrature_error(Z0, 3, kernel.STEP_DENOMINATOR)[0]
    e4 = kernel.quadrature_error(Z0, 4, kernel.STEP_DENOMINATOR)[0]
    identity = [point_sums[0].add_error((e3+e4).upper()), point_sums[1].add_error(e4.upper())]
    assert identity[0].overlaps(old_values[3]-old_values[4])
    assert identity[1].overlaps(old_values[4])
    assert (identity[0]+identity[1]).overlaps(old_values[3])

    rows = []
    for j in range(BLOCKS):
        center = RB(2**j)*sqrt2
        z = Z0*center
        sums = [[RB(0) for _ in range(ORDER)] for _ in range(2)]
        for s, polynomials in nodes:
            power = (-s*z.log()).exp()
            for which, coefficients in enumerate(polynomials):
                for m, coefficient in enumerate(coefficients):
                    sums[which][m] += (coefficient*power).real()
        low_z = Z0*2**j
        error3 = kernel.quadrature_error(low_z, 3, kernel.STEP_DENOMINATOR)[0]
        error4 = kernel.quadrature_error(low_z, 4, kernel.STEP_DENOMINATOR)[0]
        analytic_errors = [error3+error4, sqrt2*error4]
        values = {}
        for which, label in enumerate(["H", "Q"]):
            remainder = z**(-2)*remainders[which]
            error = remainder+analytic_errors[which]
            envelope = sum((abs(v)*h**m for m, v in enumerate(sums[which])), RB(0))+error
            values[label] = {"finite_Taylor_coefficients": [interval(v) for v in sums[which]],
                             "exponential_remainder_bound": interval(remainder),
                             "quadrature_error_bound": interval(analytic_errors[which]),
                             "absolute_bound": interval(envelope)}
        rows.append({"index": j, "A_lower": str(2**j), "A_upper": str(2**(j+1)),
                     "A_center": interval(center), "kernels": values})
        if j % 12 == 0:
            print("SCALAR_BLOCK", j, "A", 2**j, "H", values["H"]["absolute_bound"]["display"],
                  "elapsed", round(time.monotonic()-started, 2), flush=True)
    result = {"status": "pass: uniform completed scalar kernels on 96 dyadic A blocks",
              "precision_bits": kernel.PRECISION, "Taylor_order": ORDER, "log_half_width": interval(h),
              "contour": 2, "quadrature_step": "1/32", "quadrature_height": 16,
              "H_definition": "K3(Z0*A)-K4(Z0*A)",
              "Q_definition": "exp(-x)*K4(Z0*A_center*exp(x))",
              "S11_scalar": "(H(A)+(N/A)*K4(Z0*A))/A",
              "point_A1": {"H": interval(identity[0]), "K4": interval(identity[1]),
                           "K3": interval(identity[0]+identity[1]), "D93_overlap": True},
              "blocks": rows, "complete_A_range": ["1", str(2**BLOCKS)],
              "new_quaternion_enumeration": False, "new_Hecke_data": False,
              "full_Mellin_series_numerically_evaluated": False, "CM_anchor_derivative_nonzero": False,
              "sources": [kernel.source(p) for p in [Path(__file__), Path(kernel.__file__), prior_path,
                          DATA/"nelson_global_identification_d95.json"]]}
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS|360_nelson_completed_scalar_blocks", round(time.monotonic()-started, 2), flush=True)


if __name__ == "__main__":
    main()
