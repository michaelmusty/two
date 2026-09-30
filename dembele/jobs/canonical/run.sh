#!/usr/bin/env bash
# Run from an isolated bundle root; outputs and logs stay inside that bundle.
set -euo pipefail
cd "$(dirname "$0")/../../.."
exec 9>.canonical.lock
flock -n 9 || { echo 'A canonical job is already running'; exit 1; }
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
export PYTHONUNBUFFERED=1
n=${1:-12288}
[[ "$n" =~ ^[0-9]+$ ]] && (( n >= 10240 && n <= 16384 )) || exit 2
data=dembele/data/computed
mkdir -p logs
trap 'code=$?; echo "$code" > exit_code; date -u > finished_at' EXIT
date -u > started_at
sage -python -c 'import sys,numpy,scipy,mpmath,networkx; print(sys.version); print(numpy.__version__,scipy.__version__,mpmath.__version__,networkx.__version__)' > logs/environment.out
sage -python dembele/pari/76_quadric_generation.py > logs/quadric_generation.out 2>&1
output="$data/cm_differentials_${n}_chatelet"
echo "Refining N=$n"
sage -python dembele/pari/68_cm_differentials.py --n "$n" --radius 0.99991 --solver refine --initial "$data/cm_differentials_10240_refined.npz" --replay-digits 50 --output "$output.json" > logs/refine.out 2>&1
echo 'Auditing differential basis'
sage -python dembele/pari/70_differential_audit.py --basis "$output.npz" --output "$data/differential_audit_chatelet.json" > logs/audit.out 2>&1
echo 'Normalizing quadrics'
sage -python dembele/pari/74_canonical_gauge.py --basis "$output.npz" --comparison "$data/cm_differentials_10240_refined.npz" --output "$data/canonical_gauge.json" > logs/gauge.out 2>&1
sage -python dembele/pari/75_gauge_recognition.py > logs/recognition.out 2>&1
sage -python - <<'PY'
import json
from pathlib import Path
d=Path('dembele/data/computed')
a=json.loads((d/'differential_audit_chatelet.json').read_text())
assert a['product_rank_at_relative_1e_minus_7']==45
assert a['quadric_dimension']==91
assert a['degree3_quotient_dimension']==75
assert max(a['precise_generator_check']['relative_residuals'])<1e-7
print('CANONICAL_JOB_OK; numerical equations only')
PY
