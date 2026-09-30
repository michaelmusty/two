"""Run a bounded Rickards computation and publish artifacts only after PASS."""
import argparse
import json
import os
import re
from pathlib import Path
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
DEMBELE = HERE.parent
SAGE_LOCAL = Path('/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/10.6/local')

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('stage', choices=['smoke', 'domain', 'cover', 'geometry', 'cover-geometry'])
parser.add_argument('--gp', default=os.environ.get('GP', str(SAGE_LOCAL / 'bin/gp')))
parser.add_argument('--timeout', type=float, default=600)
args = parser.parse_args()
vendor = DEMBELE / 'vendor/rickards-fdom'
data = DEMBELE / 'data/computed'
names = {'smoke': 'rickards_smoke', 'domain': 'normalizer_domain', 'cover': 'local_s3_cover', 'geometry': 'expansion_geometry', 'cover-geometry': 'cover_geometry'}
markers = {'smoke': 'PASS|rickards_smoke', 'domain': 'PASS|65_normalizer_domain', 'cover': 'PASS|66_local_s3_cover', 'geometry': 'PASS|67_expansion_geometry', 'cover-geometry': 'PASS|80_cover_geometry'}
scripts = {'domain': '65_normalizer_domain.gp', 'cover': '66_local_s3_cover.gp', 'geometry': '67_expansion_geometry.gp', 'cover-geometry': '80_cover_geometry.gp'}

with tempfile.TemporaryDirectory(prefix='.fdom-', dir=data) as temp:
    commands = 'default(parisizemax,2000000000);\nread("fdom.gp");\n'
    commands += 'fdom_output=' + json.dumps(temp) + ';\n'
    if args.stage == 'smoke':
        commands += '''{
F=nfinit(y^2-11); A=alginit(F,[y-3,-3]); X=afuchinit(A);
print("SMOKE|signature=",afuchsignature(X));
if(afuchsignature(X)[1]!=0 || Vec(afuchsignature(X)[2])!=[2,3,3,3,3],error("wrong smoke signature"));
if(afuchcheck(X)!=0,error("smoke validation failed"));
print("PASS|rickards_smoke");
}
'''
    else:
        commands += 'read(' + json.dumps(str(HERE / scripts[args.stage])) + ');\n'
    commands += 'quit;\n'
    log = data / (names[args.stage] + '.out')
    started = time.monotonic()
    with log.open('w') as out:
        try:
            result = subprocess.run([args.gp, '-fq', '-s', '128000000'], input=commands,
                                    text=True, cwd=vendor, stdout=out,
                                    stderr=subprocess.STDOUT, timeout=args.timeout)
            code = result.returncode
            out.write(f'RUNNER|exit={code}; wall_seconds={time.monotonic()-started:.3f}\n')
        except subprocess.TimeoutExpired:
            code = 124
            out.write(f'RUNNER|TIMEOUT after {args.timeout} seconds; child terminated\n')
    output = log.read_text()
    # GP can exit zero after an error. The script must reach its final marker.
    if code or markers[args.stage] not in output:
        raise SystemExit(f'FAILED: inspect {log}')
    for artifact in Path(temp).iterdir():
        if artifact.suffix == '.json':
            # GP prints small values as "1.23 E-50" and exact real zeros
            # as "0.E-50". Preserve the digits while making valid JSON.
            content = re.sub(r'\s+E\s*([+-]?\d+)', r'e\1', artifact.read_text())
            content = re.sub(r'(\d)\.(?=[Ee])', r'\1.0', content)
            json.loads(content)
            artifact.write_text(content)
        os.replace(artifact, data / artifact.name)
    print(f'{markers[args.stage]} ({time.monotonic()-started:.3f}s); {log}')
