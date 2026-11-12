"""Record the D157 resumption and current storage; launch no computation.

Run through run_dyadic_capped.py after the fresh source-654 replay.
This is an operational observation, not a new mathematical certificate.
"""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = ROOT / "dembele/checkpoints/d157-resume-2026-10-15.json"
REPLAY = "dyadic_higher_pilot_timing_review_d157_resume_20261015_recheck01"
GIB = 1 << 30
SOURCES = {}


def source(path):
    path = Path(path).resolve()
    if str(path) not in SOURCES:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            while block := stream.read(1 << 20):
                digest.update(block)
        SOURCES[str(path)] = {"path": str(path), "sha256": digest.hexdigest()}
    return SOURCES[str(path)]


def read(stem):
    path = DATA / (stem + ".json")
    source(path)
    value = json.loads(path.read_text())
    assert value["status"] == "pass", path
    return value


def receipt(stem, args, metadata):
    row = read(stem + ".job")
    driver = ROOT / "dembele/pari/654_dyadic_higher_pilot_timing_review.py"
    assert row["driver"] == source(driver)
    assert row["command"] == ["python3", str(driver), *args]
    assert row["exit_code"] == 0 and 0 < row["wall_seconds"] <= 180
    assert row["timeout_seconds"] == 180 and row["timeout_terminates_process_group"]
    assert row["private_process_group"] > 0
    for ref in [row["log"], *row["sources"]]:
        assert source(ref["path"]) == ref, ref["path"]
    lines = Path(row["log"]["path"]).read_text().splitlines()
    assert [json.loads(line.split("|", 1)[1]) for line in lines
            if line.startswith("PHASE_METADATA|")] == [source(metadata)]
    assert "PASS|654_DYADIC_HIGHER_PILOT_TIMING_REVIEW" in lines
    return row


def main():
    assert __debug__ and not OUT.exists()
    tick = time.monotonic()
    source(__file__)
    thread_names = ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]
    assert os.environ.get("PYTHONDONTWRITEBYTECODE") == "1"
    assert all(os.environ.get(name) == "1" for name in thread_names)
    review_path = DATA / "dyadic_higher_pilot_timing_review_d157.json"
    completion_path = DATA / "dyadic_higher_pilot_timing_completion_d157.json"
    replay = receipt(REPLAY, ["--check"], review_path)
    receipt("dyadic_higher_pilot_timing_completion_d157_attempt01", ["--finish"], completion_path)
    review = read(review_path.stem)
    completion = read(completion_path.stem)
    assert completion["fixed_review"] == source(review_path)
    assert completion["full_sixteen_column_bank_precision_pi"] == 1600
    assert completion["actual_column2_precision_pi"] == completion["column0_precision_pi"] == 6400
    for key in ["report", "source_applicability_ledger"]:
        assert source(completion[key]["path"]) == completion[key]
    planning = read("dyadic_storage_timing_plan_d156")
    timing = read("dyadic_higher_pilot_timing_d157")
    for stem in ["dyadic_storage_timing_plan_d156", "dyadic_higher_pilot_timing_d157"]:
        assert source(DATA / (stem + ".json")) in review["sources"]

    checked_links = []
    for name in completion["entry_documents_updated"]:
        path = ROOT / name
        block = path.read_text().split("<!-- D157 higher pilot timing checkpoint -->", 1)[1]
        block = block.split("<!-- End D157 higher pilot timing checkpoint -->", 1)[0]
        links = re.findall(r"\]\(([^)]+)\)", block)
        assert len(links) == 4, name
        for link in links:
            target = (path.parent / link).resolve()
            assert target.is_file(), (name, link)
            checked_links.append({"document": name, "target": str(target)})
    assert len(checked_links) == 28
    locks = completion["owned_coordinator_locks_observed_free"]
    for name in locks:
        with (DATA / name).open("r") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(stream, fcntl.LOCK_UN)

    remaining = (14, 14, 16)
    stages = planning["stages"]
    required = (sum(count * stage["retained_allowance_per_column_bytes"]
                    for count, stage in zip(remaining, stages))
                + max(stage["active_extra_bytes"] for stage in stages) + 10 * GIB)
    assert required == review["remaining_free_bytes_including_reserve"] == 75002411056
    gate = ((required + GIB - 1) // GIB) * GIB
    assert gate == review["rounded_remaining_bank_free_gate_bytes"] == 70 * GIB
    jobs = sum(count * stage["column_jobs"] for count, stage in zip(remaining, stages))
    assert jobs == timing["remaining_full_route_job_count"] == 1022790
    candidate = stages[2]
    assert (candidate["seed"], candidate["target"], candidate["column_jobs"]) == (6400, 10480, 31419)
    pilot_required = candidate["retained_allowance_per_column_bytes"] + candidate["active_extra_bytes"] + 10 * GIB
    assert pilot_required == candidate["single_column_free_bytes_with_reserve"] == 13548388784
    pilot_gate = ((pilot_required + GIB - 1) // GIB) * GIB
    assert pilot_gate == 13 * GIB

    observed = datetime.now(timezone.utc).isoformat()
    usage = shutil.disk_usage(ROOT)
    device = ROOT.stat().st_dev
    volumes = [{"path": str(path), "resolved_path": str(path.resolve()),
                "same_device_as_workspace": path.stat().st_dev == device}
               for path in sorted(Path("/Volumes").iterdir())]
    result = {
        "kind": "operational_resumption_not_a_mathematical_certificate",
        "status": "pass", "checkpoint": "D157", "observed_utc": observed,
        "fresh_transitive_replay": source(DATA / (REPLAY + ".job.json")),
        "fresh_transitive_replay_wall_seconds": replay["wall_seconds"],
        "fixed_review": source(review_path), "completion": source(completion_path),
        "current_artifact_links_checked": checked_links,
        "owned_coordinator_locks_observed_free": locks,
        "process_table_observed": False,
        "full_bank_precision_pi": 1600, "columns_at_precision_6400": [0, 2],
        "filesystem_observation": {"path": str(ROOT), "total_bytes": usage.total,
            "used_bytes": usage.used, "free_bytes": usage.free,
            "workspace_device": device, "visible_volume_entries": volumes,
            "not_a_reservation": True},
        "previous_free_space_observation": timing["filesystem_observation"],
        "free_bytes_change_since_previous_observation": usage.free - timing["filesystem_observation"]["free_bytes"],
        "cause_of_free_space_change_not_investigated": True,
        "remaining_route": {"columns_by_target": dict(zip(["3200", "6400", "10480"], remaining)),
            "column_jobs": jobs, "required_free_bytes_including_10GiB_reserve": required,
            "rounded_free_gate_bytes": gate, "rounded_gate_shortfall_bytes": max(0, gate - usage.free),
            "capacity_gate_met_at_observation": usage.free >= gate,
            "conditional_active_days": review["remaining_active_days_scenarios"]},
        "unprepared_P10480_timing_candidate": {"seed_precision_pi": 6400,
            "target_precision_pi": 10480, "possible_seed_columns": [0, 2],
            "column_jobs": candidate["column_jobs"], "inventory": candidate["inventory"],
            "required_free_bytes_including_10GiB_reserve": pilot_required,
            "rounded_free_gate_bytes": pilot_gate,
            "headroom_above_rounded_gate_at_observation_bytes": usage.free - pilot_gate,
            "modeled_column_cycle_active_hours": [seconds / 3600 for seconds in candidate["modeled_column_seconds"]],
            "integrated_cost_still_unmeasured": True, "shared_review_allowances_excluded": True,
            "budget_inherited_from_D156_not_new_admission": True,
            "configuration_created": False, "production_store_created": False,
            "independent_audit_and_review_adaptation_still_required": True,
            "launch_admitted": False},
        "full_bank_and_all_further_production_pauses_retained": True,
        "new_harmonic_moments_computed": False, "production_coordinator_launched": False,
        "frozen_files_deleted_or_relocated": False, "alternate_destination_selected": False,
        "candidate_identification_proved": False, "field_polynomial_constructed": False,
        "maximum_mathematical_workers": 3, "per_job_timeout_seconds": 180,
        "per_worker_or_store_limit_bytes": 2 * GIB, "aggregate_limit_bytes": 6 * GIB,
        "thread_limits": {name: os.environ[name] for name in thread_names},
        "next_unused_numbered_source": 655,
        "sources": sorted(SOURCES.values(), key=lambda ref: ref["path"]),
        "wall_seconds": time.monotonic() - tick,
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024),
    }
    assert result["peak_rss_bytes"] <= 2 * GIB
    with OUT.open("x") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print("PHASE_METADATA|" + json.dumps(source(OUT)), flush=True)
    print("PASS|D157_RESUME_PREFLIGHT", flush=True)


if __name__ == "__main__":
    main()
