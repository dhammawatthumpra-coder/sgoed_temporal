import sys, json, time
import numpy as np
sys.path.insert(0, r'F:\_Ai\sgoed\V5\code')
from sgoed_core_v6 import run_simulation

seeds=[42,43,44,45,46]
configs=[
    {'N':7,'d':3,'gXY':0.8},
    {'N':8,'d':3,'gXY':0.8},
    {'N':8,'d':3,'gXY':1.10},
]
wall_values=[6.0,8.0,10.0,12.0,15.0]
all_results=[]
for cfg in configs:
    for wall in wall_values:
        print(f"\nN={cfg['N']} d={cfg['d']} g={cfg['gXY']:.2f} max_extent={wall:.1f}")
        rows=[]
        for seed in seeds:
            t=time.time()
            r=run_simulation(cfg['N'],6,cfg['d'],cfg['gXY'],seed,n_therm=20,n_meas=30,eps=0.25,max_extent=wall,record_trajectory=True)
            # Reconstruct late-trajectory diagnostics available from X_extents only if returned;
            # v6 currently does not return X_extents trajectory, so use result fields now.
            rows.append(r)
            print(f" seed={seed} R={r['ratio_mean']:.4f} sd={r['ratio_std']:.4f} tau={r['tau_int']:.3f} neff={r['n_eff']:.2f} acc={r['acceptance_rate']:.3f} ({time.time()-t:.2f}s)")
        mean=np.mean([x['ratio_mean'] for x in rows]); sd=np.std([x['ratio_mean'] for x in rows],ddof=1)
        all_results.append({'config':cfg,'max_extent':wall,'seed_results':rows,'seed_mean':float(mean),'seed_sd':float(sd)})

out=r'F:\_Ai\sgoed\V5\data\phase_d_wall_sensitivity.json'
with open(out,'w') as f: json.dump(all_results,f,indent=2)
print('\nSAVED',out)
