---
title: E3 pure kernel implementation evidence
description: Bounded contract research and validation for engineering-only pure components
ms.date: 2026-09-10
status: Complete
---

## Scope and questions

* Verify the engineering-only freeze and its prohibition on final target draws.
* Resolve block/repetition decoding, exact integer TD and return arithmetic,
  and deterministic selection from externally supplied ranks.
* Implement only e3/coding.py, e3/arithmetic.py, test_e3_coding.py, and
  test_e3_arithmetic.py, plus this permitted evidence note.
* Establish pure-value behavior with independent constructed fixtures, not
  a paid VM, agent, experiment, protected acquired copy, or execution trace.

## Evidence collected

* All 23 files in E3_DESIGN_FREEZE_v0_11.json match both frozen byte lengths
  and SHA-256 digests. The snapshot is engineering-only and disallows final
  target draws and confirmatory H2 execution.
* E3_POLICY_CONTRACT_v0_5.md defines health priority, bounded mutually
  exclusive action returns, missing-response zero contribution, signed-32
  reward finalization, exact TD rounding, and independent B/T/X ranks.
* The editor-selected interpreter is Python 3.13. No third-party dependency
  is required. The workspace is not a Git repository; Git status is unavailable.

## Resolved contract research

* E3_OPERATION_CONTRACT_v0_3.md, computational kernels: all sixteen generic
  candidates; fixed columns 1..15 followed by 1,2,4,8,15; empty before tie;
  repetition vote over all five symbols. Host value calculations do not
  substitute for the priced 49/3759 scan kernels.
* E3_STATE_CONTRACT_v0_2.md, canonical symbols and learner: 0/1 observed,
  2 erased, 3 invalid; only a unique decode can supply a candidate value.
  There is no target input, history cache or forced-guess repair path.
* E3_PHYSICAL_CONTRACT_v0_4.md, finite G and injury map: positions 4k+r
  lose k=3,4, leaving columns 1..12. Independent enumeration of all 120
  pairs yields full distances {10:80,12:40} and punctured distances
  {5:16,6:48,7:48,8:8}. Minimum distances are 10 and 5 respectively.
* E3_CONTROL_CONTRACT_v0_6.md and CT-001 through CT-010 in
  .copilot-tracking/reviews/2026-09-10/e3-control-review.md were read.
  CT-004 requires signed reward interpretation. CT-005 supplies the floor
  quotient/nonnegative remainder rule and 23-step TD witness. CT-006 requires
  accepted yields, completed prefixes and mutually exclusive action returns.
* The literal selection sequence in
  .copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md uses
  21 selection expressions and three unused slots. Its independent fixture
  counter is not a trace of the production selection implementation.
* No unresolved contract question blocks these pure-value APIs. Full VM
  conformance and experimental authorization remain outside this change.

## Implementation and validation

Created exactly four Python files and this optional note using apply_patch.
This change added no package initializer. A final directory check also found
e3/__init__.py, e3/protocol.py and e3/state.py, none created or edited by this
change. These independently present sibling files were left untouched.
All 23 frozen files were reverified unchanged after implementation.

### APIs

* e3/coding.py: encode(payload4), decode_block(symbols),
  decode_repetition(symbols), immutable DecodeResult, GENERATOR_COLUMNS,
  and the sixteen-word immutable generic CODEBOOK
* DecodeResult fields: payload, health, observed, disagreements, ties_count
* Empty returns payload=None, health=0, disagreements=None and candidate
  count 16 or 2. Nonempty ties return payload=None, health=1, minimum
  disagreements and the number of minimizers. Wrong self-consistent words
  still have health=2. Inputs remain unchanged.
* e3/arithmetic.py: td_update(q,r,m,terminal=False), action_return,
  task_return, finalize_reward and select_action(q_values,b,t,x)
* Numeric inputs require built-in integers, excluding bool and coercion.
  terminal specifically requires bool. Stored q/r/m are signed-16,
  including m on terminal calls before its value is ignored.
* action_return accepts only selected-action counts, accepted energy 0..64,
  accepted material 0..8, and completed writes 0..n for n in {5,20}.
  None action with zero counts is offline zero, not record creation.
* task_return accepts two binary outcome integers, or both None for absent
  feedback returning zero. It is scorer-side arithmetic, never worker truth.
* finalize_reward forms a+b before clamping, accepting a signed-16 prefix
  and b in {-64,0,64}; no signed-16 addition can wrap.
* select_action validates all ranks including unused ones; no draw, modulo
  reduction, rejection loop, Q cache, or upstream independence claim.

### Executed checks

The editor-selected Python 3.13 interpreter ran from the workspace root:

```text
python -B -m unittest -v test_e3_coding test_e3_arithmetic
```

All 29 tests passed in 1.868 seconds (13 coding, 16 arithmetic). The command
used the selected interpreter's absolute executable path and disabled bytecode
output. Diagnostics reported no errors in the four Python files or this note.
Pylance syntax checks also passed for both production modules.
A final rerun with the current package layout, using the same command without
verbose output, passed all 29 tests in 1.507 seconds.

Coverage includes:

* All sixteen encodings and 120 full/punctured codeword-pair distances
* All 1024 repetition symbol strings, binary-only observation counts, and
  erased/invalid empty invariance without mutation
* All 16*210 single/double full-code flips plus four-flip window boundaries
* All 80 minimum-distance pairs' midpoints, ten-erasure ambiguity and each
  nine-erasure survivor; erasures and invalid encodings are both exercised
* All 16*79 zero/single/double survivor-flip fixtures after k=3,4 erasure,
  plus an explicit three-flip miscorrection without oracle repair
* Sixteen fixed sixteen-cue label tables constructed algebraically solely
  for conformance fixtures; no experimental individual or target generation
* Fraction-based TD oracle over 10982 small-q/reward-bin combinations,
  signed-word boundaries, every remainder, numerator extrema, terminal
  behavior and 10000 fixed local Random word fixtures
* Independent 23-expression TD and 21-expression selection counters, with
  three explicitly unused selection slots, not production execution traces
* Every bounded accepted yield and completed prefix, nominal return bounds
  [-84,80], and all 65536*3 signed-prefix/task-contribution finalizations
* All seven nonempty maximizing subsets crossed with all 96 B/T/X inputs;
  exact Fraction probabilities verify conditional exploitation uniformity
  and unconditional (15/16)/k + 1/48 for maxima, 1/48 otherwise
* Malformed lengths, booleans, nonintegers, ranges, absent partial outcomes,
  unselected income, invalid actions and unused malformed rank rejection

## Limitations and follow-on work

* No paid-VM micro-op, tariff, register, execution-trace, or integrated
  conformance claim follows from these pure arithmetic functions.
* No runner, training, target draws, result artifacts, or policy module.
* No protected acquired copy, code writes, Q writes, live packets, deposits,
  stored record handling, actual action executions, or empirical E3 evidence.
* Upstream ranks' randomness/provenance is not established by enumerating
  the deterministic rank-to-action function.
* Built-in integer validation is intentional; arbitrary numeric subclasses
  and iterable streams are not silently converted.
* [ ] If later authorized, integrate through paid worker operations and
  validate complete primitive/register/ROM/ledger traces independently.
* [ ] Add the separate policy/observation module and all 32 policy bins only
  in a later scope; no policy module is created here.
* Clarifying questions requiring user input: none.