// D107: exact rank of all ordered-pair cubic root monomials modulo 31.
// This is a diagnostic for distinguishing directed 17-cycles algebraically.
SetColumns(0); SetQuitOnError(true); SetSeed(107391);
started := Cputime();
k := GF(31); R<x> := PolynomialRing(k);
f := x^17-2*x^16+8*x^13+16*x^12-16*x^11+64*x^9-32*x^8
     -80*x^7+32*x^6+40*x^5+80*x^4+16*x^3-128*x^2-2*x+68;
assert IsIrreducible(f);
E<alpha> := ext<k | f>;
roots := [alpha^(31^i) : i in [0..16]];
assert #Seqset(roots) eq 17 and &and[Evaluate(f,z) eq 0 : z in roots];
pairs := [[i,j] : i,j in [0..16] | i ne j];
assert #pairs eq 272;
rows := [];
for a in [1..16] do
  values := [Eltseq(roots[(a*ij[1]) mod 17+1]^2*roots[(a*ij[2]) mod 17+1]) : ij in pairs];
  for d in [1..17] do
    Append(~rows,[values[h][d] : h in [1..272]]);
  end for;
end for;
M := Matrix(k,rows);
ker := Kernel(Transpose(M));
assert Vector(k,[1 : i in [1..272]]) in ker;
printf "RANK|%o\n",Rank(M);
printf "NULLITY|%o\n",Dimension(ker);
printf "PAIRS|%o\n",pairs;
printf "KERNEL|%o\n",[[Integers()!c : c in Eltseq(v)] : v in Basis(ker)];
printf "CPU_SECONDS|%o\n",Cputime(started);
print "PASS|D107_ROOT_PAIR_MONOMIAL_RANK";
quit;

