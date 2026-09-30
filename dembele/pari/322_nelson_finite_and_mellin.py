"""D90: finite Fourier pairing and a numerical Mellin-kernel prototype.

The scalar kernel is an analytic building block from the proposed
unfolding, not a claimed global Hilbert Shimizu identity. Calibration
against Nelson's rational Bessel kernel is independent of quadrature.
"""
import argparse
import hashlib
import json
from pathlib import Path

import mpmath as mp
from sage.all import QQ, ZZ, matrix, vector

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"dembele/data/computed"
OUTPUT=DATA/"nelson_finite_mellin_d90.json"


def source(path):
    return {"path":str(path.relative_to(ROOT)),
            "sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def finite_pairing(saved):
    G=matrix(QQ,saved["arithmetic"]["relative_pairing_gram"])
    H=matrix(QQ,saved["arithmetic"]["relative_dual_in_order_coordinates"])
    assert G*H==1
    mod1=lambda v:tuple(c-c.floor() for c in v)
    zero=tuple([QQ(0)]*32)
    elements={zero}
    for v in H.columns():
        elements.update([mod1(vector(QQ,a)+v) for a in list(elements)])
    elements=sorted(elements)
    assert len(elements)==4 and elements[0]==zero
    values=[]
    for v in elements:
        v=vector(QQ,v)
        value=(v*G*v)/2
        values.append(value-value.floor())
    assert values==[0,QQ(1)/2,QQ(1)/2,QQ(1)/2]
    signs=matrix(ZZ,[[(-1)**int(2*((vector(QQ,a)*G*vector(QQ,b))%1))
                     for b in elements] for a in elements])
    assert signs*signs==4
    gauss=sum((-1)**int(2*v) for v in values)/2
    assert gauss==-1
    split=saved["CM_lattice_split"]
    direct=matrix(QQ,split["parallel_lattice_basis"]).augment(
        matrix(QQ,split["perpendicular_lattice_basis"]))
    inv=direct.inverse()
    pilot=saved["enumeration_pilot"]
    change=matrix(QQ,pilot["reduction_change"])
    included=0
    for row in pilot["representatives_in_reduced_basis"]:
        if all(c in ZZ for c in inv*change*vector(QQ,row)):
            included+=2
    return {"discriminant_group_order":4,
            "discriminant_representatives":[[str(c) for c in a] for a in elements],
            "quadratic_values_mod_1":[str(c) for c in values],
            "Fourier_numerator_matrix":[[int(c) for c in row] for row in signs.rows()],
            "Fourier_denominator":2,
            "normalized_Gauss_sum":int(gauss),
            "pilot_vectors_in_CM_direct_sum":included,
            "pilot_vectors_outside_CM_direct_sum":pilot["vectors_count_including_both_signs"]-included,
            "dropping_CM_glue_changes_enumerated_shell":included!=pilot["vectors_count_including_both_signs"]}


def mellin_kernel(degree,k,z,contour):
    """J_d,k(z), integrated up to |Im(s)|=40 (numerical, not interval)."""
    z=mp.mpf(z); c=mp.mpf(contour)
    def f(t):
        s=c+1j*t
        return mp.re((2*s-1)*mp.gamma(s)**degree *
                      mp.gamma(s+1)**(degree-1)*mp.gamma(s+k)*z**(-s))
    return mp.quad(f,[0,1,2,4,8,16,24,40])/mp.pi


def mellin_checks():
    mp.mp.dps=50
    calibration=[]
    for k,z in [(2,"0.2"),(3,"5"),(8,"30")]:
        value=mellin_kernel(1,k,z,"1.25")
        zz=mp.mpf(z); x=2*mp.sqrt(zz)
        bessel=2*zz**(mp.mpf(k)/2)*(x*mp.besselk(k-1,x)-mp.besselk(k,x))
        error=abs(value-bessel)/max(1,abs(bessel))
        assert error<mp.mpf("1e-35")
        calibration.append({"k":k,"z":z,"relative_error":mp.nstr(error,8),
                            "value":mp.nstr(value,30)})
    octic=[]
    # These are exactly the six shifts required by p_{1,1}, p_{3,1},
    # p_{5,1}, after integrating their two monomials at the split place.
    for k in range(3,9):
        value=mellin_kernel(8,k,"1","1.25")
        alternate=mellin_kernel(8,k,"1","1.75")
        error=abs(value-alternate)/max(1,abs(value))
        assert error<mp.mpf("1e-35")
        octic.append({"k":k,"z":"1","value":mp.nstr(value,30),
                      "contour_change_relative_error":mp.nstr(error,8)})
    # Eight separate rational W kernels would instead have gamma(s+k)^8;
    # seven compact places contribute gamma(s+1) without split derivatives.
    ratio=mp.gamma(2+1)**7*mp.gamma(2+2)/mp.gamma(2+2)**8
    assert abs(ratio-mp.mpf(1)/3**7)<mp.mpf("1e-45")
    return {"definition":"J_d,k(z) = integral_(c) (2s-1) Gamma(s)^d Gamma(s+1)^(d-1) Gamma(s+k) z^-s ds/(2*pi*i)",
            "working_decimal_digits":50,"imaginary_cutoff":40,
            "rational_Bessel_calibration":calibration,
            "octic_shift_values":octic,
            "naive_eight_split_factors_rejected":True,
            "interval_error_bound_proved":False,
            "global_unfolding_normalization_proved":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    path=DATA/"nelson_cm_lattice_d90.json"
    saved=json.loads(path.read_text())
    result={"status":"pass: finite calculation and scalar-kernel prototype",
            "finite_pairing":finite_pairing(saved), "Mellin_kernel":mellin_checks(),
            "sources":[source(Path(__file__)),source(path)],
            "Shimura_tangent_computed":False,
            "global_Hilbert_theta_lift_evaluated":False}
    if args.check:
        assert json.loads(OUTPUT.read_text())==result
    else:
        assert not OUTPUT.exists()
        OUTPUT.write_text(json.dumps(result,indent=2)+"\n")
    print("Finite Gauss sum:",result["finite_pairing"]["normalized_Gauss_sum"])
    print("CM glue omission loses pilot vectors:",result["finite_pairing"]["pilot_vectors_outside_CM_direct_sum"])
    print("PASS|322_nelson_finite_and_mellin")


if __name__=="__main__":
    main()
