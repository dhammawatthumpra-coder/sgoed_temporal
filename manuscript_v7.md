# The Arrow of Time Is Not in the Ensemble
## An Audited Toy-Model Quest across Equilibrium Matrices, Sequential Growth, and Causal Sets (SGOED V7)

**Author:** Sutipong Chanpengpad
*Independent Researcher, Chiang Rai, Thailand*
Email: `dhammawatthumpra@gmail.com`
ORCID: [0009-0001-4069-8576](https://orcid.org/0009-0001-4069-8576)

**Date:** September 2026

---

## Abstract

We ask a focused question in a toy universe of coupled matrix/graph/causal-set models: can the arrow of time arise from the *final equilibrium state* of a relational structure, however it is coupled? Using a disciplined audit (reproduce, significance, null test, labeling test, thermalization check, mechanism — seed counts stated per result, $\ge 10$ wherever per-seed scatter is non-trivial), we demonstrate that it cannot: **eleven structural observables** (asymmetry ratio, sign counts, Myrheim–Meyer dimension, spectral dimension, cycle ratio, time-reversal, order statistics, eigenvalue repulsion, entropy rate, …) are all time-symmetric or null-compatible at equilibrium Monte Carlo. In contrast, three *process-based* constructions produce robust directional time:

1. **Past Hypothesis** — a low-entropy (rank-1) initial state relaxes with $dS/S_0 = 0.98$, roughly $100\times$ the relaxation of a random initial state.
2. **Sequential growth** (Rideout–Sorkin style) — birth order with frozen past yields chain inheritance $1.000\pm0.000$, deterministic and scale-free ($M=16,32$); the mechanism is a contraction map induced by alignment to the past-mean direction (prefix-sum coupling).
3. **Non-equilibrium upwind transport** — a directed source→sink flow produces a $5000\times$–$6000\times$ extent decay with current $J\approx +5.77\pm0.02$ (8 seeds), reversal-symmetric ($-6.03$) and null-discriminating ($J\approx 0$).

We then audit the "emergent 4D" question that drove the project's excitement into a dead end. Euclidean IKKT-like actions at $D=4,10$ are perfectly isotropic without an engineered steering vector $\hat v$; a pseudo-Euclidean signature produces a stable $1{+}3$ split only as an engineered $\eta$ (spatial isotropy $10^{-3}$); Lorentzian real-time bosonic dynamics is unbounded below (the regulator in the literature is the fermion determinant); random-percolation causal sets give "$d\approx4$" only as a **finite-size artifact of $N=250$** that fails a scale audit to $N=1000$ under both fixed-$p$ and fixed-$k$ scalings; and spectral dimension measured on flow networks tracks drift/transience rather than geometry. The one structural discovery is that a **relational light-cone law** (matrix-distance $\le c\,\Delta t$ plus direction alignment) makes the causal dimension *scale-invariant* ($\mathrm{std}$ across $N$ of $0.002$–$0.01$, versus $0.26$–$0.82$ for percolation) — a necessary condition for a dimensionful causal set — although the absolute dimension remains parameter-controlled (diffusion/light-speed aspect), i.e., engineered.

**Bottom line:** at toy scale, the arrow of time lives in the *process* (initial condition or asymmetric construction), not in the equilibrium ensemble; and 4D does not emerge spontaneously in any of the audited frameworks. The audit itself — a six-step verification protocol and a trap catalog — is the project's transferable contribution, shipped as a runnable toolbox (`code/audit_gates.py`, Supplement A) with the full v8–v14 evidence slice (`audit_evidence/`).

**Keywords:** arrow of time, matrix models, sequential growth, causal sets, spectral dimension, Monte Carlo audit, past hypothesis

**Important Caveats:** toy-level demonstration with small sizes ($N\le 1000$ events, matrices $N\le 8$). "Real time" here means *robust directional asymmetry in a specified observable*, reproduced deterministically across seeds — not a claim about fundamental physics.

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Models and Observables](#2-models-and-observables)
  - [2.1 The matrix unit (v7 core)](#21-the-matrix-unit-v7-core)
  - [2.2 Growth, transport, and posets](#22-growth-transport-and-posets)
  - [2.3 Observables](#23-observables)
- [3. The Six-Step Audit](#3-the-six-step-audit)
- [4. Results](#4-results)
  - [4.1 Equilibrium is time-symmetric](#41-equilibrium-is-time-symmetric)
  - [4.2 Route 1: Past Hypothesis](#42-route-1-past-hypothesis)
  - [4.3 Route 2: Sequential growth and its mechanism](#43-route-2-sequential-growth-and-its-mechanism)
  - [4.4 Route 3: Non-equilibrium upwind transport](#44-route-3-non-equilibrium-upwind-transport)
  - [4.5 The 4D question: matrix spontaneous symmetry breaking](#45-the-4d-question-matrix-spontaneous-symmetry-breaking)
  - [4.6 Causal-set dimensions: percolation negative, light-cone invariance](#46-causal-set-dimensions-percolation-negative-light-cone-invariance)
  - [4.7 Spectral dimension on flow networks](#47-spectral-dimension-on-flow-networks)
- [5. Discussion](#5-discussion)
- [6. Conclusion](#6-conclusion)
- [Appendix A: Reproducibility](#appendix-a-reproducibility)
- [Appendix B: Trap Catalog](#appendix-b-trap-catalog)
- [References](#references)

---

## 1. Introduction

The question of where the arrow of time comes from has been posed across philosophy [[1](#ref-1), [9](#ref-9), [10](#ref-10)], thermodynamics, and relational physics [[2](#ref-2), [5](#ref-5)]. Our working hypothesis, following the Structural Time Framework [[6](#ref-6)] and its SGOED implementation [[7](#ref-7)], is relational: time might emerge from the *structure* of a pre-temporal system rather than being inserted as a parameter.

The project evolved through many constructions — matrix models with an observer system [[7](#ref-7)], graphs, hypergraphs, ecosystems, hybrids — and each produced metrics that "looked directional." Exactly eleven of them collapsed under scrutiny: they were histogram artifacts, labeling-dependent, null-compatible, or thermalization-limited. Two conclusions emerged as robust:

1. **Equilibrium Monte Carlo is time-symmetric.** No coupling of an equilibrium ensemble produces an arrow from the final state.
2. **The arrow requires process:** either a special initial condition (past hypothesis) or a construction whose updates are asymmetric by design (birth order, directed transport).

This manuscript reports the audited results of that quest, plus the systematic audit of the "emergent 4D" question that followed, and the one structural discovery it produced: relational light-cone locality as the condition for *scale-invariant* causal dimension.

> **Important Disclaimer:** A toy-level computational exploration with small sizes. "Time" below means *robust, reproducible directional asymmetry of an observable along a constructed axis*, not a claim about fundamental physics. Everything reported is reproduced from public scripts (Appendix [A](#appendix-a-reproducibility)).

---

## 2. Models and Observables

### 2.1 The matrix unit (v7 core)

A unit holds real symmetric matrices $X = (X^1,\dots,X^D)$ of size $N\times N$ ("system") and $Y = (Y^1,\dots,Y^d)$ ("observer"). The local action $S_X + S_Y + S_{\mathrm{coup}}$ (all terms of the IKKT-like family [[15](#ref-15)] with stability gates) is

$$S = \sum_{\mu<\nu}\mathrm{Tr}([X_\mu,X_\nu][X_\mu,X_\nu]^T) + \sum_\mu \lambda\big(\mathrm{Tr}(X_\mu^2)-Nr_0^2\big)^2 \ -\ g_{XY}\sum_\mu \hat v_\mu^2\,\mathrm{Tr}(X_\mu^4),$$

where $\hat v = \mathrm{normalize}(\mathrm{Tr}(Y^1),\dots,\mathrm{Tr}(Y^d))$ is the observer direction. The coupling $-\hat v_\mu^2\mathrm{Tr}(X_\mu^4)$ drives exactly the dimension(s) aligned with $\hat v$ to large extent $\mathrm{Tr}(X_\mu^2)/N$ — a *discrete* winner-take-all choice among $D$ dimensions (condensation ratio $\lambda_{\max}/\lambda_{2\mathrm{nd}}\approx 23$, $\sim 60\sigma$ over baseline [[7](#ref-7)]), with first-order bistability/hysteresis (audited scripts `AUDIT_v7_hysteresis*` in `audit_evidence/`; see also the v6 preprint). This mechanism is the reproducible core of the project; it picks *a* direction but does not create *flow*.

### 2.2 Growth, transport, and posets

Three process constructions were added on top of the unit:

- **Sequential growth (CSG-style [[11](#ref-11)]):** units are born one at a time; past units are frozen; the newborn thermalizes against the frozen past with coupling $S_{\mathrm{inter}} = -g\,\hat v_u\cdot \big(\sum_{j<u}\hat v_j\big)$ (prefix-sum — an exact $O(1)$ reformulation of pairwise alignment).
- **Upwind transport (Langevin, non-MC):** $M$ units on a chain; a drive pumps unit $0$, a sink absorbs at unit $M-1$, and the coupling transfers extent only forward ($F_u \propto g_t X_{u-1} - g_t X_u$); updates are overdamped Langevin with temperature $T$.
- **Causal sets / posets** [[12](#ref-12)]: relations between births are defined either probabilistically (Bernoulli links + transitive closure), or geometrically from matrix state — unit $u\prec k$ iff $|\hat v_u\cdot \hat v_k|>\theta$ **and** $D_{\mathrm{space}}(u,k)\le (c\,\Delta t)^2$ with $D_{\mathrm{space}} = \frac{1}{N}\mathrm{Tr}((X_u-X_k)^2)$ (**relational light-cone law**).

### 2.3 Observables

Directionality metrics: extent ratio $R=\mathrm{ext}(X_{\max})/\overline{\mathrm{ext}}(X_{\neq\max})$; sign-count $D$; relational dimension via relation fraction $\rho = C/\binom{N}{2}$ calibrated against synthetic Minkowski sprinklings ($d=1..8$, per-$N$ recalibration to cancel finite-size box effects; estimator after Myrheim [[13](#ref-13)]); spectral dimension $d_s = -2\,d\ln P/d\ln t$ from the return probability $P(t)=\mathrm{Tr}(T^t)/N$ of the (lazy) random walk; current $J = \overline{\mathrm{ext}}_{u} - \overline{\mathrm{ext}}_{u+1}$; entropies and counts thereof.

---

## 3. The Six-Step Audit

Every observable in this project is passed through six gates before being reported. The gates, with their pass criteria (implemented as a runnable toolbox, `code/audit_gates.py`, Supplement A):

| gate | pass criterion |
|---|---|
| 1. Reproduce | identical numbers on re-run (same seed, to machine precision) |
| 2. Significance | $\ge 10$ seeds; mean and std stabilize (5 seeds are not enough — a $2.3\sigma$ effect fell to $1.2\sigma$ in an earlier branch [[7](#ref-7)]) |
| 3. Null test | the effect separates from shuffle/baseline (≳ $3\sigma$ over the null spread) |
| 4. Labeling/permutation | the metric is invariant under relabeling of nodes |
| 5. Thermalization | the observable plateaus once $n_{\mathrm{therm}}$ is sufficient (this gate alone reversed two conclusions in this project — Section [4.3](#43-route-2-sequential-growth-and-its-mechanism), [4.2](#42-route-1-past-hypothesis)) |
| 6. Mechanism | a stated explanation of *why*, backed by the measured evidence |

*Seed-count note.* The table's "$\ge 10$ seeds" criterion applies to observables whose per-seed scatter is non-trivial (every dimension estimate and every null/labeling control here used $10$–$12$ seeds). The three deterministic routes report fewer seeds *because their scatter is negligible by construction*: sequential growth inherits the past mean deterministically (origin alignment $0.9995\pm0.0002$ std over 6 seeds, chain $0.9991\pm0.0002$), and the upwind transport current is $J=+5.773\pm0.016$ over 8 seeds ($\sim0.3\%$). For such nearly-deterministic observables, additional seeds only confirm the mean; we state the actual counts per result in Appendix [A](#appendix-a-reproducibility) rather than claiming a uniform $10$.

Appendix [B](#appendix-b-trap-catalog) lists the concrete failure modes this process caught.

---

## 4. Results

### 4.1 Equilibrium is time-symmetric

In equilibrium Metropolis sampling [[8](#ref-8)], no final-state observable distinguishes a direction of time. Eleven observables were attempted across matrix, graph, hypergraph, and ecosystem variants: extent ratio $R$, sign-count $D$, relational dimension $d_{\mathrm{MM}}$, spectral dimension $d_s$, graph asymmetry $G$, cycle ratio, time-reversal statistic, order statistics, eigenvalue repulsion, dynamic order, and entropy rate. Their failures are catalogued in Appendix [B](#appendix-b-trap-catalog) (e.g., $R\approx0.5$ is a histogram artifact; $D$ is labeling-dependent, ranging $[-98,+28]$ under node permutations; $d_{\mathrm{MM}}$ and $d_s$ are null-compatible with random graphs). The two genuinely asymmetric phases — eigenvalue condensation (discrete $\mu$ choice) and inter-unit clock synchronization (alignment $1.000\pm0.001$, null-passed) — are real but *static*: they fix a direction in space, not in time.

### 4.2 Route 1: Past Hypothesis

Following the Boltzmann/Albert past-hypothesis program [[16](#ref-16)]: a special low-entropy initial state relaxes toward equilibrium, and the arrow is the measure of that relaxation. In the v7 matrix unit ($N=4$, $g_{XY}=0$, 3 seeds):

| initial state | $dS/S_0$ | total $dS$ |
|---|---|---|
| random | 0.29 | 3 |
| **rank-1 (low entropy)** | **0.98** | **337** |

The rank-1 initial condition relaxes $\sim100\times$ more entropy than a random one, deterministically and monotonically ($S$: $344\to7$). *Mechanism:* low-entropy states have more relaxation capacity; the arrow's strength is inherited from the initial condition, not from the dynamics.

### 4.3 Route 2: Sequential growth and its mechanism

**Result.** Units born one-by-one with frozen past (coupling $g=20$, adequate thermalization) show:

| $M$ | chain inheritance | origin alignment |
|---|---|---|
| 8 | $1.000 \pm 0.000$ | $1.000$ |
| 16 | $0.998$ | $0.998$ |
| 32 | $0.998$ | $0.998$ |

Deterministic across seeds (identical statistics). **Mechanism (why 1.000):** the inter-coupling aligns each newborn to the *mean direction of all past units*; the past-mean is a contraction fixed point. Measured contraction of late units to the past mean: $0.03$ at $g=20$, $0.02$ at $g=60$. The alignment is partial at weak coupling (chain $0.43$ at $g=1$) and saturates at strong coupling — a clean coupling-strength phase structure. **Scale-free** from $M=8$ to $M=32$.

**Thermalization gate.** This route initially failed a reproduction at short thermalization ($n_{\mathrm{therm}}=30$): drift appeared and inheritance dropped. At $n_{\mathrm{therm}}=100$ the drift vanished — a thermalization artifact, not physics.

**Past hypothesis + growth.** The handoff reported a failed attempt to seed the origin with a special state. The correct fix combines: (a) a rank-1 origin ($Y^1_0=2I$ so $\hat v_0=(1,0)$), (b) frozen origin, (c) sufficient thermalization ($n_{\mathrm{therm}}=120$). With the origin untrained the earlier failure was *thermalization insufficiency*, not origin thermalization: at $n_{\mathrm{therm}}=60$ origin alignment was $0.68\pm0.45$ (one of six seeds unconverged); at $120$ it is **$0.9995\pm0.0002$** with chain $0.9991\pm0.0002$ (6 seeds). A random-origin control gives $0.90\pm0.10$ — the special initial condition genuinely determines the propagated direction. Route 2 thus realizes the past-hypothesis arrow *within* a growth process.

### 4.4 Route 3: Non-equilibrium upwind transport

Overdamped Langevin on a chain of $M=6$ units with upwind transfer, pump at unit 0, sink at unit $M-1$ (parameters: $g_{\mathrm{drive}}=5$, $g_{\mathrm{trans}}=1.2$, $g_{\mathrm{sink}}=3$, $T=0.02$):

| setup | extent profile $E_0..E_5$ | current $J$ |
|---|---|---|
| **REAL (pump@0)** | $[28.8,\,1.72,\,0.117,\,0.0247,\,0.020,\,0.005]$ | **$+5.773\pm0.016$** |
| REVERSED (pump@5) | $\sim[0.02,\dots,30.1]$ | $-6.025\pm0.022$ |
| NULL (no pump) | flat $\sim0.1$ | $+0.003\pm0.008$ |

- **Decay $5849\times$** ($=28.8/0.005$; robust audit, 8 seeds $\times$ 500 steps), dramatically larger than any equilibrium asymmetry.
- **Deterministic:** current std is $0.016$ over 8 seeds ($\sim0.3\%$).
- **Reversal-symmetric:** pumping at the far end mirrors the profile and flips the current sign — the asymmetry follows the pump, not a latent bias.
- **Null-discriminating:** without a pump the profile is flat and $J\approx0$.
- **Parameter family:** scanning $g_{\mathrm{trans}}\times g_{\mathrm{sink}}$ over a $3\times3$ grid keeps $J\in[+5.4,+5.9]$ and decay $1850$–$4000\times$, always monotone in the mean.

*Caveat:* the mean profile is strictly monotone, but per-seed profiles occasionally violate monotonicity at the thermal floor ($\sim0.02$, three orders below $E_0$) — "monotone in practice", with the residual explained as noise, consistently with the thermal floor.

### 4.5 The 4D question: matrix spontaneous symmetry breaking

Motivated by the Lorentzian IKKT programs [[3](#ref-3), [4](#ref-4), [15](#ref-15)], we asked whether the matrix unit itself can spontaneously pick a $1{+}3$ split at $D=4$ (and $1{+}9$ at $D=10$) *without* the engineered steering $\hat v$. All four probes were audited at $\ge 10$ seeds:

1. **Equilibrium, no steering ($g=0$ or symmetric driver):** perfectly isotropic at $D=4$ ($R=1.06\pm0.03$) and $D=10$ ($R=1.07\pm0.02$). The "direction choice" of the v7 action is entirely $\hat v$-engineered (the D=2 control reads $R=4.43\pm0.16$, matching the documented value).
2. **Pseudo-Euclidean signature** ($\eta=\mathrm{diag}(-1,+1,\dots)$, so space–space commutators enter with opposite sign): a stable $1{+}3$ split appears at $D=4$ — time extent $3.5$, three space extents $9.996$ each with **spatial isotropy $0.000$** across 10 seeds — but the split is the signature, not the dynamics, and *time contracts* (extents below the space block). At $D=10$ all nine space dimensions expand (no "3").
3. **Real-time dynamics (growing clock $T$):** the pure-bosonic Lorentzian action is unbounded below — extents run away ($2000$–$8700$) with no equilibrium (drift $0.13$–$0.15$). This mirrors the known fact that Lorentzian IKKT requires the fermion determinant as regulator [[3](#ref-3), [4](#ref-4)]; a CPU toy without it has no controlled configuration space.
4. **Bounded (saturating) noncommutativity** $-\sum_{i<j} g\frac{x_{ij}}{1+x_{ij}}$, $x=\|\mathrm{comm}\|^2$: equilibrium exists and is perfectly symmetric ($\mathrm{top3}$-gap $1.06\pm0.01$); a hard-wired 3-of-9 asymmetry is detectable in this regime ($1.14$) — so the negative is a *testable* negative. No $k$-of-9 selection occurs.

**Conclusion:** no configuration without $\hat v$ (or a signature choice) breaks SO($D$) at toy scale; the only "1+3" obtainable is engineered. Consistent with the known physics: Euclidean IKKT does not dimensionally reduce [[15](#ref-15)].

### 4.6 Causal-set dimensions: percolation negative, light-cone invariance

**Calibration.** The relation-fraction estimator $\rho \to d$ was calibrated on known posets per $N$: chain ($d{=}1$), Minkowski sprinklings $d{=}2..8$ ($\rho(2){=}0.25$, $\rho(4){=}0.086$, $\rho(8){=}0.011$), stable across $N{=}250,500,1000$.

**Sequential-growth poset.** The real growth output (relation $|\hat v_u\cdot\hat v_k|>0.9$) is a total order: **$d_{\mathrm{MM}}=1.00\pm0.00$** at $M=8,16$. Birth-order-only time is exactly 1-dimensional; there is no spatial structure in the current states ($\mathrm{Tr}((X_u-X_k)^2)$ is nearly constant across pairs).

**Random percolation is a finite-size artifact.** Bernoulli($p$) links plus transitive closure at $N=250$ produced a promising-looking "$d\approx4$" at $p=0.016$ ($d=4.42$). The scale audit destroys it:

| scaling (N=250/500/1000) | d_MM |
|---|---|
| fixed $p=0.02$ | 3.40 / 1.86 / **1.51** |
| fixed $k=pN=5$ | 3.40 / 4.48 / **5.35** |

No scaling invariance in either variable (std across $N$: $0.26$–$0.82$). *Mechanism:* the closure of a random DAG at large $N$ degenerates to a near-total-order (fixed $p$) or has $\rho$ scaling differently from the calibration sprinklings (fixed $k$). Per the pre-registered acceptance criteria this is recorded as a definitive negative for random percolation as a model of 4D causal sets.

**The relational light-cone law is scale-invariant — a structural discovery.** Replacing random links by the matrix-driven rule ($|\hat v_u\cdot\hat v_k|>\theta$ and $D_{\mathrm{space}}\le(c\Delta t)^2$, with birth-time rescaled to a fixed cosmic interval) yields causal dimension **invariant across $N$**:

| construction | $d_{\mathrm{MM}}$ (N=250/500/1000) | std across N |
|---|---|---|
| percolation (worst case) | 1.5–5.4 | **0.26–0.82** |
| **light-cone walk (d_sp=1)** | 1.17/1.17/1.17 | **0.002** |
| light-cone walk (d_sp=3) | 1.21/1.21/1.21 | 0.002 |
| uniform scatter, cone | 1.29/1.29/1.29 | 0.00 |

The std across $N$ drops by two orders of magnitude relative to percolation. **Locality (a light-cone) is the condition that makes causal dimension a stable property** — this is the positive content of the route. However, the absolute dimension is a monotone function of the spatial-diffusion and light-speed parameters ($\sigma$, $c$); c-scans reach $d=2$ (uniform, $d_{\mathrm{spatial}}=1$, $c=0.2$) and cross $d=4$ (3-torus walk, $c\approx0.1$–$0.2$). The dimension is parameter-controlled — again engineered, not emergent — but now *stably* so.

**Commutator-compatibility metric on real growth states — invariance without engineered coordinates.** Replacing the state difference by the commutator distance

$$D_{\mathrm{comp}}(u,k)=\frac{1}{d_{\mathrm{sp}}N}\sum_a \big|\mathrm{Tr}\big([X^a_u,X^a_k]^2\big)\big|$$

with the same cone rule, alignment threshold and transitive closure, uses states generated *directly by the sequential growth model* — no torus embedding, no spatial parameter inserted:

| construction (real states) | $d_{\mathrm{MM}}$ (N=250/500/1000) | std across N |
|---|---|---|
| commutator, $f=0.5$ ($\theta=0.7$–$0.9$) | 3.51 / 3.52 / 3.50 | **0.008** |
| commutator, $f=1.0$ | 1.89 / 1.89 / 1.90 | 0.004 |

The relation fraction is scale-invariant (5–8 seeds) and insensitive to the observer-alignment threshold $\theta$ (adjacent alignment is $1.000$ in the growth cascade, so the threshold is inert). The underlying states are near-independent, yet the commutator distance is bimodal (roughly half of the pairs nearly commute) and separation-independent; combined with the fixed-interval birth-time rescaling, this yields an $N$-independent relation fraction. **Epistemic boundary (stated plainly):** scaling invariance — the stability of the geometry — is real; the dimension *value* remains parameter-steered ($d\approx3.5$ at $f=0.5$ arises from our state-scale self-calibration of the light speed, $c_{\mathrm{ref}}=\sqrt{\overline{D}_{\mathrm{comp}}}/5$; $f=1.0$ gives $1.9$). Spontaneous dimensional selection is absent in every construction tested in this work.

### 4.7 Spectral dimension on flow networks

On a chain (64 nodes), the symmetric random walk gives the clean $d_s\approx0.8$–$0.9$ plateau (dimension 1); a biased walk (flow) first raises $d_s$ (drift) and then collapses it to $\approx0$ as the finite chain reaches stationarity ($P(t)\to$ constant). On a 3-ary tree: undirected gives a plateau rising toward the Bethe-lattice value ($\approx2$–$3$ at our depth); *pure outward flow* (transient walk) gives return probability $P(t)\to0$ and **$d_s$ diverges** ($14\to70\to278\to1110$). Verdict: on a flow network $d_s$ measures drift/transience, not geometry; spectral dimension is only well-defined on symmetric (equilibrium) structures — unlike the plateau claims of causal-dynamical-triangulation programs [[14](#ref-14)], which evaluate $d_s$ on equilibrium geometries. This closes the "$4$D via $d_s$" hope with a mechanism (and re-derives the earlier null-compatibility of $d_s$ in causal sets). *Technical note:* chains/trees are bipartite, so the raw return probability vanishes on odd $t$; the lazy walk ($T\to\frac12(I+T)$) is required before any log-derivative estimate (a documented trap, Appendix [B](#appendix-b-trap-catalog)).

---

## 5. Discussion

**Engineered $\ne$ emergence.** Every positive result here is a *construction* whose asymmetry is inserted: a special initial state, an asymmetric birth order, a directed transport term, a signature, or a diffusion/light-speed parameter. The audit's value is precisely that it forces this distinction — eleven metrics that felt like emergence were shown to be artifacts or null-compatible.

**What the quest established.** (i) Equilibrium ensembles of this toy family cannot host an arrow; (ii) process-based constructions can, deterministically, and their mechanism is understandable (relaxation capacity; contraction to the past mean; directed transport); (iii) the "4D" target is not reachable at toy scale by any equilibrium or random construction we tested, and the specific reason in each case matches known physics (no fermion regulator; no metric; no seed concentration); (iv) **relational light-cone locality is the discovered necessary condition for scale-invariant causal dimension** — a falsifiable, transferable structural claim; (v) thermalization sufficiency is the single most dangerous gate (it reversed two conclusions here, and one earlier v5→v6 correction [[7](#ref-7)]).

**Limits.** $N\le8$ matrices, $\le1000$ events, single-machine seeds; the light-cone law's dimension parameterization was not optimized beyond the scans shown; no fermion-like term was ever included; the "3" of the physical dimensional reduction remains unexplained by any toy here (it requires the phase/fermionic machinery of the Lorentzian programs [[3](#ref-3), [4](#ref-4)]).

**What an emergent theory would need (candidate directions).** A regulated (bounded) noncommutativity that *prefers* a subset of pairs; or a growth law whose spatial structure is dynamical rather than parameterized; both would be immediately testable by the same six-step audit, with $N\to1000$ scale invariance as the acceptance gate.

---

## 6. Conclusion

In the SGOED toy universe: the arrow of time is not in the equilibrium ensemble — it enters through the initial condition or through asymmetric process rules, reproducibly and deterministically (past hypothesis $dS/S_0=0.98$; growth inheritance $1.000\pm0.000$ via contraction to the past mean; upwind transport decay $>5000\times$, $J=+5.77\pm0.02$, reversal- and null-audited). The 4D question, pursued across matrix, bounded, dynamical, percolation, and spectral frameworks, yields a consistent negative — with one structural discovery (light-cone locality → scale-invariant causal dimension) and one methodological deliverable (the six-step audit + trap catalog) that transfers to any future attempt.

---

## Appendix A: Reproducibility

All scripts run on CPU with fixed seeds; results JSONs saved alongside. Key parameters:

- v7 unit: $N\le8$, $D=2$, coupling $g_{XY}=0.8$, gates $\lambda=1$, `max_extent=10`.
- Past hypothesis: `step_past_hypothesis.py` ($N=4$, 3 seeds).
- Sequential growth: `step_sequential_growth.py` ($M=8..32$, $g_{\mathrm{inter}}=20$, $n_{\mathrm{therm}}=100$); mechanism: `step_growth_mechanism.py`; past-hypothesis variant: `step_growth_past_hypothesis.py` ($n_{\mathrm{therm}}=120$).
- Transport: `step_langevin_transport_tuned.py` + `step_transport_robust.py` (8 seeds $\times$ 500 steps; scan $g_{\mathrm{trans}}\times g_{\mathrm{sink}}$).
- 4D probes: `sgoed_matrix_v15.py`, `step_v15_dynamical.py`, `step_v15_bounded.py`.
- Causal sets: `step_causal_set_dmm.py`, `step_causal_set_scale_study.py` (bitset transitive closure; per-$N$ calibration), `step_growth_lightcone.py`, `step_lightcone_followup.py`.
- Spectral dimension: `step_spectral_dimension_flow.py` (lazy walk).
- Audit toolbox (Supplement A): `code/audit_gates.py` — six gates as reusable functions, with a self-test that demonstrates each trap class. The negative-evidence slice behind Sections 3/4.1/Appendix B ships in `audit_evidence/` (v8–v14 cores, audit scripts, results) and `notes/SGOED_v8..v14_notes.md`. The bistability/hysteresis claim of Section 2.1 is backed by `audit_evidence/code/AUDIT_v7_hysteresis.py` + its result JSON.
- **Self-tuning variants audited:** degree-feedback (SOC-style, `code/step_growth_soc.py`) fails the scale-invariance gate outright in all 7 configs (std across $N$ of 0.25–1.09); curvature-feedback (`c_eff`, `code/step_growth_ceff.py`) fails outright in 2 of 12 configs (std 0.45–0.48), while its 9 remaining non-control runs sit pinned at the calibration ceiling ($d=8.00$, std $=0$ — a boundary artifact, 5 of them yielding NaN $c_{\mathrm{eff}}$ statistics — not genuine invariance); only the static-cone control passes genuinely (std 0.006). Per-config results: `results/step_growth_soc_results.json`, `results/step_growth_ceff_results.json`; full record in the living summary (updates 13–14).

Seeds: $\{42,\dots,53\}$ (≥10 for fine grids; ≥6 elsewhere, as reported). Detailed reproducibility notes and the full results chain (updates 1–17) in `matrix/SGOED_TIME_EMERGENCE_SUMMARY.md`; project context in `SGOED_PROJECT_SUMMARY.md`.

## Appendix B: Trap Catalog

Every metric that "looked exciting" in this project failed exactly one of the gates below. The catalog is supplied as a structured eight-trap table below plus a runnable toolbox (`code/audit_gates.py`, Supplement A); the full **12**-trap catalog and an eight-step auditing workflow ship as Supplement B (`SUPPLEMENT_B_AUDIT_HANDBOOK.md`); the v8–v14 scripts and results backing each row ship in `audit_evidence/`.

| # | trap | symptom | gate that caught it | fix / lesson |
|---|---|---|---|---|
| 1 | Histogram artifact | $R\approx0.5$ from symmetric graphs; shuffling the values preserves it | 3. Null | never report $R$ alone; always compare to shuffle |
| 2 | Labeling dependence | sign-count $D$ ranges $[-98,+28]$ under node permutations | 4. Labeling | use permutation-invariant metrics |
| 3 | Null-compatible dimension | $d_{\mathrm{MM}}$, $d_s$ on symmetrized graphs match random baselines | 3. Null | calibrate any dimension estimator on known posets first |
| 4 | Thermalization insufficiency | two reversals: v5's `step=2` sampler; past-hypothesis growth at $n_{\mathrm{therm}}=60$ | 5. Thermalization | verify the observable plateaus at the reported $n_{\mathrm{therm}}$ |
| 5 | Finite-size "4D" | $d\approx4$ at $N=250$ evaporates at $N=1000$ | 2. + 3. Significance/Null | run the scale audit to $N\ge1000$ before any dimension claim |
| 6 | Bipartite parity | return-probability $d_s$ vanishes on odd $t$; without the lazy walk $d_s$ oscillates by $\pm10^3$ | 5. Thermalization | use the lazy walk $T\to\frac12(I+T)$ |
| 7 | Integer overflow / closure collapse | `int8` relation-matrix matmul overflows for $N>15$; pure-squaring closure (no union) collapses to zero — silent garbage | 1. Reproduce (self-test) | `int64` arithmetic; $R\leftarrow R\vee R^2$ |
| 8 | Normalization scale | matrix-encoded distances normalized by $1/(KN)$ compress the effective light speed, zeroing the dimension readout at $c=1$ | 3. Null / calibration | unit-match (aspect calibrate) to the estimator's convention |

The transferable lesson of the whole quest: **a metric is a hypothesis about an observable, and each gate above is a way it can be falsified.**

## References

<a id="ref-1"></a>[1] Page, D. N., & Wootters, W. K. (1983). Evolution without evolution: Dynamics described by stationary observables. *Physical Review D*, 27(12), 2885–2892.

<a id="ref-2"></a>[2] Connes, A., & Rovelli, C. (1994). Von Neumann algebra automorphisms and time-thermodynamics relation. *Classical and Quantum Gravity*, 11(12), 2899–2918.

<a id="ref-3"></a>[3] Kim, S.-W., Nishimura, J., & Tsuchiya, A. (2012). Expanding (3+1)-dimensional universe from a Lorentzian matrix model for superstring theory in (9+1) dimensions. *Physical Review Letters*, 108(1), 011601.

<a id="ref-4"></a>[4] Kim, S.-W., Nishimura, J., & Tsuchiya, A. (2012). Late time behaviors of the expanding universe in the IIB matrix model. *Journal of High Energy Physics*, 2012(10), 147.

<a id="ref-5"></a>[5] Rovelli, C. (1996). Relational quantum mechanics. *International Journal of Theoretical Physics*, 35(8), 1637–1678.

<a id="ref-6"></a>[6] Chanpengpad, S. (2026). *Structural Time Framework*. Zenodo.

<a id="ref-7"></a>[7] Chanpengpad, S. (2026). *SGOED: An Atemporal Matrix Formalism for Stability-Gated Crystallization and Aggregation (Phase 1–2)*. Zenodo. [doi:10.5281/zenodo.21786260](https://doi.org/10.5281/zenodo.21786260)

<a id="ref-8"></a>[8] Metropolis, N., et al. (1953). Equation of state calculations by fast computing machines. *Journal of Chemical Physics*, 21(6), 1087–1092.

<a id="ref-9"></a>[9] Barbour, J. (1999). *The End of Time*. Oxford University Press.

<a id="ref-10"></a>[10] Rovelli, C. (2018). *The Order of Time*. Riverhead Books.

<a id="ref-11"></a>[11] Rideout, D. P., & Sorkin, R. D. (2000). Classical sequential growth dynamics for causal sets. *Physical Review D*, 61(2), 024002.

<a id="ref-12"></a>[12] Sorkin, R. D. (2005). Causal sets: Discrete gravity. In *Lectures on Quantum Gravity* (pp. 305–327). Springer.

<a id="ref-13"></a>[13] Myrheim, J. (1978). Statistical geometry. CERN preprint TH-2538.

<a id="ref-14"></a>[14] Ambjørn, J., Jurkiewicz, J., & Loll, R. (2005). Reconstructing the universe. *Physical Review D*, 72(6), 064014.

<a id="ref-15"></a>[15] Ishibashi, N., Kawai, H., Kitazawa, Y., & Tsuchiya, A. (1997). A large-$N$ reduced model as superstring. *Nuclear Physics B*, 498(1–2), 467–491.

<a id="ref-16"></a>[16] Albert, D. Z. (2000). *Time and Chance*. Harvard University Press.