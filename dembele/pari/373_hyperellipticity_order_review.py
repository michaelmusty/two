"""D99: rerun the exact saved-order audit without old graph/curve outputs.

Uses D62's arithmetic checker on a new export of the actual saved lattice.
This is a rerun, not an independent implementation of the quaternion algebra.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"
spec = importlib.util.spec_from_file_location("order_audit",Path(__file__).with_name("99_curve_identification.py"))
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def source(path):
    path = Path(path).resolve()
    return {"path":str(path),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    raw = old.orbit.export_quaternions(old.orbit.arithmetic.GP)
    order = old.exact_order_check(raw)
    assert order["algebra_finite_discriminant_norm"] == 2
    assert int(order["absolute_reduced_trace_gram_determinant"]) == 2**126
    assert order["unit_signature_rank"] == 8 and order["class_number_proved"] == 1
    paths = [Path(__file__),Path(old.__file__),Path(old.orbit.__file__),
             Path(old.orbit.arithmetic.__file__),DATA/"normalizer_domain.bin",
             Path(old.orbit.arithmetic.GP)]
    vendor = ROOT / "dembele/vendor/rickards-fdom"
    paths += sorted(vendor.glob("*.gp"))+sorted(vendor.glob("*.so"))
    out = {"status":"PASS","order":order,
           "exported_order_basis":raw["order_basis"],
           "sources":[source(p) for p in paths],
           "scope":"Exact order, field and real-place checks only; no analytic polygon or candidate identification."}
    with (DATA/"hyperellipticity_order_review_d99.json").open("x") as f:
        json.dump(out,f,indent=2,sort_keys=True)
        f.write("\n")
    print("PASS|373_HYPERELLIPTICITY_ORDER_REVIEW|2^126 trace determinant|unit signature rank 8")


if __name__ == "__main__":
    main()
