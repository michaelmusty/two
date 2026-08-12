// Local mechanism analysis at p = 3, 5, 17 for the exact (2,4,8) cover
// psi = c*y*S^2/T^8 over its degree-8 moduli field K.
// For each prime pp of K above p: valuations of all collision invariants,
// reduction of the fiber polynomials mod pp, common factors between reduced
// numerator and denominator (degree drop), and separability of the reduction.
SetColumns(0);
load "out/exact_map_248_rep1_data.m";
ZK := Integers(K);
S := SK; T := TK; A := AK; C := CK; c := cK;

items := [*
    < "disc(S)  [8 double zeros]",      Discriminant(S) >,
    < "disc(T)  [2 octuple poles]",     Discriminant(T) >,
    < "disc(A)  [3 quadruple pts /1]",  Discriminant(A) >,
    < "disc(C)  [3 simple pts /1]",     Discriminant(C) >,
    < "Res(S,T) [zeros vs poles]",      Resultant(S, T) >,
    < "Res(S,A)",                       Resultant(S, A) >,
    < "Res(S,C)",                       Resultant(S, C) >,
    < "Res(T,A)",                       Resultant(T, A) >,
    < "Res(T,C)",                       Resultant(T, C) >,
    < "Res(A,C) [within 1-fiber]",      Resultant(A, C) >,
    < "S(0)  [double zeros vs y=0]",    Evaluate(S, 0) >,
    < "T(0)  [poles vs y=0]",           Evaluate(T, 0) >,
    < "S(1)  [double zeros vs y=1]",    Evaluate(S, 1) >,
    < "T(1)  [poles vs y=1]",           Evaluate(T, 1) >,
    < "A(0)",                           Evaluate(A, 0) >,
    < "C(0)",                           Evaluate(C, 0) >,
    < "A(1)",                           Evaluate(A, 1) >,
    < "C(1)",                           Evaluate(C, 1) >,
    < "c",                              c >
*];

RKy<yy> := PolynomialRing(K);

for p in [3, 5, 17] do
    printf "\n================ p = %o ================\n", p;
    dec := Decomposition(K, p);
    printf "%o places above %o: %o\n", #dec, p,
        [ <RamificationIndex(pr[1]), InertiaDegree(pr[1])> : pr in dec ];
    for pi in [1..#dec] do
        pp := dec[pi][1];
        printf "\n-- place %o of %o (e=%o, f=%o) --\n", pi, #dec,
            RamificationIndex(pp), InertiaDegree(pp);
        for it in items do
            if it[2] ne 0 then
                v := Valuation(it[2], pp);
                if v ne 0 then
                    printf "  v(%o) = %o\n", it[1], v;
                end if;
            end if;
        end for;
        // reduction of the fiber polynomials
        Fq := ResidueClassField(pp);
        intOK := true;
        for pol in [S, T, A, C] do
            for cf in Coefficients(pol) do
                if Valuation(cf, pp) lt 0 then intOK := false; end if;
            end for;
        end for;
        if Valuation(c, pp) lt 0 then intOK := false; end if;
        if not intOK then
            printf "  (coefficients not pp-integral: a fiber point escapes to infinity mod pp)\n";
            continue;
        end if;
        RF<yb> := PolynomialRing(Fq);
        redpol := func< pol | RF![ Evaluate(cf, pp) : cf in Coefficients(pol) ] >;
        Sb := redpol(S); Tb := redpol(T); Ab := redpol(A); Cb := redpol(C);
        printf "  S mod pp factors as %o\n", [ <Degree(f[1]), f[2]> : f in Factorization(Sb) ];
        printf "  T mod pp factors as %o\n", [ <Degree(f[1]), f[2]> : f in Factorization(Tb) ];
        printf "  A mod pp factors as %o\n", [ <Degree(f[1]), f[2]> : f in Factorization(Ab) ];
        printf "  C mod pp factors as %o\n", [ <Degree(f[1]), f[2]> : f in Factorization(Cb) ];
        // reduced map: numerator y*S^2 (times unit c), denominator T^8
        numb := yb * Sb^2; denb := Tb^8;
        g := GCD(numb, denb);
        printf "  gcd(num,den) mod pp has degree %o", Degree(g);
        if Degree(g) gt 0 then
            printf "  -> reduced map degree %o (drop %o)",
                Max(Degree(numb div g), Degree(denb div g)), 17 - Max(Degree(numb div g), Degree(denb div g));
        end if;
        printf "\n";
        nn := numb div g; dd := denb div g;
        // separability of the cleaned reduced map: d(nn/dd) = (nn' dd - nn dd')/dd^2
        wr := Derivative(nn)*dd - nn*Derivative(dd);
        if wr eq 0 then
            printf "  cleaned reduced map is INSEPARABLE (derivative identically 0)\n";
        else
            printf "  cleaned reduced map separable; ram divisor degree mod pp = %o\n", Degree(wr);
        end if;
    end for;
end for;
printf "\nDONE\n";
quit;
