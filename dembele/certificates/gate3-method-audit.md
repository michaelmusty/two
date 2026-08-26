# Gate 3: auditing the chain, step by step

**Date:** 2026-08-25. Written while the baseline check runs. Each step of the
argument from the gate-1 hit to "gate 3 closed", with what it rests on.

## 1. `q0` has `abar_q0 = 0` for exactly one residual system — HIGH

From `const2val = 8` and `v_2(Norm a_q) = 8 v_lambda + 8 v_lambda'`.

Two sub-claims, both check out:

- *The constant coefficient of `charpoly(T_q|V16)` is `Norm_{H/Q}(a_q)`.* `T_q`
  on `V16` is multiplication by `a_q` on `H` as a module, so its characteristic
  polynomial is the field-theoretic one and the constant term is the norm — this
  holds whether or not `a_q` generates `H`, so it does not depend on semisimplicity
  or on the eigenvalue being primitive.
- *`H` has exactly two primes above 2, unramified of residue degree 8.* Recorded
  in `data/computed/lift_field_structure.json`.

## 2. `g16bar` splits as `f1 * f2`, degree 8 each — HIGH

Observed (two *distinct* irreducibles), and structurally forced by the two
primes above 2. Independently reproduced with the `ell = 97` invariant.

## 3. Multiplicities 4 and 2 at level `q0` — HIGH

Computed twice (`ell = 31`, `ell = 97`), on `ell`-specific invariants against
different operators. The operators were themselves shape-checked: 31.99 and
97.94 nonzeros per column against the predicted `Norm(p)+1` of 32 and 98.

## 4. The oldform baseline is `2 * m1` — **VERIFIED, `m1 = 1`**

`m1` = multiplicity of `f1` in the level-1 charpoly mod 2. I assumed `m1 = 1`
(V16 the only level-1 component with that residual system) **without checking**.
The level-1 cuspidal space is 57-dimensional; mod 2, distinct components can
share a residual system. **If `m1 = 2` the baseline is 4, the excess is zero and
steps 3–5 carry no information** — and the `ell = 97` "corroboration" would be
the same error twice, not independent evidence.

**Result (2026-08-25).** Computed against the *full* level-1 charpoly mod 2
(degree 58, not merely `V16`): **both** degree-8 factors occur with multiplicity
exactly **1**. So no other level-1 component shares either residual system, the
baseline is 2, and the observed 4 / 2 is a genuine excess of +2 on exactly one
system. The assumption that could have collapsed steps 3–5 holds.

Sub-claim, standard but still unverified here: the two degeneracy maps are
injective with trivially-intersecting images, so the old subspace really is two
copies. This is the remaining soft spot in step 4.

## 5. Excess ⇒ new forms with residual system `f1` — CONTINGENT on 4

## 6. New + level exactly `q0` + trivial character ⇒ Steinberg — HIGH

Local conductor exponent 1 with trivial central character forces the special
representation (Steinberg up to unramified twist). Standard.

## 7. `rho-bar_g = rho-bar_f`, the congruence itself — **LOW. The weak link.**

This is what gate 3 was supposed to establish, and the multiplicity method does
**not** establish it. What we have: new forms whose residual `a_31` and `a_97`
share a minimal polynomial with `f`'s. What is needed: the eigensystems agree
mod `lambda`.

Two gaps:

- **Two primes is not an eigensystem.** Brauer–Nesbitt needs agreement over
  enough primes; effective Chebotarev is vacuous at this conductor (D13), so
  there is no cheap bound to appeal to.
- **Same minimal polynomial is weaker than same eigenvalue** — it permits a
  Galois conjugate. For the *field* `E` a conjugate system is harmless (it cuts
  out the same field), but it is not the same statement, and the distinction
  should be made explicitly rather than glossed.

### The cheaper decisive test

Not "more charpolys" — those cost ~2.5 h each at level `q0`. Instead, isolate
the `f1`-primary subspace **once** (dimension `<= 32`) from the banked `T_31`,
then restrict other operators to it. Each additional prime then costs only an
operator build, and on a 32-dimensional space the eigensystem comparison is
exact rather than a multiplicity count.

`T_97` at level `q0` is **already banked**, so the first such comparison is
nearly free. Cost of the isolation: `f1` has degree 8, so `f1(T)` is 8 dense
`GF(2)` multiplies plus 2 squarings for the 4th power, about 10 x 22 min ~ 4 h,
then one more for the kernel.

This upgrades the evidence from "the residual invariant appears more often than
oldforms explain" to "here is the subspace, and here is its eigensystem".


---

## 2026-08-25: the banked operators are in different bases

The eigensystem test failed at `Solution(BW, BW * A97)` with *No solution
exists* — i.e. `T_97` does not preserve `ker f1(T_31)`. Hecke operators at
primes coprime to the level commute, so that cannot happen for correctly
assembled operators in a common basis. Direct check on the banked pair:

    random vectors where v*A*B ne v*B*A: 5 of 5     COMMUTE=false

`T_31` and `T_97` at level `q0` were computed in **separate Magma sessions**, and
the package's internal ordering (ideal-class representatives, unit generators,
`P^1` enumeration) is not guaranteed reproducible across sessions.

### What this does and does not affect

- **The multiplicity results are unaffected.** A characteristic polynomial is
  basis-independent, so multiplicities 4 and 2 at `ell = 31` and `ell = 97` stand,
  as does the baseline check (single session, level 1). The gate-3 evidence of
  D25 is intact.
- **Any JOINT analysis is invalid** across banked operators: eigenspaces,
  common kernels, restrictions. Those need operators from one session.

### The alternative explanation, and how it is being excluded

Non-commuting could equally mean **the sparse patch produces wrong operators at
level `q0`**, which would invalidate everything built on them. The shape checks
(31.99 / 32 and 97.94 / 98) and the level-1 and level-31 equality tests do not
fully exclude it, since neither exercised level `q0` against a dense reference.

`46_gate3_onesession.m` decided it (2026-08-26):

    T_31 built [1253.78 s], 31.9900 per column
    T_97 built [4268.79 s], 97.9449 per column
    COMMUTE(same session)=true  (failures 0 of 8)

**The assembly is correct.** Rebuilt in one session the operators commute, as
Hecke operators at primes coprime to the level must. The banked mismatch was
purely the basis artefact.

This is also the **strongest validation the sparse patch has had at level `q0`
itself** — the one place it had never been checked against a real invariant.
The earlier evidence there was only the shape check (nonzeros per column); the
equality-against-dense tests were at levels 1 and 31. Commutativity is a far
tighter constraint: a mis-assembled operator would have to preserve an
`O(n^2)`-dimensional family of relations by accident to pass it.

**Operational rule going forward: bank operators only with the session identity
that produced them, and never combine banked operators from different sessions.**
