# Track C swap line: erratum 1 (2026-11-12): fate and yoked agents shared optimizer state

Found during calibration for option R. It affects how every scaffolded pair
in v2–v8 was trained. No earlier module or result file is changed: the modules
are hash-pinned, and the results stand as records of what was run. This file
says what was run, what it puts in doubt, and what is being done.

## 1. The error

In every scaffolded pair, the fate agent and the yoked agent were loaded from
one phase-1 state object:

```python
state = state_from_bytes(p1)
fate.load_state(state)
yoked.load_state(state)
```

`load_state` calls `Optimizer.load_state_dict`, which does not copy tensors.
Both agents' Adam optimizers therefore held **the same** step counter and the
same first- and second-moment buffers. The network weights were separate.

During training the two agents updated in turn. Each update wrote its
gradient into the shared moments, and the other agent's next update used
them. So each agent was moved partly along its partner's gradient, and the
step counter advanced twice per iteration.

A unit test (`TestPaid.test_optimizers_are_independent`) now demonstrates the
sharing under the old loading pattern, and its absence under option R's.

## 2. How it was found

Option R trains three agents per seed from one phase-1 state. In calibration,
the derived agent's result changed with the *paid* agent's reward weight on
the same seed (seed 9100: in band 0.70, 0.80 and 0.65 at weights 1, 5 and
20). The paid agent has no legitimate path to the derived agent. Checking the
optimizers showed the shared buffers.

## 3. What is affected

| | Affected? |
| --- | --- |
| v1; v2's cold-start cells | no: each agent was initialized separately |
| phase-1 (no-fate) agents, DRIVE agents | no: one agent per optimizer |
| v2 scaffold cells, v3, v4, v5, v6, v7, v8: every fate/yoked pair, M1 and M0 | **yes** |
| options K, P and Q | the measurements are correct; the agents they measured were trained under the coupling |
| G1 (analytic) | no |

## 4. What this puts in doubt

**The yoked control was not an independent learner.** It received erasure
independent of its own E, as described. But its learning was coupled to the
fate agent's.

1. **"Fate agents regulate and yoked partners do not" (v6, v7, v8).**
   - The regulation gradient can only arise in the fate agent, because only
     its erasure depends on its own E.
   - Sharing moments leaks that gradient toward the yoked partner, and
     dilutes it in the fate agent with the partner's gradient.
   - Both effects shrink the fate–yoked gap, so the qualitative result is
     probably conservative.
   - This is an argument, not a demonstration. **The regulator rates under an
     ordinary optimizer are not known.**
2. **The nulls of v2–v4.** The fate agent's regulation gradient was diluted
   there too. The coupling may have contributed to the failure to emerge.
3. **Option K: "yoked partners match their fate partners' bypass".** Each
   yoked partner scored within 0.02 of its fate partner under full erasure
   and used the same wall channel. The results read this as "the bypass
   follows the erasure an agent experiences". The coupling is now an
   alternative explanation: the partner may have been pulled to the fate
   agent's solution.
4. **Option P: "yoked partners encode E almost as strongly as regulators".**
   This was the basis for the reading that fate added the use of E, not its
   representation. It may be leaked gradient. The same holds for the yoked
   partners' unexplained eating rates.
5. **M0 controls.** Each M0 fate agent was coupled only to its M0 yoked
   partner. Neither has a regulation gradient, so these controls are the
   least affected.

Not in doubt as measurements: the behaviour and internal states of the saved
regulators themselves (K's position code, P2's anticipation, Q-b's dependence
on interoception). Those describe agents that exist. What needs
re-establishing is how reliably such agents arise without the coupling, and
how they compare with partners that learn independently.

## 5. What is being done

- **Option R loads an independent deep copy of the phase-1 state into every
  agent** (`trackc_swap/paid.py`, `load_independent`).
- **R's training stage is therefore the first run of this line with
  independent optimizers.** It is SAT, `r` = 0.3, on 18 fresh seeds, with a
  derived agent and a yoked agent per seed. Its protocol adds a claim (R0)
  that tests whether derived regulation holds without the coupling, and
  pre-states what the leak hypothesis predicts for yoked partners' eating and
  E code.
- **Not yet rerun:** SAT `r` = 0.1, the GRADED cells, the M0 controls, and
  v6's bypass world. Until they are, v6–v8's rates in those cells carry this
  caveat.

## 6. Why it was missed

The pair-training code was written for v2 and reused, by import or by copy of
the same loading lines, in every later run. Tests checked that the two agents'
*weights* were equal at the start. No test checked that their optimizers were
separate.
