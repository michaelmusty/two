"""D72: exact successive 31-adic lifts of the D71 radicand.

Work in finite etale algebras over Z/31^n, with no floating-point or
characteristic-zero recognition. Keep the numerator's 13 free section
coordinates fixed; solve 44 linear conditions for the denominator and
then move its 16 double zeros. A separate Magma certificate checks the
exported points, jets, multiplicities and degree accounting.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import time

from sage.all import GF, Zmod, PolynomialRing, PowerSeriesRing, matrix, vector


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/"dembele/data/computed"
P = 31
MODULUS = P*P
DIGITS = 2
STEP = P
K0 = GF(P)
BASE = Zmod(MODULUS)


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_supports(text):
    assert "PASS|123_CM_FRAME_LIFT_SUPPORTS" in text
    assert not any(s in text for s in ("Runtime error", "User error", "Assertion failed", "Error:"))
    out = {}
    for part in re.split(r"^SUPPORT\|",text,flags=re.M)[1:]:
        label,degree = part.splitlines()[0].split("|")
        h = ast.literal_eval(re.search(r"^MODULUS\|(.*?)\nCOORDINATES",part,re.M|re.S).group(1))
        xs = ast.literal_eval(re.search(r"^COORDINATES\|(.*?)\nFACTOR_DEGREES",part,re.M|re.S).group(1))
        out[label] = {"degree": int(degree), "modulus": h, "coordinates": xs}
    out["D17_extra_rows"] = ast.literal_eval(
        re.search(r"^D17_EXTRA_ROWS\|(.*?)\nCPU_SECONDS",text,re.M|re.S).group(1))
    return out


def evaluate(row,xs,pairs):
    ans = xs[0].parent()(0)
    for c,(i,j) in zip(row,pairs):
        if c:
            ans += c*xs[i]*xs[j]
    return ans


def gradient(row,xs,pairs):
    ans = [xs[0].parent()(0) for _ in xs]
    for c,(i,j) in zip(row,pairs):
        if c:
            ans[i] += c*xs[j]
            ans[j] += c*xs[i]
    return ans


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


class Component:
    """One residue-field factor, represented by a fixed monic etale lift."""
    def __init__(self,label,f,coordinates,curve,pairs,previous=None):
        self.label = label
        self.degree = int(f.degree())
        self.modulus = [int(c) for c in f.list()]
        if self.degree == 1:
            self.K = K0
            self.root = -f[0]
        else:
            self.K = GF(P**self.degree,name="a",modulus=f)
            self.root = self.K.gen()
        T = PolynomialRing(BASE,"z")
        self.A = T.quotient(T(self.modulus),"b")
        self.x0 = [sum(self.K(c)*self.root**i for i,c in enumerate(row)) for row in coordinates]
        assert self.x0[14] == self.root and self.x0[15] == 1
        assert all(evaluate(q,self.x0,pairs) == 0 for q in curve)
        self.x = ([self.lift(x) for x in self.x0] if previous is None
                  else [self.A(row) for row in previous["coordinates"]])
        assert [self.reduce(x) for x in self.x] == self.x0
        J = matrix(self.K,[gradient(q,self.x0,pairs)[:14] for q in curve])
        self.curve_indices = list(J.transpose().pivots())
        assert len(self.curve_indices) == 14
        self.J0 = J.matrix_from_rows(self.curve_indices)
        self.J0_inverse = self.J0.inverse()

    def coefficients(self,a):
        a = self.A(a)
        cs = [int(c) for c in a.lift().list()]
        return cs+[0]*(self.degree-len(cs))

    def lift(self,a):
        return self.A([int(c) for c in self.K(a).polynomial().list()])

    def reduce(self,a):
        return sum(self.K(c%P)*self.root**i for i,c in enumerate(self.coefficients(a)))

    def divide_power(self,a,exponent):
        cs = self.coefficients(a)
        power = P**exponent
        assert all(c%power == 0 for c in cs)
        return sum(self.K(c//power)*self.root**i for i,c in enumerate(cs))

    def divide_step(self,a):
        return self.divide_power(a,DIGITS-1)

    def solve_A(self,M,b):
        """Solve a unit matrix over A using its residue-field inverse."""
        M0 = matrix(self.K,[[self.reduce(c) for c in row] for row in M.rows()])
        inv = M0.inverse()
        v = vector(self.A,[0]*M.ncols())
        for exponent in range(DIGITS):
            residual = vector(self.A,b)-M*v
            delta = inv*vector(self.K,[self.divide_power(c,exponent) for c in residual])
            v += (P**exponent)*vector(self.A,[self.lift(c) for c in delta])
        assert M*v == vector(self.A,b)
        return list(v)

    def lift_on_curve(self,curve,pairs):
        residual = [evaluate(curve[i],self.x,pairs) for i in self.curve_indices]
        parameter = self.x[14]
        delta = -self.J0_inverse*vector(self.K,[self.divide_step(c) for c in residual])
        self.x[:14] = [x+STEP*self.lift(d) for x,d in zip(self.x[:14],delta)]
        assert all(evaluate(q,self.x,pairs) == 0 for q in curve)
        assert self.x[14] == parameter

    def lift_cutout(self,equations,pairs):
        J = matrix(self.K,[gradient(q,self.x0,pairs)[:15] for q in equations])
        inds = list(J.transpose().pivots())
        assert len(inds) == 15
        inv = J.matrix_from_rows(inds).inverse()
        rhs = vector(self.K,[-self.divide_step(evaluate(equations[i],self.x,pairs)) for i in inds])
        delta = inv*rhs
        self.x[:15] = [x+STEP*self.lift(d) for x,d in zip(self.x[:15],delta)]
        assert all(evaluate(q,self.x,pairs) == 0 for q in equations)

    def tangent(self,curve,pairs):
        rows = [gradient(curve[i],self.x,pairs) for i in self.curve_indices]
        M = matrix(self.A,[r[:14] for r in rows])
        vals = self.solve_A(M,[-r[14] for r in rows])
        v = vals+[self.A(1),self.A(0)]
        assert all(dot(gradient(q,self.x,pairs),v) == 0 for q in curve)
        return v

    def export(self,curve,pairs,second=False,tangent=None):
        v = self.tangent(curve,pairs) if tangent is None else tangent
        out = {"label": self.label, "degree": self.degree, "etale_modulus": self.modulus,
               "coordinates": [self.coefficients(x) for x in self.x],
               "tangent": [self.coefficients(x) for x in v]}
        if second:
            v0 = [self.reduce(x) for x in v]
            w = -self.J0_inverse*vector(self.K,[evaluate(curve[i],v0,pairs) for i in self.curve_indices])
            w = list(w)+[self.K(0),self.K(0)]
            assert all(dot(gradient(q,self.x0,pairs),w)+evaluate(q,v0,pairs) == 0 for q in curve)
            out["second_jet_mod31"] = [self.coefficients(self.lift(x)) for x in w]
        return out


def point_jets(coordinates,curve,pairs):
    """Exact implicit jets over the current residue ring, centered at P32."""
    pt = [BASE(x)/BASE(coordinates[0]) for x in coordinates]
    J = matrix(BASE,[gradient(q,pt,pairs)[1:15] for q in curve])
    inds = list(J.change_ring(K0).transpose().pivots())
    assert len(inds) == 14
    inv = J.matrix_from_rows(inds).inverse()
    S = PowerSeriesRing(BASE,"t",default_prec=16)
    t = S.gen()
    xs = [S(x).add_bigoh(16) for x in pt]
    xs[15] += t
    for n in range(1,16):
        rhs = vector(BASE,[-evaluate(curve[i],xs,pairs)[n] for i in inds])
        delta = inv*rhs
        for j,c in enumerate(delta,1):
            xs[j] += c*t**n
    assert all(evaluate(q,xs,pairs) == 0 for q in curve)
    return xs


def lift_section(row,components,point_series,order,standard,pairs,expected_rank):
    """Correct a quadric in the fixed 45-dimensional integral section chart."""
    values = []
    columns = [[] for _ in standard]
    for c in components:
        values += c.coefficients(evaluate(row,c.x,pairs))
        for col,j in zip(columns,standard):
            a,b = pairs[j]
            col += c.coefficients(c.x[a]*c.x[b])
    if point_series is not None:
        values += [int(evaluate(row,point_series,pairs)[n]) for n in range(order)]
        for col,j in zip(columns,standard):
            a,b = pairs[j]
            col += [int((point_series[a]*point_series[b])[n]) for n in range(order)]
    assert all(v%STEP == 0 for v in values)
    A = matrix(K0,columns).transpose()
    pivots = list(A.pivots())
    assert A.nrows() == expected_rank and A.rank() == expected_rank
    square = A.matrix_from_columns(pivots)
    sol = square.solve_right(vector(K0,[-v//STEP for v in values]))
    delta = [0]*len(standard)
    for j,c in zip(pivots,sol):
        delta[j] = int(c)
    assert A*vector(K0,delta) == vector(K0,[-v//STEP for v in values])
    out = list(row)
    for j,c in zip(standard,delta):
        out[j] = (out[j]+STEP*c)%MODULUS
    assert all(evaluate(out,c.x,pairs) == 0 for c in components)
    if point_series is not None:
        assert all(evaluate(out,point_series,pairs)[n] == 0 for n in range(order))
    info = {"rank": expected_rank, "unknowns": len(standard),
            "correction_pivot_columns": pivots,
            "nonzero_initial_defect_coefficients": sum(v != 0 for v in values),
            "changed_coefficients": sum(c != 0 for c in delta)}
    return out,info


def compute_step(supports,candidate,original,marks,previous=None,previous_path=None):
    started = time.monotonic()
    support_log = DATA/"cm_frame_lift_supports.out"
    if previous is not None:
        assert previous["precision_digits"] == DIGITS-1
        previous_components = {(c["label"],tuple(c["etale_modulus"])):c for c in previous["components"]}
    else:
        assert DIGITS == 2
        previous_components = {}
    curve = candidate["quadrics"]
    pairs = [tuple(p) for p in candidate["monomial_pairs"]]
    assert pairs == [(i-1,j-1) for i,j in original["monomial_pairs_one_based"]]
    curve_matrix = matrix(K0,curve)
    standard = [j for j in range(136) if j not in curve_matrix.pivots()]
    assert len(standard) == 45
    T = PolynomialRing(K0,"z")
    groups = {}
    for label in ("D17","E","F"):
        data = supports[label]
        h = T(data["modulus"])
        assert h.is_squarefree() and h.degree() == data["degree"]
        components = []
        for f,e in h.factor():
            assert e == 1
            key = label,tuple(int(c) for c in f.list())
            components.append(Component(label,f,data["coordinates"],curve,pairs,previous_components.get(key)))
        groups[label] = components
    print("LIFT_DIGITS",DIGITS,flush=True)

    for c in groups["D17"]:
        c.lift_cutout(curve+supports["D17_extra_rows"],pairs)
    jets = point_jets(marks["rational_point"]["primitive_coordinates"],curve,pairs)
    old = original if previous is None else previous
    qn,ni = lift_section(old["numerator_coefficients"],groups["D17"],jets,15,standard,pairs,32)
    assert int(evaluate(qn,jets,pairs)[15])%P != 0
    print("NUMERATOR_LIFT",ni,round(time.monotonic()-started,3),flush=True)
    for c in groups["F"]:
        c.lift_cutout(curve+[qn],pairs)
    for c in groups["E"]:
        c.lift_on_curve(curve,pairs)
    qd,di = lift_section(old["denominator_coefficients"],groups["F"]+groups["E"],None,0,standard,pairs,44)
    print("DENOMINATOR_LIFT",di,round(time.monotonic()-started,3),flush=True)

    # The value conditions at E do not see its displacement because qd has
    # a double zero modulo 31. The derivative determines that displacement.
    corrections = []
    for c in groups["E"]:
        v = c.tangent(curve,pairs)
        v0 = [c.reduce(x) for x in v]
        w = -c.J0_inverse*vector(c.K,[evaluate(curve[i],v0,pairs) for i in c.curve_indices])
        w = list(w)+[c.K(0),c.K(0)]
        coefficient2 = dot(gradient(qd,c.x0,pairs),w)+evaluate(qd,v0,pairs)
        assert coefficient2 != 0
        slope = dot(gradient(qd,c.x,pairs),v)
        shift = -c.divide_step(slope)/(2*coefficient2)
        c.x = [x+STEP*c.lift(shift*d) for x,d in zip(c.x,v0)]
        assert all(evaluate(q,c.x,pairs) == 0 for q in curve)
        assert evaluate(qd,c.x,pairs) == 0
        v = c.tangent(curve,pairs)
        assert dot(gradient(qd,c.x,pairs),v) == 0
        assert c.reduce(evaluate(qn,c.x,pairs)) != 0
        corrections.append(c.coefficients(c.lift(shift)))
    print("DOUBLE_ZEROS_LIFTED",16,round(time.monotonic()-started,3),flush=True)

    components = []
    for label,group in groups.items():
        for c in group:
            v = c.tangent(curve,pairs)
            if label == "D17":
                assert evaluate(qn,c.x,pairs) == 0
                assert c.reduce(dot(gradient(qn,c.x,pairs),v)) != 0
                assert c.reduce(evaluate(qd,c.x,pairs)) != 0
            if label == "F":
                assert evaluate(qn,c.x,pairs) == evaluate(qd,c.x,pairs) == 0
                assert c.reduce(dot(gradient(qn,c.x,pairs),v)) != 0
                assert c.reduce(dot(gradient(qd,c.x,pairs),v)) != 0
            components.append(c.export(curve,pairs,second=label=="E",tangent=v))
    assert int(evaluate(qd,jets,pairs)[0])%P != 0
    result = {
        "status": "pass", "milestone": "D72", "modulus": MODULUS, "precision_digits": DIGITS,
        "sources": [source(p) for p in (__file__,support_log,
                    ROOT/"dembele/magma/123_cm_frame_lift_supports.m",
                    DATA/"cm_frame_curve_candidate.json",DATA/"cm_frame_resolvent.json",
                    DATA/"cm_frame_marks.json")],
        "monomial_pairs_zero_based": pairs, "section_chart_indices_zero_based": standard,
        "numerator_coefficients": qn, "denominator_coefficients": qd,
        "numerator_linear_system": ni, "denominator_linear_system": di,
        "point_jets": [[int(x[n]) for x in jets] for n in range(16)],
        "components": components, "E_parameter_corrections": corrections,
        "divisor_identity_at_stated_modulus": "D17 + 15*P32 - 2*E",
        "half_line_bundle": "O(E - 7*P32)",
        "characteristic_zero_equation_obtained": False,
        "Shimura_identification_certified": False,
        "genus64_cover_constructed": False, "target_field_polynomial_obtained": False,
        "wall_seconds": time.monotonic()-started,
    }
    if previous_path is not None:
        result["sources"].append(source(previous_path))
        for name in ("numerator_coefficients","denominator_coefficients"):
            assert [c%STEP for c in result[name]] == previous[name]
        for c in result["components"]:
            oldc = previous_components[c["label"],tuple(c["etale_modulus"])]
            assert [[x%STEP for x in row] for row in c["coordinates"]] == oldc["coordinates"]
    return result


def main():
    global MODULUS,BASE,DIGITS,STEP
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--digits",type=int,default=2)
    parser.add_argument("--output",type=Path,default=DATA/"cm_frame_resolvent_lift.json")
    args = parser.parse_args()
    if not 2 <= args.digits <= 32:
        parser.error("choose between 2 and 32 digits for this successive-digit implementation")
    started = time.monotonic()
    supports = parse_supports((DATA/"cm_frame_lift_supports.out").read_text())
    candidate = json.loads((DATA/"cm_frame_curve_candidate.json").read_text())
    original = json.loads((DATA/"cm_frame_resolvent.json").read_text())
    marks = json.loads((DATA/"cm_frame_marks.json").read_text())
    previous = previous_path = None
    for digits in range(2,args.digits+1):
        DIGITS = digits; MODULUS = P**digits; STEP = P**(digits-1); BASE = Zmod(MODULUS)
        result = compute_step(supports,candidate,original,marks,previous,previous_path)
        result["cumulative_wall_seconds"] = time.monotonic()-started
        path = DATA/f"cm_frame_resolvent_lift_{digits}.json"
        path.write_text(json.dumps(result,indent=2)+"\n")
        previous,previous_path = result,path
        print("PASS|124_CM_FRAME_RESOLVENT_LIFT",digits,round(result["wall_seconds"],3),flush=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print("TOTAL_WALL_SECONDS",round(time.monotonic()-started,3),flush=True)


if __name__ == "__main__":
    main()
