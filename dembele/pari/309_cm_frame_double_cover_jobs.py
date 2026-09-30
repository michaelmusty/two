"""D87: bounded saved-bank diagnostics, using the existing process-group runner."""
import argparse
import importlib
import json
import os
from pathlib import Path

runner = importlib.import_module("272_cm_frame_bounded_jobs")
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"
PROGRAM = ROOT/"dembele/pari/308_cm_frame_double_cover_paths.py"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", choices=["current", "previous"], required=True)
    parser.add_argument("--build-cache", action="store_true")
    parser.add_argument("--first", type=int, default=0)
    parser.add_argument("--stop", type=int, default=91)
    parser.add_argument("--steps", type=int, default=128)
    parser.add_argument("--bend", default="0")
    args = parser.parse_args()
    command = [runner.SAGE, "-python", str(PROGRAM), "--bank", args.bank]
    if args.build_cache:
        name = f"cm_frame_double_cover_polynomials_{args.bank}_d87_build"
        command += ["--build-cache"]
        marker = '"status": "numerical polynomial cache checked"'
    else:
        assert 0 <= args.first < args.stop <= 273 and args.steps >= 16 and args.steps % 4 == 0
        bend = str(float(args.bend)).replace(".", "p").replace("-", "m")
        name = f"cm_frame_double_cover_paths_{args.bank}_{args.first}_{args.stop}_{args.steps}_b{bend}_d87"
        command += ["--first", str(args.first), "--stop", str(args.stop), "--steps", str(args.steps),
                    "--bend", args.bend, "--output", str(DATA/(name+".json"))]
        marker = "PASS|308_SAMPLED_PATHS"
    log, receipt = DATA/(name+".out"), DATA/(name+"_job.json")
    assert not log.exists() and not receipt.exists(), "preserve previous attempts"
    job = runner.run_job(command, log, 180, marker,
                         env=dict(os.environ, DOT_SAGE="/private/tmp/dembele_pointed_recognition_sage",
                                  OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"))
    job["sources"] += [runner.source(Path(__file__)), runner.source(PROGRAM)]
    receipt.write_text(json.dumps(job, indent=2)+"\n")
    print(json.dumps({k:job[k] for k in ("status", "wall_seconds", "exit_code", "log")}), flush=True)
    assert job["status"] == "pass", "inspect the preserved attempt"


if __name__ == "__main__":
    main()
