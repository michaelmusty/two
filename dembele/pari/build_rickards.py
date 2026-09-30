"""Build the pinned Rickards checkout against an existing PARI installation."""
import argparse
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
VENDOR = HERE.parent / 'vendor/rickards-fdom'
REVISION = '79a12d3f108edce3e78d30c4a59dfc0fb01012d8'
DEFAULT = '/Applications/SageMath-10-6.app/Contents/Frameworks/Sage.framework/Versions/10.6/local'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pari-local', type=Path, default=Path(DEFAULT))
args = parser.parse_args()
prefix = args.pari_local.resolve()
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=VENDOR, text=True).strip()
if revision != REVISION:
    raise SystemExit(f'Expected {REVISION}, found {revision}; review before building a different revision')
patch = str(HERE / 'rickards-pari-2.17.patch')
if subprocess.run(['git', 'apply', '--reverse', '--check', patch], cwd=VENDOR,
                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
    subprocess.run(['git', 'apply', '--check', patch], cwd=VENDOR, check=True)
    subprocess.run(['git', 'apply', patch], cwd=VENDOR, check=True)
# Sage's bundled pari.cfg contains build-machine include/lib paths. Override
# those at make time rather than editing the installed PARI configuration.
(VENDOR / 'fdom.cfg').write_text(f"CFG='{prefix}/lib/pari/pari.cfg'\nOS='Mac'\n")
loader = VENDOR / 'fdom.gp'
source = loader.read_text()
source = re.sub(r'^fdom_library = .*$',
                f'fdom_library = strprintf("{VENDOR}/libfdom-%d-%d-%d.so", '
                'parigp_version[1], parigp_version[2], parigp_version[3]);',
                source, flags=re.MULTILINE)
loader.write_text(source)
subprocess.run(['make', f'PARI_LIB={prefix}/lib', f'PARI_INCLUDE={prefix}/include/pari'],
               cwd=VENDOR, check=True)
print(f'Built Rickards {REVISION} against {prefix}; run the smoke check next')
