"""D110 exact ideal, normalizer-coset and moving-vertex certificates.

Reuses D109's fixed Hensel splitting. It does not compute a fundamental
domain, harmonic cocycle, moments or a matched CM frame.
"""
from collections import deque
import hashlib
import json
from pathlib import Path
from sage.all import QQ, ZZ, NumberField, PolynomialRing, matrix, vector, identity_matrix

ROOT=Path(__file__).resolve().parents[2]; DATA=ROOT/"dembele/data/computed"


def source(path):
    path=Path(path).resolve()
    return {"path":str(path),"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    out=DATA/"dyadic_group_transport_d110.json"
    assert not out.exists(),"Preserve completed artifacts."
    raw_path=DATA/"dyadic_brandt_transport_export_d110.json"
    raw=json.loads(raw_path.read_text())
    old_path=DATA/"hyperellipticity_fresh_brandt_d99.json"
    old=json.loads(old_path.read_text())
    order_path=DATA/"definite_dyadic_export_d109.json"
    order=json.loads(order_path.read_text())
    split_path=DATA/"definite_dyadic_certificate_d109.json"
    split=json.loads(split_path.read_text())
    assert raw["matrix"]==old["matrix"] and raw["stabilizers"]==old["stabilizers"]
    assert raw["order_Z_basis"]==order["order_Z_basis"]
    P=PolynomialRing(QQ,"x");x=P.gen();F=NumberField(x**8-8*x**6+20*x**4-16*x*x+2,"b");b=F.gen()
    def f(row):return sum(F(QQ(c))*b**i for i,c in enumerate(row))
    def q(row):return vector(F,[f(c) for c in row])
    def m(row):return matrix(F,2,2,[f(c) for c in row])
    def fs(c):return list(map(str,F(c).list()))
    def qs(q):return [fs(c) for c in q]
    def ms(m):return [fs(c) for c in m.list()]
    def val(c):return min((8*a.valuation(2)+i for i,a in enumerate(F(c).list()) if a),default=10**9)
    def mv(m):return min(map(val,m.list()))
    def qm(q,r):
        a,c,d,e=q;A,C,D,E=r
        return vector(F,[a*A-c*C-d*D-e*E,a*C+c*A+d*E-e*D,
                         a*D+d*A+e*C-c*E,a*E+e*A+c*D-d*C])
    def norm(q):return sum(c*c for c in q)
    def qi(q):return vector(F,[q[0],-q[1],-q[2],-q[3]])/norm(q)
    def flat(q):return vector(QQ,sum([list(F(c)) for c in q],[]))
    def zb(rows):return [q(row) for row in rows]
    def zm(basis):return matrix(QQ,[flat(q) for q in basis]).transpose()
    OB=zb(raw["order_Z_basis"]);OZ=zm(OB);OZi=OZ.inverse()
    ideals={}; ideal_results=[]
    for entry in raw["selected_ideals"]:
        j=entry["class_index"];basis=zb(entry["Z_basis"]);Z=zm(basis);Zi=Z.inverse()
        assert all(c.denominator()==1 for c in (OZi*Z).list())
        assert abs((OZi*Z).det())==entry["absolute_norm"]**2
        assert all(c.denominator()==1 for z in basis for c in Zi*flat(b*z))
        assert all(c.denominator()==1 for z in basis for r in OB for c in Zi*flat(qm(z,r)))
        ideals[j]=(basis,Z,Zi)
        ideal_results.append({"class_index":j,"absolute_norm":entry["absolute_norm"],
                              "Z_index_in_order":str(abs((OZi*Z).det())),"right_order_closure_checked":True})
    assert ideals[0][1]==OZ
    edges=[];w=vector(F,[1,0,0,0])
    for k,entry in enumerate(raw["edges"]):
        a,c=entry["source_class"],entry["target_class"]
        assert [a,c]==raw["walk"][k:k+2] and old["matrix"][c][a]==entry["brandt_multiplicity"]
        t=q(entry["quaternion"]);basis,Z,Zi=ideals[a];_,W,Wi=ideals[c]
        image=zm([qm(t,z) for z in basis]); transition=Wi*image
        assert all(v.denominator()==1 for v in transition.list()) and abs(transition.det())==4
        lower=image.inverse()*zm([b*z for z in ideals[c][0]])
        assert all(v.denominator()==1 for v in lower.list()) and abs(lower.det())==4
        edges.append({"source_class":a,"target_class":c,"image_Z_index":4,"lower_Z_index":4,
                      "upper_inclusion_coordinates":[[str(v) for v in row] for row in transition.rows()],
                      "lower_inclusion_coordinates":[[str(v) for v in row] for row in lower.rows()]})
        w=qm(t,w)
    assert w==q(raw["odd_element"])
    n=norm(w);assert n==f(raw["odd_element_norm"]) and val(n)==7 and n.norm()==128
    assert all(c.denominator()==1 for c in n.list()) and w[0]==0
    assert qm(w,w)==vector(F,[-n,0,0,0])
    # A totally positive generator of p; D99 proves positive units are squares.
    lam=2+b
    assert lam.norm()==2 and val(lam)==1
    a=(n/lam).sqrt();assert a in F and a*a==n/lam
    W=w/a;assert norm(W)==lam and qm(W,W)==vector(F,[-lam,0,0,0])
    u=q(split["transport"]["quaternion"])
    g=qm(qm(W,u),qi(W))
    assert g==q(raw["norm_one_moving_element"]) and norm(g)==1
    membership={}
    for name,v in [("w",w),("w_inverse",qi(w)),("W",W),("W_inverse",qi(W)),("g",g),("g_inverse",qi(g))]:
        cs=OZi*flat(v)
        assert all(c.denominator().is_power_of(2) for c in cs)
        membership[name]={"order_coordinates":[str(c) for c in cs],
                          "maximum_denominator_2_exponent":max(int(c.denominator().valuation(2)) for c in cs)}
    print("ARITHMETIC|D99 matrix, stabilizers and D109 order identical; seven ideal inclusions verified",flush=True)

    # Construct exact local images as center+(t-x0)*slope in the fixed D109 embedding.
    E=identity_matrix(F,2);I=m(split["I_exact"]);Jc=m(split["J_constant"]);Jt=m(split["J_slope"])
    x0=f(split["Hensel"]["x0"]);root_error=split["Hensel"]["root_error_valuation"]
    def image(q):
        slope=q[2]*Jt+q[3]*I*Jt
        return q[0]*E+q[1]*I+q[2]*Jc+q[3]*I*Jc+x0*slope,slope
    transports={}
    for name,v in [("w",w),("W",W),("g",g)]:
        center,slope=image(v);error=root_error+mv(slope)
        minimum=mv(center);assert error>minimum
        nv=val(norm(v));distance=nv-2*minimum;assert distance>0
        H=center/b**minimum;Hs=slope/b**minimum
        swap=all(val(H[0,j])>0 for j in range(2))
        row=1 if swap else 0;other=1-row
        col=next(j for j in range(2) if val(H[row,j])==0)
        ratio=H[other,col]/H[row,col];digits=[];r=F(0)
        for j in range(distance):
            remaining=(ratio-r)/b**j;assert val(remaining)>=0
            digit=int(val(remaining)==0);digits.append(digit);r+=digit*b**j
        assert val(ratio-r)>=distance
        L=matrix(F,[[r,b**distance],[1,0]]) if swap else matrix(F,[[1,0],[r,b**distance]])
        transition=L.inverse()*H;transition_slope=L.inverse()*Hs
        transition_error=root_error+mv(transition_slope)
        determinant=norm(v)/b**(2*minimum)/L.det()
        assert mv(transition)>=0 and transition_error>=1 and val(determinant)==0
        assert val(center.det())==nv
        transports[name]={"quaternion":qs(v),"reduced_norm":fs(norm(v)),
                          "norm_valuation":int(nv),"matrix_center":ms(center),"matrix_slope":ms(slope),
                          "matrix_error_lower_bound":int(error),"minimum_entry_valuation":int(minimum),
                          "base_vertex_displacement":int(distance),"homothety_power":int(-minimum),
                          "target_lattice":ms(L),"target_digits":digits,"target_rows_swapped":swap,
                          "transition_center":ms(transition),"transition_slope":ms(transition_slope),
                          "transition_error_lower_bound":int(transition_error),"exact_transition_determinant":fs(determinant)}
        print(f"TRANSPORT|{name}: norm valuation {nv}; minimum entry {minimum}; displacement {distance}; transition error {transition_error}",flush=True)
    assert transports["W"]["base_vertex_displacement"]==transports["w"]["base_vertex_displacement"]
    assert transports["g"]["base_vertex_displacement"]==2*transports["W"]["base_vertex_displacement"]
    # The saved graph independently gives the minimum length of an odd closed walk at O.
    queue=deque([(0,0)]);dist={(0,0):0}
    while (0,1) not in dist:
        v,parity=queue.popleft()
        for z in range(58):
            state=(z,1-parity)
            if old["matrix"][z][v] and state not in dist:
                dist[state]=dist[v,parity]+1;queue.append(state)
    assert dist[0,1]==len(raw["walk"])-1==transports["w"]["base_vertex_displacement"]
    result={"status":"pass","milestone":"D110","matrix_and_stabilizers_identical_to_D99":True,
            "order_basis_identical_to_D109":True,"selected_ideal_checks":ideal_results,
            "walk":raw["walk"],"shortest_odd_closed_walk_length":dist[0,1],"edge_inclusion_checks":edges,
            "odd_norm":fs(n),"positive_uniformizer":fs(lam),"normalizing_scalar":fs(a),
            "normalizing_scalar_valuation":int(val(a)),"normalized_odd_square":fs(-lam),
            "localized_order_membership":membership,"transports":transports,
            "group_contract":{"localized_order":"R=O[1/b]","projective_full_group":"G=R^*/O_F[1/b]^*",
                              "norm_parity_kernel":"Gamma=image(R^1)","quotient":"G/Gamma=C2",
                              "odd_coset_representative":"W", "projective_W_order":2,
                              "normalizer_of_R_mod_Fstar_equals_G_using_class_number_one":True,
                              "geometric_uniformization_only":"Over completed maximal unramified extension; no CM labels or descent matrix inferred."},
            "full_fundamental_domain_constructed":False,"actual_harmonic_cocycle_or_moments_computed":False,
            "actual_dyadic_CM_frame_matching_proved":False,"actual_Shimura_tangent_or_jet_evaluated":False,
            "sources":[source(p) for p in [Path(__file__),raw_path,old_path,order_path,split_path,DATA/"hyperellipticity_order_review_d99.json"]]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|401_dyadic_group_transport",flush=True)


if __name__=="__main__":main()
