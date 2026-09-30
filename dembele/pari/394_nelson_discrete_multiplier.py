"""D108: certify the completed multiplier on the weight-two discrete series.

This is a necessary-condition diagnostic for a uniform spectral majorant,
not a bound on the entire spectrum or a Shimura differential evaluation.
The D98 transform at mu=1 is exactly (8*pi/N)*K_1(Z0*N).
"""
import importlib.util
import json
from pathlib import Path
import time
from sage.all import QQ

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"
spec = importlib.util.spec_from_file_location("d91_kernel", ROOT/"dembele/pari/333_nelson_interval_sum.py")
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)
RB, CB, PI = kernel.RB, kernel.CB, kernel.PI


def interval(value):
    return {"lower": str(value.lower().exact_rational()),
            "upper": str(value.upper().exact_rational()), "display": str(value)}


def ball(row):
    lo, hi = QQ(row["lower"]), QQ(row["upper"])
    value = RB((lo+hi)/2).add_error((hi-lo)/2)
    assert value.lower().exact_rational() <= lo <= hi <= value.upper().exact_rational()
    return value


def main():
    output = DATA/"nelson_discrete_multiplier_d108.json"
    assert not output.exists(), "Preserve completed artifacts."
    start = time.monotonic()
    denominator, height = 32, 16
    norms = [1, 31]
    Z0 = (4*PI*PI)**8/2**62
    arguments = {N: Z0*N for N in norms}
    logs = {N: z.log() for N, z in arguments.items()}
    sums = {N: RB(0) for N in norms}
    coarse = {N: RB(0) for N in norms}
    # Keep the completed Mellin cancellation before taking absolute values.
    for j in range(height*denominator+1):
        s = CB(2, QQ(j)/denominator)
        two_s = CB(2)**s
        base = (2*s-1)*s.gamma()**16*s**8*kernel.dedekind_zeta(2*s)*(1+two_s)/(1-1/(2*two_s))
        weight = 1 if j == 0 else 2
        for N in norms:
            term = weight*(base*(-s*logs[N]).exp()).real()
            sums[N] += term
            if j % 2 == 0:
                coarse[N] += term
        if j % 128 == 0:
            print("NODE", j, "ELAPSED", round(time.monotonic()-start, 2), flush=True)
    rows = []
    h_max = 4*PI*(5-2*RB(6).sqrt())
    h_d98 = 80*PI/221  # p=13/4, hence c=5/4.
    for N in norms:
        error, strip, tail = kernel.quadrature_error(arguments[N], 1, denominator)
        center = sums[N]/(2*PI*denominator)
        value = center.add_error(error.upper())
        error_coarse, _, _ = kernel.quadrature_error(arguments[N], 1, denominator//2)
        coarse_value = (coarse[N]/(PI*denominator)).add_error(error_coarse.upper())
        assert value.overlaps(coarse_value)
        assert value.upper().exact_rational()-value.lower().exact_rational() < QQ(1)/10**25
        H = 8*PI/N*value
        rows.append({"norm": N, "argument": interval(arguments[N]),
                     "K1": interval(value), "finite_quadrature": interval(center),
                     "strip_error": interval(strip), "vertical_tail": interval(tail),
                     "coarse_K1": interval(coarse_value), "coarse_error": interval(error_coarse),
                     "independent_mesh_overlap": True, "H_N_mu1": interval(H),
                     "minimum_uniform_comparison_constant_any_p": interval(abs(H)/h_max),
                     "minimum_uniform_comparison_constant_D98_p": interval(abs(H)/h_d98)})
        print("NORM", N, "K1", value, "H_MU1", H, flush=True)
    prior_path = DATA/"nelson_spectral_ideal_bound_d98.json"
    prior = json.loads(prior_path.read_text())
    partial = ball(prior["selected_S11_partial_sum"])
    saved_tail = ball(prior["two_saved_family_error"])
    H31 = ball(rows[1]["H_N_mu1"])
    delta = QQ(7)/64
    # Seven of eight norm-31 prime ideals are absent from the saved families.
    # For the current absolute Hecke envelopes the mass per prime is
    # (2*sqrt(31))*(2*31^(1/2+delta))=4*31^(1+delta).
    # Any comparison C*h_p has C >= |H_31(1)|/max_p h_p(1).
    weight = 7*4*RB(31)**(1+delta)
    floor = weight*abs(H31)/h_max
    # Even the stronger finite-place exponent zero would leave this floor.
    ramanujan_floor = 7*4*31*abs(H31)/h_max
    result = {"status": "pass", "milestone": "D108",
              "precision_bits": kernel.PRECISION, "contour": 2,
              "mesh_denominator": denominator, "height": height,
              "strip_half_width": 1, "pi": interval(PI), "Z0": interval(Z0),
              "multiplier_identity": "H_N(1)=8*pi/N*K1(Z0*N)",
              "comparison_transform_D2": "h_p(1)=4*pi*(p-2)/(p*(p+1))",
              "maximum_comparison_transform_D2": interval(h_max),
              "maximizing_p": interval(2+RB(6).sqrt()),
              "D98_comparison_transform_D2": interval(h_d98), "rows": rows,
              "omitted_norm31_primes": 7, "absolute_Hecke_exponent": str(delta),
              "omitted_norm31_absolute_Hecke_weight": interval(weight),
              "comparison_method_floor_from_norm31": interval(floor),
              "comparison_method_floor_with_exponent_zero": interval(ramanujan_floor),
              "saved_partial": interval(partial), "saved_two_family_error": interval(saved_tail),
              "floor_over_partial": interval(floor/abs(partial)),
              "floor_exceeds_saved_partial": floor.lower() > abs(partial).upper(),
              "full_spectrum_majorant_constructed": False,
              "actual_omitted_sum_lower_bound_claimed": False,
              "new_quaternion_enumeration": False, "new_Hecke_data": False,
              "Shimura_tangent_evaluated": False,
              "scope": "Necessary lower floor on a per-ideal absolute Hecke and positive h_p comparison, using a required discrete-series parameter. No lower bound on the actual omitted sum or all possible methods.",
              "sources": [kernel.source(p) for p in [Path(__file__), Path(kernel.__file__), prior_path,
                         ROOT/"dembele/certificates/nelson-spectral-ideal-d98.md"]]}
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("METHOD_FLOOR", floor, "FLOOR_OVER_PARTIAL", floor/abs(partial), flush=True)
    print("PASS|D108_DISCRETE_MULTIPLIER", flush=True)


if __name__ == "__main__":
    main()
