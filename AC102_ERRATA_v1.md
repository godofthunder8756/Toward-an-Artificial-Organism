# AC102 errata v1: G3/G4 predicate reversed (six-of-eight, not seven); screened-not-unseen seeds; narrowed inference

2026-09-20. Non-frozen correction note, in the AC100/101 convention. The frozen artifacts are
preserved unchanged — `ac102.py`, `AC102_PROTOCOL_v1.md` (a hashed source), and
`ac102_results_v1/{rows.jsonl, results.json, pre_run_snapshot.json}` — no gate was re-run and no
frozen code or protocol was edited. `AC102_RESULTS_v1.md` (not a hashed source) and
`AUTONOMY_RESEARCH_STATUS.md` carry the corrected narrative; this note records the corrections.

## 1. G3's predicate is reversed between the protocol and the code — six-of-eight, not seven

The frozen protocol's G3 is **"staging rescues the composition failure"**: every distinct seed that
dies under `both` must SURVIVE under `staged`, and the protocol states this gate is **expected to
FAIL** (`AC102_PROTOCOL_v1.md`, "Expected to FAIL: the engineering screen shows the death seeds die
under BOTH arms at the SAME tick (8408)").

The implementation (`ac102.py`, `gates_ac102`) instead checks the **negation** — `both` survives OR
`staged` dies (i.e. "no individual where `both` dies but `staged` survives") — and records PASS. The
frozen `results.json` stores this as `G3_timing_hypothesis_falsified_staged_does_not_rescue: true`.

The observations agree (staging does not rescue — 4934/5002 die at 8408 under both arms), but the
implementation's PASS answers a different question than the protocol's G3. Under the protocol's
stated predicate, **G3 FAILS** (staging did not rescue) and **G4 FAILS** (staging broke recovery,
2/8). The correct accounting is therefore **SIX of eight gates pass** — G1, G2, G5, G6, G7, G8 pass;
G3 and G4 fail — not seven. A green audit currently confirms the implementation's interpretation,
not agreement with the protocol. Recorded here; the frozen code and `results.json` are not edited
and not re-run.

## 2. Screened diagnostic seeds, not unseen

The protocol discloses that the entire 4872-5099 range was scanned and the final seeds selected
using their observed outcomes (the final stratum spans the death-prone material regime, two
death-prone seeds 4934/5002 and two survival seeds 4880/4950; the adversarial stratum is the four
`[3,0,2,1]` seeds 4883/4901/4928/5038, all of which survive `both` in the scan). All eight final
seeds lie inside 4872-5099. The later claim that the scan range is "excluded from finals" /
"unseen" contradicts the listed seeds. Disclosure preserves transparency; it does not make those
outcomes unseen.

Corrected disclosure: **"screened diagnostic cohort, selected from a disclosed scan of
4872-5099."** The protocol's own anti-drift line ("the scan range [is] excluded from the final
sample") also contradicts its screening disclosure; noted here, not edited (hashed source).

## 3. Headline replacement (exact wording)

> Matched runs establish a corruption-move interaction. Eight-write reconstruction staging fails to
> rescue two selected cases and introduces two additional recovery failures through loss of the
> repair trigger.

## 4. Narrowed inference

The results reject the tested eight-write staging policy, and nothing more. They do NOT establish:

- **(a) that timing is irrelevant.** The staged budget still crossed the material threshold on the
  marginal seeds (material 71/72 at the corruption tick; any spend ≥ 8 drops it below 64), and an
  intervention that fails to prevent the proposed causal event cannot rule that event out.
- **(b) that reconstruction must be immediate.** Staging introduced a SECOND failure — the program's
  majority repair removes the discrepancy signal the reconstruction depends on — which shows an
  interaction between repair scheduling and repair detection, not that every staged schedule must
  fail.
- **(c) that changing the resource currency is necessary.** "This schedule fails" and "only price
  matters" are different conclusions.

Recorded plainly: the staging suggestion failed in this implementation.
