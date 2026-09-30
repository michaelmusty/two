"""Build pinned LiftTors as one library, avoiding cross-dylib symbols on macOS.

The checkout is unmodified. By default the compiled copy uses the exact
batched validator and streamed lifting products; --upstream retains the
original, and --validator-only reproduces the D62 algorithms.
Run GP from vendor/LiftTors and load the
generated .build/lifttors/install.gp, followed by GalRep.gp and PtIsOnCurve.gp.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
from lifttors_lift import adapt_lift

HERE = Path(__file__).resolve().parent
VENDOR = HERE.parent / "vendor/LiftTors"
BUILD = HERE / ".build/lifttors"
REVISION = "fd6403caf7147b21b67dcb17dbedccea762d6262"
DEFAULT = "/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/10.6/local"
SOURCES = ["linalg", "exp", "pic", "lift", "freyruck", "rr", "torsspace", "zeta"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pari-local", type=Path, default=Path(DEFAULT))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--upstream", action="store_true")
    mode.add_argument("--validator-only", action="store_true")
    mode.add_argument("--products-only", action="store_true", help="stream products but retain the upstream tall kernel solve")
    args = parser.parse_args()
    prefix = args.pari_local.resolve()
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=VENDOR, text=True).strip()
    if revision != REVISION:
        raise SystemExit(f"Expected {REVISION}, found {revision}")
    if subprocess.check_output(["git", "diff", "HEAD", "--"], cwd=VENDOR):
        raise SystemExit("Review modified upstream sources before building")
    BUILD.mkdir(parents=True, exist_ok=True)
    library = BUILD / "liblifttors.so"
    command = ["cc", "-O3", "-Wall", "-fno-strict-aliasing", "-fPIC",
               "-dynamiclib" if platform.system() == "Darwin" else "-shared",
               f"-I{prefix / 'include'}", f"-I{VENDOR}"]
    sources = [VENDOR / f"{source}.c" for source in SOURCES]
    if not args.upstream:
        pic = (VENDOR / "pic.c").read_text()
        old = "ulong DivSub_dimval(GEN WA, GEN WB, long dim, GEN KV, GEN T, GEN p, long e, GEN pe)"
        if pic.count(old) != 1:
            raise SystemExit("Validator signature changed; review adaptation")
        pic = pic.replace(old,old.replace("DivSub_dimval", "DivSub_dimval_original"))
        pic = '#include "linalg.h"\n' + old + ';\n' + pic
        compiled_pic = BUILD / "pic_bounded.c"
        compiled_pic.write_text(pic)
        sources[sources.index(VENDOR / "pic.c")] = compiled_pic
        sources.append(HERE / "lifttors_bounded.c")
    if not args.upstream and not args.validator_only:
        compiled_lift = BUILD / "lift_streamed.c"
        compiled_lift.write_text(adapt_lift((VENDOR / "lift.c").read_text(),
                                          batched_kernel=not args.products_only))
        sources[sources.index(VENDOR / "lift.c")] = compiled_lift
        sources.append(HERE / "lifttors_streamed.c")
    command += [str(source) for source in sources]
    command += [f"-L{prefix / 'lib'}", f"-Wl,-rpath,{prefix / 'lib'}",
                "-lpari", "-lm", "-o", str(library)]
    subprocess.run(command, check=True)
    loader = (VENDOR / "install.gp").read_text()
    loader = re.sub(r'"lib(?:' + "|".join(SOURCES) + r')\.so"',
                    f'"{library}"', loader)
    loader = f'lifttors_library="{library}";\n' + loader
    if not args.upstream and not args.validator_only:
        loader += f'\ninstall("PicLift_worker_streamed","GUGGGGGG",,"{library}");\n'
        loader += f'install("PicLiftTors_original","GGLG",,"{library}");\n'
        loader += f'install("LiftMatker_batched","GGGGL",,"{library}");\n'
    (BUILD / "install.gp").write_text(loader)
    source_files = sorted([*VENDOR.glob("*.c"), *VENDOR.glob("*.h"),
                           *VENDOR.glob("*.gp")])
    manifest = {
        "repository": "https://github.com/nmascot/LiftTors",
        "revision": revision,
        "upstream_modified": False,
        "compiled_adaptation": None if args.upstream else (
            "exact batched DivSub_dimval" if args.validator_only else
            "exact batched DivSub_dimval; streamed PicLiftTors products" +
            ("" if args.products_only else "; batched lifting kernel")),
        "adapter_sha256": None if args.upstream else hashlib.sha256(
            (HERE / "lifttors_bounded.c").read_bytes()).hexdigest(),
        "lift_adapter_sha256": None if args.upstream or args.validator_only else {
            name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
            for name in ["lifttors_lift.py", "lifttors_streamed.c"]},
        "pari_prefix": str(prefix),
        "platform": platform.platform(),
        "command": command,
        "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in source_files},
        "library_sha256": hashlib.sha256(library.read_bytes()).hexdigest(),
    }
    (BUILD / "build.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {REVISION}: {library}")


if __name__ == "__main__":
    main()
