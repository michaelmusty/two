// Dump full-precision numerical Belyi map data for one Nielsen rep of the
// (4@phi, 4@phi, 4@phi^2) genus-0 degree-17 passport of PGammaL(2,16).
// Cycle types: 0 -> 1^3 2^1 4^3, 1 -> 1^3 2^1 4^3, oo -> 1^1 4^4.
// Usage:
//   BELYI_DUMP_CFS=out/dump_444_rep<i>.m POWSER_ARNOLDI_BIN=... \
//     MAKEK_RELFINDER_BIN=... magma -b repidx:=<i> 15_dump_numerics_444.m
// (set MAKEK_RELFINDER_BIN so the doomed post-dump recognition fails fast)
SetColumns(0);
AttachSpec("/Users/musty/Belyi/Code/spec");
SetVerbose("Shimura", 1);

i := StringToInteger(repidx);

G := PGammaL(2, 16);
cls := Classes(G);
a := cls[5][3];                      // order 4 over phi, type 1^3 2 4^3
Ca := Centralizer(G, a);
CaElts := [ u : u in Ca ];
C5 := Class(G, cls[5][3]);
reps := [];
seen := {};
for b in C5 do
    c := (b*a)^-1;
    if Order(c) ne 4 or not IsConjugate(G, c, cls[7][3]) then continue; end if;
    if #sub< G | a, b > ne #G then continue; end if;
    canon := Min([ Eltseq(b^u) : u in CaElts ]);
    if canon in seen then continue; end if;
    Include(~seen, canon);
    Append(~reps, [Sym(17)| a, b, c ]);
end for;
printf "Nielsen representatives: %o, computing rep %o\n", #reps, i;
assert reps[i][3]*reps[i][2]*reps[i][1] eq Id(Sym(17));

try
    X, phi := BelyiMap(reps[i]);
    printf "unexpectedly recognized!  X = %o, phi = %o\n", X, phi;
catch e
    printf "recognition failed as expected (numerics already dumped): %o\n", e`Object;
end try;
quit;
