# General radicand solver (thesis GetCandidateFunctions): given the ramification target
# R = sum of places over the ramifying branch points, find f with div(f) = R - 2D ~ 0,
# so div(f) ≡ R (mod 2) and f is supported on S (=> cover unramified outside {0,1,oo}).
# Returns f (an element of F) or nothing.
using Hecke
using Combinatorics: with_replacement_combinations

function find_radicand_rr(F, target_places, Splaces)
    Rdiv = sum(Hecke.divisor(P) for P in target_places)
    d = degree(Rdiv)                       # even
    @assert iseven(d) "target degree odd?!"
    half = div(d, 2)
    # search D = effective divisor on S-places, degree = half, with R - 2D principal
    # enumerate multisets of S-places whose total degree == half
    degs = [Int(degree(P)) for P in Splaces]
    for combo in with_replacement_combinations(1:length(Splaces), half)
        sum(degs[j] for j in combo) == half || continue
        D = sum(Hecke.divisor(Splaces[j]) for j in combo)
        E = Rdiv - 2*D
        if Hecke.is_principal(E)
            L = riemann_roch_space(2*D - Rdiv)     # dim 1; basis element g has div(g) = R - 2D
            for g in L
                iszero(g) && continue
                return g, D
            end
        end
    end
    return nothing, nothing
end
