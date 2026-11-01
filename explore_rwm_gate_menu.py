"""Bounded engineering search: can a semantic gate menu on the RWM wiring reach
the RWM-PSG v1 integration criterion (T6: Phi_s > 0 on >= 1/2 stationary mass)?

ENGINEERING / Q-EXIST probe only. Coordinate ascent from RWM-8 over a fixed,
declared menu; structural admissibility (T1 single SCC, T2 bottleneck, monitor
without sensory input) is enforced. A failure to find a witness is UNRESOLVED
for the class, not an impossibility proof. Usage:

    python explore_rwm_gate_menu.py rwm_gate_v1/menu_search.json
"""
import json
import sys
import time

from rwm.integration import phi_s
from rwm.primitives import COPY, MAJ, OR, TABLE, THRESHOLD, XOR, strongly_connected_components
from rwm.topology import A_GATE, G_GATE, K_GATE, RWM_MODULES, X_GATE, XNOR_GATE, _net
from rwm.world import agent_state_weights, closed_loop_summary

MENU = {
    "X": [(("A", "C", "oR", "X", "K"), X_GATE),
          (("C", "oR", "X", "K"), TABLE("PMUX", 4, lambda c, o, x, k: o if c else int(o + x + k >= 2))),
          (("oR", "X", "K"), MAJ(3)),
          (("K", "E"), XOR(2)),
          (("oR", "C", "E"), TABLE("oR^(~C&E)", 3, lambda o, c, e: o ^ ((1 - c) & e))),
          (("oR", "E", "K"), XOR(3))],
    "E": [(("X", "oR"), XOR(2)),
          (("X", "A", "oR"), TABLE("XOR(X&A,oR)", 3, lambda x, a, o: (x & a) ^ o))],
    "A": [(("K", "C"), A_GATE), (("K",), COPY()), (("K", "M"), XOR(2)), (("K", "C"), XNOR_GATE)],
    "I": [(("oH", "I", "K"), MAJ(3)), (("oH", "K"), XOR(2)), (("oH", "K"), OR(2))],
    "G": [(("I", "E", "C", "G"), G_GATE),
          (("I", "E", "M", "G"), THRESHOLD([2, 1, 1, 1], 2)),
          (("I", "E", "G"), MAJ(3)),
          (("I", "E"), XOR(2))],
    "K": [(("G", "K", "I", "X"), K_GATE),
          (("G", "K", "I"), TABLE("HOLD(G;K,I)", 3, lambda g, k, i: i if g else k)),
          (("K", "G"), XOR(2)),
          (("I", "X", "K"), MAJ(3)),
          (("G", "I", "X"), TABLE("G&(I|X)", 3, lambda g, i, x: g & (i | x)))],
    "C": [(("C", "M"), XOR(2)),
          (("E", "C", "G"), TABLE("~E&(C|~G)", 3, lambda e, c, g: (1 - e) & (c | (1 - g)))),
          (("E", "C", "G"), TABLE("MAJ3(~E,C,~G)", 3, lambda e, c, g: int((1 - e) + c + (1 - g) >= 2)))],
    "M": [(("C", "E"), XNOR_GATE)],
}
ORDER = ["X", "E", "A", "I", "G", "K", "C", "M"]


def build(choice):
    return _net("menu", [(n,) + MENU[n][choice[n]] for n in ORDER], RWM_MODULES)


def admissible(net):
    eff = net.effective_edges()
    if any({RWM_MODULES[a], RWM_MODULES[b]} == {"EXT", "INT"} for a, b in eff):
        return False
    if any(src in net.external for n in ("C", "M") for src in net.inputs[n]):
        return False
    return len(strongly_connected_components(net.nodes, eff)) == 1


def score(net):
    loop = closed_loop_summary(net)
    weights = agent_state_weights(net, loop.pop("_pi"))
    mass = sum(p for (s, e), p in weights.items()
               if phi_s(net, s, dict(zip(net.external, e)))["phi"] > 0)
    return mass, loop["mean_lifetime_steps"]


def main(out_path):
    t0 = time.time()
    choice = {n: 0 for n in ORDER}
    best = score(build(choice))
    trace = [{"step": "start", "choice": dict(choice), "mass": best[0], "lifetime": best[1]}]
    evaluated = 1
    for rnd in range(4):
        improved = False
        for n in ORDER:
            for k in range(len(MENU[n])):
                if k == choice[n]:
                    continue
                cand = dict(choice, **{n: k})
                net = build(cand)
                if not admissible(net):
                    continue
                sc = score(net)
                evaluated += 1
                if sc[0] > best[0] + 1e-9 or (abs(sc[0] - best[0]) < 1e-9 and sc[1] > best[1] + 1e-9):
                    best, choice, improved = sc, cand, True
                    trace.append({"step": f"round{rnd}:{n}={k}", "choice": dict(choice),
                                  "mass": sc[0], "lifetime": sc[1]})
        if not improved:
            break
    result = {
        "class": "ENGINEERING (bounded Q-EXIST probe)",
        "menu_sizes": {n: len(MENU[n]) for n in ORDER},
        "menu_gates": {n: [g.kind for _, g in MENU[n]] for n in ORDER},
        "evaluated_admissible": evaluated,
        "best_mass_phi_positive": best[0],
        "best_lifetime": best[1],
        "best_choice": choice,
        "best_gates": {n: MENU[n][choice[n]][1].kind for n in ORDER},
        "witness_found_for_T6": best[0] >= 0.5,
        "trace": trace,
        "seconds": round(time.time() - t0, 1),
    }
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=1)
    print(json.dumps({k: v for k, v in result.items() if k != "trace"}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "menu_search.json")
