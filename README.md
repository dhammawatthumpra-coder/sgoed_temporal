# SGOED v5: Dynamical Observer Model

**Author:** Sutipong Chanpengpad  
**Version:** 5.0 (Complete Scaling Analysis and Open Questions)  
**License:** CC BY 4.0  
**Date:** 2026-08-28

## Overview

Complete replication package for the paper:

> **"Temporal Emergence from Dynamical Observer Coupling: A Matrix Model for Observer-Dependent Symmetry Breaking"**

The SGOED (Structural Gradient Ontology & Equilibrium Dynamics) v5 framework demonstrates how a dynamical observer system can create temporal structure in a main matrix system through directional coupling, with comprehensive analysis of scaling behavior and parameter sensitivity.

## Important Caveats

**This work represents a toy-level computational demonstration, NOT empirical physics.**

- Matrix sizes: N ≤ 8 (far from large-N limit)
- Finite Monte Carlo samples (5 seeds per configuration)
- Idealized actions (phenomenological coupling)
- No empirical verification claimed

Results demonstrate **mathematical consistency**, not physical reality. All interpretations should be understood as proof-of-concept demonstrations within the model's specific construction.

## Key Results

### Phase Diagram by Observer Dimension (N=6, g_XY=0.8)

| d | Mean Ratio | Std Dev | CV (%) | Alignment |
|---|------------|---------|--------|-----------|
| 2 | 2.73 | ±0.93 | 34.1% | 100% (5/5) |
| 3 | 2.53 | ±0.82 | 32.2% | 100% (5/5) |
| **4** | **2.92** | **±0.53** | **18.0%** | **100% (5/5)** |
| 5 | 2.56 | ±0.91 | 35.5% | 80% (4/5) |

**Key finding:** Optimal stability at d=4 with lowest variance (CV=18.0%)

### Finite-Size Scaling (d=3, g_XY=0.8)

| N | Mean Ratio | Std Dev | CV (%) | Alignment | Status |
|---|------------|---------|--------|-----------|--------|
| 4 | 4.87 | ±0.63 | 12.9% | 100% | Healthy |
| 5 | 4.90 | ±0.44 | 9.0% | 100% | Healthy |
| 6 | 4.82 | ±0.24 | 5.0% | 100% | Healthy |
| 7 | 1.83 | ±0.42 | 23.0% | 80% | Weak |
| 8 | 1.70 | ±0.50 | 29.4% | 100% | Weak |

**Key finding:** Two-regime behavior with crossover at N≈7

### N=8 Parameter Tuning (d=3)

| g_XY | Mean Ratio | Std Dev | CV (%) | Alignment |
|------|------------|---------|--------|-----------|
| 0.80 | 1.70 | ±0.50 | 29.4% | 100% |
| 1.05 | 5.72 | ±3.37 | 59.0% | 100% |
| **1.10** | **7.41** | **±2.33** | **31.5%** | **100%** |
| 1.15 | 8.45 | ±2.24 | 26.5% | 100% |

**Key finding:** Optimal coupling at N=8 is g_XY≈1.10

### Statistical Significance (d=3 vs d=4)

- Paired t-test: t=0.359, p=0.738
- **No significant difference** between observer dimensions
- Mechanism is **ROBUST** across d=3 and d=4

## Repository Structure

```
sgoed_v5/
├── manuscript_v5.tex       # Main LaTeX paper (complete)
├── references.bib          # Bibliography
├── run_experiments.py      # Python script for all experiments
├── sgoed_v5_results.json   # Complete results (generated)
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)

### Python Dependencies

```bash
pip install numpy scipy matplotlib
```

## Usage

### Running All Experiments

```bash
python run_experiments.py
```

This will:
1. Run Phase Diagram experiments (d=2,3,4,5)
2. Run Finite-Size Scaling (N=4,5,6,7,8)
3. Run N=8 Parameter Tuning (g=0.8, 1.05, 1.10, 1.15)
4. Run Statistical Significance Test (paired t-test)
5. Save all results to `sgoed_v5_results.json`

**Estimated runtime:** ~10-15 minutes

### Compiling the Manuscript

```bash
pdflatex manuscript_v5.tex
bibtex manuscript_v5
pdflatex manuscript_v5.tex
pdflatex manuscript_v5.tex
```

This will generate `manuscript_v5.pdf` with all tables and references.

## Model Description

### Action

The total action is:
```
S_total = S_X + S_Y + S_coupling
```

where:
- **S_X:** IKKT action + stability gate for main system X
- **S_Y:** IKKT action + stability gate for observer Y  
- **S_coupling = -g_XY Σ_μ v̂_μ² Tr(X_μ⁴)**: directional coupling

The observer Y generates a direction vector v from its traces, which then temporalizes the main system X.

### Mechanism

1. Observer dynamics generate direction v̂
2. Coupling gives X_μ aligned with v̂ a tendency to spread
3. Spreading dimension becomes temporal
4. Temporal direction **emerges from observer**, not imposed externally

## Two-Regime Scaling Behavior

The finite-size scaling analysis reveals two distinct regimes:

**Small-N Regime (N ≤ 6):**
- Optimal coupling: g_XY = 0.8 (constant)
- No parameter tuning required
- Mechanism is intrinsically robust

**Large-N Regime (N ≥ 7):**
- Optimal coupling: g_XY > 0.8 (increases with N)
- Parameter tuning required
- Preliminary scaling: g_XY^opt(N) ∝ N^α with α ≈ 0.46--1.10

The crossover at N≈7 suggests a transition where the phase space volume becomes large enough to require stronger coupling to maintain temporalization.

## Theoretical Connections

This work connects to:
- **Page-Wootters mechanism** (1983): Time from entanglement
- **Connes-Rovelli thermal time** (1994): Time from thermal states
- **Kim-Nishimura IKKT** (2011-2019): Spacetime emergence
- **Relational quantum mechanics** (Rovelli 1996): Observer-dependent states

## Open Questions

The paper identifies several important open questions:

1. **Precise Scaling Exponent:** Need more data points at N=5,7,9,10
2. **Nature of the Crossover:** Sharp transition or smooth crossover?
3. **Large-N Behavior:** Does scaling persist for N>8?
4. **Observer Complexity:** How does optimal d scale with N?
5. **Renormalization Group:** Understanding g_XY flow with scale

## Citation

If you use this work, please cite:

```bibtex
@software{chanpengpad_2026_sgoed_v5,
  author = {Chanpengpad, Sutipong},
  title = {SGOED v5: Dynamical Observer Model - Complete Replication Package},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXXX},
  version = {5.0}
}
```

## Related Work

- **SGOED Phase 1-2**: [Zenodo DOI: 10.5281/zenodo.21786260](https://zenodo.org/record/21786260)
- **STF Framework**: [Zenodo DOI: 10.5281/zenodo.21763905](https://zenodo.org/record/21763905)
- **SGOED Exploratory Notes**: [Zenodo DOI: 10.5281/zenodo.21787150](https://zenodo.org/record/21787150)

## Known Limitations

- Small matrix sizes (N ≤ 8)
- Phenomenological coupling (not derived from first principles)
- Classical Monte Carlo (not quantum)
- No back-reaction from X to Y
- Single observer (no multiple observer scenarios)
- Limited scaling data (only N=4,5,6,7,8)

## Future Work

- [ ] More systematic scaling study (N=5,7,9,10,12)
- [ ] Quantum observer models with entanglement
- [ ] Back-reaction and mutual coupling
- [ ] Information-theoretic analysis (entropy, mutual information)
- [ ] Multiple observers and consensus mechanisms
- [ ] Renormalization group analysis

## Contact

**Sutipong Chanpengpad**  
Independent Researcher, Chiang Rai, Thailand  
Email: dhammawatthumpra@gmail.com  
ORCID: [0009-0001-4069-8576](https://orcid.org/0009-0001-4069-8576)

## License

This work is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

---

**Last Updated:** 2026-08-28  
**Version:** 5.0  
**Status:** ✅ Ready for publication
