// Gate 3, step 0: feasibility probe at level q0.
//
// q0 = the prime of F above 7 with norm 2401 = 7^4, found by the gate-1 scan
// on 2026-08-22 (D23).  Before committing to the full level-raising
// verification we need two numbers: the dimension of the level-q0 space
// (predicted ~58*(Nq0+1) = 139316) and the cost of one small Hecke operator
// there.  Everything downstream is priced off those.
//
// MEMORY: capped deliberately.  The 8 gate-1 scan lanes are still running on
// this host and each is up to 35 h into a prime; an OOM would destroy that
// work.  The cap makes this probe die instead of the lanes.
SetColumns(0);
SetMemoryLimit(8*1024^3);

hmf_root := GetEnv("HMF_ROOT");
require hmf_root ne "" : "Set HMF_ROOT";
AttachSpec(hmf_root cat "/spec");
SetClassGroupBounds("GRH");

Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);

q0s := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ];
printf "primes above 7 of norm 2401: %o\n", #q0s;
q0 := q0s[1];
printf "q0: Norm = %o, RamificationDegree = %o, InertiaDegree = %o\n",
    Norm(q0), RamificationDegree(q0), InertiaDegree(q0);
printf "PROBE|q0_ok\n";

t0 := Cputime();
M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
printf "space object built [%o s]\n", Cputime(t0);

t0 := Cputime();
d := Dimension(M);
printf "PROBE|DIM=%o [%o s]\n", d, Cputime(t0);
printf "predicted 58*(Nq0+1) = %o ; ratio = %o\n", 58*2402, RealField(6)!(d/(58*2402));

// smallest prime of F (norm 31), away from 2 and q0: time one Hecke operator
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
printf "timing T_31 at level q0 (norm %o)...\n", Norm(p31);
t0 := Cputime();
T31 := InternalHMFRawHeckeDefinite(M, p31);
printf "PROBE|T31_TIME=%o s  nrows=%o\n", Cputime(t0), Nrows(T31);
printf "PROBE|done\n";
quit;
