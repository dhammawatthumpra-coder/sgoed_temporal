<!-- regenerated from manuscript_v6.tex on 2026-09-01 — edit the .tex, then rebuild -->

# Temporal Emergence from Dynamical Observer Coupling: A Matrix Model for Observer-Dependent Symmetry Breaking
**Version 6: Trajectory-Mean Analysis with Corrected Sampler**

**Author:** Sutipong Chanpengpad  
*Independent Researcher, Chiang Rai, Thailand*  
Email: `dhammawatthumpra@gmail.com`  
ORCID: [0009-0001-4069-8576](https://orcid.org/0009-0001-4069-8576)

**Date:** August 2026

---

## Abstract

The Structural Time Framework (STF) proposes that time emerges from
observer-dependent ordering of pre-temporal states. We present a
computational demonstration using a matrix model where an explicit
observer system $Y$ dynamically creates the temporal direction in the
main system $X$, without any external parameters.

Our model employs a directional coupling mechanism where the observer
generates a direction vector $v$ from its matrix traces, and
dimensions of $X$ aligned with $v$ receive a temporal expansion term
$-g_{XY} \hat{v}_\mu^2 \text{Tr}(X_\mu^4)$. All results reported here
use the **v6 trajectory-mean estimator**: observables are averaged
over the measurement window (30 recorded sweeps) rather than read from
a single final configuration. Monte Carlo simulations with statistical
analysis (5 seeds per configuration, with a $30$-seed follow-up for
the observer-dimension study) show:

1.  Temporal emergence occurs robustly for observer dimensions
    $d \in \{2,3,4,5\}$ and system sizes $N \in \{4,5,\ldots,16\}$,
    with mean ratios clustering in $4.4$--$4.8$ and alignment at
    $100\%$ in every configuration.

2.  No crossover or two-regime scaling is observed: emergence remains
    healthy across the entire tested range of $N$ up to $N=16$, with
    no threshold at which fixed coupling $g_{XY}=0.8$ fails to
    temporalize the system.

3.  Perfect alignment between the temporal direction $X_{\max}$ and
    observer direction $v_{\max}$ in all healthy emergence cases.

4.  A follow-up with $n=30$ seeds per condition shows a weak but
    detectable monotonic decrease of the mean ratio with observer
    dimension (slope $\approx -0.08$ per unit $d$, $p=0.003$,
    $R^2=0.07$), although the pairwise comparison between $d=3$ and
    $d=4$ is not significant at this sample size ($t=0.52$, $p=0.61$).
    The earlier $n=5$ result ($p=0.049$) was a small-sample
    fluctuation.

**Important Caveats:** This work represents a toy-level mathematical
exploration using small matrix sizes ($N \leq 16$). Results
demonstrate mathematical consistency, not physical reality.

**Keywords:** dynamical observer, temporal emergence, matrix models,
symmetry breaking, computational demonstration
author:
- |
Sutipong Chanpengpad\
Independent Researcher, Chiang Rai, Thailand\
`dhammawatthumpra@gmail.com`\
[ORCID: 0009-0001-4069-8576](https://orcid.org/0009-0001-4069-8576)
bibliography:
- references.bib
date: 2026-09-01
title: |
**Temporal Emergence from Dynamical Observer Coupling:\
A Matrix Model for Observer-Dependent Symmetry Breaking**\
Version 6: Trajectory-Mean Analysis with Corrected Sampler

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Dynamical Observer Model](#2-dynamical-observer-model)
- [3. Computational Methodology](#3-computational-methodology)
- [4. Results](#4-results)
- [5. Discussion](#5-discussion)
- [6. Open Questions and Future Directions](#6-open-questions-and-future-directions)
- [7. Conclusion](#7-conclusion)

---

## 1. Introduction

The nature of time has been debated by philosophers and physicists for
centuries [1, 2, 3]. The
Structural Time Framework (STF) [4] proposes that time is
not fundamental but emerges from observer-dependent ordering of
pre-temporal states.

In our previous work [5], we presented a toy model
where temporal emergence was driven by an external adapter parameter
$\kappa_2$. While successful, this approach had a fundamental
limitation: the observer was represented as a parameter, not as a
dynamical system.

This paper addresses that limitation by introducing an **explicit
dynamical observer**---a matrix system $Y$ that dynamically creates the
temporal direction in the main system $X$ through coupling, without any
external parameters.

**Important Disclaimer:** We emphasize that this work is a **toy-level
computational demonstration**, not empirical physics. Our simulations
use small matrix sizes ($N \leq 16$), finite Monte Carlo samples, and
idealized actions. The results demonstrate mathematical consistency, not
physical reality.

## 2. Dynamical Observer Model

We consider two coupled matrix systems:

**Main System $X$:** $D$ Hermitian matrices $X^\mu$ of size
$N \times N$.

**Observer System $Y$:** $d$ Hermitian matrices $Y^a$ of size
$N \times N$.

The total action is: $$\begin{equation}
S_{\text{total}} = S_X + S_Y + S_{\text{coupling}}
\end{equation}$$

where $S_X$ and $S_Y$ are IKKT-like actions with stability gates, and
the directional coupling is: $$\begin{equation}
S_{\text{coupling}} = -g_{XY} \sum_\mu \hat{v}_\mu^2 \text{Tr}(X_\mu^4)
\end{equation}$$

The observer generates direction $\hat{v}$ from its traces. This
coupling temporalizes dimensions aligned with $\hat{v}$.

### 2.1 Theoretical Motivation for the Coupling

The coupling term can be understood from three perspectives:

1.  **Effective Field Theory:** Leading-order term in $1/N$ expansion.

2.  **Symmetry Breaking:** Explicitly breaks SO(D) $\rightarrow$
    SO(D-1).

3.  **Measurement Analogy:** Observer selects direction, system
    responds.

### 2.2 Why the Observer Does Not Temporalize Itself

The distinction between observer and system is relational, not
fundamental. The asymmetry in coupling reflects the measurement
paradigm: the apparatus measures the system, not vice versa. This avoids
the self-observation paradox analogous to Wigner's friend.

## 3. Computational Methodology

We use Metropolis-Hastings sampling [6] with:

- Matrix size: $N \in \{4, 5, 6, 7, 8\}$, with a larger-$N$ extension to
  $N \in \{9, 10, 12, 14, 16\}$
  (Section [4.3](#sec:fss){reference-type="ref" reference="sec:fss"})

- System dimensions: $D = 6$

- Observer dimensions: $d \in \{2, 3, 4, 5\}$

- Coupling strength: $g_{XY} \in [0.8, 1.15]$

- Thermalization: 20 sweeps

- Measurement: 30 sweeps

- Multiple seeds: $\{42, 43, 44, 45, 46\}$ (base set), plus
  $\{100,\dots,129\}$ for the $30$-seed observer-dimension study

**Thermalization check:** the observables reported below are robust to
increasing the thermalization budget. Re-running representative
configurations with $n_{\mathrm{therm}} = 20, 40, 80, 160$ leaves the
mean ratio and alignment unchanged (e.g. $R \approx 4.72$--$4.84$ at
$N=8$, $d=3$, $g_{XY}=0.8$), and the wall fraction stays at zero
throughout. We therefore regard $n_{\mathrm{therm}} = 20$ as sufficient
for the healthy (v6) regime studied here. (For the separate
two-way-coupling model of v7, in which the observer itself can be driven
into the stability gate, $n_{\mathrm{therm}}=20$ was found insufficient
and a larger budget is required; that model is not reported in this
paper.)

The sampler is the **correctness-first v6 engine**
(`code/sgoed_core_v6.py`). It computes Metropolis acceptance via an
incremental local-energy delta rather than a full-action recomputation;
the delta was validated against the full action to machine precision
(maximum relative error $< 10^{-9}$ over 4000 randomized trials,
including wall-regime edge cases). The v6 sampler updates every matrix
element at every sweep. This replaces the earlier v5 engine, which
applied a `step=2` element-skip optimization for $N>6$ (updating only
even-indexed matrix elements)---a shortcut that we subsequently
identified as the source of a spurious finite-size crossover and a
spurious variance spike at $N=8$
(Section [4.5](#sec:absence_crossover){reference-type="ref"
reference="sec:absence_crossover"}).

All observables are recorded over the measurement window and then
averaged (**trajectory mean**), rather than read from a single final
configuration.

Observables measured, with
$\text{extent}(X_\mu) \equiv \text{Tr}(X_\mu^2)/N$: $$\begin{align}
\text{Ratio} &= \frac{\text{extent}(X_{\max})}{\text{mean}(\text{extent}(X_{\neq \max}))} \\
\text{Alignment} &= \mathbb{I}(\arg\max_\mu \text{extent}(X_\mu) == \arg\max_\mu \hat{v}_\mu^2) \\
H &= -\sum_\mu p_\mu \ln p_\mu, \quad p_\mu = \frac{\text{extent}(X_\mu)}{\sum_\nu \text{extent}(X_\nu)}
\end{align}$$

A configuration is classified as **Healthy** if the mean Ratio over the
sampled seeds satisfies $1.5 < \overline{R} < 10.0$; configurations with
$\overline{R} \leq 1.5$ are labeled Weak. The upper bound $R=10$ is
chosen to match the stability-gate cutoff on the per-matrix *extent*
(`max_extent`$=10.0$) used in the action itself. We emphasize that the
two quantities are distinct: the gate acts on $\text{extent}(X_\mu) =
\text{Tr}(X_\mu^2)/N$ of a *single* matrix (a dimensionful scale),
whereas $R$ is the *dimensionless ratio* of the largest extent to the
mean of the remaining extents. When the aligned dimension is driven
toward the gate ceiling, its extent saturates just below $10.0$ while
the others remain near $1$, so $R$ approaches $\sim 10$ even though no
individual extent ever exceeds the cutoff (the gate penalty suppresses
growth before the threshold is crossed). None of the configurations
reported below have an individual extent exceeding $10.0$.

## 4. Results

### 4.1 Statistical Robustness

Table [1](#tab:stats){reference-type="ref" reference="tab:stats"}
summarizes results for optimal parameters.

   $d$   Mean Ratio            Std Dev             CV (%)    Alignment
  ----- ------------ ---------------------------- -------- --------------
    3       4.65      $\pm$`<!-- -->`{=html}0.23    4.9%    100% (30/30)
    4       4.61      $\pm$`<!-- -->`{=html}0.32    7.0%    100% (30/30)

  : Statistical analysis ($N=6$, $g_{XY}=0.8$)

A follow-up with $n=30$ seeds per condition (rather than the initial
$n=5$) gives a paired t-test of $t = 0.52$, $p = 0.61$ for the $d=3$
versus $d=4$ comparison. This is not significant. The marginally
significant result reported in an earlier draft of this version
($t=2.804$, $p=0.049$ at $n=5$) is therefore attributed to a
small-sample fluctuation and is withdrawn: with a larger sample the
pairwise difference between $d=3$ and $d=4$ is not resolved.

Across all four observer dimensions ($d=2,3,4,5$, $n=30$ each), however,
the mean ratio decreases monotonically from $4.74$ ($d=2$) to $4.49$
($d=5$), a linear trend of slope $\approx -0.08$ per unit $d$
($p=0.003$, $R^2=0.07$). The trend is weak---it explains only $\sim 7\%$
of the seed-to-seed variance---but is statistically detectable at this
sample size, consistent with a mild "dimensional dilution" of the
directional coupling. It should not be read as evidence that any single
pair of dimensions differs.

### 4.2 Observer-Dimension Phase Diagram

To investigate the role of observer complexity, we varied the observer
dimension $d \in \{2,3,4,5\}$ while keeping $N=6$, $D=6$, and
$g_{XY}=0.8$ fixed. Each configuration was evaluated over five
independent random seeds.

   $d$   Mean Ratio            Std Dev             CV (%)    Alignment     Status
  ----- ------------ ---------------------------- -------- -------------- ---------
    2       4.74      $\pm$`<!-- -->`{=html}0.15    3.1%    100% (30/30)   Healthy
    3       4.65      $\pm$`<!-- -->`{=html}0.23    4.9%    100% (30/30)   Healthy
    4       4.61      $\pm$`<!-- -->`{=html}0.32    7.0%    100% (30/30)   Healthy
    5       4.49      $\pm$`<!-- -->`{=html}0.46   10.3%    100% (30/30)   Healthy

  : Phase diagram by observer dimension ($N=6$, $g_{XY}=0.8$)

Several features are noteworthy.

1.  **No strict threshold at $d=3$:** Contrary to our initial
    expectation, even $d=2$ produces healthy temporal emergence with
    perfect alignment. This suggests that the minimum observer
    complexity required for temporalization is lower than anticipated.

2.  **Robust emergence, with a weak downward trend in $d$:** Mean ratios
    cluster in a narrow range ($4.49$--$4.74$) across all four tested
    observer dimensions, and alignment is perfect (100%, 30/30 seeds) in
    every case. With $n=30$ seeds per dimension the mean ratio decreases
    monotonically from $4.74$ ($d=2$) to $4.49$ ($d=5$), a weak trend
    (slope $\approx -0.08$ per unit $d$, $p=0.003$, $R^2=0.07$;
    Table [1](#tab:stats){reference-type="ref" reference="tab:stats"});
    the paired comparison between $d=3$ and $d=4$ is, however, not
    significant at this sample size ($p=0.61$). We therefore report a
    mild "dimensional dilution" of the directional coupling rather than
    a robust pairwise difference, and we find no evidence for an optimal
    or "sweet spot" observer dimension in this range. (An earlier v5
    draft of this table reported a spurious $d=4$ "sweet spot" and
    reduced $d=5$ alignment; those numbers could not be reproduced from
    the corrected v6 sampler and have been replaced with freshly re-run,
    seed-logged values.)

### 4.3 Finite-Size Scaling and Parameter Sensitivity

We next tested whether the observed temporal emergence is a finite-size
artifact by varying the matrix size $N$. We first fixed $d=3$ and
$g_{XY}=0.8$ and examined $N \in \{4,5,6,7,8\}$.

   $N$   Mean Ratio            Std Dev             CV (%)   Alignment    Status
  ----- ------------ ---------------------------- -------- ------------ ---------
    4       4.63      $\pm$`<!-- -->`{=html}0.19    4.2%    100% (5/5)   Healthy
    5       4.62      $\pm$`<!-- -->`{=html}0.18    4.0%    100% (5/5)   Healthy
    6       4.75      $\pm$`<!-- -->`{=html}0.17    3.5%    100% (5/5)   Healthy
    7       4.75      $\pm$`<!-- -->`{=html}0.12    2.6%    100% (5/5)   Healthy
    8       4.72      $\pm$`<!-- -->`{=html}0.05    1.0%    100% (5/5)   Healthy

  : Finite-size scaling with fixed $g_{XY}=0.8$ ($d=3$)

To test whether this robustness is a small-$N$ accident, we extended the
scan to $N \in \{9, 10, 12, 14, 16\}$ (same $d=3$, $g_{XY}=0.8$, five
seeds each):

   $N$   Mean Ratio            Std Dev             CV (%)   Alignment    $\tau_{\mathrm{int}}$
  ----- ------------ ---------------------------- -------- ------------ -----------------------
    9       4.75      $\pm$`<!-- -->`{=html}0.10    2.0%    100% (5/5)            1.8
   10       4.77      $\pm$`<!-- -->`{=html}0.06    1.3%    100% (5/5)            2.2
   12       4.76      $\pm$`<!-- -->`{=html}0.10    2.1%    100% (5/5)            1.8
   14       4.75      $\pm$`<!-- -->`{=html}0.03    0.6%    100% (5/5)            1.6
   16       4.72      $\pm$`<!-- -->`{=html}0.07    1.6%    100% (5/5)            1.9

  : Larger-$N$ extension with fixed $g_{XY}=0.8$ ($d=3$)

The robustness extends to $N=16$: the ratio remains at
$R \approx 4.7$--$4.8$, alignment stays perfect, and the wall fraction
is zero throughout. The integrated autocorrelation time
$\tau_{\mathrm{int}} \approx 1.6$--$2.2$ (measurement sweeps) confirms
that the 30 recorded trajectory points are only weakly correlated, so
the trajectory-mean estimates are well behaved.

In contrast to an earlier v5 analysis, the corrected sampler shows **no
finite-size crossover**: the ratio remains healthy and statistically
stable across the entire tested range $N=4$--$16$.

1.  **No crossover regime:** At every tested size the mean ratio stays
    within $4.6$--$4.8$ and alignment is perfect (100%). There is no $N$
    at which fixed coupling $g_{XY}=0.8$ fails to produce
    temporalization.

2.  **CV decreases monotonically with $N$:** The coefficient of
    variation falls steadily from $4.2\%$ at $N=4$ to about $1\%$ at
    $N=8$ and remains at or below $\sim 2\%$ through $N=16$. Larger
    systems produce more tightly self-averaging measurements, consistent
    with the trajectory-mean estimator averaging over more matrix
    degrees of freedom.

The apparent crossover at $N\approx 7$ reported in v5 (ratio dropping to
$\approx 1.8$ with reduced alignment) is not reproduced here. As
documented in Section [4.5](#sec:absence_crossover){reference-type="ref"
reference="sec:absence_crossover"}, it was an artifact of the v5
`step=2` element-skip shortcut, not a feature of the model.

### 4.4 Parameter Tuning at $N=8$

To examine how the coupling strength affects the strong-coupling side of
the model, we repeated the $N=8$ simulations while varying $g_{XY}$.

   $g_{XY}$   Mean Ratio            Std Dev             CV (%)   Alignment       Status
  ---------- ------------ ---------------------------- -------- ------------ --------------
     0.80        4.72      $\pm$`<!-- -->`{=html}0.05    1.0%    100% (5/5)     Healthy
     1.05       10.09      $\pm$`<!-- -->`{=html}0.20    2.0%    100% (5/5)   Gate ceiling
     1.10       10.22      $\pm$`<!-- -->`{=html}0.04    0.4%    100% (5/5)   Gate ceiling
     1.15       10.34      $\pm$`<!-- -->`{=html}0.23    2.3%    100% (5/5)   Gate ceiling

  : Parameter tuning at $N=8$ ($d=3$)

The corrected sampler changes the picture materially. At $g_{XY}=0.80$
the system is already healthy ($R \approx 4.72$, CV $1.0\%$), so **no
parameter tuning is required at $N=8$**. For $g_{XY} \geq 1.05$ the
ratio saturates near $R \approx 10$ with CV near $1$--$2\%$; this is the
gate ceiling described in Section [3](#sec:method){reference-type="ref"
reference="sec:method"}: the aligned dimension's *extent* is driven to
just below the `max_extent`$=10.0$ cutoff (individual extents peak at
$\approx 9.99$ and never exceed $10.0$), so the dimensionless ratio
approaches $\sim 10$ while the gate penalty suppresses further growth.

Two points follow. First, the non-monotonic CV spike at $g_{XY}=1.05$
(CV $=59.0\%$) reported in v5 is not reproduced here; CV is flat and
small ($0.4$--$2.3\%$) across the scanned range. Second, $g_{XY}=0.80$
is the preferred working value at $N=8$: it produces healthy emergence
well inside the Healthy window, and increasing $g_{XY}$ beyond
$\sim 1.05$ only pins the aligned extent against the gate without
further benefit.

### 4.5 On the Absence of a Crossover Regime

Unlike our earlier v5 results (which used a final-snapshot estimator and
a `step=2` element-skip shortcut for $N>6$), the v6 trajectory-mean
results show **no evidence of a crossover or phase transition** in the
range $N=4$--$16$. The ratio remains stable at $R \approx 4.6$--$4.8$
across all tested system sizes, with alignment $100\%$ and CV
*decreasing* with $N$. This demonstrates that the apparent crossover at
$N \approx 7$---and the accompanying "two-regime scaling" with a tuned
optimal coupling $g_{XY}^{\mathrm{opt}}(N)$---was an artifact of the v5
sampling strategy, not a feature of the model.

Specifically, the v5 engine applied

        step = 2 if N > 6 else 1

which caused the X-matrices at $N=7,8$ to have only their even-indexed
elements updated, leaving the odd-indexed elements frozen near their
initial values and preventing the system from thermalizing. The
Y-matrices were not subject to this skip, so the two subsystems were
treated asymmetrically. The v6 engine removes this shortcut and updates
every element at every sweep; once the system is allowed to thermalize
fully, the finite-size "crossover" disappears and the mechanism is seen
to be robust across the entire tested range.

We therefore withdraw the earlier two-regime scaling picture and the
power-law estimate $\alpha \approx 0.46$--$1.10$ for
$g_{XY}^{\mathrm{opt}}(N)$. There is no longer a set of tuned optima
from which such an exponent could be computed: $g_{XY}=0.8$ suffices for
every $N \in \{4,5,\ldots,16\}$.

### 4.6 Physical Interpretation: Robustness and Gate Saturation

With the crossover removed, the two physically meaningful observations
are the *robustness* of temporalization across $N$ and $d$, and the
*saturation* of the aligned extent against the stability gate at strong
coupling.

1.  **Robustness across system size:** The mechanism produces a healthy
    ratio and perfect alignment at every tested size, with no required
    change in coupling. This is consistent with the coupling energy
    remaining sufficient relative to thermal fluctuations throughout
    $N \leq 8$; the decrease of CV with $N$ further indicates that
    larger systems self-average, rather than destabilizing.

2.  **Gate saturation at strong coupling:** For $g_{XY} \gtrsim 1.05$ at
    $N=8$, the aligned dimension's extent is driven to the
    stability-gate ceiling ($\approx 9.99$, just below
    `max_extent`$=10.0$). The gate penalty term
    $10.0\,(\text{extent} - 10.0)^2$ then balances the coupling, pinning
    the extent just below the cutoff. The resulting ratio approaches
    $\sim 10$ while no individual extent ever exceeds $10.0$; this is
    the gate doing its job, not a new physical phase.

3.  **Spectral mechanism (rank-1 condensation):** The directional
    coupling acts on the fourth moment $\mathrm{Tr}(X_\mu^4)$, which
    strongly favors states in which a single eigen-direction dominates.
    At $g_{XY}=0.8,\ N=8$, the selected matrix is effectively rank-1:
    one eigenvalue $\lambda_{\max}\approx 6$ with the next-largest
    eigenvalue an order of magnitude smaller
    ($\lambda_{\max}/\lambda_2 \approx 20$), whereas in the uncoupled
    baseline ($g_{XY}=0$) the spectrum remains dispersed
    ($\lambda_{\max}/\lambda_2 \lesssim 1.3$). The observed ratio
    ($4.5$--$4.7$) is therefore not an artifact of the observable: it
    signals genuine eigenvalue condensation driven by the coupling,
    separated from the $g_{XY}=0$ baseline ($1.10\pm0.05$) by well over
    fifty standard deviations.

4.  **Weak observer-dimension trend:** Mean ratio decreases gently with
    observer dimension ($4.74 \to 4.49$ from $d=2$ to $d=5$ at $n=30$),
    suggesting that additional observer degrees of freedom dilute the
    directional coupling slightly. The trend is statistically detectable
    (slope $\approx -0.08$ per unit $d$, $p=0.003$) but weak
    ($R^2=0.07$), and no single pair of dimensions differs
    significantly.

### 4.7 Connection to IKKT Matrix Model

Our model shares the mechanism of directional symmetry breaking with the
IKKT matrix model [7, 8], in which
Kim and Nishimura found that spontaneous symmetry breaking SO(9)
$\rightarrow$ SO(3) requires sufficiently large $N$ for clear emergence
of (3+1)-dimensional spacetime. We note, however, that the corrected v6
results do *not* exhibit the finite-size sensitivity that an earlier v5
analysis had suggested: within the tested range $N \leq 8$, our coupling
$g_{XY}=0.8$ produces robust emergence with no required $N$-dependent
tuning. Any comparison between the two models therefore rests on the
shared qualitative idea of competition between coupling energy and the
phase space of matrix configurations, not on a demonstrated finite-size
crossover in our model.

## 5. Discussion

### 5.1 Advantages Over External Adapter

The dynamical observer approach offers several advantages:

1.  **Physical Motivation:** Observer is dynamical system, not
    parameter.

2.  **Emergent Direction:** Temporal direction emerges from observer
    dynamics.

3.  **Robustness:** Works across $d = 2,3,4,5$ and all tested
    $N = 4$--$16$ with fixed coupling, no crossover and no required
    parameter tuning.

4.  **Measurement Theory:** Observer as measurement device.

### 5.2 Relation to Philosophical Positions

Our model is consistent with several philosophical positions within the
restricted scope of our toy model:

- **Leibniz (relational time):** Temporal direction created by observer.

- **Barbour (timeless physics) [2]:** Pre-observer state is
  symmetric.

- **Rovelli (thermal time) [9, 3]:**
  Coupling creates preferred direction.

- **Relational QM [10]:** States relative to observer.

**Important:** "Consistent with" does not mean "proves" or "validates."
These philosophical positions remain open questions.

## 6. Open Questions and Future Directions

Our results raise several important questions that warrant further
investigation:

1.  **Gate saturation mechanism:** At $N=8$ and $g_{XY} \gtrsim 1.05$
    the aligned extent saturates against the stability-gate ceiling,
    pinning the ratio near $10$. A fine scan of $g_{XY}$ in the interval
    $0.80$--$1.05$ (step $0.025$) shows the entry into saturation is a
    *smooth crossover*, not a sharp transition: the ratio rises
    monotonically from $\approx 4.7$ to $\approx 10$, with the steepest
    single step ($\Delta R \approx 1.7$) near
    $g_{XY}\approx 0.875$--$0.90$, and then flattens onto the plateau
    for $g_{XY}\gtrsim 0.95$. Whether the saturation value is a
    well-defined function of `max_extent` remains open.

2.  **Large-$N$ behavior:** The corrected sampler shows robust emergence
    with fixed coupling up to $N=16$
    (Section [4.3](#sec:fss){reference-type="ref" reference="sec:fss"},
    Table [4](#tab:fss_large_n){reference-type="ref"
    reference="tab:fss_large_n"}). Whether this robustness persists at
    still larger $N$ ($N=18, 20, \ldots$) remains open; a genuine
    finite-size crossover could still emerge beyond the currently tested
    range, and would then need to be distinguished from the v5 artifact
    described in
    Section [4.5](#sec:absence_crossover){reference-type="ref"
    reference="sec:absence_crossover"}.

3.  **Observer-dimension dependence (dimensional dilution):** With
    $n=30$ seeds per dimension, the mean ratio decreases monotonically
    from $4.74$ ($d=2$) to $4.49$ ($d=5$). The trend is statistically
    detectable (slope $\approx -0.08$ per unit $d$, $p=0.003$) but weak
    ($R^2=0.07$), and the pairwise comparison between $d=3$ and $d=4$ is
    not significant ($p=0.61$). This is consistent with a mild
    "dimensional dilution" of the directional coupling over additional
    observer directions, rather than any sharp dependence. Confirming
    the physical origin of the dilution (and the concomitant rise of CV
    with $d$, from $3.1\%$ at $d=2$ to $10.3\%$ at $d=5$) would require
    still larger samples or an analytic argument.

4.  **Universality:** Would this mechanism work with different coupling
    structures or different matrix models (e.g., BFSS, Lorentzian IKKT)?
    How universal is the observer-induced temporalization phenomenon?

5.  **Feedback coupling (back-reaction):** The present model treats the
    observer $Y$ as an external field acting on $X$ with no
    back-reaction. To move beyond this one-way picture, one could
    introduce a small back-reaction term from $X$ back to $Y$ (e.g. a
    $g_{YX}$-weighted coupling in the observer action) and ask whether
    the two-way coupled system still selects a stable temporal
    direction, or whether the mutual feedback destabilizes the ordering.
    This is a natural step toward a genuinely relational, rather than
    externally driven, notion of time.

## 7. Conclusion

We have presented a toy-level computational demonstration of temporal
emergence from a dynamical observer. Our key findings:

1.  An observer system $Y$ can dynamically create the temporal direction
    in a main system $X$ through directional coupling.

2.  With the corrected v6 trajectory-mean sampler, we observe healthy
    temporal emergence (ratios $4.4$--$4.8$, alignment $100\%$) across
    the entire tested range: observer dimensions $d \in \{2,3,4,5\}$ and
    system sizes $N \in \{4,5,\ldots,16\}$, with fixed coupling
    $g_{XY}=0.8$.

3.  No finite-size crossover or two-regime scaling is observed; the
    crossover and tuned-coupling picture reported in v5 was an artifact
    of a `step=2` sampling shortcut, now removed
    (Section [4.5](#sec:absence_crossover){reference-type="ref"
    reference="sec:absence_crossover"}).

4.  Perfect alignment ($X_{\max} = v_{\max}$) in all healthy emergence
    cases confirms the observer's active role.

5.  At strong coupling ($g_{XY} \gtrsim 1.05$, $N=8$) the aligned extent
    saturates against the stability gate, pinning the ratio near $10$;
    this is gate saturation, not a new phase.

6.  Across observer dimensions, the mean ratio decreases weakly and
    monotonically with $d$ (slope $\approx -0.08$ per unit $d$,
    $p=0.003$, $R^2=0.07$ at $n=30$); the pairwise comparison between
    $d=3$ and $d=4$ is not significant ($p=0.61$). The earlier $n=5$
    "marginally significant" result ($p=0.049$) was a small-sample
    fluctuation and has been withdrawn.

**Note on the v5 v6 correction:** An earlier version of this manuscript
(v5) reported a finite-size crossover at $N\approx 7$, a two-regime
scaling picture with a tuned optimal coupling
$g_{XY}^{\mathrm{opt}}(N)$, and a non-monotonic variance spike at
$g_{XY}=1.05$. None of these are reproduced by the corrected v6 sampler.
They were traced to a `step=2` element-skip optimization in the v5
engine, which for $N>6$ updated only even-indexed matrix elements and
prevented full thermalization. The v5 numbers have therefore been
withdrawn and replaced by the v6 trajectory-mean results reported here;
the v5 manuscript is retained unchanged as `manuscript_v5.tex` for
archival comparison.

**Appropriate Interpretation:** These results demonstrate that dynamical
observer temporalization *can be represented* in a consistent
mathematical framework. They do not prove that time emerges from
observer coupling in nature.

**Final Statement:** This work is a toy-level demonstration of
mathematical consistency, not a discovery of physical laws. Following
the philosophy of our exploratory notes, we emphasize that this is a
**design framework demonstrating mathematical consistency**, not
empirical physics.
---

## References

[1] Page, Don N. & Wootters, William K. (1983). Evolution without evolution: Dynamics described by stationary observables. *Physical Review D*, 27, 2885--2892. [doi:10.1103/PhysRevD.27.2885](https://doi.org/10.1103/PhysRevD.27.2885)

[2] Barbour, Julian (1999). The End of Time. *Oxford University Press*.

[3] Rovelli, Carlo (2018). The Order of Time. *Riverhead Books*.

[4] Chanpengpad, Sutipong (2026). Structural Time Framework. *Zenodo*. [doi:10.5281/zenodo.21763905](https://doi.org/10.5281/zenodo.21763905)

[5] Chanpengpad, Sutipong (2026). SGOED: An Atemporal Matrix Formalism for Stability-Gated Crystallization and Aggregation (Phase 1-2). *Zenodo*. [doi:10.5281/zenodo.21786260](https://doi.org/10.5281/zenodo.21786260)

[6] Metropolis, Nicholas, Rosenbluth, Arianna W. & others (1953). Equation of state calculations by fast computing machines. *Journal of Chemical Physics*, 21, 1087--1092. [doi:10.1063/1.1699114](https://doi.org/10.1063/1.1699114)

[7] Kim, Sang-Woo, Nishimura, Jun & Tsuchiya, Asato (2012). Expanding (3+1)-dimensional universe from a Lorentzian matrix model for superstring theory in (9+1) dimensions. *Physical Review Letters*, 108, 011601. [doi:10.1103/PhysRevLett.108.011601](https://doi.org/10.1103/PhysRevLett.108.011601)

[8] Kim, Sang-Woo, Nishimura, Jun & Tsuchiya, Asato (2012). Late time behaviors of the expanding universe in the IIB matrix model. *Journal of High Energy Physics*, 2012, 147. [doi:10.1007/JHEP10(2012)147](https://doi.org/10.1007/JHEP10(2012)147)

[9] Connes, Alain & Rovelli, Carlo (1994). Von Neumann algebra automorphisms and time-thermodynamics relation. *Classical and Quantum Gravity*, 11, 2899--2918. [doi:10.1088/0264-9381/11/12/007](https://doi.org/10.1088/0264-9381/11/12/007)

[10] Rovelli, Carlo (1996). Relational quantum mechanics. *International Journal of Theoretical Physics*, 35, 1637--1678. [doi:10.1007/BF02302261](https://doi.org/10.1007/BF02302261)
