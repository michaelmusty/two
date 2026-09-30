"""Final D90 audit, adding rational interval proofs for the CM majorant.

The archived 325 manifest is preserved. No Sage or numerical library is
needed for this replay, including the eight real-place inequalities.
"""
import argparse
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path

spec=importlib.util.spec_from_file_location("nelson_audit",Path(__file__).with_name("325_nelson_d90_audit.py"))
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
OUTPUT=audit.DATA/"nelson_kernel_d90.json"


def interval_polynomial(coefficients, interval):
    value=(F(0),F(0))
    for c in reversed(coefficients):
        products=[x*y for x in value for y in interval]
        value=(min(products)+c,max(products)+c)
    return value


def majorant_proof(local):
    lower=[-1961570560807,-1662939224606,-1111140466040,-390180644033,
           390180644032,1111140466039,1662939224605,1961570560806]
    intervals=[(F(n,10**12),F(n+1,10**12)) for n in lower]
    polynomial=[F(c) for c in [2,0,-16,0,20,0,-8,0,1]]
    coefficient=[F(c) for c in local["arithmetic"]["majorant_coefficient_power_basis"]]
    records=[]
    for i,(lo,hi) in enumerate(intervals):
        left=interval_polynomial(polynomial,(lo,lo))[0]
        right=interval_polynomial(polynomial,(hi,hi))[0]
        assert left*right<0
        if i:assert intervals[i-1][1]<lo
        sign=-1 if i==4 else 1
        clo,chi=interval_polynomial(coefficient,(lo,hi))
        assert F(sign)-F(1,100)<clo<=chi<F(sign)+F(1,100)
        assert lo>-2 and hi<2
        alo,ahi=interval_polynomial([0,1,-1],(lo,hi))
        assert (alo>0) if i==4 else (ahi<0)
        records.append({"root_interval":[str(lo),str(hi)],
                        "majorant_coefficient_interval":[str(clo),str(chi)],
                        "target_sign":sign})
    # Eight disjoint sign-changing intervals for a degree-eight polynomial
    # account for every real embedding, with exactly one simple root each.
    A=audit.matrix(local["CM_lattice_split"]["integral_CM_involution"])
    change=audit.matrix(local["enumeration_pilot"]["reduction_change"])
    vectors=audit.transpose(audit.matrix(local["enumeration_pilot"]["representatives_in_reduced_basis"]))
    original=audit.multiply(change,vectors)
    assert audit.multiply(A,original)==original
    return {"method":"rational interval Horner arithmetic; eight disjoint sign-changing intervals exhaust degree eight",
            "real_places":records,
            "majorant_relative_error_strict_bound":"1/100",
            "first_shell_pure_K_vectors":2*len(vectors[0])}


def compute():
    result=audit.compute()
    original=json.loads((audit.DATA/"nelson_d90.json").read_text())
    assert result==original
    local=json.loads((audit.DATA/"nelson_cm_lattice_d90.json").read_text())
    result["rational_majorant_proof"]=majorant_proof(local)
    result["sources"] += [audit.source(Path(__file__)),audit.source(audit.DATA/"nelson_d90.json")]
    result["sources"]=sorted(result["sources"],key=lambda v:v["path"])
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--check",action="store_true")
    args=parser.parse_args();result=compute()
    if args.check:assert result==json.loads(OUTPUT.read_text())
    else:
        assert not OUTPUT.exists();OUTPUT.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS: D90 kernel components, 9,910 vectors, eight rational interval proofs;",len(result["sources"]),"hashes")


if __name__=="__main__":main()
