"""D90: run the local kernel calculation with Sage's rounding interface.

The failed prototype 320 and both initial job logs are retained. Also
compute the exact CM lattice splitting and a bounded enumeration pilot.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import time

from sage.all import QQ, ZZ, matrix, vector

spec = importlib.util.spec_from_file_location("nelson_local", Path(__file__).with_name("320_nelson_local_kernel.py"))
local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(local)
# Python's round() has no implementation for Sage RealNumber. The retained
# prototype uses it once when choosing rational interpolation coefficients.
local.round = lambda value: value.round()


def cm_lattice_split(arithmetic):
    saved = json.loads((local.DATA / "cm_orbit.json").read_text())
    raw = saved["quaternion_export"]
    from sage.all import NumberField, PolynomialRing, QuaternionAlgebra
    R = PolynomialRing(QQ,"s"); s = R.gen()
    F = NumberField(s**8-8*s**6+20*s**4-16*s**2+2,"b"); b=F.gen()
    B = QuaternionAlgebra(F,b-b*b,-1)
    def q(v):
        return B([F([QQ(c) for c in v[8*j:8*(j+1)]]) for j in range(4)])
    def coords(x):
        return vector(QQ,sum([list(c.vector()) for c in x.coefficient_tuple()],[]))
    basis = [q(v) for v in raw["order_basis"]]
    lattice = matrix(QQ,[coords(x) for x in basis]).transpose()
    beta = q(arithmetic["CM_beta_power_coordinates"])
    involution = lattice.inverse()*matrix(QQ,[coords(beta*x*beta**(-1)) for x in basis]).transpose()
    assert involution**2 == 1 and all(c in ZZ for c in involution.list())
    plus = matrix(ZZ,involution-1).right_kernel().basis_matrix().transpose()
    minus = matrix(ZZ,involution+1).right_kernel().basis_matrix().transpose()
    assert plus.ncols()==minus.ncols()==16
    direct = plus.augment(minus)
    invariants = [abs(int(x)) for x in direct.smith_form()[0].diagonal()]
    assert all(x in (1,2) for x in invariants)
    gram = matrix(QQ,arithmetic["majorant_gram"])
    assert plus.transpose()*gram*minus == 0
    return {"integral_CM_involution": local.rows(involution),
            "parallel_lattice_basis": local.rows(plus),
            "perpendicular_lattice_basis": local.rows(minus),
            "direct_sum_index": int(abs(direct.det())),
            "glue_invariants": sorted(invariants),
            "orthogonal_for_majorant": True}


def enumeration_pilot(arithmetic):
    """Exact rational majorant shell, not a truncated global lift.

    qfminim lists one representative per +/- pair. Its integer-matrix
    algorithm is used after clearing denominators; no floating Gram is
    used to define the search region.
    """
    gram = matrix(QQ, arithmetic["majorant_gram"])
    den = gram.denominator()
    integral = matrix(ZZ, den*gram)
    # Reduce before enumeration. PARI qflllgram flag 1 is exact integral.
    change = matrix(ZZ, integral.__pari__().qflllgram(1))
    assert abs(change.det()) == 1
    reduced = change.transpose()*integral*change
    bound = QQ(101)/100
    started=time.monotonic()
    enumeration = reduced.__pari__().qfminim((den*bound).floor(), 100000, 0)
    count = int(enumeration[0])
    vectors = matrix(ZZ,enumeration[2])
    assert vectors.ncols()*2 == count, "truncated vector list"
    norms = [(v*reduced*v)/den for v in vectors.columns()]
    assert all(0<n<=bound for n in norms)
    return {"majorant_bound": str(bound), "vectors_count_including_both_signs":count,
            "representative_count":vectors.ncols(),
            "all_vectors_returned":True,
            "minimum_in_enumerated_shell": str(min(norms)) if norms else None,
            "reduction_change":local.rows(change),
            "representatives_in_reduced_basis":local.rows(vectors.transpose()),
            "purpose":"finite lattice pilot; no section value or tail bound"},time.monotonic()-started


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    result=local.compute()
    result["CM_lattice_split"]=cm_lattice_split(result["arithmetic"])
    result["enumeration_pilot"],elapsed=enumeration_pilot(result["arithmetic"])
    result["sources"].append(local.source(Path(__file__)))
    path=local.DATA/"nelson_cm_lattice_d90.json"
    if args.check:
        assert json.loads(path.read_text())==result
    else:
        assert not path.exists()
        path.write_text(json.dumps(result,indent=2)+"\n")
    print("CM direct-sum index:",result["CM_lattice_split"]["direct_sum_index"])
    print("Pilot vectors:",result["enumeration_pilot"]["vectors_count_including_both_signs"],"seconds",elapsed)
    print("PASS|321_nelson_cm_lattice")


if __name__=="__main__":
    main()
