"""
v12 sink-hub mechanism analysis (self-written, data honesty).
Q: why is the hub a SINK (in >> out), not a source?
Tests:
  1. SVD of real W (mode 4): is the hub the target (|v1| max) or the source
     (|u1| max) of the dominant singular mode? sigma1 contribution.
  2. Mode comparison (1=baseline, 2=quartic only, 3=relational, 4=global):
     does the sink-hub arise from coupling alone (mode 2) or condensation (mode 4)?
  3. Row vs col norm of hub + who feeds it.
"""
import numpy as np
from audit_v12_ablation import run_ablation_simulation, evaluate_invariants


def analyze(W, d=3):
    N = W.shape[0]
    out = W.sum(1)
    inn = W.sum(0)
    imb = out - inn
    hub = int(np.argmax(np.abs(imb)))
    U, s, Vt = np.linalg.svd(W)
    u1, v1 = U[:, 0], Vt[0]
    u1h = abs(u1[hub])
    v1h = abs(v1[hub])
    # where is |u1| and |v1| max?
    u1max = int(np.argmax(np.abs(u1)))
    v1max = int(np.argmax(np.abs(v1)))
    # dominant mode reconstruction at hub
    contrib = s[0] * u1[hub] * v1  # W[hub, :] from rank-1 part
    row_norm_h = np.linalg.norm(W[hub])
    col_norm_h = np.linalg.norm(W[:, hub])
    # who feeds the hub (top incoming)
    top_in = np.argsort(W[:, hub])[::-1][:5]
    top_out = np.argsort(W[hub])[::-1][:5]
    return {
        "hub": hub, "hub_imb": imb[hub], "S": (out > inn).sum(),
        "sigma1/sigma2": s[0] / s[1], "sigma1": s[0],
        "|u1[hub]|": u1h, "|v1[hub]|": v1h,
        "u1max_node": u1max, "v1max_node": v1max,
        "row_norm_hub": row_norm_h, "col_norm_hub": col_norm_h,
        "top_in": top_in.tolist(), "top_out": top_out.tolist(),
    }


print("=" * 80)
print(" 1. MODE COMPARISON (N=32, 5 seeds): where does sink-hub come from?")
print("=" * 80)
for mode, name in [(1, "baseline"), (2, "quartic only"), (3, "relational"), (4, "global SVD")]:
    droots, hub_sinks, specs = [], [], []
    for s in [42, 43, 44, 45, 46]:
        W = run_ablation_simulation(mode=mode, N=32, d=3, seed=s)
        D, spec, align = evaluate_invariants(W, d=3)
        a = analyze(W)
        # D_root from hub
        Dr = 0.0
        for j in range(32):
            if j == a["hub"]:
                continue
            f = W[a["hub"], j] - W[j, a["hub"]]
            if abs(f) > 1e-4:
                Dr += np.sign(f)
        Dr /= 31
        droots.append(Dr)
        hub_sinks.append(a["hub_imb"])
        specs.append(spec)
    print(f"  mode {mode} [{name:12s}]: D_root={np.mean(droots):+.2f} +/- {np.std(droots):.2f} | "
          f"hub_imb={np.mean(hub_sinks):+6.1f} | spec={np.mean(specs):.2f}")

print()
print("=" * 80)
print(" 2. SVD DETAIL (mode 4, N=32, seed 42): hub = source (u1) or target (v1)?")
print("=" * 80)
W = run_ablation_simulation(mode=4, N=32, d=3, seed=42)
a = analyze(W)
print(f"  hub = node {a['hub']}  (imb = {a['hub_imb']:+.1f})")
print(f"  sigma1 = {a['sigma1']:.2f}, sigma1/sigma2 = {a['sigma1/sigma2']:.2f}")
print(f"  |u1[hub]| = {a['|u1[hub]|']:.3f}  (u1max at node {a['u1max_node']})")
print(f"  |v1[hub]| = {a['|v1[hub]|']:.3f}  (v1max at node {a['v1max_node']})")
print(f"  hub row-norm (out) = {a['row_norm_hub']:.2f} | col-norm (in) = {a['col_norm_hub']:.2f}")
print(f"  top incoming to hub: {a['top_in']}")
print(f"  top outgoing from hub: {a['top_out']}")
print(f"  fraction of nodes with W[:,hub] > W[hub,:] (hub receives more): "
      f"{np.mean([W[j, a['hub']] > W[a['hub'], j] for j in range(32) if j != a['hub']]):.2f}")
