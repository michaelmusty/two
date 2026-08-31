// Delta' at q0: convert the banked Eichler-mass vector (dp_W.m, from 50) to
// the true Hecke-self-adjoint pairing = the stabilizer-order diagonal, and
// verify self-adjointness of the banked dp_T31 against it on every support
// entry.  (D31: masses_i * e_i = ulcm/g is basis-INDEPENDENT, so the constant
// read in this fresh session converts the banked vector without any rebuild.)
//
// Env: HMF_ROOT, G3_MEMCAP (GB), DP_WBANK (dp_W.m), DP_TBANK (dp_T31.m),
//      DP_WTRUE (output path for the converted vector).
SetColumns(0);
memcap := GetEnv("G3_MEMCAP");
if memcap ne "" then SetMemoryLimit(StringToInteger(memcap)*1024^3); end if;
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
q0 := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ][1];
M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
stabs, ulcm, g := InternalHMFRawStabOrdersDefinite(M);
C := ulcm div g;
printf "WF|q0: ulcm %o, g %o, C = ulcm/g = %o, stabs distinct %o\n",
    ulcm, g, C, Seqset(stabs);

txt := Read(GetEnv("DP_WBANK"));
i0 := Index(txt, ":="); j0 := #txt; while txt[j0] ne ";" do j0 -:= 1; end while;
Wm := eval txt[i0+2..j0-1];
printf "WF|banked masses: N %o, distinct %o\n", #Wm, Seqset(Wm);
error if exists{ w : w in Wm | C mod w ne 0 }, "C not divisible by some banked mass";
Wt := [ C div w : w in Wm ];
printf "WF|converted W_true: distinct %o\n", Seqset(Wt);
// cross-check: multiset of converted weights = multiset of this session's stabs
printf "WF|CHECK multiset(W_true) = multiset(stabs): %o\n",
    {* w : w in Wt *} eq {* Integers()!s : s in stabs *};

txt := Read(GetEnv("DP_TBANK"));
i0 := Index(txt, ":="); j0 := #txt; while txt[j0] ne ";" do j0 -:= 1; end while;
T := eval txt[i0+2..j0-1];
printf "WF|banked T_31: %o x %o, %o nonzeros\n", Nrows(T), Ncols(T), #Support(T);
bad := 0; tot := 0;
for t in Support(T) do
    i := t[1]; j := t[2]; tot +:= 1;
    if Wt[i]*T[i,j] ne T[j,i]*Wt[j] then bad +:= 1; end if;
end for;
printf "WF|CHECK T_31 self-adjoint under W_true: %o bad of %o\n", bad, tot;
error if bad ne 0, "converted pairing is not self-adjoint: investigate before Delta'";

wt := GetEnv("DP_WTRUE");
if wt ne "" then
    Write(wt, Sprintf("Wtrue := %m;", Wt) : Overwrite := true);
    printf "WF|W_true banked to %o (same basis as dp_T31.m)\n", wt;
end if;
printf "WF|done\n";
quit;
