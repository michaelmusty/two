// Dump full-precision numerical Belyi map data for one Nielsen rep of the
// (2@0, 4@phi, 8@phi^3) passport of PGammaL(2,16), via the BELYI_DUMP_CFS hook.
// Recognition is expected to fail at default precision (that is fine: the dump
// happens first).  Equivariant renormalization + recognition happen offline in
// 11_recognize_248.m.  Usage:
//   BELYI_DUMP_CFS=out/dump_248_rep<i>.m POWSER_ARNOLDI_BIN=... \
//     magma -b repidx:=<i> 10_dump_numerics_248.m
SetColumns(0);
AttachSpec("/Users/musty/Belyi/Code/spec");
SetVerbose("Shimura", 1);

i := StringToInteger(repidx);

G := PGammaL(2, 16);
cls := Classes(G);
a := cls[3][3];
Ca := Centralizer(G, a);
CaElts := [ u : u in Ca ];
C5 := Class(G, cls[5][3]);
reps := [];
seen := {};
for b in C5 do
    c := (b*a)^-1;
    if Order(c) ne 8 then continue; end if;
    if #sub< G | a, b > ne #G then continue; end if;
    canon := Min([ Eltseq(b^u) : u in CaElts ]);
    if canon in seen then continue; end if;
    Include(~seen, canon);
    Append(~reps, [Sym(17)| a, b, c ]);
end for;
printf "Nielsen representatives: %o, computing rep %o\n", #reps, i;

try
    X, phi := BelyiMap(reps[i]);
    printf "unexpectedly recognized!  X = %o, phi = %o\n", X, phi;
catch e
    printf "recognition failed as expected (numerics already dumped): %o\n", e`Object;
end try;
quit;
