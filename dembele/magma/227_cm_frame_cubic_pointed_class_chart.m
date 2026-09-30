// D82: linear normalization of any nearby class, including divisors through P.
// The caller has loaded the precision model and the exact pointed curve jets.
PS<t>:=PowerSeriesRing(ZZ,244);
chartxs:=[&+[PS!row[j+1]*t^j:j in [0..243]]+O(t^244):row in pointed_curve_jets];
function ChartMon(e,xs) return &*[xs[j]^e[j]:j in [1..16]]; end function;
chartell:=&+[branch_parameter_linear_form[i]*chartxs[i]:i in [1..16]];
charteven:=[ChartMon(e,chartxs):e in sections_even_monomial_exponents];
chartmon3:=[ChartMon(e,chartxs):e in sections_odd_monomial_exponents];
chartodd:=[&+[cubic_lift_odd_section_rows[i][j]*chartmon3[j]:j in [1..75]]:i in [1..36]];
chartj1:=charteven cat [t*x*chartell^-1:x in chartodd];
chartj2:=[chartj1[p[1]]*chartj1[p[2]]:p in makdisi_product2_pairs];
chartjets:=RBase(Matrix(ZZ,[[Coefficient(f,j):j in [0..120]]:f in chartj2]));
chart80:=RCols(chartjets,[1..80]);
assert chart80 eq RBase(Matrix(ZZ,pointed_jet2_coefficients));

function PointedClassChart(W,G2,V2,jets)
    C:=RNormalize(RCoordinates(G2,W)); W:=RMultiply(C,G2);
    j0:=RReduce(RMultiply(C,jets));
    // The first nonzero jet order equals the multiplicity of E at P:
    // L(2D0-E) has degree 120 > 2g and is base-point free after removing E.
    mu:=Min([j:j in [1..121]|&or[j0[i,j] ne 0:i in [1..81]]]);
    gi:=Min([i:i in [1..81]|j0[i,mu] ne 0]);
    gc:=RRows(C,[gi]); g:=RMultiply(gc,G2);
    N:=RQuotient(W,RScaleRows(G2,g),G2,81);
    Nc:=RCoordinates(G2,N);
    conditions:=RMultiply(Nc,RCols(jets,[1..80]));
    assert Rank(RReduce(conditions)) eq 80;
    line:=RKernelRelaxed(conditions);
    assert Nrows(line[1]) eq 1 and RIsZero(RMultiply(line,conditions));
    rc:=RNormalize(RMultiply(line,Nc)); r:=RMultiply(rc,G2);
    pointedW:=RQuotient(N,RScaleRows(G2,r),G2,81);
    result:=RNormalize(RCoordinates(G2,pointedW));
    assert result[2] eq 0 and RIsZero(RMultiply(result,RCols(jets,[1..80])));
    assert REqual(RCols(RMultiply(result,G2),[1..640]),RCols(W,[1..640]),V2);
    return result,gc,rc,mu-1;
end function;
