

## Replication protocol recovery — 2026-08-29
- Local provenance search was performed across the repo root and the wider `F:\_Ai\sgoed` tree for executable definitions of `A_init`, `area_excess`, and `decay_len`.
- No source definition of `A_init` or `decay_len` was found in the local code/data/design artifacts. The terms currently occur only as protocol/checkpoint terminology in the handoff.
- Therefore the pilot-derived compound criterion (`argmax t={0,1}`, `decay_len >= 4`, `A_init > 2.0`) is **not yet executable from local provenance** and must not be reconstructed by inference.
- No new seeds are to be run until the exact prior definitions of `A_init` and `decay_len` are recovered or explicitly re-derived and recorded as a new protocol decision.
- This is a protocol-definition blocker, not a provenance/data-integrity failure. Existing Phase-D gates and conclusions remain unchanged.

## Definition-recovery audit — 2026-08-29 12:31:28 +07:00
- Wider recursive search across `F:\_Ai\sgoed` found no local source definition of `A_init` or `decay_len`. Exact-token and broader decay-pattern searches returned only the present handoff references; no prior executable definition was recovered.
- the repo root is **not a Git working tree** (`git -C <repo-root> log --all ...` returns `fatal: not a git repository`). Therefore there is no V5-local Git history to mine for these definitions. The only Git repository found in the wider tree is `preprint\record_B_sgoed_code`, which is a separate repository and was not treated as provenance for the V5 Phase-D protocol.
- No seed 47–66 data have been inspected or generated in this session before this protocol decision.

## Estimand definition (pre-registered 2026-08-29 12:31:28 +07:00)
The following definitions are a **new prospective protocol decision**, not recovered historical definitions, and are locked before any new-seed replication run:

### Primary quantities
1. **`A_init`** := `delta_wall(t=0)` where `t=0` denotes the first recorded point of the measurement window beginning at the selected `N_therm`.
   - Rationale: this is the directly observed first-window `delta_wall` value already present in the convergence data and corresponds to the initial displacement being tested; it introduces no new physical observable.

2. **`decay_len`** := the smallest non-negative measurement-sweep index `t` for which
   `delta_wall(t) <= A_init / e`, measured from the first point of the measurement window.
   - If no such point occurs within the prescribed observation window, `decay_len` is recorded as **undefined / not reached**, not censored into a numerical value.
   - Rationale: e-folding is a standard, threshold-free decay-length definition and does not require estimating a late-window plateau from the replication results.

### Compound candidate-anomaly criterion
A seed is classified as a **candidate anomaly** iff all of the following hold:
- `argmax(delta_wall[0:30])` occurs at `t in {0,1}`;
- `decay_len >= 4`;
- `A_init > 2.0`.

The `A_init > 2.0` and `decay_len >= 4` thresholds are explicitly **pilot-derived operational thresholds** retained from the previously specified replication design. They are not presented as theory-derived universal thresholds and will not be changed after inspecting new-seed outcomes.

### Lock / anti-snooping rule
- These definitions and thresholds are frozen as of the timestamp above.
- They must not be altered, relaxed, tightened, or replaced after any seed 47–66 result is observed, regardless of whether the outcome supports or weakens the pilot finding.
- Level-0 raw trajectories for every new seed remain reportable regardless of whether the compound criterion is met.

## Replication execution status
**🟢 READY** — the estimand and operational classification rule are now explicitly defined and timestamp-locked. No new-seed run has yet been started in this session.

## Protocol correction / final lock — 2026-08-29 12:31:28 +07:00
**Important consistency correction to the immediately preceding draft:** `A_init = delta_wall(t=0)` cannot be combined with the retained pilot threshold `A_init > 2.0`, because `delta_wall` is O(10^-1) in the pilot whereas the threshold 2.0 belongs to the previously used **ratio-scale** diagnostic. The preceding pairing is therefore superseded and must not be used for execution.

The executable prospective definition is now locked as follows:

1. **`A_init` := `ratio_trajectory[0]`**, i.e. the ratio observable at the first measurement point of the selected window. This preserves the previously used `A_init` ratio scale and makes the pilot threshold `A_init > 2.0` dimensionally/numerically coherent. No new-seed results were used to select this definition.

2. **`decay_len` := first measurement-sweep index `t >= 0` satisfying `delta_wall(t) <= delta_wall(0)/e`**, where `delta_wall(t) = 1 - E_max(t)/wall`, measured from the first point of the measurement window. If the condition is not reached within the prescribed 30-point diagnostic window, record `decay_len = undefined/not_reached` and the compound criterion fails.

3. **Primary compound candidate-anomaly rule (frozen):**
   - `argmax(delta_wall[0:30]) in {0,1}`;
   - `decay_len >= 4`;
   - `A_init > 2.0` on the ratio scale above.

4. The threshold values `2.0` and `4` are **pilot-derived operational thresholds**, explicitly acknowledged as such. They are frozen and will not be modified after any new-seed outcome is observed.

5. This final lock supersedes only the inconsistent `A_init = delta_wall` pairing above; it does **not** reopen provenance, data-integrity, convergence, or mechanism gates.

6. **Anti-snooping lock:** no seed 47–66 has been run or inspected before this final definition was recorded. No prospective definition or threshold may be changed after new-seed inspection.

**Replication execution: 🟢 READY.**


## Protocol correction — pilot back-test required before replication — 2026-08-29 12:XX +07:00
**Status change: 🟢 READY → 🔴 BLOCKED.** The previously locked compound criterion was back-tested against pilot seeds 42–46 before any new-seed execution and failed its own known pilot classification target: no seed passed all three criteria, including the known pilot anomaly seeds 45 and 46. Therefore the criterion is rejected and must not be used for replication.

### Back-test result recorded
- `A_init = ratio_trajectory[0]`, threshold `A_init > 2.0`: true for all tested wall=15 pilot seeds, hence non-discriminating/vacuous for this purpose.
- With the newly locked 1/e definition of `decay_len`, pilot values were: seed 42 = 27, 43 = 1, 44 = 13, 45 = 1, 46 = 3.
- The retained rule `decay_len >= 4` therefore rejects both known anomaly seeds 45 and 46 and is directionally inconsistent with the observed short-transient behavior.
- No seed 47–66 has been inspected or generated as part of this back-test.

### Permanent protocol rule
**No prospective classification criterion may be locked for replication without an explicit back-test against pilot seeds 42–46 (the existing pilot reference set) and a recorded result showing whether the intended pilot classification is recovered.** A criterion that fails this back-test is rejected before replication; it may not be rescued by inspecting new-seed outcomes.

### Required re-derivation before READY
1. Reconsider `A_init` on the `delta_wall` scale rather than the ratio scale, because the ratio-scale threshold `>2.0` is vacuous at wall=15.
2. If `decay_len` is retained as an e-folding crossing, its anomaly direction must reflect the observed short transient (`decay_len` small), and any threshold must be justified prospectively using only the pilot reference set before lock. Do not choose a threshold merely to force classification; document the rule and its pilot back-test.
3. Re-run the complete pilot back-test after every candidate rule. The intended pilot reference outcome is anomaly/candidate for 45 and 46 and non-candidate for 42, 43, 44, subject to an explicit statement if the pilot data cannot support a unique criterion.
4. Only after a criterion passes the back-test, is scientifically interpretable, and is timestamp-locked may `Replication execution` return to 🟢 READY.

**Current execution prohibition:** do not run or inspect seed 47–66 until this protocol-definition blocker is resolved and the revised criterion is recorded in this handoff.

## Protocol correction — explicit execution block (2026-08-29 03:XX +07:00)
**Replication execution: 🔴 BLOCKED.** The previously locked criterion failed back-test against ground-truth pilot seeds 45/46 — see correction below. This is an append-only status correction; prior READY records are retained unchanged.

## Revised criterion work — awaiting pilot back-test
Per the explicit staged protocol, `A_init` is being reconsidered on the `delta_wall` scale (`A_init = delta_wall(t=0)`), and `decay_len` retains the 1/e-crossing definition but with anomaly direction `decay_len` small. No seed 47–66 data are to be inspected or generated. No READY transition is permitted until the revised rule is back-tested against pilot seeds 42–46 and the result is reported for review.

## Revised criterion candidate + mandatory pilot back-test — 2026-08-29 12:42:48 +07:00
**Execution remains 🔴 BLOCKED.** This section records a candidate revision and its pilot-only back-test; it is **not a prospective lock** and does not authorize seed 47–66.

### Candidate definitions tested
1. **`A_init` := `delta_wall(t=0)`**, where `t=0` is the first recorded point of the 30-point measurement window.
2. **`decay_len` := smallest measurement-sweep index `t >= 0` satisfying `delta_wall(t) <= delta_wall(0)/e`**; if not reached within the 30-point diagnostic window, the value is undefined/not_reached.
3. Candidate anomaly rule:
   - `argmax(delta_wall[0:30]) in {0,1}`;
   - `decay_len <= 3`;
   - `A_init > 0.0025`.

The `0.0025` threshold is a pilot-calibrated operational candidate chosen on the `delta_wall` scale to lie above the largest observed baseline A_init in the pilot wall=15 set and below the anomalous values; it is **not yet locked**. The decay direction `<=` follows the observed short-transient interpretation and is likewise being subjected to the mandatory pilot back-test before any lock.

### Mandatory wall=15 pilot back-test (seeds 42–46)
Using the existing `phase_d_convergence_ladder.json` trajectories, with no seed 47–66 inspection or execution:

| seed | A_init = delta_wall(0) | argmax_idx | decay_len | A_init > 0.0025 | argmax criterion | decay_len <= 3 | ALL_CRITERIA |
|---:|---:|---:|---:|:---:|:---:|:---:|:---:|
| 42 | 0.0000934224 | 7 | 27 | False | False | False | **False** |
| 43 | 0.0256221 | 0 | 1 | True | True | True | **True** |
| 44 | 0.000449806 | 4 | 13 | False | False | False | **False** |
| 45 | 0.104597 | 0 | 1 | True | True | True | **True** |
| 46 | 0.179954 | 0 | 3 | True | True | True | **True** |

### Back-test assessment
The candidate does **not** satisfy the intended pilot classification because seed 43 is also classified as a candidate. Therefore **do not lock this rule and do not change execution to READY**. The requested target `45=True, 46=True, 42=False, 43=False, 44=False` is not recovered by this candidate.

This failure is informative: the proposed `A_init` threshold cannot by itself separate seed 43 from 45/46 on the first-point `delta_wall` scale, because seed 43 has a large first-point excursion despite its different subsequent shape. Any next candidate must therefore address this distinction without using seed 47–66 outcomes, and must again pass the complete 42–46 back-test before lock.

**Manuscript remains ⛔ untouched. Replication remains 🔴 BLOCKED. No seed 47–66 has been run or inspected.**


## Protocol design review — binary criterion rejected; estimand reconsideration pending — 2026-08-29 14:04:00 +07:00
**Execution remains 🔴 BLOCKED.** The pilot back-test establishes that the current binary candidate-anomaly formulation should not be repaired by repeated threshold tuning. In particular, the pilot first-point `delta_wall` values are a continuum rather than a clean two-cluster separation, and seed 43 has a large initial excursion but a different subsequent shape from seeds 45/46. Repeatedly tuning thresholds on the same five pilot seeds risks overfitting the pilot rather than defining a reproducible prospective estimand.

### Local pilot check relevant to estimand choice
Using `phase_d_convergence_ladder.json` and the wall=15, `N_therm=20` measurement windows, the locally recomputed first-point `delta_wall` values are approximately:
- seed 42: 0.00018249
- seed 43: 0.00015310
- seed 44: 0.00010759
- seed 45: 0.00033206
- seed 46: 0.00085299

Using the previously recorded `delta_first` convention from the pilot discussion gives the corresponding reported values 0.0000934, 0.0256221, 0.0004498, 0.104597, and 0.179954; the distinction is retained here rather than conflated, because the exact estimand used for prospective replication must be specified explicitly.

The current 1/e `decay_len` calculation on the locally extracted 30-point diagnostic windows gives 7, 13, 22, 1, and 2 for seeds 42–46 respectively under the direct `E_max`-derived `delta_wall` trajectory. A pilot-only Spearman check of direct first-point `delta_wall` versus this decay length is strongly negative (rho = -0.90, n=5), but this is **descriptive pilot evidence only**, not a validation of a future statistical claim.

### Design decision not yet locked
A continuous estimand is now under consideration instead of a binary `candidate anomaly` classifier. Candidate prospective forms include a pre-specified rank relationship between initial displacement and subsequent decay, or a pre-specified continuous relaxation model. **No continuous estimand, test, threshold, significance level, or seed-47–66 execution rule is locked by this entry.** The purpose of this entry is to prevent further threshold tuning from being mistaken for prospective design.

**Mandatory state:** do not inspect or run seeds 47–66; do not edit `manuscript_v5.tex`; do not change `Replication execution` to READY until the continuous-vs-binary estimand decision is explicitly resolved and the resulting prospective analysis rule is recorded with a new timestamp.
