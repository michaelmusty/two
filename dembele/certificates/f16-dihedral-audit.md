# Published resolution (2026-09-14, D42)

Dembélé's [genus-16 Shimura-curve paper](https://arxiv.org/pdf/1906.06772),
Theorem 6.4, identifies this branch with the solvable Harbater field.
The uncertainty and proposed T127 test in the historical audit below are
superseded; see `review-2026-09-14.md`. The arithmetic audit remains useful
for diagnosing the original incorrect image test.

# F16 image audit, 2026-09-14 (D41)

**D40's nonsolvability certificate is invalid.** The corrected computation leaves
a dihedral image possible. Do not start the dimension-4 period pipeline on the
assumption that these forms give a nonsolvable field.

## Error and corrected calculation

The completed `f16_steinberg.out` ends with `PASS|60_f16_steinberg`, but its two
large-image verdicts use an incorrect fallback: they check divisibility of the
surviving quadratic field's class number by 3 or 5. The order of the **trace**
in F16 is not the order of the matrix. For both quartic trace classes at 31,
`X^2 + a X + 1` has roots of order **17**. A dihedral inducing character would
therefore have order divisible by 17. The nonsplit torus is essential here;
see [Dickson's subgroup classification in Elkies's lecture notes](https://people.math.harvard.edu/~elkies/M155.15/notes.html).

`62_f16_dihedral_audit.m` independently rebuilds the nine-dimensional space of
quadratic classes unramified outside 2 and the rank-eight Legendre constraints
at all eight primes above 31. There is exactly one nontrivial survivor `M/F`.
The corrected output, `f16_dihedral_audit.out`, gives:

- `[M:Q] = 16`, signature `(0,8)`, discriminant `2^79`.
- `Cl(M) = C17`, conditional on GRH.
- One prime above 2, with `(e,f) = (16,1)` over Q.
- Both quartic trace classes at 31 have characteristic roots of order 17.

Thus the old fallback missed precisely the nontrivial class-group factor.
Local ray groups at 2 cannot add a 17-part: in any quadratic extension of F,
the residue degree is at most two, so the odd local factors divide 1 or 3.
But this survivor already has unramified order-17 characters. This does not
prove that the modular representations are dihedral; it invalidates their
claimed exclusion. Script 60's fallback has been corrected to check 17 and
print the actual class numbers. Its original output is preserved as historical
evidence; the independent script avoids a repeated 2.5-hour Hecke build.

## Completed T97 block

The old job took 8805.560 CPU seconds to build T97. On the new part its
characteristic polynomial modulo 2 is `t^40`. There remain eight joint
generalized eigenspaces, two classes up to coefficient Frobenius, each of
total dimension 20, with traces `(w,1,0)` and `(w^3,1,0)` at `(31,U,97)`.
Both have Legendre rank 8 and one dihedral survivor.

The historical verdict lines both read:

```
image contains SL2(F16) (dihedral excluded via class numbers, GRH)
```

**These lines are withdrawn.** The new verdict is:

```
dihedral NOT excluded: surviving quadratic field has class number divisible by 17
```

Agreement under the tested operators does not prove equality of full Hecke
eigensystems. In particular the number of fields, their C8 action, and the
claimed semidirect product remain undetermined. Quartic carriers do give
F16-valued residual representations, but one quartic factor of one operator
does not determine the full trace field of the degree-24 carrier.

## Next discriminating computation

Script 62 also computes ideal-class orders in M. For induction of any
nontrivial unramified order-17 character, the necessary cycle types are:

| rational prime (split completely in F) | splitting in M/F | candidate cycle type on 17 points |
|---|---|---|
| 31 | all split, classes of order 17 | `17` |
| 97 | all inert | `1 2^8` |
| 127 | all inert | `1 2^8` |
| 191 | all inert | `1 2^8` |

The measured trace zero at 97 agrees with the candidate. Trace zero alone
does not distinguish identity from a nontrivial unipotent in characteristic
two, so this is a candidate table, not a certified modular cycle table.
Computing T127 on the quartic carriers is the next direct falsification test:
any nonzero residual trace excludes this sole quadratic candidate for that
carrier. Another zero trace would not prove a dihedral image. A proof of
dihedrality requires identifying the inducing characters and certifying the
full residual congruence; a finite list of matching traces is insufficient.

Other D40 claims also require care: the smaller-base-field sweeps tested one
Hecke operator each, so their F2 traces do not establish nonexistence of all
nonsolvable systems. Monodromy Gram matrices remain usable data; transferring
the over-Q normalization and inferring recognition precision are further
steps, not consequences of this image audit.
