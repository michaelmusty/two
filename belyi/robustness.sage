load("belyi/combinatorial_tower.sage")
from sage.all import randint
import sys
o,g,q = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
TRIALS = int(sys.argv[4]) if len(sys.argv)>4 else 40
# find the positive-genus rung(s); tally span PASS/FAIL across randomized radicand choices
from collections import Counter
tally = {}
for _ in range(TRIALS):
    v = run_oracle(o,g,q,verbose=False,randomize=True)
    for (s,ram,gb,ok) in v:
        if gb>0:
            tally.setdefault((s,gb), Counter())['PASS' if ok else 'FAIL'] += 1
print(f"ROBUSTNESS [{o},{g}] quo{q}, {TRIALS} randomized radicand-choice trials:")
for (s,gb),c in sorted(tally.items()):
    print(f"  step {s} (base-genus {gb}): {dict(c)}")
