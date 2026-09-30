"""D90: enumerate a second bounded shell and retain a mixed CM vector.

The first shell is contained in K. Higher CM derivative kernels require
the perpendicular coordinate too. This is a lattice feasibility check,
not the evaluation of an automorphic differential.
"""
import hashlib
import json
from pathlib import Path

from sage.all import QQ, ZZ, matrix, vector

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"dembele/data/computed"


def main():
    path=DATA/"nelson_cm_lattice_d90.json"
    saved=json.loads(path.read_text())
    Q=matrix(QQ,saved["arithmetic"]["majorant_gram"])
    change=matrix(ZZ,saved["enumeration_pilot"]["reduction_change"])
    den=Q.denominator()
    reduced=change.transpose()*matrix(ZZ,den*Q)*change
    bound=QQ(202)/100
    out=reduced.__pari__().qfminim((den*bound).floor(),100000,0)
    V=matrix(ZZ,out[2])
    assert 2*V.ncols()==int(out[0]), "incomplete shell; retain failure"
    A=matrix(ZZ,saved["CM_lattice_split"]["integral_CM_involution"])
    original=change*V
    parallel_test=(A-1)*original
    perpendicular_test=(A+1)*original
    direct=matrix(QQ,saved["CM_lattice_split"]["parallel_lattice_basis"]).augment(
        matrix(QQ,saved["CM_lattice_split"]["perpendicular_lattice_basis"]))
    in_direct=direct.inverse()*original
    indices=[j for j in range(V.ncols())
             if parallel_test.column(j) != 0 and perpendicular_test.column(j) != 0]
    pure_parallel=sum(parallel_test.column(j)==0 for j in range(V.ncols()))
    pure_perpendicular=sum(perpendicular_test.column(j)==0 for j in range(V.ncols()))
    glued=sum(any(c not in ZZ for c in in_direct.column(j)) for j in range(V.ncols()))
    assert indices and glued
    selected=indices[0]
    v=V.column(selected)
    exact_norm=(v*reduced*v)/den
    assert 0<exact_norm<=bound
    result={"status":"pass: bounded second-shell lattice pilot",
            "majorant_bound":str(bound),"vectors_count_both_signs":int(out[0]),
            "pure_parallel_count":int(2*pure_parallel),
            "pure_perpendicular_count":int(2*pure_perpendicular),
            "mixed_count":2*len(indices),"outside_CM_direct_sum_count":int(2*glued),
            "mixed_representative_order_coordinates":[int(c) for c in original.column(selected)],
            "mixed_representative_Q_norm":str(exact_norm),
            "all_representatives_reduced_coordinates":[[int(c) for c in row] for row in V.transpose().rows()],
            "global_Hilbert_theta_lift_evaluated":False,
            "sources":[{"path":str(p.relative_to(ROOT)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
                       for p in [Path(__file__),path]]}
    target=DATA/"nelson_cm_shell_d90.json"
    assert not target.exists()
    target.write_text(json.dumps(result,indent=2)+"\n")
    print({k:v for k,v in result.items() if k.endswith('count') or k=='vectors_count_both_signs'})
    print("PASS|324_nelson_cm_shell")


if __name__=="__main__":
    main()
