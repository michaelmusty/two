using Pkg; Pkg.activate(@__DIR__); using Hecke
k = GF(13); kt, x = rational_function_field(k, "x"); ky, y = polynomial_ring(kt, "y")
F, a = function_field(y^2 - (x^5 - x), "a")     # genus 2
println("genus = ", genus(F))
for expr in ["Hecke.zeta(F)", "Hecke.dedekind_zeta(F)", "Hecke.class_number(F)",
             "Hecke.number_of_points(F,1)"]
    try; println(expr, " => ", eval(Meta.parse(expr))); catch e; println(expr, " ERR ", first(sprint(showerror,e),60)); end
end
# degree-1 places: over each x=c and x=oo, take primes with residue degree 1
Ofin = finite_maximal_order(F)
deg1 = Hecke.Place[]
for c in k
    D = zero_divisor(F(x - c))
    for (P,_) in support(D); degree(P)==1 && push!(deg1, P); end
end
for (P,_) in support(pole_divisor(F(x))); degree(P)==1 && push!(deg1, P); end
println("collected ", length(deg1), " degree-1 places over x=c,oo")
# sanity: |Pic^0| for genus-2 over F_13 is L(1); count points to cross-check later
