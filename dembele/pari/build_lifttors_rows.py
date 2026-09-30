"""Build D65 in .build/lifttors_rows without changing the D63 build or sources.

PicLiftTors uses generated rows; PicLiftTors_D63 and PicLiftTors_original
remain callable. The separate recipe preserves D63/D64 provenance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess

from build_lifttors import DEFAULT, HERE, REVISION, SOURCES, VENDOR
from lifttors_lift import replace_once
from lifttors_rows import adapt_rows

BUILD = HERE / ".build/lifttors_rows"
ADAPTATION = "D65: exact batched validator; generated lifting rows with complete kernel verification; D63 and upstream lifts retained"
ADAPTERS = ["build_lifttors_rows.py", "lifttors_rows.py", "lifttors_rows.c",
            "build_lifttors.py", "lifttors_lift.py", "lifttors_streamed.c", "lifttors_bounded.c"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pari-local", type=Path, default=Path(DEFAULT))
    args = parser.parse_args()
    prefix = args.pari_local.resolve()
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=VENDOR, text=True).strip()
    if revision != REVISION or subprocess.check_output(["git", "diff", "HEAD", "--"], cwd=VENDOR):
        raise SystemExit("Expected the unchanged pinned LiftTors checkout")
    BUILD.mkdir(parents=True, exist_ok=True)
    library = BUILD / "liblifttors_rows.so"
    signature = "ulong DivSub_dimval(GEN WA, GEN WB, long dim, GEN KV, GEN T, GEN p, long e, GEN pe)"
    pic = replace_once((VENDOR / "pic.c").read_text(), signature,
                       signature.replace("DivSub_dimval", "DivSub_dimval_original"))
    pic = '#include "linalg.h"\n' + signature + ';\n' + pic
    (BUILD / "pic_bounded.c").write_text(pic)
    (BUILD / "lift_rows.c").write_text(adapt_rows((VENDOR / "lift.c").read_text()))
    sources = [BUILD / "pic_bounded.c" if name == "pic" else
               BUILD / "lift_rows.c" if name == "lift" else VENDOR / f"{name}.c"
               for name in SOURCES]
    sources += [HERE / name for name in ["lifttors_bounded.c", "lifttors_streamed.c", "lifttors_rows.c"]]
    command = ["cc", "-O3", "-Wall", "-fno-strict-aliasing", "-fPIC",
               "-dynamiclib" if platform.system() == "Darwin" else "-shared",
               f"-I{prefix / 'include'}", f"-I{VENDOR}", *map(str, sources),
               f"-L{prefix / 'lib'}", f"-Wl,-rpath,{prefix / 'lib'}", "-lpari", "-lm", "-o", str(library)]
    subprocess.run(command, check=True)
    loader = re.sub(r'"lib(?:' + "|".join(SOURCES) + r')\.so"', f'"{library}"',
                    (VENDOR / "install.gp").read_text())
    loader = f'lifttors_library="{library}";\n' + loader
    for name, prototype in [
        ("PicLift_worker_streamed", "GUGGGGGG"), ("PicLiftTors_original", "GGLG"),
        ("PicLiftTors_D63", "GGLG"), ("LiftMatker_batched", "GGGGL"),
        ("LiftRowsPrepare", "GGGGGG"), ("LiftRowsBlock", "GGGGLGG"),
        ("LiftRowsKernel", "GGGGGGGL"), ("LiftMatker_blocks", "GGGGL"),
    ]:
        loader += f'\ninstall("{name}","{prototype}",,"{library}");\n'
    (BUILD / "install.gp").write_text(loader)
    upstream = sorted([*VENDOR.glob("*.c"), *VENDOR.glob("*.h"), *VENDOR.glob("*.gp")])
    manifest = {
        "repository": "https://github.com/nmascot/LiftTors", "revision": revision,
        "upstream_modified": False, "compiled_adaptation": ADAPTATION,
        "adapter_sha256": {name: digest(HERE/name) for name in ADAPTERS},
        "source_sha256": {path.name: digest(path) for path in upstream},
        "generated_sha256": {name: digest(BUILD/name) for name in ["pic_bounded.c", "lift_rows.c", "install.gp"]},
        "library_sha256": digest(library), "pari_prefix": str(prefix),
        "platform": platform.platform(), "command": command,
    }
    (BUILD / "build.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built D65 with retained D63/upstream paths: {library}")


if __name__ == "__main__":
    main()
