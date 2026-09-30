// D72: certify etale support algebras for the first 31-adic lift.
// No Hecke cardinality assumption or scalar multiplication is used here.
SetColumns(0); SetSeed(71); SetQuitOnError(true);
started := Cputime(); k := GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
load "dembele/data/computed/cm_frame_resolvent.m";
IC := Ideal(C_candidate); GC := GroebnerBasis(IC);
mon := [R.(p[1])*R.(p[2]) : p in resolvent_pairs];
function Quadric(row,mon)
    return &+[row[j]*mon[j] : j in [1..#mon]];
end function;
qn := Quadric(resolvent_numerator,mon);
qd := Quadric(resolvent_denominator,mon);
Eqs := [Quadric(row,mon) : row in resolvent_E_quadrics];
IE := Saturation(IC+ideal<R|Eqs>);
IE2 := Saturation(IC+ideal<R|[q*r : q,r in Eqs]>);
assert Dimension(IE) eq 1 and Degree(Scheme(P,IE)) eq 16;
assert Dimension(IE2) eq 1 and Degree(Scheme(P,IE2)) eq 32;
assert Saturation(IC+ideal<R|Eqs>) eq IE;

// Recheck the supplied exact jets, including the implicit-function condition.
PS<t> := PowerSeriesRing(k,16);
xs := [(&+[PS!resolvent_point_jets[n+1][j]*t^n : n in [0..15]])+O(t^16) : j in [1..16]];
pt := Eltseq(P32_candidate);
assert [Coefficient(x,0) : x in xs] eq [p/pt[1] : p in pt];
assert xs[1] eq 1 and xs[16]-Coefficient(xs[16],0) eq t;
assert &and[Evaluate(q,xs) eq 0 : q in polys];
dependent := [2..15];
Jac := Matrix(k,[[Evaluate(Derivative(q,j),[p/pt[1] : p in pt])
                 : j in dependent] : q in polys]);
assert Rank(Jac) eq 14;
jets := Matrix(k,[[Coefficient(Evaluate(q,xs),n) : q in mon] : n in [0..14]]);
ker := Basis(Nullspace(Transpose(jets)));
IP15 := Saturation(ideal<R|[Quadric(Eltseq(v),mon) : v in ker]>);
IP := ideal<R|[R.i-pt[i]/pt[1]*R.1 : i in [2..16]]>;
assert Dimension(IP15) eq 1 and Degree(Scheme(P,IP15)) eq 15;
assert Dimension(IE+IP) eq 0;
assert Dimension(D17_ideal+IP) eq 0;
ID32 := D17_ideal meet IP15;
assert Degree(Scheme(P,ID32)) eq 32;
assert qn in ID32 and not qn in IC;
IF := Saturation(ColonIdeal(IC+ideal<R|qn>,ID32));
assert Degree(Scheme(P,IF)) eq 28;
assert Dimension(IF+ID32) eq 0;
assert Dimension(IF+IE2) eq 0;
assert Saturation(IC+ideal<R|qn>) eq (ID32 meet IF);
assert Saturation(IC+ideal<R|qd>) eq (IE2 meet IF);
printf "DIVISOR_IDENTITY|D17 + 15*P32 - 2*E\n";
printf "E_DEGREE|%o\n", Degree(Scheme(P,IE));
printf "ODD_BRANCH_DEGREE|18\n";
printf "DOUBLE_COVER_GENUS|40\n";


procedure ExportSupport(label,J,P,R)
 k:=BaseRing(R); d:=Degree(Scheme(P,J));
 assert Dimension(J+ideal<R|R.16>) eq 0;
 S:=PolynomialRing(k,15,"grevlex");
 ia:=ideal<S|[Evaluate(f,[S.i:i in [1..15]] cat [S!1]):f in Basis(J)]>;
 L:=PolynomialRing(k,15,"lex"); il:=ideal<L|[L!f:f in GroebnerBasis(ia)]>;
 gl:=GroebnerBasis(il); assert #gl eq 15;
 U<z>:=PolynomialRing(k);
 h:=Evaluate(gl[#gl],[U!0:i in [1..14]] cat [z]);
 h/:=LeadingCoefficient(h);
 assert Degree(h) eq d and Degree(GCD(h,Derivative(h))) eq 0;
 cs:=[Evaluate(NormalForm(L.i,il),[U!0:j in [1..14]] cat [z]):i in [1..15]];
 assert cs[15] eq z;
 shape:=ideal<L|[L.i-Evaluate(cs[i],L.15):i in [1..14]] cat [Evaluate(h,L.15)]>;
 assert shape eq il;
 cs cat:=[U!1];
 assert &and[Evaluate(q,cs) mod h eq 0:q in polys];
 printf "SUPPORT|%o|%o\n",label,d;
 printf "MODULUS|%o\n",[Integers()!Coefficient(h,i):i in [0..d]];
 printf "COORDINATES|%o\n",[[Integers()!Coefficient(c,i):i in [0..d-1]]:c in cs];
 printf "FACTOR_DEGREES|%o\n",[Degree(a[1]):a in Factorization(h)];
end procedure;
ExportSupport("E",IE,P,R);
ExportSupport("F",IF,P,R);
ExportSupport("D17",D17_ideal,P,R);
printf "D17_EXTRA_ROWS|%o\n",D17_extra_rows;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|123_CM_FRAME_LIFT_SUPPORTS";quit;
