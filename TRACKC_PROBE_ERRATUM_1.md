# Option P probe: erratum 1 (2026-11-12)

Found while designing option Q. It corrects a description. No number or
verdict in [TRACKC_PROBE_RESULTS.md](TRACKC_PROBE_RESULTS.md) changes.

## The error

[TRACKC_PROBE_PROTOCOL.md](TRACKC_PROBE_PROTOCOL.md) (§2) and the docstring of
[`trackc_swap/probe.py`](trackc_swap/probe.py) say an agent can see whether it
ate on the previous step "through its previous action and previous reward".

**That is wrong.** Those two inputs are the echo channels, which have been
zeroed in the world since v3 (`trackc_swap/erasure.py`, `_NoEcho`). The agents
of v7 and v8 never received them.

## What is true instead

The only trace of a meal in the agent's input is in its view: the food it was
standing on disappears. Any knowledge of its own eating must be inferred from
that and carried in its recurrent state.

## Consequences

- **The decoders and verdicts are unaffected.** The window decoder used the
  true eating flags from the simulator. It is still a valid ceiling: what
  perfect knowledge of recent eating, plus recent interoception, says about E.
  But it is not "an ideal linear readout of the recent inputs", as the
  protocol called it. It is an upper bound that the inputs alone may not
  reach.
- **P2 is, if anything, a stronger finding than described.** Regulators'
  states carry about a fifth of the unreported change in E, although no input
  tells them directly that they ate.
- **Option Q(a) as listed cannot be run.** The results file (§8) proposed
  blanking the previous action and reward. Those inputs are already blank. Q
  uses a different test of whether anticipation is used; see
  [TRACKC_CAUSAL_PROTOCOL.md](TRACKC_CAUSAL_PROTOCOL.md).

The frozen protocol and module are left unchanged, because the probe's source
hashes pin them.
