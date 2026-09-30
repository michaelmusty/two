"""D91: a proved, deliberately conservative complete invariant cutoff.

Seven independent explicit units suffice for coverage; no claim that
they generate the full unit group is needed. Volume is a cost diagnostic,
not a certified lattice-point count or a measured running time.
"""
import hashlib
import itertools
import json
from pathlib import Path
from sage.all import AA, QQ, ZZ, NumberField, PolynomialRing, RealBallField, matrix, factorial

ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/"dembele/data/computed"


def main():
    R=PolynomialRing(QQ,"x");x=R.gen();F=NumberField(x**8-8*x**6+20*x**4-16*x*x+2,"b");b=F.gen()
    RB=RealBallField(256);places=sorted(F.embeddings(AA),key=lambda p:p(b))
    cosines=[F(2),b]
    for _ in range(2,8):cosines.append(b*cosines[-1]-cosines[-2])
    units=[1+sum(cosines[1:j+1]) for j in range(1,8)]
    assert all(u.is_integral() and (1/u).is_integral() and abs(u.norm())==1 for u in units)
    log=matrix(RB,[[abs(RB(v(u))).log() for v in places] for u in units])
    assert not log.matrix_from_columns(range(7)).det().contains_zero()
    rounded=matrix(ZZ,[[ZZ((c.mid()*10**8).round()) for c in row] for row in log.rows()])
    reduced,change=rounded.LLL(transformation=True)
    assert abs(change.det())==1 and change*rounded==reduced
    alternatives=[]
    for name,T in [("cyclotomic",matrix.identity(ZZ,7)),("LLL",change)]:
        us=[F.prod(units[j]**row[j] for j in range(7)) for row in T.rows()]
        abs_values=[[abs(RB(v(u))) for v in places] for u in us]
        vertices=[]
        for signs in itertools.product([-1,1],repeat=7):
            value=sum(RB.prod(abs_values[j][i]**signs[j] for j in range(7)) for i in range(8))
            vertices.append((value,signs))
        C=ZZ(max(v.upper() for v,_ in vertices).ceil())
        alternatives.append({"name":name,"unit_exponent_change":[list(map(int,row)) for row in T.rows()],
                             "units_power_coordinates":[list(map(str,u.vector())) for u in us],
                             "cover_constant_integer":int(C),
                             "maximum_vertex_interval":str(max(vertices,key=lambda v:v[0].mid())[0])})
    selected=min(alternatives,key=lambda a:a["cover_constant_integer"]);C=selected["cover_constant_integer"]
    local=DATA/"nelson_cm_lattice_d90.json";saved=json.loads(local.read_text())
    det=matrix(QQ,saved["arithmetic"]["majorant_gram"]).det();assert det>0
    volume_factor=RB.pi()**16/factorial(16)/RB(det).sqrt()
    estimates=[]
    for A in [1,64,359,1000,10**6]:
        radius=RB(QQ(101)/100*C)*(RB(QQ(2*A)/2**31)**(QQ(1)/8))
        # An integer upward rounding makes the actual enumeration bound
        # usable with the saved exact rational Q.
        integer_radius=ZZ(radius.upper().ceil())
        estimates.append({"invariant_A_bound":A,"sufficient_Q_bound":int(integer_radius),
                          "unrounded_Q_bound_interval":str(radius),
                          "ellipsoid_volume_at_integer_bound":str(volume_factor*integer_radius**16),
                          "volume_is_not_a_lattice_point_count":True})
    result={"status":"pass: complete but conservative central-unit reduction bound",
            "unit_rank_certified":7,"full_unit_group_generation_required":False,
            "alternatives":alternatives,"selected":selected["name"],"C":C,
            "bound":"A<=T implies some central-unit representative has Q<=1.01*C*(2*T/2^31)^(1/8)",
            "proof":"center log majorant in the parallelepiped of 2 log|units|; convex exponential sum is maximal at a vertex",
            "cost_diagnostics":estimates,"complete_cutoff_enumerated":False,
            "sources":[{"path":str(p.relative_to(ROOT)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
                       for p in [Path(__file__),local]]}
    out=DATA/"nelson_unit_cutoff_d91.json";assert not out.exists();out.write_text(json.dumps(result,indent=2)+"\n")
    print("Unit cover constants:",[(v["name"],v["cover_constant_integer"]) for v in alternatives])
    print("Complete-cutoff bounds:",estimates)
    print("PASS|336_nelson_unit_cutoff")


if __name__=="__main__":main()
