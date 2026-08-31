# SGOED-Relational Phase 2: v9-R (Causal Hypergraph) — บันทึกผลการวิจัย

วันที่: 30 สิงหาคม 2026 · สถานะ: ผลสมบูรณ์ (รันชุดทดสอบเต็ม Full Battery Audit ผ่านครบ)

---

## 🌌 1. สถาปัตยกรรม Phase 2: v9-R (จาก Graph สู่ Hypergraph)

| องค์ประกอบ | v8-R (Binary Graph) | v9-R (Causal Hypergraph) |
|---|---|---|
| **State** | 2-body edges $W_{ij} \ge 0$ | **3-body Causal Triads $T_{ijk} \ge 0$** ($i \to j \to k$) |
| **Symmetry Breaking** | Out/In degree asymmetry | **Hyper-asymmetry $R_{\text{hyper}} = \frac{\sum |T_{ijk} - T_{kji}|}{\sum (T_{ijk} + T_{kji})}$** |
| **Observer** | Subgraph $S$ ($d$ nodes) | **Sub-hypergraph $S_{\mathcal{H}}$** (Observer ควบคุม Triads) |
| **Coupling & Feedback** | Normalized direction $\hat{v}_a, \hat{w}_a$ | **Normalized Hyper-coupling & Feedback** |
| **Emergent Spacetime** | $d_{\text{MM}} \approx 1.2 - 3.5\text{D}$ | **$d_{\text{MM}} \approx 3.99\text{D} - 4.04\text{D}$ (กำเนิด 4D Spacetime สมบูรณ์!)** |

---

## 📊 2. ผลการทดลองหลัก (Key Experimental Findings)

### 2.1 กำเนิดมิติกาลอวกาศ 4 มิติ ($\approx 4\text{D}$ Spacetime Emergence)
การทดสอบข้าม 5 Seeds อิสระ (Seeds 42–46, $d=3, g_{XY}=0.8$):

| ขนาดระบบ ($N$) | เวลาเฉลี่ยต่อ Seed | $R_{\text{hyper}}$ (ความไม่สมมาตรของเวลา) | Flow Alignment | **มิติกาลอวกาศ ($d_{\text{MM}}$)** | **Proper Time ($L_{\max}$)** |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$N = 8$** | 1.83 วินาที | **0.4763** | **93.7%** | **3.89 มิติ** | 33.3 |
| **$N = 12$** | 1.50 วินาที | **0.4942** | **84.0%** | **4.04 มิติ** | 61.6 |
| **$N = 16$** | 7.05 วินาที | **0.4986** | **80.0%** | **3.99 มิติ** | 97.2 |
| **$N = 20$** | 40.70 วินาที | **0.4958** | **74.3%** | **3.51 มิติ** | 114.0 |

> **🌟 ข้อค้นพบทางฟิสิกส์ที่สำคัญที่สุด:**  
> ที่ระดับ $N = 12 - 16$ โครงสร้างความสัมพันธ์แบบ 3-Body Triads สร้างมิติของ Causal Set ได้ที่ **$d_{\text{MM}} = 3.99\text{D} - 4.04\text{D}$** ซึ่งตรงกับ **4 มิติของกาลอวกาศจริง ($3+1$ มิติ)** อย่างแม่นยำ โดยปราศจากการบังคับมิติไว้ล่วงหน้า!

---

### 2.2 การยืดขยายของลูกศรเวลา (Proper Time Expansion)
ค่า **$L_{\max}$ (Longest Causal Chain)** ยืดขยายอย่างต่อเนื่องตามขนาดเครือข่าย:
$$33.3 \to 61.6 \to 97.2 \to 114.0$$
เปรียบเสมือนการขยายตัวของกาลอวกาศ (Cosmic Proper Time Expansion) ที่มีทิศทางของลูกศรเวลาชัดเจน

---

### 2.3 ความทนทานต่อแรงสะท้อนกลับ (Feedback Robustness)
ที่ $N=12, d=3$ สแกนค่า $g_{YX} = 0.0 \to 2.0$:
- ค่า $R_{\text{hyper}}$ ทรงตัวอยู่ที่ **$\approx 0.494 - 0.497$** และ Alignment **$81\% - 88\%$** อย่างมั่นคงตลอดช่วง
- กฎ **Normalized Feedback** จาก v8-R สามารถป้องกันภาวะ Observer Runaway Collapse ใน Hypergraph ได้อย่างสมบูรณ์แบบ

> ⚠️ **คำแก้ไข (2026-08-30) — ข้อความข้างต้นสรุปเร็วเกินไป:**
> การสรุป "feedback ทนทาน/กัน runaway ได้สมบูรณ์" มาจากการสแกนแค่ $g_{YX} \le 2.0$ ซึ่งไม่ไกลพอ
> เมื่อ re-run ด้วย thermalization ที่น่าเชื่อถือ ($n_{\text{therm}} \ge 100$, N=8, 5 seeds) และสแกนไกลขึ้น พบว่า:
> **condensation จริงเกิดที่ $g_{YX} \approx 4$–$8$** (obs_extent กระโดด 0.11 → 16.5, ชน gate 5/5 ที่ $g_{YX}=8$)
> — Normalized feedback **ชะลอ** runaway แต่ **ไม่กำจัด** ระบบยังระเบิดได้ที่ coupling แรงพอ
> (รายละเอียดใน section 4. **ข้อมูลที่น่าเชื่อถือ**)

---

## 🔬 4. ข้อมูลที่น่าเชื่อถือ (re-run 2026-08-30, N=8, 5 seeds, n_therm≥100)

จาก `audit_v9_reliable_results.json`:

### 4.1 Thermalization ($g_{YX}=0.0$)
| n_therm | R_hyper | obs_extent | d_MM |
|---|---|---|---|
| 25 | 0.477 | 0.046 | 3.88 |
| 100 | 0.482 | 0.070 | 3.76 |
| 200 | 0.474 | 0.069 | 3.81 |
| 400 | 0.489 | 0.062 | 3.87 |

→ **obs_extent สมดุล ~0.06–0.07 หลัง n_therm≥100**; d_MM ≈ **3.8** (ใกล้ 4D แต่ยังไม่ใช่ 4.04 ที่เคยเคลม)

### 4.2 Feedback scan (n_therm=200)
| g_yx | obs_extent | R_hyper | ชน gate (extent>1.5) |
|---|---|---|---|
| 0.0 | 0.069 | 0.474 | 0/5 |
| 2.0 | 0.110 | 0.486 | 0/5 |
| 4.0 | 1.67 ± 2.3 | 0.502 | 2/5 |
| **8.0** | **16.5 ± 0.24** | **0.662** | **5/5** |
| 16.0 | 18.7 | 0.687 | 5/5 |

→ **condensation เกิดที่ g_yx ≈ 4–8** — observer ระเบิดชน gate ได้จริง (ข้อสรุปเดิม "กัน runaway สมบูรณ์" ไม่ถูก)
→ R_hyper พุ่ง 0.47 → 0.69 เมื่อ condensed (เหมือน v8 ไม่-normalize)

### 4.3 ข้อควรระวัง
- N=8 มี triad น้อยมาก (d=3) obs_extent จึง noisy (std ใหญ่) — ควร re-check ที่ N=12/16
- ยังไม่ re-run d_MM ที่ N=12/16 ด้วย thermalization ที่ถูกต้อง — ตัวเลข 4.04 ใน notes เดิมยังไม่ยืนยัน

### 4.4 ยืนยัน d_MM ≈ 4.0 ด้วย n_therm=100 (re-check N=12/16, 2026-08-30)

จาก `audit_v9_dimension_reliable.json` (n_therm=100, n_measure=30, 5 seeds):

| N | R_hyper | align | **d_MM** (per-seed) | L_max | obs_extent |
|---|---|---|---|---|---|
| 12 | 0.497±0.005 | 81% | **4.09 ± 0.15** [3.80, 4.13, 4.17, 4.11, 4.25] | 60.4 | 0.011 |
| 16 | 0.496±0.003 | 81% | **3.99 ± 0.19** [4.28, 3.76, 4.14, 3.84, 3.95] | 89.6 | 0.009 |

**ข้อสรุปที่ยืนยัน:**
- **d_MM ≈ 4.0 ทนทานต่อการเปลี่ยน thermalization (25→100)** — "กำเนิด 4D" ใน notes เดิมคือของจริง
  (4.04@N12, 3.99@N16 ตรงกับ 4.09/3.99 ใหม่)
- **แต่ spread กว้าง ±0.2** (seeds 3.76–4.28) → ควรสื่อเป็น "≈4 (ภายใน ±0.2)" ไม่ใช่ "4.04 เป๊ะ"
- obs_extent ที่ N ใหญ่ (0.011/0.009) น้อยกว่า N=8 (0.06) — ตามจำนวน trial ต่อ node ที่น้อยลง
- R_hyper/align ตรงกับ notes เดิม (0.49, 80–84%) — ข้อสรุปอื่นถูกต้อง

---

## 🔄 5. **d_MM ขึ้นกับ threshold มาก — ข้อสรุป "4D emergence" และ "d_MM ยุบ" เป็น artifact ของ estimator (2026-08-30)**

> ⚠️ **คำแก้ไขที่ 2 (สำคัญกว่า):** ทั้งข้อสรุป "hypergraph กำเนิด 4D" (section 2.1) **และ** ข้อสรุป
> "d_MM ยุบที่ N ใหญ่" (section 5.0 ฉบับแรก) **ล้วนเป็น artifact ของ threshold คงที่ 0.2**
> ตัววัด d_MM นี้ไม่เสถียร ไม่ควรใช้ยืนยันมิติกาลอวกาศ

### 5.0 สาเหตุ (ตรวจด้วยข้อมูล)
`compute_hyper_observables` ใช้ `flow_ik = Σ_j (T_ijk − T_kji) > threshold=0.2` คงที่ แต่ผลรวมมี
O(N) เทอม → ที่ N ใหญ่ threshold 0.2 "เกินง่ายไป" → กราฟ C หนาแน่นเกิน → d_MM ถูกกดต่ำ
(ที่ N=32 เหลือ 1.93) — ไม่ใช่ฟิสิกส์ "dimensional collapse"

### 5.1 หลักฐาน: d_MM ผันตาม threshold อย่างมาก (N=24/32, seed 42)

| N | th=0.05 | th=0.1 | th=0.2 | th=0.4 |
|---|---|---|---|---|
| 24 | 6.84 | 6.01 | 3.35 | 1.00 |
| 32 | 6.89 | 5.74 | 2.01 | 1.00 |

→ ค่า 4.0 ที่เคยเห็นเป็น coincidence ของ threshold 0.2 พอดี ไม่ใช่สมบัติทางฟิสิกส์

### 5.2 threshold ที่ scale ตาม N (ความหนาแน่น C คงที่) — trend กลับทิศ

| N | d_MM@frac=0.1 | d_MM@frac=0.3 | d_MM@frac=0.5 |
|---|---|---|---|
| 12 | 1.00 | 4.13 | 6.32 |
| 16 | 1.58 | 5.15 | 6.76 |
| 24 | 2.25 | 5.87 | 7.32 |
| 32 | 2.41 | 6.43 | 7.60 |

→ เมื่อความหนาแน่น C คงที่ d_MM **เพิ่ม**ตาม N (4.13→6.43@frac 0.3) ตรงข้ามกับ "ยุบ"
→ ยืนยันว่าข้อสรุป "ยุบ" เป็น artifact ของ threshold คงที่

### 5.3 ข้อสรุปที่ถูกต้อง (แทนที่ 2 ข้อสรุปก่อนหน้า)
1. ❌ **ไม่มี "4D emergence" ที่เชื่อถือได้** — d_MM ขึ้นกับ threshold มาก (1.0–7.6 ที่ N เดียวกัน)
2. ❌ **ไม่มี "dimensional collapse" ที่ N ใหญ่** — ตรงข้ามเมื่อ scale threshold
3. ✅ **d_MM ตัวนี้ไม่เหมาะเป็นตัวชี้วัดมิติ** — ต้องใช้ตัววัดอื่น (spectral dimension) หรือรายงาน
   เป็น sensitivity scan เท่านั้น
4. ✅ **สิ่งที่ยังยืนยันได้ (threshold ไม่กระทบ):** L_max โตตาม N (proper time ขยายจริง),
   feedback condensation ที่ g_yx≈4–8
   ⚠️ ~~R_hyper ≈ 0.50 (ลูกศรเวลา)~~ — **ถูกถอนสถานะแล้ว ดู section 6**

### 5.4 v10 engine (optimized hypergraph)
- `sgoed_hypergraph_core_v10.py`: delta O(N)/move (closure incremental 1e-16 + cfe running-sum)
  แทน full recompute O(N⁴)/move ของ v9 → **speedup 5×@N8 → 43×@N16**
- Reproduce v9 bit-for-bit (R, align, extent ตรงทุกหลัก)
- ทำให้ N=24/32 สแกนได้ในวินาที (v9 เดิมต้องชั่วโมง) — เปิดทางตรวจ N ใหญ่

---

## 🕐 6. R_hyper ≈ 0.50 และ d_s — ไม่ใช่ลูกศรเวลา / ไม่ใช่มิติ (2026-08-31)

> ⚠️ **คำแก้ไขที่ 3:** section 5.3 เดิมระบุว่า "R_hyper ≈ 0.50 = ลูกศรเวลา ยืนยันได้" — **ผิด**
> R_hyper เป็น **artifact ของ histogram ของค่า** ไม่ใช่หลักฐานทิศทางเวลา

### 6.1 ทำไม R_hyper จึงไม่ใช่ลูกศรเวลา (null test)
R_hyper = Σ|T_ijk − T_kji| / Σ(T_ijk + T_kji) วัด **ขนาด**ความต่างของ mirror pair —
ไม่ได้วัดว่าทิศทางสอดคล้องกันหรือไม่ (N=32, seed 42):

| การทดสอบ | R_hyper |
|---|---|
| จริง (thermalize) | 0.5002 |
| **shuffle ค่า triad ทั้งหมด** (ทำลายทุกโครงสร้าง) | **0.5162** (สูงกว่า real!) |
| iid uniform | 0.333 |
| mirror-swap (สลับทิศแต่ละคู่) | 0.5002 (ไม่เปลี่ยน — direction-blind โดยคณิตศาสตร์) |

→ การสลับค่าทั้งหมด (ไร้โครงสร้างใดๆ) ให้ R **สูงกว่า** real → R มาจาก histogram ของค่า
(มีค่าเล็ก/ศูนย์ปนกับค่าใหญ่ → |a−b|/(a+b) สูง) ไม่ได้มาจากทิศทางเวลา

### 6.2 ทิศทางรวม D ≈ 0 — ไม่มีลูกศรเวลา global (5 seeds)
D = Σ_{i<k} sign(Σ_j T[i,j,k] − T[k,j,i]) — ตัววัดทิศทางที่ตรง
(random → 0; ถ้ามี global arrow → |D| ใหญ่):

| ระบบ | D เฉลี่ย | max เป็นไปได้ |
|---|---|---|
| hypergraph N=32 | −0.8 ± 19.8 | 496 |
| graph v8 N=16 | +8.0 ± 20.4 | 120 |

→ D ≈ 0 ± std ใหญ่ → **ไม่มีทิศทางเวลารวม** ทั้ง graph และ hypergraph

### 6.3 d_s (spectral dimension) — null-compatible เช่นกัน
- เมธอดเดิม (directed transition matrix) ให้ค่าผิดบนกราฟที่รู้คำตอบ
  (path→4.59, grid→4.84, complete→0.035) → invalid โดยสิ้นเชิง
- เมธอดที่ถูกต้อง (heat kernel บน normalized Laplacian L_n = I − D^−1/2 A D^−1/2):
  d_s = 1.87 → 3.49 ตาม N = 8 → 32 แต่
  - **null (degree-preserving shuffle) = 3.49 = real เป๊ะ**
  - สาเหตุ: symmetrized graph มีความหนาแน่น 1.0 (complete) → d_s วัดความหนาแน่น ไม่ใช่มิติ
- d_MM^cont (continuous weighted): random data ไร้โครงสร้างให้ 1.97–2.59 ครอบคลุมค่า
  "2.42" ทั้งหมด → null-compatible (ข้อสรุป "2.42D fractal" เป็นคุณสมบัติของสูตร)
- Benincasa–Dowker chain-count (r = C4·C2/C3²): real = 1.0000 = ค่าเชิงพีชคณิตของ complete
  matrix (นอกช่วง calibration 0.088–0.746 ด้วยซ้ำ) → null-compatible

### 6.4 ข้อสรุปที่ถูกต้อง (แทนที่ 5.3 ข้อ 4)
1. ❌ **R_hyper ≈ 0.50 ไม่ใช่ลูกศรเวลา** — histogram artifact (shuffle > real)
2. ❌ **ไม่มี global temporal direction** — D ≈ 0 ± std ใหญ่ (ทั้ง graph และ hypergraph)
3. ❌ **d_MM (threshold + continuous) และ d_s (ทุกแบบ) ไม่ใช่ตัววัดมิติที่เชื่อถือได้**
   — null-compatible ทั้งหมด
4. ✅ **ที่ยังยืน:** L_max โตตาม N (causal chain ยาวขึ้น), feedback condensation (g_yx 4–8),
   และ **matrix v7 condensation ratio** (discriminate ~60σ — ดู `SGOED_v7_feedback_notes.md` §13)

สคริปต์ตรวจ: `check_r_hyper_baseline.py`, `check_r_causal_graph_baseline.py`,
`check_d_direction_multiseed.py`, `audit_spectral_dimension_correct.py`,
`audit_bd_dimension.py` (ทั้งหมดใน `matrix/`)

---

## 📁 3. สรุปรายการไฟล์ Phase 2 (v9-R)

1. `sgoed_hypergraph_core_v9.py`: Core Engine สำหรับ 3-Uniform Causal Hypergraph
2. `test_hypergraph_core_v9.py`: Unit test ทดสอบความถูกต้อง
3. `audit_v9_full_battery.py`: Script สแกนทดสอบ 4D Spacetime และ Feedback Scan
4. `audit_v9_full_battery_results.json`: ข้อมูลตัวเลขดิบที่ผ่านการตรวจสอบ
5. `SGOED_v9_hypergraph_notes.md`: บันทึกผลการวิจัยฉบับทางการ
