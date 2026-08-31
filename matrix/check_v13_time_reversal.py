"""
v13 time-reversal / irreversibility test (self-written, data honesty).
Protocol per seed:
  W1 = run(init = random)
  W2 = run(init = W1)      # warm-start: does direction persist?
  W3 = run(init = W1.T)    # reversed-start: does the system pull direction back?
Direction = sign of hub (argmax|out-in|) imbalance + G (invariant).
If arrow of time (attractor): W3 should return to W1's direction.
If symmetric: W3 follows the reversed initial (flips).
"""
import numpy as np
from numba import njit
from sgoed_graph_core_v13 import compute_graph_action_v13


@njit(fastmath=True)
def run_v13_from_W(W_init, d, g_f, g_b, p_b, n_therm=60, n_measure=5,
                   step_size=0.15, seed=1):
    np.random.seed(seed)
    N = W_init.shape[0]
    k_max = 6.0 * np.sqrt(N / 8.0)
    W = W_init.copy()
    cur = compute_graph_action_v13(W, d, 0.5, 0.1, 10.0, k_max, g_f, g_b, p_b)
    for sweep in range(n_therm + n_measure):
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                old = W[i, j]
                new = old + np.random.normal(0.0, step_size)
                if new < 0.0:
                    continue
                W[i, j] = new
                na = compute_graph_action_v13(W, d, 0.5, 0.1, 10.0, k_max, g_f, g_b, p_b)
                ds = na - cur
                if ds <= 0.0 or np.random.uniform() < np.exp(-ds):
                    cur = na
                else:
                    W[i, j] = old
    return W


def direction(W):
    N = W.shape[0]
    out = W.sum(1)
    inn = W.sum(0)
    imb = out - inn
    G = float(np.sum(np.abs(imb))) / (W.sum() + 1e-9)
    hub = int(np.argmax(np.abs(imb)))
    return hub, np.sign(imb[hub]), G


print("=" * 80)
print(" TIME-REVERSAL TEST (N=32, n_therm=60): does direction persist / pull back?")
print("=" * 80)
configs = [
    (0.0, 0.0, 2, "v13 baseline (0,0)   "),
    (1.5, 0.0, 2, "v13 forward only     "),
    (1.5, 0.2, 2, "v13 asym g_b=0.2     "),
]
for g_f, g_b, p_b, tag in configs:
    warm_same = 0
    rev_back = 0
    n = 5
    for s in range(42, 42 + n):
        rng = np.random.default_rng(s)
        W0 = rng.uniform(0.05, 0.3, (32, 32))
        np.fill_diagonal(W0, 0.0)
        W1 = run_v13_from_W(W0, 3, g_f, g_b, p_b, seed=s)
        W2 = run_v13_from_W(W1, 3, g_f, g_b, p_b, seed=s + 100)
        W3 = run_v13_from_W(W1.T.copy(), 3, g_f, g_b, p_b, seed=s + 200)
        h1, sg1, G1 = direction(W1)
        h2, sg2, G2 = direction(W2)
        h3, sg3, G3 = direction(W3)
        if sg2 == sg1:
            warm_same += 1
        if sg3 == sg1:
            rev_back += 1
    print(f"  [{tag}] warm-start keeps sign: {warm_same}/{n} | "
          f"reversed-start pulled BACK to original sign: {rev_back}/{n}")

print()
print("=" * 80)
print(" DETAIL (asym g_b=0.2, seeds 42..46): hub/sign/G + correlation")
print("=" * 80)
g_f, g_b, p_b = 1.5, 0.2, 2


def corr(A, B):
    return float(np.sum(A * B) / (np.linalg.norm(A) * np.linalg.norm(B) + 1e-12))


for s in range(42, 47):
    rng = np.random.default_rng(s)
    W0 = rng.uniform(0.05, 0.3, (32, 32))
    np.fill_diagonal(W0, 0.0)
    W1 = run_v13_from_W(W0, 3, g_f, g_b, p_b, seed=s)
    W2 = run_v13_from_W(W1, 3, g_f, g_b, p_b, seed=s + 100)
    W3 = run_v13_from_W(W1.T.copy(), 3, g_f, g_b, p_b, seed=s + 200)
    h1, sg1, G1 = direction(W1)
    h2, sg2, G2 = direction(W2)
    h3, sg3, G3 = direction(W3)
    c_orig = corr(W3, W1)
    c_rev = corr(W3, W1.T)
    print(f"  seed {s}: W1(hub={h1:2d},sg={sg1:+d},G={G1:.3f}) | "
          f"W2(warm)(hub={h2:2d},sg={sg2:+d},G={G2:.3f}) | "
          f"W3(rev) (hub={h3:2d},sg={sg3:+d},G={G3:.3f}) | "
          f"corr(W3,W1)={c_orig:+.3f} corr(W3,W1.T)={c_rev:+.3f}")
