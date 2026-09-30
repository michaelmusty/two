"""D84: bounded search and immutable collection of actual compatible 3-torsion."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "dembele/pari" / filename)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj


jobs = module("three_torsion_jobs", "272_cm_frame_bounded_jobs.py")
prior = module("three_torsion_prior", "172_cm_frame_cover_third.py")
helpers, checks = prior.helpers, prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    base = DATA / f"cm_frame_rational_three_torsion_{args.seed}"
    path, jpath = base.with_suffix(".json"), Path(str(base)+"_job.json")
    if path.exists() or jpath.exists():
        assert path.exists() and jpath.exists(), "Archive incomplete attempts before rerunning."
        report = json.loads(path.read_text()); checks.verify_records(report)
        checks.read_job(jpath, "PASS|276_RATIONAL_THREE_TORSION")
        print("PASS|277_EXISTING_TORSION", args.seed)
        return
    source = DATA / "cm_frame_cover_third.json"
    old = json.loads(source.read_text()); checks.verify_records(old)
    m = old["heuristic_coprime_cofactor"]
    assert m % 3 != 0
    chain = prior.addflip_chain(m)
    script = ROOT / "dembele/magma/276_cm_frame_rational_three_torsion.m"
    runfile = Path(str(base)+"_run.m")
    runfile.write_text(f"search_seed := {args.seed};\nsearch_chain := {helpers.magma(chain)};\nload {json.dumps(str(script))};\n")
    job = jobs.run_job(jobs.prior.magma_command(runfile), base.with_suffix(".out"), 180,
                       "PASS|276_RATIONAL_THREE_TORSION")
    job["sources"] += [checks.source(p) for p in (Path(__file__), script, runfile, source,
        ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m", DATA / "cm_frame_cover_makdisi.m")]
    jpath.write_text(json.dumps(job, indent=2)+"\n")
    assert job["status"] == "pass", job["status"]
    output = base.with_suffix(".out").read_text().replace("true", "True").replace("false", "False")
    found = helpers.field(output, "NONZERO_THREE_TORSION_FOUND")
    record = {"status": "pass", "milestone": "D84", "seed": args.seed,
              "sources": [checks.source(p) for p in (Path(__file__), jpath, source)],
              "heuristic_cofactor": m, "class_number_assumed": False,
              "found_nonzero_compatible_three_torsion": found,
              "scalar_image_killed_by_one_three_nine": helpers.field(output, "SCALAR_IMAGE_KILLED_BY_ONE_THREE_NINE"),
              "seed_divisor_indices": helpers.field(output, "SEED_DIVISOR_INDICES"),
              "coordinates_in_V2": helpers.field(output, "TORSION_COORDINATES") if found else None,
              "torsion_subgroup_complete": False}
    path.write_text(json.dumps(record, indent=2)+"\n")
    print("PASS|277_RATIONAL_THREE_TORSION", args.seed, found, round(job["wall_seconds"], 3))


if __name__ == "__main__":
    main()
