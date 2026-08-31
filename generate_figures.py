"""
SGOED v5: Figure Generator
Reads data/sgoed_v5_results.json and generates publication-quality plots.
"""
import os
import json
import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = "data"
FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)

# Load data
with open(os.path.join(DATA_DIR, "sgoed_v5_results.json"), 'r') as f:
    data = json.load(f)

plt.style.use('seaborn-v0_8-whitegrid')

# ==========================================
# Figure 1: Phase Diagram (Observer Dimension)
# ==========================================
fig, ax = plt.subplots(figsize=(8, 6))
ds = sorted([int(k) for k in data['phase_diagram'].keys()])
means = [data['phase_diagram'][str(d)]['mean'] for d in ds]
stds = [data['phase_diagram'][str(d)]['std'] for d in ds]
aligns = [data['phase_diagram'][str(d)]['align_rate']*100 for d in ds]

bars = ax.bar(ds, means, yerr=stds, capsize=8, color='steelblue', edgecolor='black', linewidth=1.2)
ax.axhline(1.5, color='green', ls='--', lw=2, label='Emergence Threshold (1.5)')
ax.axhline(10.0, color='orange', ls='--', lw=2, label='Explosion Threshold (10.0)')

# Add alignment labels
for i, (d, m, a) in enumerate(zip(ds, means, aligns)):
    ax.text(d, m + stds[i] + 0.3, f"Align: {a:.0f}%", ha='center', fontsize=10, fontweight='bold')

ax.set_xlabel('Observer Dimension $d$', fontsize=14)
ax.set_ylabel('Temporal/Spatial Ratio', fontsize=14)
ax.set_title('Phase Diagram by Observer Complexity ($N=6, g_{XY}=0.8$)', fontsize=16)
ax.set_xticks(ds)
ax.legend(fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig1_phase_diagram.png"), dpi=300)
plt.savefig(os.path.join(FIG_DIR, "fig1_phase_diagram.pdf"), dpi=300)
plt.close()
print("✅ Saved fig1_phase_diagram")

# ==========================================
# Figure 2: Finite-Size Scaling (Fixed g=0.8)
# ==========================================
fig, ax = plt.subplots(figsize=(8, 6))
Ns = sorted([int(k) for k in data['fss_fixed'].keys()])
means_fss = [data['fss_fixed'][str(N)]['mean'] for N in Ns]
stds_fss = [data['fss_fixed'][str(N)]['std'] for N in Ns]

ax.plot(Ns, means_fss, 'o-', color='crimson', linewidth=2, markersize=10, label='Mean Ratio')
ax.fill_between(Ns, 
                [m - s for m, s in zip(means_fss, stds_fss)], 
                [m + s for m, s in zip(means_fss, stds_fss)], 
                color='crimson', alpha=0.2, label='±1 Std Dev')
ax.axhline(1.5, color='green', ls='--', lw=2, label='Emergence (1.5)')

# Highlight the crossover
ax.axvspan(6.5, 8.5, color='yellow', alpha=0.2, label='Crossover Regime')

ax.set_xlabel('System Size $N$', fontsize=14)
ax.set_ylabel('Temporal/Spatial Ratio', fontsize=14)
ax.set_title('Finite-Size Scaling at Fixed Coupling ($d=3, g_{XY}=0.8$)', fontsize=16)
ax.set_xticks(Ns)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig2_fss_fixed.png"), dpi=300)
plt.savefig(os.path.join(FIG_DIR, "fig2_fss_fixed.pdf"), dpi=300)
plt.close()
print("✅ Saved fig2_fss_fixed")

# ==========================================
# Figure 3: N=8 Parameter Tuning
# ==========================================
fig, ax = plt.subplots(figsize=(8, 6))
gs = sorted([float(k) for k in data['n8_tuning'].keys()])
means_tune = [data['n8_tuning'][str(g)]['mean'] for g in gs]
stds_tune = [data['n8_tuning'][str(g)]['std'] for g in gs]
cvs_tune = [data['n8_tuning'][str(g)]['cv'] for g in gs]

# Dual axis for Ratio and CV
ax1 = ax
ax2 = ax1.twinx()

ax1.plot(gs, means_tune, 'o-', color='navy', linewidth=2, markersize=10, label='Mean Ratio')
ax1.fill_between(gs, 
                 [m - s for m, s in zip(means_tune, stds_tune)], 
                 [m + s for m, s in zip(means_tune, stds_tune)], 
                 color='navy', alpha=0.2)
                 
ax2.plot(gs, cvs_tune, 's--', color='darkorange', linewidth=2, markersize=8, label='CV (%)')

ax1.axhline(1.5, color='green', ls='--', lw=1.5, alpha=0.7)
ax1.axhline(10.0, color='orange', ls='--', lw=1.5, alpha=0.7)

ax1.set_xlabel('Coupling Strength $g_{XY}$', fontsize=14)
ax1.set_ylabel('Mean Ratio', fontsize=14, color='navy')
ax2.set_ylabel('Coefficient of Variation (%)', fontsize=14, color='darkorange')
ax1.set_title('Parameter Tuning at $N=8$ ($d=3$)', fontsize=16)

# Combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig3_n8_tuning.png"), dpi=300)
plt.savefig(os.path.join(FIG_DIR, "fig3_n8_tuning.pdf"), dpi=300)
plt.close()
print("✅ Saved fig3_n8_tuning")

print("\n🎉 All figures generated successfully in the 'figures/' directory!")
