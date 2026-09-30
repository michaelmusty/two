"""Run D65 native row-generation controls, preserving all D63/D64 artifacts.

Generated control copies use the separate D65 build. Every job has the
same 2 GB PARI stack cap and 900-second wall limit. No genus-64/a=51 job.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess

from build_lifttors_rows import ADAPTATION, BUILD, digest
from lifttors_lift import replace_once
from run_lifttors_controls import DATA, GP, HERE, ROOT, VENDOR, parse_log, run_job, source

JOBS = [
    ("formula_a2", "106_lifttors_row_system.gp", "bench_a=2;"),
    ("formula_a51", "106_lifttors_row_system.gp", "bench_a=51;"),
    ("kernel", "104_lifttors_kernel_validation.gp", ""),
    ("lift_comparison", "103_lifttors_lift_validation.gp", ""),
    ("q8", "100_lifttors_control.gp", ""),
    ("genus4_a2", "101_lifttors_scale.gp", "bench_genus=4;bench_a=2;"),
    ("genus4_a51", "101_lifttors_scale.gp", "bench_genus=4;bench_a=51;"),
    ("genus16_a2", "101_lifttors_scale.gp", "bench_genus=16;bench_a=2;"),
    ("genus64_a2", "101_lifttors_scale.gp", "bench_genus=64;bench_a=2;"),
]
OPTIONAL_JOBS = [
    ("genus16_a51", "101_lifttors_scale.gp", "bench_genus=16;bench_a=51;"),
]


def check(ok, message):
    if not ok:
        raise ValueError(message)


def checked_build():
    manifest = json.loads((BUILD / "build.json").read_text())
    check(manifest["compiled_adaptation"] == ADAPTATION, "Wrong native build")
    check(digest(BUILD / "liblifttors_rows.so") == manifest["library_sha256"], "Native library changed")
    for key, directory in [("adapter_sha256", HERE), ("source_sha256", VENDOR), ("generated_sha256", BUILD)]:
        for name, expected in manifest[key].items():
            check(digest(directory / name) == expected, f"Build input changed: {name}")
    # Reuse D64's strict check of the untouched D63 build and recorded inputs.
    spec = importlib.util.spec_from_file_location("extension_control", HERE / "105_lifttors_extension.py")
    extension = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extension)
    extension.backend_provenance()
    for record in json.loads((DATA / "lifttors_extension.json").read_text())["sources"]:
        check(digest(ROOT / record["path"]) == record["sha256"],
              f"D64 source or log changed: {record['path']}")
    return manifest


def control_text(template):
    text = replace_once((HERE / template).read_text(),
                        'read("../../pari/.build/lifttors/install.gp");',
                        f'read({json.dumps(str(BUILD / "install.gp"))});')
    if template.startswith("100_"):
        text = replace_once(text, 'writebin("../../data/computed/lifttors_q8_control.bin",',
                            'writebin("../../data/computed/lifttors_rows_q8_control.bin",')
    elif template.startswith("103_"):
        text = replace_once(text, "setrand(seed); B=PicLiftTors(Je,W,eini,2);", """setrand(seed); D=PicLiftTors_D63(Je,W,eini,2);
        check(PicEq_val(Je,A,D)==e,"upstream/D63 lift discrepancy");
        setrand(seed); B=PicLiftTors(Je,W,eini,2);""")
    elif template.startswith("104_"):
        check(text.count("LiftMatker_batched(A,T,pe,p,e)") == 2, "Kernel fixture changed")
        text = text.replace("LiftMatker_batched(A,T,pe,p,e)", "BlockKer(A,T,pe,p,e)")
        text = replace_once(text, "setrand(20260916);", """setrand(20260916);
BlockKer(A,T,pe,p,e)=
{
  my(m=matsize(A)[1],n=#A);
  my(blocks=vector((m+255)\\256,k,matrix(min(256,m-(k-1)*256),n,i,j,A[(k-1)*256+i,j])));
  LiftMatker_blocks(blocks,T,pe,p,e);
};""")
    elif template.startswith("106_"):
        text = replace_once(text, "RowBlock(k,H,S,C,Ip,Ic,rho,T,q)=", "RowBlockGP(k,H,S,C,Ip,Ic,rho,T,q)=")
        marker = "};\n{\n  if(type(bench_a)"
        text = replace_once(text, marker, """};
RowBlock(k,H,S,C,Ip,Ic,rho,T,q)=
{
  my(B=RowBlockGP(k,H,S,C,Ip,Ic,rho,T,q));
  my(BN=LiftRowsBlock(native_cache,uv,C,rho,k,T,q));
  check(valuation(Ered(B-BN,T,q),p)>=eini,"native versus GP row formula");
  BN;
};
{
  if(type(bench_a)""")
        text = replace_once(text, "R=matrix(0,n);maxblock=0;equal_entries=0;", """native_cache=LiftRowsPrepare(V,U0,uv,AB,T,q);
    R=matrix(0,n);maxblock=0;equal_entries=0;""")
        text = replace_once(text, "LS=matkerpadic(R,T,q,p,eini);", """LS=matkerpadic(R,T,q,p,eini);
    LN=LiftRowsKernel(native_cache,uv,C,rho,T,q,p,eini);
    check(#LN==#L && #EIndex(matconcat([L,LN]),T,p)[2]==#L,"native free kernel span");
    check(valuation(EMul(K,LN,T,q),p)>=eini,"native kernel against every original equation");
    print("TRACE|native_equations|compared=",equal_entries);""")
    return text


def collect(name, template, path):
    contents = path.read_text()
    report = parse_log(contents, "PASS|" + Path(template).stem)
    errors = [line for line in contents.splitlines()
              if line.lstrip().startswith("***") and "Warning:" not in line]
    check(not errors and "FAILURE|" not in contents, f"GP error: {path}")
    wall = re.findall(r"RESOURCE\|wall_seconds=([\d.]+)", contents)
    check(len(wall) == 1, "Missing or duplicated wall time")
    report["wall_seconds"] = float(wall[0])
    report["status"] = "PASS"
    report["kernel_traces"] = [
        {key: int(value) for key, value in (part.split("=") for part in line.split("|")[2:])}
        for line in contents.splitlines() if line.startswith("TRACE|row_kernel|")]
    report["cache_traces"] = [
        {key: int(value) for key, value in (part.split("=") for part in line.split("|")[2:])}
        for line in contents.splitlines() if line.startswith("TRACE|row_setup|")]
    check(report["kernel_traces"], "No native kernel was exercised")
    for trace in report["kernel_traces"]:
        check(trace["nullity"] == 0 or trace["replayed"] == trace["blocks"], "Incomplete residual verification")
    if name.startswith("formula"):
        check(report["a"] == int(name.removeprefix("formula_a")) and report["genus"] == 4,
              "Wrong formula-control parameters")
        count = sum(map(int, re.findall(r"TRACE\|native_equations\|compared=(\d+)", contents)))
        check(count == sum(s["compared_entries"] for s in report["systems"]), "Incomplete native equation comparison")
        report["native_equation_entries_compared"] = count
    if name == "lift_comparison":
        check(report["comparison_count"] == 60, "Missing lift comparisons")
        report["implementation_paths"] = ["upstream", "D63", "generated_rows"]
    if name == "kernel":
        check(report["known_kernel_cases"] == 12 and report["rank_drop_rejections"] == 6, "Missing kernel controls")
    if name.startswith("genus"):
        genus, a = map(int, re.fullmatch(r"genus(\d+)_a(\d+)", name).groups())
        check([report[k] for k in ["genus", "a", "p", "precision_exponent"]] == [genus, a, 97, 4], "Wrong scale parameters")
        check(len(report["kernel_traces"]) == 2, "Both precision steps must complete")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gp", default=GP)
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--only", nargs="+", choices=[job[0] for job in JOBS + OPTIONAL_JOBS])
    args = parser.parse_args()
    manifest = checked_build()
    controls = BUILD / "controls"
    controls.mkdir(exist_ok=True)
    reports = {}
    paths = [Path(__file__), DATA / "lifttors_controls.json", DATA / "lifttors_extension.json"]
    for name, template, prelude in JOBS + (OPTIONAL_JOBS if args.only else []):
        if args.only and name not in args.only:
            continue
        script = controls / template
        expected = control_text(template)
        if args.collect:
            check(script.read_text() == expected, "Generated control changed")
        else:
            script.write_text(expected)
        log = DATA / f"lifttors_rows_{name}.out"
        if not args.collect:
            print(f"START {name}", flush=True)
            run_job(args.gp, script, log, prelude, 900)
        reports[name] = collect(name, template, log)
        paths += [HERE / template, script, log]
        print(f"{name}: PASS; {reports[name].get('timing_ms')}; wall {reports[name]['wall_seconds']} s", flush=True)
    if args.only:
        return
    reports["backend"] = manifest
    reports["pari_version"] = subprocess.check_output([args.gp, "--version-short"], text=True).strip()
    reports["execution_policy"] = {
        "initial_pari_stack": "512M", "maximum_pari_stack": "2G",
        "per_process_timeout_seconds": 900, "peak_rss_measured": False,
        "stack_traces_are_checkpoints_not_peaks": True,
    }
    reports["scope"] = {
        "native_row_generation_integrated": True, "native_lift_materializes_full_derivative_matrix": False,
        "original_and_d63_lifts_retained": True, "recorded_d63_d64_input_digests_unchanged": True,
        "genus64_degree2_control_passed": True, "genus4_degree51_control_passed": True,
        "genus64_degree51_run": False, "target_arithmetic_sections_available": False,
        "target_polynomial_obtained": False,
    }
    paths += [DATA / "lifttors_rows_q8_control.bin", DATA / "lifttors_q8_control.bin"]
    reports["sources"] = [source(path) for path in dict.fromkeys(paths)]
    output = DATA / "lifttors_rows.json"
    output.write_text(json.dumps(reports, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()
