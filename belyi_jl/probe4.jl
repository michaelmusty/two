using Pkg; Pkg.activate(@__DIR__)
using Hecke
k = GF(7)
kt, x = rational_function_field(k, "x")
ky, y = polynomial_ring(kt, "y")
F, a = function_field(y^4 - x*(x-1), "a")
println("genus = ", genus(F), "   |Pic^0(F_7)| should be 8")

Dx = Hecke.divisor(F(x))                       # zeros over x=0, poles over x=oo
println("divisor(x) principal? ", Hecke.is_principal(Dx))   # must be TRUE
# places over x=0 and x=1 as divisors, take degree-1 pieces
D0 = Hecke.zero_divisor(F(x))                   # >=0 part: places over x=0
D1 = Hecke.zero_divisor(F(x-1))                 # places over x=1
println("deg D0 = ", degree(D0), "  deg D1 = ", degree(D1))
# a degree-0 divisor: D0 - D1
E = D0 - D1
println("deg(D0-D1) = ", degree(E))
println("is_principal(D0-D1)? ", Hecke.is_principal(E))     # expect FALSE (non-triv class)
for n in [2,4,8]
    println("is_principal(", n, "*(D0-D1))? ", Hecke.is_principal(n*E))
end
