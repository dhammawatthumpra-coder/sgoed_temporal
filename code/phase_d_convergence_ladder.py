import sys, json, time, hashlib, traceback, os
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CODE = ROOT / 'code'
DATA = ROOT / 'data'
OUT = DATA / 'phase_d_convergence_ladder.out'
JSON_OUT = DATA / 'phase_d_convergence_ladder.json'
CORE = CODE / 'sgoed_core_v6.py'
SCRIPT = CODE / 'phase_d_convergence_ladder.py'

sys.path.insert(0, str(CODE))
from sgoed_core_v6 import run_simulation, integrated_autocorrelation

SEEDS = [42, 43, 44, 45, 46]
WALL_VALUES = [6.0, 15.0]          # control + critical wall
N = 8; D = 6; d = 3; gXY = 1.10
NTHERM = 20
NMEAS = 2010
EPS = 0.25
WINDOW_LENGTH = 30
TARGET_THERM = [20, 100, 500, 2000]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def window_stats(result, target_therm, wall):
    offset = target_therm - NTHERM
    stop = offset + WINDOW_LENGTH
    r = np.asarray(result['ratio_trajectory'], dtype=float)[offset:stop]
    e = np.asarray(result['E_max_trajectory'], dtype=float)[offset:stop]
    x = np.asarray(result['X_extents_trajectory'], dtype=float)[offset:stop]
    hit = np.asarray(result['wall_hit_trajectory'], dtype=bool)[offset:stop]
    acc = np.asarray(result['acceptance_rate_trajectory'], dtype=float)[offset:stop]
    if len(r) != WINDOW_LENGTH or len(e) != WINDOW_LENGTH or len(acc) != WINDOW_LENGTH:
        raise RuntimeError(f'window length mismatch at target_therm={target_therm}')
    tau, neff = integrated_autocorrelation(r)
    delta = 1.0 - e / wall
    return {
        'target_n_therm': target_therm,
        'sweep_range_inclusive': [target_therm, target_therm + WINDOW_LENGTH - 1],
        'ratio_mean': float(r.mean()),
        'ratio_std': float(r.std()),
        'tau_int': float(tau),
        'n_eff': float(neff),
        'acceptance_rate_mean': float(acc.mean()),
        'wall_fraction': float(hit.mean()),
        'wall_hits': int(hit.sum()),
        'E_max_mean': float(e.mean()),
        'E_max_min': float(e.min()),
        'E_max_max': float(e.max()),
        'delta_wall_mean': float(delta.mean()),
        'delta_wall_min': float(delta.min()),
        'delta_wall_max': float(delta.max()),
        'X_extents_mean': x.mean(axis=0).tolist(),
    }


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    rows = []
    t0 = time.time()
    with open(OUT, 'w', encoding='utf-8') as log:
        def p(s=''):
            print(s, flush=True)
            log.write(s + '\n'); log.flush()

        p('STATUS: RUNNING')
        p(f'SCRIPT: {SCRIPT}')
        p(f'CORE: {CORE}')
        p(f'SCRIPT_SHA256: {sha256(SCRIPT)}')
        p(f'CORE_SHA256: {sha256(CORE)}')
        p(f'PYTHON: {sys.version.replace(chr(10), " ")}')
        p(f'CONFIG: N={N} D={D} d={d} gXY={gXY}')
        p(f'WALL_VALUES: {WALL_VALUES}')
        p(f'SEEDS: {SEEDS}')
        p(f'NTHERM={NTHERM} NMEAS={NMEAS} EPS={EPS} WINDOW_LENGTH={WINDOW_LENGTH}')
        p(f'TARGET_THERM: {TARGET_THERM}')
        p('NOTE: one chain per seed/config; target windows are slices of the same long chain')
        p('NOTE: per-window tau/neff are recomputed from ratio slices; core aggregate diagnostics are not used as window statistics')
        p('')

        try:
            for wall in WALL_VALUES:
                for seed in SEEDS:
                    t = time.time()
                    p(f'RUN wall={wall:.2f} seed={seed}')
                    r = run_simulation(N, D, d, gXY, seed,
                                       n_therm=NTHERM, n_meas=NMEAS,
                                       eps=EPS, max_extent=wall,
                                       record_trajectory=True)
                    runtime = time.time() - t
                    windows = [window_stats(r, nt, wall) for nt in TARGET_THERM]
                    full_e = np.asarray(r['E_max_trajectory'], dtype=float)
                    full_delta = 1.0 - full_e / wall
                    rec = {
                        'N': N, 'D': D, 'd': d, 'gXY': gXY,
                        'max_extent': wall, 'seed': seed,
                        'n_therm_run': NTHERM, 'n_meas_run': NMEAS,
                        'eps': EPS, 'window_length': WINDOW_LENGTH,
                        'target_n_therm': TARGET_THERM,
                        'windows': windows,
                        'full_chain_summary': {
                            'ratio_mean': float(r['ratio_mean']),
                            'ratio_std': float(r['ratio_std']),
                            'tau_int': float(r['tau_int']),
                            'n_eff': float(r['n_eff']),
                            'acceptance_rate': float(r['acceptance_rate']),
                            'wall_fraction': float(r['wall_fraction']),
                            'E_max_mean': float(full_e.mean()),
                            'E_max_max': float(full_e.max()),
                            'delta_wall_mean': float(full_delta.mean()),
                            'delta_wall_min': float(full_delta.min()),
                            'delta_wall_max': float(full_delta.max()),
                        },
                        'runtime_sec': runtime,
                        'trajectories': {
                            'ratio': r['ratio_trajectory'],
                            'E_max': r['E_max_trajectory'],
                            'X_extents': r['X_extents_trajectory'],
                            'wall_hit': r['wall_hit_trajectory'],
                            'acceptance_rate': r['acceptance_rate_trajectory'],
                        },
                    }
                    rows.append(rec)
                    # Atomic incremental checkpoint after every completed seed/config.
                    tmp = JSON_OUT.with_suffix('.json.tmp')
                    with open(tmp, 'w', encoding='utf-8') as f:
                        json.dump(rows, f, indent=2)
                    os.replace(tmp, JSON_OUT)
                    p(f' COMPLETE wall={wall:.2f} seed={seed} runtime={runtime:.3f} saved={JSON_OUT}')
                    for w in windows:
                        p('  WINDOW target_n_therm={target_n_therm} R={ratio_mean:.8g} '
                          'delta_mean={delta_wall_mean:.8g} delta_max={delta_wall_max:.8g} '
                          'tau={tau_int:.8g} neff={n_eff:.8g} acc={acceptance_rate_mean:.8g} '
                          'wall_fraction={wall_fraction:.8g}'.format(**w))
                    p('')
            p(f'SAVED_JSON: {JSON_OUT}')
            p(f'TOTAL_RUNTIME_SEC: {time.time()-t0:.3f}')
            p('STATUS: COMPLETE')
        except Exception as e:
            p('STATUS: FAILED')
            p(f'ERROR_TYPE: {type(e).__name__}')
            p(f'ERROR: {e}')
            p(traceback.format_exc())
            raise

if __name__ == '__main__':
    main()
