"""Engineering calibration for P1b: noise SD at which the phase-1 (noise-free) network's held memory is damaged.
Phase 1 only (no phase-2 arm, no drain/steer/lead-vs-rival contrast)."""
import json, sys, torch, numpy as np
sys.path.insert(0, "/home/user/Toward-an-Artificial-Organism")
import trackc_swap.selfcomp as SC
from trackc_swap.env import WorldConfig
from trackc_swap.train import TrainConfig
import run_p1b_selfcomp as R
seed = int(sys.argv[1]); torch.set_num_threads(1)
wc, tc = WorldConfig(wear=R.WEAR), TrainConfig()
p1 = SC.run_phase1_c(seed, wc, tc)
torch.save(p1["state"], f"{sys.argv[2]}/p1_{seed}.pt")
out = {"seed": seed}
for s in (0.15, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0):
    SC.SIGMA = s
    r = SC.CompRunner("C1NOFATE", seed, wc, tc, tag_offset=SC.EVAL_TAG_C)
    r.load_state(p1["state"]); r.agent.eval()
    _, _, lg = r.evaluate("zero", noise_p=0.5)
    pr = SC.probe_summary_c(lg)
    out[str(s)] = {k: pr[k] for k in ("clear_plain", "clear_noised")}
    print(seed, s, out[str(s)], flush=True)
json.dump(out, open(f"{sys.argv[2]}/sweep_{seed}.json", "w"), indent=1)
