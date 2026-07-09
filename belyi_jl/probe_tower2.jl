using Pkg; Pkg.activate(@__DIR__); using Hecke
k = GF(13); kt, x = rational_function_field(k, "x"); ky, y = polynomial_ring(kt, "y")
F, z = function_field(y^4 - x, "z"); println("genus X_2 = ", genus(F))
D0 = Hecke.zero_divisor(F(x)); P = support(D0)[1][1]
for (name, g) in [("x", F(x)), ("z", z), ("z^2", z^2)]
    println("  valuation(", name, ") at place/0 = ", valuation(Hecke.divisor(g), P))
end
# TOWER support: extend F by a sqrt (relative). Does Hecke build it + give places?
println("\n-- relative tower test --")
Fz, w = polynomial_ring(F, "w")
try
    F2, u = function_field(w^2 - (z-1), "u")
    println("relative extension built: ", F2)
    println("genus(F2) = ", genus(F2))
catch e; println("relative tower err: ", first(sprint(showerror,e),100)); end
