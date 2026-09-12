---
title: E3 runtime boundary research
description: Read-only implementation and Windows capability investigation for the next paid-worker boundary.
ms.date: 2026-09-10
---

## Status and scope

Complete for the requested research scope. Only this research file was edited.
No implementation, installation, elevated command, secret enumeration, experimental filesystem read
by a worker, or final experiment is authorized by this research task.

## Research questions

* What do the actual machine, kernels, upkeep, protocol codec, selected interface
  v0.9, IFR3, and integration implementation provide or still omit?
* What is the exact next paid-worker service and transport state machine, including
  dynamic requests, accounting, reset boundaries, and noninterference?
* Which Windows and Python capabilities support a trusted-code, nonadversarial
  process boundary without claiming an adversarial sandbox?
* Which implementation phases can proceed after engineering design freeze,
  with what bounded validation and performance checks, while final remains closed?

## Findings

### Authority and actual source state

The design freeze exists and a read-only verification passed all 23 entries,
including exact lengths and SHA-256. The older plan's zero-implementation and
no-snapshot statements are historical, not the current source inventory.
E3_INTEGRATION_DECISION_v0_11.md permits engineering implementation after this
freeze without routine permission requests. Engineering experiments still need
technical validation. Final target/root draws and the current confirmatory H2
launch remain prohibited, regardless of later script success.

e3/machine.py supplies a finite forward-DAG instruction fragment with literal
ROM, counted scratch PC, READ2/WRITE2, kernel arithmetic, prepaid CONTROL and S.
It does not implement an admitted service, outer/nested METER opcodes, paid
scalar ownership, permissions, source-derived complete L/T bounds, or a process
boundary. e3/kernels.py supplies actual BLOCK/REP scan ROM, not a service.
The initial inventory had no upkeep module. During final readback, e3/upkeep.py
and test_e3_upkeep.py appeared from concurrent work; both were inspected without
editing. Paid ISOLATE and AGE_LOW/HIGH wrappers now exist, as qualified below.
No worker/transport launcher or CONDITION implementation was present at closeout.
e3/physical.py supplies physical codecs/quotes/transitions, not paid services.
e3/protocol.py explicitly supplies structural/contextual codecs,
not session ordering, direction, duplication, scalar-count or live-site checks.

### Observed local capabilities and limits

The editor-selected executable is the existing Python313 installation. Executed
metadata reports CPython 3.13.3 and Windows 10.0.22631 x64. No install, service
change, account creation, elevation, or entropy/target draw was attempted.

Three disposable public-probe children ran with -I -B -S -u, shell=False,
close_fds=True, binary pipes, a non-workspace runtime working directory, and a
new environment containing only SystemRoot. All echoed the exact six bytes
00 0A 1A FF 0D 00. Startup, trusted stdlib preload, probes and shutdown together
took 0.311075, 0.312563 and 0.260397 seconds; these are not worker throughput.
Children reported isolated=1, no_site=1, no_bytecode=true, no ctypes or e3 module,
and no environment key outside the explicit SystemRoot whitelist.

After trusted preload, an audit hook raised the designated PermissionError for
built-in open, io.open, os.open, pathlib open, listdir, scandir, socket creation,
subprocess creation, registry open, and a late import. Filesystem/registry probes
used only a deliberately nonexistent public sentinel in the runtime directory;
no experimental file, real registry value, network connection or nested process
was read/created. Binary standard pipes continued working under the hook.

The same probe deliberately demonstrated a limit: os.stat on the nonexistent
sentinel reached FileNotFoundError instead of the hook. Thus an open-event deny
is not complete filesystem metadata isolation. These are actual capability-path
tests, not proof of an adversarial sandbox or the future production image.
Python explicitly warns that Python-level audit hooks can be bypassed by
malicious code. -I also does not erase os.environ or disable system site startup;
the environment whitelist and -S are separate requirements.

Microsoft documents restricted-token APIs and AppContainer on Windows; a missing
launcher is not proof that the OS lacks them or that admin is universally needed.
No usable restricted-token/AppContainer integration was established here. Treat
it as unimplemented/unverified, not a fabricated permission blocker. The feasible
next boundary trusts the Python image and limits untrusted input to interpreted
data. It must explicitly disclaim malicious Python/native code and hostile
same-user processes.

### Actual generic-image reachability probe

A fourth disposable child preloaded the actual machine/kernels and both generic
scan programs from trusted source, removed the temporary workspace search-path
entry, armed the deny hook, and executed two public canonical-empty fixtures.
REP completed 55 steps for 383 energy; BLOCK completed 3,764 steps for 4,303
energy. Both cleared scratch and imported no later module. No experimental
state, target or private root was supplied. This establishes feasibility of
these fragments under the guard, not a paid-worker or production-image pass.

The child did not load e3.inputs, e3.archive, e3.policy, ctypes, socket, or
subprocess. It DID contain winreg through the bootstrap/import closure; the
hook denied winreg events. Do not claim that an application without an explicit
registry import has no registry capability. Future packaging must explain or
remove this dependency and test its actual reachable operations.

Two actual host reference paths were confirmed:

* machine.physical.layout reaches the state module and its trusted helpers
* machine.dataclass.__globals__["inspect"].os reaches os indirectly

The source import graph is therefore not a Python object-capability sandbox.
Removing a name from one namespace or sys.path does not remove references from
function globals, module specs, imported dependencies or code objects. The probe
also necessarily leaves the generic source path in argv/module metadata; it is
not a production assertion that all host paths disappeared. Inspect __file__,
__spec__.origin, package __path__, co_filename, argv/orig_argv, exception frames,
logger handlers and loader caches in the final image. There was no code-hash or
target-hash input in these probes. Do not put a target/state/result digest into
one of those metadata channels; a 16-bit truth table is enumerable from a digest.

The enforceable model restriction is that Instruction/Operand are closed exact
types and no interpreted opcode evaluates Python, imports, reflects objects,
reads argv/environment, dereferences a host object, or accesses a filesystem.
The host can still do those things: its reviewed implementation is trusted.
Generic codebook constants contain all candidate words, not an acquired clean
copy; calling a pure decoder as a free worker helper would nevertheless violate
the selected instruction/cost model.

## Exact implementation gaps

| Component and symbols | Present evidence | Required paid-runtime addition |
|-----------------------|------------------|--------------------------------|
| e3/machine.py: Opcode, OperandKind, Instruction, Program, validate | Closed ALU/access/S fragment, forward DAG, per-path CONTROL bounds | Typed M/C/current scalar/SENSE/ATTEMPT/DUES/PASSIVE/deposit/living/rent semantics, public-header/G operands and selected linked service entries |
| e3/machine.py: _bounds, step, execute | Immutable supplied bounds; default L retains only S8; execute prepays CONTROL | Construct and validate complete G-derived L/T; real outer/nested gates; operation-specific entry/branch/S/minimum semantics; no arbitrary caller bounds |
| e3/machine.py: _step, StepResult, FragmentResult, FragmentFailure | Debit before effect, counted scratch PC, observer-only completed prefix | Real service permissions and post-effect streaming evidence; no private _step caller or fake prepayment receipt; technical interruption not biological shutdown |
| e3/kernels.py: make_scan_program, run_scan_fragment | Representation-only literal scan, independent result after S | Inline scan into controller/RESPONSE with the exact owning service scratch layout and continuation; no observer-result feedback |
| e3/machine.py: td_program, selection_program | Actual arithmetic fixtures, caller-seeded R/D | Paid record/Q loads, reward/rank capture, TD gate/store, SENSE and selection linkage |
| e3/meter.py: gate, debit, floor_quote | Current packed resources, checked c+L+T+rho | Trusted current-site quote recipes and gate dispatch; immediate scratch f3 outcome and prescribed R clobbers; no saved GateResult capability |
| e3/meter.py: deposit, debit_and_deposit, passive_grant | Typed cap/deposit arithmetic | One-shot live packet ownership, prior attempt/transport funding, TICK exception, original flow events |
| e3/protocol.py: parse_frame, encode_frame, FrameCodec | Exact structural frames and public context | Streaming partial-I/O framing, session/order/direction/duplicates/live-site/cap checks; distinguish wire errors from paid semantic BAD traps |
| e3/state.py: State, Scratch, reset; meter.canonical_activation | Exact raw state, local canonical reset/activation | Sole runtime state adoption, drop serialized input copy, cancel actual process/pipe/ownership contexts; full-source reset evidence |
| e3/upkeep.py: make_upkeep_program, _body_cost, run_upkeep | Newly present real outer-M minimum plus fragment C/access/kernel/S for ISOLATE and both AGE services | Integrate fixed services into live BEGIN/EXIT and linked ROM; derive public T from the actual calendar; CONDITION remains absent |
| e3/physical.py | Placement, prices, codecs, simultaneous physical transition | Paid AGE/CONDITION services; scheduler keeps faults outside operation; code-write permissions are not generic RAM exclusion |
| e3/policy.py; e3/arithmetic.py; e3/coding.py | Pure reference selectors/arithmetic/codecs | Paid ROM only, not free calls from a worker; scorer-side task_return remains outside |
| e3/inputs.py | Indexed HMAC input law, explicit keys, no root generator | Private owner, CNG provenance later, current-scalar adapter; never preload into worker |
| e3/archive.py: PrimitiveEvent, commit_trace, records | Pure codecs and supplied-stream commitment | Original runtime event production, external counter/hash ownership, writer/completeness checks, independent replay; no archive objects in worker |

Program immutability proves neither target independence nor service admission.
A host caller can currently construct any structurally valid literal ROM, even
one embedding a target. The production binding must select only the trusted
prospectively configured catalog, never accept an encoded Program, source,
module path, callback, caller-supplied quote table or target-dependent registry.
Keep arbitrary-program APIs for component tests outside the launch boundary.

The current machine enum is not the selected 16-byte archive ROM record ABI.
It uses auto-valued opcode enums, separate compare variants and fragment-only
operations. Do not serialize its enum values as frozen ROM opcodes. The explicit
descriptor/lowering/link encoder and its round trips remain implementation work.

## Next complete paid services

Start with no-scalar services to close real admission/accounting before dynamic
transport. The initial recommendation was ISOLATE, then AGE_LOW/HIGH and all
twenty CONDITION entries. Final inventory changed that order: reuse the newly
present ISOLATE/AGE paid wrappers, close their runtime boundary, and implement
CONDITION next rather than recreate existing work. Their literal witnesses are
adopted in v0.9/v0.11; these are not new scientific designs.

run_upkeep validates public service, exact State/Scratch, immutable explicit T
and clean entry. It builds generic ROM at base zero, quotes the entire mandatory
body, and passes that same body as minimum_exit to meter.gate. Thus its initial
minimum includes M plus the entire body plus T plus residue. Only after actual
M admission does machine.execute pay C and the fixed body. Optional rejection
is impossible for this fault-free branchless construction; the full minimum
funds all prefixes even though fragment per-step L retains only S. That specific
inductive funding argument is legitimate, not a general complete-L engine.

Remaining limits are explicit: caller-derived T, no schedule/header validation,
no CONDITION/TICK/scalars, no linked frozen entry offsets, no full original
primitive archive or process custody. The local UpkeepStatus is not a wire
EXIT/SHUTDOWN certificate. Dirty scratch fails before payment and is not freely
cleared. Do not confuse the complete fixed mandatory-body preflight with
arbitrary external gate receipts or composable multi-region continuations.

| Service slice | Frozen behavior and acceptance target |
|---------------|----------------------------------------|
| ISOLATE | Outer M128, C256, 59 CONTROL, 52 paid zero writes to lanes 848..899, S8; total 1120 energy, 13 material/source; zero scalar or RAM read |
| AGE_LOW / AGE_HIGH | Ten literal ages each; 63 CONTROL, 20 READ2, 80 kernel ALUs, 20 WRITE2, M/C/S; 952 energy and 5 material/source each; all 16 raw age encodings saturate correctly |
| CONDITION d | Outer M/C, nested M, then paid 4-energy/domain-source dues and two dedicated zero writes only if admitted; rejected 520 energy, admitted 552, body vector b(d) from cross-hub lane placement; 5/9 CONTROL |
| TICK | PASSIVE exception, M, exactly five charged grant occurrences, retained accepted-P transport, LIVING16, RENT20, S; no CONTROL; 177+sum accepted P energy |
| ADMIT | Five slot entries; rejected M/S=136 with no cue; admitted M/C/cue/four writes/S=449 energy and 1 material/source; 11 CONTROL |
| BLOCK_LESSON / REP_LESSON / COMMIT | Paid teaching capture; block staging merge; REP cell-write gates; block encoding and mandatory staging retirement; no pristine-code or teacher-success latch |
| RESPONSE | Five slot entries and learning/frozen/assay/recovery variants; paid raw slot read, DECODE gate/scan/optional guess/output, authorized dynamic feedback, record finalization, slot retirement, S |
| TERMINAL | Paid record reads, eligibility and TD gate, optional paid Q update, mandatory sixteen clear writes; mandatory 904 energy/4 material-source vector, full 1121/6 vector |
| CONTROLLER | Whole CT-corrected service: outer M, both C envelopes, DECIDE, paid offer/scan/SENSE, old record/TD, rank selection, ACTION/repair prefixes and store; no reference helper substitutes |
| TEMPLATE and scripts | Capability-specific oracle entries and genuine script bookkeeping/padding from v0.10/v0.11, after ordinary runtime works; not final eligibility |

### Gate and suffix construction

Quotes are derived internally from the admitted immutable G, current public
header and already-paid scratch predicates. Never accept L/T from the external
worker caller. Backward DAG sums with componentwise maxima give the local
mandatory suffix, omitting already-paid M/C and promoting an admitted optional
body into L. An unknown cue/address requires maxima over all possible encodings
for energy AND each source, before any discovery. No pooled material average.

T includes only later mandatory services on the fixed public calendar. For
AGE_LOW, T contains AGE_HIGH (952;5,5,5,5), twenty CONDITION minima (10400;0),
and scheduled TERMINAL minimum (904;4,4,4,4). For CONDITION d, T contains
(19-d)*520 energy plus that TERMINAL minimum if scheduled. Earlier ADMIT retains
all upkeep (12304;10,10,10,10). Conditions do not promise later optional TD or
conditioning. Retain positive energy residue 1; final leakage is separate.

For CONDITION after nested M, L is S8 on rejection; admission promotes
(32;b(d)) plus S. After dues, retain both writes and S; after the first write,
retain the second and S. There is no mid-operation fault or unpaid retry.
An optional rejected gate retains its actually paid fee and takes the selected
paid exit path. Minimum failure alone sinks remaining E and returns actual
uncleared persistent state as SHUTDOWN, discarding terminated scratch without
claiming paid S. A malformed packet, exception, process crash or wrong quote
is technical FAILED/PARTIAL, not synthesized death.

The full executor cannot delegate successive live regions to execute(): that function
prepays envelopes and terminates at S, so repeated fragment calls would erase
live scratch and double-pay or bypass admission. The new upkeep wrapper's one
fully prefunded fixed operation is a narrower valid composition, not that
successive-region shortcut. Retain one operation-owned
dispatch loop. Its only modeled continuation is Scratch PC; the initial typed
entry/M dispatch is public operation machinery, followed by the priced entry
instruction. There is no host saved PC, recursive program counter, call stack,
success latch or reusable prepayment token. Static path proof, not an acquired
fuel counter, bounds instruction steps; transport occurrence counts belong only
to the trusted monitor and cannot feed execution decisions beyond rejection of
invalid transport.

## Sequential transport and dynamic ownership

### State machine and frame limits

Keep the frozen five ABI-9 kinds, not a new JSON RPC or serialized Python object.
Fresh process starts UNBOUND; exactly one valid BIND selects a trusted catalog G.
READY accepts one BEGIN from the trusted fixed scheduler; ACTIVE executes that
service to one paid EXIT or physical SHUTDOWN. READY cannot accept SCALAR;
ACTIVE cannot accept BIND/nested BEGIN. A fixed finite sequence of completed
operations is permitted within one ownership context. Technical failure closes
the invocation; it is not resumable via an ACTIVE object or partial scratch.

The 3-byte header declares exact kind-specific payload sizes: BIND 8, BEGIN
284, SCALAR 6, EXIT/SHUTDOWN 276. The largest frame is 287 bytes. Check kind and
length before allocating payload storage. Loop on short reads/writes; reject EOF
inside a frame, noncanonical width/range, wrong direction and trailing/extra
frames. Use binary raw or exact bounded reads, not text, read-all, line parsing,
pickle, communicate(all_operation_inputs), or a preloaded packet list.

Separate transport errors from width-valid semantic traps. In particular the
current contextual codec rejects a nonaligned BLOCK TEMPLATE cue or a nonbit
REP TEMPLATE payload, but the owning interpreter must take the selected paid
BAD path after admission/capture. Do not run that convenience semantic check
as a free pre-admission gate or erase the paid prefix. Structural malformed
frames remain technical failures; neither case fabricates a biological death.

The public BEGIN validator is not a trusted caller proof. It cannot detect a
target-dependent choice among otherwise legal headers, schedule-skipping,
duplicate operations or an externally rewritten state. The boundary supervisor
must bind the actual planned sequence and last completed state, applying only
selected physical/experimental transitions between operations. No arbitrary
client may select the header, G, state replacement, support, retry or stopping.

Read one SCALAR only at its enabled immutable primitive site, debit its selected
price before exposing the value, validate its exact tag/direction and consume
once into the named R/D destination. Drop frame/input copies after use. Carry
only values in the selected scratch layout across instructions; no generic
pending-values dictionary, queued future replies, stored generator, token or
closure containing acquired values. An ephemeral I/O frame is transport, not
another interpreted register or reusable receipt.

Enforce both per-site uniqueness and the frozen service/path maximum: RL
resource/scrub 8/6, fixed resource/scrub 5/3, learning RESPONSE 4, frozen ecology
3, assay/recovery 2, TICK 5, ADMIT 1, LESSON/TEMPLATE 2, other services 0.
Direction follows tag: ACTION_REQUEST and RESPONSE_BIT are emitted, not inputs.
A repeated legal scalar remains invalid despite passing FrameCodec. A runtime
probe confirmed repeated matching BIND and OFFER pass the present codec alone.

### Host adapter versus worker protocol

The frozen wire does not contain an arbitrary REQUEST, ACK, TRACE, REPLAY or
continuation kind. Therefore adding such a worker frame to solve interactive
I/O would be a protocol change, not existing implementation. Choose a trusted
host adapter with private transport mechanics and no new interpreted input:

1. Stream original post-effect execution observations out on a distinct one-way
   host channel. They expose the actual paid gate result and counted next PC
   to the external monitor, never to interpreted instructions.
2. The monitor derives the next permitted scalar site from that PC, immutable
   G, paid admission and public header. It supplies at most the one authorized
   scalar frame. The child calls a fixed synchronous exact-read routine only
   at that site and performs its scalar debit before consumption. There is no
   application buffer of later payloads. Bytes waiting in a bounded OS pipe
   are transport, not worker-addressable storage.
3. If an implementation needs a read-readiness control token instead, specify
   and test it as host-only framing on that separate channel. It must be
   derived from the same site, carry no acquired payload/capability, never be
   a model-visible scalar or saved proof of payment, and never let the wrapper
   call an arbitrary worker helper. This is a residual transport decision to
   close in implementation, not a sixth ABI kind already approved.
4. The final-image runtime records original before/after stocks, scratch and
   effects. An external collector supplies archive phase ID, source/G digests,
   truth and generation-attempt metadata, serializes the selected 192-byte
   PrimitiveEvent and streams its hash. Those fields do not return to the child.
   A write-only redirected stderr can carry a fixed binary observer envelope;
   it must not mix arbitrary diagnostics into the ABI stdout or block on an
   undrained log. The envelope and cross-channel ordering require validation.

This monitor is not a second agent or free reference decoder. Its observations
cannot choose policy, branch, grants, input indices or scientific stopping.
Do not compute outputs in the supervisor then label a child codec round trip
as paid execution. Transport acknowledgments/backpressure are not simulated
time, energy, scalar opportunities or additional paid steps. Do not retain a
host event history inside the child; current-instruction audit temporaries are
write-only and promptly released. Active observations do not become checkpoints.

SENSE is a special trusted physical primitive: sample actual E/local P AFTER
its full sensing debit, then deliver its two encodings with no additional
encoding charges. Any host bridge must use those current sampled quantities,
not stale BEGIN stocks, free supervisor sensing, or another stock mirror in
the worker. TICK PASSIVE is the sole grant preflight exception; its five offered
occurrences and accepted-P scratch fields must be reconciled without double
deposit, a sixth scalar, or five retained uncounted packets. Both bridges need
explicit original-event/one-shot tests before their service is accepted.

### RESPONSE cannot be batched into a precomputed call

The current scan ABI is controller-shaped: cue D64:4, usefulness D68:1, saved
base D69:7. RESPONSE instead retains raw slot D64..71, valid lane D72..73,
cue D74..77, output D78, valid predicate D79 and signed b D80..95. A direct
call to run_scan_fragment is wrong: it overlaps live fields, clears scratch
at S, and returns a host summary instead of continuing the paid service.
Inline/relink the shared elemental scan template with the selected operands;
do not reconstruct these fields from an observer result.

The worker obtains its actual possibly corrupted cue only by paid slot reads.
The private evaluator keeps the ORIGINAL due cue and target separately. Once
the worker pays and emits RESPONSE_BIT, the wrapper evaluates that emitted bit
against the original due target and branch usefulness. Only at enabled RF sites
does it deliver current ECOLOGY_YIELD (0/64), then current LEARNER_RETURN
(-64/0/64) when learning is permitted. The current response must not accept a
precomputed current b before emission or use the corrupted cue as scoring truth.
Prior task return already stored in the record may influence the next TD step.

Assay/H1/recovery get neither feedback packet, not two zero packets. Spurious
emissions get no feedback. Invalid slot or rejected decode still follows paid
record finalization with locally initialized b=0 and mandatory slot retirement;
no guessed result becomes a correction input. Empty/tied admitted scans alone
enable GUESS, before the paid output. Validate unique/guess, valid/invalid slot,
valid/invalid record, due/spurious, learning/frozen and all five slots.

## Feasible nonadversarial runtime boundary

Use a fresh Windows CreateProcess-backed subprocess per ownership context.
Start with one operation per child for lifecycle validation; later reuse a
child only for a fixed sequence of completed S operations in that same context.
Never pool an old child's host memory across reset, fork, oracle revocation,
individual or history ownership. No nested halfway service or resume queue.

The supervisor resolves the existing absolute Python executable and a fixed
reviewed generic bootstrap before launch. Use shell=False, -I -B -S, binary
stdio, close_fds=True and no additional inheritable handles. Explicitly construct
the child environment from a minimal whitelist, initially SystemRoot only,
not os.environ.copy() followed by a blacklist. Print no parent environment
values. Use a fixed generic non-experimental working directory; no run/target
path, digest, lineage, secret root or callback in argv or configuration.

Preload all required trusted standard/application modules and compile catalog
ROM before processing BEGIN. -I excludes the workspace and user site, so a
bare -m e3.worker from workspace is not a solution; provide an explicit reviewed
bootstrap/package location rather than re-enable ambient path search. -S
excludes system site/.pth startup. No state-supplied eval/exec/compile/import,
pickle, marshal-code loader, plugin, arbitrary DLL or callable field is allowed.
Trusted source loading before the guard is distinct from interpreting untrusted
experimental data afterward. Do not load targets and delete them later; do not
inherit a secret-bearing parent interpreter through multiprocessing objects.

After preload, arm a deny guard for covered file/directory operations, networking,
registry, new processes, dynamic compilation/import and native loading. Test
positive normal execution and negative paths with public canaries. The guard
is defense in depth against accidental trusted-code behavior, not protection
against malicious Python or native code. stdlib/native runtime internals remain
trusted. Do not load ctypes in the worker; its absence is a dependency property,
not a proof that arbitrary memory access is impossible. Do not claim that a
socket-create guard proves every inherited socket/handle is absent.

Actual source reachability must show that interpreted instructions can reach
only state/scratch/G/header and prescribed primitives. The final process must
never contain an out-of-band target vector, secret root, due-cue history,
archive/scorer object or secret-valued environment. Acquired code/Q/raw state
and explicitly authorized teaching/ecology scalars can contain learned
target information by design; this is not a promise of zero target-correlated
bits. Reset tests must cancel that history and hold G/future Z fixed.

Process isolation with unchanged user credentials does not revoke filesystem,
registry or sibling-process access at the Windows access-token level. The probe
did not install a restricted token, AppContainer, firewall, ACL or job policy.
No claim covers adversarial native code, same-user process inspection,
side-channels, malicious source replacement or the OS/runtime itself. An OS
level deny guarantee would need a separately implemented and tested boundary.
It is not required to halt the currently authorized trusted-code implementation
because that stronger boundary is not available in the current code.

At reset close old pipes and end the ownership process, cancel references and
pending current delivery in the supervisor, construct canonical state (20 bytes
0xAA plus 256 zero bytes), and start a new child with ordinary capability and
scratch zero. Check every designated actual source before and after canonical
activation. E=0 old state is never revived. Only real S yields EXIT; interruption
restarts from a prior completed external anchor in a new context, not the dirty
frame. Observer hashes, cumulative counters and previous outputs remain external.

## Bounded validation and performance evidence

Five constructed canonical-empty scan executions per representation were timed
in the research host with actual machine.execute, not a reference decoder. Each
iteration used fresh state/scratch; ROM construction was measured separately.

| Quantity | REP | BLOCK |
|----------|-----|-------|
| Immutable scan construction seconds | 0.001061 | 0.077640 |
| Actual step count | 55 | 3764 |
| CONTROL path bound A/B | 15/0 | 44/0 |
| Actual simulated energy including C/S | 383 | 4303 |
| Five run times, seconds | 0.004905, 0.004719, 0.004539, 0.005173, 0.004728 | 0.243103, 0.253577, 0.249338, 0.285125, 0.260133 |
| Median steps/second including current validation/trace overhead | 11633 | 14844 |

These are noisy local conformance microbenchmarks, not throughput of paid
services, physics, HMAC, IPC, archive writing or replay. The combined design
has 3,320,673,872 planned outer services. A child per service at the roughly
0.26-0.31-second probe cost is plainly unsuitable for that roster; the probe
includes extra diagnostics and cannot be treated as a calibrated launch-only
coefficient. Revalidate immutable G once before acquisition, reuse within one
context, and optimize the interpreter only with exact event/state equivalence.
Never replace paid scans with pure decoder calls to obtain speed or change
simulated prices to reflect wall-clock measurements.

Keep the first implementation checks finite: one fresh context, one service,
all relevant raw encodings and prefix shortages, no corpus, no target draws,
no full engineering archive. Then measure two representations, isolated
startup separately from a fixed sequence of complete operations, trace-on/off
only where scientific execution still emits required evidence, resident/peak
memory, scalar latency and external serialization/hash overhead. Report logical
slots versus actually funded work. Use externally enforced wall-time/byte caps
as technical aborts, not energy death or outcome-selected stopping.

Executed validation records, including unsuccessful attempts:

* Design integrity: all 23 manifest entries passed using -I -B -S.
* Public process/guard probes: three completed binary round trips and covered
  operation denials, with the explicit os.stat limitation.
* Actual generic source under armed guard: both scan fragments completed,
  scratch zero, no late imports; winreg preload and indirect os reachability
  were discovered and retained as limitations.
* The combined existing machine/kernels suite ended with KeyboardInterrupt
  and exit code 1 during the 1,024-case repetition scan test. No complete-suite
  pass is claimed and the reason for interruption is not attributed to a defect.
* A reduced command mistakenly named a scan test class under test_e3_machine;
  two valid tests passed but the nonexistent selector caused one loader error.
  This was an invocation error, not a production failure.
* The corrected two-test command passed in 0.674 seconds: exact static scan
  counts/relocations and execution without pure decoder/policy/snapshot helpers.
  Test selectors should be copied from verified module/class names before use.
* New upkeep source was checked with six constructed public executions: each
  of ISOLATE/AGE_LOW/AGE_HIGH at exact full cost plus one energy and exact
  material reached EXIT, left E=1/P=0 and cleared scratch. Step counts were
  112/184/184. Removing the one-energy residue reached SHUTDOWN before any
  instruction, left P and RAM unchanged and set E=0. ISOLATE's canonical fixture
  was already clear, so its paid same-value writes left RAM unchanged.
  These six checks do not certify the whole newly present upkeep test suite.

## Evidence

* E3_DESIGN_FREEZE_v0_11.json and verify_e3_design.py: actual integrity pass
* E3_INTEGRATION_DECISION_v0_11.md: authority and next permitted execution stages
* E3_INTERFACE_CONTRACT_v0_9.md: authority inventory, exact frames, scalar caps,
  current(tag), reset ownership and original trace events
* .copilot-tracking/reviews/2026-09-10/e3-interface-review.md: IFR3 is a later
  implementation-validation obligation, not a pre-code impossibility
* e3/machine.py, e3/kernels.py, e3/meter.py, e3/protocol.py, e3/physical.py,
  e3/state.py, e3/inputs.py, e3/policy.py: inspected actual component boundaries
* e3/upkeep.py and test_e3_upkeep.py: late-arriving paid mandatory wrappers;
  source readback and six local boundary executions, no file edits
* e3/archive.py: module boundary, PrimitiveEvent, encode_trace_event,
  decode_trace_event and commit_trace inspected
* .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md:
  RESPONSE scratch/R0..R13, TERMINAL, AGE, CONDITION and L/T witnesses
* .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md:
  TICK/ADMIT/LESSON/COMMIT/ISOLATE, gate dispatch and linked-ROM conventions
* test_e3_machine.py and test_e3_kernels.py: inspected finite test coverage;
  only the explicitly listed completed checks are passes from this session
* Pylance semantic context confirmed that machine resolves meter, physical,
  State and Scratch to the inspected workspace implementations; selected
  interpreter metadata agrees with the executable runtime observations.
* [Python audit-hook limits](https://docs.python.org/3.13/library/sys.html#sys.addaudithook)
* [Python startup flags](https://docs.python.org/3.13/using/cmdline.html#cmdoption-I)
* [Windows subprocess handles and environment](https://docs.python.org/3.13/library/subprocess.html#subprocess.Popen)
* [Windows restricted tokens](https://learn.microsoft.com/en-us/windows/win32/secauthz/restricted-tokens)
* [AppContainer isolation](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation)

## Recommended next work

No additional broad literature or administrator-availability research is needed
to begin the authorized engineering implementation. The following are concrete
implementation/validation obligations, not unexplored design prerequisites:

* [ ] Integrate the now-present ISOLATE/AGE gate/C/access/S slices with internal
  calendar-derived T, actual wire failure paths and one-way original event output.
* [ ] Implement twenty CONDITION variants; extend/review existing AGE coverage
  across all raw ages, domain/source vectors, exact minima, one-short boundaries
  and every reached paid prefix. Recheck inventory first for parallel work.
* [ ] Close host-only observer framing/read-readiness ordering without changing
  the five ABI frame kinds; prove no free callback, scalar prefetch, replay
  receipt or acquired host continuation. Separately resolve SENSE sampling and
  TICK PASSIVE one-shot ownership with their selected paid tariffs.
* [ ] Implement trusted-catalog launcher/dispatcher, strict stream FSM, whitelist
  startup, final-image dependency/reachability audit, public file/network/registry
  denials and actual handle-inheritance/cancellation tests. Label security scope
  trusted-code/nonadversarial; do not mark adversarial isolation as passed.
* [ ] Inline/relink RESPONSE scan against its distinct scratch layout, then test
  output-dependent ecological feedback and all rejection/retirement variants.
* [ ] Complete remaining services, controller CT repairs, descriptor/ROM lowering,
  oracle capability and script truth tables without free pure-function execution.
* [ ] Produce original traces, external sourcewise conservation and whole-phase
  replay; test malformed/duplicate/out-of-order/extra/truncated frames, early
  scalar arrival, technical interruption and new-context restart.
* [ ] Run IFR3 full-state/actual-source reset and paired futures, including
  sixteen production bit changes, cross-block/populated/corrupt/dead histories,
  cancellation and oracle revocation. Component reset equality alone is not enough.
* [ ] Rerun the complete component suite under a declared bounded test budget;
  the interrupted command is not a pass. Measure validated backend/IPC/archive
  costs before committing to a full engineering roster or storage allocation.
* [ ] Retain engineering controls/scripts until their technical gate passes;
  retain current final prohibition unconditionally for this integrated version.

## Clarifying questions

None is needed to continue the scoped implementation. Existing authorization
covers engineering after verified design freeze, not edits during this read-only
research assignment. Protocol transport details above require an explicit tested
implementation choice, not routine user permission. A future requirement to run
hostile Python/native extensions would change the threat model and require a
different OS-enforced boundary; this investigation does not approve that scope.