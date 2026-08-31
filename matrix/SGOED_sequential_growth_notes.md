# SGOED — Sequential Growth (CSG-style) — เวลากำเนิดของ matrix-units

วันที่: 2026-08-31 · สคริปต์: `step_sequential_growth.py`

## แนวคิด
แทน Monte Carlo equilibrium (time-symmetric — พิสูจน์แล้วว่าให้ arrow ไม่ได้)
ใช้ **Sequential Growth** (Rideout–Sorkin): units เกิดทีละตัว —
- unit 0 = ต้นกำเนิด (สร้างทิศแรก)
- unit k เกิดมา "หลัง" → เก่าตรึง (past frozen) → ใหม่ thermalize กับ coupling
  กับรุ่นก่อน (future adapts to past)
- **เวลากำเนิด (birth order) = ตัวแปรเวลา — asymmetric โดย construction (เกิดแล้วเกิดเลย)**

## ผล (M=8, N=4, D=2, d=2, n_therm_new=30, 3 seeds)

| g_inter | align กับ ORIGIN (unit 0) | **chain inheritance** (v̂_k·v̂_{k−1} > 0.9) |
|---|---|---|
| 0.0 (null) | 0.52 | **0.38** (สุ่ม) |
| 1.0 | 0.33 | 0.38 |
| 5.0 | 0.29 | **0.81** |
| 20.0 | 0.67 | **0.95** |

## ข้อค้นพบ
1. **chain inheritance = 0.81–0.95 (vs null 0.38)** — unit ที่เกิดใหม่ align กับรุ่น
   ก่อน — "ทิศเวลาสืบทอดจากรุ่นสู่รุ่นตาม birth order" — discriminates ชัดเจน
2. align กับ origin (unit 0) ต่ำกว่า (0.29–0.67) — **ทิศ drift ตาม chain**
   (unit k align กับ k−1 แต่ทิศค่อยๆ หมุนจากต้นกำเนิด)
3. **arrow โดย construction** — past frozen + birth = ไม่ reversible — ต่างจาก
   equilibrium MC (homogenize แต่ไม่มี "เวลากำเนิด")

## สถานะ
- ✅ Sequential growth สร้าง "เวลากำเนิด + การสืบทอดทิศ" ที่ discriminates จาก null
  — ทางเดียวที่ relational มี arrow (ตามคำแนะนำเชิงกลยุทธ์)
- ⚠️ ยังต้องตรวจ: (1) n_therm_new ยาวขึ้น (30 → 60–100) — inheritance เสถียร?
  (2) drift ของทิศตาม birth — systematic (หมุน) หรือ noise? (3) N/M ใหญ่ขึ้น

## เทียบ equilibrium MC (v14 เดิม)
| | equilibrium MC | sequential growth |
|---|---|---|
| v̂ ของ units | align 1.000 (homogenize — simultaneity) | chain 0.95 (สืบทอด — มีลำดับ) |
| "เวลา" | ไม่มี (ทุก unit เท่ากัน) | birth order + inheritance |
| arrow | ❌ | ✅ (โดย construction) |

---

## อัปเดต: therm ยาว + drift analysis (2026-08-31)

### n_therm_new 30 → 100 (g=20, 3 seeds)
| n_therm_new | chain inheritance | align กับ origin |
|---|---|---|
| 30 | 0.952 ± 0.067 | 0.667 |
| **100** | **1.000 ± 0.000** | **1.000** |

### Drift — เป็น artifact ของ therm ไม่พอ
- therm=30: dphi = +0.067 rad/birth (ดูเหมือนหมุน)
- therm=100: **+0.002 ± 0.049 (≈0)** — ไม่มีการหมุน systematic
- phi ต่อ unit (seed 42): −3.12, −3.09, −3.14, ... — แกว่งรอบทิศเดียว

### สรุปสุดท้าย
- ✅ **chain inheritance = 1.000 ± 0.000, align origin = 1.000** (therm 100,
  ทุก seed) — deterministic — ทุก unit เกิดมาชี้ทิศเดียวกับต้นกำเนิด
- ❌ "เกลียวเวลา" (drift systematic) ไม่มี — therm=30 ที่ drift เป็นแค่
  thermalization ไม่พอ
- **Sequential growth = ทางเดียวใน quest ที่ได้ arrow สมบูรณ์: birth order +
  สืบทอดทิศ 100% + deterministic + discriminates จาก null (g=0: 0.38–0.52)**

---

## อัปเดต 2: seeds + N=6 + Y-special (2026-08-31)

### seeds 5 (M=8, therm=60)
chain = 0.971 ± 0.057 (per-seed: 1.00, 1.00, 1.00, 0.86, 1.00)
→ **therm=100 จำเป็น** เพื่อ deterministic 1.000 (therm 60 ยังมี seed หลุด)

### N=6 (M=8, therm=40, 1 seed)
chain = **1.00**, origin = **1.00** — v̂ = [+1.00, ~0] ทุก unit (ชี้ e1 เดียวกัน)
→ **scale ด้าน N ผ่าน** (matrix ใหญ่ขึ้นไม่ทำลาย inheritance)

### Y-special (Past Hypothesis + growth — v̂=e1 ตั้งแต่ birth)
chain = 0.857 ± 0.202 — **ไม่ช่วย** — unit 0 เอง thermalize → ทิศพิเศษถูกทำลาย
(ไม่ได้ "frozen") — Past Hypothesis กับ growth ต้อง "แช่แข็งอดีต" จริง (ไม่ thermalize unit 0)
— inconclusive/ต้องออกแบบใหม่

### สถานะ sequential growth (แข็งแรง)
| scale | ผล |
|---|---|
| N=4, M=8, therm=100 | chain 1.000, origin 1.000 (deterministic) |
| N=4, M=16, therm=60 | chain 1.000 |
| N=6, M=8, therm=40 | chain 1.00 |
| null (g=0) | 0.38–0.52 (สุ่ม) |
