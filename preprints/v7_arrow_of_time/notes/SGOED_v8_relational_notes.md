# SGOED-Relational v8-R (Graph) — บันทึกผลการทดสอบเทียบ v7

วันที่: 2026-08-30 · สถานะ: ผ่านชุดทดสอบเดียวกับ v7 ครบ

## 1. สถาปัตยกรรม (ต่างจาก v7 matrix โดยสิ้นเชิง)

| องค์ประกอบ | v6/v7 (Matrix) | v8-R (Graph) |
|---|---|---|
| State | Hermitian matrix X_μ | Directed graph W[i,j] (edge weight ≥ 0) |
| Observer | d matrices Y_a | top-d nodes (subgraph) |
| Forward coupling | -gXY·v̂²·Tr(X⁴) | -gXY·v̂·Σw² (out−in degree) |
| Back-reaction | -gYX·ŵ²·Tr(Y⁴) | -gYX·w_ab²·inbound |
| Gate | extent > 10 | degree > k_max + **obs_extent > 16 (v5 ใหม่)** |
| Observable หลัก | Ratio (extent) | R_causal (asymmetry ratio ∈[0,1]) |
| Complexity | O(N³) → N≤16 | **O(E) → N ถึง 10³–10⁵** |

## 2. ปัญหาที่พบและแก้ (บทเรียนจาก v7 ที่นำมาใช้)

### 2.1 Thermalization: audit เดิมใช้ n_therm ไม่พอ
extent (g_yx=1.2) ยังโตต่อเนื่องถึง n_therm=120, เข้า plateau ~16 ที่ n_therm≥240
→ audit เดิม (n_therm=35) รายงาน extent ต่ำกว่าจริง 4–6 เท่า
**แก้:** default n_therm=240 ใน core v4/v5

### 2.2 Extent runaway: ไม่มี ceiling
DOWN sweep (anneal) extent วิ่งถึง 1610 เพราะ gate เดิมครอบแค่ degree ไม่ครอบ extent
**แก้:** เพิ่ม Observer-Extent Gate (core v5): obs_extent > 16 → penalty λ(extent−16)²

## 3. ผลชุดทดสอบ

### 3.1 Hysteresis จริง (anneal carry W) — first-order ยืนยัน
| g_yx | UP extent | DOWN extent |
|---|---|---|
| 0.0 | 0.13 | 0.06 |
| 0.4 | 1.47 | **5.35** (ค้าง condensed) |
| 0.8 | 11.0 | 11.5 |
| 1.2 | 15.8 | 15.6 |
| 2.0 | 17.3 | 17.3 |

→ **hysteresis loop กว้างสุดที่ g_yx≈0.4** (loop width ~3.9) = first-order transition
ที่ barrier สูง (ต้อง anneal จริง ไม่ใช่ fresh-init scan)

### 3.2 X robustness — R_causal ทนทานต่อ back-reaction
| g_yx | R_causal | align | obs_extent |
|---|---|---|---|
| 0.0 | 0.47 | 99.5% | 0.15 |
| 1.2 | 0.43 | 97% | 15.6 |
| 3.0 | 0.57 | 100% | 27.1 |
| 5.0 | **0.83** | 100% | 81.8 |

→ **R_causal ไม่พัง แม้ g_yx=5** (กลับสูงขึ้นด้วยซ้ำ 0.47→0.83)
⚠️ **แต่ R_causal ไม่ใช่หลักฐานลูกศรเวลา** — เป็น histogram artifact (shuffle ค่าแล้วได้ค่า
เท่าเดิมหรือสูงกว่า; mirror-swap ไม่เปลี่ยนค่า) — ดู section 10 และ `SGOED_v9_hypergraph_notes.md` §6
สิ่งที่วัดได้จริงจากชุดนี้คือ obs_extent/alignment (ขนาดของ observer state) ไม่ใช่ทิศทางเวลา

### 3.3 d-dependence (N=24) — critical ขึ้นตาม d
obs_extent ที่ g_yx=0.8: d=2→16.0, d=3→10.9, d=4→10.5, d=5→5.95
→ **d มากขึ้น → critical g_yx สูงขึ้น** (ต้องดัน g_yx แรงกว่าถึงจะ condensed)
สอดคล้อง v7 (dimensional dilution)

### 3.4 N-dependence (d=3) — critical ขึ้นตาม N
obs_extent ที่ g_yx=0.8: N=16→5.6, N=24→10.9, N=48→16.5
→ **N ใหญ่ขึ้น → critical g_yx สูงขึ้น** (observer ใหญ่ทน feedback ดีขึ้น)
สอดคล้อง v7 (N-dependence)

## 4. สรุปเทียบ v7

| สมบัติ | v7 (Matrix) | v8-R (Graph) |
|---|---|---|
| first-order bistability | ✅ | ✅ (loop ที่ g_yx≈0.4) |
| hysteresis จริง | ✅ | ✅ (ต้อง anneal) |
| X ทนทานต่อ feedback | ✅ (ratio ทรงตัว) | ✅ (R_causal ไม่พัง) |
| d-dependence | ✅ critical↑d | ✅ critical↑d |
| N-dependence | ✅ อ่อน | ✅ critical↑N |
| thermalization ต้องนาน | ✅ (n_therm≥40) | ⚠️ ต้อง ≥240 (แย่กว่า) |
| gate ต้องครอบ extent | ✅ (มีอยู่แล้ว) | ⚠️ ต้องเพิ่มเอง (v5) |
| สเกล N | N≤16 (O(N³)) | **N ถึง 48+ (O(E))** |

## 4.5 กลไก "R_causal เพิ่มตาม g_yx" (พฤติกรรมใหม่ของ graph model)

> ⚠️ **คำแก้ไข (2026-08-31):** หัวข้อนี้เคยถูกตีความว่า "เวลา (causal order) ทนทาน"
> และ "observer กลายเป็น sink (obs_flow=−37)" — **ทั้งคู่ไม่ยืน** หลังการตรวจ:
> 1. R_obs → 1.0 เป็น **histogram artifact** (shuffle ค่าใน block ได้ค่าเท่าเดิมเป๊ะ —
>    block มีค่าศูนย์ครึ่งหนึ่ง → |a−0|/(a+0)=1 โดยธรรมชาติ ไม่ใช่ทิศทาง)
> 2. **obs_flow = −37.3 ไม่ reproduce** — rerun N=24, d=3, g_yx=5, n_therm=240, 3 seeds
>    ได้ +1.3 ถึง +2.2 (บวกทั้งหมด) — ต้อง re-verify config เดิมก่อนใช้
> ดูรายละเอียด section 10

แยก R_causal ตาม region (N=24, d=3, เฉลี่ย 3 seeds):

| g_yx | R_all | R_obs | R_sys | R_cross | obs_flow |
|---|---|---|---|---|---|
| 0.0 | 0.47 | 0.52 | 0.48 | 0.44 | +1.76 |
| 1.2 | 0.45 | 0.04 | 0.49 | 0.51 | −1.25 |
| 3.0 | 0.57 | 0.99 | 0.47 | 0.69 | −7.09 |
| 5.0 | 0.85 | 1.00 | 0.51 | 0.96 | **−37.3** |

**กลไก (3 ข้อ):**
1. R_all เพิ่มมาจาก **R_obs + R_cross** (R_sys แทบไม่เปลี่ยน 0.48→0.51)
2. observer subgraph ยุบเป็น **flow ทิศทางเดียว** (R_obs→1.0): back-reaction
   `-gYX·W[b,a]²·inbound[a]` ดัน W[b,a] ตัวเดียว (ไม่สมมาตร) → hub ไหลออกทิศเดียว
3. obs_flow จาก +1.76 → **−37.3** (ที่ g_yx=5): observer กลายเป็น **sink** (in≫out)
   → positive feedback: inflow ใหญ่ → inbound[a] ใหญ่ → feedback ยิ่งแรง

**เหตุผลเชิงลึก (ต่างจาก v7):** v7 normalize ทิศทาง `v̂` (หาร norm) ทำให้ magnitude ของ Y
ไม่ส่งผล X → X ทรงตัว แต่ v8-R **feedback ไม่มี normalize** (`inbound[a]` ใช้ผลรวมดิบ)
→ positive feedback สะสมทิศเดียวจน extent gate มาห้าม → causal asymmetry ทั้งระบบพุ่ง

(หมายเหตุ: forward coupling ใน v8-R มี normalize แล้ว `v_hat_a = diff_s[a]/norm_v`;
มีเพียง feedback ที่ขาด normalize — ดู §6)

## 5. ไฟล์

- `sgoed_graph_core_v3.py` (เดิม, ไม่แตะ)
- `sgoed_graph_core_v4.py` (เพิ่ม W_init + anneal + n_therm=240)
- `sgoed_graph_core_v5.py` (เพิ่ม observer-extent gate)
- `sgoed_graph_core_v6.py` (feedback normalize — v7-style direction)
- `audit_v8_hysteresis_true.py` (+json) — hysteresis จริง
- `audit_v8_full_battery.py` (+json) — ชุดทดสอบเต็ม
- `test_v3_symmetric_gate.py` — delta precision (ผ่าน 4.7e-13)

## 5.5 พิสูจน์กลไก: normalize feedback = X ทรงตัวแบบ v7 (v6)

ทดสอบว่า "R_causal พุ่ง" เป็นสมบัติของ graph model หรือ artifact ของการไม่ normalize
→ สร้าง v6 ที่ normalize inbound ใน feedback (`w_hat = inbound/||inbound||` เหมือน v7 normalize v̂)

| g_yx | v5 R (ดิบ) | v5 flow | v6 R (normalize) | v6 flow |
|---|---|---|---|---|
| 0.8 | 0.439 | −0.22 | 0.472 | +1.99 |
| 1.2 | 0.436 | −1.25 | 0.471 | +2.22 |
| 3.0 | 0.573 | −7.09 | 0.470 | +1.64 |
| 5.0 | 0.821 | −37.3 | **0.443** | +2.13 |

**ผล:** normalize แก้ runaway ได้สมบูรณ์
1. R_causal ทรงตัว (0.44–0.47) แทนที่จะพุ่ง 0.82 — ตรงกับ v7 ที่ X ratio ทรงตัว
2. obs_flow ไม่กลายเป็น sink (−37 → +2 ทรงตัว) — กลไก "observer กลายหลุมดำ" ถูกฆ่า
3. extent ยังเติบโตแต่ช้ากว่ามาก (16.4 vs 76.9 ที่ g_yx=5) — bistability ยังอยู่ ไม่ runaway

**บทสรุปเชิงโครงสร้าง:** "R_causal พุ่ง" ไม่ใช่สมบัติของ graph model แต่เป็น **artifact ของ
feedback ที่ไม่ normalize** — พอ normalize แล้ว v8-R แสดง "X ทนทาน ทรงตัว" เหมือน v7 เป๊ะ

**หลักการเชื่อมสองโมเดล:** "observer ส่งแค่ทิศ ไม่ใช่แรง (normalize)" เป็นเงื่อนไขจำเป็น
สำหรับ emergent time ที่เสถียร ทั้งใน matrix (v7) และ graph (v8-R)

## 6. Scaling test — N ถึง 384 + cost จริงคือ O(N³) ไม่ใช่ O(E) (2026-08-30)

Timing 1 run (n_therm=240, d=3, g_yx=0.8):

| N | เวลา (s) | R_causal | obs_extent |
|---|---|---|---|
| 96 | 4.91 | 0.495 | 0.088 |
| 192 | 32.5 | 0.493 | 0.018 |
| 384 | 257.3 | 0.496 | 0.006 |

**ข้อค้นพบ 2 ข้อ:**

1. **R_causal ทรงตัว ~0.49 ถึง N=384** — ลูกศรเวลา emergent ได้เสถียรที่ N ที่ v7 เข้าไม่ถึง
2. **cost จริงเป็น O(N³) ไม่ใช่ O(E) ตาม plan** — N ×4 → เวลา 52× (O(N²·⁷)) เพราะโค้ดใช้
   dense W (N×N) ไม่ใช่ sparse: transitivity delta เป็น O(N) ต่อ edge × N² edges = O(N³)/sweep
   → plan เคลม O(E)≈O(N log N) แต่ implementation ยังไม่ถึง (ต้อง sparse)

## 7. ข้อควรระวัง (ซื่อตรง)

1. **R_causal เพิ่มตาม g_yx (0.47→0.83)** — ต่างจาก v7 ที่ X ratio ทรงตัว นี่เป็นพฤติกรรม
   ใหม่ของ graph model ที่ยังไม่เข้าใจกลไกเต็มที่ (ต้องขุดต่อถ้าจะ claim)
2. **thermalization n_therm=240 เป็นค่าจาก N=24** — N ใหญ่ขึ้นอาจต้องเพิ่มอีก ยังไม่ scan
3. **critical g_yx ยังเป็น n=5 seed** (fresh init) — สัดส่วนมี uncertainty
4. extent gate (16) เป็นค่าที่เลือกจากสมดุลที่ g_yx=1.2 ไม่ใช่ derive — ถ้าเปลี่ยน model ต้อง re-tune
5. **O(N³) ไม่ใช่ O(E)** — ถ้าต้องการ N=10³–10⁵ ตาม plan ต้องเขียน sparse adjacency (ไม่ใช่ dense W)

## 8. Sparse Engine (v7) — ถูกต้อง + 13× speedup (2026-08-30)

แก้ bottleneck O(N³) ใน §6 ด้วย sparse CSR representation ใน `sgoed_graph_core_v7.py`

### 8.1 บทเรียนจากความผิดพลาด 3 ครั้ง (สำคัญ)
1. **degree = ผลรวมน้ำหนักทั้งหมด ไม่มี threshold** — ตรงกับ v3-v6; threshold ใช้เฉพาะ
   ตอนสแกน active edges ไม่ใช่ตอนคำนวณ degree
2. **W2 = W@W ต้องคำนวณจาก W ทั้งหมด** (ไม่ตัด threshold) เพราะ transitivity ใช้ทุกคู่ (i,k)
3. **correctness-first**: validate delta → W2 incremental → in-CSR ทีละขั้น ไม่เขียนรวดเดียว

### 8.2 ผลลัพธ์ (ทุกขั้น validate ผ่าน)
| ขั้น | ผล |
|---|---|
| CSR + weighted degree | ตรง dense 4e-16 |
| W2 incremental update | ตรง rebuild 2e-16 |
| delta ทุกเทอม | ตรง full action 3e-14 |
| reproduce v6 (w_min=0) | เป๊ะ (R, extent ตรงทุกหลัก) |
| in-CSR transitivity O(k) | ผ่าน |

### 8.3 Speedup (v6 dense vs v7 sparse, n_therm=240)
| N | v6 (s) | v7 (s) | speedup |
|---|---|---|---|
| 48 | 0.77 | 0.11 | 7.1× |
| 96 | 4.90 | 0.52 | 9.4× |
| 192 | 32.8 | 2.93 | 11.2× |
| 384 | 265 | 20.3 | **13.1×** |

speedup เพิ่มขึ้นตาม N (7→13×) = v7 scale ดีกว่า v6 จริง

### 8.4 ที่ยังไม่ถึง O(E) เต็ม (bottleneck ที่เหลือ)
1. **`build_csr` + `build_csr_transpose` O(N²)/sweep** — วนทุก (i,j) เพื่อ rebuild active-edge
   list ทุก sweep → bottleneck ใหม่ที่ใหญ่สุด (ต้องทำ CSR incremental rebuild)
2. `coup_fb_ext` O(d·N)/delta (d เล็ก แต่ N ใหญ่)
3. `while i < N` หา row ของ CSR entry — O(N)/edge (ควร binary search บน row_ptr)

→ ได้ sparse ที่**ถูกต้องสมบูรณ์** + เร็ว 13× แต่ O(E) เต็มต้องกำจัด build_csr O(N²)/sweep ก่อน

## 9. Tuned Sparse Engine (v8) — running-sum + 31× speedup (2026-08-30)

### 9.1 profile จริง (N=384, ต่อ sweep ~73 ms)
- `build_csr`+transpose = 24.8 ms (~34%) — **ไม่ใช่ bottleneck หลัก** ตามที่รีวิวภายนอกเคลม
- delta loop = 66% (ส่วนใหญ่คือ `coup_fb_ext` O(d·N)×2/edge + `while i<N` O(N)/edge)

### 9.2 สิ่งที่ปรับ (2 จุด จากหลักฐานไม่ใช่เดา)
1. **cfe_from_state O(d²)** — เก็บ running sum `rest_sq[a]=Σ_{q≥d}W[a,q]²`, `inbound[a]=Σ_{q≥d}W[q,a]`
   อัปเดต O(1) เมื่อ edge แตะ observer (i<d หรือ j<d) แทน recompute O(d·N) ทุก delta
2. **rows[E] precompute** — O(1) edge→row lookup แทน `while i<N`

### 9.3 Speedup (v6/v7/v8, n_therm=240, 1 run)
| N | v6 (s) | v7 (s) | v8 (s) | v8/v6 | v8/v7 |
|---|---|---|---|---|---|
| 96 | 5.68 | 0.64 | 0.34 | 16.8× | 1.9× |
| 192 | 37.0 | 3.43 | 1.41 | 26.2× | 2.4× |
| 384 | 284 | 21.8 | 9.06 | **31.4×** | 2.4× |

### 9.4 ความถูกต้อง (แยก 2 ระดับ)
| เงื่อนไข | ผล |
|---|---|
| v8 (w_min=0) vs v6 | ✅ **เหมือนกันเป๊ะ** (R, extent ตรง 1e-9) — v8 = model เดียวกับ v6 |
| v8 (w_min=0.05) vs v7 | ✅ เหมือนกันเป๊ะ — optimizer ที่ถูกต้อง ไม่เปลี่ยนผล |
| v6 vs v8 (w_min=0.05) | ⚠️ R ต่าง ~0.02–0.12 — **เพราะ threshold ขนาดนั้น** ไม่ใช่ bug ของ v8 |

Validate: cfe_from_state ตรง reference 5.5e-17, delta ตรง full action 1.06e-13

**Verdict:** ถ้าต้องการผลตรง v6 เป๊ะ → w_min=0 (v8 ยังเร็วกว่า v6 เพราะ running-sum);
w_min>0 ได้ speedup สูงแต่ R เปลี่ยนตาม threshold ต้องเลือกโดยรู้ตัว

## 10. R_causal / R_obs / obs_flow — artifact + ตัวเลขไม่ reproduce (2026-08-31)

สคริปต์ตรวจ: `check_r_causal_graph_baseline.py`, `check_v8_obs_block.py`

### 10.1 R_causal ทั้ง graph = histogram artifact
| การทดสอบ (N=16, seed 42) | R_causal |
|---|---|
| จริง (thermalize) | 0.797 |
| shuffle ค่า W ทั้งหมด (ทำลายทุกโครงสร้าง) | **0.863** (สูงกว่า!) |
| mirror-swap (สลับทิศแต่ละคู่) | 0.797 (ไม่เปลี่ยน — direction-blind โดยคณิตศาสตร์) |

### 10.2 R_obs / D_obs / obs_flow ใน observer block (N=24, d=3, 3 seeds)
shuffle ค่าภายใน obs block → R_obs, D_obs, obs_flow **เท่าเดิมเป๊ะทุกกรณี**
(เช่น g_yx=3.0: R_obs=0.998 → shuffle 0.998; D_obs=−3 → shuffle −3.0; obs_flow คงที่)
→ ค่า "R_obs → 1.0" ใน section 4.5 **ไม่ได้บ่งชี้ทิศทาง** — block มีค่าศูนย์ครึ่งหนึ่ง
(โครงสร้าง sparse) → |a−0|/(a+0)=1 โดยธรรมชาติ

### 10.3 obs_flow = −37.3 (section 4.5) ไม่ reproduce
rerun N=24, d=3, g_xy=0.8, g_yx=5.0, n_therm=240, 3 seeds (42/43/44):
obs_flow = +2.01, +1.57, +1.50 — **บวกทั้งหมด ไม่ใช่ −37.3**
→ ต้อง re-verify (config เดิมของ 4.5 ไม่ระบุครบ) ก่อนใช้ตัวเลขนี้

### 10.4 verdict
- ❌ R_causal / R_obs / "R เพิ่มตาม g_yx" — ไม่ใช่หลักฐานลูกศรเวลา (histogram artifact)
- ❌ obs_flow = −37.3 — ไม่ reproduce ในการ rerun default config
- ✅ **ที่ยังยืนใน v8:** hysteresis / first-order (anneal-carry — พลวัตจริง),
  obs_extent และ critical g_yx (d/N-dependence — ขนาดของพลวัต ไม่ใช่ทิศทาง),
  scaling + speedup ของ engine (engineering: O(N³)→O(E), 13×/31×)
- หลักฐานทิศทางเวลาของ graph model: **ยังไม่มี** — D = Σ sign(W_ik − W_ki) ≈ 0 ± 20
  (ดู `SGOED_v9_hypergraph_notes.md` §6.2)
