# Same provenance-logged worker as phase_d_g08_wall_probe.py, extended to locate the g=0.8 wall-crossover.
# No physics logic changes; only wall values are changed.
import sys,json,time,hashlib,traceback
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent; CODE=ROOT/'code'; DATA=ROOT/'data'
OUT=DATA/'phase_d_g08_wall_crossover.out'; JSON_OUT=DATA/'phase_d_g08_wall_crossover.json'
CORE=CODE/'sgoed_core_v6.py'; SCRIPT=CODE/'phase_d_g08_wall_crossover.py'
sys.path.insert(0,str(CODE)); from sgoed_core_v6 import run_simulation
SEEDS=[42,43,44,45,46]; WALL_VALUES=[3.0,3.5,4.0,4.5,5.0,5.5,6.0]
N=8;D=6;d=3;gXY=0.8;NTHERM=20;NMEAS=30;EPS=0.25
def sha256(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def main():
 rows=[]; DATA.mkdir(parents=True,exist_ok=True); t0=time.time()
 with open(OUT,'w',encoding='utf-8') as log:
  def p(s=''): print(s);log.write(s+'\n');log.flush()
  p('STATUS: RUNNING');p(f'SCRIPT: {SCRIPT}');p(f'CORE: {CORE}');p(f'SCRIPT_SHA256: {sha256(SCRIPT)}');p(f'CORE_SHA256: {sha256(CORE)}');p(f'PYTHON: {sys.version.replace(chr(10)," ")}');p(f'CONFIG: N={N} d={d} gXY={gXY}');p(f'WALL_VALUES: {WALL_VALUES}');p(f'SEEDS: {SEEDS}');p(f'NTHERM={NTHERM} NMEAS={NMEAS} EPS={EPS} D={D}');p('')
  try:
   for wall in WALL_VALUES:
    p(f'CASE max_extent={wall:.2f}'); rs=[];ds=[]
    for seed in SEEDS:
     t=time.time();r=run_simulation(N,D,d,gXY,seed,n_therm=NTHERM,n_meas=NMEAS,eps=EPS,max_extent=wall,record_trajectory=True);rt=time.time()-t
     e=np.asarray(r['E_max_trajectory'],float);hit=np.asarray(r['wall_hit_trajectory'],bool);emax=float(e.max());delta=1-emax/wall
     rs.append(float(r['ratio_mean']));ds.append(delta);rows.append({'N':N,'d':d,'gXY':gXY,'max_extent':wall,'seed':seed,'result':r,'delta_wall_max':delta,'runtime_sec':rt})
     p(f' seed={seed} R={r["ratio_mean"]:.8g} Emax={emax:.8g} delta_wall={delta:.8g} tau={r["tau_int"]:.8g} neff={r["n_eff"]:.8g} acc={r["acceptance_rate"]:.8g} wall_fraction={float(hit.mean()):.8g} runtime={rt:.3f}')
    p(f' SUMMARY R_mean={np.mean(rs):.8g} R_sd={np.std(rs,ddof=1):.8g} delta_wall_mean={np.mean(ds):.8g} delta_wall_max={np.max(ds):.8g}');p('')
   with open(JSON_OUT,'w',encoding='utf-8') as f:json.dump(rows,f,indent=2)
   p(f'SAVED_JSON: {JSON_OUT}');p(f'TOTAL_RUNTIME_SEC: {time.time()-t0:.3f}');p('STATUS: COMPLETE')
  except Exception as e:p('STATUS: FAILED');p(f'ERROR_TYPE: {type(e).__name__}');p(f'ERROR: {e}');p(traceback.format_exc());raise
if __name__=='__main__':main()
