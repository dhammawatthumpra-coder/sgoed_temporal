# SGOED V5 — สรุปภาพรวมโครงการและการตรวจสอบความซื่อตรง (2026-08-31)

เอกสารนี้สรุปผลทั้งหมดของงาน SGOED V5 (v6–v14) หลังการตรวจสอบเชิงลึก —
สิ่งที่ยืนจริง / สิ่งที่พัง / บทเรียนระเบียบวิธี — สำหรับการตัดสินใจตีพิมพ์และงานต่อ

---

## 1. โครงสร้างโมเดลที่พัฒนา

| Version | สถาปัตยกรรม | จุดประสงค์ |
|---|---|---|
| v6 | Matrix (trajectory-mean, delta sampler) | แก้ step=2 bug ของ v5 — ผล robust |
| v7 | Matrix + back-reaction (X→Y) | Bistability, hysteresis, condensation |
| v8 | Graph (relational) | ทดสอบ relational ครั้งแรก |
| v9/v10 | Hypergraph 3-uniform | Causal set / มิติกาลอวกาศ |
| v11 | Ecosystem (M universes) | Time synchronization |
| v12 | Graph + SVD condensation | Rank-1 condensation / "arrow" |
| v13 | Graph + asymmetric coupling | Emergence แบบไม่ engineered |
| v14 | Matrix-units hybrid (atom-molecule) | "เวลารวม" จากทิศของ matrix units |

---

## 2. บทสรุปแต่ละ branch (หลังตรวจสอบ)

### Matrix Model (v6/v7) — ✅ สิ่งเดียวที่ยืนจริง
- **Eigenvalue condensation ratio** discriminate จริง: g_XY=0.8 → ratio 4.55±0.35
  vs baseline 1.10±0.05 (**~60σ**), λmax/λ2nd = **23.2** (rank-1)
- Bistability + hysteresis (first-order, memory) — พลวัตจริง (anneal-carry ยืนยัน)
- กลไก: coupling `−g·v̂²·Tr(X⁴)` + gate → winner-takes-all เลือก μ จาก D —
  **"ตัวเลือก discrete"** คือเหตุผลที่ทิศทางมีอยู่จริง (graph ไม่มีตัวเลือกแบบนี้)
- ⚠️ แต่เป็นกลไกที่ใส่ใน action (engineered) — ยังไม่ใช่ "emergence" ตามนัย

### Relational (graph v8–13, hypergraph v9–10, ecosystem v11) — ❌ ไม่มีหลักฐาน "arrow of time"
| ตัววัด | ผลตรวจ |
|---|---|
| R_hyper / R_causal ≈ 0.5 | **histogram artifact** (shuffle ค่าแล้วสูงกว่า real; mirror-swap ไม่เปลี่ยน) |
| D (sign count) | **labeling-dependent** (permute node → D ∈ [−98, +28]) |
| d_MM (threshold + continuous) | **null-compatible** (random ก็ให้ค่าเดียวกัน) |
| d_s (heat kernel) | null-compatible (symmetrized graph = complete → วัดแค่ความหนาแน่น) |
| cycle ratio (feed-forward) | ≈ 0.5 = random — ไม่มี feed-forward structure |
| time-reversal (reversed-start) | ไม่ดึงกลับทิศ (corr ตาม initial) — สมมาตร |
| G / D_root (invariant) | hub structure จริง (sink-hub v12) แต่ไม่ใช่ global arrow |
| alignment | เงื่อนไขอ่อน (baseline ก็ 80–100%) |

### v12/v13 (graph ใหม่)
- **v12**: condensation (σ₁/σ₂ 7.3→12.8, 27–95σ) + sink-hub (G/D_root invariant)
  — แต่ engineered (λ_c ≈ 0.02, ตัด λ = ไม่มี), D labeling-dependent, spec ยังไม่ plateau
- **v13** (coupling-only): significance ตกเมื่อเพิ่ม seeds (2.3σ→1.2σ), D ยัง labeling-dependent

### v14 (matrix-units hybrid — แนวคิด "อะตอม-โมเลกุล")
- ✅ **v̂ sync = 1.000 ± 0.001** (ผ่าน null test — "clock synchronization" จาก
  inter-coupling — ครั้งแรกใน relational ที่ผลทำงาน)
- ❌ order (ก่อน-หลัง) ไม่เกิด — ทุกทาง (E, trade-off, repulsion, dynamic order,
  slow-align) ถูกปิดด้วย **homogenization** (coupling ที่ align = ทำให้เหมือนกัน =
  ตรงข้ามกับเวลาที่แยกขั้น)
- entropy production: universal (dS/S_init ≈ 8 คงที่) — coupling แค่เร่งอัตรา (half-life 17→4.3)

---

## 3. บทเรียนระเบียบวิธี (มีค่าที่สุดของโครงการ)

ทุก observable ใหม่ต้องผ่าน 6 ขั้น (มิฉะนั้นตกเป็น artifact):
1. **Reproduce** — รันซ้ำได้เลขเดิม
2. **Significance** — เพิ่ม seeds จน std เสถียร (5 seeds มักไม่พอ — v13: 2.3σ→1.2σ)
3. **Null test** — เทียบ random/shuffle/baseline (R, d_MM, d_s ต่างพังตรงนี้)
4. **Labeling/permutation test** — metric ต้อง invariant ต่อการเรียง node (D พังตรงนี้)
5. **Thermalization check** — n_therm ต้องพอ (v7: 20→40; graph: 240; λ_c: 40→120)
6. **Mechanism** — อธิบายได้ว่าทำไม (sink-hub = rank-1 → u₁≈0 → sink)

**ผลลัพธ์: metric 11 ตัวที่ "ดูน่าตื่นเต้น" (R≈0.5, 4D, d_s, D~N², sink-hub, 3σ arrow,
order ทุกแบบ) พังหมดเมื่อเจอการตรวจ** — กระบวนการนี้คือสิ่งที่กันไม่ให้ตีพิมพ์ข้อสรุปผิด

---

## 4. สิ่งที่ยืนจริง (ใช้รายงานได้)

1. **Matrix v7 condensation** — rank-1 eigenvalue condensation (λmax/λ2nd=23, ~60σ
   จาก baseline) + bistability/hysteresis — กลไก discrete choice (μ จาก D)
2. **v14 simultaneity** — v̂ sync 1.000±0.001 (ผ่าน null test) = "clock
   synchronization" จาก inter-coupling ของ matrix units
3. **Thermodynamic arrow** — universal (ทุก stochastic system — random→equilibrium)
4. **Engineering achievements** — v8/v10/v12 speedups (O(N³)→O(E), 13–43×)

## 5. สิ่งที่ไม่ยืน (อย่านำไปอ้าง)

- "4D emergence", "dimensional collapse", "d_s≈2.4", "fractal 2.42D"
- "ลูกศรเวลา R≈0.5" (graph/hypergraph/ecosystem)
- "Macroscopic Arrow D~N²" (v12 — labeling-dependent)
- "True Emergence 3σ" (v13 — 5-seed ปรากฏการณ์)
- "order/ก่อน-หลัง" ทุกรูปแบบ (v14 — homogenize)

---

## 6. คำแนะนำสำหรับงานต่อ

- **ตีพิมพ์ได้ (ระวังภาษา):** matrix v7 condensation + bistability (กลไก discrete
  choice) — ระบุชัดว่า engineered + toy model
- **Relational branch:** ใช้ได้เป็น "negative result" (metric ที่พัง + บทเรียน
  null/labeling test) — มีคุณค่าทางระเบียบวิธี
- **ถ้าจะ "หาเวลา" ต่อ:** ต้องเปลี่ยน paradigm — ตัวแปรเวลาต้องเป็นปริมาณที่
  "เพิ่มตามเวลา" (entropy-like) และ coupling ต้อง "แยก" (push) ไม่ใช่ "รวม" (pull)
  — alignment coupling ให้ได้แค่ simultaneity

---

*แหล่งอ้างอิงรายละเอียด: `SGOED_v7_feedback_notes.md`, `SGOED_v8_relational_notes.md`,
`SGOED_v9_hypergraph_notes.md`, `SGOED_v10_ecosystem_notes.md`, `SGOED_v12_graph_notes.md`,
`SGOED_v12_summary.md`, `SGOED_v13_asymmetric_notes.md`, `SGOED_v14_notes.md`,
`manuscript_v6.tex` (ทั้งหมดใน `` และ `matrix/`)*
