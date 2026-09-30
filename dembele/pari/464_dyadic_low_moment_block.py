"""D121 first-moment elimination on the frozen P=200 state graph.

All NumPy integer sums have explicit bounds.  This source constructs and
certifies the low inverse, and measures graph sparsity; no actual moment
precision is raised.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'dembele/data/computed'
FP = [2, 0, -16, 0, 20, 0, -8, 0]


def source(p):
    p = Path(p).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


class Ring:
    def __init__(self, bits=25):
        assert 1 <= bits <= 25
        self.bits, self.mod = bits, 1 << bits
        self.zero = np.zeros(8, dtype=np.int64)
        self.one = self.zero.copy(); self.one[0] = 1
        eye = np.eye(8, dtype=np.int64)
        def product(x, y):
            out = [0]*15
            for i, a in enumerate(x):
                for j, b in enumerate(y):
                    out[i+j] += int(a)*int(b)
            for k in range(14, 7, -1):
                for j in range(8):
                    out[k-8+j] -= out[k]*FP[j]
            return [c % self.mod for c in out[:8]]
        self.table = np.array([[product(x, y) for y in eye] for x in eye], dtype=np.int64).transpose(0, 2, 1)
        assert 8*(self.mod-1)**2 < 2**63

    def matrix(self, values):
        return np.einsum('...i,ijk->...jk', values, self.table) % self.mod

    def mul(self, a, b):
        return np.einsum('...ij,...j->...i', self.matrix(a), b) % self.mod

    def inverse_unit(self, a):
        assert int(a[0]) & 1
        z = self.one.copy()
        for _ in range((8*self.bits-1).bit_length()):
            z = self.mul(z, (2*self.one-self.mul(a, z)) % self.mod)
        assert np.array_equal(self.mul(a, z), self.one)
        return z

    def val(self, values):
        for v in range(8*self.bits):
            if np.any(values[..., v % 8] & (1 << (v//8))):
                return v
        return 8*self.bits

    def action(self, matrix, vectors):
        # matrix shape (n,n,8), vectors shape (n,8,columns).
        n = len(matrix)
        assert 8*n*(self.mod-1)**2 < 2**63
        ans = np.empty((n, 8, vectors.shape[-1]), dtype=np.int64)
        for start in range(0, n, 16):
            kernel = self.matrix(matrix[start:start+16]).transpose(0, 2, 1, 3)
            ans[start:start+16] = (kernel.reshape(-1, 8*n) @ vectors.reshape(8*n, -1)).reshape(-1, 8, vectors.shape[-1]) % self.mod
        return ans


def transports(ring):
    path = DATA/'dyadic_moment_transports_refined_d115.json'
    packet = json.loads(path.read_text())
    params, targets = [], []
    for row in packet['transitions']:
        children, edges = [], []
        for c in row['children']:
            assert c['normalized_error_pi'] >= 200
            children.append([[int((q := Fraction(x)).numerator*pow(q.denominator, -1, ring.mod) % ring.mod) for x in z]
                             for z in c['normalized_center'][:3]])
            edges.append(c['target_edge'])
        params.append(children); targets.append(edges)
    return np.array(params, dtype=np.int64), np.array(targets, dtype=np.int64), path


def graph_profile(targets):
    n = len(targets)
    graph = [set(map(int, row)) for row in targets]
    # Reachability equivalence independently determines the SCCs at n=174.
    reach = []
    for i in range(n):
        seen, queue = {i}, [i]
        for j in queue:
            for k in graph[j]-seen:
                seen.add(k); queue.append(k)
        reach.append(seen)
    remaining = set(range(n)); components = []
    while remaining:
        i = min(remaining)
        component = {j for j in remaining if j in reach[i] and i in reach[j]}
        components.append(sorted(component)); remaining -= component
    # A directed minimum-fill diagonal elimination: every pivot is a unit,
    # so this ordering is permitted without any numerical pivot hypothesis.
    rows = [s-{i} for i, s in enumerate(graph)]
    live = set(range(n)); order = []; updates = 0; maximum = 0; fills = 0
    for _ in range(n):
        choices = []
        for k in live:
            incoming = {i for i in live if k in rows[i]}
            outgoing = rows[k] & live
            fill = sum(len(outgoing-(rows[i] | {i})) for i in incoming)
            choices.append((fill, len(incoming)*len(outgoing), k, incoming, outgoing))
        fill, cost, k, incoming, outgoing = min(choices, key=lambda x:x[:3])
        order.append(k); updates += cost; fills += fill
        for i in incoming:
            rows[i] |= outgoing-{i}; rows[i].discard(k)
        live.remove(k)
        maximum = max(maximum, sum(len(rows[i] & live) for i in live))
    return {'strong_component_sizes': sorted(map(len, components), reverse=True),
            'minimum_fill_state_order': order, 'symbolic_block_updates': updates,
            'new_offdiagonal_blocks_created': fills, 'maximum_live_offdiagonal_blocks': maximum}


def gauss_jordan(matrix, ring, order):
    n = len(matrix)
    identity = np.zeros((n, n, 8), dtype=np.int64)
    identity[np.arange(n), np.arange(n), 0] = 1
    ordered = matrix[np.ix_(order, order)]
    aug = np.concatenate((ordered.copy(), identity), axis=1)
    begin = time.monotonic(); updates = 0
    for k in range(n):
        inv = ring.inverse_unit(aug[k, k])
        aug[k] = ring.mul(inv, aug[k])
        active = np.flatnonzero(np.any(aug[:, k], axis=1)); active = active[active != k]
        columns = np.flatnonzero(np.any(aug[k], axis=1))
        values = aug[active, k].copy()
        # Each inner sum has eight terms, independent of the matrix size.
        products = np.einsum('iab,jb->ija', ring.matrix(values), aug[k, columns]) % ring.mod
        aug[np.ix_(active, columns)] = (aug[np.ix_(active, columns)]-products) % ring.mod
        updates += len(active)*len(columns)
        if k % 40 == 0:
            print(f'LOW_INVERSE|pivot={k}/{n}; seconds={time.monotonic()-begin:.3f}', flush=True)
    assert np.array_equal(aug[:, :n], identity)
    inverse = np.empty_like(matrix)
    inverse[np.ix_(order, order)] = aug[:, n:]
    return inverse, {'wall_seconds': time.monotonic()-begin, 'scalar_outer_updates': updates}


def build():
    begin = time.monotonic(); ring = Ring()
    pars, targets, transport_path = transports(ring)
    a, b, c = pars[:, :, 0], pars[:, :, 1], pars[:, :, 2]
    delta = (a-ring.mul(b, c)) % ring.mod
    assert ring.val(delta) >= 1 and ring.val(c) >= 1
    n = len(targets); assert n == 174
    matrix = np.zeros((n, n, 8), dtype=np.int64)
    matrix[np.arange(n), np.arange(n), 0] = 1
    for i in range(n):
        for branch, j in enumerate(targets[i]):
            matrix[i, j] = (matrix[i, j]-delta[i, branch]) % ring.mod
    profile = graph_profile(targets)
    inverse, timing = gauss_jordan(matrix, ring, profile['minimum_fill_state_order'])
    # Verify the left inverse with the original sparse equations, without
    # multiplying by the row-reduced matrix or reusing elimination steps.
    product = inverse.copy()
    for i in range(n):
        for branch, j in enumerate(targets[i]):
            product[i] = (product[i]-ring.mul(delta[i, branch], inverse[j])) % ring.mod
    identity = np.zeros_like(matrix)
    identity[np.arange(n), np.arange(n), 0] = 1
    assert np.array_equal(product, identity)
    bank_path = DATA/'dyadic_precision200_d115.json'
    bank = json.loads(bank_path.read_text())
    moment = np.array(bank['state_moments_power_basis'], dtype=np.int64)[:, :200].transpose(0, 1, 3, 2)
    assert moment.shape == (174, 200, 8, 16)
    # Compute the low equation RHS independently from masses and higher
    # moments: phi=b+Delta*sum_{k>=1}(-c)^(k-1)*x^k.
    rhs = np.zeros((n, 8, 16), dtype=np.int64)
    assert 200*8*(ring.mod-1)**2 < 2**63
    for i in range(n):
        for branch, j in enumerate(targets[i]):
            coefficients = np.zeros((200, 8), dtype=np.int64)
            coefficients[0] = b[i, branch]
            z = delta[i, branch].copy()
            for k in range(1, 200):
                if k >= 2: coefficients[k] = z
                z = ring.mul(z, -c[i, branch] % ring.mod)
            assert not np.any(z)  # omitted columns have valuation >=200
            operator = ring.matrix(coefficients).transpose(1, 0, 2).reshape(8, 1600)
            rhs[i] = (rhs[i]+operator @ moment[j].reshape(1600, 16)) % ring.mod
    solve_start = time.monotonic()
    answer = ring.action(inverse, rhs)
    solve_seconds = time.monotonic()-solve_start
    assert np.array_equal(answer, moment[:, 1])
    binary = DATA/'dyadic_low_moment_block_d121.npz'
    assert not binary.exists()
    np.savez_compressed(binary, P=np.array(200), matrix=matrix, inverse=inverse,
                        targets=targets, params=pars, delta=delta)
    result = {'status':'pass', 'milestone':'D121', 'low_moments_eliminated':1,
        'state_count':n, 'working_precision_pi':200,
        'all_pivots_units':True, 'inverse_verified_in_original_sparse_equations':True,
        'matrix_entries_verified':n*n*8,
        'actual_harmonic_columns_checked':16, 'first_moment_coefficients_checked':n*8*16,
        'graph_profile':profile, 'inversion':timing,
        'sixteen_column_inverse_action_seconds':solve_seconds,
        'inverse_coefficient_array_bytes':int(inverse.nbytes),
        'wall_seconds':time.monotonic()-begin,
        'maximum_dot_product_integer_sum_bound':200*8*(ring.mod-1)**2,
        'actual_moment_precision_increased':False,
        'full_Schur_iteration_validated':False,
        'sources':[source(p) for p in [Path(__file__), transport_path, bank_path, binary]]}
    print('LOW_MOMENT_BLOCK|'+json.dumps({k:v for k,v in result.items() if k not in ['sources','graph_profile']}), flush=True)
    print('LOW_GRAPH|'+json.dumps(profile), flush=True)
    return result


if __name__ == '__main__':
    out = DATA/'dyadic_low_moment_block_d121.json'
    assert not out.exists()
    out.write_text(json.dumps(build(), indent=2)+'\n')
    print('PASS|464_DYADIC_LOW_MOMENT_BLOCK', flush=True)
