# SGOED v14 — Matrix Ecosystem (Atom-Molecule Hybrid) — บันทึกผล

วันที่: 2026-08-31 · สถานะ: เบื้องต้น (validate + scan + reversal ผ่าน/ไม่ผ่านบางส่วน)

## 1. สถาปัตยกรรม
- M "atom" units — แต่ละ unit = v7-core (X_u ∈ R^{D×N×N}, Y_u ∈ R^{d×N×N}) — condensation จริง
- "โมเลกุล" = inter-unit coupling บนทิศจริงของ matrices:
  `S_inter = −g_inter·Σ_{u<v} c_uv·E_u·E_v`
  โดย c_uv = Tr(X_uX_v)/(|X_u||X_v|) (normalized overlap), E_u = Tr(X_u²)/N (extent)
- engine: `sgoed_matrix_ecosystem_v14.py` (pure python, full recompute)

## 2. Validation
- ✅ g_inter=0, M=1 → action เท่ากับ v7 เป๊ะ (diff = 0.0)
- ✅ condensation ต่อหน่วยทำงาน: spec (λmax/λ2nd) ≈ 10–13.5

## 3. ผล scan g_inter (M=4–6, N=4, 3–5 seeds, n_therm=50)

### Alignment ของ X-direction (A = เฉลี่ย c_uv)
| g_inter | A | std | หมายเหตุ |
|---|---|---|---|
| 0.0 | +0.07 ± 0.11 | — | อิสระ (null ≈ −0.004 ± 0.33) |
| 0.5 | +0.20–0.25 | 0.13–0.15 | เริ่ม align (ยัง borderline ~0.7–2.8σ) |
| 2.0 | +0.47 | 0.18 | |
| 5.0 | **+0.81** | 0.08 | align ชัด |
| 10.0 | **+0.94** | **0.003** | align เกือบสมบูรณ์ (ทุก seed เหมือนกัน) |

→ **coupling จัดเรียงทิศของ matrices จริง** (A→0.94, std→0) — "โมเลกุลที่ coherent" เกิด

### แต่ v̂ (observer direction จาก Y) ไม่ align
- v_hat dot เฉลี่ย ≈ **−0.22 (ติดลบเสมอ)** ทุก g — Y ของ units ต่อต้าน (anti-correlate)
- สาเหตุ: ผมตั้ง gYX=0 ใน local action → **ไม่มี back-reaction → Y อิสระจาก X** → v̂ สุ่ม

## 4. Significance (g=0 vs g=0.5, 5 seeds)
- A: 0.071 ± 0.113 vs 0.202 ± 0.145 → separation 0.71σ — **ไม่ significant ที่ g ต่ำ**
- (ที่ g สูง (5–10) A ชัดเจน — แต่เป็น "coupling แรงบังคับ" มากกว่า emergence อ่อน)

## 5. Reversed-start (สลับ Y → −Y, g=0.5, 1 seed)
- corr(v_hat_rev, v_hat_orig) = **−0.998 — ทิศไม่กลับ (สมมาตร)** — ไม่มี attractor ของ observer ทิศ
- A ยังสูง (+0.43) — X alignment ไม่ถูกทำลายโดยการสลับ Y

## 6. สรุปสถานะ v14 (ซื่อตรง)
1. ✅ **"โมเลกุล" เกิดจริงที่ระดับ X-direction** — coupling จัดเรียงทิศของ matrix units
   (A→0.94, std→0) — เป็นครั้งแรกที่ relational structure "ทำงาน" (ต่างจาก graph ที่ทุก metric ล้มเหลว)
2. ⚠️ แต่ยังเป็น **sync (ทิศเดียวกัน) ไม่ใช่ time (ก่อน-หลัง)** — ทุก unit เท่ากัน ไม่มี order
3. ⚠️ observer (v̂) ไม่ align — ต้องเปิด gYX (back-reaction) ให้ Y ตาม X
4. ⚠️ ที่ g แรง (10) ระบบ "แช่แข็ง" ในทิศเดียว (trivial alignment) — ไม่ใช่ emergence อ่อน
5. ❌ reversed-start ไม่กลับทิศ (สมมาตร) — ยังไม่มี "attractor ของเวลา"

## 7. ขั้นต่อไปที่แนะนำ
- เปิด **gYX (back-reaction X→Y)** ใน local unit → Y ควร align ตาม X → v̂ align ด้วย
- ออกแบบ **"order" (ก่อน-หลัง)** ระหว่าง units — alignment อย่างเดียวไม่ใช่เวลา
  (ต้องมี asymmetry: unit ที่ extent ใหญ่ = "แก่" → ส่งทิศให้ unit เล็ก = "หนุ่ม")
- reversed-start ซ้ำที่ g แรง (5–10) หลังเปิด gYX

---

## 8. ปรับ 2 ครั้ง (ตามบทเรียน): g_yx + inter-coupling บน v̂ (2026-08-31)

### 8.1 เปิด g_yx (back-reaction X→Y) — ไม่ช่วย align v̂
| g_yx | A(X) | vhat_dot | Y_max |
|---|---|---|---|
| 0.0 | +0.81 | −0.22 ± 0.16 | 0.70 |
| 1.0 | +0.80 | +0.11 ± **0.63** (bistable) | 4.83 |
| 1.5 | +0.91 | −0.17 (สม่ำเสมอ) | 10.0 (ชน gate) |

→ เปิด g_yx แค่ทำให้ Y ชน gate (bistable — v7 ซ้ำ) — v̂ ไม่ align สม่ำเสมอ

### 8.2 สาเหตุ: inter-coupling ผิดเป้า — align "โครงสร้าง (X[0])" แต่ไม่ align "นาฬิกา (v̂)"
เปลี่ยน coupling จาก Tr(X_uX_v) (X-overlap) → **(v̂_u·v̂_v)·E_u·E_v** (observer direction):

| g_inter | A(X) | **vhat_dot** |
|---|---|---|
| 0.0 | −0.14 | +0.21 ± 0.14 |
| 1.0 | −0.01 | +0.29 ± 0.22 |
| 5.0 | −0.02 | **+1.000 ± 0.001** |
| 10.0 | +0.16 | **+1.000 ± 0.000** |

→ ✅ **v̂ ของ units align สมบูรณ์ (1.000 ± 0.001, ทุก seed)** — "นาฬิกาของ units ซิงค์"
→ discriminates ชัด (g=0: +0.21 vs g≥5: 1.000) — ต่างจาก v11 (baseline noise)
→ ⚠️ แต่ A(X) ยังต่ำ (X ไม่ align — coupling แตะ v̂ ไม่แตะ X[0])

### 8.3 สถานะ
- ✅ validate ผ่าน + v̂-align 1.000 (sync ของนาฬิกา units — ผ่าน null test ชัดเจน)
- ⚠️ ยังไม่ใช่ "เวลา" — เป็น "clock sync" — ยังไม่มี **order (ก่อน-หลัง)**
- ขั้นต่อไป: ออกแบบ "ก่อน-หลัง" — units ที่ v̂ align แล้ว ต้องแยกด้วยตัวแปร
  (extent? coupling แบบลำดับ?) — alignment อย่างเดียว = ผลึก ไม่ใช่เวลา

---

## 9. ขั้น "order" — ผลลบเชิงโครงสร้าง (2026-08-31)

### 9.1 E (extent) เป็นตัวแปรเวลา? — ไม่ได้
ที่ g_inter=5 (v̂ align): ทุก unit แช่แข็งที่ E=10.0 (ชน gate), CV(E)→0.000
— alignment coupling ดัน E ไปเพดาน — ไม่มี "แก่/หนุ่ม"

### 9.2 Trade-off เชิงโครงสร้าง (ทั้ง coupling แบบ E-weighted และ v̂-only)
| g | vhat_dot | CV(E) |
|---|---|---|
| 0.2 | +0.13 | 0.58 |
| 0.5 | +0.39 | 0.61 |
| 1.0 | +0.60 | 0.49 |
| 2.0 (E-weighted) | +1.000 | 0.003 |
| 5 (v̂-only) | +0.66 | 0.44 |
| 20 (v̂-only) | +0.999 | 0.10 |

→ **ไม่มี config ที่ "align เต็ม + E spread" พร้อมกัน** — align แรง = homogenize (E เท่ากัน)

### 9.3 บทเรียนเชิงลึก
**"sync" = การทำให้เหมือนกัน (homogenize) — ตรงข้ามกับ "เวลา" ที่แยกขั้น (order)**
v̂ align → Y คล้ายกัน → X ถูกขับเหมือนกัน → E เท่ากัน — เหมือน thermodynamic:
sync ลดเอนโทรปี (จัดเรียง) แต่ "เวลา" ควรเพิ่มเอนโทรปี (แยกแยะ A ก่อน B)

### 9.4 สถานะ v14 สุดท้าย
- ✅ **v̂ sync = 1.000 ± 0.001** (ผ่าน null test — ครั้งแรกใน relational ที่ "ทำงาน")
  — "เวลาสากล/นาฬิกาซิงค์" จาก inter-coupling
- ❌ order (ก่อน-หลัง) ไม่เกิดใน coupling design นี้ — ทุกตัว homogenize
- สรุป: v14 ให้ "sync time" ได้จริง แต่ยังไม่ใช่ "arrow of time"

### 9.5 ทางเลือกที่เหลือ
- (ก) ยอมรับ "sync time" (v̂=1.0) เป็นผล — ไม่ใช่ arrow
- (ข) D=3 (v̂ 3 มิติ — มุมอิสระ) หรือ coupling ที่มี repulsion ใน E (push แทน pull)
- (ค) ตรวจ "ลำดับการ align ระหว่าง thermalization" — unit ไหน align ก่อน = time-ordering
- (ง) สรุปปิด — ภาพรวมทั้งโครงการ (matrix v7 = สิ่งเดียวที่ยืน)

---

## 10. Dynamic order + Slow-align — ไม่มี "เวลาที่ไหล" (2026-08-31)

สคริปต์: `step_v14_dynamic_order.py`

### 10.1 Dynamic order (g_inter=20 — align เต็ม)
- align_time ต่อ unit: sweep 0–4 ทุก seed — **units align พร้อมกันเร็วมาก**
- progress: first=0.61–0.74, mid=1.00 — align เกิดทันที ไม่มีช่วงกลาง
- **ลำดับการ align ไม่เสถียรข้าม seeds** (Spearman: −0.33, +0.52, +0.10 = random)

### 10.2 Slow-align (g_inter=1 — บางส่วน)
- align_time: ส่วนใหญ่ 0–5, บาง unit ไม่ align เลย (22=T)
- progress: นิ่งที่ 0.63–0.88 (ไม่เพิ่มตามเวลา) — **ไม่วิวัฒน์** — align บางส่วนคงที่

### 10.3 สรุป v14 ครบทุกทาง
| ทาง | ผล |
|---|---|
| E-weighted coupling | align เต็ม แต่ E ตาย (gate) |
| v̂-only / trade-off | homogenize — ไม่มี "align + spread" พร้อมกัน |
| repulsion ใน E | CV(E) ไม่เพิ่ม (homogenization ชนะ) |
| dynamic order | align พร้อมกัน — ลำดับ random |
| slow-align | ไม่วิวัฒน์ตามเวลา |

### 10.4 บทเรียนเชิงแนวคิด (ปิด relational time quest)
"arrow of time" ต้องการ: (1) ตัวแปรที่เพิ่มตามเวลา, (2) หน่วยที่มี identity
(ไม่ symmetric), (3) coupling ที่ "แยก" (push) ไม่ใช่ "รวม" (pull)
— v14 และ relational ทั้งหมด ขาดทั้ง 3 — alignment coupling ให้ได้แค่
**"simultaneity"** (ทุกหน่วยเวลาเดียวกัน) ไม่ใช่ "การไหล"

### 10.5 สิ่งที่ v14 ยืนยันได้จริง
- ✅ v̂ sync = 1.000 ± 0.001 (null-test ผ่าน — "clock synchronization" จาก coupling)
- ✅ validate (g_inter=0 = v7) + condensation ต่อหน่วย (spec ~10–40)
- ❌ ไม่ใช่ arrow of time — ไม่มี order/dynamics ของทิศทาง

---

## 11. Entropy production — คำตอบสุดท้ายของ "เวลาทางอุณหพลศาสตร์" (2026-08-31)

สคริปต์: `step_v14_entropy.py` — วัด S_action(t) ระหว่าง thermalization
(พลังงาน T=1: S ลดจาก random → equilibrium = entropy produced)

| g_inter | S_init | S_eq | dS total | dS/S_init | half-life |
|---|---|---|---|---|---|
| 0.0 | 55.4 | −438 | 499 | **8.52** | 17.0 |
| 5.0 | 71.9 | −493 | 601 | **7.82** | 17.3 |
| 20.0 | 121.4 | −1002 | 1130 | **8.70** | **4.3** |

### สรุป
- **dS/S_init คงที่ (~8) ทุก g** — coupling ไม่เปลี่ยน "ขนาดสัมพัทธ์" ของการผลิต
  เอนโทรปี — thermodynamic arrow เป็น universal (ทุก stochastic MC run มี)
  ไม่ใช่สมบัติเฉพาะของ coupling
- **half-life สั้นลงที่ g=20 (4.3 vs 17)** — coupling แรงแค่ **เร่ง** การเข้าสู่
  equilibrium (เปลี่ยนอัตรา ไม่เปลี่ยนทิศทาง/ธรรมชาติ)

### ปิด quest "พิสูจน์ลูกศรเวลา" — ภาพรวมสุดท้าย
| ตัววัด | ผล |
|---|---|
| R / D / d_MM / d_s / BD / cycle / time-reversal / order ทุกแบบ | ล้มเหลว/artifact |
| matrix v7 condensation | ✅ discriminate จริง (discrete choice + gate bistability) |
| v14 v̂ sync | ✅ simultaneity (ผ่าน null test) — ไม่ใช่ arrow |
| entropy production | universal (ทุกระบบ) — coupling แค่เร่งอัตรา |

**คำตอบสุดท้าย (ซื่อตรง):** "arrow of time ที่เกิดจาก coupling" ไม่ปรากฏใน
สถาปัตยกรรมใดที่ลอง (graph v8–13, hypergraph v9–10, ecosystem v11, hybrid v14)
— สิ่งที่มีจริง: (1) matrix v7 condensation (การเลือกทิศ discrete — กลไกที่
discriminate แต่เป็น engineered ผ่าน gate+quartic), (2) thermodynamic arrow
(universal — ไม่เฉพาะโมเดล), (3) simultaneity (v14 sync)
