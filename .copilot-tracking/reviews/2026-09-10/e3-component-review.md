---
title: E3 component foundation review
description: Read-only review of current E3 components against the engineering-only v0.11 freeze
ms.date: 2026-09-10
---

## Review decision

Complete for the captured, explicitly named component foundation.
Status: REAL COMPONENT BUG FOUND, not an unconditional foundation pass.
One medium-severity contextual protocol validation defect is reproducible.
No high- or critical-severity defect was established. No implementation or
existing test was changed. Full VM/runtime conformance remains unimplemented
and is not counted as a collection of component security bugs.

The existing suite passes with platform skips: 172 tests run, 168 passed,
four skipped, zero failures or errors. Additional contract counterexamples
produce four expected-contract test failures for the same single finding.
These are separate from the passing repository suite.

## Scope, authority and concurrent changes

The initial directory enumeration contained eight Python files, all inspected:
e3/__init__.py, e3/state.py, e3/coding.py, e3/arithmetic.py, e3/protocol.py,
e3/physical.py, e3/meter.py and e3/policy.py. Also inspected
verify_e3_design.py and all eight corresponding test_e3_* modules explicitly
listed in the test command below.

During review, e3/archive.py and e3/inputs.py appeared through concurrent work.
Only their introductory scope declarations were read. They are NOT covered by
this foundation verdict and were not imported, executed, edited or frozen by
this review. At final enumeration the directory therefore contained ten Python
files. This is not a claim to have reviewed the continuously changing directory
as one atomic snapshot.

Normative authority follows E3_INTEGRATION_DECISION_v0_11.md:23-60, including
the v0.10 script amendments, v0.9 interface, v0.6 control/CT repairs, then the
retained v0.5 policy, v0.4 physical, v0.3 operation and v0.2 state contracts.
The 23-entry manifest is a design freeze, not a source/test freeze or permission
for hypothesis runs. No final targets, private input roots, full experiment,
bootstrap, statistical hypothesis evaluation or production worker was run.

## Finding E3-COMP-001

### Medium P2: script ecology accepts a learning-disabled BEGIN

Location: e3/protocol.py:470-485, `FrameCodec._begin()`.
Consequent behavior: e3/protocol.py:487-515, `FrameCodec.validate()`.
Missing regression coverage: test_e3_protocol.py:404-415,
`ContextTests.test_script_ecology_and_reset_future_headers()`.

`_begin()` rejects learning for PERIODIC/THRESHOLD and limits script G to three
phases, but does not require learning for timed script ecology. G=400..403
therefore accepts `Phase.ECOLOGY`, tick 6, `Service.CONTROLLER`, mask 6.
That mask means corrective writes and a planned due response, but no learning.
The same invalid permission combination also round-trips for RESPONSE.

This conflicts with E3_CONFORMANCE_CONTRACT_v0_10.md:75-84: both scripts run
the actual learning path, not the nonlearning fixed-policy path, retaining TD,
retirement, record creation and finalization. Lines 94-98 require the genuine
bookkeeping and learning RESPONSE. Lines 122-123 separately allow learning to
be disabled for script reset recovery. The distinction is knowable from the
immutable script ID and the supplied BEGIN, without history, paid state reads
or a transport state machine.

Executed deterministic counterexample, using synthetic state bytes only:

```python
import unittest
from e3.protocol import (
    BindFrame, BeginFrame, FrameCodec, Phase, Service, ProtocolError,
)

class ScriptLearningContract(unittest.TestCase):
    def test_script_ecology_requires_learning(self):
        for config_id in range(400, 404):
            with self.subTest(config_id=config_id):
                codec = FrameCodec(BindFrame(config_id))
                begin = BeginFrame(
                    Phase.ECOLOGY, 6, Service.CONTROLLER, 0, 6, bytes(276)
                )
                with self.assertRaises(ProtocolError):
                    codec.validate(begin)
```

The executed equivalent used four independent unittest cases. All four failed
with `AssertionError: ProtocolError not raised`; there were no test errors.
For every script ID, a RESPONSE with the same tick/mask also passed contextual
encode/parse. Supplying `LEARNER_RETURN=64` with that accepted BEGIN then raised
`ProtocolError`, because the scalar checker correctly honors the disabled bit.
Thus this is not merely an unused permissive constructor: the contextual API
accepts a header that selects the wrong feedback regime.

Impact is incorrect configuration validation, not a demonstrated sandbox
escape or observed experiment failure. A later adapter trusting these checks
could silently remove the learning workload that SCRIPTED is intended to
measure. The current pure policy selector does not itself execute or remove
that workload; it is not the defective component.

Proposed fix: in `_begin()`, require `Permission.LEARNING` for script G when
`phase == Phase.ECOLOGY` and the service is not entry `ISOLATE`. Reject rather
than silently changing the mask. Apply it to the BEGIN context used by both
frame encode/parse and SCALAR validation. Do not reject learning-disabled
recovery or assay, and do not force learning on ordinary FROZEN RL ecology.

Regression matrix should cover all four script IDs, first and due ticks,
CONTROLLER and RESPONSE, learning-off masks 2/6, learning-on masks 3/7, and
entry ISOLATE at tick zero. Sixteen positive contexts already passed during
review: per script ID, learning ecology mask 7, ecology ISOLATE mask 2,
recovery CONTROLLER mask 2, and assay RESPONSE mask 4.

## Executed evidence and integrity

The editor-selected interpreter was Python 3.13. Existing suites ran with `-B`:

```text
python -B -m unittest -v test_e3_state test_e3_coding test_e3_arithmetic test_e3_protocol test_e3_physical test_e3_meter test_e3_policy test_e3_design
Ran 172 tests in 8.658s
OK (skipped=4)
```

Ad hoc checks set `sys.dont_write_bytecode = True` before project imports and
used in-memory constructed values. No ad hoc source/test file was created.
Existing verifier tests use and clean their own external temporary fixtures;
they do not modify the actual design files. Automated tooling may retain its
own execution output outside the workspace. The only review-authored workspace
file is this document.

| Integrity check | Result |
|-----------------|--------|
| Before tests: verify_e3_design.py | ok=true; file_count=23; files_checked=23; failures=[] |
| After all tests and reproductions: same verifier | ok=true; file_count=23; files_checked=23; failures=[] |
| SHA-256 before/after for eight original e3 modules, verifier, eight tests and manifest | 18 captured files checked; zero changed |
| Editor diagnostics for captured modules, verifier and eight tests | No errors reported |

The hash comparison checks captured contents, not a filesystem lock or proof
against a malicious concurrent replacement. It also does not cover concurrent
new modules. The review deliberately performed no source edits, formatting,
repairs, dependency installs, bytecode generation or broad test discovery.

Additional deterministic checks beyond the existing test suite:

| Check | Observed result |
|-------|-----------------|
| Every fitting persistent field window, widths 1..32 | 59,680 allowed windows preserve surrounding bits and round-trip; 10,480 restricted windows reject without mutation |
| Every one of 3,160 physical draw slots individually activated | Exact complete byte image and typed leakage match an independent direct-byte oracle in all cases |
| Meter minimum/fee/body scalar boundary combinations | 288 independent arithmetic comparisons passed |
| Malformed meter current/local/tail/minimum/packet/permitted arguments, each component | 560 cases rejected atomically, including bool, negative, float, string, None and int32 overflow |
| Known all-zero BLOCK versus erased BLOCK | Binary zero uniquely decodes payload 0/health 2; erased input abstains/health 0 |
| Script ecology negative permission cases | Four assertion failures prove E3-COMP-001; 16 neighboring positive contexts pass |
| Verifier unsafe path spellings with guarded file opens | 14 rejected after reading the synthetic manifest, zero payload opens |
| Verifier symlink/reparse flags on root, manifest, directory and file | Eight reason-checked rejections, zero payload opens |

## Examined behavior with no additional defect established

### State layout and mutation boundaries

e3/state.py:18-95 matches the global offsets obtained by adding the 160-bit
code prefix to E3_STATE_CONTRACT_v0_2.md:35-50; it also matches the direct byte
intervals in E3_INTERFACE_CONTRACT_v0_9.md:30-39. Transition reward is signed
16-bit at global 1776; resources occupy global bits 1800..1847; reserve starts
at 1944. These coordinate systems differ intentionally, not by an offset bug.

`_ram_range()`, `_read()` and `_write()` at e3/state.py:132-165, together with
`State.read_bits()`/`write_bits()` at 212-229, correctly handle unaligned
1..32-bit fields and preserve bits outside the requested window. The additional
70,160-window sweep includes both restricted boundary crossings. Typed E/P
setters check the full value before mutation. Raw snapshots preserve invalid,
reserved and high resource bits rather than normalizing them.

Existing test_e3_state.py:173-312 and 332-408 cover signed extremes,
sub-two-bit neighbor preservation, restricted lanes, all 48 resource high-bit
positions, malformed types and atomic rejection. Tests at 421-487 cover the
separate 32-byte scratch, explicit zeroing and absence of an implicit paid
service claim. State/reset/snapshot APIs intentionally do not supervise worker
lifetimes or cancel external handles.

### Coding values and arithmetic

e3/coding.py:19-128 matches the parity columns and unique-minimum/abstention
rules in E3_OPERATION_CONTRACT_v0_3.md:136-155 and the health priority in
E3_POLICY_CONTRACT_v0_5.md:239-246. Repetition tests enumerate all 1,024 raw
five-symbol inputs; BLOCK tests cover all 16 generic words, 120 pair distances,
ties, invalid symbols, puncturing and deliberate miscorrection.

`decode_block([0] * 20)` returns
`DecodeResult(payload=0, health=2, observed=20, disagreements=0, ties_count=1)`.
The all-zero binary group is genuinely observed and uniquely decodes zero;
zero is not a missing/false payload. Conversely `[2] * 20` and `[3] * 20`
abstain. No default guess is injected and no true target is consulted.
`encode(True)` and `encode(False)` raise TypeError; test_e3_coding.py:204-232
already checks these and malformed decode symbols. No encoder-bool gap was
found in the inspected implementation.

e3/arithmetic.py:26-45 implements reward clipping, exact signed floor
quotient/remainder round-even and final signed-16 saturation. This is
mathematically equivalent to the signed absolute-value definition in
E3_POLICY_CONTRACT_v0_5.md:263-282 and the CT-005 floor-remainder repair in
E3_CONTROL_CONTRACT_v0_6.md:156-167. Tests compare rational arithmetic at
signed extremes, negative ties, every remainder and fixed local fixtures.

`action_return()`, `task_return()` and `finalize_reward()` at
e3/arithmetic.py:48-114 use accepted amounts, actual completed writes, signed
stored rewards and a wide sum before clipping. Missing outcomes give
informational zero, not a created record. Corrupted signed rewards are clipped
when consumed, not sanitized on loading raw state. All 65,536 stored reward
values crossed with the three permitted task returns are tested at
test_e3_arithmetic.py:185-198. Requiring a valid signed-16 `m` even for terminal
calls is a documented pure-function input convention, not a paid successor read.

Independent primitive counters in test_e3_arithmetic.py are mathematical
witnesses, not traces of production kernel instructions. Missing actual kernel
PC/register/meter execution is explicitly documented and is not misreported as
an implemented conformance failure.

### Physical placement, damage and input validation

e3/physical.py:90-159 and 194-272 match the 25-vertex tree, 1,080 faultable
RAM lanes, 948 accessible lanes, 132 reserve lanes, source-local 17/23 code
and 10/14 auxiliary prices, and conditioning dues. All map rows/routes and
source balances are checked in test_e3_physical.py:108-272.

`fault_thresholds()` implements exactly h=(age+1)/1000 and e=age/10000
through integer thresholds against uniform integers 0..9999. Tests at
274-280 count every one of 10,000 possible ranks for every age using Fraction;
359-376 exercise strict threshold boundaries in actual transitions.
`FaultFrame` at e3/physical.py:294-326 rejects bool and every malformed draw
before any state write; `apply_faults()` revalidates the whole frame.

`apply_faults()` at e3/physical.py:375-420 uses one current pre-fault state for
all hazards. Age words themselves use their physical storage domains, not the
domains they describe. Same-step age corruption cannot change a later lane's
hazard, but the next call uses the corrupted current ages. Existing tests at
378-451 distinguish both cases and test malformed final-slot atomicity.

All-9999 draws cause no RAM changes but still lose one from each positive
resource. Resources are typed unsigned stocks, never XOR targets. Dead-state
calls do not revive or update flags. Code erasure overrides flips; invalid/erased
code is never populated by sign flip. Hub damage clears the actual hub's RAM
including its portions of age words and reserve; it does not clear every age
that describes that hub. These are the selected physical laws, not bugs.

Primary 32-site lesion, all four hub lesions, odd/even floor resource losses,
stale-state independence and high resource values pass. The additional one-hot
draw experiment independently exercises all 3,160 slot-to-lane mappings, not
only an all-zero/all-9999 aggregate. Loss results contain no retained snapshot,
age vector or fault frame; the one temporary pre-fault copy is trusted physics
working storage, not worker state.

### Meter arithmetic, gates, deposits and atomicity

e3/meter.py:106-185 correctly distinguishes the minimum rejection/retirement
path from the optional-body remainder. It checks M+minimum_exit+T+rho first,
pays exactly 128, then checks c+L+T+rho against the remaining stock. Source
equality is allowed; energy retains positive residue. For E=137, c=0, L=264,
minimum_exit=8, it pays 128, rejects the body and leaves E=9. This is correct,
not an omitted 264-energy minimum or a last-energy debit.

All numeric cost components are nonnegative strict built-in integers bounded
by INT32_MAX. This is the correct nonnegative cost-vector domain despite using
signed-32 intermediates. Signed rewards and negative observer deltas have
different APIs; negative costs must not be accepted as credits. The 560 added
malformed-input cases verify rejection before fee, debit, physical shutdown
sink or deposit, including hostile in-memory `Cost` field corruption.

`debit_and_deposit()` at e3/meter.py:296-316 validates packet/caps before any
debit and computes acceptance after that debit. At E=65535, c=20 and an offered
20, it accepts all 20 and returns E to 65535; computing acceptance against the
pre-debit cap would have been wrong. Actual overflow is returned, not retained
as stock. `passive_grant()` is the explicit pre-fee exception and ignores all
grants after E=0. New canonical activation does not reuse stale acquired RAM.

Accepted-material transport per hop, quote maxima before paid address
discovery, one-shot packets, operation ordering and service-specific residue
are caller obligations explicitly stated in e3/meter.py:7-16 and 269-315.
The absence of automatic per-hop charging here is therefore not a component
bug or false claim. Current caller-supplied quote vectors are not stored escrow
or reusable admission receipts. test_e3_meter.py:397-433 correctly preserves
mandatory TERMINAL clearing while optional TD rejects in the AN-001 witness.

### Policy selectors and remaining frame semantics

e3/policy.py:93-138 implements resource priority for fixed rules, exact h=3
thresholds, public planned-clock periodicity and the SCRIPT-U usefulness
predicate. RL/DRIVE uses the supplied current damaged row without a hidden
resource override or history. All 32 observation states and rank alternatives
are tested, as are the nine periods. DRIVE's selected scrub bonus remains 16
even when no write completed, correctly following
E3_POLICY_CONTRACT_v0_5.md:429-451. No-maintenance is explicitly a component
diagnostic, not a new authorized BIND catalog entry.

`PolicyConfig` cuts describe upstream observation binning; `decide()` receives
the already formed state index and must not rebucket it. Validating unused
Q/rank placeholders for fixed/script functions does not require paid Q reads
or consumption of forbidden random packets. This is documented API behavior.

Apart from E3-COMP-001, the reviewed protocol checks pass structural lengths,
strict integers/enums, reserved bits, exact scalar widths, signed tag17,
code-specific teaching, immutable BIND, template capability and semantic BAD
input checks. The due mask is a planned calendar fact, not stored slot validity;
query RESPONSE occurs even without a planned due query, to retire fault-created
contents. These distinctions are intentional. H1-family G is not synonymous
with assay phase: its development still permits learning feedback. Ordinary
learning-disabled RL ecology is the declared FROZEN mode and must remain legal.

Duplicate/order/count enforcement, current-opcode direction, paid TEMPLATE
BAD handling, scalar consumption and completed-S certification belong to the
documented future transport/executor. No missing FSM or direct low-level call
is presented here as a security vulnerability.

### Freeze verifier path safety and platform limits

verify_e3_design.py:47-76 rejects symlinks and Windows reparse points at every
path component before reading, rejects noncanonical relative paths including
traversal, UNC/drive/ADS aliases, and checks resolved containment. Root ancestry
is separately checked at 104-109. JSON duplicate keys, nonstandard constants,
strict boolean flags, nonnegative integer sizes and exact lowercase SHA-256
schema are validated before file hashing at 117-159.

The suite's four native symlink tests at test_e3_design.py:210-245 skipped
because Windows returned error 1314. The deterministic metadata test at
247-269 passed. Additional in-memory fixtures guarded `Path.open()` and
verified the intended rejection reason: symlink/reparse metadata at root,
manifest, nested directory and payload prevented all payload opens. Fourteen
unsafe names were rejected after the synthetic manifest was actually parsed
(`file_count=1`, `files_checked=0`), avoiding false positives from a fixture
that never reaches the target validation. No real external user file or secret
was accessed by these probes. No elevation or native junction creation was
attempted.

This supports static-tree path rejection, not native junction integration or
resistance to concurrent adversarial replacement. The verifier explicitly
requires a quiescent tree and does not claim an OS sandbox. Hash integrity
without an externally anchored trusted manifest is also not authenticity or
implementation conformance; successful verification grants no execution rights.

## Recommended follow-up and clarifications

* [ ] Fix E3-COMP-001 and add the contextual script permission regression matrix
  in a separately authorized implementation change.
* [ ] Run the four native symlink tests and native Windows junction fixtures in
  a suitable test environment; no privilege change is needed for this review.
* [ ] Review concurrent e3/archive.py and e3/inputs.py separately once their
  authors provide stable source/tests. They are not included in the 18-file
  unchanged-content check.
* [ ] When the runtime exists, test paid instruction traces, service ownership,
  packet order/count/direction, sourcewise quote derivation, accepted transport,
  script bookkeeping, and real reset/isolation. These are later integration
  gates, not additional defects inferred from the current component scope.

No user clarification is required for the finding or the captured foundation
review. This review does not authorize implementation edits, final targets or
experimental promotion.