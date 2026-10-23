"""Additive post-processing for N2. The value_optimal / value_always_predict fields in N2_output.json
are INVALID (loop variable r was overwritten inside rollout(); the rate fields are unaffected).
Recompute both from the stored stage-1 Q values and the law marginal P(N, y~1). Reference-only."""
import json
from fractions import Fraction as Fr
from acq_model import graded_model, PHI, CUES
M = graded_model(); o = json.load(open("N2_output.json"))
vo = Fr(0); vp = Fr(0)
for N in CUES:
    for rec in range(6):
        p = Fr(1, 2) * sum(Fr(1, 2) * M["e"](y, Y, N) * ((1 - PHI) * M["q"](rec, y, 0) + PHI * M["q"](rec, y, 1)) for Y in (0, 1) for y in range(6))
        Q = {a: Fr(v) for a, v in o["graded_stage1_received"][f"{N},y~={rec+1}"]["Q"].items()}
        vo += p * max(Q.values()); vp += p * Q["P"]
r = {"value_optimal": str(vo), "value_always_predict": str(vp), "value_gain": str(vo - vp), "floats": [float(vo), float(vp), float(vo - vp)],
     "note": "Supersedes the INVALID value fields of N2_output.json graded_optimal_policy; rates there are valid."}
json.dump(r, open("N2_postproc_values.json", "w"), indent=1); print(r)
