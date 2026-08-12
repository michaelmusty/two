// Local mechanism analysis at p = 3, 5, 17 for the exact (4,4,4) cover
// psi = c*y^2*F^4*E/G^4 over its degree-8 moduli field K (rep 1).
SetColumns(0);
load "out/exact_map_444_rep1_data.m";
F := FK; E := EK; G := GK; H := HK; J := JK; c := cK;

items := [*
    < "disc(F) [3 quad zeros]",      Discriminant(F) >,
    < "disc(E) [3 simple zeros]",    Discriminant(E) >,
    < "disc(G) [4 quad poles]",      Discriminant(G) >,
    < "disc(H) [3 quad pts /1]",     Discriminant(H) >,
    < "disc(J) [3 simple pts /1]",   Discriminant(J) >,
    < "Res(F,E)",                    Resultant(F, E) >,
    < "Res(F,G)",                    Resultant(F, G) >,
    < "Res(E,G)",                    Resultant(E, G) >,
    < "Res(H,J)",                    Resultant(H, J) >,
    < "Res(F,H)",                    Resultant(F, H) >,
    < "Res(G,H)",                    Resultant(G, H) >,
    < "Res(G,J)",                    Resultant(G, J) >,
    < "F(0)",  Evaluate(F, 0) >,  < "E(0)",  Evaluate(E, 0) >,
    < "G(0)",  Evaluate(G, 0) >,  < "F(1)",  Evaluate(F, 1) >,
    < "E(1)",  Evaluate(E, 1) >,  < "G(1)",  Evaluate(G, 1) >,
    < "c",     c >
*];

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
                if v ne 0 then printf "  v(%o) = %o\n", it[1], v; end if;
            end if;
        end for;
        intOK := true;
        for pol in [F, E, G, H, J] do
            for cf in Coefficients(pol) do
                if Valuation(cf, pp) lt 0 then intOK := false; end if;
            end for;
        end for;
        if Valuation(c, pp) lt 0 then intOK := false; end if;
        if not intOK then
            printf "  (coefficients not pp-integral: a fiber point escapes to infinity mod pp)\n";
            continue;
        end if;
        Fq := ResidueClassField(pp);
        RF<yb> := PolynomialRing(Fq);
        redpol := func< pol | RF![ Evaluate(cf, pp) : cf in Coefficients(pol) ] >;
        Fb := redpol(F); Eb := redpol(E); Gb := redpol(G);
        Hb := redpol(H); Jb := redpol(J);
        printf "  F mod pp: %o  E: %o  G: %o  H: %o  J: %o\n",
            [ <Degree(f[1]), f[2]> : f in Factorization(Fb) ],
            [ <Degree(f[1]), f[2]> : f in Factorization(Eb) ],
            [ <Degree(f[1]), f[2]> : f in Factorization(Gb) ],
            [ <Degree(f[1]), f[2]> : f in Factorization(Hb) ],
            [ <Degree(f[1]), f[2]> : f in Factorization(Jb) ];
        numb := yb^2 * Fb^4 * Eb; denb := Gb^4;
        g := GCD(numb, denb);
        printf "  gcd(num,den) mod pp has degree %o", Degree(g);
        if Degree(g) gt 0 then
            printf "  -> reduced map degree %o (drop %o)",
                Max(Degree(numb div g), Degree(denb div g)),
                17 - Max(Degree(numb div g), Degree(denb div g));
        end if;
        printf "\n";
        nn := numb div g; dd := denb div g;
        wr := Derivative(nn)*dd - nn*Derivative(dd);
        if wr eq 0 then
            printf "  cleaned reduced map is INSEPARABLE\n";
        else
            printf "  cleaned reduced map separable; ram divisor degree mod pp = %o\n", Degree(wr);
        end if;
    end for;
end for;
printf "\nDONE\n";
quit;
