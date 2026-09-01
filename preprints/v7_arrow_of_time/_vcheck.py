import re

tex = open("manuscript_v7.tex", encoding="utf-8").read()
checks = {
    "double-num 'subsection{1 The'":      r"\\subsection\{1 The",
    "double-num 'subsection{2 Growth'":   r"\\subsection\{2 Growth",
    "double-num 'subsection{1 Equilibrium'": r"\\subsection\{1 Equilibrium",
    "bare label{abstract}":                r"(?<!\\)label\{abstract\}",
    "guarded brackets {[}\\cite":          r"\{\[?\}\\cite|\\cite[^\n]*\{\]\}",
}
clean = True
for name, pat in checks.items():
    hits = len(re.findall(pat, tex))
    if hits:
        clean = False
        print(f"FOUND {hits:2d}  {name}")
        for m in re.finditer(pat, tex):
            print("   ", tex[max(0, m.start()-40):m.end()+20].replace("\n", " ")[:110])
    else:
        print(f"ok      {name}")
print("CLEAN" if clean else "NEEDS FIX")
# check headings look right now (sample)
for m in re.finditer(r"\\subsection\{[^}]{0,40}\}", tex):
    s = m.group(0)
    if "matrix unit" in s or "Equilibrium" in s or "Growth" in s:
        print("  heading:", s)