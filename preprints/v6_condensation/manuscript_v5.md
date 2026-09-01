# Temporal Emergence from Dynamical Observer Coupling: A Matrix Model for Observer-Dependent Symmetry Breaking
**Version 5: Complete Scaling Analysis and Open Questions**

**Author:** Sutipong Chanpengpad  
*Independent Researcher, Chiang Rai, Thailand*  
Email: `dhammawatthumpra@gmail.com`  
ORCID: [0009-0001-4069-8576](https://orcid.org/0009-0001-4069-8576)  

**Date:** August 2026

---

## Abstract

The Structural Time Framework (STF) proposes that time emerges from observer-dependent ordering of pre-temporal states. We present a computational demonstration using a matrix model where an explicit observer system $Y$ dynamically creates the temporal direction in the main system $X$, without any external parameters.

Our model employs a directional coupling mechanism where the observer generates a direction vector $v$ from its matrix traces, and dimensions of $X$ aligned with $v$ receive a temporal expansion term $-g_{XY} \hat{v}_\mu^2 \text{Tr}(X_\mu^4)$. Monte Carlo simulations with statistical analysis (5 seeds per configuration) show:

1. Temporal emergence occurs robustly for observer dimensions $d \in \{2,3,4,5\}$, with mean ratios clustering in $4.6$--$4.8$ and no statistically distinguishable differences between dimensions.
2. Perfect alignment between the temporal direction $X_{\max}$ and observer direction $v_{\max}$ in healthy emergence cases.
3. Two-regime scaling behavior: robust emergence for $N \le 6$ with fixed coupling, but parameter tuning required for $N \ge 7$.
4. A paired comparison between $d=3$ and $d=4$ found no significant difference ($t=1.043$, $p=0.356$); with $n=5$ seeds per condition this test has limited power and does not by itself establish equivalence or robustness.

**Important Caveats:** This work represents a toy-level mathematical exploration using small matrix sizes ($N \le 8$). Results demonstrate mathematical consistency, not physical reality.

**Keywords:** dynamical observer, temporal emergence, matrix models, symmetry breaking, computational demonstration

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Dynamical Observer Model](#2-dynamical-observer-model)
  - [2.1 Theoretical Motivation for the Coupling](#21-theoretical-motivation-for-the-coupling)
  - [2.2 Why the Observer Does Not Temporalize Itself](#22-why-the-observer-does-not-temporalize-itself)
- [3. Computational Methodology](#3-computational-methodology)
- [4. Results](#4-results)
  - [4.1 Statistical Robustness](#41-statistical-robustness)
  - [4.2 Observer-Dimension Phase Diagram](#42-observer-dimension-phase-diagram)
  - [4.3 Finite-Size Scaling and Parameter Sensitivity](#43-finite-size-scaling-and-parameter-sensitivity)
  - [4.4 Parameter Tuning at $N=8$](#44-parameter-tuning-at-n8)
  - [4.5 Two-Regime Scaling Picture](#45-two-regime-scaling-picture)
  - [4.6 Physical Interpretation of the Crossover](#46-physical-interpretation-of-the-crossover)
  - [4.7 Connection to IKKT Matrix Model](#47-connection-to-ikkt-matrix-model)
- [5. Discussion](#5-discussion)
  - [5.1 Advantages Over External Adapter](#51-advantages-over-external-adapter)
  - [5.2 Relation to Philosophical Positions](#52-relation-to-philosophical-positions)
- [6. Open Questions and Future Directions](#6-open-questions-and-future-directions)
- [7. Conclusion](#7-conclusion)
- [References](#references)

---

## 1. Introduction

The nature of time has been debated by philosophers and physicists for centuries. The Structural Time Framework (STF) [[6](#ref-6)] proposes that time is not fundamental but emerges from observer-dependent ordering of pre-temporal states.

In our previous work [[7](#ref-7)], we presented a toy model where temporal emergence was driven by an external adapter parameter $\kappa_2$. While successful, this approach had a fundamental limitation: the observer was represented as a parameter, not as a dynamical system.

This paper addresses that limitation by introducing an **explicit dynamical observer**—a matrix system $Y$ that dynamically creates the temporal direction in the main system $X$ through coupling, without any external parameters.

> **Important Disclaimer:** We emphasize that this work is a **toy-level computational demonstration**, not empirical physics. Our simulations use small matrix sizes ($N \le 8$), finite Monte Carlo samples, and idealized actions. The results demonstrate mathematical consistency, not physical reality.

---

## 2. Dynamical Observer Model

We consider two coupled matrix systems:

- **Main System $X$:** $D$ Hermitian matrices $X^\mu$ of size $N \times N$.
- **Observer System $Y$:** $d$ Hermitian matrices $Y^a$ of size $N \times N$.

The total action is:
$$S_{\text{total}} = S_X + S_Y + S_{\text{coupling}}$$

where $S_X$ and $S_Y$ are IKKT-like actions with stability gates, and the directional coupling is:
$$S_{\text{coupling}} = -g_{XY} \sum_\mu \hat{v}_\mu^2 \text{Tr}(X_\mu^4)$$

The observer generates direction $\hat{v}$ from its traces. This coupling temporalizes dimensions aligned with $\hat{v}$.

### 2.1 Theoretical Motivation for the Coupling

The coupling term can be understood from three perspectives:

1. **Effective Field Theory:** Leading-order term in $1/N$ expansion.
2. **Symmetry Breaking:** Explicitly breaks $\text{SO}(D) \to \text{SO}(D-1)$.
3. **Measurement Analogy:** Observer selects direction, system responds.

### 2.2 Why the Observer Does Not Temporalize Itself

The distinction between observer and system is relational, not fundamental. The asymmetry in coupling reflects the measurement paradigm: the apparatus measures the system, not vice versa. This avoids the self-observation paradox analogous to Wigner's friend.

---

## 3. Computational Methodology

We use Metropolis-Hastings sampling with:
- Matrix size: $N \in \{4, 5, 6, 7, 8\}$
- System dimensions: $D = 6$
- Observer dimensions: $d \in \{2, 3, 4, 5\}$
- Coupling strength: $g_{XY} \in [0.8, 1.2]$
- Thermalization: 20--25 sweeps
- Measurement: 30--40 sweeps
- Multiple seeds: $\{42, 43, 44, 45, 46\}$

Observables measured, with $\text{extent}(X_\mu) \equiv \text{Tr}(X_\mu^2)/N$:
$$\text{Ratio} = \frac{\text{extent}(X_{\max})}{\text{mean}(\text{extent}(X_{\neq \max}))}$$
$$\text{Alignment} = \mathbb{I}(\arg\max_\mu \text{extent}(X_\mu) == \arg\max_\mu \hat{v}_\mu^2)$$
$$H = -\sum_\mu p_\mu \ln p_\mu, \quad p_\mu = \frac{\text{extent}(X_\mu)}{\sum_\nu \text{extent}(X_\nu)}$$

A configuration is classified as **Healthy** if the mean Ratio over the five seeds satisfies $1.5 < \overline{R} < 10.0$; the upper bound $R=10$ coincides with the stability-gate cutoff (`max_extent`) used in the action itself, beyond which a quadratic penalty term dominates and suppresses further extent growth. Configurations with $\overline{R} \le 1.5$ are labeled Weak; none of the configurations reported below exceed the upper bound.

---

## 4. Results

### 4.1 Statistical Robustness

Table 1 summarizes results for optimal parameters.

**Table 1:** Statistical analysis ($N=6$, $g_{XY}=0.8$)

| $d$ | Mean Ratio | Std Dev | CV (%) | Alignment |
| :---: | :---: | :---: | :---: | :---: |
| 3 | 4.82 | $\pm$0.24 | 5.0% | 100% (5/5) |
| 4 | 4.60 | $\pm$0.28 | 6.0% | 100% (5/5) |

Paired t-test: $t = 1.043$, $p = 0.356$. This fails to reject the null of no difference between $d=3$ and $d=4$; note that with $n=5$ seeds per condition, absence of a significant difference is not evidence of equivalence, and this test alone does not establish robustness.

### 4.2 Observer-Dimension Phase Diagram

To investigate the role of observer complexity, we varied the observer dimension $d \in \{2,3,4,5\}$ while keeping $N=6$, $D=6$, and $g_{XY}=0.8$ fixed. Each configuration was evaluated over five independent random seeds.

**Table 2:** Phase diagram by observer dimension ($N=6$, $g_{XY}=0.8$)

| $d$ | Mean Ratio | Std Dev | CV (%) | Alignment | Status |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 2 | 4.81 | $\pm$0.46 | 9.5% | 100% (5/5) | Healthy |
| 3 | 4.82 | $\pm$0.24 | 5.0% | 100% (5/5) | Healthy |
| 4 | 4.60 | $\pm$0.28 | 6.0% | 100% (5/5) | Healthy |
| 5 | 4.62 | $\pm$0.16 | 3.4% | 100% (5/5) | Healthy |

Several features are noteworthy:

1. **No strict threshold at $d=3$:** Contrary to our initial expectation, even $d=2$ produces healthy temporal emergence with perfect alignment. This suggests that the minimum observer complexity required for temporalization is lower than anticipated.
2. **No significant differences across $d$:** Mean ratios cluster in a narrow range ($4.6$--$4.8$) across all four tested observer dimensions, and alignment is perfect (100%, 5/5 seeds) in every case. CV varies between $3.4\%$ and $9.5\%$ with no clear monotonic trend, and the paired comparison between $d=3$ and $d=4$ (Table 1) found no significant difference. We do not find evidence for an optimal or "sweet spot" observer dimension in this range; within the resolution of five seeds per configuration, the mechanism appears robust to the choice of $d \in \{2,3,4,5\}$. (An earlier draft of this table, generated before the simulation pipeline was consolidated into `code/sgoed_core.py`, had reported a spurious $d=4$ "sweet spot" and reduced $d=5$ alignment; those numbers could not be reproduced from the current codebase and have been replaced with freshly re-run, seed-logged values.)

### 4.3 Finite-Size Scaling and Parameter Sensitivity

We next tested whether the observed temporal emergence is a finite-size artifact by varying the matrix size $N$. We first fixed $d=3$ and $g_{XY}=0.8$ and examined $N \in \{4,5,6,7,8\}$.

**Table 3:** Finite-size scaling with fixed $g_{XY}=0.8$ ($d=3$)

| $N$ | Mean Ratio | Std Dev | CV (%) | Alignment | Status |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 4.87 | $\pm$0.63 | 12.9% | 100% (5/5) | Healthy |
| 5 | 4.90 | $\pm$0.44 | 9.0%  | 100% (5/5) | Healthy |
| 6 | 4.82 | $\pm$0.24 | 5.0%  | 100% (5/5) | Healthy |
| 7 | 1.83 | $\pm$0.42 | 23.0% | 80% (4/5)  | Weak |
| 8 | 1.70 | $\pm$0.50 | 29.4% | 100% (5/5) | Weak |

The data reveal two distinct regimes:

1. **Small-$N$ regime ($N \le 6$):** For $N=4,5,6$, the ratio remains stable near $R \approx 4.8$--$4.9$, with perfect alignment. This indicates that the mechanism is robust in the small-$N$ regime.
2. **Crossover regime ($N \approx 7$):** At $N=7$, the ratio drops to $R \approx 1.83$ and the alignment rate falls to 80%. This suggests the onset of a crossover where the fixed coupling $g_{XY}=0.8$ is no longer sufficient to produce strong temporalization.
3. **Large-$N$ sensitivity ($N \ge 7$):** At $N=8$, emergence remains weak for fixed $g_{XY}=0.8$, despite perfect alignment. This indicates that the observer direction is still correctly selected, but the coupling strength is insufficient to amplify it into a strong temporal hierarchy.

### 4.4 Parameter Tuning at $N=8$

To determine whether the weak emergence at $N=8$ represents a genuine breakdown or merely parameter sensitivity, we repeated the simulations at $N=8$ while varying $g_{XY}$.

**Table 4:** Parameter tuning at $N=8$ ($d=3$)

| $g_{XY}$ | Mean Ratio | Std Dev | CV (%) | Alignment | Status |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 0.80 | 1.70 | $\pm$0.50 | 29.4% | 100% (5/5) | Weak |
| 1.05 | 5.72 | $\pm$3.37 | 59.0% | 100% (5/5) | High variance |
| 1.10 | 7.41 | $\pm$2.33 | 31.5% | 100% (5/5) | Healthy / preferred |
| 1.15 | 8.45 | $\pm$2.24 | 26.5% | 100% (5/5) | Near boundary |

These results show that the apparent failure at $N=8$ is not a genuine absence of the mechanism. Instead, $N=8$ requires stronger coupling to restore temporal emergence.

The value $g_{XY}=1.10$ provides a useful compromise: it produces a healthy mean ratio $R \approx 7.41$, perfect alignment, and remains safely below the upper boundary $R=10$ on average. We therefore regard
$$g_{XY}^{\mathrm{opt}}(N=8) \approx 1.10$$
as the preferred working value in this parameter range.

We note that CV is non-monotonic in $g_{XY}$ over the scanned range, peaking at $g_{XY}=1.05$ (CV $=59.0\%$) before falling again at $g_{XY}=1.10, 1.15$. The cause of this spike is unclear from the present data: with $n=5$ seeds at a single point, we cannot distinguish an ordinary sampling fluctuation from a genuine feature of the model near $g_{XY}=1.05$. We flag this as an open question (Section [6](#6-open-questions-and-future-directions)) rather than propose a mechanism for it.

### 4.5 Two-Regime Scaling Picture

The combined finite-size and tuning data suggest a two-regime scaling structure.

**Table 5:** Estimated optimal coupling by system size

| $N$ | $g_{XY}^{\mathrm{opt}}$ | Mean Ratio | Alignment | Regime |
| :---: | :---: | :---: | :---: | :---: |
| 4 | 0.80 | 4.87 | 100% | Small-$N$ |
| 5 | 0.80 | 4.90 | 100% | Small-$N$ |
| 6 | 0.80 | 4.82 | 100% | Small-$N$ |
| 7 | $>0.80$ | 1.83 at $g=0.8$ | 80% | Crossover |
| 8 | $\approx 1.10$ | 7.41 | 100% | Tuned large-$N$ |

For $N \le 6$, the same coupling $g_{XY}=0.8$ produces stable temporal emergence. For $N \ge 7$, however, the system enters a regime where the coupling must be increased to maintain a strong temporal hierarchy.

We caution that only two anchor values of $g_{XY}^{\mathrm{opt}}$ are available ($\approx 0.8$ for $N \le 6$, and $\approx 1.10$ at $N=8$, itself selected by eye from four scanned values rather than fit), so any "power-law exponent" computed from them is a secant slope between two points, not an independent statistical estimate, and the two numbers below are not separate pieces of evidence but different pairings of the same two anchors. If one nonetheless assumes a power-law form
$$g_{XY}^{\mathrm{opt}}(N) \propto N^\alpha,$$
then using the range $N=6 \to 8$ gives
$$\alpha = \frac{\ln(1.10/0.80)}{\ln(8/6)} \approx \frac{0.318}{0.288} \approx 1.10,$$
while using the wider range $N=4 \to 8$ (which additionally assumes no change in $g_{XY}^{\mathrm{opt}}$ between $N=4$ and $N=6$) gives
$$\alpha = \frac{\ln(1.10/0.80)}{\ln(8/4)} \approx \frac{0.318}{0.693} \approx 0.46.$$

The factor-of-two spread between these two secant slopes is expected from their construction and should not be read as evidence against a power law; conversely, agreement between them would not have been evidence for one either, since both are computed from the same two data points. With only two anchors, the data cannot distinguish a power law from other monotonically increasing forms of $g_{XY}^{\mathrm{opt}}(N)$. Determining $\alpha$ (or ruling out a power law) would require $g_{XY}^{\mathrm{opt}}$ at intermediate points such as $N=7$ and beyond $N=8$. We therefore report these numbers only as a preliminary, non-independent sensitivity check, not as a scaling-exponent measurement, and the data are more naturally read as evidence for a crossover near $N \approx 7$ between a small-$N$ regime, where no tuning is required, and a larger-$N$ regime, where $g_{XY}$ must increase with system size.

### 4.6 Physical Interpretation of the Crossover

The observed crossover can be interpreted in several complementary ways:

1. **Phase-space volume:** Each matrix contains $N^2$ real degrees of freedom before symmetry constraints. For $N=8$, there are $d \times N^2 = 3 \times 64 = 192$ independent matrix elements (for $d=3$). Thermal fluctuations at inverse temperature $\beta = 1$ compete with the coupling energy $\propto g_{XY}$. For fixed $g_{XY}$, larger $N$ means more fluctuations, requiring larger $g_{XY}$ to maintain the symmetry-broken phase.
2. **Competition with IKKT term:** The IKKT commutator term scales as $\sim N^2$ in the large-$N$ limit. To overcome this and create a preferred direction, the coupling term must also scale appropriately, suggesting $g_{XY} \propto N^\alpha$ for some $\alpha > 0$.
3. **Entropy argument:** The number of possible configurations grows exponentially with $N$. To select a specific temporal direction from this exponentially large space requires coupling energy that grows with system size.

### 4.7 Connection to IKKT Matrix Model

This scaling behavior is reminiscent of the IKKT matrix model [[3](#ref-3), [4](#ref-4)]. In the Lorentzian IKKT model, Kim and Nishimura found that spontaneous symmetry breaking $\text{SO}(9) \to \text{SO}(3)$ requires $N \ge 10$ for clear emergence of (3+1)-dimensional spacetime. While the coupling in their model is fixed by $g^2$, the large-$N$ limit requires careful extrapolation and shows sensitivity to initial conditions.

Our model shows a similar sensitivity, but with an explicit scaling parameter $g_{XY}$ that must be tuned with $N$. This suggests that both spontaneous and observer-induced symmetry breaking face similar challenges in the large-$N$ limit, namely the competition between coupling energy and phase space volume.

---

## 5. Discussion

### 5.1 Advantages Over External Adapter

The dynamical observer approach offers several advantages:

1. **Physical Motivation:** Observer is dynamical system, not parameter.
2. **Emergent Direction:** Temporal direction emerges from observer dynamics.
3. **Robustness:** Works across $d = 2,3,4,5$ and multiple seeds.
4. **Measurement Theory:** Observer as measurement device.

### 5.2 Relation to Philosophical Positions

Our model is consistent with several philosophical positions within the restricted scope of our toy model:

- **Leibniz (relational time):** Temporal direction created by observer.
- **Barbour (timeless physics) [[9](#ref-9)]:** Pre-observer state is symmetric.
- **Rovelli (thermal time) [[2](#ref-2), [10](#ref-10)]:** Coupling creates preferred direction.
- **Relational QM [[5](#ref-5)]:** States relative to observer.

> **Important:** "Consistent with" does not mean "proves" or "validates." These philosophical positions remain open questions.

---

## 6. Open Questions and Future Directions

Our results raise several important questions that warrant further investigation:

1. **Precise Scaling Exponent:** Our preliminary estimate $\alpha \approx 0.46$--$1.10$ is based on limited data points. More systematic studies at intermediate system sizes ($N=5, 7, 9, 10$) are needed to confirm the power-law scaling hypothesis and determine whether $\alpha$ is constant or varies with $N$.
2. **Nature of the Crossover:** Is the crossover at $N \approx 7$ a sharp transition or a smooth crossover? Does it depend on observer dimension $d$? Would increasing $d$ at large $N$ reduce the required coupling strength?
3. **Large-$N$ Behavior:** The scaling behavior at $N > 8$ remains unexplored. Key questions include: Does the scaling $g_{XY}^{\text{opt}}(N) \propto N^\alpha$ persist? Is there a critical $N_c$ where the mechanism breaks down permanently? How does the continuum limit ($N \to \infty$) behave?
4. **Sweet Spot Determination:** At $N=8$, the optimal coupling appears to be $g_{XY}^{\text{opt}} \approx 1.10$. Finer sampling in this range (e.g., $g_{XY} = 1.08, 1.12$) would identify the precise sweet spot where emergence is strongest with minimal variance.
5. **Observer Complexity Scaling:** How does the optimal observer dimension $d^{\text{opt}}$ scale with $N$? Is there a relation $d^{\text{opt}}(N) \propto N^\beta$? Would larger $d$ at large $N$ restore emergence without requiring stronger coupling?
6. **Universality:** Would this mechanism work with different coupling structures or different matrix models (e.g., BFSS, Lorentzian IKKT)? How universal is the observer-induced temporalization phenomenon?
7. **Connection to Quantum Gravity:** The finite-size scaling and crossover behavior may have analogs in emergent spacetime scenarios. Can this model be connected to holographic duality or other quantum gravity frameworks?
8. **Renormalization Group Analysis:** The scaling behavior suggests the need for RG analysis to understand how $g_{XY}$ flows with scale. Such an analysis would determine whether the scaling is a physical feature of the continuum theory or an artifact of our phenomenological coupling.
9. **Non-Monotonic Variance Near $g_{XY}=1.05$:** At $N=8$, the coefficient of variation peaks sharply at $g_{XY}=1.05$ (CV $=59.0\%$) between lower values at $g_{XY}=0.80$ and higher values at $g_{XY}=1.10,1.15$ (Section [4.4](#44-parameter-tuning-at-n8)). Is this a reproducible feature of the model (e.g., proximity to a region of enhanced fluctuations) or an artifact of $n=5$ seeds at a single point? Denser sampling around $g_{XY}=1.05$ with more seeds would be needed to distinguish these possibilities.

---

## 7. Conclusion

We have presented a toy-level computational demonstration of temporal emergence from a dynamical observer. Our key findings:

1. An observer system $Y$ can dynamically create the temporal direction in a main system $X$ through directional coupling.
2. For coupling $g_{XY} \in [0.8, 1.2]$ and observer dimensions $d \in \{2, 3, 4, 5\}$, we observe healthy temporal emergence with ratios $1.8$--$8.5$.
3. Perfect alignment ($X_{\max} = v_{\max}$) in healthy emergence cases confirms the observer's active role.
4. Two-regime scaling: robust for $N \le 6$, parameter tuning required for $N \ge 7$.
5. A paired comparison between $d=3$ and $d=4$ found no significant difference ($p = 0.356$), though with $n=5$ seeds per condition this does not by itself establish robustness or equivalence.

**Appropriate Interpretation:** These results demonstrate that dynamical observer temporalization *can be represented* in a consistent mathematical framework. They do not prove that time emerges from observer coupling in nature.

**Final Statement:** This work is a toy-level demonstration of mathematical consistency, not a discovery of physical laws. Following the philosophy of our exploratory notes, we emphasize that this is a **design framework demonstrating mathematical consistency**, not empirical physics.

---

## References

<a id="ref-1"></a>[1] Page, D. N., & Wootters, W. K. (1983). Evolution without evolution: Dynamics described by stationary observables. *Physical Review D*, 27(12), 2885–2892. [doi:10.1103/PhysRevD.27.2885](https://doi.org/10.1103/PhysRevD.27.2885)

<a id="ref-2"></a>[2] Connes, A., & Rovelli, C. (1994). Von Neumann algebra automorphisms and time-thermodynamics relation. *Classical and Quantum Gravity*, 11(12), 2899–2918. [doi:10.1088/0264-9381/11/12/007](https://doi.org/10.1088/0264-9381/11/12/007)

<a id="ref-3"></a>[3] Kim, S.-W., Nishimura, J., & Tsuchiya, A. (2012). Expanding (3+1)-dimensional universe from a Lorentzian matrix model for superstring theory in (9+1) dimensions. *Physical Review Letters*, 108(1), 011601. [doi:10.1103/PhysRevLett.108.011601](https://doi.org/10.1103/PhysRevLett.108.011601)

<a id="ref-4"></a>[4] Kim, S.-W., Nishimura, J., & Tsuchiya, A. (2012). Late time behaviors of the expanding universe in the IIB matrix model. *Journal of High Energy Physics*, 2012(10), 147. [doi:10.1007/JHEP10(2012)147](https://doi.org/10.1007/JHEP10(2012)147)

<a id="ref-5"></a>[5] Rovelli, C. (1996). Relational quantum mechanics. *International Journal of Theoretical Physics*, 35(8), 1637–1678. [doi:10.1007/BF02302261](https://doi.org/10.1007/BF02302261)

<a id="ref-6"></a>[6] Chanpengpad, S. (2026). *Structural Time Framework*. Zenodo. [doi:10.5281/zenodo.21763905](https://doi.org/10.5281/zenodo.21763905)

<a id="ref-7"></a>[7] Chanpengpad, S. (2026). *SGOED: An Atemporal Matrix Formalism for Stability-Gated Crystallization and Aggregation (Phase 1-2)*. Zenodo. [doi:10.5281/zenodo.21786260](https://doi.org/10.5281/zenodo.21786260)

<a id="ref-8"></a>[8] Metropolis, N., Rosenbluth, A. W., et al. (1953). Equation of state calculations by fast computing machines. *Journal of Chemical Physics*, 21(6), 1087–1092. [doi:10.1063/1.1699114](https://doi.org/10.1063/1.1699114)

<a id="ref-9"></a>[9] Barbour, J. (1999). *The End of Time*. Oxford University Press.

<a id="ref-10"></a>[10] Rovelli, C. (2018). *The Order of Time*. Riverhead Books.
