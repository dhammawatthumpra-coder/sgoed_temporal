"""Rebuild manuscript markdown FROM the LaTeX manuscript (tex is master).

Generalised from preprints/v6_condensation/build_md_from_tex.py so both
preprint versions share one flow:

    tmpl -> render_manuscript.py -> .tex (root + preprint)
         -> pdflatex/bibtex       -> .pdf
         -> build_md.py           -> .md (root + preprint)   [this step]
         -> verify_paths.py

Usage:
    python build/build_md.py --version v6
    python build/build_md.py --version v7

For each version this regenerates BOTH the root and the preprint .md from
their own .tex, so the two can never drift.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

VERSIONS = {
    "v6": {
        "dir": "preprints/v6_condensation",
        "title": ("Temporal Emergence from Dynamical Observer Coupling: "
                  "A Matrix Model for Observer-Dependent Symmetry Breaking"),
        "subtitle": "**Version 6: Trajectory-Mean Analysis with Corrected Sampler**",
    },
    "v7": {
        "dir": "preprints/v7_arrow_of_time",
        "title": "The Arrow of Time Is Not in the Ensemble",
        "subtitle": ("## An Audited Toy-Model Quest across Equilibrium Matrices, "
                     "Sequential Growth, and Causal Sets (SGOED V7)"),
    },
}

AUTHOR_BLOCK = """**Author:** Sutipong Chanpengpad  
*Independent Researcher, Chiang Rai, Thailand*  
Email: `dhammawatthumpra@gmail.com`  
ORCID: [0009-0001-4069-8576](https://orcid.org/0009-0001-4069-8576)

**Date:** September 2026"""


def pandoc(src, out, standalone=False):
    cmd = ["pandoc", str(src), "-t", "markdown", "-o", str(out)]
    if standalone:
        cmd.insert(-2, "--standalone")
    subprocess.run(cmd, check=True)
    return Path(out).read_text(encoding="utf-8")


def strip_texttt_renewcommand(tex_path, tmp_tex):
    """The preamble redefines \\texttt (for path hyphenation); pandoc would
    expand that macro into '=\\-' junk instead of reading code spans, so give
    it a copy without the redefinition."""
    s = Path(tex_path).read_text(encoding="utf-8")
    s2 = re.sub(r"\\renewcommand\{\\texttt\}\[1\]\{[^}]*\}", "", s)
    Path(tmp_tex).write_text(s2, encoding="utf-8")
    return tmp_tex


def extract_abstract(std):
    """Abstract from the standalone YAML block scalar."""
    suffix = std.split("abstract: |", 1)[1]
    lines = []
    for line in suffix.splitlines():
        if line.startswith("  "):
            lines.append(line[2:])
        elif not line.strip():
            continue  # blank line inside the block scalar
        else:
            break  # first unindented YAML field ends the block
    return "\n".join(lines).strip()


def renumber_headings(body):
    body = re.sub(r"\s*\{#[^}]*\}", "", body)
    out = []
    sec = 0
    sub = 0
    for ln in body.splitlines():
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
    return "\n".join(out)


def convert_citations(body):
    order = []
    for grp in re.findall(r"\[@([^\]]+)\]", body):
        for k in grp.split(";"):
            k = k.strip().lstrip("@")
            if k and k not in order:
                order.append(k)
    for grp in sorted(set(re.findall(r"\[@([^\]]+)\]", body)),
                      key=lambda g: body.index(g)):
        keys = [k.strip().lstrip("@") for k in grp.split(";")]
        nums = [order.index(k) + 1 for k in keys]
        body = body.replace(f"[@{grp}]", "[" + ", ".join(str(n) for n in nums) + "]", 1)
    return body, order


def load_bib(bib_path, order):
    text = Path(bib_path).read_text(encoding="utf-8")
    entries = {}
    for part in text.split("@")[1:]:
        m = re.match(r"(\w+)\s*\{\s*([\w_:]+),\s*", part, re.S)
        if not m:
            continue
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}", part[m.end():], re.S):
            fields[fm.group(1)] = " ".join(fm.group(2).split())
        entries[m.group(2)] = fields
    return [entries.get(k, {}) for k in order]


def fmt_authors(s):
    names = [x.strip() for x in s.split(" and ")]
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " & " + names[-1]


def format_references(refs):
    out = []
    for i, f in enumerate(refs, 1):
        authors = fmt_authors(f.get("author", f.get("editor", "Unknown")))
        year = f.get("year", "n.d.")
        title = f.get("title", "")
        journal = (f.get("journal") or f.get("booktitle") or f.get("publisher")
                   or f.get("howpublished", ""))
        loc = []
        if journal:
            loc.append(f"*{journal}*")
        if f.get("volume"):
            loc.append(f["volume"] + (f"({f['number']})" if f.get("number") else ""))
        if f.get("pages"):
            loc.append(f["pages"])
        line = f"[{i}] {authors} ({year}). {title}."
        if loc:
            line += " " + ", ".join(loc) + "."
        if f.get("doi"):
            line += f" [doi:{f['doi']}](https://doi.org/{f['doi']})"
        out.append(line)
    return "\n\n".join(out)


def build(tex_path, md_out, cfg):
    tex_path = Path(tex_path)
    tmp_tex = tex_path.parent / "_md_tex_tmp.tex"
    tmp_body = tex_path.parent / "_md_body_tmp.md"
    tmp_std = tex_path.parent / "_md_std_tmp.md"

    clean_tex = strip_texttt_renewcommand(tex_path, tmp_tex)
    body = pandoc(clean_tex, tmp_body)
    std = pandoc(clean_tex, tmp_std, standalone=True)
    abstract = extract_abstract(std)

    body = renumber_headings(body)
    body, order = convert_citations(body)

    front = (f"# {cfg['title']}\n{cfg['subtitle']}\n\n{AUTHOR_BLOCK}\n\n---\n\n"
             f"## Abstract\n\n{abstract}\n\n---\n\n## Table of Contents\n")
    toc = []
    for ln in body.splitlines():
        m = re.match(r"^## (.*)$", ln)
        if m:
            title = m.group(1)
            slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
            toc.append(f"- [{title}](#{slug})")

    refs = load_bib(tex_path.parent / "references.bib", order)
    md = (front + "\n".join(toc) + "\n\n---\n\n" + body
          + "\n---\n\n## References\n\n" + format_references(refs) + "\n")
    md = ("<!-- regenerated from "
          + tex_path.name + " by build/build_md.py -- edit the .tex (via the "
          "template), then rebuild -->\n\n" + md)

    Path(md_out).write_text(md, encoding="utf-8")
    tmp_tex.unlink()
    tmp_body.unlink()
    tmp_std.unlink()
    print(f"built {md_out} ({len(md.splitlines())} lines, {len(refs)} references)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True, choices=sorted(VERSIONS))
    args = ap.parse_args()
    cfg = VERSIONS[args.version]
    d = REPO / cfg["dir"]
    build(REPO / f"manuscript_{args.version}.tex",
          REPO / f"manuscript_{args.version}.md", cfg)
    build(d / f"manuscript_{args.version}.tex",
          d / f"manuscript_{args.version}.md", cfg)


if __name__ == "__main__":
    main()
