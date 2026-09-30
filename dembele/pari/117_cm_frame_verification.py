"""Run or collect the exact D69 smoothness and point-count certificates.

Uses Python's standard library and local Magma. Each job has its own
180-second timeout and 2 GB memory cap. No analytic relation or Shimura
identification is certified by these algebraic checks.
"""
import argparse
import ast
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
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--collect-only", action="store_true")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("positive timeout required")
    smooth_script = ROOT / "dembele/magma/117_cm_frame_smoothness.m"
    counts_script = ROOT / "dembele/magma/118_cm_frame_point_counts.m"
    jobs = [("smoothness", smooth_script, "117_CM_FRAME_SMOOTHNESS")]
    for degree in (1, 2):
        launcher = DATA / f"cm_frame_points31_degree{degree}.m"
        content = (f"extension_degree := {degree};\n"
                   'load "dembele/magma/118_cm_frame_point_counts.m";\n')
        if args.collect_only:
            if launcher.read_text() != content:
                raise ValueError(f"launcher mismatch: {launcher}")
        else:
            launcher.write_text(content)
        jobs.append((f"points31_degree{degree}", launcher, "118_CM_FRAME_POINT_COUNTS"))
    report_path = DATA / "cm_frame_curve_verification.json"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        for item in report["sources"]:
            if source(item["path"]) != item:
                raise ValueError(f"changed input: {item['path']}")
        for job in report["jobs"]:
            if source(job["log"]["path"]) != job["log"]:
                raise ValueError(f"changed log: {job['log']['path']}")
    else:
        report = {
            "status": "running", "milestone": "D69", "date": "2026-09-18",
            "sources": [source(p) for p in (
                __file__, smooth_script, counts_script,
                DATA / "cm_frame_curve_candidate.m",
                DATA / "cm_frame_curve_candidate.json",
                DATA / "cm_frame_curve_check.json",
                DATA / "levelraise_p2k_charpolys.m",
                DATA / "f16_steinberg.out",
            )],
            "timeout_seconds_per_job": args.timeout,
            "memory_limit_bytes_per_job": 2_000_000_000,
            "jobs": [], "Shimura_identification_certified": False,
            "target_field_polynomial_obtained": False,
        }
    outputs = {}
    for name, script, marker in jobs:
        log_path = DATA / f"cm_frame_{name}.out"
        if args.collect_only:
            output = log_path.read_text()
        else:
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
            if status == "pass" and (f"PASS|{marker}" not in output
                                     or any(error in output for error in ERRORS)):
                status = "failed"
            report["jobs"].append({
                "name": name, "script": source(script), "log": source(log_path),
                "command": command, "exit_code": exit_code, "status": status,
                "wall_seconds": time.monotonic()-started,
            })
            report["status"] = "running" if status == "pass" else status
            report_path.write_text(json.dumps(report, indent=2)+"\n")
            print(name, status, f"{report['jobs'][-1]['wall_seconds']:.3f}s", flush=True)
            if status != "pass":
                print(output[-3000:], flush=True)
                raise SystemExit(1)
        if f"PASS|{marker}" not in output or any(error in output for error in ERRORS):
            raise ValueError(f"invalid completion log: {name}")
        outputs[name] = output

    smooth = outputs["smoothness"]
    coefficients = ast.literal_eval(field(smooth, "DISCRIMINANT_COEFFICIENTS"))
    assert len(coefficients) == 91 and coefficients[0] == 1 and coefficients[-1] == 16
    counts = []
    for degree in (1, 2):
        output = outputs[f"points31_degree{degree}"]
        fibers = []
        for line in output.splitlines():
            if line.startswith("FIBER|"):
                _, value, size, count = line.split("|")
                fibers.append({"base_value_power_coordinates": ast.literal_eval(value),
                               "frobenius_orbit_size": int(size), "point_count": int(count)})
        infinity = int(field(output, "FIBER_INFINITY"))
        saved_degree, count = map(int, field(output, "POINT_COUNT").split("|"))
        assert saved_degree == degree
        assert sum(f["frobenius_orbit_size"] for f in fibers) == 31**degree
        assert sum(f["frobenius_orbit_size"]*f["point_count"] for f in fibers)+infinity == count
        expected = list(map(int, field(output, "EXPECTED_POINT_COUNTS").split("|")))
        assert count == expected[degree-1]
        counts.append({"extension_degree": degree, "field_cardinality": 31**degree,
                       "curve_point_count": count, "Hecke_prediction": expected[degree-1],
                       "base_fiber_orbits": fibers, "infinity_point_count": infinity})
    report.update({
        "status": "pass",
        "proof": "dembele/certificates/cm-frame-verification.md",
        "smoothness": {
            "method": "finite free degree-30 projection and squarefree trace discriminants on both charts",
            "free_basis_degrees": ast.literal_eval(field(smooth, "BASIS_DEGREES")),
            "discriminant_modulus": 31, "discriminant_coefficients_ascending": coefficients,
            "discriminant_factor_degrees": ast.literal_eval(field(smooth, "DISCRIMINANT_FACTOR_DEGREES")),
            "infinity_trace_determinant": int(field(smooth, "INFINITY_DISCRIMINANT")),
            "rational_point_mod31": ast.literal_eval(field(smooth, "RATIONAL_POINT_MOD31")),
            "smooth_over_F31": True, "smooth_over_Q": True,
            "geometrically_integral_over_Q_and_F31": True,
            "genus": 16, "canonical_embedding": True,
        },
        "point_counts": counts,
        "point_count_scope": "two counts at the single split prime 31; not a full Euler factor or an identification proof",
        "Hecke_trace_polynomial_coefficients_ascending": ast.literal_eval(
            field(outputs["points31_degree1"], "HECKE_TRACE_POLYNOMIAL")),
    })
    report_path.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS: smooth canonical genus-16 curve; point counts 50 and 1400 match; Shimura identification open.", flush=True)


if __name__ == "__main__":
    main()
