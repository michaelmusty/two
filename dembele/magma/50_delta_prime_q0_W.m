// Delta' at q0, step 1 (gate5-delta-prime-plan.md #1): the mass vector W and
// a T_31 in ONE session's basis.
//
// The raw basis is session-dependent (D26b).  The Delta' pipeline needs only
// the PAIR (T_31, W) in one consistent basis: h_g and L_g come from T_31
// alone, and the Gram matrix pairs L_g against W.  So this script rebuilds
// the raw space, reads W, rebuilds T_31, and banks BOTH (T31_BANK, W_BANK) —
// that pair is authoritative for Delta' whatever else happens.  It ALSO
// compares the rebuilt T_31 against the gate-3 banked gk_s3_T31: if they are
// equal, this session reproduced the gate-3 basis and the other three banked
// operators (T_97/127/191) remain usable alongside W for cross-checks; if
// not, they are not — a report, not a failure.
//
// Env: HMF_ROOT, G3_MEMCAP (GB), G3_T31BANK (path to gk_s3_T31.m),
// W_BANK (output path for the mass vector), T31_BANK (output path for the
// rebuilt T_31), optional G3_LEVEL (smoke test).
SetColumns(0);
memcap := GetEnv("G3_MEMCAP");
if memcap ne "" then SetMemoryLimit(StringToInteger(memcap)*1024^3); end if;
AttachSpec(GetEnv("HMF_ROOT") cat "/spec");
SetClassGroupBounds("GRH");
Qx<x> := PolynomialRing(Rationals());
F<b> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
g31e := F![1, 2, 0, -4, 0, 1, 0, 0];
p31 := ideal<OF | OF!g31e>;
lev := GetEnv("G3_LEVEL");
if lev eq "" then
    q0 := [ p[1] : p in Factorization(7*OF) | Norm(p[1]) eq 2401 ][1];
else
    ln := StringToInteger(lev);
    q0 := [ p[1] : p in Factorization(ln*OF) | Norm(p[1]) eq ln ][1];
end if;
printf "DW|level norm %o\n", Norm(q0);

M := HilbertCuspForms(F, q0, [2 : i in [1..8]]);
t0 := Cputime();
W := InternalHMFRawInnerProductDefinite(M);
printf "DW|mass vector read [%o s]: N = %o, distinct %o, min %o, max %o, sum %o\n",
    Cputime(t0), #W, #Seqset(W), Min(W), Max(W), &+W;

t0 := Cputime();
S := InternalHMFRawHeckeDefiniteSparse(M, p31);
printf "DW|T_31 rebuilt [%o s], memory %o MB\n", Cputime(t0), GetMemoryUsage() div 1024^2;

bankfile := GetEnv("G3_T31BANK");
if bankfile ne "" then
    txt := Read(bankfile);
    i := Index(txt, ":=");
    j := #txt; while txt[j] ne ";" do j -:= 1; end while;
    Sb := eval txt[i+2..j-1];
    printf "DW|banked T_31 loaded: %o x %o, %o nonzeros\n", Nrows(Sb), Ncols(Sb), #Support(Sb);
    match := (S eq Parent(S)!Sb);
    printf "DW|CHECK rebuilt T_31 equals banked gk_s3_T31: %o\n", match;
    if not match then
        printf "DW|basis differs from the gate-3 session: gk_s3_T97/127/191 are\n";
        printf "DW|NOT usable with this W; the (T_31, W) pair banked below is.\n";
    end if;
end if;

// self-adjointness of the banked/rebuilt operator under W (cheap, sparse):
// W_i * T[i,j] = T[j,i] * W_j for all stored entries and their mirrors.
ok := true;
for t in Support(S) do
    i1 := t[1]; j1 := t[2];
    if W[i1]*S[i1,j1] ne S[j1,i1]*W[j1] then ok := false; break; end if;
end for;
printf "DW|CHECK T_31 self-adjoint under W: %o\n", ok;

wb := GetEnv("W_BANK");
if wb ne "" then
    Write(wb, Sprintf("Wmass := %m;", W) : Overwrite := true);
    printf "DW|mass vector banked to %o\n", wb;
end if;
tb := GetEnv("T31_BANK");
if tb ne "" then
    Write(tb, Sprintf("T31 := %m;", S) : Overwrite := true);
    printf "DW|rebuilt T_31 banked to %o (same session/basis as W)\n", tb;
end if;
printf "DW|done\n";
quit;
