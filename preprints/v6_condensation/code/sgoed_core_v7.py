"""
SGOED v7 core — two-way (feedback) coupling with back-reaction X -> Y.

This is a MODEL CHANGE over v6. It adds a back-reaction term to the action:

    Forward (as in v6):   -g_XY * sum_mu  v_hat_mu^2  * Tr(X_mu^4)
    Back-reaction (new):  -g_YX * sum_a   w_hat_a^2   * Tr(Y_a^4)

where
    v_hat = direction built from Y traces (drives X), and
    w_hat = direction built from X traces (drives Y).

With g_YX = 0 this reduces exactly to the v6 action (used as a sanity check).

The sampler uses FULL-action recomputation (not the v6 incremental delta) for
correctness-first simplicity; the model is small (N <= 8) so speed is not a
concern here.
"""
import numpy as np


def _compute_v_hat(Y, D):
    """Direction vector (length D) built from Y traces; drives X."""
    d = Y.shape[0]
    traces = np.array([np.trace(Y[a]).real for a in range(d)])
    v = np.zeros(D)
    v[:min(d, D)] = traces[:min(d, D)]
    norm = np.linalg.norm(v)
    return v / (norm + 1e-8) if norm > 1e-8 else np.zeros(D)


def _compute_w_hat(X, d):
    """Direction vector (length d) built from X traces; drives Y."""
    D = X.shape[0]
    traces = np.array([np.trace(X[mu]).real for mu in range(D)])
    w = np.zeros(d)
    w[:min(D, d)] = traces[:min(D, d)]
    norm = np.linalg.norm(w)
    return w / (norm + 1e-8) if norm > 1e-8 else np.zeros(d)


def action_v7(X, Y, gXY, gYX, max_extent=10.0, lam=1.0, lamY=1.0, r0=1.0, rY=0.5):
    S = 0.0
    D, N, _ = X.shape
    d = Y.shape[0]

    # System X: IKKT + gate
    for mu in range(D):
        for nu in range(mu + 1, D):
            comm = X[mu] @ X[nu] - X[nu] @ X[mu]
            S += np.trace(comm @ comm.T).real
        tr2 = np.trace(X[mu] @ X[mu]).real
        S += lam * (tr2 - N * r0 ** 2) ** 2

    # Observer Y: IKKT + gate
    for a in range(d):
        for b in range(a + 1, d):
            comm = Y[a] @ Y[b] - Y[b] @ Y[a]
            S += np.trace(comm @ comm.T).real
        tr2 = np.trace(Y[a] @ Y[a]).real
        S += lamY * (tr2 - N * rY ** 2) ** 2

    # Forward coupling Y -> X
    v_hat = _compute_v_hat(Y, D)
    for mu in range(D):
        X2 = X[mu] @ X[mu]
        extent = np.trace(X2).real / N
        if extent < max_extent:
            S -= gXY * v_hat[mu] ** 2 * np.trace(X2 @ X2).real
        else:
            S += 10.0 * (extent - max_extent) ** 2

    # Back-reaction X -> Y
    w_hat = _compute_w_hat(X, d)
    for a in range(d):
        Y2 = Y[a] @ Y[a]
        extentY = np.trace(Y2).real / N
        if extentY < max_extent:
            S -= gYX * w_hat[a] ** 2 * np.trace(Y2 @ Y2).real
        else:
            S += 10.0 * (extentY - max_extent) ** 2

    return S


def run_simulation(N, D, d, gXY, gYX, seed, n_therm=20, n_meas=30, eps=0.25,
                   max_extent=10.0, lam=1.0, lamY=1.0, r0=1.0, rY=0.5,
                   record_trajectory=True):
    rng = np.random.RandomState(seed)

    X = np.zeros((D, N, N))
    for mu in range(D):
        A = rng.randn(N, N) * 0.5
        X[mu] = (A + A.T) / 2
    Y = np.zeros((d, N, N))
    for a in range(d):
        A = rng.randn(N, N) * 0.3
        Y[a] = (A + A.T) / 2

    S_curr = action_v7(X, Y, gXY, gYX, max_extent, lam, lamY, r0, rY)

    def observe():
        ext = np.array([np.trace(X[mu] @ X[mu]).real / N for mu in range(D)])
        extY = np.array([np.trace(Y[a] @ Y[a]).real / N for a in range(d)])
        v_hat = _compute_v_hat(Y, D)
        k = int(np.argmax(ext)); vmax = ext[k]
        ratio = vmax / (np.delete(ext, k).mean() + 1e-8)
        alignment = (k == int(np.argmax(np.abs(v_hat))))
        return ratio, alignment, float(vmax), float(extY.max())

    traj = {'ratio': [], 'alignment': [], 'X_max_extent': [], 'Y_max_extent': []}

    n_accept = n_propose = 0
    for sweep in range(n_therm + n_meas):
        # X updates
        for mu in range(D):
            for i in range(N):
                for j in range(i, N):
                    n_propose += 1
                    old = X[mu, i, j]
                    X[mu, i, j] = old + eps * rng.randn()
                    if i != j:
                        X[mu, j, i] = X[mu, i, j]
                    S_new = action_v7(X, Y, gXY, gYX, max_extent, lam, lamY, r0, rY)
                    dS = S_new - S_curr
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S_curr = S_new
                        n_accept += 1
                    else:
                        X[mu, i, j] = old
                        if i != j:
                            X[mu, j, i] = old
        # Y updates
        for a in range(d):
            for i in range(N):
                for j in range(i, N):
                    n_propose += 1
                    old = Y[a, i, j]
                    Y[a, i, j] = old + eps * rng.randn()
                    if i != j:
                        Y[a, j, i] = Y[a, i, j]
                    S_new = action_v7(X, Y, gXY, gYX, max_extent, lam, lamY, r0, rY)
                    dS = S_new - S_curr
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        S_curr = S_new
                        n_accept += 1
                    else:
                        Y[a, i, j] = old
                        if i != j:
                            Y[a, j, i] = old
        if record_trajectory and sweep >= n_therm:
            R, A, xmax, ymax = observe()
            traj['ratio'].append(R); traj['alignment'].append(A)
            traj['X_max_extent'].append(xmax); traj['Y_max_extent'].append(ymax)

    if record_trajectory:
        ratios = np.asarray(traj['ratio'])
        return {
            'ratio_mean': float(ratios.mean()), 'ratio_std': float(ratios.std()),
            'alignment_rate': float(np.mean(traj['alignment'])),
            'X_max_extent': float(np.mean(traj['X_max_extent'])),
            'Y_max_extent': float(np.mean(traj['Y_max_extent'])),
            'acceptance_rate': float(n_accept / max(n_propose, 1)),
            'ratio_trajectory': ratios.tolist(),
            'X_max_extent_trajectory': traj['X_max_extent'],
            'Y_max_extent_trajectory': traj['Y_max_extent'],
        }
    R, A, xmax, ymax = observe()
    return {'ratio_mean': float(R), 'alignment_rate': float(A),
            'X_max_extent': float(xmax), 'Y_max_extent': float(ymax),
            'acceptance_rate': float(n_accept / max(n_propose, 1))}
