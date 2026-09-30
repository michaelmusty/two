"""D87 adapter: speed up interior samples with checked finite-polynomial tails."""
import ctypes as ct
import hashlib
import importlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

core = importlib.import_module("313_cm_frame_double_cover_adaptive")
base = core.base


def library():
    path = base.HERE/"315_cm_frame_double_cover_tail.c"
    flags = shlex.split(subprocess.check_output(["pkg-config", "--cflags", "--libs", "flint"], text=True))
    version = subprocess.check_output(["pkg-config", "--modversion", "flint"], text=True).strip()
    compiler = shlex.split(os.environ.get("CC", "cc"))
    digest = hashlib.sha256(path.read_bytes()+repr((flags, version, compiler)).encode()).hexdigest()[:20]
    target = base.HERE/".build"/f"cover_tail_{digest}.so"
    if not target.exists():
        fd, temporary = tempfile.mkstemp(prefix="cover_tail_", suffix=".so", dir=target.parent)
        os.close(fd)
        try:
            subprocess.run([*compiler, "-std=c11", "-O3", "-Wall", "-Wextra", "-Werror",
                            "-fPIC", "-shared", str(path), "-o", temporary, *flags], check=True)
            os.replace(temporary, target)
        finally:
            Path(temporary).unlink(missing_ok=True)
    lib = ct.CDLL(str(target))
    lib.cover_evaluate2.restype = ct.c_int
    lib.cover_evaluate2.argtypes = [ct.c_void_p]*3+[ct.c_long]*2
    return lib


class Continuation(core.Continuation):
    def __init__(self, bank, bend):
        super().__init__(bank, bend)
        assert max(self.poly.bounds(2)) < core.mp.mpf("1e8"), "finite-polynomial coefficient bound failed"


def main():
    core.library = library
    core.Continuation = Continuation
    core.main()
    path = Path(sys.argv[sys.argv.index("--output")+1])
    record = json.loads(path.read_text())
    record["sources"] += [base.source(Path(__file__)), base.source(base.HERE/"315_cm_frame_double_cover_tail.c")]
    record["evaluation_method"] = "finite polynomial tails bounded in balls below 1e-65 absolute; coefficient bound 1e8 checked"
    path.write_text(json.dumps(record, indent=2)+"\n")
    print("PASS|316_FINITE_TAIL_PATHS", flush=True)


if __name__ == "__main__":
    main()
