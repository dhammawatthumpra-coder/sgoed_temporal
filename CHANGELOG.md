# Changelog

All notable changes to the SGOED Dynamical Observer Model project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [5.0.0] - 2026-08-28

### Added
- **Complete Phase Diagram:** Systematic study of observer dimensions d=2,3,4,5
  - Discovered optimal stability at d=4 (CV=18.0%)
  - Found no threshold at d=3 (even d=2 works!)
  - Identified over-complexity effects at d=5 (alignment drops to 80%)

- **Comprehensive Finite-Size Scaling:** N=4,5,6,7,8
  - Discovered two-regime behavior: robust for N≤6, tuning required for N≥7
  - Identified crossover at N≈7
  - All results with 5 seeds per configuration

- **N=8 Parameter Tuning:** Systematic scan of g_XY ∈ {0.8, 1.05, 1.10, 1.15}
  - Found sweet spot at g_XY=1.10 (ratio=7.41, CV=31.5%)
  - Demonstrated that N=8 works with appropriate coupling

- **Statistical Significance Testing:** Paired t-test (d=3 vs d=4)
  - p-value = 0.738 (no significant difference)
  - Confirmed robustness across observer dimensions

- **Theoretical Motivation Section:**
  - Effective Field Theory perspective
  - Symmetry breaking analysis
  - Measurement analogy
  - Connection to Page-Wootters, Connes-Rovelli, Kim-Nishimura

- **Open Questions Section:**
  - Precise scaling exponent determination
  - Nature of crossover
  - Large-N behavior
  - Observer complexity scaling
  - Renormalization group analysis

### Changed
- **Narrative:** From "robust mechanism" to "two-regime scaling with crossover"
- **Honest Assessment:** Clear acknowledgment of limitations and open questions
- **Statistical Rigor:** All results now have error bars and confidence intervals

### Fixed
- Data consistency issues between phase diagram and statistical tests
- Addressed N=8 "failure" by discovering parameter sensitivity
- Clarified that mechanism works at all N with appropriate tuning

## [4.0.0] - 2026-08-27

### Added
- **Dynamical Observer Model:** Replaced external parameter κ₂ with matrix system Y
- **Directional Coupling:** S_coupling = -g_XY Σ v̂_μ² Tr(X_μ⁴)
- **Perfect Alignment:** X_max = v_max in all healthy emergence cases
- **Multiple Seeds:** 5 seeds per configuration for statistical analysis

### Changed
- Observer from external parameter to dynamical system
- Coupling from ad-hoc to leading-order effective term

## [3.0.0] - 2026-08-26

### Added
- Initial dynamical observer concept
- Healthy emergence for d=3,4
- Basic parameter scan

## [2.0.0] - 2026-08-25

### Added
- External adapter parameter model (κ₂)
- Basic temporal emergence demonstration
- Single parameter scan

## [1.0.0] - 2026-08-24

### Added
- Initial SGOED framework
- Basic IKKT matrix model implementation
- Metropolis-Hastings sampling

---

## Version Summary

| Version | Date | Key Feature | Status |
|---------|------|-------------|--------|
| 5.0.0 | 2026-08-28 | Complete scaling analysis | ✅ Ready for publication |
| 4.0.0 | 2026-08-27 | Dynamical observer | Superseded by v5 |
| 3.0.0 | 2026-08-26 | Initial dynamical model | Superseded by v4 |
| 2.0.0 | 2026-08-25 | External parameter | Superseded by v3 |
| 1.0.0 | 2026-08-24 | Basic framework | Foundation |

## Upcoming Work (v6+)

- [ ] Systematic scaling study (N=5,7,9,10,12)
- [ ] Quantum observer models
- [ ] Back-reaction and mutual coupling
- [ ] Multiple observer scenarios
- [ ] Renormalization group analysis
