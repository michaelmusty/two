"""D97: signed displacement blocks, using only the certified D92/D93 data.

Reduced conjugation makes every complete displacement shell real. Its
phase sum is an exact element of F, computed from reduced traces without
recovering an angle. Discrete Abel summation retains cancellation before
taking absolute values. The saved infinite-tail bounds remain necessary;
finite signed-count observations are never extrapolated.
"""
import importlib.util
import json
from pathlib import Path
import time
from sage.all import AA, QQ, NumberField, PolynomialRing, QuaternionAlgebra

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("scalar", Path(__file__).with_name("360_nelson_completed_scalar_blocks.py"))
scalar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scalar)
RB, CB = scalar.RB, scalar.CB
interval, ball = scalar.interval, scalar.ball


def canonical(v):
    v = tuple(v)
    return v if next(c for c in v if c) > 0 else tuple(-c for c in v)


def coefficients(x):
    return list(map(str, x.list()))


def summarize(rows):
    """A rigorous finite Abel bound; no infinite-tail claim is made here."""
    signed = sum((r["term"] for r in rows), RB(0))
    grouped_absolute = sum((abs(r["term"]) for r in rows), RB(0))
    atomic_absolute = sum((r["atomic_absolute"] for r in rows), RB(0))
    phase = RB(0)
    abel = RB(0)
    abel_bound = RB(0)
    for i, row in enumerate(rows):
        phase += row["phase"]
        difference = row["f"] - rows[i+1]["f"] if i+1 < len(rows) else row["f"]
        abel += phase*difference
        abel_bound += abs(phase)*abs(difference)
    assert abel.overlaps(signed)
    best = min(grouped_absolute.upper(), abel_bound.upper()).exact_rational()
    assert abs(signed).lower().exact_rational() <= best
    return {"groups": len(rows), "classes": sum(r["count"] for r in rows),
            "signed_sum": interval(signed), "signed_phase_sum": interval(phase),
            "atomic_absolute_sum": interval(atomic_absolute),
            "grouped_absolute_sum": interval(grouped_absolute),
            "Abel_reconstruction": interval(abel), "Abel_absolute_bound": interval(abel_bound),
            "best_finite_bound_upper": str(best)}


def main():
    started = time.monotonic()
    output = DATA / "nelson_signed_orbit_blocks_d97.json"
    assert not output.exists()
    names = ["nelson_completed_majorant_d96.json",
             "nelson_norm_one_d92_T25600.json",
             "nelson_norm_one_sum_d92_T25600_exact_d93.json",
             "nelson_prime31_b27_d93_T25600.json",
             "nelson_prime31_sum_d93_exact_d93.json"]
    prior, unit, unit_sum, prime, prime_sum = [json.loads((DATA/n).read_text()) for n in names]
    R = PolynomialRing(QQ, "s")
    s = R.gen()
    F = NumberField(s**8-8*s**6+20*s**4-16*s**2+2, "b")
    b = F.gen()
    B = QuaternionAlgebra(F, b-b*b, -1)
    place = sorted(F.embeddings(AA), key=lambda v: v(b))[4]
    real = lambda x: RB(place(x))
    root = real(b)
    families = []
    for label, N, enumeration, saved in [("unit", 1, unit, unit_sum), ("prime31_b27", 31, prime, prime_sum)]:
        n = F(1) if N == 1 else F(list(map(QQ, enumeration["norm_generator"]["totally_positive_generator_coefficients"])))
        assert n.norm() == N
        classes = {canonical(map(QQ, row["quaternion_power_coordinates"])): row for row in enumeration["classes"]}
        assert len(classes) == len(enumeration["classes"])
        kernels = {tuple(row["A_field_coefficients"]): row for row in saved["kernels"]}
        terms = {row["class_index"]: row["values"]["1"] for row in saved["class_terms"]}
        groups = {}
        partners = []
        for q, row in classes.items():
            conjugate = canonical(q[:8]+tuple(-c for c in q[8:]))
            mate = classes[conjugate]
            key = tuple(row["A_field_coefficients"])
            assert mate["A_field_coefficients"] == list(key)
            partners.append([row["index"], mate["index"]])
            quaternion = B([F(q[8*j:8*(j+1)]) for j in range(4)])
            assert quaternion.reduced_norm() == n
            A = F(list(map(QQ, key)))
            trace = 2*F(q[:8])
            tau = N*trace**2/(4*n*A)
            phase_real = 1-8*tau+8*tau**2
            phase = real(phase_real)
            assert phase.lower() >= -1 and phase.upper() <= 1 or phase_real in [F(-1), F(1)]
            if key not in groups:
                values = {v["k"]: ball(v["value"]) for v in kernels[key]["values"]}
                a = real(A)
                assert a.overlaps(ball(kernels[key]["A"]))
                f = (values[3]-(1-N/a)*values[4])/a
                groups[key] = {"A_field": A, "A": a, "f": f, "phase_field": F(0),
                               "indices": [], "saved_real": RB(0), "saved_imag": RB(0), "atomic_absolute": RB(0)}
            g = groups[key]
            value = terms[row["index"]]
            old_real, old_imag = ball(value["real"]), ball(value["imag"])
            assert (phase*g["f"]).overlaps(old_real)
            g["phase_field"] += phase_real
            g["indices"].append(row["index"])
            g["saved_real"] += old_real
            g["saved_imag"] += old_imag
            g["atomic_absolute"] += abs(CB(old_real, old_imag))
        rows = sorted(groups.values(), key=lambda g: g["A"].mid())
        encoded = []
        cumulative = RB(0)
        prefix_counts = 0
        # These are finite-range observations for the entire ideal family,
        # not estimates for individual right orbits or for an infinite tail.
        observed_constants = {"1/2": RB(0), "2/3": RB(0)}
        max_candidates = {key: [] for key in observed_constants}
        for i, g in enumerate(rows):
            if i:
                assert rows[i-1]["A"].upper() < g["A"].lower()
            assert g["A"].upper() <= 25600
            g["phase"] = real(g["phase_field"])
            g["term"] = g["phase"]*g["f"]
            g["count"] = len(g["indices"])
            assert g["term"].overlaps(g["saved_real"]) and g["saved_imag"].contains_zero()
            cumulative += g["phase"]
            prefix_counts += g["count"]
            for theta in observed_constants:
                max_candidates[theta].append(abs(cumulative)/(g["A"]/N)**QQ(theta))
            encoded.append({"A_field_coefficients": coefficients(g["A_field"]), "A": interval(g["A"]),
                            "class_indices": sorted(g["indices"]), "phase_sum_field_coefficients": coefficients(g["phase_field"]),
                            "phase_sum": interval(g["phase"]), "radial_scalar": interval(g["f"]),
                            "signed_term": interval(g["term"]), "cumulative_signed_phase": interval(cumulative),
                            "cumulative_count": prefix_counts})
        for theta, candidates in max_candidates.items():
            observed_constants[theta] = {"lower": str(max(v.lower().exact_rational() for v in candidates)),
                                         "upper": str(max(v.upper().exact_rational() for v in candidates))}
        cutoffs = []
        shells = []
        previous = 0
        for T in [400, 1600, 6400, 25600]:
            assert all(not (g["A"].lower() <= T <= g["A"].upper()) for g in rows)
            selected = [g for g in rows if g["A"].upper() < T]
            summary = summarize(selected)
            old = next(r for r in saved["cutoffs"] if r["cutoff"] == T)
            assert summary["classes"] == old["class_count"]
            assert ball(summary["signed_sum"]).overlaps(ball(old["partial_sums"]["1"]["real"]))
            cutoffs.append({"cutoff": T, **summary})
            shell = [g for g in selected if g["A"].lower() > previous]
            shells.append({"lower_exclusive": previous, "upper_inclusive": T, **summarize(shell)})
            previous = T
        family = {"label": label, "norm": N, "norm_generator": coefficients(n),
                  "class_count": len(classes), "group_count": len(rows), "conjugation_partners": sorted(partners),
                  "groups": encoded, "cutoffs": cutoffs, "shells": shells,
                  "observed_finite_prefix_constants": observed_constants,
                  "finite_prefix_constant_scope": "whole saved ideal family, N<=A<=25600 only; no extrapolation"}
        families.append(family)
        print("SIGNED_FAMILY", label, "classes", len(classes), "groups", len(rows), flush=True)
        for row in shells:
            print("SHELL", label, row["lower_exclusive"], row["upper_inclusive"],
                  "sum", row["signed_sum"]["display"], "atomic", row["atomic_absolute_sum"]["display"],
                  "grouped", row["grouped_absolute_sum"]["display"], "Abel", row["Abel_absolute_bound"]["display"], flush=True)
        print("FINITE_CONSTANTS", label, {k: str(ball(v)) for k, v in observed_constants.items()}, flush=True)
    result = {"status": "pass: exact signed-shell grouping and finite Abel bounds; no certified signed infinite tail",
              "precision_bits": scalar.kernel.PRECISION, "split_field_root": interval(root),
              "phase_formula": "tau=N*Trd(alpha)^2/(4*n*A); Re(Phi_1)=1-8*tau+8*tau^2",
              "families": families,
              "unchanged_omitted_ideal_error_upper": prior["certified_omitted_S11_error_upper"],
              "unchanged_full_S11_error_upper": prior["certified_full_S11_error_upper"],
              "unchanged_full_S11_enclosure": prior["full_S11_rational_enclosure"],
              "signed_infinite_tail_bound_proved": False, "new_quaternion_enumeration": False,
              "new_Hecke_data": False, "enumeration_expansion_justified": False,
              "CM_anchor_derivative_nonzero": False,
              "sources": [scalar.kernel.source(p) for p in [Path(__file__), Path(scalar.__file__), Path(scalar.kernel.__file__)]+[DATA/n for n in names]]}
    output.write_text(json.dumps(result, indent=2)+"\n")
    print("PASS|363_nelson_signed_orbit_blocks", round(time.monotonic()-started, 3), flush=True)


if __name__ == "__main__":
    main()
