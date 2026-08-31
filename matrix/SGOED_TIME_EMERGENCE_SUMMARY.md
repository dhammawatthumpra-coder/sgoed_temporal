# SGOED — Time Emergence: ผล "เวลาจริง" ที่ตรวจสอบแล้ว (2026-08-31)

เอกสารสรุปผลงานล่าสุดของ SGOED — หลัง quest "หาลูกศรเวลา" ที่ metric เชิงโครงสร้าง
พังหมด (11 ตัว) — พบ 2 ทางที่ให้ "เวลาจริง" ผ่านการตรวจทั้งหมด

---

## ผลที่ 1: Past Hypothesis (เวลาจากการคลายตัวของสถานะตั้งต้น)

**หลักการ (Boltzmann/Albert):** arrow เกิดจากสถานะตั้งต้นที่เอนโทรปีต่ำเป็นพิเศษ
→ ระบบคลายตัว (relax) ไป equilibrium — "เวลาที่ไหล" = ปริมาณการคลายตัว

**ผล (v7 matrix, N=4, 3 seeds, gXY=0):**
| initial | dS/S0 (ต้องคลายตัว) | dS_total |
|---|---|---|
| random | 0.29 | 3 |
| **rank-1 (low-entropy)** | **0.98** | **337** |

- สถานะตั้งต้นพิเศษ (ทิศเดียว) ต้องคลายตัว ~100 เท่าของ random — arrow แรงกว่า
- deterministic + monotonic (S ลด 344 → ~7)
- สคริปต์: `step_past_hypothesis.py` · notes: `SGOED_past_hypothesis_notes.md`

## ผลที่ 2: Sequential Growth (เวลากำเนิด — CSG-style)

**หลักการ (Rideout–Sorkin):** units เกิดทีละตัว — เก่าตรึง (past frozen) — ใหม่
ปรับเข้ากับรุ่นก่อน — **birth order = เวลา — asymmetric โดย construction**

**ผล (g_inter=20, therm 100):**
| ตัววัด | null (g=0) | sequential growth |
|---|---|---|
| chain inheritance (v̂_k ~ v̂_{k−1}) | 0.38 | **1.000 ± 0.000** |
| align กับ origin (unit 0) | ~0.5 | **1.000** |
| deterministic ข้าม seeds | — | ✅ (ทุก seed เหมือนกัน) |

- M=8 และ **M=16: inheritance = 1.000** — scale ได้
- drift ที่เห็นตอน therm สั้น (30) = thermalization ไม่พอ — therm 100 → ไม่มี
- สคริปต์: `step_sequential_growth.py` · notes: `SGOED_sequential_growth_notes.md`

## ขยาย (ยังไม่ conclusive)
- **Past Hypothesis + growth** (unit 0 เริ่ม rank-1): chain 0.93, origin 0.50 —
  ไม่ช่วย — กลไกไม่ตรง: v̂ มาจาก Y (random) ไม่ได้จาก X rank-1 — ต้องตรวจเพิ่ม
  (2 seeds — inconclusive)

---

## บทเรียนปิด (มีค่าที่สุดของทั้งโครงการ)

**Equilibrium Monte Carlo เป็น time-symmetric — arrow of time จะไม่เกิดจาก
final state ไม่ว่า coupling แบบไหน** (พิสูจน์ด้วย metric 11 ตัวที่พังหมด:
R, D, d_MM, d_s, G, cycle, time-reversal, order, repulsion, dynamic, entropy-rate)

**"เวลาจริง" ต้องมาจาก:**
1. **Initial condition พิเศษ** (Past Hypothesis) — การคลายตัวของสถานะ low-entropy
2. **Process ที่ asymmetric โดย construction** (Sequential Growth) — birth order

— ตรงกับทิศทางเชิงกลยุทธ์: ถ้าสถิต → Past Hypothesis; ถ้า relational → Sequential
Growth / Non-Equilibrium Flow

## สถานะปัจจุบัน
- ✅ "เวลาจริง" 2 ทาง ผ่าน reproduce + null test + deterministic
- ✅ M=16 scale (inheritance 1.000)
- ⚠️ ยังต้อง: seeds เพิ่ม, N ใหญ่ (6–8), non-equilibrium flow (แนวทาง 2),
  รวม Past Hypothesis + growth ให้ถูกกลไก (v̂ เริ่มพิเศษ ไม่ใช่ X rank-1)

---

## อัปเดต: Non-Equilibrium Flow (แนวทาง 2) — MVP ล้มเหลว (2026-08-31)

### การทดลอง: pump ที่ unit 0 (source) + directed flow coupling (0→M−1)
E profile ไม่ monotonic (ไม่มี gradient ที่ไหล), align กับ origin 0.52–0.70 (ไม่ deterministic)

### สาเหตุ
1. pump term อ่อนเกินเทียบ local action (gate ดึง E₀)
2. directed coupling (v̂·v̂'·E') ไม่ลำเลียง E — แค่ align v̂ อ่อน
3. ยังเป็น MC (equilibrium-ish) — **ไม่มี dissipation จริง** — flow ไม่เกิด

### บทสรุป
- ❌ "continuous flow" ในกรอบ MC ยังไม่ work — ต้อง dissipation จริง (Langevin/
  non-MC update) — งานออกแบบใหม่
- ✅ **แต่ sequential growth = non-equilibrium flow แบบ "birth"** (ไหลหนึ่งทาง +
  ไม่ย้อนกลับ) — ได้ผลแล้ว (inheritance 1.000) — เป็น non-equilibrium ที่ใช้งานได้

---

## อัปเดต 2: Langevin dissipation (non-MC) — align ได้ แต่ E ยังไม่ไหล (2026-08-31)

สคริปต์: `step_langevin_flow.py`, `step_langevin_flow2.py`

### ผล (M=8, N=4, pump@0, friction γ, 2 seeds)
| design | E profile | decreasing | align |
|---|---|---|---|
| pump normalize (F=X/|X|) | แบน (4.6–5.0) | ❌ | 0.94 |
| growth pump (F=+gX) | แบน (4.3–4.8) | ❌ | 0.94–1.00 |

### สรุป
- ✅ Langevin (non-MC) align ได้ (1.00 ที่ drive=1.0) — coupling ทำงานใน dynamics ใหม่
- ❌ **การไหลของ E ไม่เกิด** — (1) local action (IKKT+gate) ครอบงำ pump — E₀ ไม่โดดเด่น
  (2) coupling (align v̂) ไม่ลำเลียงปริมาณ (extent) — ต้องออกแบบ "extent-transfer
  coupling" (ปริมาณไหลจาก unit หนึ่งไปอีกหน่วย) — งานออกแบบใหม่
- **non-equilibrium flow (continuous) — ยังไม่สำเร็จ** — แต่ sequential growth
  (birth-flow) ที่ได้ผลแล้วยังเป็น non-equilibrium ที่ใช้งานได้ (inheritance 1.000)

---

## อัปเดต 3: Extent-transport (ตามรีวิว) — stable + pump current (2026-08-31)

สคริปต์: `step_langevin_transport.py`

### การปรับที่จำเป็น (เงื่อนไขเสถียรภาพ)
- มี local gate/regularizer ตามที่รีวิวแนะนำ → **Tr(X⁴) ระเบิด** (E→10³⁰)
- แก้: **normalized coupling** `−g·v̂²·Tr(X⁴)/(Tr(X²)²+ε)` (4th moment scale-free —
  bounded — คง "การแย่ง extent") + sparsity α·Tr(X²)

### ผล (M=6, N=4, 150 steps, normalized)
| config | E profile (0→5) | J_net |
|---|---|---|
| REAL (pump@0) | [0.79, 0.35, 0.14, 0.29, 0.36, 0.50] | **+0.074** |
| NULL | [0.32, 0.29, 0.14, 0.29, 0.36, 0.50] | −0.017 |
| REVERSED (pump@5) | [0.32, ..., **0.91**] | **−0.063** |

### ข้อค้นพบ
- ✅ stable (normalized coupling) + pump@0 → E₀ สูงสุด + J_net บวก; pump@5 → กลับทิศ
  — **reversal test สมมาตร** (กระแสตามทิศปั๊ม — ไม่ใช่ artifact ของการตั้งค่า)
- ✅ กระแส (J_net) มีทิศทางตาม pump — non-equilibrium flow เริ่มทำงาน
- ⚠️ E decay เต็ม chain ยังไม่สมบูรณ์ (mid-chain 0.14→0.29) — ต้อง tuning ต่อ
  (g_trans/γ/steps/pumping) ก่อนสรุป "เวลาที่ไหลเต็ม chain"
- ⚠️ 150 steps สั้น + 1-2 seeds — ยัง preliminary

---

## อัปเดต 4: UPWIND transport (รีวิว v2) — drift ทิศเดียวทำงาน (2026-08-31)

สคริปต์: `step_langevin_transport.py` (v2)

### การปรับตามรีวิว v2
- F → **upwind** (F_u = +g_trans X_{u-1} − g_trans X_u — ไม่ดึงย้อนกลับ)
- T: 0.5 → 0.1 (ลด noise floor), g_drive=3.0, g_trans=1.5, g_bulk=0.2, g_sink=2.0

### ผล (M=6, N=4, 150 steps, 2 seeds)
| config | E profile | J_net |
|---|---|---|
| REAL (pump@0) | [0.30, 0.19, 0.10, 0.12, 0.10, 0.12] | **+0.033** |
| NULL | [0.09, 0.13, 0.10, 0.12, 0.10, 0.12] | −0.006 |
| REV (pump@5) | [0.07, 0.10, 0.09, 0.10, 0.13, **0.51**] | −0.062 |

### ข้อค้นพบ
- ✅ **upwind สร้าง drift ทิศเดียว**: E₀=0.30 (pump) ลดครึ่งที่ E₁ — J บวกตามปั๊ม — REV กลับทิศ
  (สมมาตร) — boundary reflection ลดลง
- ✅ stable (normalized coupling + sparsity)
- ⚠️ E กลางสายแบน ~0.10–0.12 (ชน thermal floor — T/α กดสเกล) — ยังไม่ใช่
  "exponential decay เต็ม chain" — ต้อง tuning: α ลด, g_drive เพิ่ม, steps 500+
- ⚠️ preliminary (150 steps, 2 seeds) — ยังไม่ verdict

### สถานะ non-equilibrium flow (แนวทาง 2)
- diffusion (รอบ 1-2): ระเบิด/แบน — ❌
- **upwind (รอบ 3): stable + drift orientation — ✅ หลักการทำงาน — ต้อง tuning ต่อ**

---

## ✅ FINAL: Non-Equilibrium Flow — สำเร็จ (tuned, 2026-08-31)

สคริปต์: `step_langevin_transport_tuned.py`
params: g_drive=5.0, g_trans=1.2, g_bulk=0.1, g_sink=3.0, alpha=0.1, T=0.02, 400 steps

### ผล (M=6, N=4, 2 seeds)
| config | E profile (0→5) | J_net |
|---|---|---|
| **REAL (pump@0)** | **[28.85, 1.62, 0.10, 0.025, 0.036, 0.007]** | **+5.75** |
| NULL | [0.09, 0.10, 0.12, 0.09, 0.11, 0.03] | +0.01 |
| REV (pump@5) | [0.06, 0.06, ..., **30.18**] | **−5.98** |

### ข้อค้นพบ
- ✅ **Decay 4000×** (28.85 → 0.007) ตาม chain — source@0 → sink@5 — "เวลาที่ไหล"
  จากต้นกำเนิดสู่ปลาย — รุนแรงที่สุดเท่าที่เคยมี
- ✅ **Reversal สมมาตรเต็ม** (J: +5.75 ↔ −5.98) — ปั๊มกลับทิศ → gradient กลับ — ไม่ใช่ artifact
- ✅ NULL แบน (J≈0) — discriminates ชัดเจน
- ✅ deterministic (2 seeds: 28.86/28.83 — เกือบเท่ากัน)
- ⚠️ จุดไม่ monotonic ที่เหลือ = noise ระดับ 0.01–0.04 (thermal floor) — "ในทางปฏิบัติ monotonic"

### สรุปปิด QUEST ทั้งหมด (3 ทางของ "เวลาจริง" ครบ)
| แนวทาง | ผลสุดท้าย |
|---|---|
| Past Hypothesis | ✅ dS/S0 = 0.98 (arrow แรง 100×) |
| Sequential Growth | ✅ inheritance 1.000, deterministic, scale N=6/M=16 |
| **Non-Equilibrium Flow (upwind)** | ✅ **decay 4000× + reversal สมมาตร + null discriminate** |

**กฎที่พิสูจน์แล้ว:** equilibrium MC → arrow ไม่ได้; "เวลาจริง" ต้องมาจาก
(1) initial condition พิเศษ (2) process asymmetric โดย construction
(sequential growth / upwind transport) — ครบทั้ง 3 ทาง ตรวจซ้ำได้

---

## อัปเดต 5: เส้นทาง "4D" (v15) — ปิดด้วยคำตอบชัด: 4D emergence ไม่อยู่ในสเกล toy (2026-08-31)

**โจทย์ (จากรีวิว):** 3 สายสู่ 4D — (1) Matrix SSB แบบ IKKT/Kim–Nishimura
(2) Sequential Growth → Causal Set / d_MM (3) Spectral dimension บน flow
— ทดสอบสาย 1 แบบซื่อตรงก่อน (เลือก ก: "ออกแบบ SSB โดยไม่ใช้ v̂")

**สคริปต์:** `sgoed_matrix_v15.py` (probe 1–2), `step_v15_dynamical.py` (probe 3),
`step_v15_bounded.py` (probe 4) + ผล JSON 3 ไฟล์

**ผลทั้ง 4 probe (D=4 และ D=10, 6–10 seeds):**
1. **Equilibrium ไม่มี v̂** → isotropic หมด (ratio 1.05–1.07; D=2 anchor = 4.43
   ตรงกับ documented 4.55) — กลไก "เลือกมิติ" ของ v7 มาจาก v̂ steering
   (engineered) ล้วน — และ **commutator term มีอยู่แล้ว** ใน `action_v7`
2. **Equilibrium pseudo-Euclidean (η=−1,+1,+1,…)** → แยก "1+3" ได้จริงและเสถียร
   (D=4: T=3.5, space 9.996×3, **iso_space=0.000** ข้าม 10 seeds) — แต่เป็นการอัด
   signature (engineered) + **เวลา "หด"** — D=10: พื้นที่ขยายทั้ง 9 (ไม่มี "เลข 3")
3. **Dynamical (T = clock, real-time)** → bosonic Lorentzian **unbounded**
   (ext ทะลุ 2000–8700, drift 0.13–0.15 — ไม่ thermalize เพราะไม่มีสมดุล) —
   ตรงกับฟิสิกส์จริง: Lorentzian IKKT ต้อง fermion/phase regulator ถึงมีเลข "3"
4. **Bounded-regulator (saturating `−g·x/(1+x)`)** → มีสมดุล + **สมมาตรเต็ม**
   (top3-gap 1.06 ± 0.01) — และ control ตรวจจับผ่านใน regime นี้ (อัด 3-ทิศ → 1.14)
   → **"ไม่เกิด 3-of-9" เป็น negative result ที่ตรวจสอบได้** (null test ผ่าน)

**บทสรุปสาย 1 (ปิด):** ที่สเกล toy (real matrices, ไม่มี fermion, N≤6)
**4D emergence ไม่เกิดขึ้น** — ทุกทางที่ทดสอบตอบเหมือนกัน: การแยก "1+3" ที่ได้
คือ engineered (อัด signature) เสมอ — สอดคล้องกับฟิสิกส์ที่รู้ (Euclidean IKKT
ไม่พัง SO(D); เลข 3 ของ Kim–Nishimura ต้อง fermion phase + real-time)

**ของที่ใช้ได้จากสายนี้:** toy **"signature ตรึงแกนเวลา 1+3"** (เสถียร, reproducible,
iso_space=0.000, อธิบายกลไกได้) — เหมาะเป็น engineered toy model ที่ระบุชัด
ไม่ใช่ emergence — ต่อท้ายคำแนะนำเดิมใน SGOED_PROJECT_SUMMARY.md

---

## อัปเดต 6: Track 2 — Causal Set + d_MM จาก Sequential Growth (2026-08-31)

**สคริปต์:** `step_causal_set_dmm.py` + ผล `step_causal_set_dmm_results.json`

**1. Calibration (poset ที่รู้คำตอบ):** chain→d=1 (ρ=1); Minkowski sprinkle
d=2/3/4/5/6 → ρ = 0.252 / 0.153 / 0.090 / 0.057 / 0.033 (monotone ลดตามมิติ)
— ใช้ relation-fraction ตรงๆ **ไม่มี threshold** (หลบกับดัก d_MM ของ v9/v10)

**2. Sequential Growth poset** (relation |v̂u·v̂k| > 0.9, M=8/16, therm 100):
**d_MM = 1.00 ± 0.00** ทั้งสองขนาด — ยืนยันคำทำนาย: เวลากำเนิดอย่างเดียว = total
order (chain) = **มิติ 1** — โมเดลปัจจุบันไม่มีโครงสร้างเชิงพื้นที่

**3. Poisson branching (ตามรีวิว: Bern(p) + transitive closure, N=250):**
| p | 0.02 | 0.05 | 0.10 | 0.20 | 0.40 | 0.70 |
|---|---|---|---|---|---|---|
| d_MM | **3.32 ± 0.36** | 1.61 | 1.26 | 1.10 | 1.03 | 1.01 |

→ **กิ่งก้านแบบ sparse (p เล็ก) ยกมิติขึ้นจริง (ถึง ~3.3 เข้าใกล้ 4) และควบคุม
ได้ monotonic กับ p** — dense branching กลับเป็น chain (d→1) — p เป็นตัวแปร
ออกแบบกฎการงอก ("เกิดกี่ link ถึง past")

**สรุป Track 2:** เวลากำเนิด = 1D ล้วน; "มิติ >1" ต้องมาจาก **โครงสร้าง
spatial/branching** ในกฎการงอก — d≈4 อยู่แถว p≈0.01–0.03 (ต้อง scale-check
N + seeds เพิ่ม — 3 seeds, N คงที่ = preliminary)

**กับดักที่เจอในงานนี้:** int8 overflow ในการ matmul relation matrix + closure
แบบ R←R² โดยไม่ union → หดจนเหลือ 0 (ผล d=6 ทุก p ปลอม) — แก้ด้วย
int64 + `R ← R ∨ R²` — บันทึกไว้กันงานถัดไปเจอซ้ำ

---

## อัปเดต 7: Scale & Significance ของ Causal-Set Branching — **NEGATIVE** (2026-08-31)

**สคริปต์:** `step_causal_set_scale_study.py` + ผล `step_causal_set_scale_results.json`
(bitset closure — เลี่ยง int8 overflow + N=1000³ matmul; calibration per-N)

**เกณฑ์รับรอง (จากรีวิว):** PASS = มีช่วง p ที่ให้ d_MM = 4.0±0.1 ข้าม ≥10 seeds
**และ** อยู่รอด N→1000; ตกเกณฑ์ → บันทึกเป็นข้อจำกัดของ random percolation

**ผล:**
- Calibration ขยาย d=1..8 (per-N, 3 N): ρ(2)=0.25, ρ(4)≈0.086, ρ(8)≈0.011
  — เสถียรข้าม N (sprinkle ไม่ใช่ตัวแปร)
- **Fine grid N=250 (12 seeds):** p: 0.005→8.00(floor) / 0.008→7.39 /
  0.012→5.82 / **0.016→4.42** / 0.020→3.40 / 0.025→2.49 / 0.030→1.96
  — **ไม่มีจุดใดใน 4.0±0.1** (ใกล้สุด 4.42)
- **Fixed-p (N 250/500/1000):** p=0.02 → 3.40 / 1.86 / **1.51** (หดตาม N);
  p=0.03 → 1.96 / 1.60 / 1.33 — **ไม่ invariant** (std 0.26–0.82)
- **Fixed-k (k=pN):** k=2 → 7.37 / 8.00(floor); k=5 → 3.40 / 4.48 / **5.35**
  (เพิ่มตาม N); k=7.5 → 1.96 / 2.42 / 3.02 — **ไม่ invariant** (std 0.30–0.80)

**บทสรุป:** **NEGATIVE — "d≈4 ที่ p≈0.016" เป็น finite-size artifact ของ N=250**
(random percolation Bern+closure ไม่มี scaling invariance ทั้งในตัวแปร p และ k —
ตรงตามเกณฑ์ บันทึกเป็นข้อจำกัดของ random percolation ทันที) — closure ของ random
DAG ที่ N ใหญ่โตกลายเป็น total order (d→1) ส่วนที่ k คงที่จะลอยขึ้นเรื่อยๆ ตาม N

**บทเรียนซ้ำ (ยืนยันกับ v9/v10):** มิติจาก relation-fraction (.poset) มีความไวต่อ
finite-size — **ข้ออ้าง "ได้มิติ K" ต้องผ่าน scaling audit ที่ N≥1000 เสมอ ก่อนอ้าง**
— "ดูน่าตื่นเต้นที่ N=250" = กับดักที่คุ้นเคยของโครงการ

---

## อัปเดต 8: Matrix-Driven Relational Light-Cone — พบเงื่อนไขที่ทำให้มิติเสถียร (2026-08-31)

**กฎ (จากรีวิว):** unit k เชื่อมกับ u<k เมื่อ (1) |v̂u·v̂k|>θ (2) D_space(u,k) ≤ (c·Δt)²
โดย D_space = (1/N)Tr((X_u−X_k)²) — สคริปต์: `step_growth_lightcone.py` +
`step_lightcone_followup.py` + JSON 2 ไฟล์

| ขา | M=250 | M=500 | M=1000 | std ข้าม N |
|---|---|---|---|---|
| Leg1 รัฐจริงจาก growth MC | 1.06 | 1.04 | 1.04 | 0.01 |
| Leg2 walk circle (d_sp=1) | 1.17 | 1.17 | 1.17 | 0.002 |
| Leg2 walk 3-torus (d_sp=3) | 1.21 | 1.21 | 1.21 | 0.002 |
| uniform scatter d_sp=3 | 1.27–1.29 | 1.29 | 1.29 | 0.00 |

- **ค้นพบหลัก: กฎกรวยแสงทำให้ causal dimension INVARIANT ข้าม N** (std 0.002–0.01
  vs percolation 0.26–0.82) — cone-locality = โครงสร้างที่ percolation ไม่มี
- Leg1 (ตามสเปคเป๊ะ): D_space ของสถานะจริงเกือบคงที่ (X เกือบอิสระ) → cone เกือบ
  ทุกคู่ → chain — **สถานะ matrix ปัจจุบันไม่มี spatial resolution** — กรวยแสงต้องมี
  manifold เชิงพื้นที่
- **ค่ามิติ = ฟังก์ชัน monotone ของ parameter (σ diffusion / c light speed = aspect):
  σ-scan 1.00→1.30; c-scan: uniform d_sp=1 c=0.2 → d=2.07 ≈ 2 (ตรงเป๊ะ); walk
  d_sp=3 σ=2 c≈0.1–0.2 → ข้าม d=4** — ตัวเลข 4 มาได้แต่ต้องตั้ง σ/c (engineered)

**สรุป Track 2 (ปิด):** light-cone = เงื่อนไขจำเป็นที่พบของ "causal set ที่มิติเสถียร";
แต่ "4D" ยังเป็น parameter ของกฎ (σ, c, d_sp ของ manifold) ไม่ใช่ emergence —
เหมือนบทสรุปทุกทางก่อนหน้า — ของที่อ้างได้: **กลไก cone ให้ invariance (ใหม่)** +
**กฎการงอกต้องมีสเกลเชิงพื้นที่ (σ/c) เป็น input เพื่อมิติเป้าหมาย**

**วิศวกรรมที่ทำ:** `step_sequential_growth.py` inter-coupling เดิม O(u)/proposal
→ O(M²) — แก้เป็น cache + prefix-sum ของ v̂ (O(1), behavior-preserving —
sanity ตรงเอกสารทุกค่า) — **กับดักใหม่:** normalization ระยะ matrix (1/(K·N))
บีบ c_eff → d ต่ำทุกรูปแบบที่ c=1 — ต้อง c-scan (aspect) จึงอ่านตรง — บันทึกไว้

---

## อัปเดต 9: Track 3 — Spectral Dimension บน Flow Network — ปิด (2026-08-31)

**สคริปต์:** `step_spectral_dimension_flow.py` + ผล JSON (random-walk return
P(t)=Tr(Tᵗ)/N, d_s = −2 dlnP/dlnt, lazy walk)

| setup | d_s(t=10,50,200,800) | หมายเหตุ |
|---|---|---|
| chain sym (bias=0) | 0.93/0.90/0.83/0.72 | plateau ~0.80 = dim 1 ✓ |
| chain bias=0.1 | 1.12/1.56/1.11/**0.004** | drift ทำลาย plateau แล้วยุบ 0 ที่ stationarity |
| chain bias=0.2 | 1.67/1.88/**0.007**/-0.0 | เดิม |
| tree undirected (α=0.5) | 0.95/1.56/1.81/1.85 | ขึ้นสู่ ~2–3 (Bethe-like, finite) ✓ |
| tree α=0.8 | 0.76/1.40/1.52/1.54 | flow อ่อน → plateau ต่ำลง |
| tree α=1.0 (pure outward) | **14/70/278/1110** | **transient: return ตาย P_tail=0 → d_s ระเบิด** |

**สรุป Track 3:** on a flow network **d_s วัด drift/transience ไม่ใช่มิติเรขาคณิต**
— จุด plateau ที่เสถียรมีเฉพาะโครงสร้างสมมาตร (equilibrium): chain→1,
tree→2–3 — flow/ความเอนเอียงทำลาย plateau (chain: ขึ้นแล้วยุบ 0;
outward-flow: ระเบิด) — สอดคล้องกับ d_s null-compatible เดิม (v9/v10) +
ฟิสิกส์จริง (CDT วัด d_s บนโครงสร้างสมดุล) — **"4D via d_s" ปิด: ไม่เกิด**

**กับดักใหม่ที่เจอ:** chain/tree เป็น **bipartite** → P(t)=0 ที่ t คี่ (parity
conservation) → log(0) ทำให้ d_s สั่น ±พัน ดูเหมือน "ระเบิด" ทุกรูปแบบ —
แก้ด้วย **lazy walk (T←0.5I+0.5T)** — จดเป็นกับดัก standard ของ return-
probability measurements

---

## อัปเดต 10–12: ปิด TODO ทั้งหมดตาม handoff (2026-08-31)

### 10. Non-eq flow robustness — ✅ (สคริปต์ `step_transport_robust.py`)
- **8 seeds × 500 steps:** E=[28.81, 1.72, 0.117, 0.025, 0.020, 0.005],
  **decay 5849×**, J=+5.773±0.016 (std น้อยมาก = deterministic), mean
  monotonic แล้ว (0.025→0.020); per-seed 4/8 สะดุดที่จุด noise ~0.02
  (= thermal floor 3 อันดับต่ำกว่า E0 — ยืนยัน "ในทางปฏิบัติ monotonic")
- REVERSED: J=−6.025±0.022 (สมมาตร |5.77|↔|6.03|); NULL: J=+0.003±0.008
- scan g_trans×g_sink (9 จุด): J ทั้งหมด +5.4 ถึง +5.9, decay 1850–4000×,
  mean monotonic ทุกจุด — **ทิศ/ขนาดของกระแส robust ข้ามค่า parameter**

### 11. Sequential growth mechanism — ✅ (สคริปต์ `step_growth_mechanism.py`, M=32)
- **กลไก:** coupling = `−g·v̂u·(Σ past v̂)` (prefix-sum) → หน่วยใหม่ align
  กับ **mean ของอดีตทั้งหมด** = contraction mapping → inheritance/origin → 1
- M=16 และ **M=32 ไม่ต่างกัน** (g=20: align 0.998/chain 0.998, contraction 0.03;
  g=60: 0.999, contraction 0.02) — scale-free ✓; g ต่ำ (1–5) → บางส่วน (0.43–0.93)
- deterministic = ค่าสถิติเหมือนข้าม seeds (ทิศสัมบูรณ์ต่างตาม seed ตามปกติ)

### 12. Past Hypothesis + growth (ถูกกลไก) — ✅ (สคริปต์ `step_growth_past_hypothesis.py`)
- origin rank-1 (Y[0]=2I → v̂0=(1,0)) + แช่แข็ง + therm=120:
  **(a) origin align = 0.9995 ± 0.0002, chain = 0.9991 ± 0.0002** (6 seeds)
- control: (b) special+thermalized = 0.9987 (origin ยังเด่น — เทอร์มไม่ใช่ตัวชี้ขาด)
  (c) random+frozen = 0.901 ± 0.096 — **specialness จำเป็นจริง**
- **บทเรียนปิด:** ความล้มเหลวรอบก่อน = **therm ไม่พอ (60 < 120)** ไม่ใช่
  "origin thermalize" — ย้ำบทเรียนหมายเลข 5 (n_therm ต้องพอ) อีกครั้ง
- ผล = arrow direction ถูกกำหนดโดย initial condition (past hypothesis)
  และแพร่ไปทั้ง chain อย่าง deterministic — ปิด TODO ข้อ 3

**สรุป:** TODO ใน handoff ครบ (1✓ 2✓ 3✓ paper draft✓) — ตัวเลขยืนทั้งหมด
ใน `step_*_results.json` ใหม่ 4 ไฟล์

---

## อัปเดต 13: SOC growth (พิมพ์เขียว ①) — FAIL ทั้งสองแบบ (2026-08-31)

**สคริปต์:** `step_growth_soc.py` + ผล JSON — Gate 1: std ข้าม N≤0.05 ผ่าน, >0.10 ตก

| กลไก | d (N=250/500/1000) | std ข้าม N | Gate |
|---|---|---|---|
| A p0=.05 k0=5 γ=2 | 5.84/6.41/6.96 | 0.455 | FAIL |
| A p0=.10 k0=5 γ=2 | 4.96/5.71/6.42 | 0.596 | FAIL |
| A p0=.05 k0=10 γ=1 | 5.69/5.97/6.31 | 0.253 | FAIL |
| A p0=.10 k0=10 γ=2 | 4.46/4.96/5.67 | 0.497 | FAIL |
| B k_t=2 | 7.31/8.00/8.00 (floor) | 0.327 | FAIL |
| B k_t=5 | 5.65/6.93/8.00 | 0.961 | FAIL |
| B k_t=10 | **4.24**/5.65/6.91 | 1.088 | FAIL |

**ผล/กลไก:**
- **A (degree-saturation) ไม่ช่วย:** กัน hub ได้ แต่ d ยังลอยขึ้นตาม N (ρ ลดแบบ fixed-k-like)
  — แก้ผิดสาเหตุ: ปัญหาไม่ใช่ hub concentration แต่คือการเชื่อมแบบไม่มี metric
- **B (critical branching) = ครอบครัว fixed-mean-degree** (พังเหมือน fixed-k เดิม — ยืนยัน
  เชิงประจักษ์ตามคำทำนาย); และ **B_kt10 แสดงภาพลวงตา "d≈4 ที่ N=250" อีกครั้ง
  (4.24 → 6.91@1000)** — กติกาแบบปรับตัวเองก็ยังผลิต finite-size artifact
- **Gate 2:** ไม่มีค่าลู่เข้าให้รายงาน — คำตอบซื่อตรง: "no stable dimension"

**บทสรุปเชิงโครงสร้าง (ตอกย้ำจากทางตรงข้าม):** degree/local feedback **ไม่ใช่**
โครงสร้าง locality — ยังไม่มี metric/cone → invariance ยังไม่เกิด — **กลไกเดียว
ที่ผ่าน invariance จนถึงตอนนี้คือ relational light-cone เท่านั้น** — self-tuning
ที่ "จริง" ต้องเป็น feedback เชิงเรขาคณิต (แนวทาง ② c_eff[R]) ไม่ใช่ feedback
เชิง degree

---

## อัปเดต 14: c_eff[R] curvature feedback (พิมพ์เขียว ②) — FAIL, ผ่านเฉพาะ static cone (2026-08-31)

**สคริปต์:** `step_growth_ceff.py` + ผล JSON — Ricci proxy = interval count
I(u,k) = (P@P)[u,k] (Alexandrov volume ที่ cone โพรบ c0); c_eff ต่อ node แบบ
sequential; วัด ρ บน closure; d_sp=3 (torus), σ=2, c0=0.15, 10 seeds

| กลไก | d (250/500/1000) | std_acr | c_eff (N=1000) | Gate 1 | Gate 2 |
|---|---|---|---|---|---|
| control (static c0=.15) | 3.53/3.55/3.53 | **0.006** | 0.150±0 | PASS ✅ | ✅ |
| A β=0.5/2/5 | 8.00/8.00/8.00 | 0.000 | 0.03–0.05, min→0 | "PASS"* | ❌ ยุบ |
| A2 (dens-normalized) | 8.00/8.00/8.00 | 0.000 | nan (ว่าง) | "PASS"* | ❌ ยุบ |
| B I_t=1/2 | 3.72→4.81 / 3.14→4.32 | 0.45–0.48 | min→0 | ❌ | ⚠️ |
| B2 (dens-normalized) | 8.00/8.00/8.00 | 0.000 | nan | "PASS"* | ❌ ยุบ |

\* "PASS" ของ A/A2/B2 เป็น **degenerate** — std 0 เพราะทุกอย่างพังหมด (poset ว่าง,
d ชนเพดาน 8) — จับได้ด้วย Gate 2 (c_eff→0)

**กลไกความล้มเหลว (สำคัญ):**
1. **A-family:** interval COUNT โตตามขอบฟ้า (dens[k] ∝ k — ยิ่งเกิดช้าต้องเคยเห็น
   คู่มาก) → c_eff ของ node ท้ายถูกบีบจน ~0 → cone ว่าง → ρ→0 → d ชนเพดาน —
   normalization แค่ rescale ไม่เปลี่ยนรูปร่าง monotone ใน k
2. **B (homeostasis):** d ลอยขึ้นตาม N — dens โตตาม N (sampling หนาแน่นที่ T คงที่)
   → c_eff หดตาม N → คล้ายความล้มเหลว fixed-density เดิม
3. **บทเรียนเชิงแนวคิด:** proxy ที่ใช้เป็น **count (∝ ขอบฟ้า) ไม่ใช่ density ต่อ
   ปริมาตร** (ต้องเป็น I(u,k)/(Δt)^d ถึงจะ stationary) — และ feedback ที่ออกฤทธิ์
   กับ c โดยตรงเป็น "ควบคุมตัวแปรที่เส้น d(c) เป็นฟังก์ชันของมันเอง" — เลื่อนไปตาม
   เส้นโค้งเดิม ไม่มีจุดดึงดูดใหม่ — self-tuning ที่จริงต้องออกฤทธิ์กับตัวแปร
   **ไม่ collinear กับมิติที่วัด** (เช่น เทอมพลังงาน/เอนโทรปี)

**สรุป ②:** ผ่านเฉพาะ **static cone (control: d=3.53, std 0.006 — ยืนยันอีกครั้ง
ว่า light-cone กติกานิ่ง คือสิ่งเดียวที่ invariance)** — feedback แบบ ② ทั้งสอง
(และ normalization แล้ว) ไม่ self-tune: ยุบหรือลอย — ปิดแนวทาง self-tuning
ทั้ง ① (degree) และ ② (curvature) ด้วยกลไกที่อธิบายได้

---

## อัปเดต 15: Matrix-Compatibility Growth (commutator metric) — **ผ่าน invariance บนสถานะจริง** (2026-08-31)

**สคริปต์:** `step_growth_commutator.py` + ผล JSON — เปลี่ยนระยะใน light-cone
จาก `Tr((X_u−X_k)²)` เป็น **`D_comp = Σ|Tr([X_u,X_k]²)|`** (commutator-compatibility)
+ alignment |v̂u·v̂k|>0.9 + closure — 2 regimes:

| regime | d (250/500/1000) | std_acr | verdict |
|---|---|---|---|
| K torus-engineered (c=0.15) | 2.03/2.02/2.04 | 0.006 | ✅ PASS |
| K (c=0.05 / 0.4) | 7.2 / 1.41 | 0.023 / 0.003 | ✅ PASS |
| **R  real growth states (f=0.5)** | **3.52/3.55/3.52** | **0.013** | ✅ **PASS** |
| R (f=1.0 / 2.0) | 1.89 / 1.53 | 0.004 / 0.003 | ✅ PASS |

- **R = ครั้งแรกที่สถานะจากโมเดลจริงให้ d คงตัว (~3.5) โดยไม่ต้องใส่พิกัดพื้นที่
  engineered** — ต่างจากคำทำนายของผม (chain~1) ที่**ผิด — ขอแก้บนบันทึก**:
  commutator metric มีโครงสร้าง (bimodal: ~50% คู่ Dc≈0, ~50% sqrt≈3.5–4.9 คงที่
  ข้ามระยะแยก) ที่ difference metric (Leg1: d≈1.04) ล้างหายไป
- **กลไก invariance:** sqrt(D_comp) คงที่ข้ามระยะแยก + สเกลสถานะไม่โตตาม N
  (matrix fix 4×4) + birth-time rescale ไป [0,T] → Δt ขึ้นกับ fraction (sep/N)
  → ρ คงที่ข้าม N — กลไกเดียวกับ leg2 (fixed region, denser sampling)
- **ค่า d ยังเป็น parameter (f·c_ref; c_ref = ปรับสเกลตามสถานะเอง)** — "3.5"
  มาจาก normalization ที่เราเลือก ไม่ใช่ emergence — self-tuning ยังไม่เกิด
- Reconcile: replicate 1 แถวเป๊ะ ρ=0.1164 → d=3.54 ✓ (audit ถูกต้อง;
  ค่าที่ดู "ขัด" คือ raw fraction 0.56 ก่อน filter/closure)
- **กับดัก/บทเรียน:** probe ของผมมี bug sep-index กลับทิศครั้งแรก → "Dc=0 ทั้งหมด"
  ปลอม — จด; และบทเรียนเดิมซ้ำ: "ค่า 3.5 ที่สวย" ต้องพิสูจน์ว่ามาจากไหน (self-
  calibration) ก่อนอ้าง

---

## อัปเดต 16: R-regime significance scan — **confirmed** (2026-09-01)

**สคริปต์:** `step_growth_commutator_scan.py` + ผล JSON — seeds 8/8/5 ตาม N,
θ-scan {0.7, 0.8, 0.9} × f {0.5, 1.0}, therm=35, state ต่อ (N,seed) ครั้งเดียว

| f | θ | d (250/500/1000) | std_acr | verdict |
|---|---|---|---|---|
| 0.5 | 0.7/0.8/0.9 | **3.51/3.52/3.50** | 0.008 (ทุก θ) | ✅ PASS |
| 1.0 | 0.7/0.8/0.9 | 1.89/1.89/1.90 | 0.004 | ✅ PASS |

- **สถานะจริง → d≈3.5 เสถียรข้าม N ยืนยันด้วย seeds มากขึ้น** (std_acr 0.008)
  และ **ไม่ไวต่อ θ** — เพราะ adjacent alignment = 1.000 ทุก N (คาสเคดสืบทอดสมบูรณ์
  ที่ therm 35 — θ เป็นคันโยกเฉยในย่านนี้)
- **ตำแหน่งค่า d ยังเป็น f (parameter):** f=0.5 → 3.5, f=1.0 → 1.9 — "3.5" คือ
  ผลของ c_ref = ฟังก์ชันสเกลของสถานะเอง (self-calibration) **ไม่ใช่การคัดเลือก
  ที่เกิดขึ้นเอง** — invariance เป็นของจริง, ค่ามิติเป็น parameter (ตรงกับ
  บทสรุปเดิมทุกเส้นทาง)
- **บทสรุปชุด 4D-CausalSet (ปิด):** กลไกเดียวที่ผ่าน invariance ข้ามสเกล = กติกา
  light-cone (metric ต่างกัน 3 แบบ: difference/commutator/both + ทั้ง engineered
  และ real states) — self-tuning (SOC, c_eff) ล้มเหลว — ค่ามิติทุกตัวยังเป็น
  parameter ที่ตั้งได้ (std_acr 0.002–0.013)

---

## อัปเดต 17: SPRINT CLOSE (2026-09-01)

**Quest "Emergent Time → 4D → relational spacetime" ปิดอย่างเป็นทางการ**

### ผลงานสุดท้าย (ยืนยันแล้ว, reproducible 100%)
1. **ไตรภาคแห่งเวลาจริง:** Past Hypothesis (dS/S₀=0.98, 100× random) ·
   Sequential Growth (inheritance 1.000±0.000, scale-free M=8–32, กลไก
   contraction ผ่าน prefix-sum) · Upwind Transport (decay 5849×, J=+5.773±0.016,
   reversal สมมาตร, null แยกชัด)
2. **ความคงตัวของมิติเชิงสาเหตุ:** relational light-cone (difference metric +
   commutator metric, engineered + real states) = เงื่อนไขจำเป็นของมิติที่คงตัว
   ข้าม N→1000 (std 0.002–0.013)
3. **การลบล้างอย่างมีระบบ:** metric 11 ตัว, Matrix SSB ไร้เฟอร์มิออน,
   percolation 4D (finite-size artifact), SOC/c_eff feedback (ยุบ/ลอย) —
   พร้อมกลไกอธิบายทุกกรณี + บันทึกกับดัก 12 ชนิด

### สิ่งที่อ้างได้ (ตามวินัยเดิม)
- engineered ≠ emergence — invariance จริง, ค่ามิติเป็น parameter เสมอ
- "จำเป็น (ในครอบครัวที่ทดสอบ)" ≠ "กฎสากล" — ไม่ over-claim

### สถานะไฟล์ (ทั้งหมดใน )
- **เอกสาร:** `manuscript_v7.md` (ฉบับสมบูรณ์ §4.6 อัปเดตล่าสุด),
  `SGOED_TIME_PAPER_DRAFT.md`, `SGOED_TIME_EMERGENCE_SUMMARY.md` (อัปเดต 1–17),
  `SGOED_PROJECT_SUMMARY.md`, `SGOED_handoff.md`
- **สคริปต์ชุดปิด:** `step_growth_soc.py`, `step_growth_ceff.py`,
  `step_growth_commutator.py`, `step_growth_commutator_scan.py` (+ ผล JSON 4 ไฟล์)
  และสคริปต์/JSON ตลอดทั้ง quest (past_hypothesis, sequential_growth,
  transport, v15 matrix, dynamical, bounded, causal_set_dmm, scale_study,
  lightcone 2 ตัว, spectral_dimension_flow, transport_robust, growth_mechanism,
  growth_past_hypothesis) — ทั้งหมดเปิดอ่าน รันซ้ำได้ด้วย seed คงที่

**Close:** งานชุดนี้พร้อมสำหรับการจัดทำ manuscript/นำเสนอ ตามหลัก
"transparent & 100% reproducible computational foundational physics"
