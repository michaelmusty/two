"""Final D93 audit: exact arithmetic plus corrected analytic exports.

The frozen 350 audit is retained as an arithmetic/provenance checkpoint.
The five 351 replays supersede the original analytic endpoint exports.
This audit uses standard Python and exact fractions, not Sage or Arb.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("prime_audit", Path(__file__).with_name("350_nelson_prime31_audit_refined.py"))
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
read_interval = prior.prev.read_interval
NAMES = {
    "d91": "nelson_interval_sum_d91.json",
    "norm_one": "nelson_norm_one_sum_d92_T25600.json",
    "norm_one_tail": "nelson_norm_one_packing_tail_d92.json",
    "prime31": "nelson_prime31_sum_d93.json",
    "all_ideals": "nelson_all_ideal_bounds_d93.json",
}


def intervals(value, path=()):
    if isinstance(value, dict):
        if "lower" in value and "upper" in value:
            yield path, read_interval(value)
        else:
            for key, child in value.items():
                yield from intervals(child, path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from intervals(child, path + (index,))


def compute():
    sources = {}

    def bind(path, expected=None):
        path = Path(path)
        if not path.is_absolute():
            path = ROOT / path
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected is not None:
            assert digest == expected, path
        name = str(path.relative_to(ROOT))
        sources[name] = {"path": name, "sha256": digest}

    def read(name):
        path = DATA / name
        bind(path)
        result = json.loads(path.read_text())
        for row in result.get("sources", []):
            bind(row["path"], row["sha256"])
        return result

    original = prior.compute()
    assert original == read("nelson_prime31_d93.json")
    d92 = read("nelson_norm_one_d92.json")
    exact = {}
    export_checks = []
    jobs = []
    for stage, name in NAMES.items():
        old = read(name)
        corrected_name = name[:-5] + "_exact_d93.json"
        new = read(corrected_name)
        exact[stage] = new
        metadata = new["endpoint_replay"]
        assert metadata["stage"] == stage
        assert metadata["method"] == "MPFR lower/upper().exact_rational()"
        control = metadata["pi_regression_control"]
        assert Q(control["exact_lower"]) < Q(control["old_lower"]) < Q(control["old_upper"]) < Q(control["exact_upper"])
        old_rows = dict(intervals(old))
        new_rows = dict(intervals(new))
        assert old_rows.keys() == new_rows.keys()
        for path, (lo, hi) in new_rows.items():
            assert lo <= hi
            assert all(v.denominator & (v.denominator - 1) == 0 for v in [lo, hi])
            previous = old_rows[path]
            assert prior.prev.overlap((lo, hi), previous)
            # This verifies the scale of the correction; agreement with
            # the old output is not used as an enclosure certificate.
            scale = max(Q(1), abs(lo), abs(hi))
            assert max(abs(lo - previous[0]), abs(hi - previous[1])) < scale / 10**40
        export_checks.append({"stage": stage, "artifact": corrected_name,
                              "interval_records": len(new_rows), **metadata["counts"]})
        job_name = f"nelson_endpoint_{stage}_attempt01.job.json"
        job = read(job_name)
        bind(job["log"]["path"], job["log"]["sha256"])
        assert job["status"] == "pass" and job["timeout_seconds"] == 180
        assert job["timeout_terminates_process_group"]
        jobs.append({"path": str((DATA / job_name).relative_to(ROOT)),
                     "status": job["status"], "wall_seconds": job["wall_seconds"]})
    print("EXACT_ENDPOINT_EXPORTS_PASS", sum(row["interval_records"] for row in export_checks), flush=True)

    unit = exact["norm_one"]
    packing = exact["norm_one_tail"]
    # The D92 exact class counts are bound to the unchanged arithmetic
    # certificate. The analytic checker uses only these set lengths.
    sets = {row["cutoff"]: range(row["norm_one_classes"]) for row in d92["exact"]}
    norm_one_audit = prior.prev.analytic_checks(unit, packing, sets)
    z0 = read_interval(next(row for row in exact["d91"]["kernels"]
                            if row["majorant_field_element"] == ["1"] + ["0"] * 7)["Z"])
    for row in packing["cutoffs"]:
        for a in ["1", "3", "5"]:
            for option in row["infinite_norm_one_tail"][a]["alternatives"]:
                c = Q(option["contour"])
                constants = next(v for v in unit["tail_constants"]["contours"] if Q(v["contour"]) == c)["constants"][a]
                b1 = read_interval(constants["2"]["bound"])[1]
                b2 = read_interval(constants[str(int(a) + 2)]["bound"])[1]
                m1 = read_interval(row["moment_bounds"][str(c)]["sum_A_to_minus_p_minus_one_upper_bound"])[1]
                m2 = read_interval(row["moment_bounds"][str(c + 1)]["sum_A_to_minus_p_minus_one_upper_bound"])[1]
                error = read_interval(option["bound"])[1]
                assert (error / (b1 * m1 + b2 * m2))**c.denominator * z0[0]**c.numerator >= 1
    packet = read("nelson_prime31_b27_d93_T25600.json")
    prime_audit = prior.analytic_checks(packet, exact["prime31"], exact["all_ideals"],
                                        unit["tail_constants"]["contours"], z0)
    print("CORRECTED_ANALYTIC_REPLAY_PASS", flush=True)

    # Reassemble final component enclosures by exact fraction arithmetic.
    # This avoids treating a product of serialized boxes as identical to
    # the corresponding original Arb operation on tighter live balls.
    selected = exact["prime31"]["weighted_first_quartic_orbit"][0]
    root = [Q(v) for v in prime_audit["refined_Hecke_root_intervals"][0]]
    root_abs = max(map(abs, root))
    summary = {}
    for a in ["1", "3", "5"]:
        unit_error = read_interval(packing["cutoffs"][-1]["infinite_norm_one_tail"][a]["absolute_error_bound"])[1]
        prime_error = read_interval(exact["prime31"]["cutoffs"][-1]["infinite_prime_family_tail"][a]["absolute_error_bound"])[1]
        other_error = read_interval(exact["all_ideals"]["uncomputed_norm_ideal_bounds"][a]["absolute_error_bound"])[1]
        two_error = unit_error + root_abs * prime_error
        partial = selected["unit_plus_prime_families"][a]["partial_sum"]
        enclosures = {}
        for part in ["real", "imag"]:
            lo, hi = read_interval(partial[part])
            if a == "1" and part == "imag":
                assert lo <= 0 <= hi
                enclosures[part] = {"two_families": ["0", "0"], "formal_series": ["0", "0"]}
            else:
                enclosures[part] = {
                    "two_families": [str(lo - two_error), str(hi + two_error)],
                    "formal_series": [str(lo - two_error - other_error), str(hi + two_error + other_error)],
                }
        summary[a] = {"partial_sum": partial, "two_family_absolute_tail_upper": str(two_error),
                      "all_other_ideals_absolute_upper": str(other_error), "enclosures": enclosures}
    lo, hi = read_interval(packing["cutoffs"][-1]["full_norm_one_family_enclosures"]["1"]["real"])
    assert 6193 < lo < hi < 8443
    lo, hi = map(Q, summary["1"]["enclosures"]["real"]["two_families"])
    assert lo < 0 < hi
    assert Q(summary["1"]["all_other_ideals_absolute_upper"]) < 2685 * 10**13
    for name in ["nelson_d93_audit_attempt01.job.json", "nelson_d93_audit_attempt02.job.json"]:
        job = read(name)
        bind(job["log"]["path"], job["log"]["sha256"])
    bind(Path(__file__))
    return {
        "status": "pass: exact-endpoint prime-family certificate; global bounds remain too loose",
        "supersedes_analytic_endpoint_exports": list(NAMES.values()),
        "exact_cutoffs": original["exact_cutoffs"], "cosets": original["cosets"],
        "norm_one_analytic": norm_one_audit, "prime_analytic": prime_audit,
        "endpoint_checks": export_checks, "certified_selected_sums": summary,
        "original_computational_jobs": original["jobs"], "endpoint_replay_jobs": jobs,
        "sources": sorted(sources.values(), key=lambda row: row["path"]),
        "all_ideal_absolute_convergence_proved": True, "complete_A_cutoff_evaluated": False,
        "useful_CM_accuracy_reached": False, "global_Shimizu_test_vector_identification_proved": False,
        "Shimura_derivative_computed": False,
        "next": "review global kernel/summation and test-vector identification before extending the Hecke bank or cutoff",
        "audit_scope": "exact arithmetic and rational interval-output checks; Arb nodes, recursion and analytic integrals bound to runs; proofs in D93 report",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = compute()
    output = DATA / "nelson_prime31_exact_d93.json"
    if args.check:
        assert result == json.loads(output.read_text())
    else:
        assert not output.exists()
        output.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: D93 exact-endpoint final audit;", len(result["sources"]), "hashes")


if __name__ == "__main__":
    main()
