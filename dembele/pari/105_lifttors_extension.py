"""Calibrate degree-51 arithmetic and check a row-wise lifting prototype.

Uses the unchanged D63 library. Each GP job has a 2 GB PARI stack cap
and a 900-second wall limit. This never launches a genus-64/a=51 job.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import re
import subprocess

from run_lifttors_controls import DATA, GP, HERE, ROOT, VENDOR, parse_log, run_job, source


JOBS = [
    (f"genus4_a{a}_{kind}", script, f"lifttors_g4_a{a}_{kind}.out", a)
    for kind, script in [
        ("scale", "101_lifttors_scale.gp"),
        ("rows", "106_lifttors_row_system.gp"),
    ]
    for a in (2, 51)
]


def check(ok, message):
    if not ok:
        raise ValueError(message)


def backend_provenance():
    """Keep the completed D63 controls tied to their unchanged sources."""
    build = json.loads((HERE / ".build/lifttors/build.json").read_text())
    historical = json.loads((DATA / "lifttors_controls.json").read_text())
    check(build == historical["backend"], "Rebuild must match the D63 manifest")
    check(build["compiled_adaptation"] ==
          "exact batched DivSub_dimval; streamed PicLiftTors products; batched lifting kernel",
          "Expected the full D63 adaptation")
    check(source(HERE / ".build/lifttors/liblifttors.so")["sha256"] ==
          build["library_sha256"], "Compiled library changed")
    for name, digest in build["source_sha256"].items():
        check(source(VENDOR / name)["sha256"] == digest, f"Upstream source changed: {name}")
    adapters = {"lifttors_bounded.c": build["adapter_sha256"],
                **build["lift_adapter_sha256"]}
    for name, digest in adapters.items():
        check(source(HERE / name)["sha256"] == digest, f"Adapter changed: {name}")
    for record in historical["sources"]:
        check(source(ROOT / record["path"])["sha256"] == record["sha256"],
              f"D63 source or log changed: {record['path']}")
    return build, historical


def collect_job(name, script, path, a):
    contents = path.read_text()
    report = parse_log(contents, "PASS|" + Path(script).stem)
    check(not any(word in contents for word in ("FAILURE|", "  ***")),
          f"GP reported an error: {path}")
    for key, expected in {"genus": 4, "p": 97, "a": a, "precision_exponent": 4}.items():
        check(report[key] == expected, f"Wrong {key} in {name}")
    wall = re.findall(r"RESOURCE\|wall_seconds=([\d.]+)", contents)
    check(len(wall) == 1, f"Expected one wall time: {path}")
    report["wall_seconds"] = float(wall[0])
    report["status"] = "PASS"
    if name.endswith("scale"):
        check(report["d0"] == 9 and report["section_dimensions"] == [6, 15, 24],
              "Incorrect genus-4 section dimensions")
        report["lifting_system_stack_checkpoints"] = [
            {"rows": int(m), "columns": int(n),
             "stack_bytes_relative_to_lift_entry": int(b)}
            for m, n, b in re.findall(
                r"TRACE\|lift_system\|rows=(\d+)\|columns=(\d+)\|stack_bytes=(\d+)", contents)
        ]
        check(len(report["lifting_system_stack_checkpoints"]) == 2,
              "Missing a lifting system")
    else:
        check(sum(report["frobenius_cycle_lengths"]) == report["evaluation_points"],
              "Frobenius cycles do not cover evaluation points")
        check([s["initial_precision"] for s in report["systems"]] == [1, 2],
              "Both starting precisions must be checked")
        for system in report["systems"]:
            check([system["rows"], system["columns"], system["rank"],
                   system["kernel_dimension"], system["selected_rows"]] ==
                  [(report["evaluation_points"] - 24) * 6, 19, 9, 10, 9],
                  "Unexpected lifting-system dimensions")
            check(system["full_field_witness"] and system["compared_entries"] ==
                  system["rows"] * system["columns"], "Incomplete equation comparison")
    return report


def storage_projection(systems):
    """Conditional object-tree sizes, never measured stack usage or RSS."""
    scenarios = []
    for nz, assumption in [
        (646, "D63 row count, also the minimum for d0=129"),
        (663, "hypothetical thirteen full Frobenius orbits of length 51"),
    ]:
        rows, columns = (nz - 324) * 66, 259
        entries = rows * columns
        estimates = []
        payload_rates = []
        for s in systems:
            count = s["rows"] * s["columns"]
            rate = Fraction(s["entry_payload_bytes"], count)
            # A t_MAT has n column pointers; each t_COL has m entry pointers.
            # Each object also has a one-word header. Check against measurements.
            words = count + 2 * s["columns"] + 1
            word_bytes = Fraction(s["matrix_size_bytes"] - s["entry_payload_bytes"], words)
            check(word_bytes == 8, "Unexpected PARI object container size")
            estimates.append(round(entries * rate + 8 * (entries + 2 * columns + 1)))
            payload_rates.append(float(rate))
        scenarios.append({
            "evaluation_points": nz, "assumption": assumption,
            "rows": rows, "columns": columns, "field_entries": entries,
            "measured_payload_bytes_per_entry": payload_rates,
            "projected_matrix_tree_bytes": estimates,
            "single_row_block_entries": (nz - 324) * columns,
            "full_matrix_to_row_block_entry_ratio": 66,
        })
    return {
        "kind": "conditional extrapolation from genus-4/a=51 entry representations",
        "is_measured_genus64_storage": False,
        "is_peak_rss_or_stack_usage": False,
        "is_proved_lower_bound": False,
        "includes_other_objects_and_temporary_allocations": False,
        "scenarios": scenarios,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gp", default=GP)
    parser.add_argument("--collect", action="store_true", help="reuse the four saved GP logs")
    args = parser.parse_args()
    build, historical = backend_provenance()
    version = subprocess.check_output([args.gp, "--version-short"], text=True).strip()
    check(version == historical["pari_version"], "PARI version differs from D63")
    reports = {}
    paths = [Path(__file__), HERE / "run_lifttors_controls.py", DATA / "lifttors_controls.json"]
    for name, script, output, a in JOBS:
        path = DATA / output
        if not args.collect:
            run_job(args.gp, script, path, f"bench_genus=4;bench_a={a};bench_e=4;", 900)
        reports[name] = collect_job(name, script, path, a)
        paths += [HERE / script, path]
        print(f"{name}: PASS; wall {reports[name]['wall_seconds']} s")
    for a in (2, 51):
        check(reports[f"genus4_a{a}_scale"]["evaluation_points"] ==
              reports[f"genus4_a{a}_rows"]["evaluation_points"], "Different point counts")
    small = reports["genus4_a2_scale"]
    large = reports["genus4_a51_scale"]
    reports["comparison"] = {
        "lift_time_ratio": large["timing_ms"]["lift_one_point"] / small["timing_ms"]["lift_one_point"],
        "jacobian_object_size_ratio": large["jacobian_size_bytes"] / small["jacobian_size_bytes"],
        "point_counts_also_differ": True,
        "is_genus64_runtime_forecast": False,
        "equation_entries_compared": sum(
            s["compared_entries"] for a in (2, 51)
            for s in reports[f"genus4_a{a}_rows"]["systems"]),
    }
    reports["storage_projection"] = storage_projection(reports["genus4_a51_rows"]["systems"])
    reports["backend"] = build
    reports["pari_version"] = version
    reports["execution_policy"] = {
        "initial_pari_stack": "512M", "maximum_pari_stack": "2G",
        "per_process_timeout_seconds": 900, "worker_threads": 1,
        "random_seed": 20260916, "peak_rss_measured": False,
    }
    reports["scope"] = {
        "genus4_degree51_known_torsion_lift_passed": True,
        "degree51_equation_entries_use_full_residue_field": True,
        "control_torsion_point_is_rational": True,
        "control_has_target_residual_representation": False,
        "row_formula_and_all_equations_verified": True,
        "production_row_generation_integrated": False,
        "d63_backend_and_source_digests_unchanged": True,
        "genus64_degree51_run": False,
        "target_arithmetic_sections_available": False,
        "target_polynomial_obtained": False,
    }
    reports["sources"] = [source(path) for path in dict.fromkeys(paths)]
    output = DATA / "lifttors_extension.json"
    output.write_text(json.dumps(reports, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()
