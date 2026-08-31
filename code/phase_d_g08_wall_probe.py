import sys, json, time, hashlib, traceback
from pathlib import Path
import numpy as np
ROOT=Path(r"F:\_Ai\sgoed\sgoed"); CODE=ROOT/'code'; DATA=ROOT/'data'
OUT=DATA/'phase_d_g08_wall_probe.out'; JSON_OUT=DATA/'phase_d_g08_wall_probe.json'
CORE=CODE/'sgoed_core_v6.py'; SCRIPT=CODE/'phase_d_g08_wall_probe.py'
sys.path.insert(0,str(CODE)); from sgoed_core_v6 import run_simulation
SEEDS=[42,43,44,45,46]; WALL_VALUES=[1.5,1.75,2.0,2.25,2.5]
N=8; D=6; d=3; gXY=0.8; NTHERM=20; NMEAS=30; EPS=0.25

def sha256(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

def main():
 DATA.mkdir(parents=True,exist_ok=True); rows=[]; t_all=time.time()
 with open(OUT,'w',encoding='utf-8') as log:
  def p(s=''): print(s); log.write(s+'\n'); log.flush()
  p('STATUS: RUNNING'); p(f'SCRIPT: {SCRIPT}'); p(f'CORE: {CORE}')
  p(f'SCRIPT_SHA256: {sha256(SCRIPT)}'); p(f'CORE_SHA256: {sha256(CORE)}')
  p(f'PYTHON: {sys.version.replace(chr(10)," ")}'); p(f'CONFIG: N={N} d={d} gXY={gXY}')
  p(f'WALL_VALUES: {WALL_VALUES}'); p(f'SEEDS: {SEEDS}'); p(f'NTHERM={NTHERM} NMEAS={NMEAS} EPS={EPS} D={D}'); p('')
  try:
   for wall in WALL_VALUES:
    p(f'CASE N={N} d={d} gXY={gXY:.2f} max_extent={wall:.2f}'); vals=[]; deltas=[]; emaxs=[]
    for seed in SEEDS:
     t=time.time(); r=run_simulation(N,D,d,gXY,seed,n_therm=NTHERM,n_meas=NMEAS,eps=EPS,max_extent=wall,record_trajectory=True); rt=time.time()-t
     e=np.asarray(r.get('E_max_trajectory',[]),float); x=np.asarray(r.get('X_extents_trajectory',[]),float); hit=np.asarray(r.get('wall_hit_trajectory',[]),bool)
     emax=float(np.max(e)) if e.size else float('nan'); delta=1-emax/wall if wall else float('nan')
     vals.append(float(r['ratio_mean'])); deltas.append(delta); emaxs.append(emax)
     rec={'N':N,'d':d,'gXY':gXY,'max_extent':wall,'seed':seed,'result':r,'runtime_sec':rt,'delta_wall_max':delta}; rows.append(rec)
     p(f' seed={seed} R={r["ratio_mean"]:.8g} tau={r["tau_int"]:.8g} neff={r["n_eff"]:.8g} acc={r["acceptance_rate"]:.8g} Emax={emax:.8g} delta_wall={delta:.8g} wall_fraction={float(np.mean(hit)) if hit.size else float("nan"):.8g} wall_hits={int(np.sum(hit))}/{len(hit)} runtime={rt:.3f}')
    p(f' SUMMARY R_mean={np.mean(vals):.8g} R_sd={np.std(vals,ddof=1):.8g} delta_wall_mean={np.mean(deltas):.8g} delta_wall_max={np.max(deltas):.8g} Emax_max={np.max(emaxs):.8g}'); p('')
   with open(JSON_OUT,'w',encoding='utf-8') as f: json.dump(rows,f,indent=2)
   p(f'SAVED_JSON: {JSON_OUT}'); p(f'TOTAL_RUNTIME_SEC: {time.time()-t_all:.3f}'); p('STATUS: COMPLETE')
  except Exception as e:
   p('STATUS: FAILED'); p(f'ERROR_TYPE: {type(e).__name__}'); p(f'ERROR: {e}'); p(traceback.format_exc()); raise
if __name__=='__main__': main()
