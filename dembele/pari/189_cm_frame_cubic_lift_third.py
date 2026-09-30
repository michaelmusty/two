"""Compute the actual third modulo 961 in bounded, resumable scalar chunks."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


old = module("lift_third_old", ROOT / "dembele/pari/172_cm_frame_cover_third.py")
helpers, jobs, checks = old.helpers, old.jobs, old.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collect-only", action="store_true")
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()
    result_path = DATA / "cm_frame_cubic_lift_third.json"
    if args.collect_only:
        report = json.loads(result_path.read_text())
        checks.verify_records(report)
        assert report["three_division_computed"]
        print("PASS|189_CM_FRAME_CUBIC_LIFT_THIRD_PROVENANCE")
        return
    pilot_path = DATA / "cm_frame_cubic_lift_pilot_job.json"
    pilot = checks.read_job(pilot_path, "PASS|188_CM_FRAME_CUBIC_LIFT_PILOT")
    delta = helpers.field(Path(pilot["log"]["path"]).read_text(), "LIFT_DELTA_COORDINATES")
    old_report = json.loads((DATA / "cm_frame_cover_third.json").read_text())
    scalar = 31*old_report["proposed_scalar"]+10
    assert 3*scalar+1 == 31*(3*old_report["proposed_scalar"]+1)
    chain = old.addflip_chain(scalar)
    saved_indices, saved_coordinates = [1], [delta]
    script = ROOT / "dembele/magma/190_cm_frame_cubic_lift_third.m"
    chunk_jobs = []
    for start in range(2, len(chain)+1, 40):
        end = min(start+39, len(chain))
        keep = sorted({1, end} | {i for item in chain[end:] for i in item[1:] if 0 < i <= end})
        stem = DATA / f"cm_frame_cubic_lift_third_{end:03d}"
        job_path = Path(str(stem)+"_job.json")
        if job_path.exists() and not args.rebuild:
            job = checks.read_job(job_path, "PASS|190_CM_FRAME_CUBIC_LIFT_THIRD")
        else:
            input_path = Path(str(stem)+"_input.m")
            inputs = {"chain": chain, "chain_start": start, "chain_end": end,
                      "saved_indices": saved_indices, "saved_coordinates": saved_coordinates,
                      "keep_indices": keep}
            input_path.write_text("// D81 immutable scalar chunk input.\n"+
                "\n".join(f"lift_{key} := {helpers.magma(value)};" for key, value in inputs.items())+"\n")
            wrapper = Path(str(stem)+"_run.m")
            wrapper.write_text(f'SetQuitOnError(true);\nload "{input_path.relative_to(ROOT)}";\n'
                               f'load "{script.relative_to(ROOT)}";\n')
            job = jobs.run_job(jobs.magma_command(wrapper), stem.with_suffix(".out"), 180,
                               "PASS|190_CM_FRAME_CUBIC_LIFT_THIRD")
            sources = [Path(__file__), script, input_path, wrapper, pilot_path,
                       ROOT / "dembele/magma/186_cm_frame_cubic_lift_arithmetic.m",
                       ROOT / "dembele/magma/187_cm_frame_cubic_lift_model.m",
                       ROOT / "dembele/pari/172_cm_frame_cover_third.py",
                       ROOT / "dembele/pari/125_cm_frame_resolvent_lift_check.py"]+chunk_jobs[-1:]
            job["sources"] = [checks.source(p) for p in sources]
            job["chain_range"] = [start, end]
            job_path.write_text(json.dumps(job, indent=2)+"\n")
            if job["status"] != "pass":
                raise RuntimeError(f"scalar chunk {start}..{end}: {job['status']}")
        output = Path(job["log"]["path"]).read_text()
        saved_indices = helpers.field(output, "CHECKPOINT_INDICES")
        saved_coordinates = helpers.field(output, "CHECKPOINT_COORDINATES")
        assert saved_indices == keep
        chunk_jobs.append(job_path)
        print("SCALAR_CHUNK", start, end, "PASS", round(job["wall_seconds"], 3), flush=True)
    assert "PASS|THIRD_RELATION_AND_SYMMETRIES_MOD961" in output
    coords = saved_coordinates[saved_indices.index(len(chain))]
    mpath = DATA / "cm_frame_cubic_lift_third.m"
    mpath.write_text("// D81: verified class third modulo 961; entries c0+961*c1.\n"+
        f"lift_third_coordinates := {helpers.magma(coords)};\n"+
        f"lift_delta_coordinates := {helpers.magma(delta)};\n")
    report = {"status": "pass", "milestone": "D81", "date": "2026-09-22",
              "sources": [checks.source(p) for p in [Path(__file__), *chunk_jobs,
                          DATA / "cm_frame_cover_third.json"]],
              "magma_artifact": checks.source(mpath), "modulus": 961,
              "scalar": scalar, "addflip_steps": len(chain)-1,
              "three_division_computed": True, "frobenius_fixed": True,
              "antiinvariant": True, "class_number_assumed": False,
              "candidate_coordinates": coords, "delta_coordinates": delta}
    result_path.write_text(json.dumps(report, indent=2)+"\n")
    print("PASS|189_CM_FRAME_CUBIC_LIFT_THIRD")


if __name__ == "__main__":
    main()
