// Compatibility intrinsic absent from the local Magma V2.29-8 installation.

intrinsic SmallPeriodMatrix(P::ModMatFldElt) -> ModMatFldElt
{Convert a big period matrix (Omega_1 | Omega_2) to Omega_2^-1 Omega_1.}
    g := Nrows(P);
    require Ncols(P) eq 2*g : "big period matrix must have twice as many columns as rows";
    omega_1 := Submatrix(P, 1, 1, g, g);
    omega_2 := Submatrix(P, 1, g + 1, g, g);
    return omega_2^-1 * omega_1;
end intrinsic;
