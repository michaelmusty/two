"""D87: numerical pullback of the exact double-cover function to the disk.

This reads saved differential banks; it does not solve for new differentials.
Errors from the geometry and truncated expansions are NOT certified by FLINT
arithmetic balls.  All reported agreements are numerical diagnostics.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

import mpmath as mp

from cm_acb import Backend, evaluate

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data/computed"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def decimal(x):
    return mp.nstr(x, 35)


def pair(z):
    return [decimal(mp.re(z)), decimal(mp.im(z))]


def first_gp_vector(path):
    """The first entry is a JSON-compatible list; later entries contain GP ~."""
    text = Path(path).read_text().strip()
    assert text.startswith("[[")
    depth = 0
    for k in range(1, len(text)):
        depth += (text[k] == "[") - (text[k] == "]")
        if depth == 0:
            return json.loads(text[1:k+1])
    raise ValueError("unterminated first GP vector")


def permutation_sign(p):
    assert sorted(p) == [1, 2, 3]
    return (-1)**sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3))


def side_points(radius):
    raw = json.loads((DATA / "expansion_geometry.json").read_text(), parse_float=str)
    permutations = first_gp_vector(DATA / "genus64_cosets.gp")
    assert len(raw["cm_actions"]) == len(permutations) == 277
    sides = []
    for index, (entry, permutation) in enumerate(zip(raw["cm_actions"], permutations)):
        a, b = [mp.mpc(*z) for z in entry]
        assert abs(abs(a)**2 - abs(b)**2 - 1) < mp.mpf("1e-40")
        rotation = abs(b) < mp.mpf("1e-40")
        w = radius/2 if rotation else -b/a/(1+1/abs(a))
        gw = (a*w+b)/(mp.conj(b)*w+mp.conj(a))
        assert max(abs(w), abs(gw)) < radius
        sides.append({"index_zero_based": index, "w": w, "gw": gw,
                      "v": (w/radius)**32, "gv": (gw/radius)**32,
                      "rotation": rotation, "permutation": permutation,
                      "expected_sign": permutation_sign(permutation)})
    return sides


class Pullback:
    def __init__(self, bank_name):
        self.name = bank_name
        frame = json.loads((DATA / "cm_projective_frame.json").read_text())["banks"][bank_name]
        self.bank_path = Path(frame["source"]["path"])
        assert source(self.bank_path)["sha256"] == frame["source"]["sha256"]
        metadata = json.loads(self.bank_path.with_suffix(".json").read_text())
        self.radius = mp.mpf(str(metadata["radius"]))
        self.backend = Backend(digits=50)
        self.bank = self.backend.read(self.bank_path, rows=metadata["n"], columns=16)
        self.change = mp.matrix([[mp.mpc(*z) for z in row]
                                for row in frame["frame"]["change_matrix"]])
        self.model_path = DATA / "cm_frame_B3_rational_model.json"
        model = json.loads(self.model_path.read_text())
        self.pairs = model["monomial_pairs_zero_based"]
        self.numerator = model["numerator_coefficients"]
        self.denominator = model["denominator_coefficients"]
        first = self.bank.to_mpmath(rows=2) * self.change
        p0, p1 = list(first[0, :]), list(first[1, :])
        constant = self.quadrics(p0)
        n1 = sum(c*(p1[i]*p0[j]+p0[i]*p1[j])
                 for c, (i, j) in zip(self.numerator, self.pairs))
        self.r0 = n1 / constant["d"]
        self.origin = {"n0": pair(constant["n"]), "d0": pair(constant["d"]),
                       "n1": pair(n1), "R0_from_linear_term": pair(self.r0),
                       "numerator_constant_relative_to_linear": decimal(abs(constant["n"]/n1)),
                       "n0_cancellation_ratio": decimal(constant["n_condition"]),
                       "d0_cancellation_ratio": decimal(constant["d_condition"])}

    def quadrics(self, point):
        monomials = [point[i]*point[j] for i, j in self.pairs]
        ns = [c*x for c, x in zip(self.numerator, monomials)]
        ds = [c*x for c, x in zip(self.denominator, monomials)]
        n, d = sum(ns), sum(ds)
        return {"n": n, "d": d, "u": n/d,
                "n_condition": abs(n)/sum(map(abs, ns)),
                "d_condition": abs(d)/sum(map(abs, ds))}

    def values(self, nodes):
        raw = evaluate(self.bank, self.backend.vector(nodes)).to_mpmath()
        coordinates = raw * self.change
        return [self.quadrics(list(coordinates[i, :])) for i in range(len(nodes))]

    def sources(self):
        return [source(p) for p in [Path(__file__), HERE/"cm_acb.py", HERE/"cm_acb.c",
                self.bank_path, self.bank_path.with_suffix(".json"),
                DATA/"cm_projective_frame.json", self.model_path,
                DATA/"expansion_geometry.json", DATA/"genus64_cosets.gp",
                HERE/"66_local_s3_cover.gp", HERE/"67_expansion_geometry.gp",
                HERE.parent/"vendor/rickards-fdom/fdom.c"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", choices=["current", "previous"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output exists; preserve earlier attempts")
    mp.mp.dps = 70
    start = time.monotonic()
    pullback = Pullback(args.bank)
    sides = side_points(pullback.radius)
    result = []
    for first in range(0, len(sides), 32):
        group = sides[first:first+32]
        values = pullback.values([s[k] for s in group for k in ("v", "gv")])
        for side, left, right in zip(group, values[::2], values[1::2]):
            result.append({**{k:v for k,v in side.items() if k not in ("w", "gw", "v", "gv")},
                           **{k:pair(side[k]) for k in ("w", "gw", "v", "gv")},
                           "u_left": pair(left["u"]), "u_right": pair(right["u"]),
                           "u_relative_residual": decimal(abs(right["u"]/left["u"]-1)),
                           "n_cancellation_minimum": decimal(min(left["n_condition"], right["n_condition"])),
                           "d_cancellation_minimum": decimal(min(left["d_condition"], right["d_condition"]))})
        print(json.dumps({"completed_sides": len(result), "seconds": time.monotonic()-start}), flush=True)
    nonrotations = [s for s in result if not s["rotation"]]
    report = {"status": "numerical diagnostic only", "bank": args.bank,
              "sources": pullback.sources(), "origin": pullback.origin,
              "sides": result,
              "nonrotation_u_relative_residual_max": decimal(max(mp.mpf(s["u_relative_residual"]) for s in nonrotations)),
              "side_count": len(result), "rotation_count": len(result)-len(nonrotations),
              "limitations": ["saved geometry is not interval certified",
                              "no rigorous differential truncation bound",
                              "function invariance does not determine square-root character",
                              "complex comparison cannot identify a constant quadratic twist"],
              "wall_seconds": time.monotonic()-start}
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ("bank", "origin", "nonrotation_u_relative_residual_max", "wall_seconds")}), flush=True)


if __name__ == "__main__":
    main()
