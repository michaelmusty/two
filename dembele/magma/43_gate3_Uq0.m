// Gate 3, step 3a: build U_q0 at level q0, and time it.
//
// q0 divides the level, so the operator at q0 is U_q0, not T_q0.  Its cost is
// the one unmeasured quantity left in gate 3: the level-1 operator at norm 2401
// took 36 h, and the level-prime version may or may not be cheaper.  Measure,
// bank, and only then do the linear algebra.
//
// NOTE ON THE TEST THIS FEEDS.  Checking "U_q0 = +-1 mod 2" is VACUOUS here.
// Oldforms from level 1 satisfy x^2 - a_q0 x + Nq0; with Nq0 = 2401 = 1 mod 2
// and a_q0 = 0 mod lambda (the gate-1 hit), that is (x+1)^2 mod 2 -- so
// oldforms have U_q0 = 1 too.  What separates them is that on the Steinberg
// part U_q0 is genuinely scalar (U - 1 = 0) while on the old part U - 1 is
// nilpotent but NONZERO.  So the discriminating quantity is
// dim ker(U_q0 - 1) on the excess-carrying subspace.
SetColumns(0);
SetMemoryLimit(StringToInteger(GetEnv("G3_MEMCAP"))*1024^3);
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
q0 := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ][1];
M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
printf "U|level q0 dim %o, Norm(q0) = %o\n", Dimension(M), Norm(q0);
t0 := Cputime();
U := InternalHMFRawHeckeDefiniteSparse(M, q0);
el := Cputime(t0);
printf "U|U_q0 built: %o x %o, %o nonzeros, %o per column [%o s = %o h]\n",
    Nrows(U), Ncols(U), #Support(U), RealField(6)!(#Support(U)/Ncols(U)),
    el, RealField(4)!(el/3600);
Write("gate3_Uq0_sparse.m", Sprintf("Uq0 := %m;", U) : Overwrite := true);
printf "U|banked\n";
quit;
