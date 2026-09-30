// D77: test small rational square classes using the norm before field roots.
// No maximal order, class group, or integer factorization is requested.
SetQuitOnError(true); SetColumns(0); SetSeed(77);
started:=Cputime();
load "dembele/data/computed/cm_frame_B3_fiber.m";
T<x>:=PolynomialRing(Rationals()); f:=T!fiber_nonic_coefficients;
K<a>:=NumberField(f);
alpha:=K!fiber_unit;
assert alpha ne 0 and Norm(alpha) eq fiber_unit_norm;
possible:=[c:c in [1,-1,2,-2,3,-3,6,-6]|IsSquare(fiber_unit_norm/c)];
printf "NORM_COMPATIBLE_SMALL_CLASSES|%o\n",possible;
assert #possible le 1;
found:=false; chosen:=0; witness:=K!0;
for c in possible do
    ok,s:=IsSquare(alpha/c);
    if ok then
        assert c*s^2 eq alpha;
        found:=true; chosen:=c; witness:=s;
    end if;
end for;
printf "SMALL_RATIONAL_SQUARECLASS_FOUND|%o\n",found;
printf "SMALL_RATIONAL_SQUARECLASS|%o\n",chosen;
printf "SQUARECLASS_WITNESS|%o\n",[Sprint(Coefficient(T!Eltseq(witness),i)):i in [0..8]];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|159_CM_FRAME_B3_FIBER_SQUARECLASS";
quit;
