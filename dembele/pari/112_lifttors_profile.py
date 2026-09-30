"""D67: collect checkpointed allocations without changing D66 arithmetic.

Scale jobs are single-threaded, under the existing 2 GB/900 s limits.
No genus-64/degree-51 run is defined.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess

from build_lifttors_profile import ADAPTATION, BASE, BUILD, checked_base, digest
from lifttors_lift import replace_once
from run_lifttors_controls import DATA, GP, HERE, ROOT, run_job, source

spec = importlib.util.spec_from_file_location("degree51_control", HERE / "108_lifttors_degree51.py")
d66 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d66)
JOBS = [
    ("validation", "113_lifttors_profile_validation.gp", ""),
    ("genus4_a51", "101_lifttors_scale.gp", "bench_genus=4;bench_a=51;"),
    ("genus16_a51", "101_lifttors_scale.gp", "bench_genus=16;bench_a=51;"),
]


def c_tokens(value):
    pattern = r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    value = re.sub(pattern, lambda m: " " if m[0].startswith(("/*", "//")) else m[0], value, flags=re.S)
    return re.findall(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\w+|>>=|<<=|\.\.\.|->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||\+=|-=|\*=|/=|%=|&=|\^=|\|=|##|[^\s]', value)


def checked_build():
    checked_base()
    manifest = json.loads((BUILD / "build.json").read_text())
    d66.rows.check(manifest["compiled_adaptation"] == ADAPTATION, "Wrong profiling build")
    d66.rows.check(manifest["base_build_sha256"] == digest(BASE / "build.json"), "Base build changed")
    d66.rows.check(manifest["library_sha256"] == digest(BUILD / "liblifttors_profile.so"), "Profile library changed")
    for key, directory in [("adapter_sha256", HERE), ("generated_sha256", BUILD)]:
        for name, expected in manifest[key].items():
            d66.rows.check(digest(directory / name) == expected, f"Profiling input changed: {name}")
    # Remove only the diagnostic scaffolding, then compare every remaining
    # C token with the preserved source. This complements the runtime checks.
    originals = {"pic_profile.c": BASE / "pic_reduction.c",
                 "lift_profile.c": HERE / ".build/lifttors_rows/lift_rows.c",
                 "linalg_profile.c": HERE.parent / "vendor/LiftTors/linalg.c",
                 "validator_profile.c": HERE / "lifttors_bounded.c"}
    for name, original in originals.items():
        text = (BUILD / name).read_text().removeprefix('#include "lifttors_profile.h"\n')
        text = re.sub(r'\s*LiftProfileFrame d67_frame;', '', text)
        text = re.sub(r'\s*LiftProfile(?:Start|Point)\([^;]+;', '', text)
        text = re.sub(r'return LiftProfileEndU?\(&d67_frame,\((.*?)\)\);', r'return \1;', text, flags=re.S)
        d66.rows.check(c_tokens(text) == c_tokens(original.read_text()), f"Non-diagnostic source change: {name}")
    return manifest


def control_text(template):
    text = d66.control_text(template)
    return replace_once(text, f'read({json.dumps(str(BASE / "install.gp"))});',
                        f'read({json.dumps(str(BUILD / "install.gp"))});\nLiftProfileEnable(1);')


def allocation_report(text):
    events = []
    growth_events = []
    calls = {}
    active = []
    numeric = ["id", "parent", "e", "stack_bytes", "local_stack_bytes", "object_bytes", "elapsed_ms", "stack_capacity"]
    for line in text.splitlines():
        growth = re.search(r'Warning: increasing stack size to (\d+)', line)
        if growth:
            ident = active[-1] if active else None
            growth_events.append({"new_capacity_bytes": int(growth[1]), "active_call": ident,
                                  "function": calls[ident]["function"] if ident else None,
                                  "preceding_checkpoint": calls[ident]["events"][-1] if ident else None})
        if not line.startswith("TRACE|allocation|"):
            continue
        event = dict(part.split("=", 1) for part in line.split("|")[2:])
        for key in numeric:
            event[key] = int(event[key])
        ident = event["id"]
        d66.rows.check(0 <= event["local_stack_bytes"] <= event["stack_bytes"] <= event["stack_capacity"],
                       "Invalid stack checkpoint")
        if event["stage"] == "enter":
            d66.rows.check(ident not in calls and event["parent"] == (active[-1] if active else 0),
                           "Invalid single-thread call nesting")
            calls[ident] = {"function": event["function"], "parent": event["parent"], "e": event["e"],
                            "entry_stack_bytes": event["stack_bytes"], "events": [], "children": [],
                            "maximum_checkpoint_bytes": event["stack_bytes"], "maximum_checkpoint": event}
            if active:
                calls[active[-1]]["children"].append(ident)
            active.append(ident)
        d66.rows.check(active and active[-1] == ident, "Event outside its active call")
        call = calls[ident]
        d66.rows.check(not call["events"] or event["elapsed_ms"] >= call["events"][-1]["elapsed_ms"],
                       "Nonmonotonic cumulative timer")
        call["events"].append(event)
        for ancestor in active:
            if event["stack_bytes"] > calls[ancestor]["maximum_checkpoint_bytes"]:
                calls[ancestor]["maximum_checkpoint_bytes"] = event["stack_bytes"]
                calls[ancestor]["maximum_checkpoint"] = event
        if event["stage"] == "exit":
            call["elapsed_ms"] = event["elapsed_ms"]
            call["exit_stack_bytes"] = event["stack_bytes"]
            call["exclusive_ms"] = event["elapsed_ms"] - sum(calls[c]["elapsed_ms"] for c in call["children"])
            # Millisecond rounding at each child boundary allows a small error.
            d66.rows.check(call["exclusive_ms"] >= -len(call["children"]), "Child timings exceed parent")
            active.pop()
        events.append(event)
    d66.rows.check(events and not active, "Incomplete allocation trace")
    aggregate = {}
    for call in calls.values():
        name = call["function"]
        summary = aggregate.setdefault(name, {"calls": 0, "inclusive_ms": 0, "exclusive_ms": 0,
                                               "maximum_checkpoint_bytes": 0})
        summary["calls"] += 1
        summary["inclusive_ms"] += call["elapsed_ms"]
        summary["exclusive_ms"] += call["exclusive_ms"]
        summary["maximum_checkpoint_bytes"] = max(summary["maximum_checkpoint_bytes"], call["maximum_checkpoint_bytes"])
    lifts = [{"id": ident, **call} for ident, call in calls.items() if call["function"] == "PicLiftTors"]
    d66.rows.check(len(lifts) == 1, "Expected one instrumented lift")
    lift = lifts[0]
    d66.rows.check([e["e"] for e in lift["events"] if e["stage"] == "iteration_J"] == [2, 4], "Both precision steps")
    # Restrict group-operation costs to the lift; exclude initialization and
    # the independent input/output checks in the surrounding GP control.
    in_lift = set()
    def visit(ident):
        in_lift.add(ident)
        for child in calls[ident]["children"]:
            visit(child)
    visit(lift["id"])
    lift_aggregate = {}
    for ident in in_lift:
        call = calls[ident]
        summary = lift_aggregate.setdefault(call["function"], {"calls": 0, "inclusive_ms": 0, "exclusive_ms": 0})
        summary["calls"] += 1
        summary["inclusive_ms"] += call["elapsed_ms"]
        summary["exclusive_ms"] += call["exclusive_ms"]
    return {"event_count": len(events), "call_count": len(calls), "function_totals": aggregate,
            "stack_growth_events": growth_events,
            "lift_function_totals": lift_aggregate, "lift": lift,
            "largest_checkpoints": sorted(events, key=lambda e: e["stack_bytes"], reverse=True)[:12],
            "calls": {str(k): v for k, v in calls.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gp", default=GP)
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--only", nargs="+", choices=[job[0] for job in JOBS])
    args = parser.parse_args()
    manifest = checked_build()
    controls = BUILD / "controls"
    controls.mkdir(exist_ok=True)
    reports = {}
    paths = [Path(__file__), DATA / "lifttors_degree51.json", BASE / "build.json", BUILD / "build.json"]
    for name, template, prelude in JOBS:
        if args.only and name not in args.only:
            continue
        script = HERE / template
        if template.startswith("101_"):
            script = controls / template
            expected = control_text(template)
            if args.collect:
                d66.rows.check(script.read_text() == expected, "Generated profiling control changed")
            else:
                script.write_text(expected)
        log = DATA / f"lifttors_profile_{name}.out"
        if not args.collect:
            print(f"START {name}", flush=True)
            run_job(args.gp, script, log, prelude, 900)
        if name == "validation":
            report = d66.collect_plain(log, template)
            d66.rows.check(report["comparison_count"] == 20 and report["exact_matrices_and_random_states_equal"],
                           "Incomplete diagnostic comparisons")
        else:
            report = d66.rows.collect(name, template, log)
            report["allocations"] = allocation_report(log.read_text())
        reports[name] = report
        paths += [HERE / template, script, log]
        print(f"{name}: PASS; wall {report['wall_seconds']} s", flush=True)
    if args.only:
        return
    reports["backend"] = manifest
    reports["pari_version"] = subprocess.check_output([args.gp, "--version-short"], text=True).strip()
    reports["execution_policy"] = {"initial_pari_stack": "512M", "maximum_pari_stack": "2G",
                                    "per_process_timeout_seconds": 900, "peak_rss_measured": False,
                                    "allocation_traces_are_checkpoints_not_peaks": True}
    reports["scope"] = {"arithmetic_or_reclamation_changed": False, "prior_d63_through_d66_inputs_unchanged": True,
                         "original_C_tokens_recovered_after_removing_hooks": True,
                         "genus64_degree51_run": False, "target_arithmetic_sections_available": False,
                         "target_polynomial_obtained": False}
    reports["sources"] = [source(p) for p in dict.fromkeys(paths)]
    output = DATA / "lifttors_profile.json"
    output.write_text(json.dumps(reports, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()
