"""D109: exact order, Hensel splitting, and one arithmetic edge transport.

The Magma matrices are only proposals. All certificate inequalities below
use exact rational number-field arithmetic; no p-adic equality is trusted.
"""
from pathlib import Path
import hashlib
import json
from sage.all import QQ, ZZ, GF, NumberField, PolynomialRing, matrix, vector, identity_matrix

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "dembele/data/computed"


def source(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    target = DATA / "definite_dyadic_certificate_d109.json"
    assert not target.exists(), "Preserve completed artifacts."
    raw_path = DATA / "definite_dyadic_export_d109.json"
    raw = json.loads(raw_path.read_text())
    R = PolynomialRing(QQ, "z"); z = R.gen()
    poly = R(raw["field_polynomial_ascending"])
    F = NumberField(poly, "b"); b = F.gen()
    def f(row):
        return sum(F(QQ(c))*b**i for i,c in enumerate(row))
    def fs(x):
        return [str(c) for c in F(x).list()]
    def ms(M):
        return [fs(c) for c in M.list()]
    def qs(q):
        return [fs(c) for c in q]
    def val(x):
        x = F(x)
        return min((8*c.valuation(2)+i for i,c in enumerate(x.list()) if c), default=10**9)
    def mv(M):
        return min(val(x) for x in M.list())
    assert val(b)==1 and val(2)==8 and poly.discriminant()==2**31
    assert raw["quaternion_parameters"] and [f(x) for x in raw["quaternion_parameters"]]==[-1,-1]
    one = vector(F,[1,0,0,0])
    def qm(q,r):
        a,c,d,e = q; A,C,D,E = r
        return vector(F,[a*A-c*C-d*D-e*E, a*C+c*A+d*E-e*D,
                         a*D+d*A+e*C-c*E, a*E+e*A+c*D-d*C])
    def norm(q):
        return sum(x*x for x in q)
    def flat(q):
        return vector(QQ,sum([list(F(c)) for c in q],[]))
    basis = [vector(F,[f(c) for c in q]) for q in raw["order_Z_basis"]]
    Z = matrix(QQ,[flat(q) for q in basis]).transpose(); Zi = Z.inverse()
    def integral(q):
        return all(c.denominator()==1 for c in Zi*flat(q))
    assert len(basis)==32 and integral(one)
    assert all(integral(b*q) for q in basis)
    assert all(integral(qm(q,r)) for q in basis for r in basis)
    gram = matrix(QQ,[[F(2*qm(q,r)[0]).trace() for r in basis] for q in basis])
    disc = gram.det()
    assert abs(disc)==2**124
    OF = matrix(QQ,[[QQ(c) for c in row] for row in raw["OF_Z_basis"]])
    assert abs(OF.det())==1
    print("ORDER|32-dimensional Z-lattice closed; trace discriminant 2^124",flush=True)

    E = identity_matrix(F,2)
    approx = [matrix(F,2,2,[f(c) for c in row]) for row in raw["approximate_basis_matrices"]]
    assert approx[0]==E
    A, B = approx[1:3]
    # Choose a cyclic vector whose rational conjugating matrix loses least valuation.
    candidates = []
    for v in [vector(F,[1,0]),vector(F,[0,1]),vector(F,[1,1])]:
        C = matrix(F,[v,A*v]).transpose()
        if C.det(): candidates.append((val(C.det()),C))
    _, C = min(candidates,key=lambda p:p[0]); Ci = C.inverse()
    I0 = matrix(F,[[0,-1],[1,0]])
    Jprop = Ci*B*C; x0,y = Jprop[0,0],Jprop[1,0]
    residual = x0*x0+y*y+1
    n,s = val(residual),val(2*x0)
    assert residual and n>2*s
    d = n-s
    # Hensel produces the unique t with t^2+y^2+1=0 and v(t-x0)>s;
    # its exact distance from x0 is d. J(t)=Jc+t*Jt.
    I = C*I0*Ci
    Jc = C*matrix(F,[[0,y],[y,0]])*Ci
    Jt = C*matrix(F,[[1,0],[0,-1]])*Ci
    assert I*I==-E
    assert I*Jc+Jc*I==0 and I*Jt+Jt*I==0
    assert Jt*Jt==E and Jc*Jt+Jt*Jc==0 and Jc*Jc==y*y*E
    def image(q):
        const = q[0]*E+q[1]*I+q[2]*Jc+q[3]*I*Jc
        slope = q[2]*Jt+q[3]*I*Jt
        return const+x0*slope, slope
    reductions = []
    image_centers = []
    image_error_bounds = []
    for q in basis:
        center,slope = image(q)
        assert mv(center)>=0
        bound = d+mv(slope)
        assert bound>=1
        reductions.append([int(val(c)==0) for c in center.list()])
        image_centers.append(ms(center)); image_error_bounds.append(int(bound))
    reduced = matrix(GF(2),reductions)
    assert reduced.rank()==4
    pivots = list(reduced.transpose().pivots())
    assert len(pivots)==4
    print(f"SPLITTING|Hensel n={n}, s={s}; root error={d}; order error>={min(image_error_bounds)}",flush=True)

    # First try the small exact Hamilton units, then the exported projective generators.
    unit_candidates = [vector(F,[0,1,0,0]),vector(F,[0,0,1,0]),vector(F,[0,0,0,1])]
    unit_candidates += [vector(F,[F(1)/2,F(i)/2,F(j)/2,F(k)/2])
                        for i in [-1,1] for j in [-1,1] for k in [-1,1]]
    unit_candidates += [vector(F,[f(c) for c in row]) for row in raw["projective_unit_generators"]]
    witness = None
    for q in unit_candidates:
        if norm(q)!=1 or not integral(q): continue
        center,slope = image(q)
        if mv(center)<0 or d+mv(slope)<1: continue
        red = matrix(GF(2),2,2,[int(val(c)==0) for c in center.list()])
        if red!=identity_matrix(GF(2),2):
            witness=(q,center,slope,red); break
    assert witness is not None, "No norm-one nontrivial neighbor transport among these bounded candidates."
    q,Qc,Qt,red = witness
    assert integral(vector(F,[q[0],-q[1],-q[2],-q[3]])) and red.det()==1
    lines = [vector(GF(2),[1,0]),vector(GF(2),[0,1]),vector(GF(2),[1,1])]
    perm = [lines.index(red*l) for l in lines]
    a = next(i for i in range(3) if perm[i]!=i); target_line = perm[a]
    # L_l is the inverse image of l in O_K^2; these are the three neighbors.
    lattices = [matrix(F,[[1,0],[0,b]]),matrix(F,[[b,0],[0,1]]),matrix(F,[[1,0],[1,b]])]
    left,right = lattices[target_line].inverse(),lattices[a]
    transport_center = left*Qc*right
    transport_slope = left*Qt*right
    transport_error = d+mv(transport_slope)
    assert mv(transport_center)>=0 and transport_error>=1
    # Exact determinant is Norm(q)*det(L_source)/det(L_target)=1.
    assert norm(q)*lattices[a].det()/lattices[target_line].det()==1
    print(f"TRANSPORT|norm-one unit sends neighbor {a} to {target_line}; permutation {perm}",flush=True)
    result = {
        "status":"pass", "milestone":"D109",
        "field_polynomial_ascending":raw["field_polynomial_ascending"],
        "quaternion_parameters":[-1,-1], "order_Z_rank":32,
        "order_contains_one_and_is_closed":True, "order_stable_under_b":True,
        "absolute_reduced_trace_discriminant":str(disc),
        "Hensel": {"x0":fs(x0),"y":fs(y),"residual":fs(residual),
                    "residual_valuation":int(n),"derivative_valuation":int(s),
                    "root_error_valuation":int(d),
                    "root_definition":"t^2+y^2+1=0, v(t-x0)>s"},
        "conjugating_matrix":ms(C),"I_exact":ms(I),"J_constant":ms(Jc),"J_slope":ms(Jt),
        "order_image_centers":image_centers,"order_image_error_lower_bounds":image_error_bounds,
        "order_image_reductions":reductions,"residue_rank":4,
        "residue_basis_Z_indices":list(map(int,pivots)),
        "integral_local_order_isomorphism_certified":True,
        "transport": {"quaternion":qs(q),"reduced_norm":"1",
                      "unit_order_coordinates":[str(c) for c in Zi*flat(q)],
                      "matrix_center":ms(Qc),"matrix_slope":ms(Qt),
                      "mod_pi_matrix":[int(c) for c in red.list()],
                      "neighbor_permutation":perm,"source_neighbor":int(a),"target_neighbor":int(target_line),
                      "source_lattice":ms(lattices[a]),"target_lattice":ms(lattices[target_line]),
                      "conjugated_center":ms(transport_center),"conjugated_slope":ms(transport_slope),
                      "conjugated_error_lower_bound":int(transport_error),
                      "exact_conjugated_determinant":"1", "fixes_base_vertex":True},
        "new_ideal_class_or_tree_enumeration":False,
        "actual_harmonic_cocycle_or_moments_computed":False,
        "dyadic_CM_frame_matching_proved":False,
        "sources":[source(Path(__file__)),source(raw_path)]}
    target.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|398_definite_dyadic_certificate",flush=True)


if __name__=="__main__": main()
