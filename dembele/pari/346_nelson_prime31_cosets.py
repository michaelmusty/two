"""D93: certify right O^1 orbits using O/(31,b-27)O = M_2(F_31).

The right ideal alpha*O is the preimage of matrices with image in one
line. Equal lines therefore mean alpha_i^{-1}*alpha is a norm-one unit.
At most 32 orbits exist; an example for each line proves exactly 32.
"""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
from sage.all import GF,QQ,ZZ,matrix,vector

spec=importlib.util.spec_from_file_location("norm_one",Path(__file__).with_name("339_nelson_norm_one_search.py"))
norm_one=importlib.util.module_from_spec(spec);spec.loader.exec_module(norm_one)
DATA=norm_one.DATA


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--bound",type=int,default=6400);args=p.parse_args()
    path=DATA/f"nelson_prime31_b27_d93_T{args.bound}.json";packet=json.loads(path.read_text())
    out=DATA/f"nelson_prime31_cosets_d93_T{args.bound}.json";assert not out.exists()
    d=norm_one.setup();F,B,b=d["F"],d["B"],d["b"];basis=d["basis"];n=F([QQ(c) for c in packet["norm_generator"]["totally_positive_generator_coefficients"]])
    O=matrix(QQ,d["raw"]["quaternion_export"]["order_basis"]).transpose();Oinv=O.inverse()
    left=[]
    for q in basis:
        L=Oinv*matrix(QQ,[d["coords"](q*r) for r in basis]).transpose()
        assert L.denominator()==1;left.append(matrix(ZZ,L))
    def order_coords(q):
        v=Oinv*d["coords"](q);assert v.denominator()==1;return vector(ZZ,v)
    def left_matrix(v):return sum((v[i]*left[i] for i in range(32) if v[i]),matrix(ZZ,32,32))
    N=left_matrix(order_coords(B(n)));assert N.det()==31**4
    K=GF(31);br=K(27);a=br-br*br;identity=matrix.identity(K,2)
    ii=matrix(K,[[0,a],[1,0]])
    x,y=next((K(x),K(y)) for x in range(31) for y in range(31) if K(x*x)-a*K(y*y)==-1)
    jj=matrix(K,[[x,-a*y],[y,-x]])
    assert ii*ii==a*identity and jj*jj==-identity and ii*jj==-jj*ii
    units=[identity,ii,jj,ii*jj]
    assert matrix(K,[m.list() for m in units]).rank()==4
    def reduce_field(v):return sum((K(c)*br**j for j,c in enumerate(v.vector())),K(0))
    def rho(q):return sum((reduce_field(c)*m for c,m in zip(q.coefficient_tuple(),units)),matrix(K,2,2))
    images=[rho(q) for q in basis];reduction=matrix(K,[m.list() for m in images]).transpose()
    assert reduction.rank()==4 and reduction*matrix(K,N)==0
    # These checks also verify closure of the saved order and the ring map.
    for i,q in enumerate(basis):
        actual=reduction*matrix(K,left[i])
        assert actual==matrix(K,[(images[i]*m).list() for m in images]).transpose()
    def line(m):
        assert m.rank()==1
        v=next(v for v in m.columns() if any(v))
        return int(v[1]/v[0]) if v[0] else 31
    grouped={};witnesses=[];counts=Counter()
    ordered=sorted(packet["classes"],key=lambda r:QQ(r["A_interval"][0]))
    for row in ordered:
        q=d["quat"](row["quaternion_power_coordinates"]);assert q.reduced_norm()==n
        label=line(rho(q));counts[label]+=1
        if label not in grouped:
            v=order_coords(q);bar=order_coords(q.conjugate());L=left_matrix(v);Lbar=left_matrix(bar)
            assert abs(L.det())==31**2 and L*Lbar==N and Lbar*L==N
            ell=vector(K,[1,label]) if label<31 else vector(K,[0,1])
            ideal_image=matrix(K,[[ell[0],0,ell[1],0],[0,ell[0],0,ell[1]]]).row_space()
            assert (reduction*matrix(K,L)).column_space()==ideal_image
            grouped[label]={"line_label":label,"line_vector":list(map(int,ell)),"representative_class_index":row["index"],
                            "representative_A_interval":row["A_interval"],"order_coordinates":list(map(int,v)),
                            "conjugate_order_coordinates":list(map(int,bar)),"left_matrix":[list(map(int,r)) for r in L.rows()],
                            "conjugate_left_matrix":[list(map(int,r)) for r in Lbar.rows()],"ideal_index":31**2,
                            "q":q}
        representative=grouped[label]["q"];gamma=representative**(-1)*q
        assert gamma.reduced_norm()==F(1)
        v=order_coords(gamma);assert representative*sum((v[i]*basis[i] for i in range(32) if v[i]),B(0))==q
        witnesses.append({"class_index":row["index"],"line_label":label,"right_norm_one_order_coordinates":list(map(int,v))})
    assert 0<len(grouped)<=32
    representatives=[]
    for label in sorted(grouped):
        row=grouped[label].copy();del row["q"];representatives.append(row)
    result={"status":"pass: exact local ideal classification and right norm-one orbit witnesses",
            "invariant_A_cutoff":args.bound,"prime_norm":31,"prime_b_residue":27,
            "finite_embedding":{"i":list(map(int,ii.list())),"j":list(map(int,jj.list())),
                                "reduction_matrix":[list(map(int,r)) for r in reduction.rows()],
                                "rank":4,"ring_multiplication_pairs_checked":1024},
            "norm_scalar_matrix":[list(map(int,r)) for r in N.rows()],
            "norm_scalar_index":31**4,"norm_ideal_index":31**2,
            "realized_lines":sorted(grouped),"realized_orbits":len(grouped),
            "universal_orbit_count_upper_bound":32,"all_32_orbits_exhibited":len(grouped)==32,
            "coset_counts":dict(counts),"coset_representatives":representatives,"class_witnesses":witnesses,
            "separation_argument":"each alpha_i*(O^1/{+1,-1}) orbit is an isometric image of the D92 norm-one orbit",
            "sources":[norm_one.source(p) for p in [Path(__file__),Path(norm_one.__file__),path]+d["paths"]]}
    out.write_text(json.dumps(result,indent=2)+"\n")
    print("REALIZED_ORBITS",len(grouped),"of 32; counts",dict(sorted(counts.items())),flush=True)
    print("PASS|346_nelson_prime31_cosets")


if __name__=="__main__":main()
