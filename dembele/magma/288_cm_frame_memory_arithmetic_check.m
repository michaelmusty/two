// D85: compare the precision-aware inverse with Magma's native Galois-ring inverse.
SetQuitOnError(true); SetColumns(0); SetSeed(85284); started:=Cputime();
precision_digits:=128;
load "dembele/magma/285_cm_frame_memory_arithmetic.m";
UZ<t>:=PolynomialRing(Integers()); AG<b>:=GaloisRing(31,128,t^2+29*t+3);
for size in [1,4,9,16,32] do
    repeat A:=RandomMatrix(AG,size,size); until Rank(RReduce(RFromNative(A))) eq size;
    pair:=RFromNative(A); inverse:=RInverse(pair);
    assert inverse eq RFromNative(A^-1);
    assert RMultiply(pair,inverse) eq RId(size);
    bad:=inverse; bad[1][1,1]+:=31^127;
    assert RMultiply(pair,bad) ne RId(size);
    printf "NATIVE_INVERSE_AGREEMENT|%o|%o\n",size,Cputime(started);
end for;
for nr in [1,7,32] do
    A:=RandomMatrix(AG,nr,41); f:=RandomMatrix(AG,1,41);
    assert RScaleRows(RFromNative(A),RFromNative(f)) eq RFromNative(A*DiagonalMatrix(Eltseq(f)));
end for;
print "PASS|288_MEMORY_ARITHMETIC";
quit;
