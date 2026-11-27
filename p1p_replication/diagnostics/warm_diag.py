"""Diagnostic (not a study): how fast does the CIFG learn the phase-1 memory at wrong cost 0? Non-study seeds."""
import sys, json, numpy as np, torch
sys.path.insert(0, "/home/user/Toward-an-Artificial-Organism")
from multiprocessing import Pool
from trackc_swap import archswap
archswap.install()
from trackc_swap import selfmon
from trackc_swap.env import WorldConfig
from trackc_swap.train import TrainConfig
from run_trackc_paid import PAY, WEAR

def job(a):
    seed, fb, iters = a
    torch.set_num_threads(1)
    wc, tc = WorldConfig(wear=WEAR), TrainConfig()
    r = selfmon.MonRunner("C1NOFATE", seed, wc, tc, pay=PAY[1])
    if fb is not None:
        if fb == "gru":
            pass
        else:
            with torch.no_grad():
                r.agent.core.x2g.bias[:archswap.N_CELL].fill_(fb)
    r.world.wrong = 0.0
    zeros = np.zeros((tc.rollout, tc.n_envs), dtype=np.float32)
    curve = []
    for i in range(iters):
        r.rollout(zeros, learn=True)
        st = r.end_episode_if_due()
        if st is not None:
            curve.append(round(st["correct_rate"], 3))
    return {"seed": seed, "fb": fb, "curve": curve}

if __name__ == "__main__":
    jobs = [(3900, 1.0, 3600), (3901, 1.0, 3600), (3900, 0.0, 3600), (3901, 0.0, 3600)]
    with Pool(4) as p:
        for res in p.imap_unordered(job, jobs):
            print(json.dumps(res), flush=True)
