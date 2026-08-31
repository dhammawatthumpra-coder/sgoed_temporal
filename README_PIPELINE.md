# SGOED v5: Reproducible Research Pipeline

**Paper Title:** Temporal Emergence from Dynamical Observer Coupling  
**Author:** Sutipong Chanpengpad  
**Version:** 5.0 (Complete Scaling Analysis and Open Questions)

---

## 📂 Project Structure

```text
V5/
├── README.md                  # This file
├── manuscript_v5.tex          # Main LaTeX manuscript
├── references.bib             # Bibliography
│
├── code/
│   └── sgoed_core.py          # Core Monte Carlo simulation engine
│
├── run_all_experiments.py     # Master script to run all simulations
├── generate_figures.py        # Generates publication plots
├── generate_latex_tables.py   # Generates LaTeX tables from data
│
├── data/                      # (Auto-generated) JSON results
├── figures/                   # (Auto-generated) PNG/PDF plots
└── tables/                    # (Auto-generated) .tex table files
```

---

## 🚀 How to Reproduce the Paper (Step-by-Step)

### Prerequisites
Make sure you have Python 3.8+ installed with the following packages:
```bash
pip install numpy scipy matplotlib
```
*(And a LaTeX distribution like TeX Live or MiKTeX for compiling the PDF).*

### Step 1: Run All Experiments
This will execute the Phase Diagram, FSS, N=8 Tuning, and Statistical Tests.
*Estimated time: ~10-15 minutes.*

```bash
python run_all_experiments.py
```
*Output: Creates `data/sgoed_v5_results.json`*

### Step 2: Generate Publication Figures
Reads the JSON data and creates high-resolution plots.

```bash
python generate_figures.py
```
*Output: Creates `figures/fig1_phase_diagram.pdf`, etc.*

### Step 3: Generate LaTeX Tables
Automatically formats the statistical results into `.tex` files.

```bash
python generate_latex_tables.py
```
*Output: Creates `tables/tab_phase_diagram.tex`, etc.*

### Step 4: Compile the Manuscript
Update your `manuscript_v5.tex` to include the auto-generated tables and figures:
```latex
% In your Results section, replace the hardcoded tables with:
\input{tables/tab_phase_diagram.tex}
\input{tables/tab_fss_fixed.tex}
\input{tables/tab_n8_tuning.tex}

% Include figures like this:
\begin{figure}[ht]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/fig1_phase_diagram.pdf}
    \caption{Phase diagram by observer complexity.}
\end{figure}
```

Then compile:
```bash
pdflatex manuscript_v5.tex
bibtex manuscript_v5
pdflatex manuscript_v5.tex
pdflatex manuscript_v5.tex
```

---

## 📊 Key Results Expected

1. **Phase Diagram:** Optimal observer complexity at $d=4$ (CV=18.0%).
2. **FSS:** Robust emergence for $N \leq 6$, crossover at $N \geq 7$.
3. **Tuning:** $N=8$ requires $g_{XY} \approx 1.10$ for healthy emergence.
4. **Stats:** Paired t-test confirms robustness ($p = 0.738$).

---

## 📜 License
This code and the associated paper are licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.
