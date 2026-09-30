"""Deploy an isolated, hash-verified canonical computation, or inspect it.

Uses the existing CoCalc credentials without printing or uploading them.
"""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import re
import shlex
import sys
import tarfile

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from remote_magma.cocalc import env,rexec

FILES=[f'dembele/pari/{name}' for name in (
    '68_cm_differentials.py','70_differential_audit.py',
    '74_canonical_gauge.py','75_gauge_recognition.py','76_quadric_generation.py')]
FILES += [f'dembele/data/computed/{name}' for name in (
    'expansion_geometry.json','stable_graph_audit.json',
    'cm_differentials_10240_refined.npz','cm_differentials_4096_fullradius.npz',
    'cm_differentials_8192_eigen.npz')]
FILES += ['dembele/jobs/canonical/run.sh']


def bundle():
    stream=io.BytesIO()
    manifest={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES}
    with tarfile.open(fileobj=stream,mode='w:gz') as archive:
        for name in FILES:
            archive.add(ROOT/name,arcname=name,recursive=False)
        raw=json.dumps(manifest,indent=2).encode()
        info=tarfile.TarInfo('inputs.sha256.json'); info.size=len(raw)
        archive.addfile(info,io.BytesIO(raw))
    return stream.getvalue()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['bundle','deploy','status','fetch'])
    p.add_argument('--remote',default='two_canonical_d46_20260915')
    p.add_argument('--n',type=int,default=12288)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    if not re.fullmatch(r'two_canonical_[a-zA-Z0-9_]+',args.remote):
        p.error('remote must be an isolated two_canonical_* directory name')
    if not 10240<=args.n<=16384:
        p.error('n must be between 10240 and 16384')
    if args.action=='bundle':
        if not args.output: p.error('bundle requires --output')
        raw=bundle(); args.output.write_bytes(raw)
        print(f'Bundle: {len(raw)} bytes; {len(FILES)} input files')
        return
    conf=env(); remote=shlex.quote(args.remote)
    def call(command,**kw):
        result=rexec(conf,command,**kw)
        if result.get('sock_timeout'):
            raise RuntimeError('Socket timeout: inspect status before retrying a launch or upload')
        if result.get('exit_code')!=0:
            raise RuntimeError(f"Remote command failed: {result.get('stderr')} {result.get('stdout')}")
        return result.get('stdout','')
    if args.action=='status':
        print(call(f'cd {remote} && for f in started_at finished_at exit_code runner.out; do if test -f "$f"; then cat "$f"; fi; done; if test -f pid; then ps -p "$(cat pid)" -o pid,etime,time,rss,args || true; fi'))
        return
    if args.action=='fetch':
        if not args.output: p.error('fetch requires --output (a new local archive path)')
        if args.output.exists(): p.error('output already exists')
        # Results are fetched only after the runner has stopped writing.
        call(f'cd {remote} && test -f exit_code && tar czf results.tgz logs dembele/data/computed inputs.sha256.json started_at finished_at exit_code runner.out')
        size=int(call(f'wc -c < {remote}/results.tgz').strip())
        expected=call(f'sha256sum {remote}/results.tgz').split()[0]
        raw=bytearray()
        for offset in range(0,size,48000):
            encoded=call(f'dd if={remote}/results.tgz bs=1 skip={offset} count=48000 status=none | base64 -w0')
            raw.extend(base64.b64decode(encoded))
        assert len(raw)==size and hashlib.sha256(raw).hexdigest()==expected
        args.output.write_bytes(raw); print(f'Fetched and verified {size} bytes')
        return
    raw=bundle()
    # mkdir refuses an existing directory: never replace a job or banked data.
    call(f'mkdir {remote}')
    encoded=base64.b64encode(raw).decode()
    count=(len(encoded)+63999)//64000
    for i,start in enumerate(range(0,len(encoded),64000),1):
        call(f"printf '%s' '{encoded[start:start+64000]}' >> {remote}/bundle.b64",timeout=300)
        if i%10==0 or i==count: print(f'Uploaded {i}/{count} chunks',flush=True)
    digest=hashlib.sha256(raw).hexdigest()
    call(f'cd {remote} && base64 -d bundle.b64 > bundle.tgz && echo "{digest}  bundle.tgz" | sha256sum -c - && tar xzf bundle.tgz',timeout=300)
    verify="import json,hashlib,pathlib; m=json.loads(pathlib.Path('inputs.sha256.json').read_text()); assert all(hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h for p,h in m.items()); print('INPUT_HASHES_OK')"
    print(call(f'cd {remote} && python3 -c {shlex.quote(verify)}'))
    print(call(f'cd {remote} && (nohup bash dembele/jobs/canonical/run.sh {args.n} > runner.out 2>&1 < /dev/null & echo $! > pid)',timeout=259200,sock_timeout=60))
    print(f'Launched in {args.remote}; use status to inspect completion',flush=True)


if __name__=='__main__':
    main()
