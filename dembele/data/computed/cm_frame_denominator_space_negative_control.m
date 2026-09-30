// D74: check reduced rational sections and their finite-precision coordinates.
// This verifier does not repeat the integer-kernel/LLL or coordinate solves.
SetQuitOnError(true); SetColumns(0); SetSeed(74);
started:=Cputime(); k:=Rationals();
load "dembele/data/computed/cm_frame_curve_candidate.m";
load "dembele/data/computed/cm_frame_doubling_normalized_128.m";
load "dembele/data/computed/cm_frame_denominator_space_reduced.m";
load "dembele/data/computed/cm_frame_denominator_space_coordinates.m";
space_denominator_coordinates[1] +:= normalized_modulus div 31;
IC:=Ideal(C_candidate); GC:=GroebnerBasis(IC);
mon:=[R.(p[1])*R.(p[2]):p in pairs];
function Quadric(row,mon)
    return &+[row[i]*mon[i]:i in [1..#mon]];
end function;
assert #space_section_rows eq 17 and #space_witness_rows eq 17;
assert #space_denominator_coordinates eq 17;
n:=Quadric(normalized_numerator,mon);
r:=Quadric(space_second_numerator,mon);
U<z>:=PolynomialRing(GF(31)); h:=U!normalized_residual_modulus;
coords:=[U!c:c in normalized_residual_coordinates];
value:=(&+[U!space_second_numerator[i]*coords[pairs[i][1]]*coords[pairs[i][2]]:i in [1..#pairs]]) mod h;
assert Degree(GCD(value,h)) eq 0;
for i in [1..17] do
    d:=Quadric(space_section_rows[i],mon);
    s:=Quadric(space_witness_rows[i],mon);
    assert NormalForm(r*d-n*s,IC) eq 0;
end for;
assert Rank(Matrix(GF(31),rows)) eq 91;
assert Rank(Matrix(GF(31),rows cat space_section_rows)) eq 108;
print "PASS|17_EXACT_INDEPENDENT_DENOMINATOR_SECTIONS";
q:=&+[space_denominator_coordinates[i]*Quadric(space_section_rows[i],mon):i in [1..17]];
d:=Quadric(normalized_denominator,mon);
residual:=NormalForm(q-d,IC);
assert &and[Denominator(c) mod 31 ne 0:c in Coefficients(residual)];
assert &and[Numerator(c) mod normalized_modulus eq 0:c in Coefficients(residual)];
printf "MODULUS|%o\n",normalized_modulus;
print "SPACE_DIMENSION|17";
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|136_CM_FRAME_DENOMINATOR_SPACE_CHECK";
quit;
