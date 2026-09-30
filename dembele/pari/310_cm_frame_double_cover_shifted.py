"""D87: move side samples off elliptic fixed points before taking ratios.

The original balanced-endpoint convolution check failed at common zeros of
all pulled-back differentials.  Keep that failed attempt; reuse its checked
algebraic convolution code at the unused perturbed samples from script 79.
"""
import argparse
import importlib
import json
from pathlib import Path

import mpmath as mp
import numpy as np

prior = importlib.import_module("308_cm_frame_double_cover_paths")
base = prior.base
balanced_sides = base.side_points


def shifted_sides(radius):
    sides = balanced_sides(radius)
    raw = json.loads((base.DATA/"expansion_geometry.json").read_text(), parse_float=str)
    rng = np.random.default_rng(71420)
    for side, entry in zip(sides, raw["cm_actions"]):
        if side["rotation"]:
            continue
        a, b = [mp.mpc(*z) for z in entry]
        perturbation = mp.mpf(".005")*mp.sqrt(float(rng.random()))*mp.exp(2j*mp.pi*float(rng.random()))
        midpoint = side["w"]
        w = (midpoint+perturbation)/(1+mp.conj(midpoint)*perturbation)
        gw = (a*w+b)/(mp.conj(b)*w+mp.conj(a))
        assert max(abs(w), abs(gw)) < radius
        side.update(w=w, gw=gw, v=(w/radius)**32, gv=(gw/radius)**32)
    return sides


base.side_points = shifted_sides


def make_cache(bank):
    prior.make_cache(bank)
    cache, receipt_path = prior.cache_paths(bank)
    receipt = json.loads(receipt_path.read_text())
    backend = prior.Backend(digits=50)
    polynomial = backend.read(cache, receipt["rows"], 2)
    sides, endpoints, _ = prior.folded_points(mp.mpf(receipt["radius"]))
    values = prior.evaluate(polynomial, backend.vector(endpoints)).to_mpmath()
    records = []
    for s in sides:
        record = {k:v for k,v in s.items() if k not in ("w", "gw", "v", "gv")}
        record.update({k:base.pair(s[k]) for k in ("w", "gw", "v", "gv")})
        if s["rotation"]:
            record["rotation_character"] = base.pair((s["gw"]/s["w"])**16)
            record["rotation_v_invariance_error"] = base.decimal(abs(s["gv"]/s["v"]-1))
        else:
            left, right = [values[s[k+"_path"], 0]/values[s[k+"_path"], 1] for k in ("v", "gv")]
            record.update(u_left=base.pair(left), u_right=base.pair(right),
                          u_relative_residual=base.decimal(abs(right/left-1)))
        records.append(record)
    receipt.update(endpoint_strategy="script 79 deterministic hyperbolic perturbations; seed 71420",
                   side_records=records,
                   nonrotation_u_relative_residual_max=base.decimal(max(mp.mpf(s["u_relative_residual"]) for s in records if not s["rotation"])))
    receipt["sources"] += [base.source(Path(__file__)), base.source(base.HERE/"79_acb_refinement.py")]
    receipt_path.write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({k:receipt[k] for k in ("bank", "folded_endpoint_count", "nonrotation_u_relative_residual_max")}), flush=True)
    print("PASS|310_SHIFTED_CACHE", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", choices=["current", "previous"], required=True)
    parser.add_argument("--build-cache", action="store_true")
    parser.add_argument("--first", type=int, default=0)
    parser.add_argument("--stop", type=int, default=550)
    parser.add_argument("--steps", type=int, default=128)
    parser.add_argument("--bend", default="0")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    mp.mp.dps = 70
    if args.build_cache:
        make_cache(args.bank)
    else:
        assert args.output and not args.output.exists(), "preserve earlier path samples"
        prior.run_paths(args)


if __name__ == "__main__":
    main()
