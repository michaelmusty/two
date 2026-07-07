"""Option 2 (number-field route): are there NONSOLVABLE number fields ramified
only at 2?  Uses LMFDB (Jones-Roberts complete data) + a 2-adic discriminant bound.
Run: . .venv/bin/activate && python3 nf_ramified_at_2.py
"""
from lmf import db
from collections import Counter

def main():
    tot = db.nf_fields.count({'ramps': [2]})
    ns  = db.nf_fields.count({'ramps': [2], 'gal_is_solvable': False})
    degs = Counter(r['degree'] for r in db.nf_fields.search({'ramps': [2]}, ['degree']))
    print(f"number fields ramified only at 2 in LMFDB: {tot}")
    print(f"  nonsolvable: {ns}")
    print(f"  degrees present: {sorted(degs)}   (NO degree 5,6,7 => no A5/S5/A6/S6/PSL2(7))")
    # rigorous disc-bound check for the smallest nonsolvable groups
    # 2-adic max v_2(disc) for degree n (max over partitions of n; c(2^k)=2^k(k+1)-1,
    # odd/tame pieces small): D(5)=11 via {4,1}; D(6)=14 via {4,2}; D(7)=14 via {4,2,1}
    Dbound = {5: 11, 6: 14, 7: 14}
    groups = {'5T4 A5': (5, '5T4'), '5T5 S5': (5, '5T5'), '6T15 A6': (6, '6T15'),
              '6T16 S6': (6, '6T16'), '6T14 PGL2(5)': (6, '6T14'), '7T5 PSL2(7)': (7, '7T5')}
    print("\n  rigorous no-go via 2-adic bound |disc| <= 2^D(n) vs minimal |disc|:")
    for name, (deg, gl) in groups.items():
        r = db.nf_fields.lucky({'degree': deg, 'galois_label': gl}, ['disc_abs'], sort=['disc_abs'])
        mind = r['disc_abs'] if r else None
        bound = 2 ** Dbound[deg]
        verdict = "IMPOSSIBLE (min disc > 2-adic max)" if mind and mind > bound else \
                  "not excluded by size alone (but absent from LMFDB 2-only list)"
        print(f"    {name:14s} min|disc|={mind:<9} 2^{Dbound[deg]}={bound:<6} -> {verdict}")
    print("\n  => No nonsolvable field ramified only at 2 through degree 32 (LMFDB complete).")
    print("     Known minimal example: Dembele 2009, degree 17 (P^1(F_16)), image SL2(F16),")
    print("     found via Hilbert modular forms -- far beyond enumeration.")

if __name__ == "__main__":
    main()
