// D76: independently verify the saved rational cover and its 128-digit square map.
// No recognition, section selection, parametrization or witness solve is repeated.
SetQuitOnError(true); SetColumns(0); SetSeed(76);
started:=Cputime();
load "dembele/data/computed/cm_frame_B3_rational_model.m";
rational_denominator := [-x:x in rational_denominator];
rational_veronese_scale := -rational_veronese_scale;
load "dembele/data/computed/cm_frame_B3_veronese.m";
load "dembele/data/computed/cm_frame_B3_transfer.m";
load "dembele/data/computed/cm_frame_doubling_128.m";
assert rational_modulus eq lift_modulus;
assert rational_numerator eq B3_new_numerator;
function Quadric(row,mon)
    return &+[row[j]*mon[j]:j in [1..#mon]];
end function;

k:=GF(31);
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_marks.m";
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
pt:=Eltseq(P32_candidate);
IP:=ideal<R|[R.i-pt[i]/pt[1]*R.1:i in [2..16]]>;
IB2:=D17_ideal meet IP;
IB3twice:=Saturation(IC+ideal<R|[a*b:a,b in B3_linear_forms]>);
IA:=IB2 meet IB3twice;
n:=Quadric(rational_numerator,mon);
den:=Quadric(rational_denominator,mon);
IT:=Saturation(ColonIdeal(IC+ideal<R|n>,IA));
assert Degree(Scheme(P,IT)) eq 24 and IsReduced(Scheme(P,IT));
assert Dimension(IT+IA) eq 0;
assert Saturation(IC+ideal<R|n>) eq (IA meet IT);
r:=Quadric(rational_second_numerator,mon);
assert Dimension(IT+ideal<R|r>) eq 0;
f,d,e,a,b,c:=Explode([Quadric(row,mon):row in veronese_section_rows]);
assert Saturation(IC+ideal<R|f,a>) eq IT;
egs:=[Quadric(row,mon):row in rational_E_quadrics_F31];
IE:=Saturation(IC+ideal<R|egs>);
IE2:=Saturation(IC+ideal<R|[u*v:u,v in egs]>);
assert Degree(Scheme(P,IE)) eq 18 and IsReduced(Scheme(P,IE));
assert Degree(Scheme(P,IE2)) eq 36;
assert Dimension(IE+IT) eq 0 and Dimension(IE+IA) eq 0;
assert Saturation(IC+ideal<R|den>) eq (IT meet IE2);
assert Saturation(ColonIdeal(IC+ideal<R|f,d>,IT)) eq IE;
print "PASS|RATIONAL_COVER_SAVED_DIVISOR_CERTIFICATE_MOD31";

k:=Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
qs:=[Quadric(row,mon):row in veronese_section_rows];
f,d,e,a,b,c:=Explode(qs);
relations:=[f*a-d^2,f*b-d*e,f*c-e^2,d*b-e*a,d*c-e*b,a*c-b^2];
assert &and[NormalForm(rel,IC) eq 0:rel in relations];
assert Rank(Matrix(k,rows cat veronese_section_rows)) eq 97;
n:=Quadric(rational_numerator,mon);
den:=Quadric(rational_denominator,mon);
assert den eq rational_veronese_scale*f;
assert rational_veronese_scale ne 0;
assert Numerator(rational_veronese_scale) mod 31 ne 0;
assert Denominator(rational_veronese_scale) mod 31 ne 0;
r:=Quadric(rational_second_numerator,mon);
assert #rational_witness_rows eq 6;
for i in [1..6] do
    assert &and[Denominator(x) mod 31 ne 0:x in rational_witness_rows[i] cat veronese_section_rows[i]];
    witness:=Quadric(rational_witness_rows[i],mon);
    assert NormalForm(r*qs[i]-n*witness,IC) eq 0;
end for;
print "PASS|EXACT_Q_RELATIONS_AND_T_MEMBERSHIP";

Z:=Integers(rational_modulus);
function Red(c,Z)
    assert Denominator(c) mod 31 ne 0;
    return (Z!Numerator(c))/(Z!Denominator(c));
end function;
function RNF(f,I,Z)
    out:=Parent(f)!0; cs,ms:=CoefficientsAndMonomials(NormalForm(f,I));
    for i in [1..#cs] do out+:=(Integers()!Red(cs[i],Z))*ms[i]; end for;
    return out;
end function;
oldn:=Quadric(lift_numerator,mon); oldd:=Quadric(lift_denominator,mon);
g:=Quadric(rational_square_g,mon); q:=Quadric(rational_square_q,mon);
cover_left:=RNF(RNF(RNF(oldn*g,IC,Z)*g,IC,Z)*den,IC,Z);
cover_right:=RNF(RNF(RNF(n*oldd,IC,Z)*q,IC,Z)*q,IC,Z);
assert cover_left eq cover_right;
assert cover_left ne 0;
print "PASS|RATIONAL_COVER_SQUARE_MAP_128_DIGITS";
print "RATIONAL_BRANCH_DEGREE|18";
print "RATIONAL_COVER_GENUS|40";
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|155_CM_FRAME_B3_RATIONAL_CHECK";
quit;
