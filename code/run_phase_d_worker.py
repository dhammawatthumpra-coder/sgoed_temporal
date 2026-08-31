import sys
import json
import time
import hashlib
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(r"F:\_Ai\sgoed\V5")
CODE = ROOT / "code"
DATA = ROOT / "data"
OUT = DATA / "phase_d_worker.out"
JSON_OUT = DATA / "phase_d_worker.json"
CORE = CODE / "sgoed_core_v6.py"
SCRIPT = CODE / "run_phase_d_worker.py"

sys.path.insert(0, str(CODE))
from sgoed_core_v6 import run_simulation

SEEDS = [42, 43, 44, 45, 46]
CONFIGS = [{"N": 8, "d": 3, "gXY": 1.10}]
WALL_VALUES = [6.0, 8.0, 10.0, 12.0, 15.0]
NTHERM = 20
NMEAS = 30
EPS = 0.25
D = 6


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    rows = []
    start_all = time.time()
    with open(OUT, "w", encoding="utf-8") as log:
        def p(msg=""):
            print(msg)
            log.write(msg + "\n")
            log.flush()

        p("STATUS: RUNNING")
        p(f"SCRIPT: {SCRIPT}")
        p(f"CORE: {CORE}")
        p(f"SCRIPT_SHA256: {sha256(SCRIPT)}")
        p(f"CORE_SHA256: {sha256(CORE)}")
        p(f"PYTHON: {sys.version.replace(chr(10), ' ')}")
        p(f"CONFIGS: {json.dumps(CONFIGS)}")
        p(f"WALL_VALUES: {WALL_VALUES}")
        p(f"SEEDS: {SEEDS}")
        p(f"NTHERM={NTHERM} NMEAS={NMEAS} EPS={EPS} D={D}")
        p("")
        try:
            for cfg in CONFIGS:
                for wall in WALL_VALUES:
                    p(f"CASE N={cfg['N']} d={cfg['d']} gXY={cfg['gXY']:.2f} max_extent={wall:.1f}")
                    for seed in SEEDS:
                        t0 = time.time()
                        r = run_simulation(cfg["N"], D, cfg["d"], cfg["gXY"], seed,
                                           n_therm=NTHERM, n_meas=NMEAS, eps=EPS,
                                           max_extent=wall, record_trajectory=True)
                        elapsed = time.time() - t0
                        rec = {"N": cfg["N"], "d": cfg["d"], "gXY": cfg["gXY"],
                               "max_extent": wall, "seed": seed, "result": r,
                               "runtime_sec": elapsed}
                        rows.append(rec)
                        p((" seed={seed} R={R:.8g} Rsd={Rsd:.8g} tau={tau:.8g} "
                           "neff={neff:.8g} acc={acc:.8g} Emax={emax:.8g} "
                           "wall_fraction={wf:.8g} wall_hits={wh}/{nm} runtime={rt:.3f}").format(
                            seed=seed,
                            R=float(r.get("ratio_mean", np.nan)),
                            Rsd=float(r.get("ratio_std", np.nan)),
                            tau=float(r.get("tau_int", np.nan)),
                            neff=float(r.get("n_eff", np.nan)),
                            acc=float(r.get("acceptance_rate", np.nan)),
                            emax=float(np.max(r.get("E_max_trajectory", [np.nan]))),
                            wf=float(r.get("wall_fraction", np.nan)),
                            wh=int(np.sum(r.get("wall_hit_trajectory", []))),
                            nm=int(len(r.get("wall_hit_trajectory", []))),
                            rt=elapsed))
                    vals = [float(x["result"].get("ratio_mean", np.nan)) for x in rows
                            if x["max_extent"] == wall]
                    wfs = [float(x["result"].get("wall_fraction", np.nan)) for x in rows
                           if x["max_extent"] == wall]
                    emaxs = [float(np.max(x["result"].get("E_max_trajectory", [np.nan]))) for x in rows
                             if x["max_extent"] == wall]
                    p(f" SEED_SUMMARY mean={np.mean(vals):.8g} sd={np.std(vals, ddof=1):.8g} "
                      f"wall_fraction_mean={np.mean(wfs):.8g} Emax_trajectory_max={np.max(emaxs):.8g}")
                    p("")
            with open(JSON_OUT, "w", encoding="utf-8") as jf:
                json.dump(rows, jf, indent=2, default=lambda x: float(x) if isinstance(x, np.floating) else x)
            p(f"SAVED_JSON: {JSON_OUT}")
            p(f"TOTAL_RUNTIME_SEC: {time.time() - start_all:.3f}")
            p("STATUS: COMPLETE")
        except Exception as exc:
            p("STATUS: FAILED")
            p(f"ERROR_TYPE: {type(exc).__name__}")
            p(f"ERROR: {exc}")
            p("TRACEBACK:")
            for line in traceback.format_exc().splitlines(): p(line)
            raise

if __name__ == "__main__":
    main()
