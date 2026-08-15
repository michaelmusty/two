// k=4 genus-2 corner: the (2@0, 8@phi, 8@phi^3) passport (Ni = 12).
// REPIDX in env selects the representative (1..12).
SetColumns(0);
AttachSpec("/Users/musty/Belyi/Code/spec");
SetVerbose("Shimura", 1);
i := 1;
G := PGammaL(2, 16);
cls := Classes(G);
cm := ClassMap(G);
a := cls[3][3];
Ca := Centralizer(G, a);
CaElts := [ z : z in Ca ];
reps := [];
seen := {};
for b in Class(G, cls[10][3]) do
    c := (b*a)^-1;
    if Order(c) ne 8 or cm(c) ne 11 then continue; end if;
    if #sub<G|a,b> ne #G then continue; end if;
    canon := Min([ Eltseq(b^z) : z in CaElts ]);
    if canon in seen then continue; end if;
    Include(~seen, canon);
    Append(~reps, [Sym(17)| a, b, c]);
end for;
printf "genus-2 (2,8,8) Nielsen reps: %o, computing rep %o\n", #reps, i;
assert reps[i][3]*reps[i][2]*reps[i][1] eq Id(Sym(17));
try
    X, phi := BelyiMap(reps[i]);
    printf "RECOGNIZED: X = %o\n", X;
catch e
    printf "recognition/computation ended: %o\n", e`Object;
end try;
printf "MARKER|g2_done\n";
quit;
