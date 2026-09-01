"""Rebuild manuscript_v6.md FROM manuscript_v6.tex (tex is authoritative)."""
import re

# ---- inputs ----
body = open("_v6_body_raw.md", encoding="utf-8").read()       # pandoc tex->md, no citeproc
std = open("_v6_standalone.md", encoding="utf-8").read()      # for YAML abstract
tex = open("manuscript_v6.tex", encoding="utf-8").read()
bib = open("references.bib", encoding="utf-8").read()

# ---- 1. abstract from YAML (stop at the first unindented field) ----
suffix = std.split("abstract: |", 1)[1]
_lines = []
for line in suffix.splitlines():
    if line.startswith("  "):
        _lines.append(line[2:])
    elif not line.strip():
        continue                 # blank line inside the block scalar
    else:
        break                    # first unindented YAML field ends the block
abstract = "\n".join(_lines).strip()

# ---- 2. strip pandoc heading ids, renumber headings ----
body = re.sub(r"\s*\{#sec:[^}]*\}", "", body)
body = re.sub(r"\s*\{#[^}]*\}", "", body)
lines = body.splitlines()
out = []
sec = 0
sub = 0
for ln in lines:
    m = re.match(r"^(#+)\s+(.*)$", ln)
    if m:
        lvl, title = len(m.group(1)), m.group(2)
        if lvl == 1:
            sec += 1
            sub = 0
            out.append(f"## {sec}. {title}")
        else:
            sub += 1
            out.append(f"### {sec}.{sub} {title}")
    else:
        out.append(ln)
body = "\n".join(out)

# ---- 3. citations: collect order, replace [@k; @k2] -> [n, n2] ----
order = []
for grp in re.findall(r"\[@([^\]]+)\]", body):
    for k in grp.split(";"):
        k = k.strip().lstrip("@")      # second/multi @ survives [^]]+ capture
        if k not in order:
            order.append(k)
for grp in set(re.findall(r"\[@([^\]]+)\]", body)):
    nums = [order.index(k.strip().lstrip("@")) + 1 for k in grp.split(";")]
    body = body.replace(f"[@{grp}]", "[" + ", ".join(str(n) for n in nums) + "]", 1)

# ---- 4. references section formatted from references.bib ----
def bib_fields(entry):
    f = {}
    for m in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}", entry, re.S):
        f[m.group(1)] = " ".join(m.group(2).split())
    return f

entries = {}
for part in bib.split("@")[1:]:
    m = re.match(r"(\w+)\s*\{\s*([\w_:]+),\s*", part, re.S)
    if not m:
        continue
    key = m.group(2)
    f = {}
    for fm in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}", part[m.end():], re.S):
        f[fm.group(1)] = " ".join(fm.group(2).split())
    entries[key] = f

def fmt_authors(s):
    names = [x.strip() for x in s.split(" and ")]
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " & " + names[-1]

refs = []
for i, k in enumerate(order, 1):
    f = entries.get(k, {})
    authors = fmt_authors(f.get("author", f.get("editor", "Unknown")))
    year = f.get("year", "n.d.")
    title = f.get("title", k)
    journal = f.get("journal") or f.get("booktitle") or f.get("publisher") or f.get("howpublished", "")
    vol = f.get("volume", "")
    pages = f.get("pages", "")
    doi = f.get("doi", "")
    loc = []
    if journal:
        loc.append(f"*{journal}*")
    if vol:
        loc.append(vol + (f"({f.get('number')})" if f.get("number") else ""))
    if pages:
        loc.append(pages)
    line = f"[{i}] {authors} ({year}). {title}."
    if loc:
        line += " " + ", ".join(loc) + "."
    if doi:
        line += f" [doi:{doi}](https://doi.org/{doi})"
    refs.append(line)

# ---- 5. assemble ----
front = """# Temporal Emergence from Dynamical Observer Coupling: A Matrix Model for Observer-Dependent Symmetry Breaking
**Version 6: Trajectory-Mean Analysis with Corrected Sampler**

**Author:** Sutipong Chanpengpad  
*Independent Researcher, Chiang Rai, Thailand*  
Email: `dhammawatthumpra@gmail.com`  
ORCID: [0009-0001-4069-8576](https://orcid.org/0009-0001-4069-8576)

**Date:** September 2026

---

## Abstract

{abstract}

---

## Table of Contents
"""

toc = []
for ln in body.splitlines():
    m = re.match(r"^## (.*)$", ln)
    if m:
        title = m.group(1)
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        toc.append(f"- [{title}](#{slug})")
toc = "\n".join(toc)

md = (front.format(abstract=abstract) + toc + "\n\n---\n\n"
      + body + "\n---\n\n## References\n\n" + "\n\n".join(refs) + "\n")
md = "<!-- generated from manuscript_v6.tex (" + tex.split("Version 6:")[1].splitlines()[0].strip() if False else md
md = "<!-- regenerated from manuscript_v6.tex on 2026-09-01 — edit the .tex, then rebuild -->\n\n" + md

with open("manuscript_v6.md", "w", encoding="utf-8") as f:
    f.write(md)
print("manuscript_v6.md rebuilt:", len(md.splitlines()), "lines,", len(refs), "references")