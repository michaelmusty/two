"""D87: independently unwrap saved samples and audit the numerical character.

Uses only Python's standard library.  Passing this audit is NOT a rigorous
certificate of the analytic input, of descent, or of the arithmetic twist.
"""
import argparse
import cmath
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE, DATA = ROOT/"dembele/pari", ROOT/"dembele/data/computed"
OUTPUT = DATA/"cm_frame_double_cover_character_d87.json"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def z(pair):
    return complex(*map(float, pair))


def number(x):
    return format(x, ".12g")


def unwrap(values):
    """Accumulate arguments; independent of nearest-square-root selection."""
    phase = cmath.phase(values[0])
    for a, b in zip(values, values[1:]):
        phase += cmath.phase(b/a)
    return math.sqrt(abs(values[-1]))*cmath.exp(.5j*phase)


def check_path(path):
    samples = path["samples"]
    times = [float(s["t"]) for s in samples]
    values = [z(s["R"]) for s in samples]
    derivatives = [z(s["logarithmic_derivative_along_path"]) for s in samples]
    assert times[0] == 0 and times[-1] == 1
    assert all(a < b for a,b in zip(times, times[1:]))
    arguments = [abs(cmath.phase(b/a)) for a,b in zip(values, values[1:])]
    moduli = [abs(math.log(abs(b/a))) for a,b in zip(values, values[1:])]
    estimates = [(times[j+1]-times[j])*max(abs(derivatives[j]), abs(derivatives[j+1]))
                 for j in range(len(times)-1)]
    assert max(arguments+moduli+estimates) < .15000001
    root = unwrap(values)
    assert abs(root/z(path["sqrt_R_endpoint"])-1) < 1e-10, "stored root disagrees with sampled winding"
    assert abs(root/z(path["coarse_sqrt_R_endpoint"])-1) < 1e-10
    assert abs(root**2/values[-1]-1) < 1e-10
    return root, len(samples), max(arguments), max(moduli), max(estimates)


def sign(permutation):
    assert sorted(permutation) == [1, 2, 3]
    return (-1)**sum(permutation[i] > permutation[j] for i in range(3) for j in range(i+1, 3))


def exact_permutations():
    text = (DATA/"genus64_cosets.gp").read_text().strip()
    depth = 0
    for k in range(1, len(text)):
        depth += (text[k] == "[")-(text[k] == "]")
        if depth == 0:
            result = json.loads(text[1:k+1]); assert len(result) == 277
            return result
    raise ValueError("unterminated permutation vector")


def campaign(bank, bend, permutations):
    paths = {}
    files = sorted(DATA.glob(f"cm_frame_double_cover_tail_{bank}_*_b{bend}_d87.json"))
    if bend == "0p0":
        files = [DATA/f"cm_frame_double_cover_adaptive_{bank}_0_26_b0p0_d87.json", *files]
    count, angle, modulus, derivative = 0, 0., 0., 0.
    for file in files:
        report = json.loads(file.read_text())
        assert report["bank"] == bank
        for path in report["paths"]:
            root, n, a, b, c = check_path(path)
            i = path["path_index"]
            if i in paths:
                assert abs(root/paths[i]-1) < 1e-10, "full polynomial and tail-skipping controls disagree"
            else:
                paths[i] = root
                count += n; angle = max(angle, a); modulus = max(modulus, b); derivative = max(derivative, c)
    assert set(paths) == set(range(550)), f"incomplete campaign: {bank} {bend}, {len(paths)} paths"
    receipt = json.loads((DATA/f"cm_frame_double_cover_polynomials_{bank}_d87.json").read_text())
    assert receipt["independent_checked_endpoints"] == receipt["folded_endpoint_count"] == 550
    assert float(receipt["full_convolution_substitution_relative_error_max"]) < 1e-42
    checks = []
    for side, permutation in zip(receipt["side_records"], permutations):
        expected = sign(permutation)
        assert side["permutation"] == permutation and side["expected_sign"] == expected
        if side["rotation"]:
            value = z(side["rotation_character"])
            assert float(side["rotation_v_invariance_error"]) < 1e-35
        else:
            value = (z(side["gw"])/z(side["w"]))**16*paths[side["gv_path"]]/paths[side["v_path"]]
        error = abs(value-expected)
        assert error < 1e-5, f"character mismatch at side {side['index_zero_based']}: {value} vs {expected}"
        checks.append({"side_index_zero_based": side["index_zero_based"], "expected_sign": expected,
                       "computed_character": [number(value.real), number(value.imag)],
                       "distance_to_expected_sign": number(error), "rotation": side["rotation"]})
    assert len(checks) == 277
    return {"bank": bank, "bend": bend, "paths": len(paths), "samples": count,
            "side_generators_matched": len(checks), "maximum_sign_error": number(max(float(s["distance_to_expected_sign"]) for s in checks)),
            "maximum_argument_step": number(angle), "maximum_log_modulus_step": number(modulus),
            "maximum_endpoint_derivative_step_estimate": number(derivative),
            "side_checks": checks}, paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    permutations = exact_permutations()
    campaigns, roots = [], []
    for bank, bend in [("current", "0p0"), ("previous", "0p0"), ("current", "0p03")]:
        report, values = campaign(bank, bend, permutations)
        campaigns.append(report); roots.append(values)
        print("SAMPLED_CHARACTER_MATCH", bank, bend, report["side_generators_matched"], report["maximum_sign_error"], flush=True)
    cross_bank = max(abs(roots[1][i]/roots[0][i]-1) for i in range(550))
    cross_path = max(abs(roots[2][i]/roots[0][i]-1) for i in range(550))
    assert cross_bank < 1e-5 and cross_path < 1e-10
    # Known winding controls and an explicitly reversed stored branch.
    for winding in range(-3, 4):
        values = [cmath.exp(2j*math.pi*winding*k/128) for k in range(129)]
        assert abs(unwrap(values)-(-1)**winding) < 1e-12
    pilot = json.loads((DATA/"cm_frame_double_cover_adaptive_current_0_26_b0p0_d87.json").read_text())
    bad = copy.deepcopy(pilot["paths"][0])
    bad["sqrt_R_endpoint"] = [str(-float(x)) for x in bad["sqrt_R_endpoint"]]
    rejected = False
    try:
        check_path(bad)
    except AssertionError as error:
        assert "stored root" in str(error); rejected = True
    assert rejected
    # Exact S3 parity is independently reconstructed, not trusted from the cache.
    trivial_character_mismatches = sum(sign(p) < 0 for p in permutations)
    assert trivial_character_mismatches == 133
    artifacts = sorted(p for p in DATA.glob("cm_frame_double_cover_*d87*") if p.is_file() and p != OUTPUT)
    scripts = sorted(p for p in HERE.iterdir() if p.is_file() and p.name[:3].isdigit() and 306 <= int(p.name[:3]) <= 318)
    sources = [source(p) for p in [*scripts, *artifacts, DATA/"cm_frame_cubic_adjoint_audit_128.json"]]
    seen, linked = {}, set()

    def walk(value):
        if isinstance(value, dict):
            if "path" in value and "sha256" in value:
                path = Path(value["path"]).resolve(); key = str(path)
                if key not in seen:
                    seen[key] = hashlib.sha256(path.read_bytes()).hexdigest()
                assert seen[key] == value["sha256"], "changed source: "+key
                if path.suffix == ".json" and key not in linked:
                    linked.add(key); walk(json.loads(path.read_text()))
            for item in value.values(): walk(item)
        elif isinstance(value, list):
            for item in value: walk(item)

    walk(sources)
    jobs = []
    for path in artifacts:
        if not path.name.endswith("_job.json"): continue
        job = json.loads(path.read_text())
        expected_failure = path.name == "cm_frame_double_cover_polynomials_current_d87_build_job.json"
        assert job["status"] == ("failed" if expected_failure else "pass")
        assert job["timeout_terminates_process_group"] and job["timeout_seconds"] == 180
        assert job["wall_seconds"] < 180
        jobs.append({"name": path.name, "status": job["status"], "wall_seconds": job["wall_seconds"]})
    summary = {"status": "pass: numerical character comparison only", "milestone": "D87", "date": "2026-09-23",
               "sources": sources, "campaigns": campaigns,
               "cross_bank_sqrt_relative_error_max": number(cross_bank),
               "cross_path_sqrt_relative_error_max": number(cross_path),
               "controls": {"known_windings": 7, "reversed_stored_branch_rejected": rejected,
                            "trivial_character_mismatches": trivial_character_mismatches,
                            "full_polynomial_and_finite_tail_overlap_paths": 26},
               "jobs": jobs, "verified_file_hashes": len(seen), "linked_json_records": len(linked),
               "rigorous_analytic_identification_obtained": False, "constant_arithmetic_twist_identified": False,
               "D77_conditional_scalar_twist_uniqueness_retained": True,
               "selected_cubic_class_identified": False, "target_field_constructed": False,
               "limitations": ["geometry and differential-series tail remain uncertified",
                               "endpoint logarithmic derivative estimates are refinement guides, not interval bounds",
                               "complex signs do not distinguish constant arithmetic quadratic twists",
                               "matching the sign quotient does not identify the selected 3-division class"]}
    if args.check:
        assert json.loads(OUTPUT.read_text()) == summary, "changed numerical audit"
    else:
        assert not OUTPUT.exists(), "do not overwrite an earlier root"
        OUTPUT.write_text(json.dumps(summary, indent=2)+"\n")
    print("PASS|318_NUMERICAL_CHARACTER_AUDIT", len(seen), len(linked), flush=True)


if __name__ == "__main__":
    main()
