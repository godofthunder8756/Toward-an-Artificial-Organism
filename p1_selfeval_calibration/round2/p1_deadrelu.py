import sys, numpy as np, torch
sys.path.insert(0, "/home/user/Toward-an-Artificial-Organism")
from trackc_swap.selfeval import RTSSAgent, PlainAgent, RegisterWorld, Q_LO
from trackc_swap.env import WorldConfig
from run_trackc_paid import WEAR, RATE
torch.set_num_threads(2)
S = sys.argv[1]
for seed in (9904, 9905, 9906, 9907):
    for arm in ("FATE", "LOSS", "YOKED", "PFATE"):
        for p in (3600, 7200):
            sd = torch.load(f"{S}/calibp1b/weights/seed{seed}_{arm}_{p}.pt")
            ag = PlainAgent() if arm == "PFATE" else RTSSAgent()
            ag.load_state_dict(sd)
            w = RegisterWorld(64, WorldConfig(wear=WEAR), np.random.SeedSequence([seed, 77]), RATE)
            obs = torch.from_numpy(w.reset()); h = ag.init_state(64)
            alive = None; ents = []
            with torch.no_grad():
                for t in range(400):
                    logits, v, h2 = ag.step(obs, h)
                    if arm != "PFATE":
                        z = ag.lat(h2[:, :ag.hidden])[:, :ag.task_dim]
                        a = (z > 0).any(0)
                        alive = a if alive is None else alive | a
                    d = torch.distributions.Categorical(logits=logits); ents.append(d.entropy().mean().item())
                    idx = d.sample(); w.next_gain = np.zeros(64)
                    o, r, done = w.step(idx.numpy()); obs = torch.from_numpy(o); h = h2
            print(seed, arm, p, "task units ever active:", None if alive is None else int(alive.sum()), "/48", "entropy %.3f" % np.mean(ents))
