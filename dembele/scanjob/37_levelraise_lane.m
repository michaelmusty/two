// Level-raising prime scan (period route, gate 1).
// Find primes q0 of F with abar_{q0} = 0 in F_256 for Dembele's constituents,
// i.e. lambda | a_{q0} in the Hecke field H of the unique 16-dimensional
// characteristic-zero component.  Since Nq is odd, the level-raising
// congruence a_q = +-(Nq+1) mod lambda is exactly abar_q = 0, and
// lambda | a_q  <=>  the constant term of charpoly(T_q | V16) is even
// (Norm(lambda) = 2^8; v_2(Norm(a_q)) = 8 v_lambda + 8 v_lambda').
//
// Usage (one process per lane, cwd = the directory holding scan2_lane*.out):
//   HMF_ROOT=/path/to/hilbertmodularforms LANE=i NLANES=8 \
//     magma -b ../two_scanjob2/37_levelraise_lane.m >> scan2_lane$i.out 2>&1
//
// RESTART SAFETY (2026-08-16).  The chatelet project restarts on an hours
// scale and a prime costs 14-20 h, so a lane must never redo work.  Two
// properties give that:
//
//   (1) SELF-HARVEST.  The static DONE set below is augmented at startup by
//       every prime already recorded in the lane logs.  Previously a restart
//       replayed the lane's first non-DONE prime, which cost ~130 CPU-hours
//       across the 8 lanes on 2026-08-15/16 alone.
//   (2) STABLE ASSIGNMENT.  Lanes are assigned by position in the FULL sorted
//       prime list, before any done-filtering, so the assignment does not
//       shift when the harvested set grows.  (With the position filter applied
//       after filtering -- the old behaviour -- two lanes restarting with
//       different harvest sets could be handed the same prime.)  This agrees
//       with the historical assignment because the 24 statically-DONE primes
//       are exactly the 24 smallest by norm and 24 = 0 mod 8.
SetColumns(0);
hmf_root := GetEnv("HMF_ROOT");
require hmf_root ne "" : "Set HMF_ROOT";
lane := StringToInteger(GetEnv("LANE"));
nlanes := StringToInteger(GetEnv("NLANES"));
AttachSpec(hmf_root cat "/spec");
SetClassGroupBounds("GRH");

Qx<x> := PolynomialRing(Rationals());
F<beta> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
M := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
assert Dimension(M) eq 57;

Zz<z> := PolynomialRing(Integers());

// build the 16-dimensional constituent subspace from T_31
g31 := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31>;
T31 := InternalHMFRawHeckeDefinite(M, p31);
cp31, rem := Quotrem(Zz!CharacteristicPolynomial(T31), z - (Norm(p31) + 1));
assert rem eq 0;
fac := Factorization(cp31);
deg16 := [ f[1] : f in fac | Degree(f[1]) eq 16 ];
assert #deg16 eq 1;
g16 := deg16[1];
printf "degree-16 factor at 31 found; building V16...\n";
T31q := ChangeRing(T31, Rationals());
V16 := Kernel(Evaluate(g16, T31q));
assert Dimension(V16) eq 16;
B16 := BasisMatrix(V16);
printf "V16 built.\n";

// ---- done set: static, plus everything already recorded in the lane logs ----
DONE := {31, 97, 127, 191, 193, 223, 257, 353, 17,383,449,479,577,607,641,673,769,863,929,991,1087,1151,1153,1217};
nstatic := #DONE;
harvested := {};
try
    // match the full printf pattern, so a half-written line from a killed
    // process cannot register a truncated prime
    logtext := Pipe("grep -hoE 'q over [0-9]+\\): trace' scan2_lane*.out 2>/dev/null", "");
    for ln in Split(logtext, "\n") do
        parts := Split(ln, " ):");
        if #parts ge 3 then
            s := parts[3];
            if #s gt 0 and forall{ c : c in Eltseq(s) | c in "0123456789" } then
                Include(~harvested, StringToInteger(s));
            end if;
        end if;
    end for;
catch e
    printf "log harvest failed (%o); continuing with the static DONE set\n", e`Object;
end try;
DONE join:= harvested;
printf "done set: %o static, %o harvested from logs, %o distinct\n",
    nstatic, #harvested, #DONE;
printf "harvested: %o\n", Sort(SetToSequence(harvested));

// primes of F by norm -- the FULL list; the lane filter uses position here,
// so it is unaffected by how much of the list is already done
NORMBOUND := 20000;
prs := [];
for q in PrimesUpTo(NORMBOUND) do
    if q eq 2 then continue; end if;
    // conjugate primes give the same parity verdict (V16 is Gal(F/Q)-stable),
    // so ONE prime per rational prime suffices: 8x cheaper
    fac := Factorization(q*OF);
    if Norm(fac[1][1]) le NORMBOUND then Append(~prs, fac[1][1]); end if;
end for;
Sort(~prs, func< a, b | Norm(a) - Norm(b) >);
printf "full list: %o primes of F with norm <= %o (%o still to do)\n",
    #prs, NORMBOUND, #[ p : p in prs | Factorization(Norm(p))[1][1] notin DONE ];

// MEMORY (2026-08-16).  A lane's Magma process grows monotonically: ~12 GB
// after one prime, ~15 GB during the second, and the per-prime requirement
// itself rises with Nq.  Eight mature lanes then exceed the 125 GB host and
// the OOM killer takes the largest -- losing a whole in-flight prime, and
// endangering the other tenants sharing the machine.  CHATELET.md's own
// guidance is to start a fresh process per slice; that used to cost a
// recomputed prime, but with the log self-harvest above a restart is free.
// So: do PRIMES_PER_RUN primes, then exit and let the watchdog relaunch.
// Overhead is the ~12 min startup against a 14-20 h prime, under 2%.
ppr := GetEnv("PRIMES_PER_RUN");
primes_per_run := ppr eq "" select 1 else StringToInteger(ppr);
printf "will exit after %o completed prime(s) so the watchdog restarts fresh\n",
    primes_per_run;

hits := 0;
done_this_run := 0;
for pi in [1..#prs] do
    if (pi mod nlanes) ne lane then continue; end if;
    pr := prs[pi];
    q := Factorization(Norm(pr))[1][1];
    if q in DONE then continue; end if;
    t0 := Cputime();
    Tq := InternalHMFRawHeckeDefinite(M, pr);
    Tqq := ChangeRing(Tq, Rationals());
    // restrict to V16: rows of B16 * Tq expressed in basis B16
    R := B16 * Tqq;
    Sol := Solution(B16, R);   // Sol * B16 = R
    cp16 := Zz!CharacteristicPolynomial(Sol);
    c0 := Integers()!Coefficient(cp16, 0);
    tr := Integers()!(-Coefficient(cp16, 15));
    ev := IsEven(c0);
    printf "Nq=%o (q over %o): trace=%o const2val=%o %o  [%o s]\n",
        Norm(pr), q, tr mod 2,
        c0 eq 0 select -1 else Valuation(c0, 2),
        ev select "<== LEVEL-RAISING PRIME" else "",
        RealField(4)!Cputime(t0);
    if ev then hits +:= 1; end if;
    if hits ge 4 then printf "found %o admissible primes; stopping\n", hits; break; end if;
    done_this_run +:= 1;
    if done_this_run ge primes_per_run then
        printf "completed %o prime(s) this run; exiting for a fresh process\n",
            done_this_run;
        break;
    end if;
end for;
printf "DONE (%o hits)\n", hits;
quit;
