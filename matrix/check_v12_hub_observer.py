"""
v12 sink-hub vs observer dependence test (self-written, data honesty).
Q: is the dominant sink-hub tied to the OBSERVER nodes (coupling target) or
   an independent property of the system?
Tests:
  1. Hub identity over many seeds: is hub (argmax|out-in|) an observer node?
  2. Move observer offset (0, 8, N-d): does the hub follow the observer?
  3. D_root, S, imb_norm vs offset
Replicates run_v12 with configurable observer start index.
"""
import numpy as np
from numba import njit


@njit(fastmath=True)
def compute_action_obs(W, obs_start, d, alpha=0.5, beta=0.1, lambda_gate=10.0,
                       k_max=6.0, g_xy=1.5, lambda_cond=0.15, eps=1e-7):
    N = W.shape[0]
    s_sparsity = 0.0
    for i in range(N):
        for j in range(N):
            if i != j:
                s_sparsity += alpha * W[i, j] ** 2
    s_trans = 0.0
    for i in range(N):
        for k in range(N):
            if i == k:
                continue
            w2 = 0.0
            for j in range(N):
                if j != i and j != k:
                    w2 += W[i, j] * W[j, k]
            s_trans += beta * (w2 - W[i, k]) ** 2
    s_gate = 0.0
    out = np.zeros(N)
    inn = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                out[i] += W[i, j]
                inn[j] += W[i, j]
        if out[i] > k_max:
            s_gate += lambda_gate * (out[i] - k_max) ** 2
        if inn[i] > k_max:
            s_gate += lambda_gate * (inn[i] - k_max) ** 2
    # coupling on observer nodes at obs_start..obs_start+d-1
    s_coupling = 0.0
    diff_s = np.zeros(d)
    sum_sq = 0.0
    for a in range(d):
        diff_s[a] = out[obs_start + a] - inn[obs_start + a]
        sum_sq += diff_s[a] ** 2
    norm_v = np.sqrt(sum_sq) + eps
    for a in range(d):
        v_hat_a = diff_s[a] / norm_v
        sq4 = 0.0
        for j in range(N):
            if j != obs_start + a:
                sq4 += W[obs_start + a, j] ** 4
        s_coupling += -g_xy * v_hat_a * sq4
    # global SVD condensation
    s_cond = 0.0
    if lambda_cond > 0.0:
        M = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                s = 0.0
                for k in range(N):
                    s += W[i, k] * W[j, k]
                M[i, j] = s
        tr = 0.0
        for i in range(N):
            for j in range(N):
                tr += M[i, j] ** 2
        s_cond = -lambda_cond * tr
    return s_sparsity + s_trans + s_gate + s_coupling + s_cond


@njit(fastmath=True)
def run_sim_obs(N, obs_start, d, seed, n_therm=40, n_measure=20,
                step_size=0.15, g_xy=1.5, lambda_cond=0.15):
    np.random.seed(seed)
    k_max = 6.0 * np.sqrt(N / 8.0)
    W = np.random.uniform(0.05, 0.3, (N, N))
    for i in range(N):
        W[i, i] = 0.0
    cur = compute_action_obs(W, obs_start, d, k_max=k_max, g_xy=g_xy,
                             lambda_cond=lambda_cond)
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
                na = compute_action_obs(W, obs_start, d, k_max=k_max,
                                        g_xy=g_xy, lambda_cond=lambda_cond)
                ds = na - cur
                if ds <= 0.0 or np.random.uniform() < np.exp(-ds):
                    cur = na
                else:
                    W[i, j] = old
    return W


def metrics(W, obs_start, d):
    N = W.shape[0]
    out = W.sum(1)
    inn = W.sum(0)
    imb = out - inn
    hub = int(np.argmax(np.abs(imb)))
    hub_is_obs = int(obs_start <= hub < obs_start + d)
    D_root = 0.0
    for j in range(N):
        if j == hub:
            continue
        f = W[hub, j] - W[j, hub]
        if abs(f) > 1e-4:
            D_root += np.sign(f)
    D_root /= (N - 1)
    mw = W.sum() / (N * (N - 1)) + 1e-9
    imb_norm = np.mean(np.abs(imb)) / mw
    n_src = int((imb > 1e-6).sum())
    n_snk = int((imb < -1e-6).sum())
    S = (n_src - n_snk) / N
    obs_imb = np.mean(imb[obs_start:obs_start + d])
    return hub, hub_is_obs, D_root, S, imb_norm, obs_imb, imb[hub]


print("=" * 80)
print(" 1. N=32, obs at offset 0 (standard): hub identity over 20 seeds")
print("=" * 80)
hubs, hub_obs, droots, Ss, imbns = [], [], [], [], []
for s in range(42, 62):
    W = run_sim_obs(32, 0, 3, s)
    hub, ho, Dr, S, imb, oi, hi = metrics(W, 0, 3)
    hubs.append(hub)
    hub_obs.append(ho)
    droots.append(Dr)
    Ss.append(S)
    imbns.append(imb)
    print(f"  seed {s}: hub={hub} (obs? {bool(ho)}) D_root={Dr:+.2f} S={S:+.2f} obs_imb={oi:+.1f} hub_imb={hi:+.1f}")
print(f"  hub is OBSERVER node: {sum(hub_obs)}/{len(hub_obs)}")
print(f"  hub node indices: {sorted(set(hubs))}")

print()
print("=" * 80)
print(" 2. N=32, observer offset moved (8 and 29): does hub follow?")
print("=" * 80)
for off in [8, 29]:
    hubs_o, hub_obs_o, droots_o = [], [], []
    for s in range(42, 52):
        W = run_sim_obs(32, off, 3, s)
        hub, ho, Dr, S, imb, oi, hi = metrics(W, off, 3)
        hubs_o.append(hub)
        hub_obs_o.append(ho)
        droots_o.append(Dr)
    print(f"  offset={off}: hub is observer at new position: {sum(hub_obs_o)}/10 | "
          f"hubs={sorted(set(hubs_o))} | D_root={np.mean(droots_o):+.2f} +/- {np.std(droots_o):.2f}")

print()
print("=" * 80)
print(" 3. N=24 offset 0 and 8 (5 seeds) - robustness")
print("=" * 80)
for off in [0, 8]:
    hubs_o, hub_obs_o, droots_o = [], [], []
    for s in range(42, 47):
        W = run_sim_obs(24, off, 3, s)
        hub, ho, Dr, S, imb, oi, hi = metrics(W, off, 3)
        hubs_o.append(hub)
        hub_obs_o.append(ho)
        droots_o.append(Dr)
    print(f"  N=24 offset={off}: hub is observer: {sum(hub_obs_o)}/5 | D_root={np.mean(droots_o):+.2f}")
