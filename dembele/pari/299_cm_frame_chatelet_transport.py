"""D86: hash-verified incremental uploads and immutable remote Magma jobs.

Only explicitly enumerated mathematical sources/data and the remote worker
are uploaded. The configured API credentials remain local.
"""
import base64
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import shlex
import sys
import tarfile
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from remote_magma.cocalc import env, rexec

DATA = ROOT / "dembele/data/computed"
REMOTE = "two_remote_magma/dembele_d86_128_20260922"
WORKER = ROOT / "dembele/pari/298_cm_frame_remote_worker.py"
LOCAL = DATA / "chatelet_d86_128"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def immutable(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == data, path
    else:
        path.write_bytes(data)


def call(command, timeout=120, max_output=2000000, sock_timeout=45):
    result = rexec(env(), command, timeout=timeout, max_output=max_output, sock_timeout=sock_timeout)
    if result.get("sock_timeout"):
        raise RuntimeError("Chatelet socket timeout; inspect the saved job before retrying")
    if result.get("exit_code") != 0:
        raise RuntimeError("Chatelet command failed: "+result.get("stderr", "")+result.get("stdout", ""))
    return result.get("stdout", "")


def python(code, **kwargs):
    return call("python3 -c "+shlex.quote(code), **kwargs)


def magma_inputs(wrapper):
    paths = set()
    def visit(path):
        path = path.resolve()
        if path in paths:
            return
        assert path.is_relative_to(ROOT) and path.suffix == ".m"
        paths.add(path)
        for name in re.findall(r'load\s+"([^"]+)"\s*;', path.read_text()):
            child = Path(name)
            assert not child.is_absolute(), "Remote loads must be repository relative"
            visit(ROOT / child)
    visit(wrapper)
    return paths


def upload_files(paths):
    manifest = {str(p.relative_to(ROOT)): source(p)["sha256"] for p in sorted(paths)}
    code = ("import hashlib,json,pathlib; root=pathlib.Path("+repr(REMOTE)+
        "); root.mkdir(parents=True,exist_ok=True); manifest="+repr(manifest)+
        "; missing=[]\nfor name,digest in manifest.items():\n p=root/name\n"
        " if p.exists():\n  assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name\n"
        " else: missing.append(name)\nprint(json.dumps(missing))")
    missing = json.loads(python(code))
    if not missing:
        return manifest
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as tar:
        for name in missing:
            tar.add(ROOT / name, arcname=name, recursive=False)
    raw = gzip.compress(stream.getvalue(), mtime=0); digest = hashlib.sha256(raw).hexdigest()
    bundle_name = REMOTE+"/upload_"+digest
    # An interrupted transfer has individually immutable chunks and is resumable.
    encoded = base64.b64encode(raw).decode()
    chunks = [encoded[i:i+64000] for i in range(0, len(encoded), 64000)]
    for index, chunk in enumerate(chunks):
        name = bundle_name+f"_{index:05d}.part"
        python("from pathlib import Path; p=Path("+repr(name)+
            "); text="+repr(chunk)+"; assert not p.exists() or p.read_text()==text; p.write_text(text)")
        if (index+1) % 25 == 0 or index+1 == len(chunks):
            print("CHATELET_UPLOAD", index+1, "/", len(chunks), "chunks;", len(missing), "new files", flush=True)
    code = ("import base64,hashlib,io,pathlib,tarfile; root=pathlib.Path("+repr(REMOTE)+
        "); raw=base64.b64decode(''.join(pathlib.Path("+repr(bundle_name)+
        "+f'_{i:05d}.part').read_text() for i in range("+str(len(chunks))+"))); "
        "assert hashlib.sha256(raw).hexdigest()=="+repr(digest)+"; manifest="+repr(manifest)+
        "; tar=tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz')\n"
        "for entry in tar.getmembers():\n assert entry.isfile() and entry.name in manifest\n"
        " data=tar.extractfile(entry).read(); assert hashlib.sha256(data).hexdigest()==manifest[entry.name]\n"
        " p=root/entry.name; p.parent.mkdir(parents=True,exist_ok=True)\n"
        " if p.exists(): assert p.read_bytes()==data\n else: p.write_bytes(data)\n"
        "print('REMOTE_INPUT_HASHES_OK')")
    assert "REMOTE_INPUT_HASHES_OK" in python(code, timeout=300)
    return manifest


def execute(wrapper, base, marker, expected_failure=None):
    assert re.fullmatch(r"[A-Za-z0-9_]+", base.name)
    paths = magma_inputs(wrapper) | {WORKER}
    manifest = upload_files(paths)
    local = LOCAL / base.name; local.mkdir(parents=True, exist_ok=True)
    remote_job = REMOTE+"/jobs/"+base.name
    spec = {"wrapper": str(wrapper.relative_to(ROOT)), "inputs": manifest,
        "marker": marker, "expected_failure": expected_failure,
        "timeout_seconds": 1800, "memory_limit_bytes": 8000000000}
    spec_raw = (json.dumps(spec, indent=2)+"\n").encode()
    immutable(local / "spec.json", spec_raw)
    code = ("from pathlib import Path; import base64; p=Path("+repr(remote_job+"/spec.json")+
        "); p.parent.mkdir(parents=True,exist_ok=True); raw=base64.b64decode("+
        repr(base64.b64encode(spec_raw).decode())+
        "); assert not p.exists() or p.read_bytes()==raw; p.write_bytes(raw)")
    python(code)
    state = python("from pathlib import Path; p=Path("+repr(remote_job)+
        "); print('done' if (p/'status.json').exists() else 'started' if (p/'started.json').exists() or (p/'launcher.pid').exists() else 'new')").strip()
    if state == "new":
        worker_cmd = ["python3", str(WORKER.relative_to(ROOT)), "jobs/"+base.name+"/spec.json"]
        launch = ("cd "+shlex.quote(REMOTE)+" && (nohup "+shlex.join(worker_cmd)+
            " > "+shlex.quote("jobs/"+base.name+"/worker.log")+
            " 2>&1 < /dev/null & echo $! > "+shlex.quote("jobs/"+base.name+"/launcher.pid")+")")
        response = rexec(env(), launch, timeout=86400, sock_timeout=45)
        immutable(local / "launch.json", (json.dumps(response, indent=2)+"\n").encode())
        if not response.get("sock_timeout") and response.get("exit_code") != 0:
            raise RuntimeError("Remote launch failed; inspect the launch receipt")
        print("CHATELET_LAUNCHED", base.name, "8 GB / 1800 seconds", flush=True)
    # No job is relaunched on an ambiguous network result. Poll its durable state.
    while True:
        status = python("from pathlib import Path; p=Path("+repr(remote_job)+
            "); print((p/'status.json').read_text() if (p/'status.json').exists() else '{}')")
        result = json.loads(status)
        if result:
            break
        diagnostic = python("from pathlib import Path; p=Path("+repr(remote_job)+
            "); print((p/'worker.log').read_text()[-2000:] if (p/'worker.log').exists() else '')")
        if "Traceback" in diagnostic:
            raise RuntimeError("Remote worker failed: "+diagnostic)
        print("CHATELET_RUNNING", base.name, flush=True)
        time.sleep(20)
    immutable(local / "remote_status.json", (json.dumps(result, indent=2)+"\n").encode())
    pack = python("import gzip,hashlib,json; from pathlib import Path; p=Path("+repr(remote_job)+
        "); raw=(p/'output.log').read_bytes(); z=gzip.compress(raw); (p/'output.log.gz').write_bytes(z); "
        "print(json.dumps({'bytes':len(z),'sha256':hashlib.sha256(z).hexdigest()}))")
    pack = json.loads(pack); compressed = bytearray()
    for offset in range(0, pack["bytes"], 240000):
        encoded = python("import base64; from pathlib import Path; p=Path("+repr(remote_job+"/output.log.gz")+
            "); f=p.open('rb'); f.seek("+str(offset)+"); print(base64.b64encode(f.read(240000)).decode())",
            max_output=400000)
        compressed.extend(base64.b64decode(encoded))
    assert len(compressed) == pack["bytes"]
    assert hashlib.sha256(compressed).hexdigest() == pack["sha256"]
    raw = gzip.decompress(compressed)
    assert len(raw) == result["output_bytes"] and hashlib.sha256(raw).hexdigest() == result["output_sha256"]
    immutable(base.with_suffix(".out"), raw)
    record = dict(result, log=source(base.with_suffix(".out")), execution_host="chatelet.mit.edu",
        remote_directory=remote_job,
        sources=[source(p) for p in sorted(paths | {Path(__file__), ROOT / "remote_magma/cocalc.py",
            local / "spec.json", local / "remote_status.json"})])
    if (local / "launch.json").exists():
        record["sources"].append(source(local / "launch.json"))
    print("CHATELET_FINISHED", base.name, result["status"], round(result["wall_seconds"], 3),
          "peak RSS", result["maximum_resident_bytes"], flush=True)
    return record
