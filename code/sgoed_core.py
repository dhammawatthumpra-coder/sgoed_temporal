"""
SGOED v5 Core Simulation Engine
Dynamical Observer Model for Temporal Emergence
"""
import numpy as np

def action_v3(X, Y, gXY, max_extent=10.0, lam=1.0, lamY=1.0, r0=1.0, rY=0.5):
    """
    Computes the total action for the SGOED v3 model with directional coupling.
    """
    S = 0.0
    D, N, _ = X.shape
    d = Y.shape[0]
    
    # System IKKT + gate
    for mu in range(D):
        for nu in range(mu+1, D):
            comm = X[mu] @ X[nu] - X[nu] @ X[mu]
            S += np.trace(comm @ comm.T).real
        tr2 = np.trace(X[mu] @ X[mu]).real
        S += lam * (tr2 - N * r0**2)**2
    
    # Observer IKKT + gate
    for a in range(d):
        for b in range(a+1, d):
            comm = Y[a] @ Y[b] - Y[b] @ Y[a]
            S += np.trace(comm @ comm.T).real
        tr2 = np.trace(Y[a] @ Y[a]).real
        S += lamY * (tr2 - N * rY**2)**2
    
    # Directional coupling
    Y_traces = np.array([np.trace(Y[a]).real for a in range(d)])
    v = np.zeros(D)
    v[:min(d, D)] = Y_traces[:min(d, D)]
    v_norm = np.linalg.norm(v)
    v_hat = v / (v_norm + 1e-8) if v_norm > 1e-8 else np.zeros(D)
    
    for mu in range(D):
        X_mu_sq = X[mu] @ X[mu]
        X_mu_4 = X_mu_sq @ X_mu_sq
        extent = np.trace(X_mu_sq).real / N
        
        if extent < max_extent:
            S -= gXY * (v_hat[mu]**2) * np.trace(X_mu_4).real
        else:
            S += 10.0 * (extent - max_extent)**2
            
    return S

def run_simulation(N, D, d, gXY, seed, n_therm=20, n_meas=30, eps=0.25, max_extent=10.0):
    """
    Runs a single Monte Carlo simulation and returns observables.
    """
    np.random.seed(seed)
    
    # Initialize X and Y
    X = np.zeros((D, N, N))
    for mu in range(D):
        A = np.random.randn(N, N) * 0.5
        X[mu] = (A + A.T) / 2
        
    Y = np.zeros((d, N, N))
    for a in range(d):
        A = np.random.randn(N, N) * 0.3
        Y[a] = (A + A.T) / 2
        
    S_curr = action_v3(X, Y, gXY, max_extent)
    
    # Metropolis-Hastings sweeps
    for sweep in range(n_therm + n_meas):
        # Optimize step size for larger N
        step = 2 if N > 6 else 1
        
        # Update X
        for mu in range(D):
            for i in range(0, N, step):
                for j in range(i, N, step):
                    old = X[mu, i, j]
                    X[mu, i, j] = old + eps * np.random.randn()
                    if i != j: X[mu, j, i] = X[mu, i, j]
                    
                    S_new = action_v3(X, Y, gXY, max_extent)
                    dS = S_new - S_curr
                    if dS < 0 or np.random.rand() < np.exp(-dS):
                        S_curr = S_new
                    else:
                        X[mu, i, j] = old
                        if i != j: X[mu, j, i] = old
                        
        # Update Y
        for a in range(d):
            for i in range(N):
                for j in range(i, N):
                    old = Y[a, i, j]
                    Y[a, i, j] = old + eps * np.random.randn()
                    if i != j: Y[a, j, i] = Y[a, i, j]
                    
                    S_new = action_v3(X, Y, gXY, max_extent)
                    dS = S_new - S_curr
                    if dS < 0 or np.random.rand() < np.exp(-dS):
                        S_curr = S_new
                    else:
                        Y[a, i, j] = old
                        if i != j: Y[a, j, i] = old
                        
    # Analysis / Observables
    X_extents = np.array([np.trace(X[mu] @ X[mu]).real / N for mu in range(D)])
    Y_traces = np.array([np.trace(Y[a]).real for a in range(d)])
    
    v = np.zeros(D)
    v[:min(d, D)] = Y_traces[:min(d, D)]
    v_norm = np.linalg.norm(v)
    v_hat = v / (v_norm + 1e-8) if v_norm > 1e-8 else np.zeros(D)
    
    X_max_idx = int(np.argmax(X_extents))
    X_max_val = X_extents[X_max_idx]
    X_others = np.delete(X_extents, X_max_idx)
    ratio = X_max_val / (X_others.mean() + 1e-8)
    
    v_max_idx = int(np.argmax(np.abs(v_hat)))
    alignment = (X_max_idx == v_max_idx)
    
    # Entropy
    p_mu = X_extents / (X_extents.sum() + 1e-10)
    entropy = -np.sum(p_mu * np.log(p_mu + 1e-10))
    max_entropy = np.log(D)
    
    return {
        'ratio': float(ratio),
        'alignment': bool(alignment),
        'entropy_norm': float(entropy / max_entropy),
        'X_max_idx': X_max_idx,
        'v_max_idx': v_max_idx
    }
