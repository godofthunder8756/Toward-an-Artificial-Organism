"""Descriptive (no training): how often does the body leave the band during a cue delay in stored
base-cell derived and paid agents, and what reliability would fate imply? Used for P1's power check."""
import sys, json
sys.path.insert(0, '.')
import numpy as np, torch
from dataclasses import asdict
from trackc_swap.env import WorldConfig, fate_gain
from trackc_swap.relocate import RelocAgent, RelocSwapWorld
from multiprocessing import Pool
RATE = 0.3
def run(args):
    seed, arm = args
    torch.set_num_threads(1)
    wc = WorldConfig(wear=0.001)
    sd = torch.load(f'trackc_length/weights/seed{seed}_{arm}_3600.pt', weights_only=True)
    world = RelocSwapWorld(128, "M1", wc, np.random.SeedSequence([seed, 77, 11]))
    torch.manual_seed(seed)
    agent = RelocAgent(64, RATE, 0.15); agent.load_state_dict(sd); agent.eval(); agent.__dict__['_world'] = world
    gen = torch.Generator().manual_seed(seed * 7919 + 77)
    rel, oob = [], []
    for ep in range(2):
        obs = world.reset(); h = agent.init_state(128)
        T = wc.horizon
        G = np.zeros((T, 128))
        for t in range(T):
            g = fate_gain(world.E, wc); G[t] = g
            with torch.no_grad():
                logits, _, h = agent.step(torch.from_numpy(obs), h, torch.from_numpy(g).float(), gen)
                a = torch.multinomial(torch.softmax(logits, -1), 1, generator=gen).squeeze(-1).numpy()
            obs, _, _ = world.step(a)
        for i in range(128):
            for tc in np.flatnonzero(world.cue_on[:T, i]):
                tp = tc + wc.cue_delay + 1
                if tp >= T: continue
                gg = G[tc:tp, i]
                rel.append(float(np.prod(1 - np.minimum(1, RATE * gg)))); oob.append(bool((gg > 0).any()))
    rel, oob = np.array(rel), np.array(oob)
    return {"seed": seed, "arm": arm, "n_probes": len(rel), "oob_share": float(oob.mean()), "rel_mean": float(rel.mean()),
            "rel_below_0.9": float((rel < 0.9).mean()), "rel_below_0.5": float((rel < 0.5).mean())}
if __name__ == "__main__":
    jobs = [(s, a) for s in range(1500, 1528) for a in ("DERIVED",)]
    with Pool(4) as p:
        out = list(p.map(run, jobs))
    json.dump(out, open(sys.argv[1], 'w'))
    from statistics import median
    for k in ("n_probes", "oob_share", "rel_mean", "rel_below_0.9", "rel_below_0.5"):
        v = [o[k] for o in out]; print(k, 'median', round(median(v), 4), 'min', round(min(v), 4), 'max', round(max(v), 4))
