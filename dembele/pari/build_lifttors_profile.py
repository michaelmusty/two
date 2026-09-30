"""D67: a separate diagnostic build of the unchanged D66 arithmetic."""
import importlib.util
import json
import subprocess

from build_lifttors_reduction import BUILD as BASE, digest
from lifttors_profile import profile_lift, profile_linalg, profile_pic, profile_validator
from run_lifttors_controls import DATA, HERE, ROOT, VENDOR

BUILD = HERE / ".build/lifttors_profile"
ADAPTATION = "D67: D66 arithmetic with allocation and timing checkpoints; no arithmetic or reclamation changes"
ADAPTERS = ["build_lifttors_profile.py", "lifttors_profile.py", "lifttors_profile.h", "lifttors_profile.c"]


def checked_base():
    spec = importlib.util.spec_from_file_location("degree51_control", HERE / "108_lifttors_degree51.py")
    previous = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(previous)
    base = previous.checked_build()
    report = json.loads((DATA / "lifttors_degree51.json").read_text())
    previous.rows.check(base == report["backend"], "Recorded D66 build changed")
    for record in report["sources"]:
        previous.rows.check(digest(ROOT / record["path"]) == record["sha256"],
                            f"Recorded D66 input changed: {record['path']}")
    return base


def main():
    base = checked_base()
    BUILD.mkdir(parents=True, exist_ok=True)
    inputs = [
        (BASE / "pic_reduction.c", "pic_profile.c", profile_pic),
        (HERE / ".build/lifttors_rows/lift_rows.c", "lift_profile.c", profile_lift),
        (VENDOR / "linalg.c", "linalg_profile.c", profile_linalg),
        (HERE / "lifttors_bounded.c", "validator_profile.c", profile_validator),
    ]
    substitutions = {}
    for path, name, transform in inputs:
        (BUILD / name).write_text(transform(path.read_text()))
        substitutions[str(path)] = str(BUILD / name)
    library = BUILD / "liblifttors_profile.so"
    substitutions[str(BASE / "liblifttors_reduction.so")] = str(library)
    if any(base["command"].count(key) != 1 for key in substitutions):
        raise ValueError("Unexpected D66 compiler inputs")
    command = [substitutions.get(part, part) for part in base["command"]]
    command[1:1] = [f"-I{HERE}", str(HERE / "lifttors_profile.c")]
    subprocess.run(command, check=True)
    loader = (BASE / "install.gp").read_text().replace(str(BASE / "liblifttors_reduction.so"), str(library))
    loader += f'\ninstall("LiftProfileEnable","vL",,"{library}");\n'
    (BUILD / "install.gp").write_text(loader)
    names = [name for _, name, _ in inputs] + ["install.gp"]
    manifest = {
        "compiled_adaptation": ADAPTATION, "arithmetic_changed": False,
        "base_build_sha256": digest(BASE / "build.json"),
        "base_library_sha256": base["library_sha256"],
        "revision": base["revision"], "upstream_modified": False,
        "adapter_sha256": {name: digest(HERE / name) for name in ADAPTERS},
        "generated_sha256": {name: digest(BUILD / name) for name in names},
        "library_sha256": digest(library), "command": command,
        "pari_prefix": base["pari_prefix"], "platform": base["platform"],
    }
    (BUILD / "build.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built diagnostic-only library: {library}")


if __name__ == "__main__":
    main()
