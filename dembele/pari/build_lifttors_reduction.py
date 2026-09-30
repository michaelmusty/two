"""D66: preserve vectors of embedding matrices when reducing a Jacobian.

Build separately from the recorded D65 library, with its compiler command
and inputs verified. PicRed_original is retained only for the shape audit.
"""
import importlib.util
import json
import subprocess

from build_lifttors_rows import BUILD as BASE, digest
from lifttors_lift import replace_once
from run_lifttors_controls import DATA, HERE, ROOT

BUILD = HERE / ".build/lifttors_reduction"
ADAPTATION = "D66: D65 generated lifting rows plus shape-correct PicRed auxiliary evaluation tables"


def checked_base():
    spec = importlib.util.spec_from_file_location("rows_control", HERE / "107_lifttors_rows.py")
    rows = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rows)
    manifest = rows.checked_build()
    for record in json.loads((DATA / "lifttors_rows.json").read_text())["sources"]:
        rows.check(digest(ROOT / record["path"]) == record["sha256"],
                   f"Recorded D65 input changed: {record['path']}")
    return manifest


def corrected_pic(text):
    start = text.index("GEN PicRed(GEN J, ulong e)")
    end = text.index("GEN DivMul(", start)
    original = text[start:end]
    fixed = replace_once(original, "ulong i;", "ulong i,j;")
    fixed = replace_once(fixed,
        "\tgmael(Je,13,1) = FpXM_red(gmael(J,13,1),pe);\n"
        "\tgmael(Je,13,2) = FpXM_red(gmael(J,13,2),pe);",
        """\t/* RRspaceEval returns one matrix for each embedding, in a vector. */
\tfor(i=1;i<=2;i++)
\t{
\t\tGEN source = gmael(J,13,i), reduced;
\t\tif(typ(source)!=t_VEC)
\t\t\tpari_err(e_MISC,"PicRed: expected an embedding vector of matrices");
\t\treduced = cgetg(lg(source),t_VEC);
\t\tfor(j=1;j<lg(source);j++)
\t\t{
\t\t\tif(typ(gel(source,j))!=t_MAT)
\t\t\t\tpari_err(e_MISC,"PicRed: expected an embedding vector of matrices");
\t\t\tgel(reduced,j) = FpXM_red(gel(source,j),pe);
\t\t}
\t\tgmael(Je,13,i) = reduced;
\t}""")
    return text[:start] + original.replace("GEN PicRed(", "GEN PicRed_original(", 1) + fixed + text[end:]


def main():
    base = checked_base()
    BUILD.mkdir(parents=True, exist_ok=True)
    pic = BUILD / "pic_reduction.c"
    pic.write_text(corrected_pic((BASE / "pic_bounded.c").read_text()))
    library = BUILD / "liblifttors_reduction.so"
    substitutions = {str(BASE / "pic_bounded.c"): str(pic),
                     str(BASE / "liblifttors_rows.so"): str(library)}
    if any(base["command"].count(key) != 1 for key in substitutions):
        raise ValueError("Unexpected D65 compiler command")
    command = [substitutions.get(part, part) for part in base["command"]]
    subprocess.run(command, check=True)
    loader = (BASE / "install.gp").read_text().replace(str(BASE / "liblifttors_rows.so"), str(library))
    loader += f'\ninstall("PicRed_original","GU",,"{library}");\n'
    (BUILD / "install.gp").write_text(loader)
    manifest = {
        "compiled_adaptation": ADAPTATION,
        "base_build": str(BASE.relative_to(ROOT) / "build.json"),
        "base_build_sha256": digest(BASE / "build.json"),
        "base_library_sha256": base["library_sha256"],
        "revision": base["revision"], "upstream_modified": False,
        "adapter_sha256": {"build_lifttors_reduction.py": digest(HERE / "build_lifttors_reduction.py")},
        "generated_sha256": {name: digest(BUILD / name) for name in ["pic_reduction.c", "install.gp"]},
        "library_sha256": digest(library), "command": command,
        "pari_prefix": base["pari_prefix"], "platform": base["platform"],
    }
    (BUILD / "build.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built corrected PicRed separately: {library}")


if __name__ == "__main__":
    main()
