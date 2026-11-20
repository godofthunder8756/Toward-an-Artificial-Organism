"""P1c post-hoc (disclosed, exploratory; written after the final result was known).

Question: the frozen drain probe lowers the shown interoceptive reading by 0.15. The fate gain is
two-sided (out of band, 0.4-0.6, on either side). So a drain raises the apparent risk only when the
pre-drain reading lies below 0.55, and lowers it when the reading lies above the band. PFATE's per-seed
drain effects at 3600 are large in both signs while PYOKED's are near zero. Does the sign follow where
the body sits?

Method: reload each seed's saved 3600 weights (PFATE and PYOKED), run the frozen probe evaluation
(overwrite off, drain on half the trials) in a fresh evaluation world, and log the pre-drain reading
(the noiseless delayed energy the agent is shown) at every probe. For each clear trial, the apparent
change in gain the drain causes is dg = gain(x - 0.15) - gain(x). Trials are split into
UP (dg > 0: the drain makes the body look worse), FLAT (dg = 0) and DOWN (dg < 0: it looks better).
Per seed and arm: abstention on drained trials minus abstention on undrained trials of the same split
(undrained trials are split by the dg they would have had).
Nothing frozen is modified; module classes are subclassed in this script only.
"""
import json, os, sys
import numpy as np
import torch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
torch.set_num_threads(1)
import trackc_swap.selfover as SO
from trackc_swap.selfeval import Q_LO, DRAIN_SHIFT
from run_p1c_selfover import WorldConfig, TrainConfig
import run_p1c_selfover as R

SEEDS = R.FINAL_SEEDS
REPEATS = 3   # independent evaluation worlds per seed and arm (more trials than the frozen single run)


def g_of(x, c):
    half = 0.5 * (c.band_hi - c.band_lo)
    return np.maximum(np.maximum(c.band_lo - x, x - c.band_hi), 0.0) / half


class LogWorld(SO.OverWorld):
    def step(self, action):
        t = self.t
        pr = self.probe[t]
        n_logs = len(self.probes_log)
        if self.record and pr.any():
            td = max(t - self.cfg.intero_delay, 0)
            x = np.asarray(self.Ehist[td])[np.flatnonzero(pr)].copy()
        out = super().step(action)
        if self.record and pr.any() and len(self.probes_log) > n_logs:
            self.extra.append(x)
        return out


SO.OverWorld = LogWorld   # OverRunner looks the class up at construction


def run(seed, arm, rep, wc, tc):
    c = SO.OverRunner(arm, seed, wc, tc, 0.04, Q_LO, tag_offset=SO.EVAL_TAG_O + 100 + rep)
    sd = torch.load(os.path.join(ROOT, "p1c_selfover", "weights", f"seed{seed}_{arm}_3600.pt"))
    c.agent.load_state_dict(sd)
    c.agent.eval()
    c.world.extra = []
    _, _, lg = c.evaluate("zero", drain_p=0.5)
    x = np.concatenate(c.world.extra)
    assert len(x) == len(lg), (len(x), len(lg))
    return lg, x


def main():
    wc, tc = WorldConfig(wear=R.WEAR), TrainConfig()
    out = {}
    for seed in SEEDS:
        out[seed] = {}
        for arm in ("PFATE", "PYOKED"):
            lgs, xs = zip(*[run(seed, arm, k, wc, tc) for k in range(REPEATS)])
            lg, x = np.concatenate(lgs), np.concatenate(xs)
            clear = lg[:, 0] == 0
            drained = lg[:, 1] == 1
            abst = 1.0 - lg[:, 2]
            dg = g_of(x - DRAIN_SHIFT, wc) - g_of(x, wc)
            split = np.where(dg > 1e-9, "UP", np.where(dg < -1e-9, "DOWN", "FLAT"))
            rec = {"x_mean_clear": float(np.mean(x[clear])),
                   "share": {}, "effect": {}, "n": {}}
            m_all_d, m_all_p = clear & drained, clear & ~drained
            rec["drain_effect_all"] = float(abst[m_all_d].mean() - abst[m_all_p].mean())
            for s in ("UP", "FLAT", "DOWN"):
                md, mp = m_all_d & (split == s), m_all_p & (split == s)
                rec["share"][s] = float(np.mean(split[clear] == s))
                rec["n"][s] = [int(md.sum()), int(mp.sum())]
                rec["effect"][s] = (float(abst[md].mean() - abst[mp].mean())
                                    if md.sum() >= 10 and mp.sum() >= 10 else None)
            out[seed][arm] = rec
        print(seed, {a: (round(out[seed][a]["drain_effect_all"], 3),
                         {k: (None if v is None else round(v, 3)) for k, v in out[seed][a]["effect"].items()},
                         round(out[seed][a]["x_mean_clear"], 3)) for a in out[seed]}, flush=True)
    with open(os.path.join(os.path.dirname(__file__), "drain_by_body.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
