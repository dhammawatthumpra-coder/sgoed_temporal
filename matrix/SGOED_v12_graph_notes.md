# SGOED-Relational v12: Graph with Non-Linear SVD Condensation — บันทึกผลการวิจัย

วันที่: 31 สิงหาคม 2026 · สถานะ: ผลสมบูรณ์ (ผ่านการทดสอบ Discrimination, Full Scaling & 4-Mode Ablation Study)
สคริปต์ประมวลผลหลัก: `sgoed_graph_core_v12.py` / `audit_v12_full_battery.py` / `audit_v12_ablation.py`

---

## 🌟 1. บทนำและสถาปัตยกรรม v12 (The Breakthrough)

ในเวอร์ชันก่อนหน้า (v8) โครงสร้าง Graph มีข้อจำกัดที่ขาด Non-linear Positive Feedback ทำให้เกิดเพียง Histogram Asymmetry แต่ไม่มีทิศทางเวลาจริง ($D \approx 0$)

ใน **v12 Graph Core** เราได้แก้ปัญหานี้อย่างสมบูรณ์แบบด้วยการเพิ่ม **Non-linear Positive Feedback 2 ตัว**:
1. **Quartic Observer Coupling ($S_{\text{coupling}}^{\text{quartic}}$):** $-g_{XY} \sum_a \hat{v}_a \sum_j W_{aj}^4$ (พจน์กำลัง 4 บีบให้เกิด Single Dominant Outflow)
2. **Exact SVD Quartic Condensation ($S_{\text{cond}}$):** $-\lambda_{\text{cond}} \mathrm{Tr}((W W^T)^2) = -\lambda_{\text{cond}} \sum_i \sigma_i^4$ (บีบให้เกิด **Rank-1 SVD Dominance / Super-Hub** เหมือนกับพจน์ $\mathrm{Tr}(X^4)$ ใน Matrix Model)

---

## 📊 2. ผลการทดลอง Full Scaling Battery ($N = 8 \to 48$, 5 Seeds, $n_{\text{therm}}=120$)

| ขนาดระบบ ($N$) | เวลาประมวลผล (ต่อ seed) | **Spectral Ratio ($\sigma_1 / \sigma_2$)** | Uncoupled Baseline Ratio | **Net Direction ($D$)** | Baseline $D$ | Flow Alignment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$N = 8$** | 0.85 วินาที | **3.40 $\pm$ 1.08** | 1.46 | **-1.2** | +4.2 | **100.0%** |
| **$N = 16$** | **0.13 วินาที** | **7.31 $\pm$ 0.34** | 2.44 | **-12.9 $\pm$ 15.0** | -0.6 | **100.0%** |
| **$N = 24$** | 0.88 วินาที | **10.30 $\pm$ 0.30** | 2.88 | **-58.7 $\pm$ 23.7** | +2.0 | **100.0%** |
| **$N = 32$** | 3.35 วินาที | **12.82 $\pm$ 0.61** | 3.19 | **-134.9 $\pm$ 23.7** | +8.2 | **100.0%** |
| **$N = 48$** | 25.43 วินาที | **12.60 $\pm$ 0.46** | 3.66 | **-287.4 $\pm$ 66.2** | +5.0 | **100.0%** |

---

## 🔬 3. ผลการทดลอง Ablation Study: Engineered vs True Emergence (10 Seeds, $n_{\text{therm}}=120$)

เพื่อตอบคำถามเชิงแนวคิดว่า "ลูกศรเวลาและ Condensation เกิดจากอะไร และพจน์ SVD มีความจำเป็นอย่างไร":

| สถาปัตยกรรม Model | $N=16$ ($D \mid \text{Spec}$) | $N=24$ ($D \mid \text{Spec}$) | $N=32$ ($D \mid \text{Spec}$) | บทสรุปทางฟิสิกส์ |
|---|---|---|---|---|
| **1. Uncoupled Null** ($g_{XY}=0, \lambda=0$) | $-0.6 \pm 11.5 \mid 2.44$ | $+2.0 \pm 18.1 \mid 2.88$ | $+8.2 \pm 23.6 \mid 3.19$ | สมมาตร ไร้ลูกศรเวลา ($D \approx 0$) |
| **2. Quartic Coupling ONLY** ($\lambda=0$) | $-34.0 \pm 13.9 \mid 3.07$ | $-49.0 \pm 22.0 \mid 2.34$ | $-34.0 \pm 18.6 \mid 2.45$ | ⚠️ D = 1.8–2.5σ (**ไม่ significant**) และไม่สเกลตาม N; Spec ไม่สูงกว่า baseline → **ไม่ยืนยัน "Pure Emergence"** |
| **3. Relational Observer SVD** | $-37.8 \pm 8.6 \mid 3.72$ | $-62.4 \pm 18.8 \mid 2.58$ | $-65.1 \pm 26.4 \mid 3.08$ | D แรงกว่า mode 2 เล็กน้อย (2.5–4.4σ) แต่ Spec ยังเท่า baseline → ไม่สร้าง condensation |
| **4. Global SVD (Full v12)** | $-12.9 \pm 15.0 \mid 7.31$ | $-58.7 \pm 23.7 \mid 10.30$ | $-134.9 \pm 23.7 \mid 12.82$ | ✅ Spec = **condensation จริง (27–95σ)**; D significant เฉพาะ N=32 (5.7σ) — N=16/24 ยังอ่อน (0.9σ/2.5σ) |

---

## 🧠 4. การตกผลึกทางวิทยาศาสตร์ (The Final Verdict — หลังตรวจ significance)

1. **Quartic coupling อย่างเดียว ไม่ยืนยัน "True Emergence":**
   - D = −34…−49 มี significance แค่ **1.8–2.5σ** (10 seeds) และ **ไม่สเกลตาม N** (−34/−49/−34)
   - Spec ของ mode 2/3 (2.34–3.72) **ไม่สูงกว่า baseline** (2.44–3.19) → quartic coupling คนเดียว
     **ไม่สร้าง condensation** — ข้อสรุปเดิม "Pure Emergence" ถูกถอน (ดู §5)
2. **SVD Global term เป็นต้นตอของ condensation จริง:**
   - พจน์ $\mathrm{Tr}((WW^T)^2)$ (mode 4) เพียงตัวเดียวที่ให้ Spec = 7.31 → 12.82 (แยกจาก
     baseline 27–95σ) — condensation และ super-hub มาจาก term นี้
   - D ของ mode 4 เป็นลบทุก seed ที่ N ≥ 24 (N=32: −134.9 ± 23.7 = **5.7σ**) แต่ที่ N=16/24
     ยังอ่อน (0.9σ / 2.5σ) — "Macroscopic Arrow" ยังต้อง seeds มากขึ้นเพื่อยืนยัน N=24/48
3. **เชิงแนวคิด (สำคัญ):** condensation ยังเป็น **engineered** (λ_cond ถูกใส่ใน action โดยตรง)
   — การตัด term ทิ้ง (mode 2/3) ทำให้ไม่มี condensation → **ยังไม่ใช่ emergence**
4. **ความเร็ว:** SGOED-Relational v12 รวมความเร็วของ Graph Model เข้ากับพลวัต Eigenmode
   Condensation (เฉพาะเมื่อเปิด λ_cond) — ข้อเท็จจริงเชิง engineering ยังคงอยู่

---

## 🔍 5. การตรวจสอบความซื่อตรง (Data Honesty Audit — 2026-08-31)

สคริปต์ตรวจ: `check_v12_baseline_significance.py`, `audit_v12_ablation.py` (reproduce ตรงทุกค่า)

### 5.1 Reproduce
- Full battery: σ 3.40/5.97/8.31/10.15/12.60, D −1.2/−10.4/−62.2/−153.8/−280.0 (n_therm=40) — ตรง
- Ablation (n_therm=120, 10 seeds): ทุกค่าตรง JSON (D, spec, std) — reproducible 100%

### 5.2 Significance ของ D (สำคัญที่สุด — ablation เปิดเผย)
| Mode | N=16 | N=24 | N=32 |
|---|---|---|---|
| 2 (quartic only) | −34±14 → 2.5σ | −49±22 → 2.2σ | −34±19 → 1.8σ |
| 3 (relational) | −38±9 → 4.4σ | −62±19 → 3.3σ | −65±26 → 2.5σ |
| 4 (full SVD) | −13±15 → **0.9σ** | −59±24 → 2.5σ | −135±24 → **5.7σ** |

→ "ลูกศรเวลา" มีนัยเฉพาะ mode 4 ที่ N=32 (5.7σ) — mode 2/3 ที่เคยสรุป "True Emergence"
ไม่ถึงเกณฑ์ 3σ และ D ไม่สเกลตาม N → **ข้อสรุป "Pure Emergence" ถูกถอน**

### 5.3 Condensation มาจาก global SVD term เท่านั้น
Spec: mode 2/3 (2.34–3.72) ≈ baseline (2.44–3.19) — ไม่เพิ่ม; mode 4 (7.31–12.82) = 27–95σ
→ ตัด λ_cond ทิ้ง = ไม่มี condensation → **ยังเป็น engineered term ไม่ใช่ emergence**

### 5.4 สิ่งที่ยังต้องทำก่อนสรุป "Macroscopic Arrow of Time"
- N=24/48: ต้อง seeds เพิ่ม (std_D ใหญ่ — N=48 ±66)
- Thermalization: n_therm 40→120 spec ยังไต่ (9.22→12.29@N32) — ตรวจ n_therm 240 เพิ่ม
- กลไก D<0 ยังไม่ได้วิเคราะห์เชิงโครงสร้าง (ทำไมเป็นลบ — observer source/sink?)

### 5.5 สรุปสถานะ v12
- ✅ condensation (spec) + bias เชิงลบของ D (ทุก seed N≥24) — ข้อเท็จจริง reproducible
- ⚠️ ยังไม่ใช่ emergence (λ_cond engineered); significance ของ D ยังจำกัดที่ N=32

---

## 6. Workplan 4 ข้อ — ผล + verdict (2026-08-31)

### 6.1 D significance (seeds เพิ่ม)
| N | seeds | D | significance | ลบทุก seed? |
|---|---|---|---|---|
| 24 | 30 | −59.6 ± 20.4 | **2.9σ** | 30/30 |
| 32 | 10 | −134.9 ± 23.7 | 5.7σ | 10/10 |
| 48 | 25 | **−297.0 ± 42.4** | **7.0σ** | 25/25 |

→ N=48 ยืน 7σ; แต่ N=24 ยัง 2.9σ (borderline) — ต้อง seeds เพิ่มที่ N=24

### 6.2 Thermalization: spec ยังไม่ plateau
N=32: n_therm 40→120→240 → spec 10.15 → 12.47 → **14.18** (ยังไต่ +14% ที่ 240)
→ ค่า spec ทุกรายงานในตารางเป็น lower bound — ต้อง n_therm > 240 เพื่อค่าสุดท้าย
D คงที่กว่า: −154 → −150 → −141 (เปลี่ยนแปลงเล็กน้อย)

### 6.3 λ_cond scaling (N=32, 10 seeds) — engineered ชัดเจน
| λ_cond | D | sig | spec |
|---|---|---|---|
| 0.00 | −7 ± 20 | 0.4σ | 1.41 |
| 0.02 | −39 ± 24 | 1.6σ | 1.75 |
| 0.05 | −47 ± 40 | 1.2σ | 6.62 |
| 0.10 | −71 ± 21 | 3.4σ | 9.50 |
| **0.15** | **−138 ± 24** | **5.7σ** | 10.13 |
| 0.20 | −143 ± 39 | 3.7σ | 11.10 |
| 0.30 | −163 ± 31 | 5.3σ | 13.04 |
| **0.50** | **−1 ± 16** | **0.1σ** | 13.70 |

→ D significant เฉพาะช่วง λ ∈ [0.10, 0.30]; λ→0 = ไม่มีทั้ง D และ condensation;
λ ใหญ่เกิน (0.5) = over-condensed (spec สูงแต่ D กลับเป็น noise)
→ **ไม่ใช่ emergence — เป็น engineered term ที่ทำงานเฉพาะช่วงพารามิเตอร์แคบๆ**

### 6.4 กลไก D<0 — พบว่า D ขึ้นกับ labeling (สำคัญที่สุด)
- กลไกจริง: coupling + λ_cond สร้าง **super-source nodes** (top-8 มี out−in ≈ +139 เท่ากันหมด,
  node 1: W[1,k]≈12 แต่ W[k,1]≈0.01) — hubs ไหลออกทิศเดียว
- **แต่ D = Σ_{i<j} sign(W_ij − W_ji) ขึ้นกับเลข index ของ node โดยตรง:**
  - permute ป้าย sys nodes (คง obs): D → −44 ± 39 (range [−98, +28] — มีทั้งบวก!)
  - permute ป้ายทั้งหมด: D → −11 ± 91 (range [−172, +128])
- F_net (ผลรวม asymmetry จริง, invariant ต่อ labeling) = −195 (N=24) / −1003 (N=48)
- **บทสรุป:** "D ลบทุก seed" เป็นจริงภายใต้ labeling เดียวกัน แต่ D ไม่ใช่ตัววัดที่
  invariant ต่อการเรียง node → **"Macroscopic Arrow of Time (D ~ N²)" ยังไม่ใช่หลักฐาน
  ทิศทางเวลาทางกายภาพที่ robust** — ต้องใช้ตัววัด invariant (เช่น F_net, source/sink count,
  alignment) หรือรายงาน D เป็น labeling-dependent อย่างโปร่งใส

### 6.5 สถานะ v12 สุดท้าย
- ✅ spec condensation (engineered λ_cond, ช่วง λ แคบ) — reproducible 27–95σ
- ⚠️ D: bias ลบ reproducible แต่ labeling-dependent — ยังไม่ใช่ arrow of time ที่ robust
- ⚠️ emergence: ยังไม่ผ่าน (λ→0 = ไม่มีปรากฏการณ์)

---

## 7. ตัววัดทิศทางที่ invariant ต่อ labeling — ยืนยัน sink-hub จริง (2026-08-31)

สคริปต์: `check_v12_invariant_metrics.py`

### 7.1 ปัญหาของ D
D = Σ_{i<j} sign(W_ij − W_ji) ขึ้นกับเลข index (permute sys labels → D ∈ [−98, +28])
→ ต้องใช้ตัววัดที่ invariant ต่อ labeling: S (source−sink), D_root (hub direction),
imb_norm (|out−in| เฉลี่ย) — **ยืนยันว่า invariant เป๊ะ** (permute แล้วค่าคงที่ทุกหลัก)

### 7.2 ผล (10 seeds)
| ตัววัด | baseline (N=48) | real (N=48) | real (N=32) |
|---|---|---|---|
| S = (src−snk)/N | +0.012 ± 0.079 | **+0.200 ± 0.045** | +0.150 ± 0.041 |
| **D_root** (hub dir) | −0.087 ± 0.228 | **−0.830 ± 0.106** (~6.6σ) | **−0.955 ± 0.082** |
| imb_norm (|out−in|/W̄) | 8.1 ± 1.0 | **59.0 ± 2.4** | 38.3 ± 1.4 |
| spec | 3.72 | 11.64 | 9.17 |

### 7.3 กลไกที่แท้จริง: "sink-hub" (absorbing center)
- hub = node ที่ |out−in| ใหญ่สุด → **เป็น sink แรง: ดูด flow จาก ~83–95% ของ node อื่น**
  (D_root ลบ = W[hub,j] ≪ W[j,hub] เกือบทุก j)
- มี source มากกว่า sink เล็กน้อย (S=+0.15–0.20) แต่ sink-hub ตัวเดียวครอบงำ imbalance
  (imb_norm = 59 เทียบ baseline 8)
- นี่คือโครงสร้างทิศทางที่ **invariant ต่อ labeling — จริง** (ต่างจาก v8/hypergraph ที่ D≈0)

### 7.4 verdict แก้ไข §6.5
- ❌ D (sign-count) เอง — labeling-dependent → ใช้เป็นตัวชี้วัดไม่ได้ (แต่ bias ลบที่เห็น
  เป็นภาพสะท้อนของ sink-hub จริง)
- ✅ **v12 มีโครงสร้างทิศทางจริงที่ robust:** sink-hub ครอบงำ (D_root = −0.83 ถึง −0.96,
  แยกจาก baseline 6–7σ) — "single dominant sink" เกิดจาก coupling quartic + λ_cond
- ⚠️ ยังเป็น engineered (λ scan §6.3) และเป็น "absorbing hub" มากกว่า "arrow of time
  ที่ขยายทั่วระบบ" — ถ้าจะรายงานควรใช้ D_root / S / imb_norm แทน D

---

## 8. sink-hub เกี่ยวข้องกับ observer หรือไม่? — ไม่ (2026-08-31)

สคริปต์: `check_v12_hub_observer.py` (replicate engine + obs_offset)

### 8.1 ผล (N=32, 20 seeds, obs ที่ 0..2)
- hub (argmax|out−in|) เป็น **obs node เพียง 3/20 (15%)** — ส่วนใหญ่เป็น sys node
  (hubs = {1,2,3,4,5,11,12,13,14,16} — กระจาย ไม่มี node ประจำ)
- hub เป็น **sink แรงเสมอ**: hub_imb ≈ −74 ถึง −122 (ทุก seed) แม้ S=+0.12..+0.25
  (มี source มากกว่า แต่ sink-hub ตัวเดียวดูดทั้งหมด)
- D_root = −0.68 ถึง −1.00 (ทุก seed — sink-hub ครอบงำเสมอ)

### 8.2 ย้ายตำแหน่ง observer (offset = 8, 29)
| offset | hub เป็น obs ที่ตำแหน่งใหม่ | D_root |
|---|---|---|
| 0 (มาตรฐาน) | 3/20 (15%) | −0.83 ± 0.09 |
| 8 | 2/10 | −0.87 ± 0.08 |
| 29 | 0/10 | −0.84 ± 0.15 |

→ hub **ไม่ติดตาม observer** — ย้าย obs ไปไหน sink-hub ก็เกิดที่ node อื่น
→ N=24 (5 seeds, offset 0/8): hub เป็น obs 0/5, D_root ≈ −0.9 — เหมือนกัน

### 8.3 บทสรุป
- ✅ **sink-hub เป็น emergent structure จริงของพลวัต v12** (self-organized) — ไม่ผูกกับ
  ตำแหน่ง observer, invariant ต่อ labeling (§7) และต่อ obs placement
- กลไก: coupling + λ_cond สร้างการแข่งขัน → node หนึ่ง "ชนะ" กลายเป็น sink ดูด flow
  จาก ~70–100% ของ node อื่น (D_root ลบเสมอ)
- ⚠️ ยังเป็น engineered (ต้อง λ_cond ∈ [0.10, 0.30]) และ hub เป็น "absorbing center"
  ไม่ใช่ "arrow of time ทั่วระบบ" — แต่ข้อเท็จจริง "single dominant sink ที่
  self-organized และ robust" ใช้รายงานได้

---

## 9. กลไก "ทำไม hub เป็น sink" — คำตอบสมบูรณ์ (2026-08-31)

สคริปต์: `check_v12_sink_mechanism.py`

### 9.1 Coupling ให้ SOURCE hub แต่ global SVD พลิกเป็น SINK
| mode | D_root | hub_imb | spec |
|---|---|---|---|
| 1 baseline | −0.10 ± 0.35 | −1.2 | 3.17 |
| 2 quartic only | −0.76 ± 0.07 | **+24.5 (source!)** | 2.36 |
| 3 relational | −0.63 ± 0.09 | **+43.7 (source!)** | 2.74 |
| 4 global SVD | −0.96 ± 0.08 | **−311.4 (sink แรง)** | 12.81 |

→ coupling quartic สร้าง hub ที่เป็น **source** (+24/+44) — พอใส่พจน์
−λ·Tr((WWᵀ)²) (mode 4) hub **พลิกเป็น sink** (−311)

### 9.2 กลไกเชิงคณิตศาสตร์ (SVD detail, mode 4, N=32 seed 42)
- σ₁ = 217.7, σ₁/σ₂ = 12.9 (dominant mode ครอบงำ)
- |u₁[hub]| = **0.000** (hub ไม่อยู่ใน source direction — u₁max ที่ node 1)
- hub row-norm (ส่งออก) = 0.04, col-norm (รับ) = 58.9 — รับจาก 100% ของ node
- **กลไก:** W ≈ σ₁·u₁·v₁ᵀ → node ที่ u₁[i] ≈ 0 **ส่งออกไม่ได้** (W[i,:] ≈ 0)
  แต่ยังรับได้ (W[:,i] ∝ v₁[i]·u₁ ของคนอื่น) → **กลายเป็น sink-hub โดยอัตโนมัติ**

### 9.3 สรุป mechanistic (ครบวงจร)
1. coupling quartic → source bias (hub ส่งออก)
2. global SVD → dominant rank-1 mode ครอบงำ W
3. node ที่ u₁ ≈ 0 ถูกตัดจากการส่ง → รับจากทุก node → sink-hub
4. **sink-hub = ผลข้างเคียงเชิงโครงสร้างของ rank-1 condensation** (u₁≈0 → sink)
   ไม่ใช่ arrow of time ทางกายภาพ

### 9.4 ผลต่อการตีความ v12
- "ทิศทาง" (D_root ลบ) ที่เห็น = **ภาพของ rank-1 condensation ที่สร้าง sink** — เชิงกลไก
  อธิบายได้หมด ไม่เหลือ "emergence ที่ลึกลับ"
- v12 ข้อเท็จจริงที่รายงานได้: condensation (spec 27–95σ) + sink-hub (D_root −0.8..−1.0,
  invariant ต่อ labeling และไม่ผูกกับ observer) — ทั้งคู่เป็นผลของ engineered λ_cond

---

## 10. λ→0 scaling + n_therm plateau + Global invariant metric G (2026-08-31)

สคริปต์: `step_lambda_scaling_G.py`, `step_therm_plateau.py`

### 10.1 G (Global invariant metric)
นิยาม: **G = Σ_i |out_i − in_i| / Σ_{i≠j} W_ij** (สัดส่วน net imbalance ของ total flow)
- **invariant ต่อ labeling เป๊ะ** (permute 6 รอบ → 1.2139 คงที่ทุกหลัก)
- discriminate: baseline G ≈ 0.27, condensed G ≈ 1.2–1.7
- ใช้แทน D ได้ (D labeling-dependent) — G สะท้อน "ความเข้มข้นของทิศทาง" ทั้งระบบ

### 10.2 λ→0 scaling — มี threshold jump (N=32, 10 seeds)
| λ | spec | D_root | G | S |
|---|---|---|---|---|
| 0.000 | 1.53 | −0.10 | 0.27 | +0.06 |
| 0.005 | 1.52 | −0.26 | 0.29 | +0.05 |
| 0.020 | 1.67 | −0.27 | 0.40 | +0.07 |
| **0.050** | **5.05** | **−0.88** | **1.70** | +0.48 |
| 0.080 | 7.87 | −0.85 | 1.73 | +0.39 |
| 0.120 | 8.20 | −0.95 | 1.45 | +0.29 |
| 0.200 | 10.11 | −0.72 | 1.07 | +0.02 |
| 0.300 | 11.92 | **+0.78** | 0.46 | **−0.56** |

1. **λ < 0.02: ระบบเป็น baseline ล้วน** (spec≈1.5, D_root≈0, G≈0.27) → **λ→0 = ไม่มี
   emergence** — condensation ต้องมี λ ≥ λ_c
2. **λ_c ≈ 0.02–0.05: jump ฉับพลัน** (spec 1.67→5.05, G 0.40→1.70) — ไม่ใช่ linear decay
   = **engineered phase transition** (2 เฟส: สมมาตร / condensed) — เปิดด้วย λ
3. **λ ≥ 0.3: over-condensation พลิกทิศ** — D_root กลับเป็น +0.78, S=−0.56 (hub กลายเป็น
   source) — bistable-ish ที่ λ แรงเกิน

### 10.3 n_therm plateau (N=32, 3 seeds)
| n_therm | spec | D_root | G |
|---|---|---|---|
| 240 | 13.76 | −0.914 | 1.2330 |
| 480 | 15.04 | −0.914 | 1.2297 |
| 960 | 16.51 | −0.957 | 1.2300 |

→ **G และ D_root ลู่เข้าแล้ว** (plateau ที่ 240) แต่ **spec ยังไต่ไม่ plateau**
(13.76→16.51) — σ₁/σ₂ ยังโตตาม scale ของ W — **รายงาน spec เป็น lower bound เสมอ**

### 10.4 สรุป v12 (อัปเดต)
- condensation = engineered phase ที่เปิดด้วย λ_c ≈ 0.02–0.05 (ไม่ใช่ emergence — λ→0 ไม่มี)
- โครงสร้างทิศทาง (sink-hub): วัดด้วย G/D_root — invariant, plateau เร็ว (n_therm ≥ 240)
- spec ยังไม่ plateau — ตัวเลข σ₁/σ₂ ทั้งหมดเป็น lower bound
- λ แรงเกิน (>0.2) → over-condensation พลิกทิศ (bistable ที่ λ สูง)

---

## 10.5 λ_c fine scan — λ_c ≈ 0.02 (N=32, 10 seeds)

สคริปต์: `step_lambda_c_fine.py`

### n_therm=40 (เร็ว แต่ therm ไม่พอที่จุด critical)
| λ | 0.015 | 0.020 | 0.025 | 0.030 | 0.035 | 0.050 |
|---|---|---|---|---|---|---|
| G | 0.33 | 0.40 | 0.48 | 0.89 | 1.32 | 1.70 |
| condensed | 0/10 | 0/10 | 0/10 | **8/10** | 10/10 | 10/10 |

→ ที่ n_therm=40 ดูเหมือน λ_c ≈ 0.03

### ผล thermalization ที่จุด critical (λ=0.030) — therm ไม่พอทำให้ λ_c ดูสูงเกิน
| n_therm | spec | G | condensed |
|---|---|---|---|
| 40 | 2.26 | 0.885 | 8/10 |
| 120 | 4.56 | 1.840 | 10/10 |
| 240 | 8.40 | 1.895 | 10/10 |

→ G เพิ่ม 2 เท่า (0.885→1.895) — **ที่จุด critical ต้อง n_therm ≥ 120** (เหมือน v7:
therm ไม่พอให้ "mixed" ปลอม — บทเรียนซ้ำ)

### n_therm=120 (λ_c ที่ถูกต้อง)
| λ | spec | G | condensed |
|---|---|---|---|
| 0.015 | 2.74 | 0.99 | 6/10 (mixed) |
| **0.020** | 3.12 | 1.53 | **10/10** |
| 0.025 | 3.25 | 1.61 | 10/10 |
| 0.030 | 4.56 | 1.84 | 10/10 |
| 0.035 | 6.36 | 1.85 | 10/10 |

→ **λ_c ≈ 0.02** (n_therm ≥ 120) — transition width ≈ 0.01 (0.015 → 0.020 เต็ม)
→ ใต้ 0.015: baseline ล้วน (λ→0 = ไม่ emergence — ยืนยันอีกครั้ง)
→ spec ที่ λ ใกล้ λ_c: std ใหญ่ (finite-size noise) — λ_c เป็นช่วงกว้าง ~0.005 ไม่ใช่จุด sharp

---

## 10.6 ขยาย N (64/96) — λ_c เพิ่มตาม N, sink-hub scale-invariant (2026-08-31)

สคริปต์: `step_scale_N.py`

### ตาราง (n_therm ไม่เท่ากัน — ระวัง: N ใหญ่ therm สั้นกว่า)
| N | λ | spec | D_root | G | hub_imb | สถานะ |
|---|---|---|---|---|---|---|
| 32 | 0.02 | 3.12 | −0.9 | 1.53 | ≈−100 | condensed (therm 120) |
| 32 | 0.05 | 5.05 | −0.88 | 1.70 | ≈−100 | condensed |
| 64 | 0.03 | 3.2 | +0.2/−0.4 | 0.27 | +10/−10 | **ยังไม่ condensed** (therm 30) |
| 64 | 0.05 | 5.7 | −0.86 | 1.51–1.55 | −73/−75 | condensed (therm 30) |
| 96 | 0.02 | 5.12 | +0.28 | 0.13 | +7.5 | ไม่ condensed (therm 20) |
| 96 | 0.03 | 4.84 | +0.26 | 0.20 | +8.3 | ไม่ condensed (therm 20) |

### ข้อค้นพบ
1. **λ_c เพิ่มตาม N:** N=32 λ_c≈0.02 (therm 120) → N=64 λ_c > 0.03 (ยังไม่ condensed ที่ 0.03,
   เริ่มที่ ~0.05) → N=96 λ_c > 0.03
   - กลไก: เทอม −λ·Σσ⁴ ต้องชนะ sparsity/transitivity ที่ scale ตาม N ต่างกัน —
     engineered term ต้องแรงขึ้นเมื่อระบบใหญ่
   - ⚠️ ข้อจำกัด: therm ที่ N=64/96 (30/20) น้อยกว่า 120 ที่ N=32 — λ_c ที่เห็น
     เป็น **upper bound** (therm ไม่พอ → λ_c ดูสูง) — trend "เพิ่มตาม N" ยังชัด
     (N=64 ไม่ condensed ที่ 0.03 ซึ่ง N=32 condensed เต็มที่ therm เดียวกัน)
2. **sink-hub scale-invariant** (เมื่อ condensed): G ≈ 1.51–1.70, D_root ≈ −0.86
   ข้าม N=32/64 — fraction ของ imbalance คงที่ (hub ดูด proportion คงที่ของ flow)
   hub_imb ≈ −73 ถึง −100 (N=64 therm 30 ยังไม่เต็ม — lower bound)
3. spec ที่ N=96 ยังสูง (5.1) แม้ D_root บวก — spec ไม่ได้บอกทิศทาง (ยืนยันอีกครั้ง)

### สิ่งที่ควรทำต่อ (ถ้าเดินต่อ)
- N=64 therm=120 (λ 0.03/0.04/0.05) เพื่อ λ_c ที่แม่นยำ (ใช้เวลานาน ~5–10 นาที/seed)
- ถ้า λ_c(N) เป็น trend จริง → engineered scaling: λ_c ∝ N^γ — ต้อง fit ก่อนสรุป
