r"""Definite S-arithmetic group for darmonpoints, fed by Magma-exported
Brandt data (Tate pilot, phase 3 — see README.md and
../certificates/tate-pilot-plan.md).

darmonpoints (8.3) has no definite branch for a totally real base field:
``ArithGroup(base, ...)`` routes every signature-(n,0) field to the Fuchsian
class, whose fundamental domain is out of reach here
(gate4-darmonpoints-assessment.md). This module supplies the same interface
from data the definite side gives for free: finite unit groups, the Brandt
ideal classes, and explicit `P^1(F_p)` tree representatives.

Data flow: ``57_tate_pilot_export.m`` (ONE Magma session — the rids order is
session-dependent, D26b) writes ``tate_export.json``:

    {
      "F_poly":      [c0..c8],            # x^8-8x^6+20x^4-16x^2+2 (monic, ZZ)
      "B_invariants":[a_coords, b_coords],# B = (a,b | F), each an F-elt as
                                          #   8 rationals in the power basis
      "O_basis":     [4 x [4 x F-elt]],   # Eichler order of level p31,
                                          #   Z_F-basis in B-coords (1,i,j,k)
      "p_gen":       F-elt,               # totally positive generator of p31
      "ideal_classes": [per class: 4 x [4 x F-elt] Z_F-basis],  # session order
      "bt_reps":     [32 x quaternion],   # quaternion = 4 x F-elt; map to the
                                          #   standard P^1(F_31) matrices
      "wp":          quaternion,          # norm generates p31, normalizes
                                          #   the Iwahori intersection
      "unit_gens":   [quaternions],       # generators of O^x / Z_F^x
      "splitting":   {"prec": M,          # B -> M2(Q_31): images of i, j
                      "I": [4 ints], "J": [4 ints]},   # entries mod 31^M
      "eigen":       {"a97": ..., "vector": [ints]},   # the chosen curve's
                                          #   saturated cocycle, SAME session
    }

Everything here indexes quaternions as coordinate 4-tuples over F and F-elts
as rational 8-tuples in the power basis of the defining polynomial.

Status: SKELETON. Method contracts are pinned; bodies raise until phase 2
lands. The reuse boundary (methods NOT reimplemented, per the assessment):
``reduce_in_amalgam`` (purely p-adic), ``get_covering``/``subdivide`` (tree
combinatorics over ``get_BT_reps``), the cohomology and integration layers.
"""

import json


class DefiniteArithGroupData:
    """Loader/validator for tate_export.json."""

    def __init__(self, path):
        with open(path) as f:
            self.raw = json.load(f)
        # TODO(phase 3): build F, B, O, and typed elements from the raw data;
        # validate: B ramified exactly at the 8 infinite places; O has level
        # p31; the bt_reps embed to the standard P^1(F_31) matrices; wp
        # normalizes; unit_gens generate a group of the order the stab-orders
        # bank predicts.


class DefiniteArithGroup:
    """The `Gpn`/`Gn` pair contract (small: the p31-Iwahori level group;
    large: O[1/p31]^x). Element arithmetic runs in Sage's quaternion algebra
    over F; order membership tests against the exported Z_F-basis."""

    def __init__(self, data, S_arithmetic):
        self.data = data
        self.S_arithmetic = S_arithmetic
        raise NotImplementedError("phase 3")

    def gens(self):
        """Small group: exported unit_gens. Large group: unit_gens plus the
        BT edge elements (Ihara: units + one generator per quotient-graph
        edge; the Brandt graph is connected)."""
        raise NotImplementedError

    def _is_in_order(self, x):
        """Coordinates of x in the exported O-basis are Z_F-integral
        (denominator check after solving the 4x4 F-linear system)."""
        raise NotImplementedError


class DefiniteBigArithGroup:
    """BigArithGroup-shaped façade over the exported data.

    Reused from darmonpoints unchanged (bound in as plain functions or via
    subclassing once the pilot wiring settles): reduce_in_amalgam,
    get_covering, subdivide, coset_reps machinery.
    """

    def __init__(self, export_path):
        self.data = DefiniteArithGroupData(export_path)
        raise NotImplementedError("phase 3")

    # --- identity / bookkeeping -------------------------------------------
    def base_field(self):
        raise NotImplementedError

    def prime(self):
        """The rational prime 31 (the norm-31 prime is degree 1, so the
        completion is Q_31 and darmonpoints' rational-p code paths apply)."""
        raise NotImplementedError

    def use_shapiro(self):
        return False

    def small_group(self):
        raise NotImplementedError

    def large_group(self):
        raise NotImplementedError

    def is_in_Gpn_order(self, x):
        raise NotImplementedError

    def Gpn_Obasis(self):
        raise NotImplementedError

    # --- the tree ---------------------------------------------------------
    def get_BT_reps(self):
        """The 32 exported quaternions; identity first, embedding to the
        standard matrices [[a,1],[-1,0]]-style representatives of
        P^1(F_31) (cf. sarithgroup.get_BT_reps `_hardcode_matrices`)."""
        raise NotImplementedError

    def get_BT_reps_twisted(self):
        """[1] + wp-conjugates, as in the base class."""
        raise NotImplementedError

    def wp(self):
        raise NotImplementedError

    # --- local structure --------------------------------------------------
    def local_splitting(self, prec):
        """I, J, K in M2(Q_31) mod 31^prec from the exported splitting;
        re-export at higher precision when prec exceeds the bank's."""
        raise NotImplementedError

    def embed(self, q, prec):
        raise NotImplementedError

    def get_embedding(self, prec):
        raise NotImplementedError
