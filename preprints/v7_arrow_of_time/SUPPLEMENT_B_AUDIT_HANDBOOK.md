# SGOED Audit Handbook — คู่มือ 6 ประตูตรวจสอบสำหรับ observable ใดๆ (ทีมอ้างอิง)

**สถานะ:** อ้างอิงภายในทีม (v1, 2026-09-01) · คู่หู executable: `preprints/v7_arrow_of_time/code/audit_gates.py`
**ความสัมพันธ์กับเอกสารอื่น:** manuscript_v7 §3 = checklist 6 gate แบบย่อ; Appendix B = ตารางกับดัก 8 ตัว (versioned ของบทความ); เอกสารนี้ = **รุ่นเต็ม 12 กับดัก + workflow** — เมื่อเจอกับดักใหม่ ให้อัปเดตที่นี่ก่อน แล้วค่อยย่อลงบทความ

---

## 1. หลักการเดียวของทั้งคู่มือ

> **ทุก metric คือสมมุติฐานเกี่ยวกับ observable — แต่ละช่องโหว่ในบทนี้คือวิธีที่มันจะถูกพิสูจน์ว่าผิด**
> ตัวเลขที่ "ดูน่าตื่นเต้น" ไม่เคยเป็นผลก่อนผ่าน 6 ประตู — ถ้าข้ามไป เจอทีหลังเสมอ (เจอมาแล้วทั้ง 12 กับดักนี้)

## 2. Six Gates (เกณฑ์ผ่าน + เมื่อไหร่ที่กัด)

| # | Gate | เกณฑ์ผ่าน | เมื่อไหร่ที่มันกัดเรา |
|---|---|---|---|
| 1 | **Reproduce** (`gate1_reproduce`) | รันซ้ำ seed เดียวกัน → เลขเดิมถึง machine precision | unseeded RNG, float artifact, ไม่ deterministic |
| 2 | **Significance** (`gate2_significance`) | ≥10 seeds; std ≤ 5% ของ \|mean\| | 5 seeds มักไม่พอ — v13: 2.3σ → 1.2σ เมื่อเพิ่ม seeds |
| 3 | **Null test** (`gate3_null`) | \|obs − null\| ≥ 3σ ของความแปรปรวนรวม | R≈0.5 (histogram), d_MM/d_s null-compatible, สเกลการ normalize |
| 4 | **Labeling/permutation** (`gate4_labeling`) | metric เปลี่ยน ≤ tol ภายใต้การเรียง node ใหม่ | D: ช่วง [−98, +28] ภายใต้ permutation |
| 5 | **Thermalization** (`gate5_thermalization`) | observable plateau เมื่อ n_therm เพิ่ม | v5 step=2; past-hypothesis therm 60→120 (0.68→0.9995!) |
| 6 | **Mechanism** (`gate6_mechanism`) | เขียนอธิบาย *ทำไม* ได้ + ชี้หลักฐานไฟล์ | ผลที่ผ่าน 1–5 แต่ไม่มีคำอธิบาย = เดี๋ยวก็ถูกจับ |

**ลำดับบังคับ:** ห้ามข้าม — ถ้าตกประตูไหน ให้หยุด อธิบาย/แก้ แล้วเริ่ม Gate 1 ใหม่กับ metric เวอร์ชันที่แก้แล้ว

## 3. Trap Catalog v2.0 (รุ่นเต็ม 12 กับดัก)

| # | กับดัก | อาการ (จากโปรเจกต์นี้) | Gate ที่จับ | ข้อแก้ |
|---|---|---|---|---|
| 1 | Histogram artifact | R≈0.5 จาก graph สมมาตร — shuffle แล้วค่าอยู่เหมือนเดิม | 3 Null | ห้ามรายงาน R ตัวเดียว ต้องเทียบ shuffle เสมอ |
| 2 | Labeling dependence | D ∈ [−98, +28] ภายใต้ permutation | 4 Labeling | metric ต้อง invariant ต่อฉลาก node |
| 3 | Null-compatible dimension | d_MM/d_s ของ graph ตรงกับ random baseline | 3 Null | calibrate estimator กับ poset ที่รู้คำตอบก่อน |
| 4 | Thermalization ไม่พอ | v5 step=2 สร้าง crossover ปลอม; past-hypothesis 0.68→0.9995 ที่ therm 120 | 5 Therm | ตรวจ plateau ที่ n_therm ที่รายงาน |
| 5 | Finite-size "4D" | d≈4 ที่ N=250 สลายที่ N=1000 (ทั้ง fixed-p และ fixed-k) | 2+3 | ต้อง audit scaling ถึง N≥1000 ก่อนอ้างมิติ |
| 6 | Bipartite parity | return probability = 0 ทุก t คี่ → d_s สั่น ±10³ | 5 Therm | lazy walk: T ← ½(I+T) |
| 7 | int8 overflow | relation-matrix matmul int8 ล้นที่ N>15 — silent garbage | 1 Reproduce | ใช้ int64/float |
| 8 | Closure แบบไม่ union | R←R² โดยไม่รวม edge เดิม → หดจนเป็น 0 | 1 Reproduce | ใช้ R ← R ∨ R² จน fixpoint |
| 9 | Normalization scale | ระยะ matrix ÷(KN) บีบ c_eff → d ต่ำทุกแบบที่ c=1 | 3 Null | unit-match (aspect calibrate) กับ convention ของ estimator |
| 10 | λ_c สูงเกินจริง | ค่า λ_c ดูใหญ่ถ้า therm ไม่พอ (MC ที่ยังไม่สมดุล) | 5 Therm | วาง plateau ก่อนอ่าน λ_c |
| 11 | Tr(X⁴) ระเบิด | quartic ไม่ normalized → E→10³⁰ | 1 Reproduce | normalise scale-free (4th moment / (TrX²)²) |
| 12 | Seeds น้อยไป | 2.3σ → 1.2σ เมื่อ 5→N seeds | 2 Significance | ≥10 seeds + รายงาน std เสมอ |

## 4. Workflow: ตรวจ observable ใหม่ (8 ขั้น)

1. เขียน `observe(seed) -> float` ให้ deterministic (seed เข้าเป็น parameter)
2. รัน `gate1` — ถ้าตก: จับ unseeded RNG/artifact ก่อนไปต่อ
3. รัน `gate2` ที่ 10–20 seeds — รายงาน mean±std; ดู std เหลืออีกไหมถ้าเพิ่ม seeds
4. เขียน `null_observe` (shuffle/randomized/baseline) → `gate3` — ถ้าแยกไม่ออก: จบ (negative ที่มีคุณค่า) หรือ redesign
5. `gate4` ด้วย permutation ของ instance — ถ้า metric ขยับตามฉลาก: หา metric invariant
6. `gate5` (scan n_therm) — หา plateau ก่อนเชื่อตัวเลขใด
7. จบด้วย `gate6` — เขียนกลไก + ชี้ไฟล์ผล
8. บันทึกลง results JSON ทันที (ไม่งั้น "รันซ้ำได้ 100%" หาย)

## 5. Case studies (หนึ่งบรรทัดต่อบทเรียน)

- **Thermalization กลับผล 2 ครั้ง:** past-hypothesis growth — therm 60 → align 0.68±0.45, therm 120 → 0.9995±0.0002 (มีแต่ Gate 5 ที่จับ)
- **Scale audit ฆ่า "4D":** p=0.016 ที่ N=250 → d=4.42; ที่ N=1000 → 1.51–8.0 แล้วแต่ scaling (มีแต่ Gate 2+3)
- **Null ฆ่า R:** R≈0.5 ของ graph สมมาตรอยู่รอดทุกการตั้งค่า แต่ shuffle ก็ให้ค่าเดิม — metric ไม่เคยวัดทิศทาง
- **กับดัก 7+8 เงียบที่สุด:** output ดูสมเหตุสมผลทั้งที่เลขภายในล้น/ว่าง — มีแต่ Gate 1 (rerun กับกรณีที่รู้คำตอบ) ที่จับได้

## 6. การดูแล (ยึดเป็นกติกา)

- พบกับดักใหม่ → เพิ่มแถวในตารางนี้ (ฉบับเต็ม) → ซิงก์ย่อลง manuscript Appendix B (ฉบับตีพิมพ์ 8 ตัว) → ถ้า toolbox ต้องรู้ ก็เพิ่ม case ใน self-test ของ `audit_gates.py`
- ทุกผลลบที่เจอ = ผลงาน (บันทึก ไม่ใช่ซ่อน) — ตามธรรมเนียมของโปรเจกต์

*อ้างอิงตัวเลข: notes อัปเดต 1–17 ใน `notes/SGOED_TIME_EMERGENCE_SUMMARY.md`, `notes/SGOED_PROJECT_SUMMARY.md`, และ scripts `audit_evidence/`*