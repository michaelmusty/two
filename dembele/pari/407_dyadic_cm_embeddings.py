"""D112: exact dyadic CM coordinates and the seventeen localized ideal classes.

Uses only the existing eight ordinary reversed edges and D110's W anchor.
The geometric interpretation and reciprocity convention are audited separately.
Run with Sage through runner 272, with a 180-second cap.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
from sage.all import QQ, ZZ, NumberField, PolynomialRing, QuaternionAlgebra, matrix, vector, identity_matrix

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"

def source(p):
    p=Path(p).resolve();return {"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}

def main():
    out=DATA/"dyadic_cm_embeddings_d112.json";assert not out.exists()
    names=["dyadic_quotient_export_d111.json","dyadic_harmonic_certificate_d111.json",
           "dyadic_group_transport_d110.json","definite_dyadic_certificate_d109.json","cm_orbit.json"]
    raw,graph,group,split,saved=[json.loads((DATA/n).read_text()) for n in names]
    P=PolynomialRing(QQ,"x");x=P.gen();F=NumberField(x**8-8*x**6+20*x**4-16*x*x+2,"b");b=F.gen()
    B=QuaternionAlgebra(F,-1,-1);ii,jj,kk=B.gens();lam=2+b
    def f(row):return F([QQ(c) for c in row])
    def q(row):return B([f(c) for c in row])
    def fs(c):return list(map(str,F(c).list()))
    def qs(v):return [fs(c) for c in v.coefficient_tuple()]
    def coords(v):return vector(QQ,sum([list(c) for c in v.coefficient_tuple()],[]))
    def val(c):return min((8*a.valuation(2)+i for i,a in enumerate(F(c).list()) if a),default=10**9)
    def mv(m):return min(map(val,m.list()))
    def dyadic(cs):return all(c.denominator().is_power_of(2) for c in cs)
    def power2(c):return abs(QQ(c).numerator()).is_power_of(2) and QQ(c).denominator().is_power_of(2)
    OB=[q(v) for v in raw["order_Z_basis"]];OZ=matrix(QQ,[coords(v) for v in OB]).transpose();OZi=OZ.inverse()
    W=q(group["transports"]["W"]["quaternion"])
    assert W*W==B(-lam) and kk*W==-W*kk and kk.reduced_norm()==1
    assert all(c in ZZ for c in OZi*coords(kk)) and all(c in ZZ for c in OZi*coords(~kk))
    M=NumberField(P(saved["CM_orbit"]["CM_polynomial_ascending"]),"beta");beta=M.gen()
    assert beta**16+16*beta**14+104*beta**12+352*beta**10+660*beta**8+672*beta**6+336*beta**4+64*beta**2+2==0
    classes=M.class_group(proof=True);assert classes.order()==17
    oldgen=M.fractional_ideal([M([QQ(c) for c in row]) for row in saved["CM_orbit"]["class_generator_ideal_basis"]])
    exponent=int(classes(oldgen).list()[0]);assert exponent%17
    def label(a):return int(classes(a).list()[0])*pow(exponent,-1,17)%17
    ib=M.integral_basis();ibm=matrix(QQ,[z.vector() for z in ib]).transpose()
    def embed(z,v=W):return sum((B(c)*v**j for j,c in enumerate(z.list())),B(0))
    assert embed(-beta*beta-2)==B(b)
    assert all(dyadic(OZi*coords(embed(z))) for z in ib)
    pM=M.ideal(beta);assert pM.norm()==2 and M.ideal(2)==pM**16
    roots_unity=int(M.number_of_roots_of_unity());assert roots_unity==2
    assert label(M.ideal(31,beta-19))==3
    spec=importlib.util.spec_from_file_location("d59",ROOT/"dembele/pari/96_cm_orbit.py")
    d59=importlib.util.module_from_spec(spec);spec.loader.exec_module(d59)
    proposals=[{"name":"W","quaternion":W,"reversed_edge":None,"normalizing_scalar":F(1),"sign":1}]
    for orbit in graph["inverted_edge_orbits"]:
        assert len(orbit)==1;e=orbit[0];j=raw["edges"][e]["source_class"]
        assert raw["edges"][e]["target_class"]==j
        if raw["stabilizers"][j]!=1:continue
        t=q(raw["edges"][e]["quaternion"]);assert t.reduced_trace()==0
        scale=(t.reduced_norm()/lam).sqrt();v=t/scale;assert v*v==B(-lam)
        for sign in [1,-1]:proposals.append({"name":f"edge_{e}_{'plus' if sign==1 else 'minus'}",
            "quaternion":sign*v,"reversed_edge":e,"normalizing_scalar":scale,"sign":sign})
    assert len(proposals)==17
    T=PolynomialRing(F,"T");Et=NumberField(T.gen()**2+f(split["Hensel"]["y"])**2+1,"t");t=Et.gen()
    def mat(key):return matrix(Et,2,2,[Et(f(c)) for c in split[key]])
    I,Jc,Jt=map(mat,["I_exact","J_constant","J_slope"]);Id=identity_matrix(Et,2)
    J=Jc+t*Jt;assert I*I==J*J==-Id and I*J==-J*I
    x0=f(split["Hensel"]["x0"]);error=split["Hensel"]["root_error_valuation"]
    def es(z):return [fs(c) for c in list(Et(z))]
    def em(m):return [es(c) for c in m.list()]
    def center(m):return matrix(F,2,2,[sum((F(c)*x0**k for k,c in enumerate(list(z))),F(0)) for z in m.list()])
    def slope(m):return matrix(F,2,2,[F(list(z)[1]) for z in m.list()])
    entries=[]
    for idx,proposal in enumerate(proposals):
        v=proposal["quaternion"];assert all(dyadic(OZi*coords(embed(z,v))) for z in ib)
        u=B(1) if idx==0 else v+W;assert u!=B(0) and v*u==u*W
        image=matrix(QQ,[coords(u*embed(z)) for z in ib]).transpose()
        columns=d59.preimage_lattice(OZi,image)
        generators=[sum((columns[j,k]*ib[j] for j in range(16)),M(0)) for k in range(16)]
        ideal=M.fractional_ideal(generators)
        original=ibm*columns;actual=matrix(QQ,[z.vector() for z in ideal.basis()]).transpose()
        change=original.inverse()*actual
        assert dyadic(change.list()) and dyadic(change.inverse().list()) and power2(change.det())
        assert all(dyadic(OZi*coords(u*embed(z))) for z in ideal.basis())
        np=ideal.norm()*u.reduced_norm().norm();assert power2(np)
        cl=label(ideal)
        A=v[0]*Id+v[1]*I+v[2]*J+v[3]*I*J;assert A*A==-lam*Id and A.trace()==0
        S=matrix(Et,[[1,A[0,0]],[0,A[1,0]]]);standard=matrix(Et,[[0,-lam],[1,0]])
        assert S.det()!=0 and A*S==S*standard
        Sc,Ss=center(S),slope(S);se=error+mv(Sc.inverse()*Ss);assert se>=1
        assert error+val(F(list(S.det())[1]))>val(Sc.det())
        if idx==0:
            K=I*J;ref=S.inverse()*K*S;assert ref*standard==-standard*ref
            anchor={"quaternion":qs(kk),"order_coordinates":list(map(str,OZi*coords(kk))),
                    "CM_chart_action":em(ref),"norm":"1","exchanges_fixed_points":True}
        entries.append({"index":idx,"name":proposal["name"],"reversed_edge":proposal["reversed_edge"],
          "sign":proposal["sign"],"normalizing_scalar":fs(proposal["normalizing_scalar"]),
          "embedded_beta":qs(v),"intertwiner":qs(u),"relative_ideal_class":cl,
          "ideal_basis_power_coordinates":[list(map(str,z.list())) for z in ideal.basis()],
          "ideal_norm":str(ideal.norm()),"norm_product":str(np),
          "localized_intersection_change_determinant":str(change.det()),
          "splitting_matrix":em(A),"CM_coordinate_matrix":em(S),
          "CM_coordinate_center":[fs(c) for c in Sc.list()],"CM_coordinate_slope":[fs(c) for c in Ss.list()],
          "CM_coordinate_lattice_error_lower_bound":int(se),"CM_coordinate_determinant_valuation":int(val(Sc.det())),
          "point_formula":"S*(beta:1); affine z=(beta+A00)/A10; eigenvalue beta"})
        print(f"CM|{idx}: {proposal['name']}; relative class {cl}; norm product {np}; coordinate error {se}",flush=True)
    labels=[row["relative_ideal_class"] for row in entries];assert sorted(labels)==list(range(17))
    assert all((entries[i]["relative_ideal_class"]+entries[i+1]["relative_ideal_class"])%17==0 for i in range(1,17,2))
    result={"status":"pass","milestone":"D112","entries":entries,"relative_class_labels":labels,
      "anchor_exchange":anchor,"CM_integral_basis":[list(map(str,z.list())) for z in ib],
      "CM_roots_of_unity":roots_unity,"dyadic_CM_prime_principal_generator":"beta","dyadic_CM_prime_norm":2,
      "class_number_proved":17,"prime31_beta19_class_in_saved_generator":3,
      "full_integer_ring_embeds_in_localized_order":True,
      "coordinate_convention":"A*S=S*[[0,-(2+b)],[1,0]]; exact t is the D109 Hensel root",
      "global_CM_point_label_matching_claimed_by_this_arithmetic_packet":False,
      "actual_moments_or_Shimura_jet_computed":False,
      "sources":[source(p) for p in [Path(__file__),Path(d59.__file__)]+[DATA/n for n in names]]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS|407_dyadic_cm_embeddings",flush=True)

if __name__=="__main__":main()
