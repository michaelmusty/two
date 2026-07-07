using Pkg
Pkg.activate(".")
Pkg.add("Hecke")
using Hecke
println("Hecke version: ", pkgversion(Hecke))
