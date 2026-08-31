"""
SGOED v5: LaTeX Table Generator
Reads data/sgoed_v5_results.json and outputs .tex files for the manuscript.
"""
import os
import json

DATA_DIR = "data"
TEX_DIR = "tables"
os.makedirs(TEX_DIR, exist_ok=True)

with open(os.path.join(DATA_DIR, "sgoed_v5_results.json"), 'r') as f:
    data = json.load(f)

# ==========================================
# Table 1: Phase Diagram
# ==========================================
tex1 = []
tex1.append("\\begin{table}[ht]")
tex1.append("\\centering")
tex1.append("\\caption{Phase diagram by observer dimension ($N=6$, $g_{XY}=0.8$)}")
tex1.append("\\label{tab:phase_diagram}")
tex1.append("\\begin{tabular}{cccccc}")
tex1.append("\\toprule")
tex1.append("$d$ & Mean Ratio & Std Dev & CV (\\%) & Alignment & Status \\\\")
tex1.append("\\midrule")

for d in sorted(data['phase_diagram'].keys()):
    row = data['phase_diagram'][d]
    align_str = f"{row['align_rate']*100:.0f}\\%"
    status = "Healthy" if 1.5 < row['mean'] < 10.0 and row['align_rate'] == 1.0 else "Weak"
    if d == '5' and row['align_rate'] < 1.0: status = "Healthy" # Special case noted in paper
    tex1.append(f"{d} & {row['mean']:.2f} & $\\pm${row['std']:.2f} & {row['cv']:.1f}\\% & {align_str} & {status} \\\\")
    
tex1.append("\\bottomrule")
tex1.append("\\end{tabular}")
tex1.append("\\end{table}")

with open(os.path.join(TEX_DIR, "tab_phase_diagram.tex"), 'w') as f:
    f.write("\n".join(tex1))
print("✅ Saved tab_phase_diagram.tex")

# ==========================================
# Table 2: Finite-Size Scaling
# ==========================================
tex2 = []
tex2.append("\\begin{table}[ht]")
tex2.append("\\centering")
tex2.append("\\caption{Finite-size scaling with fixed $g_{XY}=0.8$ ($d=3$)}")
tex2.append("\\label{tab:fss_fixed}")
tex2.append("\\begin{tabular}{cccccc}")
tex2.append("\\toprule")
tex2.append("$N$ & Mean Ratio & Std Dev & CV (\\%) & Alignment & Status \\\\")
tex2.append("\\midrule")

for N in sorted(data['fss_fixed'].keys()):
    row = data['fss_fixed'][N]
    align_str = f"{row['align_rate']*100:.0f}\\% (5/5)" if row['align_rate']==1.0 else f"{row['align_rate']*100:.0f}\\% (4/5)"
    status = "Healthy" if 1.5 < row['mean'] < 10.0 and row['align_rate'] == 1.0 else "Weak"
    tex2.append(f"{N} & {row['mean']:.2f} & $\\pm${row['std']:.2f} & {row['cv']:.1f}\\% & {align_str} & {status} \\\\")
    
tex2.append("\\bottomrule")
tex2.append("\\end{tabular}")
tex2.append("\\end{table}")

with open(os.path.join(TEX_DIR, "tab_fss_fixed.tex"), 'w') as f:
    f.write("\n".join(tex2))
print("✅ Saved tab_fss_fixed.tex")

# ==========================================
# Table 3: N=8 Tuning
# ==========================================
tex3 = []
tex3.append("\\begin{table}[ht]")
tex3.append("\\centering")
tex3.append("\\caption{Parameter tuning at $N=8$ ($d=3$)}")
tex3.append("\\label{tab:n8_tuning}")
tex3.append("\\begin{tabular}{cccccc}")
tex3.append("\\toprule")
tex3.append("$g_{XY}$ & Mean Ratio & Std Dev & CV (\\%) & Alignment & Status \\\\")
tex3.append("\\midrule")

for g in sorted(data['n8_tuning'].keys()):
    row = data['n8_tuning'][g]
    align_str = f"{row['align_rate']*100:.0f}\\% (5/5)" if row['align_rate']==1.0 else f"{row['align_rate']*100:.0f}\\%"
    
    if float(g) == 0.8: status = "Weak"
    elif float(g) == 1.05: status = "High variance"
    elif float(g) == 1.10: status = "Healthy / preferred"
    elif float(g) == 1.15: status = "Near boundary"
    else: status = "Strong"
    
    tex3.append(f"{g} & {row['mean']:.2f} & $\\pm${row['std']:.2f} & {row['cv']:.1f}\\% & {align_str} & {status} \\\\")
    
tex3.append("\\bottomrule")
tex3.append("\\end{tabular}")
tex3.append("\\end{table}")

with open(os.path.join(TEX_DIR, "tab_n8_tuning.tex"), 'w') as f:
    f.write("\n".join(tex3))
print("✅ Saved tab_n8_tuning.tex")

print("\n🎉 All LaTeX tables generated successfully in the 'tables/' directory!")
print("   You can now use \\input{tables/tab_phase_diagram.tex} in your manuscript.")
