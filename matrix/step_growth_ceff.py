"""
SGOED — c_eff[R] curvature-driven geometric feedback (blueprint ②)
===================================================================
Make the light speed a DYNAMIC variable responding to local causal
density (Alexandrov/interval volume as the Ricci curvature proxy),
instead of an external constant.

Geometry: 3-torus walk (d_sp=3, sigma=2.0) with matrix-encoded distance
(fixed stochastic geometry; N only refines the sampling of t in [0,T]).

Interval proxy (computable in closed form): for the PROBE cone at c=c0,
I(u,k) = #{w : u<w<k, probe(u,w) & probe(w,k)} = (P @ P)[u,k] with P the
probe relation matrix (flat cone -> transitive, so 2-step paths ARE the
intervals). Per-node birth density dens[k] = mean_{u<k} I(u,k).

Feedback rules (per node k, set at birth, sequential in time):
  A (gravitational dilution): c_eff(k) = c0 / (1 + beta * dens[k]/I_0)
  B (dimensional homeostasis): c_eff(k) = c0 * exp(-kappa * (dens[k]/I_t - 1))
  Control:                       c_eff(k) = c0

Links: (u,k) related iff dist2(u,k) <= (c_eff(k)*dt)^2 (per-k cone);
measured rho on the TRANSITIVE CLOSURE (per-k cones need not be transitive).

Gates (as specified):
  Gate 1: std_across N in {250,500,1000} x 10 seeds <= 0.05 PASS.
  Gate 2: c_eff converges to a steady distribution (report mean/std/min,
          no collapse to 0, no chaotic oscillation).
  Gate 3: record the self-tuned d_MM honestly.
"""
import json
import sys
import numpy as np
sys.path.insert(0, ".")
from step_causal_set_scale_study import calibration, read_dim
from step_growth_soc import closure_rho

Ns = [250, 500, 1000]
SEEDS = range(42, 52)


def geometry(N, seed, d_sp=3, sigma=2.0, T=10.0, L=10.0, Nm=5, n_grid=2000):
    rng = np.random.RandomState(seed)
    dt_ = T / (n_grid - 1)
    walk = np.cumsum(rng.normal(0.0, sigma * np.sqrt(dt_), (n_grid, d_sp)), axis=0) % L
    idx = np.round(np.linspace(0, n_grid - 1, N)).astype(int)
    s = walk[idx]                                   # (N, d_sp)
    w = 2.0 * np.pi / L
    Xf = np.zeros((N, d_sp * Nm * Nm))
    for a in range(d_sp):
        A = rng.randn(Nm, Nm) * 0.5
        B = rng.randn(Nm, Nm) * 0.5
        A = (A + A.T) / 2
        B = (B + B.T) / 2
        ca, sa = np.cos(w * s[:, a]), np.sin(w * s[:, a])
        Xf[:, a * Nm * Nm:(a + 1) * Nm * Nm] = np.einsum("n,ij->nij", ca, A).reshape(N, -1) \
            + np.einsum("n,ij->nij", sa, B).reshape(N, -1)
    G = Xf @ Xf.T
    n2 = np.einsum("ii->i", G)
    dist2 = (n2[:, None] + n2[None, :] - 2.0 * G) / (d_sp * Nm)
    t = np.linspace(0.0, T, N)
    dt = t[:, None] - t[None, :]
    return dist2, dt


def run_ceff(N, seed, c0, rule, param, I_0=1.0):
    dist2, dt = geometry(N, seed)
    probe = (dist2 <= (c0 * dt) ** 2).astype(np.int64)
    np.fill_diagonal(probe, 0)
    Ipairs = probe @ probe                          # (N,N): interval counts at probed cone
    dens = np.array([np.mean(Ipairs[:k, k]) for k in range(N)])
    dens_n = dens / (dens.mean() + 1e-9)     # per-volume density proxy (scale-free)
    if rule == "control":
        c_eff = np.full(N, c0)
    elif rule == "A":
        c_eff = c0 / (1.0 + param * dens / I_0)
    elif rule == "A2":
        c_eff = c0 / (1.0 + param * dens_n)
    elif rule == "B":
        c_eff = c0 * np.exp(-1.0 * (dens / param - 1.0))
    else:  # B2
        c_eff = c0 * np.exp(-param * (dens_n - 1.0))
    # links with per-k cone
    children = [[] for _ in range(N)]
    for k in range(1, N):
        hit = dist2[:k, k] <= (c_eff[k] * dt[:k, k]) ** 2
        for u in np.nonzero(hit)[0]:
            children[k].append(int(u))
    rho = closure_rho(N, children)
    return rho, c_eff


def audit(name, rule, param, c0=0.15):
    rows = {}
    ceff_stat = []
    for N in Ns:
        ds, rhos = calibration(N, seeds=8)
        dims = []
        for s in SEEDS:
            rho, c_eff = run_ceff(N, s, c0, rule, param)
            dims.append(read_dim(rho, ds, rhos))
            if N == 1000:
                late = c_eff[N // 2:]
                ceff_stat.append([float(late.mean()), float(late.std()), float(late.min())])
        rows[str(N)] = [float(np.mean(dims)), float(np.std(dims))]
    means = [rows[str(N)][0] for N in Ns]
    std_acr = float(np.std(means))
    verdict = "PASS" if std_acr <= 0.05 else ("FAIL" if std_acr > 0.10 else "BORDERLINE")
    if ceff_stat:
        cm = np.mean([c[0] for c in ceff_stat])
        cs = np.mean([c[1] for c in ceff_stat])
        cmin = min(c[2] for c in ceff_stat)
        g2 = f"c_eff mean={cm:.3f} std={cs:.3f} min={cmin:.3f}"
    else:
        g2 = "c_eff n/a"
    print(f"[{name:24s}] d={means[0]:.2f}/{means[1]:.2f}/{means[2]:.2f} "
          f"std_acr={std_acr:.3f} {g2} -> {verdict}")
    return {"d": {str(N): rows[str(N)] for N in Ns}, "std_across_N": std_acr,
            "verdict": verdict, "c_eff1000": {"mean": cm, "std": cs, "min": cmin}
            if ceff_stat else None}


if __name__ == "__main__":
    out = {}
    print("control (static c0=0.15)")
    out["control_c015"] = audit("control c0=.15", "control", None, c0=0.15)
    print("\nA gravitational dilution: c_eff = c0/(1+beta*dens)")
    for b in [0.5, 2.0, 5.0]:
        out[f"A_beta{b}"] = audit(f"A beta={b}", "A", b, c0=0.15)
    out["A_beta2_c025"] = audit("A beta=2 c0=.25", "A", 2.0, c0=0.25)
    print("\nA2 (density-normalized): c_eff = c0/(1+beta*dens_n)")
    for b in [0.5, 2.0, 5.0]:
        out[f"A2_beta{b}"] = audit(f"A2 beta={b}", "A2", b, c0=0.15)
    print("\nB homeostasis: c_eff = c0*exp(-(dens/I_t - 1))")
    for kt in [1.0, 2.0]:
        out[f"B_It{kt}"] = audit(f"B I_t={kt}", "B", kt, c0=0.15)
    print("\nB2 (density-normalized): c_eff = c0*exp(-kappa*(dens_n-1))")
    for ka in [0.5, 2.0]:
        out[f"B2_kappa{ka}"] = audit(f"B2 kappa={ka}", "B2", ka, c0=0.15)
    with open(r"F:\_Ai\sgoed\V5\matrix\step_growth_ceff_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nsaved -> step_growth_ceff_results.json")