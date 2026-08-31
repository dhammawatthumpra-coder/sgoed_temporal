"""One-off assembler: pandoc body -> manuscript_v7.tex (v6-template style)."""
import re

BODY = open("_v7_body.tex", encoding="utf-8").read()

# --- 0. unicode -> LaTeX ---
BODY = BODY.replace("≥", "$\\geq$").replace("±", "$\\pm$")
BODY = BODY.replace("→", "$\\rightarrow$").replace("ø", "\\o")
BODY = BODY.replace("≈", "$\\approx$").replace("≤", "$\\leq$")
BODY = BODY.replace("−", "-").replace("≳", "$\\gtrsim$")
BODY = BODY.replace("×", "$\\times$")

# --- 1. drop title block (H1 title + subtitle + author block) up to Abstract ---
i_abs = BODY.index("\\subsection{Abstract}")
BODY = BODY[i_abs:]

# --- 2. extract Abstract, drop TOC ---
i_toc = BODY.index("\\subsection{Table of Contents}", i_abs)
abstract = BODY[len("\\subsection{Abstract}\n"):i_toc].strip()
i_s1 = BODY.index("\\subsection{1.", i_toc)
BODY = BODY[i_s1:]

# --- 3. drop the References section at the end ---
i_ref = BODY.find("\\subsection{References}")
if i_ref != -1:
    BODY = BODY[:i_ref].rstrip()

# --- 4. promote headings + strip manual numbers ---
BODY = re.sub(r"\\subsection\{(\d+)\.\s*", r"\\subsection{", BODY)
BODY = re.sub(r"\\subsubsection\{(\d+)\.\s*", r"\\subsubsection{", BODY)
BODY = BODY.replace("\\subsection{", "\\section{").replace("\\subsubsection{", "\\subsection{")

# --- 5. appendices (pandoc auto-labels B only; A gets one here) ---
BODY = re.sub(r"\\section\{Appendix A: Reproducibility\}",
              r"\\appendix\n\\section{Reproducibility}\\label{appendix-a-reproducibility}", BODY)
BODY = re.sub(r"\\section\{Appendix B: Trap Catalog\}\\label\{appendix-b-trap-catalog\}",
              r"\\section{Trap Catalog}\\label{appendix-b-trap-catalog}", BODY)

# --- 5b. pandoc strips the manual number from heading ids; restore links ---
BODY = BODY.replace("\\hyperref[42-route-1-past-hypothesis]",
                    "\\hyperref[route-1-past-hypothesis]")
BODY = BODY.replace("\\hyperref[43-route-2-sequential-growth-and-its-mechanism]",
                    "\\hyperref[route-2-sequential-growth-and-its-mechanism]")

# --- 6. reference hyperlinks -> \cite{} ---
KEYS = {1: "page_wootters_1983", 2: "connes_rovelli_1994", 3: "kim_nishimura_2011",
        4: "kim_nishimura_2012", 5: "rovelli_rqm_1996", 6: "chanpengpad_stf",
        7: "chanpengpad_sgoed_v2", 8: "metropolis_1953", 9: "barbour_1999",
        10: "rovelli_2018", 11: "rideout_sorkin_2000", 12: "sorkin_2005",
        13: "myrhem_1978", 14: "ambjorn_jurkiewicz_loll_2005",
        15: "ishibashi_kawai_kitazawa_tsuchiya_1997", 16: "albert_2000"}


def repl(m):
    return "\\cite{%s}" % KEYS[int(m.group(1))]


BODY = re.sub(r"\\hyperref\[ref-(\d+)\]\{\d+\}", repl, BODY)

PREAMBLE = r"""\documentclass[12pt,a4paper]{article}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{calc}
\newcounter{none}
\providecommand{\real}[1]{#1}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{enumitem}
\usepackage{url}
\usepackage{doi}

\geometry{margin=1in}
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

% Theorem environments
\newtheorem{definition}{Definition}
\newtheorem{proposition}{Proposition}
\newtheorem{remark}{Remark}

% Title information
\title{\textbf{The Arrow of Time Is Not in the Ensemble}\\[0.4cm]
       \large An Audited Toy-Model Quest across Equilibrium Matrices,
       Sequential Growth, and Causal Sets (SGOED V7)}

\author{Sutipong Chanpengpad\\
\small Independent Researcher, Chiang Rai, Thailand\\
\small \texttt{dhammawatthumpra@gmail.com}\\
\small \href{https://orcid.org/0009-0001-4069-8576}{ORCID: 0009-0001-4069-8576}}

\date{\today}

\begin{document}

\maketitle

\begin{abstract}
__ABSTRACT__
\end{abstract}

"""

TAIL = r"""
\bibliographystyle{plain}
\bibliography{references}

\end{document}
"""

with open("manuscript_v7.tex", "w", encoding="utf-8") as f:
    f.write(PREAMBLE.replace("__ABSTRACT__", abstract) + BODY + TAIL)
print("manuscript_v7.tex written (%d lines body)" % len(BODY.splitlines()))