// Delta' at q0, step (b) of gate5-delta-prime-plan.md Addendum 2026-08-31:
// per-prime construction of L_g mod p by Wiedemann projection.
//
// For each worker prime p (word-size, odd):
//   1. mu := minimal polynomial of T mod p, from one Krylov pass
//      (2N sparse matvecs) + Berlekamp-Massey via the extended Euclidean
//      algorithm on (x^{2N}, sum s_i x^i); validated by convolving the
//      recurrence against the sequence at random offsets.
//   2. Check h_g | mu and gcd(mu/h_g, h_g) = 1 (else the prime is skipped:
//      mu must see h_g exactly once for the projection to work).
//   3. w := (mu/h_g)(T) v  (Horner, ~N sparse matvecs) lies in ker h_g(T);
//      verified exactly by h_g(T) w = 0.
//   4. L_g mod p is spanned by w, Tw, ..., T^{d-1} w (L_g x Q is a
//      1-dimensional K_g-vector space when multiplicity one holds; a rank
//      defect triggers a retry with a fresh v, and persistent defect is a
//      finding, not an error).  The REDUCED echelon basis w.r.t. its pivot
//      columns is canonical, so bases from different primes CRT together.
//   5. Bank B_p (rows as integer sequences), the pivot columns, and p.
//
// The combiner (53) CRTs the banks, rationally reconstructs B over Q,
// saturates over Z, and forms Gamma = B W B^t with the mass vector from
// 50_delta_prime_q0_W.m.
//
// Env: HMF_ROOT (unused but harmless), G3_MEMCAP (GB),
//      LG_TBANK (banked sparse integer T, e.g. gk_s3_T31.m),
//      LG_HG (file defining hg := [c0, ..., 1], the integer coeffs of h_g),
//      LG_PRIMES (comma-separated primes for this worker),
//      LG_OUT (output path prefix; one file per prime).
SetColumns(0);
memcap := GetEnv("G3_MEMCAP");
if memcap ne "" then SetMemoryLimit(StringToInteger(memcap)*1024^3); end if;
Zz<z> := PolynomialRing(Integers());

// ---------- inputs ---------------------------------------------------------
txt := Read(GetEnv("LG_TBANK"));
i0 := Index(txt, ":=");
j0 := #txt; while txt[j0] ne ";" do j0 -:= 1; end while;
T := eval txt[i0+2..j0-1];
N := Ncols(T);
printf "LG|T loaded: %o x %o, %o nonzeros\n", Nrows(T), N, #Support(T);
hgtxt := Read(GetEnv("LG_HG"));
i0 := Index(hgtxt, ":=");
j0 := #hgtxt; while hgtxt[j0] ne ";" do j0 -:= 1; end while;
hgcf := eval hgtxt[i0+2..j0-1];
hgZ := Zz!hgcf;
d := Degree(hgZ);
error if hgcf[#hgcf] ne 1, "h_g must be monic";
printf "LG|h_g degree %o\n", d;

// minimal polynomial of the sequence s (length 2N) by EEA:
// r0 = x^{2N}, r1 = sum s_i x^{2N-1-i} (reversed generating function);
// iterate r_{j+1} = r_{j-1} mod r_j with cofactors v_j (r = u*r0 + v*r1);
// stop when deg r < N: mu = v_j normalized (this convention makes the
// cofactor itself the minimal polynomial; validated against the sequence).
function seqMinPoly(s, p)
    Fpz := PolynomialRing(GF(p));
    n2 := #s;
    r0 := (Fpz.1)^n2;
    r1 := Fpz![ s[n2 + 1 - i] : i in [1..n2] ];   // s reversed
    v0 := Fpz!0; v1 := Fpz!1;
    while Degree(r1) ge n2 div 2 do
        q, r := Quotrem(r0, r1);
        r0 := r1; r1 := r;
        v0, v1 := Explode([ v1, v0 - q*v1 ]);
    end while;
    return (1/LeadingCoefficient(v1)) * v1;
end function;

// check that mu annihilates the recurrence at nchk random offsets
function muChecks(mu, s, nchk)
    dm := Degree(mu);
    cf := Coefficients(mu);
    for t in [1..nchk] do
        off := Random(0, #s - dm - 1);
        acc := &+[ cf[i+1]*s[off + i + 1] : i in [0..dm] ];
        if acc ne 0 then return false; end if;
    end for;
    return true;
end function;

// ---------- per-prime worker -----------------------------------------------
for ps in Split(GetEnv("LG_PRIMES"), ",") do
    p := StringToInteger(ps);
    error if not IsPrime(p) or p le 2, "LG_PRIMES entries must be odd primes";
    Fp := GF(p);
    Fpz := PolynomialRing(Fp);
    hgp := Fpz!hgcf;
    if not IsSquarefree(hgp) then
        printf "LG|p=%o: h_g not squarefree mod p, SKIP\n", p; continue;
    end if;
    Tp := ChangeRing(T, Fp);
    V := VectorSpace(Fp, N);
    t0 := Cputime();
    v := Random(V); u := Random(V);
    // Krylov pass: s_i = u . (v T^i), i = 0..2N-1
    s := [ Fp | ];
    w := v;
    for i in [1..2*N] do
        Append(~s, InnerProduct(u, w));
        w := w*Tp;
    end for;
    printf "LG|p=%o: Krylov pass [%o s]\n", p, Cputime(t0);
    t0 := Cputime();
    mu := seqMinPoly(s, p);
    ok := muChecks(mu, s, 50);
    printf "LG|p=%o: mu degree %o [%o s], recurrence check %o\n",
        p, Degree(mu), Cputime(t0), ok;
    error if not ok, "minimal-polynomial convention failed the recurrence check";
    ok, mprime := IsDivisibleBy(mu, hgp);
    if not ok then
        printf "LG|p=%o: h_g does not divide mu (u,v missed the g-part), retrying u\n", p;
        // second u over the SAME Krylov data is not stored; cheapest retry is
        // a fresh (u,v) pass -- rare, so just do it once
        v := Random(V); u := Random(V);
        s := [ Fp | ]; w := v;
        for i in [1..2*N] do Append(~s, InnerProduct(u, w)); w := w*Tp; end for;
        mu := seqMinPoly(s, p);
        ok, mprime := IsDivisibleBy(mu, hgp);
        error if not ok, "h_g does not divide mu after retry: wrong h_g or bad prime";
    end if;
    if GCD(mprime, hgp) ne 1 then
        printf "LG|p=%o: h_g^2 | mu mod p (bad prime), SKIP\n", p; continue;
    end if;
    // projection w = mprime(T) v, Horner
    t0 := Cputime();
    mc := Coefficients(mprime);
    w := mc[#mc]*v;
    for i := #mc-1 to 1 by -1 do
        w := w*Tp + mc[i]*v;
    end for;
    printf "LG|p=%o: projection [%o s]\n", p, Cputime(t0);
    // exact membership: h_g(T) w = 0
    hc := Coefficients(hgp);
    y := hc[#hc]*w;
    for i := #hc-1 to 1 by -1 do y := y*Tp + hc[i]*w; end for;
    error if not IsZero(y), "projected vector is not annihilated by h_g";
    printf "LG|p=%o: CHECK h_g(T)w = 0: true\n", p;
    // orbit basis w, wT, ..., wT^{d-1}
    rows := [ w ];
    for i in [1..d-1] do Append(~rows, rows[#rows]*Tp); end for;
    Borb := Matrix(rows);
    Bp := EchelonForm(Borb);
    rkp := Rank(Bp);
    printf "LG|p=%o: orbit rank %o (want %o)\n", p, rkp, d;
    if rkp lt d then
        printf "LG|p=%o: rank defect, SKIP (retry with another prime or v)\n", p;
        continue;
    end if;
    Bp := RowSubmatrix(Bp, 1, d);
    pivs := [ Min(Support(Bp[i])) : i in [1..d] ];
    out := Sprintf("%o_p%o.m", GetEnv("LG_OUT"), p);
    Write(out, Sprintf("p := %o;\npivs := %o;\nBrows := %o;\n",
        p, pivs, [ [ Integers()!Bp[i,j] : j in [1..N] ] : i in [1..d] ])
        : Overwrite := true);
    printf "LG|p=%o: banked %o\n", p, out;
end for;
printf "LG|done\n";
quit;
