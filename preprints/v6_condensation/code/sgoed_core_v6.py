"""SGOED v6 core — correctness-first sampler with diagnostic telemetry."""
import numpy as np


def action_v3(X, Y, gXY, max_extent=10.0, lam=1.0, lamY=1.0, r0=1.0, rY=0.5):
    S = 0.0
    D, N, _ = X.shape
    d = Y.shape[0]
    for mu in range(D):
        for nu in range(mu + 1, D):
            comm = X[mu] @ X[nu] - X[nu] @ X[mu]
            S += np.trace(comm @ comm.T).real
        tr2 = np.trace(X[mu] @ X[mu]).real
        S += lam * (tr2 - N * r0 ** 2) ** 2
    for a in range(d):
        for b in range(a + 1, d):
            comm = Y[a] @ Y[b] - Y[b] @ Y[a]
            S += np.trace(comm @ comm.T).real
        tr2 = np.trace(Y[a] @ Y[a]).real
        S += lamY * (tr2 - N * rY ** 2) ** 2
    v_hat = _compute_v_hat(Y, D)
    for mu in range(D):
        X2 = X[mu] @ X[mu]
        extent = np.trace(X2).real / N
        if extent < max_extent:
            S -= gXY * v_hat[mu] ** 2 * np.trace(X2 @ X2).real
        else:
            S += 10.0 * (extent - max_extent) ** 2
    return S


def _compute_v_hat(Y, D):
    d = Y.shape[0]
    traces = np.array([np.trace(Y[a]).real for a in range(d)])
    v = np.zeros(D)
    v[:min(d, D)] = traces[:min(d, D)]
    norm = np.linalg.norm(v)
    return v / (norm + 1e-8) if norm > 1e-8 else np.zeros(D)


def _x_mu_local_energy(X, mu, v_hat, gXY, max_extent, lam, r0):
    D, N, _ = X.shape
    Xmu = X[mu]
    E = 0.0
    for nu in range(D):
        if nu != mu:
            comm = Xmu @ X[nu] - X[nu] @ Xmu
            E += np.trace(comm @ comm.T).real
    tr2 = np.trace(Xmu @ Xmu).real
    E += lam * (tr2 - N * r0 ** 2) ** 2
    X2 = Xmu @ Xmu
    extent = tr2 / N
    if extent < max_extent:
        E -= gXY * v_hat[mu] ** 2 * np.trace(X2 @ X2).real
    else:
        E += 10.0 * (extent - max_extent) ** 2
    return E


def _y_a_local_energy(Y, a, lamY, rY):
    d, N, _ = Y.shape
    Ya = Y[a]
    E = 0.0
    for b in range(d):
        if b != a:
            comm = Ya @ Y[b] - Y[b] @ Ya
            E += np.trace(comm @ comm.T).real
    tr2 = np.trace(Ya @ Ya).real
    return E + lamY * (tr2 - N * rY ** 2) ** 2


def _coupling_total(X, v_hat, gXY, max_extent):
    D, N, _ = X.shape
    S = 0.0
    for mu in range(D):
        X2 = X[mu] @ X[mu]
        extent = np.trace(X2).real / N
        if extent < max_extent:
            S -= gXY * v_hat[mu] ** 2 * np.trace(X2 @ X2).real
        else:
            S += 10.0 * (extent - max_extent) ** 2
    return S


def propose_delta_X(X, Y, mu, i, j, new_val, gXY, max_extent, lam, r0, v_hat):
    old = X[mu, i, j]
    old_local = _x_mu_local_energy(X, mu, v_hat, gXY, max_extent, lam, r0)
    X[mu, i, j] = new_val
    if i != j:
        X[mu, j, i] = new_val
    new_local = _x_mu_local_energy(X, mu, v_hat, gXY, max_extent, lam, r0)
    X[mu, i, j] = old
    if i != j:
        X[mu, j, i] = old
    return new_local - old_local


def propose_delta_Y(X, Y, D, a, i, j, new_val, gXY, max_extent, lamY, rY):
    old_local = _y_a_local_energy(Y, a, lamY, rY)
    v_old = _compute_v_hat(Y, D)
    c_old = _coupling_total(X, v_old, gXY, max_extent)
    old = Y[a, i, j]
    Y[a, i, j] = new_val
    if i != j:
        Y[a, j, i] = new_val
    new_local = _y_a_local_energy(Y, a, lamY, rY)
    v_new = _compute_v_hat(Y, D)
    c_new = _coupling_total(X, v_new, gXY, max_extent)
    Y[a, i, j] = old
    if i != j:
        Y[a, j, i] = old
    return (new_local - old_local) + (c_new - c_old), v_new


def integrated_autocorrelation(x, c=5.0):
    n = len(x)
    if n < 4:
        return 1.0, float(n)
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    var = np.dot(x, x) / n
    if var <= 0:
        return 1.0, float(n)
    tau = 0.5
    for M in range(1, n - 1):
        rho = np.dot(x[:n-M], x[M:]) / n / var
        tau += rho
        if M >= c * tau:
            break
    tau = max(tau, 0.5)
    return tau, max(n / (2 * tau), 1.0)


def run_simulation(N, D, d, gXY, seed, n_therm=20, n_meas=30, eps=0.25,
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
    v_hat = _compute_v_hat(Y, D)
    n_accept = n_propose = 0
    traj = {'ratio': [], 'alignment': [], 'entropy_norm': [], 'X_extents': [],
            'wall_hit': [], 'E_max': [], 'acceptance_rate': []}

    def observe():
        ext = np.array([np.trace(X[mu] @ X[mu]).real / N for mu in range(D)])
        traces = np.array([np.trace(Y[a]).real for a in range(d)])
        v = np.zeros(D); v[:min(d, D)] = traces[:min(d, D)]
        vh = v / (np.linalg.norm(v) + 1e-8) if np.linalg.norm(v) > 1e-8 else np.zeros(D)
        k = int(np.argmax(ext)); vmax = ext[k]
        ratio = vmax / (np.delete(ext, k).mean() + 1e-8)
        alignment = (k == int(np.argmax(np.abs(vh))))
        p = ext / (ext.sum() + 1e-10)
        entropy = -np.sum(p * np.log(p + 1e-10)) / np.log(D)
        hit = ext >= max_extent
        return ratio, alignment, entropy, ext, bool(np.any(hit)), float(vmax)

    for sweep in range(n_therm + n_meas):
        sweep_accept0 = n_accept
        sweep_propose0 = n_propose
        for mu in range(D):
            for i in range(N):
                for j in range(i, N):
                    n_propose += 1
                    old = X[mu, i, j]
                    new = old + eps * rng.randn()
                    dS = propose_delta_X(X, Y, mu, i, j, new, gXY, max_extent, lam, r0, v_hat)
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        X[mu, i, j] = new
                        if i != j: X[mu, j, i] = new
                        n_accept += 1
        for a in range(d):
            for i in range(N):
                for j in range(i, N):
                    n_propose += 1
                    old = Y[a, i, j]
                    new = old + eps * rng.randn()
                    dS, v_new = propose_delta_Y(X, Y, D, a, i, j, new, gXY, max_extent, lamY, rY)
                    if dS < 0 or rng.rand() < np.exp(-dS):
                        Y[a, i, j] = new
                        if i != j: Y[a, j, i] = new
                        v_hat = v_new
                        n_accept += 1
        if record_trajectory and sweep >= n_therm:
            R, A, H, ext, hit, emax = observe()
            traj['ratio'].append(R); traj['alignment'].append(A); traj['entropy_norm'].append(H)
            traj['X_extents'].append(ext.tolist()); traj['wall_hit'].append(hit); traj['E_max'].append(emax)
            traj['acceptance_rate'].append((n_accept-sweep_accept0) / max(n_propose-sweep_propose0, 1))

    acc = n_accept / max(n_propose, 1)
    if record_trajectory:
        ratios = np.asarray(traj['ratio'])
        tau, neff = integrated_autocorrelation(ratios)
        return {
            'ratio_mean': float(ratios.mean()), 'ratio_std': float(ratios.std()),
            'alignment_rate': float(np.mean(traj['alignment'])),
            'entropy_mean': float(np.mean(traj['entropy_norm'])),
            'acceptance_rate': float(acc), 'tau_int': float(tau), 'n_eff': float(neff),
            'n_meas_raw': len(ratios), 'ratio_trajectory': ratios.tolist(),
            'X_extents_trajectory': traj['X_extents'], 'E_max_trajectory': traj['E_max'],
            'wall_hit_trajectory': traj['wall_hit'],
            'wall_fraction': float(np.mean(traj['wall_hit'])),
            'acceptance_rate_trajectory': traj['acceptance_rate'],
        }
    R, A, H, ext, hit, emax = observe()
    return {'ratio_mean': float(R), 'ratio_std': 0.0, 'alignment_rate': float(A),
            'entropy_mean': float(H), 'acceptance_rate': float(acc),
            'X_extents': ext.tolist(), 'E_max': emax, 'wall_hit': hit}
