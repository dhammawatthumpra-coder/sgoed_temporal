# Handoff — SGOED V5: Quest "Emergent Time" (Arrow of Time)

**วันที่:** 2026-08-31 · **ภาษา:** ต้องตอบเป็นภาษาไทยเท่านั้น (ตาม AGENTS.md)
**งานทั้งหมดอยู่ที่:** `F:\_Ai\sgoed\sgoed\` และ `F:\_Ai\sgoed\sgoed\matrix\`

---

## 1. สถานะงาน (จบชุดหลักแล้ว)

ค้นหา "arrow of time" ในโมเดล SGOED — **ผลสุดท้าย: เวลาจริงต้องมาจาก process/initial condition ไม่ใช่ equilibrium MC**

**พิสูจน์แล้ว (ผ่าน reproduce + null test + deterministic):**
1. **Past Hypothesis** — initial low-entropy (rank-1) → dS/S0 = 0.98 (arrow แรง 100× เทียบ random)
2. **Sequential Growth (CSG-style)** — birth order + past frozen → chain inheritance = **1.000 ± 0.000** (deterministic, scale N=6/M=16)
3. **Non-Equilibrium Flow (upwind transport)** — source/sink + advection → **decay 4000× (E₀=28.85 → E₅=0.007)** + reversal สมมาตร (±5.7) + null discriminate

**กฎที่จารึก:** equilibrium Monte Carlo = time-symmetric → arrow ไม่เกิดจาก final state (metric 11 ตัวพิสูจน์แล้ว: R, D, d_MM, d_s, G, cycle ratio, time-reversal, order ทุกแบบ ฯลฯ)

## 2. เอกสารอ้างอิง (อ่านก่อนทำงานต่อ — ไม่ทำซ้ำเนื้อหาที่นี่)

| ไฟล์ | เนื้อหา |
|---|---|
| `matrix\SGOED_TIME_EMERGENCE_SUMMARY.md` | **เอกสารหลัก — ผลเวลาจริง 3 ทาง + วิวัฒนาการ (FINAL)** |
| `SGOED_PROJECT_SUMMARY.md` | ภาพรวมโครงการ v6–v14 + บทเรียนระเบียบวิธี 6 ขั้น |
| `matrix\SGOED_sequential_growth_notes.md` | รายละเอียด sequential growth |
| `matrix\SGOED_past_hypothesis_notes.md` | Past Hypothesis |
| `matrix\SGOED_v14_notes.md` | v14 (matrix-units hybrid — simultaneity 1.000 แต่ order ไม่เกิด) |
| `matrix\SGOED_v12_graph_notes.md` + `SGOED_v12_summary.md` | v12 (condensation engineered, sink-hub, G metric) |
| `matrix\SGOED_v13_asymmetric_notes.md` | v13 (coupling-only — ไม่ significant ที่ 10 seeds) |
| `matrix\SGOED_v7_feedback_notes.md`, `v8/v9/v10` notes | matrix/graph/hypergraph/ecosystem ผลตรวจก่อนหน้า |

**สคริปต์ที่รันได้:** `step_langevin_transport_tuned.py` (non-eq flow — สำเร็จ), `step_sequential_growth.py` (growth), `step_past_hypothesis.py`

## 3. TODO / งานที่ค้าง (ถ้าสานต่อ)

- **Non-eq flow:** seeds เพิ่ม (5+), steps 500+, scan g_trans/g_sink — ยืนยัน decay 4000× deterministic + "strictly monotonic" ที่จุด noise (0.025→0.036)
- **Sequential growth:** วิเคราะห์กลไกเชิงลึก (ทำไม inheritance 1.000 — coupling strength) + M=32
- **Past Hypothesis + growth ที่ถูกกลไก** (เริ่ม Y พิเศษ + แช่แข็งต้นกำเนิด — รอบก่อนล้มเพราะ unit 0 เอง thermalize)
- **สรุป paper** (ถ้าจะตีพิมพ์): matrix v7 condensation + "เวลาจริง 3 ทาง" — ระบุ engineered + toy model

## 4. บทเรียนระเบียบวิธี (บังคับใช้กับ observable ใหม่ทุกตัว)

Reproduce → Significance (seeds พอ: 5 มักไม่พอ — v13: 2.3σ→1.2σ) → **Null test** (shuffle/baseline) → **Labeling/permutation test** (D พังตรงนี้) → Thermalization check (n_therm ต้องพอ) → Mechanism (อธิบายได้ว่าทำไม)

**กับดักที่เจอ:** R≈0.5 = histogram artifact; d_MM/d_s = null-compatible; D = labeling-dependent; λ_c ดูสูงเกินถ้า therm ไม่พอ; Tr(X⁴) ระเบิดถ้าไม่ normalized — **ทุก metric ที่ "ดูน่าตื่นเต้น" ต้องผ่าน 6 ขั้นก่อนอ้าง**

## 5. Suggested Skills (สำหรับ agent ใหม่)

- `handoff` — อ่านเอกสารนี้ต่อ
- `ponytail-review` / `ponytail-audit` — ก่อนสรุปโค้ดทุกครั้ง (ตาม AGENTS.md)
- `systematic-debugging` / `diagnosing-bugs` — ถ้าต่อโค้ด simulation
- `code-reviewer` — ถ้าจะ review engine ก่อนตีพิมพ์
- `karpathy-guidelines` (ปฏิบัติ: simplicity, surgical changes, ภาษาไทย)

## 6. หมายเหตุ

- ไม่มี sensitive data (ไม่มี API key/password) — โค้ด/notes เปิดอ่านได้
- ตัวเลขทั้งหมด reproducible — อย่า accept metric ใหม่โดยไม่ผ่าน null + labeling test
- ผู้ใช้สนใจ "เวลาจริง" (emergence) โดยเฉพาะ — นำเสนอด้วยความซื่อตรง (ไม่ over-claim: engineered ≠ emergence)