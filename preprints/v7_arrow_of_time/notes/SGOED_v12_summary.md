# SGOED-Relational v12 — สรุปผลการตรวจสอบ (Data-Honest Summary)

วันที่: 2026-08-31 · แหล่งข้อมูล: `SGOED_v12_graph_notes.md` (§1–10) — ตัวเลขทุกค่า
ผ่านการ reproduce + significance + null/labeling test

---

## 1. โมเดล

- กราฟทิศทาง W (N×N, ค่าบวก), observer d nodes
- Action = sparsity + transitivity + gate +
  **quartic coupling** `−g_xy·Σ_a v̂_a·Σ_j W_aj⁴` +
  **global SVD condensation** `−λ_cond·Tr((WWᵀ)²) = −λ_cond·Σ_i σ_i⁴`
- Sampler: full-action recompute ทุก move (ถูกต้องโดย construction)

## 2. ข้อเท็จจริงที่ยืนยันแล้ว (ผ่านการตรวจทั้งหมด)

1. **Condensation (σ₁/σ₂):** 3.40 → 12.60 ตาม N = 8→48 (n_therm=40) —
   แยกจาก baseline 27–95σ — reproducible ตรงทุกค่า
2. **sink-hub:** node เดียว (argmax|out−in|) เป็น **sink** ดูด flow จาก 83–95% ของ node
   อื่น (D_root = −0.83 ถึง −0.96) — **invariant ต่อ labeling เป๊ะ** และ **ไม่ผูกกับ
   observer** (hub เป็น sys node 85–100%; ย้ายตำแหน่ง obs แล้ว hub ไม่ติดตาม)
3. **กลไก sink-hub (อธิบายครบ):** coupling ให้ source-hub (+24) แต่ global SVD สร้าง
   rank-1 mode (σ₁ = 218, σ₁/σ₂ ≈ 13) → node ที่ u₁ ≈ 0 ส่งออกไม่ได้ (W[i,:]≈0)
   แต่ยังรับได้ → กลายเป็น sink-hub โดยอัตโนมัติ
4. **G = Σ|out−in|/ΣW (global imbalance fraction):** invariant ต่อ labeling,
   discriminate: baseline ≈ 0.27 vs condensed ≈ 1.2–1.7 — ตัววัดทิศทางที่แนะนำใช้แทน D
5. **λ phase transition:** λ_c ≈ 0.02–0.05 (jump ฉับพลัน: spec 1.67→5.05);
   λ < 0.02 = baseline ล้วน; λ ≥ 0.3 = over-condensation พลิกทิศ (D_root → +0.78)

## 3. ข้อจำกัด (ต้องระบุเมื่อรายงาน)

- **Engineered:** ตัด λ_cond = ไม่มีทั้ง condensation และทิศทาง (λ→0 = baseline) —
  ไม่ใช่ emergence
- **D (sign-count) ใช้ไม่ได้:** labeling-dependent (permute sys → D ∈ [−98, +28]) —
  ใช้ G / D_root แทน
- **spec ยังไม่ plateau:** n_therm 960 (N=32) = 16.51 ยังไต่ — ตัวเลข σ₁/σ₂ ทั้งหมด
  เป็น **lower bound**; G/D_root ลู่เข้าแล้วที่ n_therm ≥ 240
- **D significance:** N=24 = 2.9σ (borderline), N=48 = 7.0σ, N=32 = 5.7σ
- **"sink-hub" ≠ arrow of time:** เป็น absorbing center (จุดดูดกลาง) ไม่ใช่ทิศทางเวลา
  ที่ขยายทั่วระบบตามนัย cosmology
- alignment = 100% ทุก mode รวม baseline (ไม่ discriminate — ใช้เป็นตัวรองเท่านั้น)

## 4. Verdict

v12 = graph model ที่มี **engineered condensation phase** (เปิดที่ λ_c) →
สร้างโครงสร้างทิศทางจริง (sink-hub) ที่ **invariant ต่อ labeling และ self-organized
(ไม่ผูกกับ observer)** — เป็นความก้าวหน้าจริงเหนือ v8 (v8: D ≈ 0 ไม่มีทิศทาง)
แต่ยังไม่ใช่ "emergence ของลูกศรเวลา" — เรียกได้ว่า "engineered rank-1 condensation
สร้าง sink-hub" อย่างตรงไปตรงมา

**ตัวเลขที่ใช้รายงานได้:** spec (ระบุ lower bound + n_therm), G, D_root, hub_imb

## 5. ไฟล์อ้างอิง

- `sgoed_graph_core_v12.py` (engine) · `audit_v12_full_battery.py` / `audit_v12_ablation.py`
- ตรวจซื่อตรง: `check_v12_baseline_significance.py`, `check_v12_invariant_metrics.py`,
  `check_v12_hub_observer.py`, `check_v12_sink_mechanism.py`, `step_lambda_scaling_G.py`,
  `step_therm_plateau.py`
