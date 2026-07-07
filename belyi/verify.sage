# Milestone 1: verification primitives for (2-group) Belyi maps.
#
# A Belyi map here is an extension L = K[y]/(F) of the rational function field
# K = k(x), ramified only over x in {0, 1, oo}. Since ramification orders are
# 2-powers and char(k) = p is odd, all ramification is TAME, so Riemann-Hurwitz is
# exact:  2g - 2 = -2 deg + sum_{P over 0,1,oo} (e_P - 1).  Hence a cover is Belyi
# (ramified only over {0,1,oo}) iff the genus predicted from the local data at
# 0,1,oo equals the true genus L.genus().  That single identity is our workhorse.
#
# Ramification convention (calibrated against y^2 = x and y^16 = 1-x in Sage 10.6):
#   order.decomposition(prime) returns triples whose LAST entry is the
#   ramification index e; the middle entry is the residue degree f.

from sage.all import lcm, Infinity

def _ram_indices(dec):
    return sorted(int(t[-1]) for t in dec)      # e = last component (calibrated)

def ramification_over(L, x, a):
    """Multiset (sorted list) of ramification indices of L/K over x = a (a in k or oo)."""
    if a is Infinity:
        dec = L.maximal_order_infinite().decomposition()
    else:
        K = x.parent()
        prime = (x - a).zeros()[0].prime_ideal()
        dec = L.maximal_order().decomposition(prime)
    return _ram_indices(dec)

def local_data(L, x):
    return {0: ramification_over(L, x, 0),
            1: ramification_over(L, x, 1),
            Infinity: ramification_over(L, x, Infinity)}

def genus_from_local(deg, ram):
    """Tame Riemann-Hurwitz genus assuming ramification only over {0,1,oo}."""
    S = sum(sum(e - 1 for e in ram[p]) for p in (0, 1, Infinity))
    assert S % 2 == 0, ("odd total ramification -- not tame?", S)
    return 1 - deg + S // 2

def passport(ram):
    """The three ramification ORDERS (lcm of each local multiset) over 0, 1, oo."""
    return tuple(int(lcm(ram[p])) for p in (0, 1, Infinity))

def verify_belyi(L, x, expected_passport=None, expected_genus=None, name=""):
    """Return a dict of computed invariants and assert the Belyi identity + expectations."""
    deg = int(L.degree())
    ram = local_data(L, x)
    g_local = genus_from_local(deg, ram)
    g_true = int(L.genus())
    is_belyi = (g_local == g_true)          # tame RH identity: no other branch points
    pp = passport(ram)
    result = dict(name=name, degree=deg, genus=g_true, passport=pp,
                  ramification={k: v for k, v in ram.items()},
                  is_belyi=is_belyi, genus_from_local=g_local)
    assert is_belyi, (f"{name}: NOT Belyi -- extra ramification "
                      f"(genus_from_0,1,oo={g_local} != true genus={g_true})")
    if expected_genus is not None:
        assert g_true == expected_genus, (name, "genus", g_true, expected_genus)
    if expected_passport is not None:
        assert tuple(sorted(pp)) == tuple(sorted(expected_passport)), \
            (name, "passport", pp, expected_passport)
    return result
