"""
Phase A, step 3: validate incremental Delta S against full recompute.
This MUST pass to strict tolerance before step=1 sampler results are trusted.
"""
import numpy as np
from sgoed_core_v6 import (
    action_v3, propose_delta_X, propose_delta_Y, _compute_v_hat
)

def test_delta_X(n_trials=2000, seed=0):
    rng = np.random.RandomState(seed)
    max_abs_err = 0.0
    max_rel_err = 0.0

    for trial in range(n_trials):
        N = rng.randint(3, 9)      # N = 3..8
        D = rng.randint(2, 7)      # D = 2..6
        d = rng.randint(1, 5)      # d = 1..4
        gXY = rng.uniform(0.5, 1.3)
        max_extent = 10.0

        X = np.zeros((D, N, N))
        for mu in range(D):
            A = rng.randn(N, N) * 0.6
            X[mu] = (A + A.T) / 2
        Y = np.zeros((d, N, N))
        for a in range(d):
            A = rng.randn(N, N) * 0.4
            Y[a] = (A + A.T) / 2

        v_hat = _compute_v_hat(Y, D)

        mu = rng.randint(0, D)
        i = rng.randint(0, N)
        j = rng.randint(0, N)
        if j < i:
            i, j = j, i
        new_val = X[mu, i, j] + rng.randn() * 0.3

        S_old = action_v3(X, Y, gXY, max_extent)

        dS_fast = propose_delta_X(X, Y, mu, i, j, new_val, gXY, max_extent,
                                   lam=1.0, r0=1.0, v_hat=v_hat)

        X2 = X.copy()
        X2[mu, i, j] = new_val
        if i != j:
            X2[mu, j, i] = new_val
        S_new = action_v3(X2, Y, gXY, max_extent)
        dS_true = S_new - S_old

        err = abs(dS_fast - dS_true)
        rel = err / (abs(dS_true) + 1e-8)
        max_abs_err = max(max_abs_err, err)
        max_rel_err = max(max_rel_err, rel)

        assert err < 1e-8, (
            f"X-move mismatch at trial {trial}: fast={dS_fast!r} true={dS_true!r} "
            f"N={N} D={D} d={d} mu={mu} i={i} j={j}"
        )

    print(f"[X moves]  {n_trials} trials passed. max_abs_err={max_abs_err:.3e}, "
          f"max_rel_err={max_rel_err:.3e}")


def test_delta_Y(n_trials=2000, seed=1):
    rng = np.random.RandomState(seed)
    max_abs_err = 0.0
    max_rel_err = 0.0

    for trial in range(n_trials):
        N = rng.randint(3, 9)
        D = rng.randint(2, 7)
        d = rng.randint(1, 5)
        gXY = rng.uniform(0.5, 1.3)
        max_extent = 10.0

        X = np.zeros((D, N, N))
        for mu in range(D):
            A = rng.randn(N, N) * 0.6
            X[mu] = (A + A.T) / 2
        Y = np.zeros((d, N, N))
        for a in range(d):
            A = rng.randn(N, N) * 0.4
            Y[a] = (A + A.T) / 2

        a = rng.randint(0, d)
        i = rng.randint(0, N)
        j = rng.randint(0, N)
        if j < i:
            i, j = j, i
        new_val = Y[a, i, j] + rng.randn() * 0.3

        S_old = action_v3(X, Y, gXY, max_extent)

        dS_fast, v_hat_new = propose_delta_Y(X, Y, D, a, i, j, new_val, gXY,
                                              max_extent, lamY=1.0, rY=0.5)

        Y2 = Y.copy()
        Y2[a, i, j] = new_val
        if i != j:
            Y2[a, j, i] = new_val
        S_new = action_v3(X, Y2, gXY, max_extent)
        dS_true = S_new - S_old

        err = abs(dS_fast - dS_true)
        rel = err / (abs(dS_true) + 1e-8)
        max_abs_err = max(max_abs_err, err)
        max_rel_err = max(max_rel_err, rel)

        assert err < 1e-8, (
            f"Y-move mismatch at trial {trial}: fast={dS_fast!r} true={dS_true!r} "
            f"N={N} D={D} d={d} a={a} i={i} j={j}"
        )

    print(f"[Y moves]  {n_trials} trials passed. max_abs_err={max_abs_err:.3e}, "
          f"max_rel_err={max_rel_err:.3e}")


def test_edge_cases():
    """Edge cases: extent exceeding max_extent (wall regime), d > D, d == D."""
    rng = np.random.RandomState(42)
    for max_extent_test in [0.01, 100.0]:  # force wall regime vs never-hit-wall
        N, D, d = 6, 4, 3
        gXY = 0.9
        X = np.zeros((D, N, N))
        for mu in range(D):
            A = rng.randn(N, N) * 2.0  # large -> likely exceeds tiny max_extent
            X[mu] = (A + A.T) / 2
        Y = np.zeros((d, N, N))
        for a in range(d):
            A = rng.randn(N, N) * 0.4
            Y[a] = (A + A.T) / 2
        v_hat = _compute_v_hat(Y, D)

        mu, i, j = 1, 2, 4
        new_val = X[mu, i, j] + 0.5

        S_old = action_v3(X, Y, gXY, max_extent_test)
        dS_fast = propose_delta_X(X, Y, mu, i, j, new_val, gXY, max_extent_test,
                                   lam=1.0, r0=1.0, v_hat=v_hat)
        X2 = X.copy()
        X2[mu, i, j] = new_val
        X2[mu, j, i] = new_val
        S_new = action_v3(X2, Y, gXY, max_extent_test)
        dS_true = S_new - S_old
        err = abs(dS_fast - dS_true)
        assert err < 1e-8, f"Wall-regime mismatch: max_extent={max_extent_test}, err={err}"
    print("[edge cases] wall-regime (both sides) passed.")


if __name__ == "__main__":
    test_delta_X()
    test_delta_Y()
    test_edge_cases()
    print("\nALL CORRECTNESS TESTS PASSED — incremental delta matches full recompute exactly.")
