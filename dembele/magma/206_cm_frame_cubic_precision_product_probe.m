// D82: compare exact products at eight digits before changing the arithmetic.
SetQuitOnError(true); SetColumns(0); SetSeed(82206);
Z:=Integers(31^8); A:=RandomMatrix(Z,81,201); B:=RandomMatrix(Z,201,640);
t:=Cputime(); native:=A*B; printf "NATIVE_PRODUCT_SECONDS|%o\n",Cputime(t);
t:=Cputime(); integer:=ChangeRing(ChangeRing(A,Integers())*ChangeRing(B,Integers()),Z);
printf "INTEGER_PRODUCT_SECONDS|%o\n",Cputime(t); assert integer eq native;
// Small representative row-space product too.
A:=RandomMatrix(Z,201,640); B:=RandomMatrix(Z,640,201);
t:=Cputime(); native:=A*B; printf "NATIVE_LARGE_PRODUCT_SECONDS|%o\n",Cputime(t);
t:=Cputime(); integer:=ChangeRing(ChangeRing(A,Integers())*ChangeRing(B,Integers()),Z);
printf "INTEGER_LARGE_PRODUCT_SECONDS|%o\n",Cputime(t); assert integer eq native;
print "PASS|206_CM_FRAME_CUBIC_PRECISION_PRODUCT_PROBE";quit;
