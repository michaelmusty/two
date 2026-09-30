// D85 redirected loads; original SHA256 83c52081ae13bc1fbe71bc9c83f4bb0ea699601880cb8a93ab48e1fbef3a06ac
// D85 checkpoint split of 240_cm_frame_cubic_pointed_direct_function.m; SHA256 51046f3a71cd609bda05b31d7702feceda7f6b20801e517b25c2fa435058a5be
SetQuitOnError(true); SetColumns(0); SetSeed(83262); started:=Cputime();
load "dembele/magma/d85_128_199_cm_frame_cubic_precision_model.m";
WRcoords:=RBase(Matrix(ZZ,checkpoint_descended_divisor_coordinates));
qcoeff:=RBaseRow(checkpoint_q_coefficients); q:=RMultiply(qcoeff,RG1);
ucoeff:=RBaseRow(checkpoint_u_coefficients); u:=RMultiply(ucoeff,RG4);
fcoeff:=RBaseRow(checkpoint_f_coefficients); f:=RMultiply(fcoeff,RG2);
c:=RBaseRow([checkpoint_norm_scalar]); ut:=RTau(u,tt); qt:=RTau(q,tt);
xs:=[pt[1..16]:pt in liftpts[1..1024]];

C4:=RFromNative(Matrix(AG,[[&*[pt[j]^e[j]:j in [1..16]]:pt in xs]:e in cubic_quartic_monomials]));
C10:=RFromNative(Matrix(AG,[[&*[pt[j]^e[j]:j in [1..16]]:pt in xs]:e in cubic_decic_monomials]));
assert Rank(RReduce(C4)) eq 105 and Rank(RReduce(C10)) eq 285;
arow:=RCoordinates(C4,RMultiply(c,f));
denrow:=RCoordinates(C4,RScaleRows(q,qt));
numrow:=RCoordinates(C10,RMultiply(c,RAdd(RScaleRows(u,qt),RScaleRows(ut,q))));
C7:=RFromNative(Matrix(AG,[[&*[pt[j]^e[j]:j in [1..16]]:pt in xs]:e in pointed_septic_monomials]));
assert Rank(RReduce(C7)) eq 195;
ellvalues:=RFromNative(Matrix(AG,1,1024,[&+[branch_parameter_linear_form[j]*pt[j]:j in [1..16]]:pt in xs]));
denvalues:=RScaleRows(q,qt);
rawtrace:=RMultiply(c,RAdd(RScaleRows(u,qt),RScaleRows(ut,q)));
good:=[j:j in [1..1024]|RReduce(denvalues)[1,j] ne 0];
assert #good gt 660;
bvalues:=RScaleRows(RCols(rawtrace,good),RPointInverse(RCols(denvalues,good)));
septicrow:=RCoordinates(RCols(C7,good),RScaleRows(RCols(ellvalues,good),bvalues));
assert RScaleRows(RMultiply(septicrow,C7),denvalues) eq RScaleRows(ellvalues,rawtrace);
assert arow[2] eq 0 and septicrow[2] eq 0;
a0:=&+[arow[1][1,i]*pointed_a_leading_weights[i]:i in [1..105]];
b0:=&+[septicrow[1][1,i]*pointed_trace_leading_weights[i]:i in [1..195]];
assert IsUnit(a0*b0) and b0^2 eq 4*a0^3;
lambda:=2*a0*b0^-1;
arow:=RMultiply(RBaseRow([lambda^2]),arow);
septicrow:=RMultiply(RBaseRow([lambda^3]),septicrow);
numrow:=RMultiply(RBaseRow([lambda^3]),numrow);
assert &+[arow[1][1,i]*pointed_a_leading_weights[i]:i in [1..105]] eq 1;
assert &+[septicrow[1][1,i]*pointed_trace_leading_weights[i]:i in [1..195]] eq 2;
assert RScaleRows(RMultiply(septicrow,C7),denvalues) eq RScaleRows(ellvalues,RMultiply(numrow,C10));
print "PASS|FIXED_LINEAR_DENOMINATOR_AND_ROOT_FREE_SCALAR_NORMALIZATION";
if previous_cubic_modulus gt 1 then
    assert [[z mod previous_cubic_modulus:z in row]:row in BaseCoefficients(WRcoords)] eq previous_cubic_descended_divisor_coordinates;
    for item in [* <qcoeff,previous_cubic_q_coefficients>, <ucoeff,previous_cubic_u_coefficients>,
        <fcoeff,previous_cubic_f_coefficients>, <arow,previous_cubic_a_coefficients>,
        <denrow,previous_cubic_denominator_coefficients>, <numrow,previous_cubic_trace_numerator_coefficients>,
        <septicrow,previous_cubic_trace_septic_coefficients> *] do
        assert [z mod previous_cubic_modulus:z in BaseCoefficients(item[1])[1]] eq item[2];
    end for;
    assert (Integers()!c[1][1,1]) mod previous_cubic_modulus eq previous_cubic_norm_scalar;
    assert (Integers()!lambda) mod previous_cubic_modulus eq previous_cubic_scaling_scalar;
end if;
print "PASS|POINTED_COEFFICIENTWISE_REDUCTION";
printf "POINTED_DESCENDED_DIVISOR_COORDINATES|%o\n",BaseCoefficients(WRcoords);
printf "POINTED_Q_COEFFICIENTS|%o\n",BaseCoefficients(qcoeff)[1];
printf "POINTED_U_COEFFICIENTS|%o\n",BaseCoefficients(ucoeff)[1];
printf "POINTED_F_COEFFICIENTS|%o\n",BaseCoefficients(fcoeff)[1];
printf "POINTED_NORM_SCALAR|%o\n",Integers()!c[1][1,1];
printf "POINTED_A_COEFFICIENTS|%o\n",BaseCoefficients(arow)[1];
printf "POINTED_DENOMINATOR_COEFFICIENTS|%o\n",BaseCoefficients(denrow)[1];
printf "POINTED_TRACE_NUMERATOR_COEFFICIENTS|%o\n",BaseCoefficients(numrow)[1];
printf "POINTED_TRACE_SEPTIC_COEFFICIENTS|%o\n",BaseCoefficients(septicrow)[1];
printf "POINTED_SCALING_SCALAR|%o\n",Integers()!lambda;
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|262_POINTED_LAST";quit;
