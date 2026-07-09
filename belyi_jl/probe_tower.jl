using Pkg; Pkg.activate(@__DIR__); using Hecke
k = GF(13); kt, x = rational_function_field(k, "x"); ky, y = polynomial_ring(kt, "y")
# X_2 as an ABSOLUTE model over k(x): z^4 = x  (tower P^1 c X_1 c X_2)
F, z = function_field(y^4 - x, "z"); println("genus X_2 = ", genus(F))
# valuations of functions at places over x=0
D0 = Hecke.zero_divisor(F(x))
P = support(D0)[1][1]                       # a place (prime ideal) over x=0
println("place over x=0: degree ", degree(Hecke.divisor(P)))
for (name, g) in [("x", F(x)), ("z", z), ("z^2", z^2)]
    println("  valuation(", name, ") at place over 0 = ", valuation(Hecke.divisor(g), P))
end
# is_square / sqrt of an element (recovering lower generators)?
println("is_square(F(x))? ", is_square(F(x)))
try
    ok, r = is_square_with_sqrt(F(x)); println("is_square_with_sqrt(x): ", ok, "  r^2==x: ", ok && r^2==F(x))
catch e; println("is_square_with_sqrt err: ", first(sprint(showerror,e),60)); end
