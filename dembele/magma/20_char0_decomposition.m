// Characteristic-zero newform decomposition of the level-one weight-two space.
//
// Required environment:
//   HMF_ROOT=/path/to/hilbertmodularforms

SetColumns(0);

hmf_root := GetEnv("HMF_ROOT");
if hmf_root eq "" then
    error "Set HMF_ROOT to the pinned hilbertmodularforms checkout";
end if;
AttachSpec(hmf_root cat "/spec");

Qx<x> := PolynomialRing(Rationals());
F<beta> := NumberField(x^8 - 8*x^6 + 20*x^4 - 16*x^2 + 2);
OF := Integers(F);
M := HilbertCuspForms(F, 1*OF, [2 : i in [1..8]]);
assert Dimension(M) eq 57;

pieces := NewformDecomposition(M);
dimensions := Sort([Dimension(piece) : piece in pieces]);
assert dimensions eq [1, 2, 2, 4, 16, 32];

printf "RESULT|newform_piece_count|%o\n", #pieces;
printf "RESULT|newform_dimensions|%o\n", dimensions;
for index in [1..#pieces] do
    printf "PIECE|%o|dimension|%o\n", index, Dimension(pieces[index]);
end for;
print "PASS|dembele_char0_decomposition";
