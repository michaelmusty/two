"""Run/collect the exact D70 marked-divisor certificate with bounded Magma.

Script 119 discovers the marked candidates and proves the ordinary-point
jet assertion. This script checks the divisors, their good specialization,
the nonic Galois group, and a failed branch-function ansatz. CM labels and
identification of the Shimura curve remain unproved.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
MAGMA = "/Applications/Magma/magma"
ERRORS = ("Runtime error", "User error", "Assertion failed", "Error:")
MARKER = "PASS|120_CM_FRAME_MARKS"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def field(output, label):
    match = re.search(r"^" + re.escape(label) + r"\|(.+)$", output, re.MULTILINE)
    if match is None:
        raise ValueError(f"missing output field {label}")
    return match.group(1).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("positive timeout required")
    script = ROOT / "dembele/magma/120_cm_frame_marks.m"
    log_path = DATA / "cm_frame_marks_check.out"
    report_path = DATA / "cm_frame_marks_check.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        for item in report["sources"] + [report["job"]["log"]]:
            if source(item["path"]) != item:
                raise ValueError(f"changed input or log: {item['path']}")
        if report["job"]["status"] != "pass":
            raise ValueError("saved job did not pass")
    else:
        report = {
            "status": "running", "milestone": "D70", "date": "2026-09-18",
            "sources": [source(p) for p in (
                __file__, script, ROOT/"dembele/pari/119_cm_frame_marks.py",
                DATA/"cm_frame_curve_candidate.m", DATA/"cm_frame_curve_candidate.json",
                DATA/"cm_frame_curve_verification.json",
                DATA/"cm_frame_marks.m", DATA/"cm_frame_marks.json",
            )],
            "timeout_seconds": args.timeout, "memory_limit_bytes": 2_000_000_000,
            "Shimura_identification_certified": False,
            "CM_mark_identifications_certified": False,
            "genus64_cover_constructed": False,
            "target_field_polynomial_obtained": False,
        }
        started = time.monotonic()
        command = [MAGMA, "-bn", "-l", "2000000000", str(script)]
        status, exit_code = "failed", None
        with log_path.open("w") as log:
            try:
                run = subprocess.run(command, cwd=ROOT, stdout=log,
                                     stderr=subprocess.STDOUT, timeout=args.timeout)
            except subprocess.TimeoutExpired:
                status = "timeout"
            else:
                exit_code = run.returncode
                status = "pass" if exit_code == 0 else "failed"
        output = log_path.read_text()
        if status == "pass" and (MARKER not in output or any(e in output for e in ERRORS)):
            status = "failed"
        report["job"] = {"command": command, "log": source(log_path),
                         "exit_code": exit_code, "status": status,
                         "wall_seconds": time.monotonic()-started}
        report["status"] = status
        report_path.write_text(json.dumps(report, indent=2)+"\n")
        print(status, f"{report['job']['wall_seconds']:.3f}s", flush=True)
        if status != "pass":
            print(output[-4000:], flush=True)
            raise SystemExit(1)
    output = log_path.read_text()
    if MARKER not in output or any(e in output for e in ERRORS):
        raise ValueError("invalid completion log")
    coefficients = [str(Fraction(s.strip())) for s in
                    field(output,"NONIC_POLYNOMIAL_COEFFICIENTS").strip("[] ").split(",")]
    assert len(coefficients) == 10 and coefficients[-1] == "1"
    order, identifier = map(int,field(output,"NONIC_GALOIS").split("|"))
    rr_dimension = int(field(output,"RR_DIMENSION_2B3_MINUS_B2_MOD31"))
    assert (order,identifier,rr_dimension) == (72,15,0)
    marks = json.loads((DATA/"cm_frame_marks.json").read_text())
    assert marks["ordinary_point_certificate"]["canonical_jet_rank"] == 16
    report.update({
        "status": "pass", "proof": "dembele/certificates/cm-frame-marks.md",
        "rational_point": {"primitive_coordinates": marks["rational_point"]["primitive_coordinates"],
                           "height": marks["rational_point"]["height"],
                           "ordinary_on_candidate_over_Q": True},
        "marked_divisors": {"closed_point_degrees": [1,17,9], "reduced_disjoint_over_Q": True,
                            "flat_reduced_disjoint_specialization_at_31": True,
                            "transposition_branch_support_candidate_degree": 18,
                            "three_cycle_branch_support_candidate_degree": 9},
        "nonic_residue_field": {
            "generator": "X15/X16 on B3", "polynomial_coefficients_ascending": coefficients,
            "Galois_group_order": order, "transitive_group": "9T15",
            "GaloisProof_passed": True, "structure": "(C3)^2 semidirect C8 = AGL(1,9)",
            "CM_class_field_identification_certified": False,
            "is_target_nonsolvable_field": False,
        },
        "simple_branch_relation": {
            "B2": "D17 + P32", "B3": "degree-nine closed point",
            "h0_2B3_minus_B2_mod31": 0, "h0_2B3_minus_B2_over_Q": 0,
            "B2_linearly_equivalent_to_2B3": False,
            "method": "residual ideal in |2K| modulo 31, then proper-flat semicontinuity",
            "excludes": "a rational function with divisor B2-2B3",
            "does_not_exclude": "other double covers or the required degree-three cover",
        },
    })
    report_path.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS: exact ordinary point, marked degrees 1/17/9, nonic group 9T15; cover and Shimura identification open.")


if __name__ == "__main__":
    main()
