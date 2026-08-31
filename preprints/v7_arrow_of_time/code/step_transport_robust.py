"""
SGOED handoff TODO #1 — Non-equilibrium flow robustness audit
=============================================================
Confirm the tuned upwind transport at: 8 seeds x 500 steps, plus
g_trans x g_sink scan, plus null and reversal re-checks.
Questions: is the 4000x decay deterministic? Is strict monotonicity
only broken at the thermal floor (per-seed stats)? Does J_net follow
the pump sign symmetrically?
"""
import json
import sys
import numpy as np
sys.path.insert(0, ".")
from step_langevin_transport_tuned import run_transport_tuned

DEFAULT = dict(M=6, N=4, g_xy=0.8, g_trans=1.2, g_drive=5.0, g_bulk=0.1,
               g_sink=3.0, alpha=0.1, E_max=30.0, lam_g=5.0, dt=0.005,
               T=0.02)
out = {}


def run_batch(n_steps, seeds, reverse=False, **kw):
    ps, Js, als = [], [], []
    for s in seeds:
        E, al, J = run_transport_tuned(**{**DEFAULT, **kw}, n_steps=n_steps,
                                       seed=s, reverse=reverse)
        ps.append(E)
        Js.append(J)
        als.append(al)
    return np.array(ps), np.array(Js), np.array(als)


# 1) default params: 8 seeds x 500 steps
ps, Js, als = run_batch(500, range(42, 50))
Em = ps.mean(axis=0)
mono_ok = sum(1 for p in ps if all(p[u] > p[u + 1] for u in range(5)))
print(f"[A default 8x500] E={np.round(Em, 4)} decay={Em[0]/Em[5]:.0f}x "
      f"J={np.mean(Js):+.3f}±{np.std(Js):.3f} strict_mono={mono_ok}/8 "
      f"E3/E4={np.mean(ps[:, 3]):.3f}/{np.mean(ps[:, 4]):.3f}")
out["A_default"] = {"E": Em.tolist(), "decay": float(Em[0] / Em[5]),
                    "J_mean": float(np.mean(Js)), "J_std": float(np.std(Js)),
                    "strict_mono": mono_ok,
                    "E3_E4": [float(np.mean(ps[:, 3])), float(np.mean(ps[:, 4]))]}

# 2) reversal: pump at the other end
ps, Js, als = run_batch(500, range(42, 47), reverse=True)
Em_r = ps.mean(axis=0)
print(f"[B REVERSED 6x500] E={np.round(Em_r, 4)} "
      f"J={np.mean(Js):+.3f}±{np.std(Js):.3f}")
out["B_reversed"] = {"E": Em_r.tolist(), "J_mean": float(np.mean(Js)),
                     "J_std": float(np.std(Js))}

# 3) null (no pump)
ps, Js, als = run_batch(300, range(42, 46), g_drive=0.0)
print(f"[C NULL 4x300] E={np.round(ps.mean(axis=0), 4)} "
      f"J={np.mean(Js):+.3f}±{np.std(Js):.3f}")
out["C_null"] = {"E": ps.mean(axis=0).tolist(), "J_mean": float(np.mean(Js)),
                 "J_std": float(np.std(Js))}

# 4) g_trans x g_sink scan (2 seeds x 300 steps)
print("[D scan g_trans x g_sink] decay E0/E5:")
scan = {}
for gt in [0.8, 1.2, 1.6]:
    for gs in [2.0, 3.0, 4.0]:
        ps, Js, _ = run_batch(300, range(42, 44), g_trans=gt, g_sink=gs)
        Emx = ps.mean(axis=0)
        d = Emx[0] / Emx[5]
        print(f"   gt={gt} gs={gs}: decay={d:8.1f}x J={np.mean(Js):+.3f} E={np.round(Emx, 3)}")
        scan[f"{gt}/{gs}"] = {"decay": float(d), "J": float(np.mean(Js)),
                              "E": Emx.tolist()}
out["D_scan"] = scan

with open(r"F:\_Ai\sgoed\V5\matrix\step_transport_robust_results.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nsaved -> step_transport_robust_results.json")