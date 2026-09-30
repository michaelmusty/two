"""D93 adapter for the frozen D92 exhaustive interval enumerator."""
import argparse
import importlib.util
import json
from pathlib import Path
from sage.all import QQ,ZZ,matrix

spec=importlib.util.spec_from_file_location("coverage",Path(__file__).with_name("340_nelson_norm_one_coverage.py"))
coverage=importlib.util.module_from_spec(spec);spec.loader.exec_module(coverage)
DATA=coverage.DATA


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--bound",type=int,default=6400);args=p.parse_args()
    path=DATA/f"nelson_prime31_b27_d93_T{args.bound}.json";packet=json.loads(path.read_text())
    out=DATA/f"nelson_prime31_coverage_d93_T{args.bound}.json";assert not out.exists()
    m=packet["majorant"];G=matrix(QQ,m["gram"]);change=matrix(ZZ,m["reduction_change"]);assert abs(change.det())==1
    print("INTERVAL_ENUM_START",args.bound,flush=True)
    found,proof=coverage.enumerate_exact(change.transpose()*G*change,QQ(m["cutoff"]))
    expected={coverage.canonical(v) for v in packet["enumeration"]["representatives_reduced_coordinates"]}
    assert None not in expected and len(expected)*2==packet["enumeration"]["vectors_including_both_signs"]
    assert found==expected
    corrupt=set(expected);corrupt.pop();assert corrupt!=found
    result={"status":"pass: exhaustive interval enumeration equals saved prime-norm list",
            "invariant_A_cutoff":args.bound,"interval_precision_bits":256,"signed_pair_count":len(found),
            "proof":proof,"depends_on_qfminim_roundoff_guarantee":False,"omitted_vector_control_rejected":True,
            "sources":[coverage.source(p) for p in [Path(__file__),Path(coverage.__file__),path]]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|345_nelson_prime31_coverage")


if __name__=="__main__":main()
