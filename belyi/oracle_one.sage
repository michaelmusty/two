load("belyi/combinatorial_tower.sage")
import sys
o,g,q = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
print(f"ORACLE [{o},{g}] quo{q}:")
for (s,ram,gb,ok) in run_oracle(o,g,q,verbose=False):
    print(f"  step {s}: ramify {ram}  base-genus {gb}  span={'PASS' if ok else 'FAIL'}")
