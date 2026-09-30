"""D71: construct or independently verify a double cover over F31.

The scalar used for discovery is a Hecke guess, not a proved Jacobian
order. Only the explicit final divisor identity certifies the cover.
Neither its characteristic-zero lift nor its Shimura identification is
certified. Default mode checks the saved candidate; --discover reruns
the bounded geometric divisor arithmetic first.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import time


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
MAGMA = "/Applications/Magma/magma"
ERRORS = ("Runtime error", "User error", "Assertion failed", "Error:")
STEM = "cm_frame_resolvent"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def verify_sources(items):
    for item in items:
        if source(item["path"]) != item:
            raise ValueError(f"changed source or artifact: {item['path']}")


def run_magma(script, log_path, timeout, marker):
    command = [MAGMA, "-bn", "-l", "2000000000", str(script)]
    started = time.monotonic()
    status, exit_code = "failed", None
    with log_path.open("w") as log:
        try:
            run = subprocess.run(command, cwd=ROOT, stdout=log,
                                 stderr=subprocess.STDOUT, timeout=timeout)
        except subprocess.TimeoutExpired:
            status = "timeout"
        else:
            exit_code = run.returncode
            output = log_path.read_text()
            if exit_code == 0 and marker in output and not any(e in output for e in ERRORS):
                status = "pass"
    return {"command": command, "status": status, "exit_code": exit_code,
            "wall_seconds": time.monotonic()-started,
            "timeout_seconds": timeout, "memory_limit_bytes": 2_000_000_000,
            "log": source(log_path)}


def read_discovery(output):
    if "PASS|BRANCH_HALF_MOD31" not in output or any(e in output for e in ERRORS):
        raise ValueError("invalid discovery log")
    def array(label, following):
        value = re.search(r"^"+label+r" (.*?)\n"+following, output, re.MULTILINE|re.DOTALL)
        if value is None:
            raise ValueError(f"missing discovery array {label}")
        return ast.literal_eval(value.group(1))
    num = array("NUMERATOR", "DENOMINATOR")
    den = array("DENOMINATOR", "E_QUADRICS")
    eqs = array("E_QUADRICS", "MONOMIAL_PAIRS")
    pairs = array("MONOMIAL_PAIRS", r"PASS\|BRANCH_HALF_MOD31")
    assert len(pairs) == 136 and len({tuple(p) for p in pairs}) == 136
    assert all(1 <= i <= j <= 16 for i,j in pairs)
    assert all(len(row) == 136 and all(isinstance(c,int) and 0 <= c < 31 for c in row)
               for row in [num,den]+eqs)
    assert re.search(r"^HALF_CLASS_RR_DIMENSION 1$", output, re.MULTILINE)
    return {"monomial_pairs_one_based": pairs, "numerator_coefficients": num,
            "denominator_coefficients": den, "E_quadric_coefficients": eqs}


def write_magma_candidate(candidate):
    marks = json.loads((DATA/"cm_frame_marks.json").read_text())
    values = {
        "resolvent_pairs": candidate["monomial_pairs_one_based"],
        "resolvent_numerator": candidate["numerator_coefficients"],
        "resolvent_denominator": candidate["denominator_coefficients"],
        "resolvent_E_quadrics": candidate["E_quadric_coefficients"],
        "resolvent_point_jets": marks["ordinary_point_certificate"]["canonical_jet_coefficients"],
    }
    (DATA/(STEM+".m")).write_text(
        "// D71: coefficients over F31; mixed monomials have no factor of two.\n"
        + "".join(f"{name} := {value};\n" for name,value in values.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--discover", action="store_true")
    mode.add_argument("--collect-only", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--discovery-timeout", type=int, default=900)
    args = parser.parse_args()
    if min(args.timeout,args.discovery_timeout) < 1:
        parser.error("positive timeouts required")
    report_path = DATA/(STEM+"_check.json")
    candidate_path = DATA/(STEM+".json")
    if args.collect_only:
        report = json.loads(report_path.read_text())
        verify_sources(report["sources"]+[report["job"]["log"]])
        assert report["job"]["status"] == "pass"
        candidate = json.loads(candidate_path.read_text())
        verify_sources(candidate["discovery_sources"]+[candidate["discovery_job"]["log"]])
    else:
        if args.discover:
            # Preserve the exact discovery source used in the initial run.
            # It loads this task-owned scratch file; the archived copy is hashed.
            shutil.copyfile(DATA/(STEM+"_input.m"), "/private/tmp/dembele_d71_half_input.m")
            script = ROOT/"dembele/magma/121_cm_frame_resolvent.m"
            log_path = DATA/(STEM+"_discovery.out")
            job = run_magma(script,log_path,args.discovery_timeout,"PASS|BRANCH_HALF_MOD31")
            if job["status"] != "pass":
                (DATA/(STEM+"_discovery_failure.json")).write_text(json.dumps(job,indent=2)+"\n")
                raise RuntimeError(f"discovery {job['status']}; see {log_path}")
            candidate = read_discovery(log_path.read_text())
            candidate.update({"discovery_job": job,
                              "discovery_sources": [source(p) for p in (
                                  script,DATA/(STEM+"_input.m"),
                                  DATA/"cm_frame_curve_candidate.m",DATA/"cm_frame_marks.m",
                                  DATA/"cm_frame_marks.json",DATA/"cm_frame_curve_verification.json")]})
            candidate_path.write_text(json.dumps(candidate,indent=2)+"\n")
        candidate = json.loads(candidate_path.read_text())
        verify_sources(candidate["discovery_sources"]+[candidate["discovery_job"]["log"]])
        write_magma_candidate(candidate)
        script = ROOT/"dembele/magma/122_cm_frame_resolvent_check.m"
        log_path = DATA/(STEM+"_check.out")
        sources = [source(p) for p in (
            __file__,script,candidate_path,DATA/(STEM+".m"),
            DATA/"cm_frame_curve_candidate.m",DATA/"cm_frame_marks.m",
            DATA/"cm_frame_marks.json",DATA/"cm_frame_curve_verification.json",
            DATA/"cm_frame_marks_check.json",DATA/"levelraise_p2k_charpolys.m")]
        job = run_magma(script,log_path,args.timeout,"PASS|122_CM_FRAME_RESOLVENT_CHECK")
        report = {"status": job["status"], "milestone": "D71", "date": "2026-09-18",
                  "sources": sources, "job": job}
        report_path.write_text(json.dumps(report,indent=2)+"\n")
        print(job["status"],f"{job['wall_seconds']:.3f}s",flush=True)
        if job["status"] != "pass":
            print(log_path.read_text()[-5000:],flush=True)
            raise SystemExit(1)
    output = Path(report["job"]["log"]["path"]).read_text()
    assert "PASS|122_CM_FRAME_RESOLVENT_CHECK" in output
    assert not any(e in output for e in ERRORS)
    counts = list(map(int,re.search(r"^POINT_COUNTS\|(\d+)\|(\d+)$",output,re.MULTILINE).groups()))
    fibers = re.findall(r"^COVER_FIBER\|(.+)\|([^|]+)\|(\d+)\|(\d+)$",output,re.MULTILINE)
    assert len(fibers) == 50
    assert [sum(int(row[j]) for row in fibers) for j in (2,3)] == counts
    assert sum(row[1] == "ramified" for row in fibers) == 1
    assert sum(counts) == 100
    nonsquare = int(re.search(r"^TWIST_NONSQUARE\|(\d+)$",output,re.MULTILINE).group(1))
    expected = int(re.search(r"^HECKE_EXPECTED_POINTS\|(\d+)$",output,re.MULTILINE).group(1))
    matching_twists = [c for c,n in zip([1,nonsquare],counts) if n == expected]
    verification = json.loads((DATA/"cm_frame_curve_verification.json").read_text())
    coefs = verification["Hecke_trace_polynomial_coefficients_ascending"]
    guess = sum(int(c)*32**i for i,c in enumerate(coefs))
    assert guess == 1640801490553691915934375 and guess % 2 == 1
    report.update({
        "field_characteristic": 31,
        "equation": "z^2 = q_num/q_den; coefficients in cm_frame_resolvent.m",
        "divisor_identity": "div(q_num/q_den) = D17 + 15*P32 - 2*E; deg(E)=16",
        "branch_divisor": "D17 + P32", "branch_degree": 18,
        "half_line_bundle": "O(E - 7*P32)", "half_line_bundle_degree": 9,
        "geometrically_connected": True, "smooth_projective_cover_genus": 40,
        "point_counts_over_F31": counts, "constant_twist_nonsquare": nonsquare,
        "norm_one_Hecke_expected_points_over_F31": expected,
        "twist_scalars_matching_that_count": matching_twists,
        "rational_ramified_points": 1,
        "heuristic_Jacobian_order_used_only_for_discovery": guess,
        "Jacobian_order_certified": False, "half_class_uniqueness_certified": False,
        "cover_lifted_to_characteristic_zero": False,
        "saved_sign_monodromy_matched": False, "Shimura_identification_certified": False,
        "genus64_cover_constructed": False, "target_field_polynomial_obtained": False,
    })
    report_path.write_text(json.dumps(report,indent=2)+"\n")
    print(f"PASS: exact genus-40 double cover over F31; twist counts {counts}. Lifting and identification remain open.")


if __name__ == "__main__":
    main()
