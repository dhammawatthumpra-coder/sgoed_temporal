"""Verify the user's audit claims: v6 lambda ratio, v7 SOC/curvature words."""
import os
import re

v6m = open("preprints/v6_condensation/manuscript_v6.md", encoding="utf-8").read()
v7m = open("preprints/v7_arrow_of_time/manuscript_v7.md", encoding="utf-8").read()

print("== v6 md: '≈20' / '≈23' occurrences ==")
for pat in [r"\\approx\s*2[03]", r"\\\\approx 2[03]"]:
    for m in re.finditer(pat, v6m):
        i = max(0, m.start() - 70)
        print("  ctx:", re.sub(r"\s+", " ", v6m[i:m.end() + 40])[:130])
print("== v7 md word counts ==")
for w in ["SOC", "curvature", "self-tuning", "feedback", "c_eff", "ceff", "sgoed_matrix_v15"]:
    print(f"  {w}: {len(re.findall(w, v7m))}")

print("== scripts in v7 preprint code/ matching soc/ceff ==")
for fn in os.listdir("preprints/v7_arrow_of_time/code"):
    if "soc" in fn.lower() or "ceff" in fn.lower():
        print("  ", fn)

if os.path.exists("matrix/audit_v7_eigenvalue_results.json"):
    ev = open("matrix/audit_v7_eigenvalue_results.json", encoding="utf-8").read()
    print("== eigenvalue json present; snippet ==")
    print(ev[:300])
else:
    print("no matrix/audit_v7_eigenvalue_results.json")

print("== v6 md §4.6 area (lambda_max wording) ==")
i = v6m.find("lambda_")
if i != -1:
    print(re.sub(r"\s+", " ", v6m[max(0, i - 120):i + 160]))