using Pkg; Pkg.activate(@__DIR__); using Hecke
k = GF(13); kt, x = rational_function_field(k, "x"); ky, y = polynomial_ring(kt, "y")
F, a = function_field(y^2 - (x^5 - x), "a")     # genus 2 (Q8-like)
println("genus = ", genus(F))
# probe native capabilities for Pic^0 / zeta / place enumeration
for expr in ["number_of_points(F, 1)", "l_polynomial(F)", "class_number(F)",
             "zeta_function(F)", "euler_characteristic(F)"]
    try; println(expr, " => ", eval(Meta.parse(expr))); catch e; println(expr, " ERR ", first(sprint(showerror,e),55)); end
end
# place enumeration by degree
for expr in ["places(F, 1)", "places(F, 2)", "degree_one_places(F)"]
    try; r=eval(Meta.parse(expr)); println(expr, " => ", length(r), " places"); catch e; println(expr, " ERR ", first(sprint(showerror,e),55)); end
end
# any divisor-class-group / picard functionality
println("\nnames matching class/picard/pic/zeta/lpoly/points:")
for n in names(Hecke; all=true)
    s=String(n)
    occursin(r"(?i)(class_group|class_number|picard|l_polynomial|zeta|number_of_points|degree_one|^places$|riemann_roch)", s) && println("  ", s)
end
