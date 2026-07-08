# Hecke.jl solver for 2-group Belyi maps (Path C)

Julia 1.12 + Hecke 0.39. Handles the piece Sage could not: computing radicands on
POSITIVE-genus intermediate rungs, which needs the full Pic^0 (divisor class group)
and its 2-torsion.

Architecture: the group theory stays in Sage/GAP (belyi/export_skeleton.sage emits a
JSON tower skeleton: per-level genus, per-step ramified branch points). Hecke reads it
and builds the tower, solving each radicand with divisor(f)/is_principal_with_data/
riemann_roch_space over F_p.

CONFIRMED (probe5.jl): Hecke gives the full Pic^0. For z^4=x(x-1)/F_7 (genus 1,
|Pic^0|=8), is_principal(P0-P1)=false and 2*(P0-P1) is principal -- a Pic^0[2] class,
exactly what the radicand solver needs. (Sage's class_group gave the affine order 1.)

Run: julia belyi_jl/<script>.jl

## CRUX finding (radicand solver)
Hecke gives correct is_principal (full Pic^0) and riemann_roch_space, but NO packaged
function-field class group / Jacobian. Our Belyi curves have rational branch points =>
rational 2-torsion => |Pic^0(F_p)| is ALWAYS even (checked z^4=x(x-1): no odd |Pic^0|
for p<60). So the radicand needs div(f) = D mod 2 with [D] in 2*Pic^0 and a HALVING
E with 2E ~ D in a group WITH 2-torsion -- needs Pic^0[2] structure, not just
is_principal. This is the piece Magma packages (function_field class group) that the
thesis's Algorithm 5.4 relies on. Options: (a) build class-group halving on Hecke's
is_principal (Hafner-McCurley-style, substantial); (b) check Oscar for packaged
function-field Jacobians; (c) use the thesis's specific iterative-structure trick.
