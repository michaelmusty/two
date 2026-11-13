# D158: methodology review and pivot to "compute first, verify the polynomial"

Date: 2026-11-13. Strategic review requested by the user after the move to
a new host. No mathematical certificate; this records a change of method.

**Decision (user, 2026-11-13): adopt the pivot.** Stop pursuing a proof
that the exact genus-16 candidate is the Shimura quotient (D101–D157).
Treat the candidate curves as correct, compute the degree-257 polynomial
by p-adic torsion at a well-chosen prime, and verify the final polynomial
directly. The P10480 bank is not launched and is no longer on the route.

## 1. Inputs to the review

- Shaowu Zhang, *Rigidity to Non-Rigidity: The Inverse Galois Problem for
  M23 and Beyond* (VaNTAGe slides, 2026-11-10), on
  Huang–Jackson–Lee–Poonen–Pries–Zhang, arXiv:2608.08538.
- `michaelmusty/Belyi` pull request 41 (genus-4 non-hyperelliptic Belyi
  maps; `Doc/genus4.md`, `Doc/adr-genus4.md`).
- This repository's D100, D120, D130, D152, D155 and the 2026-09-28
  stocktake.

Lessons taken from the M23 work:

1. Rigor is deferred to the end. The genus-4 curve is computed numerically
   "without controlling errors"; only the final polynomial is verified
   exactly. The intermediate curve is never proved correct.
2. Failed recognition was a coordinate problem ("more digits do not repair
   unsuitable coordinates"); a parameter defined over the number field
   made 40 digits sufficient.
3. Exact objects were obtained by linear algebra modulo many primes and
   reconstruction, not by one high-precision lift plus lattice reduction.

## 2. Why rigidity/Belyi maps do not give the field directly

- A G-cover of P^1 has good reduction only outside primes dividing |G|
  (Beckmann). |SL2(F256)| is divisible by 3, 5, 17, 257; specialization
  adds further ramification. Rigidity realizes groups, not prescribed
  ramification.
- Only 2-group Belyi maps have good reduction outside 2; this is the
  legacy obstruction. *Unchecked remark:* the outer Galois action on the
  pro-2 fundamental group of P^1 minus three points has pro-2-by-abelian
  image (Anderson–Ihara), which appears to make every field arising from
  such covers solvable, independently of Lemma B. Not written out.
- Arithmetic triangle groups have trace fields of small degree (Takeuchi;
  from memory at most 5, not rechecked); F has degree 8.

## 3. Diagnosis of the D101–D157 methodology

1. It proves an intermediate object. A polynomial over F can be verified
   directly (ramification only at 2 from discriminants, Galois group from
   Frobenius cycle types and group theory, Hecke traces at a few primes).
2. The quadratic-twist problem of D130 does not affect the final field:
   a quadratic twist changes a mod-2 representation by a character with
   values ±1, trivial in characteristic 2, and SL2(F256) has no subgroup
   of index 2. Remaining ambiguities are finite and are caught by final
   verification.
3. The exact genus-64 cubic (D86 negative recognition) is not needed for a
   Mascot-style computation: a p-adic model of Y at one prime plus
   evaluation functions pulled back from the exact curve C suffice.
4. The certified-precision process (180-second cap, frozen replay) is
   overhead for a computation verified at the end.

## 4. The new plan

1. **Choose the prime by Frobenius order.** The torsion backend must work
   over an extension of the residue field of degree equal to the order of
   Frobenius on the target. Published values (Dembélé, Table 1): 255/257
   at norm 31, 51/257 at norm 97. About 6% of SL2(F256) has order 3, 5, 15
   or 17. Scan primes of small norm: `dembele/pivot/01_frobenius_order_scan.m`.
2. Rebuild the p-adic model of Y at the chosen prime (X is exact over Q;
   select the cubic class by point counts against Hecke data, as in D84).
3. Cost one torsion point on Chatelet. Go/no-go gate.
4. Compute the 257 values, recognize coefficients in F, verify directly.

## 5. Process for the new track

Agreed with the user: keep logs and results; update DECISIONS, HANDOFF and
REFERENCES as work proceeds; the 180-second cap, 2 GiB limits, three-worker
limit and frozen-replay requirement do not apply to new-track work on
Chatelet. All earlier frozen artifacts stay untouched. The D157 transitive
replay cannot pass on host `otto` (seven out-of-repository files are
unavailable) and is not required for this track.

## 6. Unresolved risks

- Torsion cost at genus 64 is unmeasured even at small extension degree.
- The scan may find no small-order prime at accessible norm.
- Target isolation in J(Y)[2] must be rechecked at the chosen prime.
- Final verification (absolute degree 2056 before closure) is substantial.
- Identification of C with the Shimura quotient is abandoned as a goal;
  correctness of the candidate is an assumption until the end.
