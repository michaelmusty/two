"""B1: LMFDB genus-2 scan for nonsolvable Q(J[2]) among 2-power-conductor curves.
Run in the venv:  . .venv/bin/activate && python3 lmfdb_genus2_scan.py
For genus 2, g2c_curves.two_torsion_field = [nf_label, poly, [deg,Tnum], flag];
[deg,Tnum] is Gal(Q(J[2])) in nTt notation.  Nonsolvable nTt among g2c:
5T4=A5, 5T5=S5, 6T15=A6, 6T16=S6.  Result: 0 nonsolvable at 2-power conductor.
"""
from lmf import db

NONSOLV = {(5, 4), (5, 5), (6, 15), (6, 16)}   # A5, S5, A6, S6

def is_two_power(n):
    return n > 1 and (n & (n - 1)) == 0

def main():
    tot = ns = ns_2pow = twopow = twopow_solv = 0
    for r in db.g2c_curves.search({}, ['cond', 'two_torsion_field']):
        ttf = r['two_torsion_field']
        if not ttf or not ttf[2]:
            continue
        tot += 1
        key = tuple(ttf[2])
        nonsolv = key in NONSOLV
        twop = is_two_power(r['cond'])
        ns += nonsolv
        twopow += twop
        if nonsolv and twop:
            ns_2pow += 1
        if twop and not nonsolv:
            twopow_solv += 1
    print(f"g2c curves with two_torsion_field: {tot}")
    print(f"  nonsolvable Q(J[2]):            {ns}")
    print(f"  conductor a power of 2:         {twopow}")
    print(f"  BOTH (the prize in genus 2):    {ns_2pow}")
    print(f"  2-power conductor & solvable:   {twopow_solv}")

if __name__ == "__main__":
    main()
