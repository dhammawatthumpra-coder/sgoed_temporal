# SGOED v7 — Feedback Coupling (Back-reaction X→Y) — บันทึกผล

วันที่: 2026-08-30 · สถานะ: ผลสมบูรณ์ (รันสะอาดด้วย n_therm=40, n=30)

## 1. โมเดล (v7 ต่างจาก v6 ตรงไหน)

v7 เพิ่ม **back-reaction** ให้ observer Y ถูก temporalize กลับโดย X:

```
Forward (v6 เดิม):   -g_XY · Σ_μ v̂_μ² · Tr(X_μ⁴)    (Y → X)
Back-reaction (ใหม่): -g_YX · Σ_a ŵ_a² · Tr(Y_a⁴)    (X → Y)
```

- `v̂` = ทิศจาก trace ของ Y (normalize แล้ว), `ŵ` = ทิศจาก trace ของ X
- ที่ `g_YX = 0` action ลดกลับเป็น v6 เป๊ะ (sanity check: diff = 0.0 ถึง machine precision)
- sampler ใช้ **full-action recompute** (ไม่ใช้ delta ของ v6) เพื่อความถูกต้อง

โค้ด: `code/sgoed_core_v7.py` — `action_v7()`, `run_simulation()`

## 2. ผลหลัก (4 ข้อ)

### 2.1 ทิศทางเวลา (X) ทนทานต่อ back-reaction สุดขั้ว
X ratio อยู่ ~4.8±0.15, alignment 100% **ตลอดช่วง g_YX = 0 ถึง 5** (แรงกว่า forward 6 เท่า)
→ ทิศทางเวลาที่ X ชี้ **ไม่เคยพังเลย**

### 2.2 สิ่งที่พังคือ observer (Y) เอง — ชน stability gate
ที่ g_YX เกิน critical Y_max_extent พุ่งชน gate (10.0) แบบ bistable:
- **ก้อน "Y เล็ก"** (≈0.5–0.7) กับ **ก้อน "Y ชน gate"** (≈10.0) สองก้อนชัดเจน

### 2.3 Critical g_YX (n_therm=40, n=30, d=3, N=6, g_XY=0.8)
| g_YX | ชน gate % |
|---|---|
| 1.00 | 0% |
| 1.05 | 23% |
| 1.10 | 47% |
| 1.20 | 50% |
| 1.30 | 73% |
| 1.40 | 90% |

→ **midpoint ≈ 1.1–1.2**, ช่วง transition กว้าง ~1.0–1.4

### 2.4 Dependence ต่าง ๆ
- **d มากขึ้น → critical g_YX สูงขึ้น** (d=5: ≈1.5–1.8, d=3: ≈1.1–1.2) — สอดคล้อง "dimensional dilution": observer หลายมิติกระจายแรง back-reaction จึงชน gate ยากกว่า
- **N เล็กลง → ชน gate ง่ายขึ้น** (N=4 ชนง่ายกว่า N=8)
- **ไม่มีกฎง่าย g_YX ≳ α·g_XY** — ที่ g_XY=1.15 Y ชน gate ง่ายขึ้น (เพราะ X เองเข้า saturation แล้ว forward loop ผ่าน extent)

## 3. บทเรียนเชิงระเบียบวิธี (สำคัญ)

**thermalization check เป็นสิ่งจำเป็นก่อนสรุปผล**
- ที่ `n_therm=20` (ค่าที่ใช้ตลอด v6) ผล v7 transition ดูเหมือน "continuous distribution" ของ Y_max
- พอ `n_therm=40` เผย **bistability จริง** (สองก้อนแยก) — บาง seed ค้างอยู่ตรงกลางเพราะ thermalize ไม่เสร็จ
- v6 healthy config ไม่มีปัญหานี้ (ratio นิ่งที่ n_therm 20→160) แต่ v7 transition ต้อง ≥40

## 4. ไฟล์ audit ทั้งหมด (ชุด v7)

| ไฟล์ | เนื้อหา |
|---|---|
| `code/sgoed_core_v7.py` | engine v7 (action + run, full recompute) |
| `AUDIT_v7_feedback.py` (+json/log) | สแกน g_YX 0.1–0.5 (เล็ก) |
| `AUDIT_v7_feedback_high.py` (+json/log) | สแกน g_YX 0.5–5.0 (สูง) |
| `AUDIT_v7_feedback_fine.py` (+json/log) | สแกน g_YX 1.0–2.0 step 0.1 |
| `AUDIT_v7_feedback_n30.py` (+json/log) | n=30 transition (แต่ n_therm=20 → ต้องใช้ด้วยความระวัง) |
| `AUDIT_v7_relative.py` (+json/log) | relative g_YX/g_XY + N-dependence |
| `AUDIT_v7_transition_clean.py` (+json/log) | **transition สะอาด n_therm=40 n=30 (ใช้ตัวนี้หลัก)** |
| `AUDIT_v7_d5_bistability.py` (+json/log) | d=5 bistability check |
| `AUDIT_v7_d3_fine.py` (+json/log) | d=3 fine step 0.05 pinpoint |

## 5. Hysteresis — ยืนยัน first-order transition (2026-08-30)

ทดสอบโดย anneal ต่อเนื่อง (carry X,Y ข้ามขั้น ไม่ re-randomize) สแกน UP vs DOWN:

| g_YX | UP (จาก Y เล็ก) Ymax | DOWN (จาก Y ชน gate) Ymax |
|---|---|---|
| 0.5 | 0.58 (เล็ก) | 0.59 (เล็ก) |
| 0.8 | 0.60 (เล็ก) | 0.63 (เล็ก) |
| 1.0 | 5.89 (3/5 เริ่มชน) | **9.94 (ค้างชน 5/5)** |
| 1.1 | 6.22 (3/5 ชน) | 9.98 (ชน) |
| 1.2 | 8.13 (4/5 ชน) | 9.99 (ชน) |
| 1.3 | 9.99 (ชน 5/5) | 9.99 (ชน) |

**สรุป: มี hysteresis loop = first-order transition ยืนยันแล้ว**
- สแกนขึ้น: ชน gate ต้องดันถึง g_YX ≈ 1.0–1.3
- สแกนลง: ค้างชน gate ลงไปถึง g_YX = 1.0 แล้วเด้งกลับ Y เล็กที่ 0.8
- ระบบ "จำ" สถานะก่อนหน้า (memory) — ลายเซ็น first-order ที่ continuous transition จะไม่มี

โค้ด/ผล: `AUDIT_v7_hysteresis.py` (+json/log)

## 6. ข้อควรระวัง / งานที่ยังค้าง

1. hysteresis ใช้ 5 seeds ต่อทิศ — loop robust พอ (ทุก seed พฤติกรรมเดียวกัน) แต่ความกว้างของ loop ยังแม่นได้อีกถ้า n ใหญ่ขึ้น
2. สัดส่วนชน gate 50%±9% (SE binomial n=30) → transition midpoint มี uncertainty ±0.05 ใน g_YX
3. ผล v7 ทั้งหมดเป็น **โมเดลใหม่ (v7)** — ไม่ควรปนใน `manuscript_v6.tex` (ที่ยึด v6)
4. `AUDIT_v7_feedback_n30` ใช้ n_therm=20 → ตัวเลข "continuous" ในนั้นล้าสมัย ถูกแทนด้วย `_transition_clean`

## 8. ระดับ A — dependence ต่าง ๆ (n=30, n_therm=40, 2026-08-30)

### 8.1 n=30 hysteresis — loop width ยืนยัน (A1)
| g_YX | UP ชน gate | DOWN ชน gate |
|---|---|---|
| 0.8 | 0% | 0% |
| 1.0 | 23% | 100% |
| 1.1 | 77% | 100% |
| 1.2 | 93% | 100% |
| 1.3 | 97% | 100% |
| 1.4 | 100% | 100% |

→ loop width ≈ 0.3 ใน g_YX, first-order ยืนยันด้วย n=30 (ทุก seed สม่ำเสมอ)

### 8.2 d-dependence — monotonic (A2)
critical g_YX (50% ชน gate): d=3 ≈ 1.1, d=4 ≈ 1.2–1.3, d=5 ≈ 1.5–1.8
→ **monotonic** ไม่มี curve/จุดหักเห สอดคล้อง dimensional dilution

### 8.3 N-dependence — อ่อน (A3)
N=4, 6, 8 ที่ g_YX=1.3 ชน gate ≈ 77%, 73%, 77% — **แทบไม่ต่าง** สรุป "N เล็กเปราะกว่า" ยังไม่แข็งแรง N=12 ไม่ได้ทำ (full recompute ช้าเกินไป)

### 8.4 gXY-dependence — critical ลดเมื่อ gXY เพิ่ม (A4)
| g_XY | critical g_YX (50%) | X ratio ณ จุดนั้น |
|---|---|---|
| 0.8 | ~1.2 | 4.8 (healthy) |
| 1.15 | ~1.1 | 10.2 (X saturation) |

→ ไม่ใช่กฎ g_YX ≳ α·g_XY ง่าย ๆ; feedback loop ผ่าน extent ที่ซับซ้อน

## 9. ระดับ B — pinpoint + scaling law (2026-08-30)

### 9.1 d=5 fine scan (B5) — pinpoint critical
g_YX 1.40..1.90 step 0.05, n=30, n_therm=40:

| g_YX | ชน gate | g_YX | ชน gate |
|---|---|---|---|
| 1.40 | 40% | 1.65 | 57% |
| 1.45 | 50% | 1.70 | 63% |
| 1.50 | 50% | 1.75 | 63% |
| 1.55 | 43% | 1.80 | 67% |
| 1.60 | 43% | 1.85 | 80% |
| | | 1.90 | 80% |

→ critical d=5 ≈ **1.45** (50% แรก) แต่ curve **ไม่ monotonic สะอาด** (มี plateau
ที่ 1.45–1.6 ก่อนไต่ต่อ) — เป็น noise ของ n=30 (±9%) หรือ transition กว้างกว่า d=3

### 9.2 Scaling law critical g_YX vs d (B7)
refined critical (50% hit): **d=3 → 1.15, d=4 → 1.25, d=5 → 1.45**

| fit | ผล |
|---|---|
| linear | g_c = 0.150·d + 0.683 (R²=0.96) |
| power law | g_c ~ d^0.446 |
| g_c/d | 0.38, 0.31, 0.29 (ลดลง, ไม่คงที่) |

→ critical g_YX โต**แบบ sublinear** ตาม d (ไม่ใช่ ∝d ที่ dimensional dilution
บริสุทธิ์ทำนาย) แปลว่า observer หลายมิติ "เจือจาง" coupling ช้ากว่าที่ naive dilution
คาด
⚠️ แค่ 3 จุด (d=3,4,5) ไม่พอฟิต scaling law จริงจัง — ต้อง d=6,7 เพิ่ม

### 9.3 N=12 — DEFERRED (B6)
v7 ใช้ full recompute ที่ N=12 = 144 matrix elements × O(N²) action ต่อ update
ช้าเกินไป ต้อง optimize เป็น incremental delta sampler (แบบ v6) ก่อนถึงทำได้จริง

## 10. กลไก bistability = eigenvalue condensation (ยืนยันแล้ว, 2026-08-30)

### 10.1 หลักฐานจาก eigenvalue spectrum
ตัวชี้ `c_top` = สัดส่วนของ extent (Tr Y²) ที่อยู่ใน eigenvalue ใหญ่สุด (เรียงตาม |magnitude|):

| สถานะ | extent | c_top |
|---|---|---|
| basin เล็ก (Y ไม่ชน gate) | 0.46–0.72 | 0.34–0.48 (กระจาย) |
| basin ชน gate | 9.99–10.00 | **0.96–0.99 (condensed)** |

- basin เล็ก: eigenvalue กระจายหลายตัว (|λ| ~ 1)
- basin ชน gate: eigenvalue เด่นตัวเดียว |λ| ≈ 7.6 ครอง 96–98% ของ extent

### 10.2 กลไก nonlinear — Tr(Y⁴) กระโดด
`Tr(Y⁴)/(N·extent²)` กระโดดจาก ~1.9 (กระจาย) → ~5.5 (condensed, ขีดบน = N = 6)

→ coupling term `−gYX·ŵ²·Tr(Y⁴)` กระโดด ~3× ต่อ extent เดิมเมื่อเกิด condensation
→ positive feedback: condensed มากขึ้น → coupling แรงขึ้น → double-well → bistability

### 10.3 ทำไม naive mean-field ล้มเหลว
naive mean-field สมมติ `Tr(Y⁴) ≈ N·extent²` (eigenvalue กระจายสม่ำเสมอ) ซึ่ง
**ละ condensation ที่เป็นหัวใจของ nonlinearity** ไป จึงทำนาย continuous shift
+ diverge ที่ gYX=6 แทน bistability จริงที่ ~1.2

### 10.4 ข้อสังเกตเชิงเทคนิค
eigenvalue ที่เด่นเป็น**ค่าลบ** (λ ≈ −7.6) ในหลาย seed — ต้องเรียง eigenvalue ตาม
|magnitude| ไม่ใช่ตามค่า มิฉะนั้น c_top จะต่ำผิด (bug ที่เจอและแก้แล้วใน script แรก)

### 10.5 Derive analytic: 2-state energy-crossing model
โมเดล Y eigenvalue เป็น 2 สถานะ แล้วหาจุดที่ action ข้ามกัน:

| ปริมาณ | Y เล็ก (spread) | Y ชน gate (condensed) |
|---|---|---|
| Tr(Y²) | N·rY² = 1.5 | N·10 = 60 |
| Tr(Y⁴) | N·rY⁴ = 0.375 | N²·10² = **3600** |

`Tr(Y⁴)` ต่างกัน **~9600×** ระหว่างสองสถานะ → นี่คือที่มาของ first-order ที่แหลม

critical gYX จาก crossing = λY·(N·10−N·rY²)² / (w²·(TrY⁴_c − TrY⁴_s)):

| w² (alignment X→Y) | critical gYX |
|---|---|
| 1.0 (basin เล็ก) | 0.95 |
| **0.79** | **1.20** ← ตรงค่าที่วัด |
| 0.67 (ที่ transition) | 1.42 |

→ naive mean-field (w²=1 คงที่) ให้ 0.95 ต่ำไป 7%; รวม feedback ของ w²
(alignment ลดลงเมื่อ Y เริ่มชน) เลื่อน critical ไป ~1.2 ตรงจริง

**กลไกครบวง:** Y condense → Tr(Y⁴) กระโดด 9600× → positive feedback; แต่
ขณะเดียวกัน Y condense → Tr(Y) เปลี่ยน → X trace เปลี่ยน → w² ลด (1.0→0.67)
→ หน่วง back-reaction → สมดุลที่ gYX≈1.2

### 10.6 บทเรียนเชิงระเบียบวิธี: w² เป็น stochastic — จุดจบ analytic ที่ถูกต้อง
พยายาม "ปิด loop" ด้วย closed-form self-consistency ของ w² (model เป็นฟังก์ชัน
ราบรื่นของ extent e) แล้วหา minima ของ free energy → **สร้าง artifact** (extra
minima ปลอม) ไม่ใช่ transition จริง

สาเหตุ: w² ไม่ใช่ฟังก์ชัน deterministic ของ extent — ข้อมูลจริงแสดงว่า seed ต่างกัน
ที่ extent เดียวกันให้ w² ต่างกัน (gYX=1.3: seed 42 ได้ 0.67, seed 43 ได้ 1.00) เพราะ
w² ขึ้นกับว่า trace ของ X reorient ไปทางไหน ซึ่งเป็นผลของ thermal fluctuation ทั้งระบบ

**ข้อสรุป:** 2-state model (§10.5) คือจุดจบ analytic ที่ถูกต้อง — จับ essence ได้ครบ
(condensation + Tr(Y⁴) jump 9600× + first-order + critical ≈1.2) ส่วน w² ที่เป็น
stochastic อธิบายได้ดีที่สุดด้วย simulation ไม่ใช่ closed-form ซึ่งสมเหตุสมผลทางฟิสิกส์

## 11. N=12 X-robustness — X ยังแข็งแรงที่ N ใหญ่ (2026-08-30)

คำถาม: ที่ N=12 (matrix ใหญ่ 144 elements) ทิศทางเวลา X ยังทนทานต่อ back-reaction ไหม?

ผล (d=3, gXY=0.8, n_therm=40, 5 seeds):

| g_YX | X ratio | X align | Y_max |
|---|---|---|---|
| 0.8 | 4.849 ± 0.061 | 100% | 0.55 (เล็ก) |
| 1.5 | 4.782 ± 0.081 | 100% | 10.0 (ชน gate) |
| 2.0 | 4.761 ± 0.125 | 100% | 10.0 |
| 3.0 | 4.933 ± 0.145 | 100% | 10.0 |
| 5.0 | 4.889 ± 0.017 | 100% | 10.0 |

**คำตอบ: ใช่** — แม้ Y ชน gate เต็มที่ (Ymax=10.0, 5/5 seed) X ratio ยัง 4.76–4.93,
alignment 100% ทุก seed ทุก g_YX รวม g_YX=5.0 (แรงกว่า forward 6 เท่า)

### เทียบ N=6 vs N=12
| | N=6 | N=12 |
|---|---|---|
| X ratio ที่ g_YX สูง | ~4.7–4.8 | ~4.8–4.9 |
| Y ชน gate ที่ g_YX | ~1.2 | ~1.5 (ช้ากว่า) |

→ N ใหญ่ขึ้น Y ทน feedback ได้ดีขึ้นเล็กน้อย (สอดคล้อง A3: N-dependence อ่อน,
N ใหญ่เปราะน้อยลง) ส่วน X ยัง healthy ทั้งคู่

### ข้อสังเกตเชิงเทคนิค
acceptance rate ที่ N=12 ลดลงเหลือ 0.44–0.46 (จาก 0.59 ที่ N=6) — ปกติสำหรับ matrix
ใหญ่ (proposal step eps=0.25 ใหญ่เกินไปเล็กน้อย) ไม่กระทบข้อสรุปเชิงคุณภาพ

## 12. N≥12: eps fix + N=16 trend + d=4,5 ที่ N=12 (2026-08-30)

### 12.1 ปรับ step size ที่ N=12 (eps fix)
acceptance ที่ N=12 ต่ำ (0.46) เพราะ eps=0.25 ใหญ่เกินไป แก้โดยลด eps:

| eps | acceptance | X ratio |
|---|---|---|
| 0.25 (เดิม) | 0.46 | 4.78 |
| **0.20** | **0.55** | 4.81 |
| 0.18 | 0.62 | 4.99 |
| 0.15 | 0.62 | 4.88 |
| 0.12 | 0.67 | 5.00 |

→ ใช้ **eps=0.20** เป็นมาตรฐานสำหรับ N≥12 (acceptance กลับมา ~0.55 ไม่ต้องเพิ่ม n_therm)

### 12.2 N=16 — critical g_YX เพิ่มขึ้นตาม N (ยืนยัน)
critical g_YX (50% ชน gate, d=3): N=6 ≈ 1.2, N=12 ≈ 1.5, **N=16 ≈ 1.7–2.0**
→ แนวโน้ม "critical เพิ่มขึ้นตาม N" ยังคงอยู่: N ใหญ่ขึ้น Y ทน feedback ได้ดีขึ้น
(back-reaction เจือจางต่อ degree of freedom มากขึ้น)

### 12.3 d=4,5 ที่ N=12 — scaling law ยังถือ (เชิงคุณภาพ)
critical g_YX ที่ N=12: d=3 ≈ 1.5, d=4 ≈ 1.7, d=5 ≈ 2.0–2.2
→ critical ยังเพิ่มขึ้นตาม d ที่ N ใหญ่ สอดคล้อง `g_c ~ d^0.446` จาก N=6

### 12.4 ข้อควรระวัง
- ข้อ 12.2/12.3 ใช้ n=5 (pilot) — สัดส่วนชน gate ±22% (SE binomial n=5) critical เป็นช่วง
- ที่ N=16, g_YX=2.0 มี seed หนึ่ง X ratio ตกเหลือ 3.65 (จาก 5) — outlier ที่ต้องจับตา
  (ยังไม่ conclusive ว่า thermalization หรือสัญญาณเริ่ม destabilize ที่ N ใหญ่)

## 7. ความหมายทางฟิสิกส์ (ตีความอย่างระวัง)

Back-reaction ทำให้ **observer อิ่มตัว/ชน gate ก่อนที่จะรบกวนการชี้ทิศทางเวลา** — เป็นหลักฐานว่า asymmetry "observer วัด system ไม่ใช่กลับกัน" แข็งแรง: Y ส่งให้ X แค่ "ทิศ" (normalize) แต่ X ส่งกลับ Y เป็น "แรง" (coupling energy) จึง Y พังก่อน X รู้สึก


## 13. Discrimination Test — condensation ratio แยกจาก baseline จริง (2026-08-31)

ตรวจว่า "X ratio" (max extent / mean rest) discriminate จากสถานะไร้ coupling จริงหรือไม่
(สคริปต์: `matrix/check_v7_condensation_discrimination.py`, N=8, D=3, d=2, n_therm=40, 5 seeds):

| สถานะ | X ratio | alignment |
|---|---|---|
| null (random init, ไม่ thermalize) | 1.32 ± 0.18 | — |
| baseline (g_XY = 0, thermalize) | **1.10 ± 0.05** | 60% |
| จริง g_XY = 0.8 | **4.55 ± 0.35** | **100%** |
| จริง g_XY = 1.05 (gate) | **9.61 ± 0.46** | **100%** |

- ratio จริงห่างจาก baseline ~60σ → **discriminate ชัดเจน** (ต่างจาก R_causal/R_hyper ของ
  graph/hypergraph ซึ่ง shuffle ค่าแล้วได้ค่าเท่าเดิม — ดู `SGOED_v9_hypergraph_notes.md` §6)
- **Spectral signature (ยืนยันกลไก):** X_μ ที่ coupling เลือกมี eigenvalue ตัวเดียว = 5.99
  ตัวรอง = 0.26 → **λmax/λ2nd = 23.2 = rank-1 condensation จริง** (baseline g_XY=0:
  spectrum กระจาย −1.8…1.4, ratio 1.29)
- alignment 100% vs 60% baseline → coupling เลือก μ ตรงกับ v̂ จาก Y จริง ไม่ใช่เรื่องบังเอิญ

→ **ข้อสรุป:** condensation ratio เป็น observable ที่ตรวจสอบแล้วว่าเป็นฟิสิกส์จริง —
แกนหลักของ matrix model (v6/v7) ที่จะนำไปเผยแพร่
