# SGOED-Relational v13: Asymmetric Observer-System Coupling — บันทึกผลการวิจัย

วันที่: 31 สิงหาคม 2026 · สถานะ: ผลสมบูรณ์ (ผ่านการทดสอบ Fast Asymmetry Scan ครบ $N=16, 24, 32$)
สคริปต์ประมวลผลหลัก: `sgoed_graph_core_v13.py` / `audit_v13_fast_scan.py`

---

## 🌟 1. บทนำและแนวคิด v13 (The Asymmetry Hypothesis)

ใน v13 เราได้ตัดพจน์ Engineered SVD Condensation ออกทั้งหมด ($\lambda_{\text{cond}} = 0$) และทดสอบสมมติฐาน:
**"ความไม่สมมาตรของปฏิสัมพันธ์ระหว่างผู้สังเกตการณ์กับระบบ ($g_f > g_b$) สามารถสร้างและตรึงลูกศรเวลา (Arrow of Time $D$) ได้เองตามธรรมชาติหรือไม่?"**

โครงสร้าง Coupling:
1. **Forward Coupling ($S_{\text{forward}}$):** $-g_f \sum_a \hat{v}_a \sum_{j \ge d} W_{aj}^4$ ($g_f = 1.5$, Quartic power $p=4$)
2. **Back-reaction Coupling ($S_{\text{back}}$):** $-g_b \sum_a \hat{v}_a \sum_{j \ge d} W_{ja}^p$ ($g_b < g_f$, $p \in \{2, 4\}$)

---

## 📊 2. ผลการทดลอง Asymmetry Scan ($N = 16, 24, 32$, 5 Seeds)

### 2.1 โครงสร้าง Back-reaction กำลังสอง ($p_b = 2$) — **สภาวะที่เสถียรที่สุด**

| ขนาดระบบ ($N$) | สภาวะ Coupling ($g_b$) | **Net Direction ($D$)** | **Significance ($\sigma$)** | Root Source Flow ($D_{\text{root}}$) | Spectral Ratio |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$N = 16$** | $g_b = 0.0$ (Pure Forward) | $-12.4 \pm 11.3$ | $1.1\sigma$ | $+13.97$ | 2.06 |
| | **$g_b = 0.2$ (Asymmetric)** | **$-13.6 \pm 3.9$** | **$3.5\sigma$ (ผ่านเกณฑ์ $3\sigma$!)** | **$+12.68$** | 1.84 |
| | $g_b = 1.5$ (Symmetric) | $-15.6 \pm 11.3$ | $1.4\sigma$ | $+11.90$ | 1.81 |
| **$N = 24$** | $g_b = 0.0$ (Pure Forward) | $-19.6 \pm 10.8$ | $1.8\sigma$ | $+12.86$ | 1.77 |
| | **$g_b = 0.2$ (Asymmetric)** | **$-16.2 \pm 5.2$** | **$3.1\sigma$ (ผ่านเกณฑ์ $3\sigma$!)** | **$+15.14$** | 1.91 |
| | $g_b = 1.5$ (Symmetric) | $-16.8 \pm 14.2$ | $1.2\sigma$ | $+11.90$ | 1.56 |
| **$N = 32$** | $g_b = 0.0$ (Pure Forward) | $-12.6 \pm 17.3$ | $0.7\sigma$ | $+12.93$ | 1.57 |
| | **$g_b = 0.2$ (Asymmetric)** | **$-23.0 \pm 10.1$** | **$2.3\sigma$** | **$+12.39$** | 1.50 |
| | $g_b = 1.5$ (Symmetric) | $-12.4 \pm 10.4$ | $1.2\sigma$ | $+15.85$ | 1.69 |

---

## 🔬 3. การค้นพบทางฟิสิกส์ที่สำคัญของ v13

### 3.1 Asymmetric Coupling ช่วยตรึงลูกศรเวลา (Variance Suppression & Stability)
- เมื่อไม่มี Back-reaction ($g_b = 0$) หรือสมมาตรเกินไป ($g_b = 1.5$) ความแปรปรวนของลูกศรเวลาจะสูงมาก ($\sigma_D \approx \pm 11 - 17$) ทำให้ Significance ต่ำ ($\sim 1\sigma$)
- แต่เมื่อมี **Asymmetric Back-reaction อ่อนๆ ($g_b = 0.2, p_b = 2$)**:
  - ความแปรปรวนลดลงกว่า **$3\times$** ($\sigma_D \approx \pm 3.9 - 5.2$)
  - ส่งผลให้ **ลูกศรเวลามีนัยสำคัญทางสถิติทะลุเกณฑ์ $3\sigma$ ($3.5\sigma$ ที่ $N=16$, $3.1\sigma$ ที่ $N=24$)** โดยปราศจากการใส่ engineered term ใดๆ!

### 3.2 Observer ทำหน้าที่เป็น Super Source Node ($D_{\text{root}} > 0$)
- ค่า $D_{\text{root}} = +12.0 \to +15.1$ เป็นบวกเข้มข้นทุกกรณี แสดงว่า Observer Node มี Outflow เหนือ Inflow อย่างเด็ดขาด และเป็นผู้กำหนดทิศทางเวลาให้แก่ระบบส่วนกลาง

---

## 📁 4. สรุปรายการไฟล์ v13
1. `sgoed_graph_core_v13.py`: Core Engine สำหรับ Asymmetric Coupling Graph
2. `audit_v13_fast_scan.py`: Fast Real-Time Asymmetry Scan
3. `audit_v13_fast_results.json`: ข้อมูลตัวเลขดิบของการทดลอง
4. `SGOED_v13_asymmetric_notes.md`: บันทึกผลการวิจัยฉบับทางการ

---

## 🔍 5. การตรวจสอบความซื่อตรง (Data Honesty Audit — 2026-08-31)

สคริปต์ตรวจ: `check_v13_critical.py` (N=32, 10 seeds, n_therm=120)

### 5.1 Reproduce
audit รันซ้ำตรงทุกค่า (D, D_root, spec) — reproducible ✓
✅ ไม่มี engineered λ_cond จริง — v13 เป็น coupling-only (เป็นข้อดีของงานนี้)

### 5.2 ❌ Significance "3.5σ/3.1σ" ไม่ robust — เป็นปรากฏการณ์ 5-seed
| config | 5 seeds (audit) | 10 seeds (ตรวจ) |
|---|---|---|
| N=32 g_b=0.2 | −23.0 ± 10.1 (2.3σ) | **−33.1 ± 27.7 (1.2σ)** |

ขยายเป็น 10 seeds → std โตขึ้น ~3× (10.1 → 27.7) → significance ตก (2.3σ → 1.2σ)
→ ค่า 3.5σ/3.1σ ที่ N=16/24 มาจาก 5 seeds เฉพาะ — ยังไม่ใช่หลักฐาน robust

### 5.3 ❌ D ยัง labeling-dependent (metric เดิม)
permute ป้าย sys nodes (asym, seed 42): D = −69 → range [−69, −1] (เฉลี่ย −28 ± 21)
→ D เปลี่ยนตามการเรียง node — เหมือน v12 — ใช้เป็นหลักฐานทิศทางไม่ได้

### 5.4 ⚠️ G (invariant metric) — forward coupling มีผลจริง แต่ asymmetric ไม่เพิ่ม
| config | G (Σ\|out−in\|/ΣW) |
|---|---|
| baseline (0,0) | 0.204 ± 0.022 |
| forward only (1.5,0) | 0.374 ± 0.042 |
| asym (1.5, 0.2, p2) | 0.381 ± 0.055 |

→ forward coupling เพิ่ม G 1.8× (มีทิศทางจริงจาก forward) แต่ **g_b=0.2 ไม่เพิ่ม G**
(0.374 → 0.381 ไม่มีนัย) — "variance suppression" ที่อ้างไม่ปรากฏในตัววัด invariant

### 5.5 ⚠️ D_root = "out−in ของ argmax out_deg" — บวกโดยนิยาม
- root = node 0 (observer): out=25.8, in=2.6 → D_root=+23.3 — observer เป็น source
  ของ forward coupling จริง (v̂_a>0 → ดัน W[a,j] โต)
- **แต่** node ที่ส่งออกมากสุดย่อมมี imbalance บวกเป็นส่วนใหญ่ → D_root>0 ไม่ใช่
  "การค้นพบ" — metric นี้ยังไม่ normalized ต่อ N (เทียบข้าม N ตรงๆ ไม่ได้)

### 5.6 v13 ไม่มี condensation
spec ≈ 1.4–2.1 ทุกจุด (baseline ~1.5) — ต่างจาก v12 (spec 7–13) — v13 วัดได้แค่
"ทิศทาง/ความไม่สมดุล" ไม่ใช่ rank-1 condensation

### 5.7 verdict
- ✅ ไม่มี engineered term (ข้อดี) + forward coupling เพิ่ม G จริง (1.8×)
- ❌ "arrow of time ผ่านเกณฑ์ 3σ" ยังไม่ยืน — 10 seeds significance ตก; D labeling-
  dependent; asymmetric (g_b) ไม่เพิ่ม G
- ❌ "observer super source (D_root>0)" — จริงในแง่ forward coupling แต่ metric
  บวกโดยนิยาม — ไม่ใช่หลักฐานใหม่
- สรุป: v13 เป็น coupling-only ที่มี bias ทิศทางอ่อน (G 0.38) แต่ยังไม่ใช่
  "asymmetric coupling สร้างลูกศรเวลาที่ robust" ตามที่สรุปใน §3

---

## 6. Cycle Ratio (feed-forward test) — ไม่มี feed-forward structure (2026-08-31)

สคริปต์: `check_cycle_ratio.py` — นับ cyclic triples (d_ij·d_jk·d_ki > 0) / triples ที่มีทิศทาง
— feed-forward (ลูกศรเวลา) → ratio << 0.5; random → ~0.5; invariant ต่อ labeling

### ผล (N=32, 10 seeds)
| config | cycle_ratio | null (shuffle) |
|---|---|---|
| v13 baseline (0,0) | 0.4956 ± 0.0061 | 0.5026 |
| v13 forward only | 0.5010 ± 0.0046 | 0.4977 |
| v13 asym g_b=0.2 | 0.4996 ± 0.0058 | 0.5012 |
| v12 baseline (0,0) | 0.5004 ± 0.0034 | 0.4988 |
| v12 full (λ=0.15) | 0.5228 ± 0.0171 | 0.5013 |

### สรุป
- ❌ **ทุก config ให้ cycle ratio ≈ 0.5 = random** — ไม่มี feed-forward structure
  (v13 ทั้งหมด: 0.496–0.501; v12 full: 0.523 — cyclic มากกว่า random เล็กน้อย
  ตรงข้าม feed-forward — sink-hub สร้าง cycles รอบ hub ที่รับจากทุก node)
- ✅ permutation sanity: cycle ratio ≈ 0.5 (±0.01) — invariant ในทางปฏิบัติ
- **ความหมาย:** ทิศทางที่เห็น (G, D_root, sink-hub) เป็น "hub structure" ไม่ใช่
  "global direction ที่สอดคล้องกันระดับ triple" — ลูกศรเวลาเชิง feed-forward
  ยังไม่มีหลักฐานในทั้ง v12 และ v13
- นี่คือตัววัดที่ 5 (หลัง R, D, d_MM, d_s, G) ที่ invariant + null-testable —
  ผลลบชัดเจน: **โมเดลนี้ไม่มี signature ของลูกศรเวลาเชิงโครงสร้าง**

---

## 7. Time-Reversal / Irreversibility test — ไม่มี attractor ของทิศทาง (2026-08-31)

สคริปต์: `check_v13_time_reversal.py` — protocol ต่อ seed:
W1 = run(random init) → W2 = run(init=W1, warm) → W3 = run(init=W1.T, reversed)
ถ้ามีลูกศรเวลา/attractor: W3 ควรถูกดึงกลับทิศเดียวกับ W1 (และ corr(W3,W1) > corr(W3,W1.T))

### ผล (N=32, asym g_b=0.2)
| n_therm | warm keeps sign | reversed pulls back | corr(W3,W1) | corr(W3,W1.T) |
|---|---|---|---|---|
| 60 | 10/10 | 9/10 | +0.442 | **+0.494** |
| 120 | 3/3 | 3/3 | +0.300 | **+0.385** |
| 240 | 3/3 | **2/3** | +0.202 | **+0.389** |

baseline (0,0): reversed pulls back 1/5, corr เท่ากัน (0.542 vs 0.539 — สมมาตร)

### สรุป
- ❌ **"sign pulls back 9/10" เป็น artifact ของ metric ตื้น** — sign ของ hub imbalance
  เปลี่ยน node ได้ง่าย — แต่โครงสร้างทั้งหมด (corr) **ยังตาม W1.T เสมอ**
  (corr(W3,W1) ลดลง 0.44→0.20 ตาม therm ที่ยาวขึ้น — ระบบยิ่ง "ยอมรับ" ทิศที่เริ่ม)
- ❌ G3 < G1 ทุกกรณี (0.36→0.29, 0.52→0.28) — reversed-start ไม่ฟื้น imbalance
- ❌ baseline ก็สมมาตร (1/5) — asym ต่างกันที่ sign level แต่ correlation ไม่ยืนยัน
- **บทสรุป: ไม่มี irreversibility / attractor ของทิศทาง** — ระบบรับทิศทางที่ initial
  ให้ (W1.T → จบใกล้ W1.T) — coupling ไม่ได้ "ดึงกลับ"

### สถานะการพิสูจน์ลูกศรเวลา (รวม 7 วิธี)
| วิธี | ผล |
|---|---|
| R (asymmetry ratio) | histogram artifact |
| D (sign count) | labeling-dependent |
| d_MM / d_s / BD | null-compatible |
| G / D_root | hub structure (ไม่ใช่ global arrow) |
| cycle ratio (feed-forward) | ≈ random (0.5) |
| **time-reversal** | **ไม่ดึงกลับ (corr ตาม initial)** |
| alignment | เงื่อนไขอ่อน (baseline ก็ 80–100%) |

→ **graph/hypergraph models (v8–v13) ไม่มีหลักฐานลูกศรเวลา** — ทั้งเชิงโครงสร้าง
และเชิงพลวัต — หลักฐานทิศทางที่ยังยืนมีเฉพาะ **matrix v7 condensation ratio**
(discriminate จริง, ดู SGOED_v7_feedback_notes.md §13)
