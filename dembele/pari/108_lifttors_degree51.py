"""D66 degree-51 calibration and the separate PicRed correction controls.

No genus-64/degree-51 job, increased stack cap, or modified earlier artifact.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess

from build_lifttors_reduction import ADAPTATION, BASE, BUILD, checked_base, digest
from lifttors_lift import replace_once
from run_lifttors_controls import DATA, GP, HERE, ROOT, parse_log, run_job, source

spec = importlib.util.spec_from_file_location("rows_control", HERE / "107_lifttors_rows.py")
rows = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rows)
JOBS = [
    ("audit", "110_lifttors_reduction_audit.gp", "lifttors_reduction_audit.out", ""),
    ("validation", "111_lifttors_reduction_validation.gp", "lifttors_reduction_validation.out", ""),
    ("storage", "109_lifttors_storage.gp", "lifttors_storage.out", ""),
    ("lift_comparison", "103_lifttors_lift_validation.gp", "lifttors_reduction_lift_comparison.out", ""),
    ("q8", "100_lifttors_control.gp", "lifttors_reduction_q8.out", ""),
    ("genus16_a51", "101_lifttors_scale.gp", "lifttors_reduction_genus16_a51.out", "bench_genus=16;bench_a=51;"),
]


def checked_build():
    base = checked_base()
    rows.check(base == json.loads((DATA / "lifttors_rows.json").read_text())["backend"],
               "Recorded D65 build changed")
    manifest = json.loads((BUILD / "build.json").read_text())
    rows.check(manifest["compiled_adaptation"] == ADAPTATION, "Wrong D66 build")
    rows.check(manifest["base_build_sha256"] == digest(BASE / "build.json"), "Base build changed")
    rows.check(manifest["library_sha256"] == digest(BUILD / "liblifttors_reduction.so"), "D66 library changed")
    for key, directory in [("adapter_sha256", HERE), ("generated_sha256", BUILD)]:
        for name, expected in manifest[key].items():
            rows.check(digest(directory / name) == expected, f"D66 input changed: {name}")
    return manifest


def control_text(template):
    text = rows.control_text(template)
    text = replace_once(text, str(BASE / "install.gp"), str(BUILD / "install.gp"))
    if template.startswith("100_"):
        text = replace_once(text, "lifttors_rows_q8_control.bin", "lifttors_reduction_q8_control.bin")
    return text


def collect_plain(path, template):
    text = path.read_text()
    report = parse_log(text, "PASS|" + Path(template).stem)
    errors = [line for line in text.splitlines() if line.lstrip().startswith("***") and "Warning:" not in line]
    rows.check(not errors and "FAILURE|" not in text, f"GP error: {path}")
    wall = re.findall(r"RESOURCE\|wall_seconds=([\d.]+)", text)
    rows.check(len(wall) == 1, "Missing or duplicated wall time")
    report.update(wall_seconds=float(wall[0]), status="PASS")
    return report


def storage_projection(storage):
    """Conditional object-tree projection using each matrix's entry costs.

    The known-curve bases have one constant column in V1,V2,W0,U1,U2;
    KV has a dense block and a negative identity, and V3 is generated.
    These assumptions are checked at g=16, not asserted for the target Y.
    """
    observed = next(r for r in storage["records"] if r["precision_exponent"] == 2)
    result = {}
    for genus, npoints in [(16, 204), (64, 663)]:
        dims = [genus + 2, 3 * genus + 3, 5 * genus + 4]
        sizes = {f"V{i+1}": (npoints, k) for i, k in enumerate(dims)}
        sizes.update({f"KV{i+1}": (npoints-k, npoints) for i, k in enumerate(dims)})
        sizes.update(W0=(npoints, dims[0]), U1=(npoints, 2*genus+2),
                     U2=(npoints, 2*genus+2), evaluation_inverse=(dims[1], dims[1]))
        objects = {}
        for name, (m, n) in sizes.items():
            entry = observed["matrices"][name]
            m0, n0 = entry["rows"], entry["columns"]
            z0, c0 = entry["zero_entries"], entry["unit_constant_entries"]
            zeros, constants = (m*(m-1), m) if name.startswith("KV") else (
                (0, m) if name in ["V1", "V2", "W0", "U1", "U2"] else (0, 0))
            if genus == 16:
                rows.check((z0, c0) == (zeros, constants), f"Unexpected sparsity: {name}")
                rows.check(entry["object_bytes"] - entry["entry_bytes"] == 8*(1+n*(m+2)), "Matrix tree headers")
            mean = entry["nontrivial_entry_bytes"] / (m0*n0-z0-c0)
            # The zero and constant polynomial trees have 16 and 48 bytes.
            rows.check(entry["entry_bytes"] - entry["nontrivial_entry_bytes"] == 16*z0+48*c0,
                       f"Unexpected constant representation: {name}")
            objects[name] = round((m*n-zeros-constants)*mean+16*zeros+48*constants+8*(1+n*(m+2)))
        result[f"genus{genus}"] = {"evaluation_points": npoints, "matrix_object_bytes": objects,
                                   "matrix_object_bytes_sum": sum(objects.values())}
    result.update(precision_exponent=2, conditional=True, peak_rss=False, stack_lower_bound=False,
                  assumptions="Same known-curve bases, one rational auxiliary embedding each, full 51-cycles, comparable entry costs; shared storage is not accounted for")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gp", default=GP)
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--only", nargs="+", choices=[job[0] for job in JOBS])
    args = parser.parse_args()
    manifest = checked_build()
    controls = BUILD / "controls"
    controls.mkdir(exist_ok=True)
    baseline = DATA / "lifttors_rows_genus16_a51.out"
    reports = {"d65_genus16_a51": rows.collect("genus16_a51", "101_lifttors_scale.gp", baseline)}
    paths = [Path(__file__), HERE / "build_lifttors_reduction.py", baseline,
             DATA / "lifttors_rows.json", DATA / "lifttors_q8_control.bin", BASE / "build.json", BUILD / "build.json"]
    for name, template, filename, prelude in JOBS:
        if args.only and name not in args.only:
            continue
        script = HERE / template
        if template.startswith(("100_", "101_", "103_")):
            script = controls / template
            expected = control_text(template)
            if args.collect:
                rows.check(script.read_text() == expected, "Generated D66 control changed")
            else:
                script.write_text(expected)
        path = DATA / filename
        if not args.collect:
            print(f"START {name}", flush=True)
            run_job(args.gp, script, path, prelude, 900)
        reports[name] = (rows.collect(name, template, path) if name in ["lift_comparison", "q8", "genus16_a51"]
                         else collect_plain(path, template))
        paths += [HERE / template, script, path]
        print(f"{name}: PASS; wall {reports[name]['wall_seconds']} s", flush=True)
    if args.only:
        return
    rows.check(reports["audit"]["auxiliary_table_failures"] == 10, "Missing original bug reproduction")
    reports["audit"]["meaning"] = "Audit completed; the original reduction defect was reproduced"
    expected = {"embedding_matrices_checked": 25, "point_evaluations_checked": 20,
                "projective_vectors_checked": 80, "composition_checks": 15, "malformed_table_rejections": 2}
    rows.check(all(reports["validation"][k] == v for k, v in expected.items()), "Incomplete reduction controls")
    rows.check(reports["storage"]["full_field_entry_witness"], "Missing field witness")
    reports["storage_projection"] = storage_projection(reports["storage"])
    reports["backend"] = manifest
    reports["pari_version"] = subprocess.check_output([args.gp, "--version-short"], text=True).strip()
    reports["execution_policy"] = {"initial_pari_stack": "512M", "maximum_pari_stack": "2G",
                                    "per_process_timeout_seconds": 900, "peak_rss_measured": False}
    reports["scope"] = {"genus16_degree51_control_passed_before_and_after_fix": True,
                         "reduced_auxiliary_evaluation_bug_reproduced_and_corrected": True,
                         "recorded_d63_d64_d65_inputs_unchanged": True,
                         "genus64_degree51_run": False, "corrected_build_genus64_run": False,
                         "target_arithmetic_sections_available": False, "target_polynomial_obtained": False}
    paths += [DATA / "lifttors_reduction_q8_control.bin"]
    reports["sources"] = [source(path) for path in dict.fromkeys(paths)]
    output = DATA / "lifttors_degree51.json"
    output.write_text(json.dumps(reports, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()
