"""Engineering check (phase 1 only): does paid phase 1 develop body regulation? No arm, no contrast."""
import json, sys, torch
sys.path.insert(0, "/home/user/Toward-an-Artificial-Organism")
import trackc_swap.selfcomp as SC
from trackc_swap.env import WorldConfig
from trackc_swap.train import TrainConfig
import run_p1b_selfcomp as R
from run_p1_selfeval import regulates
seed = int(sys.argv[1]); torch.set_num_threads(1)
p1 = SC.run_phase1_c(seed, WorldConfig(wear=R.WEAR), TrainConfig(), pay=R.PAY[1], reg_iters=4800)
ev = p1["eval"]; pr = ev["probes"]
out = {"seed": seed, "in_band": ev["in_band"], "eat_low": ev["eat_rate_low"], "eat_high": ev["eat_rate_high"],
       "regulates": regulates(ev), "abstain": ev["abstain_rate"], "clear_correct": pr["clear_plain"]["correct_given_report"],
       "clear_abstain": pr["clear_plain"]["abstain"], "noised_acc": pr["clear_noised"]["correct_given_report"],
       "curve_in_band": p1["curve_in_band"]}
json.dump(out, open(f"{sys.argv[2]}/reg_{seed}.json", "w"))
print(json.dumps({k: v for k, v in out.items() if k != "curve_in_band"}), p1["curve_in_band"][::30], flush=True)
