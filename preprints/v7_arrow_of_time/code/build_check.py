"""Build check for the v7 manuscript. Run after `python build_tex.py`.

Exit code 0 iff all regression checks pass. Detects the four classes
found in the second audit:
  (1) dot-leftover in promoted headings (e.g. section{. Introduction)
  (2) bare label{abstract} leaking into the abstract body
  (3) pandoc {[}/{]} guards still around converted citations
      (double brackets [[1]] in the PDF, since \\cite adds its own)
  (4) double manual numbers in headings after promotion
"""
import re
import sys

tex = open("manuscript_v7.tex", encoding="utf-8").read()

checks = [
    ("dot-leading section",      r"\\section\{\. "),
    ("dot-leading subsection",   r"\\subsection\{\. "),
    ("double-num subsection{1 The",         r"\\subsection\{1 The"),
    ("double-num subsection{2 Growth",      r"\\subsection\{2 Growth"),
    ("double-num subsection{1 Equilibrium", r"\\subsection\{1 Equilibrium"),
    ("bare label{abstract}",     r"(?<!\\)label\{abstract\}"),
    ("guarded bracket before cite",   r"\{\[\} ?\\cite"),
    ("guarded bracket after cite",    r"\\cite[^\{]*\{\]\}"),
    ("citation wrapped in []",         r"\[ ?\\cite|\\cite[^\{]*\] ?\}"),
]
clean = True
for name, pat in checks:
    hits = len(re.findall(pat, tex))
    if hits:
        clean = False
        print(f"FOUND {hits:2d}  {name}")
        for m in re.finditer(pat, tex):
            print("   ", tex[max(0, m.start() - 40):m.end() + 20].replace("\n", " ")[:110])
    else:
        print(f"ok      {name}")

bad_heads = re.findall(r"\\(?:sub)*section\{\d", tex)
if bad_heads:
    clean = False
    print("FOUND %2d  numbered headings not stripped" % len(bad_heads))
    for h in bad_heads[:6]:
        print("   ", h)

print("CLEAN" if clean else "NEEDS FIX")
sys.exit(0 if clean else 1)
