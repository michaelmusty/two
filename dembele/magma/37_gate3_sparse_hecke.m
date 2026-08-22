// Gate 3, step 1: one Hecke operator at level q0, sparsely.
// Level q0 has dim 109240; the dense assembly wants 45.5 GB, the sparse one
// should want ~42 MB.  This measures the real cost and confirms the operator
// is what we expect (~Norm(p)+1 nonzeros per column).
SetColumns(0);
SetMemoryLimit(12*1024^3);          // protect the gate-1 scan lanes on this host
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");

Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
q0 := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ][1];

t0 := Cputime();
M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
d := Dimension(M);
printf "G3|level q0 (norm %o), dim %o [%o s]\n", Norm(q0), d, Cputime(t0);

g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
t0 := Cputime();
T := InternalHMFRawHeckeDefiniteSparse(M, p31);
el := Cputime(t0);
nz := #Support(T);
printf "G3|T_31 sparse: %o x %o, %o nonzeros, %o per column [%o s]\n",
    Nrows(T), Ncols(T), nz, RealField(6)!(nz/Ncols(T)), el;
printf "G3|expected ~Norm(p)+1 = %o per column\n", Norm(p31)+1;
printf "G3|dense would have been %o GB\n", RealField(4)!(Nrows(T)*Ncols(T)*4/1024^3);
// bank it so later stages need not recompute
Write("gate3_T31_sparse.m", Sprintf("T31 := %m;", T) : Overwrite := true);
printf "G3|written\n";
quit;
