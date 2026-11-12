"""Bounded operational check after the user's disk cleanup; no production.

The source-654 replay authenticates the mathematical checkpoint. This
check also loads the production libraries and records current capacity.
"""
import ctypes
from datetime import datetime, timezone
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import re
import resource
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
OUT = ROOT / "dembele/checkpoints/d157-cleanup-check-2026-10-16.json"
REPLAY = "dyadic_higher_pilot_timing_review_d157_cleanup_20261016_recheck01"
GIB = 1 << 30


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


prior = module(ROOT / "dembele/checkpoints/d157_resume_20261015.py", "cleanup_observation_helpers")
source, read, receipt = prior.source, prior.read, prior.receipt


def main():
    assert __debug__ and not OUT.exists()
    start = time.monotonic()
    source(__file__)
    source(prior.__file__)
    threads = ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
               "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]
    assert os.environ.get("PYTHONDONTWRITEBYTECODE") == "1"
    assert all(os.environ.get(key) == "1" for key in threads)
    review_path = DATA / "dyadic_higher_pilot_timing_review_d157.json"
    completion_path = DATA / "dyadic_higher_pilot_timing_completion_d157.json"
    replay = receipt(REPLAY, ["--check"], review_path)
    receipt("dyadic_higher_pilot_timing_completion_d157_attempt01", ["--finish"], completion_path)
    review = read(review_path.stem)
    completion = read(completion_path.stem)
    assert completion["fixed_review"] == source(review_path)

    # Preserve and authenticate yesterday's operational record as history.
    old_path = ROOT / "dembele/checkpoints/d157-resume-2026-10-15.json"
    old_receipt = read("dyadic_resume_preflight_d157_20261015_attempt01.job")
    for ref in [old_receipt["driver"], old_receipt["log"], *old_receipt["sources"]]:
        assert source(ref["path"]) == ref
    old_lines = Path(old_receipt["log"]["path"]).read_text().splitlines()
    assert [json.loads(line.split("|", 1)[1]) for line in old_lines
            if line.startswith("PHASE_METADATA|")] == [source(old_path)]
    assert "PASS|D157_RESUME_PREFLIGHT" in old_lines
    old = json.loads(old_path.read_text())
    for ref in old["sources"]:
        assert source(ref["path"]) == ref

    # Importing the engine loads its GMP wrapper but does not open a store.
    engine = module(ROOT / "dembele/pari/554_dyadic_resumable_staged_production.py", "cleanup_production_import")
    bridge = read("dyadic_higher_pilot_seed_bridge_d156")
    known = {ref["path"]: ref for ref in bridge["sources"]}
    dependencies = [source(path) for path in sorted(engine.immutable_dependencies())]
    assert all(known[ref["path"]] == ref for ref in dependencies)
    native = []
    for filename, symbol in [
        ("dyadic_block_kernel_d121.dylib", "dembele_block_mul"),
        ("dyadic_polynomial_kernel_d122.dylib", "dembele_poly_mul"),
        ("dyadic_adaptive_polynomial_kernel_d124.dylib", "dembele_adaptive_poly_mul"),
    ]:
        path = DATA / filename
        assert source(path) == known[str(path)]
        library = ctypes.CDLL(str(path))
        assert getattr(library, symbol)
        native.append({"library": source(path), "exported_symbol_loaded": symbol})

    deleted = subprocess.run(["git", "ls-files", "--deleted", "-z"], cwd=ROOT,
                             check=True, capture_output=True, timeout=15).stdout.decode().split("\0")
    deleted = sorted(path for path in deleted if path)
    store = DATA / "dyadic_rowjournal_P6400_col00_d132"
    expected = sorted(str((store / name).relative_to(ROOT))
                      for name in ["WORKSPACE.bin", "aux_ready009.bin"])
    assert deleted == expected, deleted
    retired_path = store / "retired_0022.json"
    retired = json.loads(retired_path.read_text())["value"]
    assert retired["name"] == "aux_ready009.bin"
    sealed_path = store / "SEALED.json"
    sealed = json.loads(sealed_path.read_text())["value"]
    assert sealed["all_remaining_files_frozen"]
    for path in [retired_path, sealed_path]:
        source(path)

    links = []
    for name in completion["entry_documents_updated"]:
        path = ROOT / name
        block = path.read_text().split("<!-- D157 higher pilot timing checkpoint -->", 1)[1]
        block = block.split("<!-- End D157 higher pilot timing checkpoint -->", 1)[0]
        targets = re.findall(r"\]\(([^)]+)\)", block)
        assert len(targets) == 4
        for target in targets:
            resolved = (path.parent / target).resolve()
            assert resolved.is_file(), (name, target)
            links.append({"document": name, "target": str(resolved)})
    assert len(links) == 28
    locks = completion["owned_coordinator_locks_observed_free"]
    for name in locks:
        with (DATA / name).open("r") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(stream, fcntl.LOCK_UN)

    observed = datetime.now(timezone.utc).isoformat()
    usage = shutil.disk_usage(ROOT)
    gate = review["rounded_remaining_bank_free_gate_bytes"]
    assert gate == 70 * GIB
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024)
    assert peak <= 2 * GIB
    result = {
        "kind": "operational_cleanup_check_not_a_new_mathematical_certificate",
        "status": "pass", "checkpoint": "D157", "observed_utc": observed,
        "fresh_transitive_replay": source(DATA / (REPLAY + ".job.json")),
        "fresh_transitive_replay_wall_seconds": replay["wall_seconds"],
        "fixed_review": source(review_path), "completion": source(completion_path),
        "required_checkpoint_sources_missing_or_changed": False,
        "production_engine_import_passed": True,
        "production_dependencies_matched_to_frozen_bridge": dependencies,
        "native_libraries_loaded": native,
        "tracked_missing_paths": deleted,
        "tracked_missing_paths_already_observed_in_previous_session": True,
        "tracked_missing_paths_are_retired_scratch": True,
        "auxiliary_retirement_record": source(retired_path),
        "sealed_store_record": source(sealed_path),
        "workspace_scratch_removed_by_frozen_store_seal_method": True,
        "previous_operational_record": source(old_path),
        "current_artifact_links_checked": links,
        "owned_coordinator_locks_observed_free": locks,
        "filesystem_observation": {"path": str(ROOT), "total_bytes": usage.total,
            "used_bytes": usage.used, "free_bytes": usage.free, "not_a_reservation": True},
        "previous_free_bytes": old["filesystem_observation"]["free_bytes"],
        "free_bytes_increase_since_previous_observation": usage.free - old["filesystem_observation"]["free_bytes"],
        "remaining_bank_free_gate_bytes": gate,
        "remaining_bank_capacity_gate_met_at_observation": usage.free >= gate,
        "free_bytes_above_remaining_bank_gate": usage.free - gate,
        "full_bank_precision_pi": 1600, "columns_at_precision_6400": [0, 2],
        "production_launched": False, "frozen_files_restored_modified_or_deleted": False,
        "new_production_admission_granted": False, "next_unused_numbered_source": 655,
        "maximum_mathematical_workers": 3, "per_job_timeout_seconds": 180,
        "per_worker_or_store_limit_bytes": 2 * GIB, "aggregate_limit_bytes": 6 * GIB,
        "thread_limits": {key: os.environ[key] for key in threads},
        "scope": "D157 checkpoint and its transitive provenance, production runtime imports, completion and prior resume records; no inventory of unrelated personal files or tools.",
        "sources": sorted(prior.SOURCES.values(), key=lambda ref: ref["path"]),
        "wall_seconds": time.monotonic() - start, "peak_rss_bytes": peak,
    }
    with OUT.open("x") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print("PHASE_METADATA|" + json.dumps(source(OUT)), flush=True)
    print("PASS|D157_CLEANUP_CHECK", flush=True)


if __name__ == "__main__":
    main()
