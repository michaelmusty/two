"""Run, reproduce or collect the exact D72 31-adic lift certificates.

Default checks the saved lift in Magma and runs a highest-digit corruption
control. --lift first rebuilds support algebras and all requested digits.
The result is an equation modulo 31^n, not a number-field reconstruction.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"
MAGMA = "/Applications/Magma/magma"
SAGE = "/usr/local/bin/sage"
ERRORS = ("Runtime error", "User error", "Assertion failed", "Error:", "Traceback (most recent call last)")


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def verify_sources(items):
    for item in items:
        if source(item["path"]) != item:
            raise ValueError(f"changed source or artifact: {item['path']}")


def run_job(command,log_path,timeout,marker,env=None,expected_failure=None):
    started = time.monotonic()
    status,exit_code = "failed",None
    with log_path.open("w") as log:
        try:
            run = subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,
                                 timeout=timeout,env=env)
        except subprocess.TimeoutExpired:
            status = "timeout"
        else:
            exit_code = run.returncode
            output = log_path.read_text()
            if expected_failure is None:
                if exit_code == 0 and marker in output and not any(e in output for e in ERRORS):
                    status = "pass"
            elif exit_code != 0 and expected_failure in output and "Assertion failed" in output and marker not in output:
                status = "pass"
    job = {"command": command, "status": status, "exit_code": exit_code,
           "wall_seconds": time.monotonic()-started, "timeout_seconds": timeout,
           "log": source(log_path)}
    if command[0] == MAGMA:
        job["memory_limit_bytes"] = 2_000_000_000
    return job


def magma_command(path):
    return [MAGMA,"-bn","-l","2000000000",str(path)]


def write_magma_data(lift):
    lines = ["// D72: exact finite-precision lift; generated from the Sage JSON."]
    for name,key in (("lift_modulus","modulus"),("lift_numerator","numerator_coefficients"),
                     ("lift_denominator","denominator_coefficients"),("lift_point_jets","point_jets")):
        lines.append(f"{name} := {lift[key]};")
    lines.append("lift_components := [*")
    for i,c in enumerate(lift["components"]):
        vals = [json.dumps(c["label"]),str(c["degree"]),str(c["etale_modulus"]),
                str(c["coordinates"]),str(c["tangent"]),str(c.get("second_jet_mod31",[]))]
        lines.append("<"+",".join(vals)+">"+("," if i+1<len(lift["components"]) else ""))
    lines.append("*];")
    path = DATA/"cm_frame_resolvent_lift.m"
    path.write_text("\n".join(lines)+"\n")
    return path


def check_stages(lift):
    original = json.loads((DATA/"cm_frame_resolvent.json").read_text())
    previous = None
    stages = []
    for digits in range(2,lift["precision_digits"]+1):
        path = DATA/f"cm_frame_resolvent_lift_{digits}.json"
        stage = json.loads(path.read_text())
        verify_sources(stage["sources"])
        assert stage["modulus"] == 31**digits and stage["precision_digits"] == digits
        assert stage["status"] == "pass"
        assert stage["numerator_linear_system"]["rank"] == 32
        assert stage["denominator_linear_system"]["rank"] == 44
        smaller = original if previous is None else previous
        modulus = 31**(digits-1)
        for key in ("numerator_coefficients","denominator_coefficients"):
            assert [c%modulus for c in stage[key]] == smaller[key]
        if previous is not None:
            old = {(c["label"],tuple(c["etale_modulus"])):c for c in previous["components"]}
            for c in stage["components"]:
                oldc = old[c["label"],tuple(c["etale_modulus"])]
                for key in ("coordinates","tangent"):
                    assert [[v%modulus for v in row] for row in c[key]] == oldc[key]
            assert [[v%modulus for v in row] for row in stage["point_jets"]] == previous["point_jets"]
        stages.append(source(path))
        previous = stage
    assert previous == lift
    return stages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--lift",action="store_true")
    modes.add_argument("--collect-only",action="store_true")
    parser.add_argument("--calibrate",action="store_true",
                        help="recompute the exact rational numerator and its height before checking")
    parser.add_argument("--digits",type=int,default=8)
    parser.add_argument("--timeout",type=int,default=120)
    parser.add_argument("--lift-timeout",type=int,default=240)
    args = parser.parse_args()
    if not 2 <= args.digits <= 32 or min(args.timeout,args.lift_timeout) < 1:
        parser.error("positive timeouts and between 2 and 32 digits required")
    if args.collect_only and args.calibrate:
        parser.error("--collect-only cannot recompute the numerator")
    report_path = DATA/"cm_frame_resolvent_lift_check.json"
    jobs_path = DATA/"cm_frame_resolvent_lift_jobs.json"
    if args.lift:
        support_script = ROOT/"dembele/magma/123_cm_frame_lift_supports.m"
        solver = ROOT/"dembele/pari/124_cm_frame_resolvent_lift.py"
        support = run_job(magma_command(support_script),DATA/"cm_frame_lift_supports.out",
                          args.timeout,"PASS|123_CM_FRAME_LIFT_SUPPORTS")
        support["sources"] = [source(p) for p in (
            support_script,DATA/"cm_frame_curve_candidate.m",DATA/"cm_frame_marks.m",
            DATA/"cm_frame_resolvent.m",DATA/"cm_frame_resolvent_check.json")]
        jobs = {"support_job": support}
        jobs_path.write_text(json.dumps(jobs,indent=2)+"\n")
        if support["status"] != "pass":
            raise RuntimeError(f"support job {support['status']}")
        env = os.environ.copy()
        env["DOT_SAGE"] = "/private/tmp/dembele-d72-sage"
        env["OPENBLAS_NUM_THREADS"] = "1"
        solver_job = run_job([SAGE,"-python",str(solver),"--digits",str(args.digits)],
                             DATA/"cm_frame_resolvent_lift.out",args.lift_timeout,
                             f"PASS|124_CM_FRAME_RESOLVENT_LIFT {args.digits} ",env=env)
        solver_job["sources"] = [source(solver),source(DATA/"cm_frame_lift_supports.out")]
        solver_job["environment"] = {k:env[k] for k in ("DOT_SAGE","OPENBLAS_NUM_THREADS")}
        jobs["solver_job"] = solver_job
        jobs_path.write_text(json.dumps(jobs,indent=2)+"\n")
        if solver_job["status"] != "pass":
            raise RuntimeError(f"lift job {solver_job['status']}")
    jobs = json.loads(jobs_path.read_text())
    for job in jobs.values():
        assert job["status"] == "pass"
        verify_sources(job["sources"]+[job["log"]])
    lift_path = DATA/"cm_frame_resolvent_lift.json"
    lift = json.loads(lift_path.read_text())
    stages = check_stages(lift)
    calibration_path = DATA/"cm_frame_lift_numerator_job.json"
    if args.lift or args.calibrate:
        calibration_script = ROOT/"dembele/pari/126_cm_frame_lift_numerator.py"
        env = os.environ.copy()
        env["DOT_SAGE"] = "/private/tmp/dembele-d72-sage"
        env["OPENBLAS_NUM_THREADS"] = "1"
        calibration = run_job([SAGE,"-python",str(calibration_script)],
                              DATA/"cm_frame_lift_numerator.out",args.timeout,
                              "PASS|126_CM_FRAME_LIFT_NUMERATOR",env=env)
        calibration["sources"] = [source(calibration_script)]
        if calibration["status"] == "pass":
            calibration["sources"].append(source(DATA/"cm_frame_lift_numerator.json"))
        calibration["environment"] = {k:env[k] for k in ("DOT_SAGE","OPENBLAS_NUM_THREADS")}
        calibration_path.write_text(json.dumps(calibration,indent=2)+"\n")
        if calibration["status"] != "pass":
            raise RuntimeError(f"rational numerator job {calibration['status']}")
    calibration = json.loads(calibration_path.read_text())
    verify_sources(calibration["sources"]+[calibration["log"]])
    numerator_report = json.loads((DATA/"cm_frame_lift_numerator.json").read_text())
    verify_sources(numerator_report["sources"])
    assert calibration["status"] == numerator_report["status"] == "pass"
    assert numerator_report["agrees_with_lift_modulus"] == lift["modulus"]
    script = ROOT/"dembele/magma/125_cm_frame_resolvent_lift_check.m"
    if args.collect_only:
        report = json.loads(report_path.read_text())
        verify_sources(report["sources"]+report["stage_artifacts"]+
                       [report["job"]["log"],report["negative_control"]["log"]])
        assert report["job"]["status"] == report["negative_control"]["status"] == "pass"
    else:
        data_path = write_magma_data(lift)
        log_path = DATA/"cm_frame_resolvent_lift_check.out"
        job = run_job(magma_command(script),log_path,args.timeout,"PASS|125_CM_FRAME_RESOLVENT_LIFT_CHECK")
        report = {"status": job["status"], "milestone": "D72", "date": "2026-09-18",
                  "job": job, "stage_artifacts": stages,
                  "sources": [source(p) for p in (
                      __file__,script,data_path,lift_path,jobs_path,
                      DATA/"cm_frame_curve_candidate.m",DATA/"cm_frame_marks.m",
                      DATA/"cm_frame_resolvent.m",DATA/"cm_frame_curve_verification.json",
                      DATA/"cm_frame_marks_check.json",DATA/"cm_frame_resolvent_check.json",
                      calibration_path,DATA/"cm_frame_lift_numerator.json")]}
        report_path.write_text(json.dumps(report,indent=2)+"\n")
        print("certificate",job["status"],f"{job['wall_seconds']:.3f}s",flush=True)
        if job["status"] != "pass":
            print(log_path.read_text()[-4000:])
            raise SystemExit(1)
        # Change only the newest p-adic digit; all lower-precision data agree.
        needle = 'load "dembele/data/computed/cm_frame_resolvent_lift.m";'
        control_source = script.read_text().replace(
            needle,needle+"\nlift_numerator[1] +:= lift_modulus div 31;")
        assert control_source != script.read_text()
        control = DATA/"cm_frame_resolvent_lift_negative_control.m"
        control.write_text(control_source)
        negative = run_job(magma_command(control),control.with_suffix(".out"),args.timeout,
                           "PASS|125_CM_FRAME_RESOLVENT_LIFT_CHECK",
                           expected_failure="assert nv eq 0 and nd0 ne 0;")
        negative["mutation"] = "add 31^(digits-1) to numerator coefficient of X1^2"
        negative["lower_precision_preserved"] = True
        report["negative_control"] = negative
        report["sources"].append(source(control))
        if negative["status"] != "pass":
            report["status"] = "failed"
            report_path.write_text(json.dumps(report,indent=2)+"\n")
            raise RuntimeError("corruption control was not rejected as expected")
    output = Path(report["job"]["log"]["path"]).read_text()
    assert "PASS|125_CM_FRAME_RESOLVENT_LIFT_CHECK" in output
    assert not any(e in output for e in ERRORS)
    assert int(re.search(r"^MODULUS\|(\d+)$",output,re.M).group(1)) == lift["modulus"]
    components = re.findall(r"^COMPONENT_PASS\|(D17|E|F)\|(\d+)$",output,re.M)
    degrees = {label:sum(int(d) for l,d in components if l==label) for label in ("D17","E","F")}
    assert degrees == {"D17":17,"E":16,"F":28}
    report.update({
        "status": "pass", "precision_digits": lift["precision_digits"], "modulus": lift["modulus"],
        "divisor_identity": "D17 + 15*P32 - 2*E", "component_degrees": degrees,
        "half_line_bundle_degree": 9, "branch_degree": 18,
        "verified_reduction_compatibility_at_each_digit": True,
        "characteristic_zero_equation_obtained": False,
        "Shimura_identification_certified": False,
        "genus64_cover_constructed": False,"target_field_polynomial_obtained": False,
    })
    report_path.write_text(json.dumps(report,indent=2)+"\n")
    print(f"PASS: divisor identity modulo 31^{lift['precision_digits']} = {lift['modulus']}; highest-digit corruption rejected.")


if __name__ == "__main__":
    main()
