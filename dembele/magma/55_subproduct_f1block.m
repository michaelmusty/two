// Sub-product analysis of the q0 f1-block: is ANY sub-product of the 2-adic
// factors of h' a global factor (Deligne-bounded balanced lift)?
SetColumns(0);
Zz<z> := PolynomialRing(Integers());
load "../data/computed/dp_hg_f1_block.m";
K := 192;
R2K := Integers(2^K);
cpm := CharacteristicPolynomial(Rblk1);
printf "SP|block charpoly degree %o\n", Degree(cpm);
Zp := pAdicRing(2, K);
Zpz := PolynomialRing(Zp);
facs := Factorization(Zpz!cpm);
printf "SP|2-adic factors: %o\n", [ <Degree(t[1]), t[2]> : t in facs ];
olds := [ t : t in facs | t[2] ge 2 ];
error if #olds ne 1, "old factor (multiplicity 2) not unique";
u1 := olds[1][1];
printf "SP|u1 degree %o multiplicity %o\n", Degree(u1), olds[1][2];
newpieces := [ t[1] : t in facs | t[2] eq 1 ] cat
             [ olds[1][1] : i in [1..olds[1][2]-2] ];   // extra u1 copies beyond old, if any
printf "SP|new pieces degrees: %o (total %o)\n",
    [ Degree(p) : p in newpieces ], &+[ Degree(p) : p in newpieces ];
R2Kz := PolynomialRing(R2K);
function toR2K(p)
    return R2Kz![ R2K!(Integers()!c) : c in Coefficients(p) ];
end function;
function balanced(pol)
    return Zz![ (c lt 2^(K-1)) select c else c - 2^K where c is Integers()!co
              : co in Coefficients(pol) ];
end function;
bound := func< d | Binomial(d, d div 2) * 12^d >;
n := #newpieces;
found := 0;
for mask in [1..2^n-1] do
    prod := R2Kz!1;
    d := 0;
    for i in [1..n] do
        if mask div 2^(i-1) mod 2 eq 1 then
            prod *:= toR2K(newpieces[i]);
            d +:= Degree(newpieces[i]);
        end if;
    end for;
    bl := balanced(prod);
    mx := Max([ Abs(co) : co in Coefficients(bl) ]);
    if mx le bound(d) then
        found +:= 1;
        printf "SP|GLOBAL sub-product: mask %o, degree %o, max|coeff| ~2^%o (bound ~2^%o)\n",
            mask, d, Ilog2(Max(mx,1)), Ilog2(bound(d));
        printf "SP|  = %o\n", bl;
    end if;
end for;
printf "SP|sub-products passing the bound: %o of %o\n", found, 2^n-1;
printf "SP|done\n";
quit;
