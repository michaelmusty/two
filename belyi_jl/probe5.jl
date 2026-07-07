using Pkg; Pkg.activate(@__DIR__)
using Hecke
k = GF(7)
kt, x = rational_function_field(k, "x")
ky, y = polynomial_ring(kt, "y")
F, a = function_field(y^4 - x*(x-1), "a")
println("genus = ", genus(F))

# individual degree-1 places over x=0 and x=1 (each cover is totally ramified there,
# so a single place P0, P1 of degree 1).  Extract at multiplicity 1 from the support.
D0 = Hecke.zero_divisor(F(x)); D1 = Hecke.zero_divisor(F(x-1))
supp0 = support(D0); supp1 = support(D1)
println("support(D0) = ", supp0)
# build the multiplicity-1 place divisors from the prime ideals in the support
P0 = Hecke.divisor(supp0[1][1])          # first prime ideal, multiplicity 1
P1 = Hecke.divisor(supp1[1][1])
println("deg P0 = ", degree(P0), "  deg P1 = ", degree(P1))
E = P0 - P1
println("is_principal(P0 - P1)? ", Hecke.is_principal(E))
for n in 1:8
    if Hecke.is_principal(n*E)
        println("smallest n with n*(P0-P1) principal: ", n, "  (=> order in Pic^0)")
        break
    end
end
