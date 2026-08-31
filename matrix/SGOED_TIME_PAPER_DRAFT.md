# SGOED V5 — Paper Draft: "Arrow of Time" (รวบรวมผลทั้งหมด, 2026-08-31)

เส้นทาง quest "เวลาจริง" สู่ 4D — ร่างโครงบทความ + ตารางข้ออ้าง (ซื่อตรง: engineered ≠ emergence)

---

## 1. โจทย์และกรอบ

SGOED = โมเดลมหภาค toy ที่ถามว่า "ลูกศรเวลาเกิดจากโครงสร้าง relational
(ไม่ต้องสมมุติ spacetime เป็นหลัง) ได้หรือไม่" — กรอบ: matrix/graph/poset
Monte Carlo + Langevin — ผลทั้งหมด reproducible, N ขนาดเล็ก (4–1000), บน CPU

**กฎกลางที่พิสูจน์ด้วย metric 11 ตัว:** Equilibrium Monte Carlo เป็น
time-symmetric — arrow ไม่ออกมาจาก final state ไม่ว่าคัปปลิงแบบใด —
"เวลาจริง" จึงต้องมาจาก (1) initial condition พิเศษ (2) process ที่
asymmetric โดย construction

## 2. ระเบียบวิธี (บังคับทุก observable)

1. Reproduce → 2. Significance (seeds ≥ 10; 5 มักไม่พอ — v13: 2.3σ→1.2σ)
3. Null test → 4. Labeling/permutation → 5. Thermalization (n_therm พอ)
6. Mechanism — อธิบายได้ว่าทำไม

**กับดักที่เจอทั้งหมด:** R≈0.5 = histogram artifact; d_MM/d_s = null-
compatible; D = labeling-dependent; λ_c สูงเกินถ้า therm ไม่พอ; Tr(X⁴)
ระเบิดถ้าไม่ normalized; int8-overflow ในการ matmul relation matrix;
closure แบบ R←R² (ไม่ union) หดจน 0; normalization ระยะ matrix บีบ c_eff;
finite-size ("d≈4 ที่ N=250" = artifact — ต้อง audit N→1000)

## 3. ผลที่ยืนจริง — "เวลาจริง 3 ทาง" (อัปเดต 1–4 ใน TIME_EMERGENCE_SUMMARY)

| แนวทาง | ผล | ตัววัด | ผ่าน |
|---|---|---|---|
| Past Hypothesis | initial low-entropy (rank-1) → dS/S0 = 0.98 (แรง 100× random) | S ลด 344→7, deterministic | ✅ |
| Sequential Growth (CSG-style) | birth order + past frozen → chain inheritance **1.000 ± 0.000** | deterministic, M=8/16 | ✅ |
| Non-Equilibrium Flow (upwind) | decay **4000×** (28.85→0.007) + reversal สมมาตร (+5.75/−5.98) + null (J≈0) | deterministic (2 seeds 28.86/28.83) | ✅ |

**กลไก:** arrow = กรวยความสัมพันธ์เชิงสาเหตุที่ asymmetric โดย
construction — inheritance และ transport ทิศเดียว — **แต่เป็น engineered
(ใส่กฎ asymmetric เข้าไปเอง)** — อ้างได้ว่าเป็น "กลไกตัวอย่าง" ไม่ใช่ emergence

## 4. การสอบสวน "4D" — ผลลบ + ค้นพบโครงสร้าง (อัปเดต 5–8)

### 4.1 Matrix SSB แบบ IKKT/Kim–Nishimura — ปิด (engineered)
- commutator term มีอยู่แล้วใน action_v7; กลไกเลือกมิติ = v̂ steering (engineered)
- Equilibrium D=4/10 ไม่มี v̂ → isotropic หมด (ratio ~1.05)
- pseudo-Euclidean (η=−1,+) → แยก 1+3 เสถียร (iso_space = 0.000) แต่เป็นการอัด
  signature + เวลาหด; D=10 → พื้นที่ขยายทั้ง 9 (ไม่มี "เลข 3")
- Dynamical (T=clock): bosonic Lorentzian unbounded (runaway 2000–8700) —
  ต้อง fermion/phase regulator (ตรงกับฟิสิกส์จริง) — ไม่มีในสเกล toy
- Bounded-regulator (saturating comm): สมดุล + สมมาตรเต็ม (top3-gap 1.06);
  control ตรวจจับผ่าน (1.14) → "ไม่เกิด 3-of-9" = negative ที่ตรวจสอบได้

### 4.2 Causal Set d_MM (Track 2)
- calibration d=1..8 (ρ: 0.25/0.086/0.011 สำหรับ 2/4/8) — เสถียรข้าม N
- Sequential growth poset → d_MM = **1.00** (chain — เวลากำเนิด = 1D ล้วน)
- **Random percolation (Bern+closure) — NEGATIVE:** "d≈4 ที่ p=0.016" เป็น
  finite-size artifact ของ N=250 — พังทั้ง fixed-p (d: 3.40→1.51@1000) และ
  fixed-k — บันทึกเป็นข้อจำกัดของ random percolation (null test ผ่าน)
- **Matrix-Driven Light-Cone (ค้นพบ):** กฎกรวยแสง (D_space = (1/N)Tr((X_u−X_k)²)
  ≤ (c·Δt)² + alignment) ให้ **causal dimension INVARIANT ข้าม N**
  (std 0.002 vs 0.26–0.82 ของ percolation) — cone-locality = เงื่อนไขจำเป็น
  ของมิติเสถียร — แต่ค่า d = ฟังก์ชัน (σ diffusion, c light speed, d_sp manifold):
  c-scan เล่นได้ตั้งแต่ 1 จนข้าม 4 (σ-scan 1.00→1.30) — มิติเป็น parameter
  (engineered) ไม่ใช่ emergence — Leg1 (สถานะจริง) = chain เพราะ X เกือบอิสระ
  (โมเดลยังไม่มีโครงสร้างเชิงพื้นที่)
- **Commutator-compatibility metric (ใหม่ — ปิด Track ด้วยการยืนยัน):** เปลี่ยน
  ระยะเป็น D_comp = (1/(d_sp·N))·Σ|Tr([X_u,X_k]²)| ใช้**สถานะจาก growth จริง
  โดยตรง** (ไม่มี torus ประกอบ) → **invariance ข้าม N: d = 3.51/3.52/3.50,
  std = 0.008** (8/8/5 seeds) — θ-scan ไม่มีผล (adjacent alignment = 1.000) —
  ครั้งแรกที่สถานะจริงให้มิติคงตัว (~3.5) — **แต่ค่า d ยัง parameter-steered
  (f·c_ref; self-calibration ของสเกลสถานะ; f=1.0 → 1.9)** — ขอบเขตอ้าง:
  "ความคงตัวของเรขาคณิตเป็นจริง; การคัดเลือกค่ามิติ (spontaneous selection)
  ยังไม่เกิด" — สคริปต์ `step_growth_commutator.py` + `step_growth_commutator_scan.py`

### 4.3 Spectral Dimension บน Flow Network (Track 3) — ปิด
- d_s (return probability, lazy walk) บน chain: สมมาตร → plateau ~1 ✓
- bias/flow ทำลาย plateau (chain: ขึ้นแล้วยุบ 0 ที่ stationarity)
- tree: undirected → ~2–3 (Bethe-like ✓); pure outward-flow → **transient
  d_s ระเบิด (14→1110)** — flow วัด drift/transience ไม่ใช่มิติ
- สอดคล้อง d_s null เดิม (v9/v10) + CDT (วัดบนโครงสร้างสมดุล) — ปิด "4D via d_s"

## 5. ตารางข้ออ้าง (เขียน paper ใช้ตรงนี้)

| อ้างได้ | อ้างไม่ได้ |
|---|---|
| Equilibrium MC ไม่ให้ arrow (negative, 11 metric + กลไกอธิบาย) | "arrow of time emergent" — 3 ทางเป็น engineered |
| เครื่องมือ reproducible: condensation v7 (λmax/λ2nd=23, ~60σ), bistability | "4D spacetime emergence" (ทุกเส้นทาง) |
| d_MM = 1 ของ chain growth (เชิงปริมาณ) | "d≈4 ทุกมาตร" (finite-size/parameter) |
| Percolation ไม่มี scaling invariance (NEGATIVE + null ผ่าน) | "random percolation ≈ 4D causal set" |
| Light-cone = เงื่อนไข invariance ของ causal dimension (ค้นพบใหม่) | "กฎนี้ให้ 4D" — ต้องตั้ง σ/c |
| กับดัก/บทเรียนระเบียบวิธี (มีคุณค่าเชิงระเบียบวิธี) | engineered toy = emergence |

## 6. โครงร่างบทความที่เสนอ (manuscript_v7)

1. Intro: ทำไม time ไม่เกิดจาก equilibrium structure; quest
2. Methods: โมเดล (matrix units, Langevin, growth, poset) + ระเบียบวิธี 6 ขั้น
3. Results A: เวลาจริง 3 ทาง (Past Hypothesis / Sequential Growth /
   Non-Equilibrium Flow) — engineered toy models + deterministic
4. Results B: negative 4D — matrix SSB, bounded regulator, dynamical,
   percolation scale audit (finite-size artifact)
5. Results C: light-cone invariance (โครงสร้างที่ทำให้มิติเสถียร) + parameter map
6. Discussion: engineered ≠ emergence; บทเรียน null/labeling/scale audit;
   ทางออกจริงต้อง fermion-like structure หรือ spatial structure ในกฎการงอก
7. Appendix: ผลตัวเลขเต็ม + ไฟล์/สคริปต์อ้างอิง

**หมายเหตุ:** manuscript_v6 (matrix v7+condensation) มีอยู่แล้ว — ร่างนี้ต่อยอด
เป็น "part 2: time-arrow และ負 results" หรือผสานเป็น论文เดียว

## 7. ไฟล์อ้างอิง (ทั้งหมดใน V5/)

- `matrix/SGOED_TIME_EMERGENCE_SUMMARY.md` — ผล + อัปเดต 1–8 (หลัก)
- `SGOED_PROJECT_SUMMARY.md` — โครงการ v6–v14 + 6 ขั้น
- `matrix/SGOED_handoff.md` — สถานะและ TODO
- สคริปต์: `step_past_hypothesis.py`, `step_sequential_growth.py`,
  `step_langevin_transport_tuned.py`, `sgoed_matrix_v15.py`,
  `step_v15_dynamical.py`, `step_v15_bounded.py`, `step_causal_set_dmm.py`,
  `step_causal_set_scale_study.py`, `step_growth_lightcone.py`,
  `step_lightcone_followup.py` (+ JSON ผลทุกตัว)