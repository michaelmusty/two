// D82: bound the cost of the repeated pointwise section products at eight digits.
SetQuitOnError(true); SetColumns(0); SetSeed(82207); precision_digits:=8;
load "dembele/magma/197_cm_frame_cubic_precision_arithmetic.m";
function DirectScale(A,f)
    n:=Ncols(A[1]); aa:=Eltseq(A[1]); ab:=Eltseq(A[2]); fa:=Eltseq(f[1]); fb:=Eltseq(f[2]);
    x:=[]; y:=[];
    for i in [1..#aa] do
        j:=(i-1) mod n+1; q:=ab[i]*fb[j];
        Append(~x,aa[i]*fa[j]-3*q);
        Append(~y,aa[i]*fb[j]+ab[i]*fa[j]-29*q);
    end for;
    return <Matrix(ZZ,Nrows(A[1]),n,x),Matrix(ZZ,Nrows(A[1]),n,y)>;
end function;
for rows in [81,201,321] do
    A:=<RandomMatrix(ZZ,rows,1024),RandomMatrix(ZZ,rows,1024)>;
    f:=<RandomMatrix(ZZ,1,1024),RandomMatrix(ZZ,1,1024)>;
    t:=Cputime(); a:=RScaleRows(A,f); printf "DIAGONAL_SCALE_SECONDS|%o %o\n",rows,Cputime(t);
    t:=Cputime(); b:=DirectScale(A,f); printf "DIRECT_SCALE_SECONDS|%o %o\n",rows,Cputime(t);
    assert a eq b;
end for;
print "PASS|207_CM_FRAME_CUBIC_PRECISION_SCALE_PROBE";quit;
