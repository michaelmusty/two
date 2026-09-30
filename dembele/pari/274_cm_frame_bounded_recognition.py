"""Run existing recognition workers with process-group timeouts and immutable reuse.

Use this entry point for future Sage recognition jobs; the earlier frozen
CLIs call a runner that can leave descendants alive on timeout.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "dembele/pari" / filename)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


runner = module("bounded_recognition_runner", "272_cm_frame_bounded_jobs.py")
prior = module("bounded_recognition_prior", "201_cm_frame_cubic_precision.py")
checks = prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--program", choices=("coefficients", "joint", "height"), required=True)
    parser.add_argument("--digits", type=int, default=64)
    parser.add_argument("--train", type=int, default=60)
    parser.add_argument("--root-index", type=int, choices=range(8), default=0)
    args = parser.parse_args(); n, train, index = args.digits, args.train, args.root_index
    assert n >= 8 and (args.program == "coefficients" or 1 < train < n)
    if args.program == "coefficients":
        filename = "258_cm_frame_cubic_adjoint_recognition.py"
        arguments = ["--digits", str(n), "--worker"]
        base = DATA / f"cm_frame_cubic_adjoint_{n}_recognition"
        marker = "PASS|232_CM_FRAME_CUBIC_ADJOINT_RECOGNITION"
    elif args.program == "joint":
        filename = "259_cm_frame_cubic_adjoint_joint_recognition.py"
        arguments = ["--digits", str(n), "--train", str(train), "--root-index", str(index), "--worker"]
        base = DATA / f"cm_frame_cubic_adjoint_joint_{n}_{train}_{index}"
        marker = "PASS|259_CM_FRAME_CUBIC_ADJOINT_JOINT_RECOGNITION"
    else:
        assert n == 64, "The current dual-height worker is specialized to the 64-digit data."
        filename = "271_cm_frame_cubic_dual_height.py"
        arguments = ["--train", str(train), "--root-index", str(index), "--worker"]
        base = DATA / f"cm_frame_cubic_adjoint_dual_height_64_{train}_{index}"
        marker = "PASS|271_DUAL_RECOGNITION_HEIGHT"
    result, jpath = base.with_suffix(".json"), Path(str(base)+"_job.json")
    if result.exists() or jpath.exists():
        assert result.exists() and jpath.exists(), "Archive the incomplete attempt before a new run."
        checks.read_job(jpath, marker)
        record = json.loads(result.read_text()); checks.verify_records(record)
        assert record["status"] == "pass"
        assert any(item.get("path") == str(jpath.resolve()) for item in record["sources"])
        print("PASS|274_EXISTING_RECOGNITION_VERIFIED", base.name, flush=True)
        return
    source = ROOT / "dembele/pari" / filename
    cache = Path("/private/tmp/dembele_pointed_recognition_sage"); cache.mkdir(exist_ok=True)
    job = runner.run_job([runner.SAGE, "-python", str(source), *arguments], base.with_suffix(".out"),
        180, marker, env=dict(os.environ, DOT_SAGE=str(cache)))
    job["sources"] += [checks.source(Path(__file__)), checks.source(source)]
    jpath.write_text(json.dumps(job, indent=2)+"\n")
    if job["status"] != "pass": raise RuntimeError(f"{base.name}: {job['status']}")
    record = json.loads(result.read_text())
    record["sources"] += [checks.source(Path(__file__)), checks.source(jpath)]
    result.write_text(json.dumps(record, indent=2)+"\n"); checks.verify_records(record)
    print("PASS|274_BOUNDED_RECOGNITION", base.name, round(job["wall_seconds"], 3), flush=True)


if __name__ == "__main__":
    main()
