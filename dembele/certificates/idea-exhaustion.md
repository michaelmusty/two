# Exhaustion report: constructive routes to the explicit polynomial

## Verdict

Every concrete idea presently available for producing an explicit degree-\(257\)
polynomial is blocked. The Costa–Schiavone–Voight architecture remains the right
target shape, but it is waiting on a period / torsion front end that does not exist
in usable form for

\[
(F,N,g)=(\mathbf Q(\zeta_{32})^+,\ (1),\ 16).
\]

Machine-readable checklist: `dembele/data/computed/idea_exhaustion.json`.

## Killed routes

| Idea | Why dead |
|---|---|
| Twisted-\(L\) Oda periods | Conductor norm \(991\); \(\sim10^{10}\) coeffs/digit ([period-feasibility.md](period-feasibility.md)) |
| Greenberg–Voight Shimura \(H_1\) | Level‑1 even-degree \(F\) is definite; Magma `IsDefinite=true`; API is Hecke-only ([torsion-construction-scorecard.md](torsion-construction-scorecard.md)) |
| Magma `RieSrf` period matrices | Needs a curve equation; returns \(\operatorname{Jac}(C)\), not the RM 16-fold |
| Hack HMF `force_indefinite` / raw Brandt | No finite disc prime at level \(1\); Brandt data does not integrate to periods |
| CSV method without new front end | Eisenstein back end ready (genus‑4 control); paper supplies no period-free path |
| \(\Omega^+\) + RM \(\Rightarrow\) other signs | Split spaces are \(H\Omega^{s_i}\oplus H\Omega^+\); RM does not mix \(W_\infty\)-eigenspaces; Oda’s opposite-sign relation does not produce single-negative signs |
| \(\Omega^+\) alone | \(\sim4\cdot10^6\) coeffs/digit may be computable, but useless for the CSV lattice without \(s_i\) |
| Dense Frobenius–Hunter | \(\log_{10}(\mathrm{vol})\approx24084\) ([frob-disc-gate.md](frob-disc-gate.md)) |
| Trinomials \(x^{257}+ax+b\) | Exhaustive: \(0/930\) over \(\mathbf F_{31}\) realize any required type \(257^1\), \(1^2\cdot255^1\), or \(1^2\cdot51^5\); same absence in \(2000\) samples mod \(97\) |
| Other \(x^{257}+ax^k+b\) | For \(k\in\{2,3,5,17,51,128,256\}\), no inert / no \(51\)-type in samples; only \(k=2\) yields some \(1^2\cdot255\) |
| Quadrinomials | \(3000\) samples mod \(31\): \(0\) inert, \(0\) type \(51\); house bound \(\log_{10}(M^n)\approx232\) for \(M=8\) makes small-height search meaningless |
| LMFDB / tables | No deg‑257 or \(\mathrm{PSL}_2(\mathbf F_{256})\) field ramified only at \(2\) is tabulated; Dembélé’s existence proof is non-explicit |
| Classical \(S_2(\Gamma_0(2^k))\) | Through level \(256\), max newform Hecke degree is \(2\), nowhere near residue field \(\mathbf F_{256}\) |
| Modular CRT reconstruction of the 16-fold | No algorithm/package; ppAV moduli dimension \(136\) |
| Čerednik–Drinfeld from our Brandt module | Needs a Shimura curve / place of multiplicative reduction; our JL algebra is totally definite of finite discriminant \(1\) |
| Mascot division polynomials | Requires a curve model of the AV (CSV uses this *after* periods) |
| Inner twist / base change to smaller AV | Ruled out by residual traces ([constructive-feasibility.md](constructive-feasibility.md)) |
| Descent \(\Rightarrow\) periods | Even a descended 16-fold is \(\mathrm{GSpin}_{17}\)-type; Cunningham–Dembélé has a Schur-index gap |

## Not killed, but not actionable

| Idea | Status |
|---|---|
| Overconvergent / quaternionic \(2\)-adic symbols | Research programme; no implementation for this \((F,1)\) |
| Level-raising + CD at an auxiliary prime | Speculative; would change the modular problem |
| A genuinely new period algorithm for definite JL / Hilbert modular varieties of degree \(8\) | Does not exist yet |

## What remains true

- Characteristic-zero lift, residual match, \(C_8\)-equivariance, and (GRH) narrow principality of \(\lambda,\lambda'\) and the codifferent are solid.
- The Eisenstein isogeny-invariant back end is validated in genus \(4\) and is ready if periods appear.
- Frobenius cycle types on \(\mathbf P^1(\mathbf F_{256})\) are recorded for any future non-Hunter method.
- Remote job `lift_field_generators` may still finish and remove GRH from principality; it does not produce the polynomial.

## Recommended posture

Stop spending compute on variants of killed routes. The next advance has to be external to the present toolkit: a new mathematical construction of periods or of \(\lambda\)-torsion for this specific definite level‑one form, or an unexpected explicit model of the abelian variety. Until then, the explicit-polynomial problem is stalled at a documented hard stop.
