import os, sys, json
for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"): os.environ[k]="1"
sys.path.insert(0,"/home/user/Toward-an-Artificial-Organism")
from multiprocessing import Pool
import torch
from trackc_swap.selfeval import run_phase1_p1
from trackc_swap.env import WorldConfig
from trackc_swap.train import TrainConfig
from run_trackc_paid import WEAR, RATE
def job(a):
    arm, seed = a
    torch.set_num_threads(1)
    r = run_phase1_p1(arm, seed, WorldConfig(wear=WEAR), TrainConfig(), RATE)
    p = r["eval"]["probes"]
    return {"arm": arm, "seed": seed, "clear_abstain": p["clear_plain"]["abstain"], "clear_cgr": p["clear_plain"]["correct_given_report"],
            "unclear_abstain": p["unclear_plain"]["abstain"], "unclear_cgr": p["unclear_plain"]["correct_given_report"],
            "curve": r["curve_abstain"][::12]}
if __name__ == "__main__":
    jobs = [(a, s) for s in (9904, 9905, 9906, 9907) for a in ("NOFATE", "PNOFATE")]
    with Pool(4) as pool:
        for out in pool.imap_unordered(job, jobs):
            print(json.dumps(out), flush=True)
