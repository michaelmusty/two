"""D84: independently certify a subgroup of compatible thirds, with an error control."""
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


prior = module("ambiguity_prior", "277_cm_frame_rational_three_torsion.py")
jobs, helpers, checks = prior.jobs, prior.helpers, prior.checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1])
    args = parser.parse_args()
    label = "_".join(map(str, args.seeds))
    base = DATA / f"cm_frame_third_ambiguity_{label}"
    path = base.with_suffix(".json")
    if path.exists():
        record = json.loads(path.read_text()); checks.verify_records(record)
        assert record["status"] == "pass"
        print("PASS|278_EXISTING_AMBIGUITY", label)
        return
    sources, coordinates = [], []
    for seed in args.seeds:
        source = DATA / f"cm_frame_rational_three_torsion_{seed}.json"
        record = json.loads(source.read_text()); checks.verify_records(record)
        sources.append(source)
        if record["found_nonzero_compatible_three_torsion"]:
            coordinates.append(record["coordinates_in_V2"])
    assert coordinates
    input_path = Path(str(base)+"_input.m")
    input_path.write_text("torsion_coordinates := " + helpers.magma(coordinates) + ";\n")
    script = ROOT / "dembele/magma/278_cm_frame_third_ambiguity_check.m"
    records = []
    for control in (False, True):
        case = Path(str(base)+( "_control" if control else "_check"))
        runfile, jpath = Path(str(case)+"_run.m"), Path(str(case)+"_job.json")
        assert not jpath.exists(), "Archive unfinished attempts before rerunning."
        runfile.write_text(f'load {json.dumps(str(input_path))};\ncorrupt_torsion := {str(control).lower()};\nload {json.dumps(str(script))};\n')
        job = jobs.run_job(jobs.prior.magma_command(runfile), case.with_suffix(".out"), 180,
            "PASS|278_THIRD_AMBIGUITY", expected_failure="assert torsion_relation_ok;" if control else None)
        job["sources"] += [checks.source(p) for p in (Path(__file__), script, runfile, input_path,
            ROOT / "dembele/magma/170_cm_frame_cover_class_arithmetic.m",
            DATA / "cm_frame_cover_makdisi.m", DATA / "cm_frame_cover_third_check_input.m", *sources)]
        jpath.write_text(json.dumps(job, indent=2)+"\n")
        assert job["status"] == "pass", job["status"]
        records.append(jpath)
    output = Path(str(base)+"_check.out").read_text().replace("[*", "[").replace("*]", "]")
    rank = helpers.field(output, "VERIFIED_TORSION_RANK_LOWER_BOUND")
    thirds = helpers.field(output, "THIRD_COORDINATES")
    labels = helpers.field(output, "THIRD_LABELS")
    assert len(thirds) == len(labels) == 3**rank
    data = {"status": "pass", "milestone": "D84", "sources": [checks.source(p) for p in (Path(__file__), *records)],
            "rank_lower_bound": rank, "third_count_lower_bound": len(thirds),
            "third_labels": labels, "third_coordinates": thirds,
            "generator_coordinates": helpers.field(output, "GENERATOR_COORDINATES"),
            "independent_class_checks_passed": True, "wrong_torsion_rejected": True,
            "torsion_subgroup_complete": False, "class_number_assumed": False,
            "arithmetic_identification_certified": False}
    path.write_text(json.dumps(data, indent=2)+"\n")
    print("PASS|278_THIRD_AMBIGUITY_COLLECTED", rank, len(thirds))


if __name__ == "__main__":
    main()
