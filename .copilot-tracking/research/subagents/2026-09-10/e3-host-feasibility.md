---
title: E3 bounded host performance conformance
description: Measured scan timing and observer-trace memory with conditional engineering workload arithmetic, not hypothesis runs
ms.date: 2026-09-10
---

## Decision and scope

The unchanged Python scan component is suitable for small conformance fixtures,
not yet an efficient implementation for the selected engineering roster. Improve
host interpretation and bounded observer-trace handling before considering full
engineering. No acquisition, development, recovery, assay, ecology, oracle,
SCRIPTED product, hypothesis run, target draw, private key or bootstrap was run.
The projections below neither authorize a run nor forecast its completion time.

Only [benchmark_e3_components.py](benchmark_e3_components.py) and this note were
created by this task. No kernel, machine, meter, state, E1/E2 file, contract,
manifest, dependency or existing tracking artifact was edited. No notebook,
installation, output directory or automatic benchmark report file was created.
The benchmark prints one JSON object; this note was separately authored from
the observed output. Editor infrastructure may retain terminal/tool responses
outside the workspace; that is not a benchmark output writer.

The read-only [design verifier](verify_e3_design.py) passed all 23 entries before
implementation and inside each successful benchmark invocation, then again
after validation. No failed entry or manifest repair occurred. The
[integration decision](E3_INTEGRATION_DECISION_v0_11.md#decision) authorizes this
engineering implementation test, not promotion to final experiments. Design
integrity is not an implementation-conformance certificate or source freeze.

## API and fixture evidence

The benchmark calls the actual `run_scan_fragment(code, state, scratch)` API in
[e3/kernels.py](e3/kernels.py). Its wrapper builds a generic ROM, calls
`machine.execute()`, and interprets returned post-effect events after S.
No private `_step()` invocation, free decoder, cached acquired result,
monkeypatch, validation bypass or replacement interpreter is used in timing.

Fixture construction follows [test_e3_kernels.py](test_e3_kernels.py) and
[test_e3_machine.py](test_e3_machine.py): allocate fresh State/Scratch, place
literal symbols at paid-read lanes, set D64:4 cue to zero, D68:1 usefulness to
one, and PC to zero. These are trusted test inputs, not lessons or a full body
activation. All other initial bytes are zero except the explicit energy field.

| Fixture | Symbols at selected lanes | Expected payload | Health | Observed |
|---------|---------------------------|-----------------:|-------:|---------:|
| REP clean | Five ones | 1 | 2 | 5 |
| REP single corrupt | Zero followed by four ones | 1 | 3 | 5 |
| BLOCK clean | Twenty zeroes, encoded payload zero | 0 | 2 | 20 |
| BLOCK single corrupt | One followed by nineteen zeroes | 0 | 3 | 20 |

REP reads lanes 0,4,8,12,16; BLOCK reads lanes 0..19. All four observations are
untied. No random target table or host encoding/decoding helper is needed.
Conformance checks verify actual read values/addresses, ordered PC events,
each primitive debit, envelope payment, result writes, HALT, complete scratch
clearing, positive energy residue and unchanged nonenergy persistent bytes.

Inspection corrected two hypotheses about current host cost:

* [e3/machine.py](e3/machine.py) `execute()` validates the ROM once per call and
  invokes its internal finite interpreter, not public `step()` on each site.
  `step()` would revalidate the ROM per separate call, but it is not this path.
* `StepResult` stores eight fields: `pc`, `opcode`, `charge`, `paid`, `status`,
  `next_pc`, `value`, `lane`. It does not store full State/Scratch snapshots.
  The internal list becomes a returned tuple. Both can briefly coexist.

`run_scan_fragment()` rebuilds the ROM on every call; construction itself
validates operands and the Program. `execute()` then validates it and local
bounds again. [e3/meter.py](e3/meter.py) performs checked affordability and
packed resource updates for each primitive. These are source observations,
not a profiler attribution of which operation dominates runtime.

## Commands and validation

Commands used the editor-selected CPython 3.13 interpreter, with `-B` to
prevent bytecode writes. From the workspace root, the equivalent command lines
were:

```powershell
python -B verify_e3_design.py
python -B benchmark_e3_components.py --repeats 2
python -B -m unittest test_e3_kernels.TestScanPrograms.test_exact_static_counts_bases_stage_and_relocations test_e3_kernels.TestScanPaymentsAndFailures.test_no_free_control_entry_and_failed_envelope_has_no_effect test_e3_machine.TestInstructionEffects.test_s_clears_all_scratch_and_never_writes_pc_afterward
```

The actual invocations selected the full Python313 executable path explicitly;
the final benchmark also used the absolute workspace script path. Paths and
user identity are not included in benchmark host metadata. The three named
tests were finally executed through a captured subprocess using that same
interpreter: exit 0, three tests, 0.372 seconds, OK. A subsequent imported
`verify()` returned `ok=true`, `file_count=23`, `files_checked=23`, no failures.

Additional bounded validation passed:

* AST parsing and Pylance syntax validation
* Pylance diagnostics and editor errors empty after a sequence-narrowing fix
* CLI rejects repeats 0,33,-1 and nonintegers, and rejects unknown arguments;
  every tested rejection returns exit 1 and valid JSON with empty stderr
* Help returns JSON with exit 0, not argparse's plain-text stdout
* Default 8 and maximum 32 parser paths verified with execution mocked out;
  these are not extra timing runs
* Failed design verification prevents benchmark execution, checked with a mock
* Scan-cap arithmetic checked for every permitted repeats value 1..32
* The validation process did not import `e3.inputs`

A preliminary timing invocation passed before the type-only narrowing fix.
It returned 5.432617 seconds wall, 1.062500 seconds process CPU, 18 REP and
7 BLOCK scans. Its code-level means were 4.600231 ms REP and 347.952250 ms
BLOCK. The final-revision invocation below is the reported measurement, not a
selection of whichever run was faster. The difference demonstrates host noise;
neither run supplies a confidence interval.

Terminal evidence limitations are retained: a requested rerun returned unrelated
unittest output naming a nonexistent test class; another combined command
returned a different test selection, and a multiline terminal check exited 1
without its expected result. None was treated as successful benchmark or
validation evidence. Explicit JSON benchmark output and captured subprocess
validation replaced those ambiguous responses. Initial `git status` also failed
because this workspace is not a Git repository; no Git-clean claim is made.

## Bounds and measurement method

The default `--repeats 8` and maximum 32 are workload requests, not permission to
exceed caps. For each of two REP fixtures, measured scans are
`min(4 * repeats, 31)`; for each of two BLOCK fixtures they are
`min(repeats, 6)`. Add one warmup per fixture and one single-corrupt BLOCK
memory sample. Thus an invocation performs at most 64 REP and 15 BLOCK scans,
within hard caps 64 and 16. At repeats 2 it performs 18 REP and 7 BLOCK scans:
16/4 timed, 2/2 warmups, and 0/1 memory.

A fixed 10-second admission budget covers component work after imports and
verification. It stops starting new scans and returns `bounded_partial`/exit 1
when the bounded requested sample cannot finish. It does not fill ten seconds
with extra work. It is not a preemptive CPU quota or hard wall-time guarantee:
an already-started finite scan, compilation, checks and JSON can finish after
the deadline. No unbounded worker or phase is invoked.

`perf_counter()` surrounds the actual scan API after warmups. Times include ROM
building, static validation, bounds, metering, execution, returned trace and
post-S observation. Fixture setup, checks, trace destruction and JSON encoding
are outside each sample. GC remains enabled. One separate memory scan uses
`tracemalloc` with one frame, then turns it off before throughput samples.
No batch of retained traces accumulates between scans.

## Measured host and timings

Final-revision report: `ok=true`, `status=complete`, repeats 2. Elapsed time
after script imports was 7.155796800 seconds wall and 2.406250 seconds process
CPU. These clocks differ; neither is simulated energy, and interpreter startup
before `main()` is not included. No affinity, isolation or background-load
control was imposed.

| Metadata | Observed value |
|----------|----------------|
| Python | CPython 3.13.3, 64-bit |
| OS | Windows 11, version 10.0.22631 |
| Machine | AMD64 |
| Processor | Intel64 Family 6 Model 170 Stepping 4, GenuineIntel |
| Logical CPUs | 14 |
| Performance-counter resolution | 0.0000001 seconds |
| Execution | Serial, bytecode writes disabled, GC enabled |

| Fixture | Timed scans | Mean ms/scan | Median ms | Min ms | Max ms | ns/instruction |
|---------|------------:|-------------:|----------:|-------:|-------:|---------------:|
| REP clean | 8 | 6.654600 | 6.465500 | 5.875100 | 7.653700 | 120992.73 |
| REP single corrupt | 8 | 6.122988 | 6.445800 | 4.276200 | 7.022600 | 111327.05 |
| BLOCK clean | 2 | 419.046000 | 419.046000 | 409.031300 | 429.060700 | 111329.97 |
| BLOCK single corrupt | 2 | 380.801600 | 380.801600 | 358.892600 | 402.710600 | 101169.39 |

The ns/instruction column divides the entire API time by returned instruction
count. It is not a native CPU instruction timing or isolated interpreter-step
latency. Samples are too small and noisy to attribute clean/corrupt differences
to input content.

Raw timed samples, seconds, rounded to nine decimal places:

```json
{
  "rep_one": [0.006402300, 0.007444500, 0.006240900, 0.005875100, 0.007000900, 0.006090700, 0.007653700, 0.006528700],
  "rep_one_single_corrupt": [0.006806400, 0.006515100, 0.004276200, 0.007022600, 0.006637800, 0.006376500, 0.005187100, 0.006162200],
  "block_zero": [0.429060700, 0.409031300],
  "block_zero_single_corrupt": [0.402710600, 0.358892600]
}
```

One cold ROM build took 2.854600 ms REP / 134.417300 ms BLOCK; one additional
validation took 1.739900 ms / 62.860500 ms. These single measurements are not
steady-state rates and are not subtracted from the API samples.

## Literal instructions and simulated charges

| Quantity per successful fragment | REP | BLOCK |
|---------------------------------|----:|------:|
| Kernel ALUs | 34 | 3699 |
| READ2 instructions | 5 | 20 |
| CONTROL instructions | 15 | 44 |
| S instructions | 1 | 1 |
| Actual returned instruction events | 55 | 3764 |
| Kernel plus routed-read energy | 119 | 4039 |
| Actual CONTROL-envelope energy | 256 | 256 |
| S energy | 8 | 8 |
| Total fragment energy | 383 | 4303 |
| Initial fixture energy | 384 | 4304 |
| Residual energy | 1 | 1 |

Each READ2 costs 17; kernel ALUs cost one; CONTROL events cost zero individually
because the actual C256 envelope was prepaid. All material vectors are zero.
Both clean and corrupt cases pass the same counts. These are standalone
fragments, not complete RESPONSE or CONTROLLER tariffs. M128, DECIDE, scalar
admission, controller closure, full-service suffixes, writes and upkeep are
outside this benchmark. No omitted charge is claimed to be free in a service.

## One BLOCK trace and observer memory

One single-corrupt BLOCK scan ran with `tracemalloc`. Its instrumented wall time
was 3.132941600 seconds and is excluded from all projections. Memory units in
this section are literal bytes, not serialized record sizes or process RSS.

| Measurement | Bytes |
|-------------|------:|
| Current baseline immediately after tracing starts | 0 |
| Fixture plus held before-State/Scratch snapshots | 1028 |
| Current after API, result retained | 1133060 |
| API current allocation delta | 1132032 |
| API traced peak | 2132748 |
| API peak above fixture baseline | 2131720 |
| Current with result plus before/after snapshots held | 1133490 |
| Recursive unique-object size of `FragmentResult` | 775036 |
| Recursive size of complete `ScanFragmentResult` | 775176 |
| Recursive size of result plus four snapshots and tuple | 776004 |
| One `StepResult`, shallow | 96 |
| Returned 3764-element steps tuple, shallow | 30152 |

The trace graph contains 14785 distinct identities, 3764 actual step records
and one envelope record. The complete scan result adds the observation and
wrapper, reaching 14788 identities; the result-plus-snapshots tuple reaches
14793. Approximate recursive size uses `sys.getsizeof`, a set of visited IDs,
and only builtin leaves/containers plus the known frozen trace dataclasses.
Enums are shallow leaves. No filesystem/module graph, arbitrary `__dict__`,
private buffer traversal or `sys.path` alteration is involved.

The only full raw snapshots are four observer boundary copies with payload
lengths 276,32,276,32. There are zero per-instruction full snapshots. JSON
contains their entire hex encodings and the post-S observation. The exact
contents can also be stated without long hex strings: all bytes zero except
State-before byte 0=1, byte 225=208 and byte 226=16; State-after byte 0=1 and
byte 225=1; Scratch-before byte 8=16. Scratch-after is all zero. Byte indices
here are zero-based data offsets, not source lines. Pre-S payload zero and
health three come from returned write events, not a pre-S RAM snapshot/hook.

The fixture, before copies, after copies and original returned result remain
held when memory is read. Checks and recursive sizing occur after tracing is
stopped. Traced current/peak include different allocations than reachable-object
sizing: temporary ROMs, allocator reuse, caches and preexisting shared integers
prevent equating the two. This is not a leak measurement or an additive marginal
ownership estimate. Tracemalloc does not measure all native memory or RSS.

Keeping one returned trace is manageable. Naively multiplying 775036 bytes by
84492800 hypothetical BLOCK scans gives 65484961740800 bytes, about 65.5 TB,
of non-deduplicated trace attribution. That is not measured resident memory or
an archive prediction; shared leaves and bounded disposal change storage.
The selected archive does not require retaining Python opcode objects for
every scan, much less full State/Scratch copies per instruction.

## Selected engineering workload arithmetic

Sources are the selected [evaluation v0.8 counts](E3_EVALUATION_CONTRACT_v0_8.md#exact-logical-counts-and-conservative-physical-bounds),
[script additions](E3_CONFORMANCE_CONTRACT_v0_10.md#script-resets-rows-and-separate-archive-allocation),
and [integrated extension](E3_INTEGRATION_DECISION_v0_11.md#exact-ac-04-catalog-extension).
Do not use the superseded v0.7 workload or combined final-plus-engineering total.

There are 64 engineering cells. Per cell, T=400, H=496,
P+J+D=200+200+6=406, K=536 and conservative canonical reset roster R=400.

$$
F_{core}=64[2043(400)+256(496+406+400)+507(536)]+8192
=91033088.
$$

$$
F_{scripts}=512(507)+256(256)=325120,
\qquad F_{engineering}=91358208.
$$

The oracle contributes 8192 once. Script ecology contributes 259584, and
script reset futures 65536. Thus each code has 45679104 logical due responses.

$$
C_{core}=64[2048(400)+128(496+400)+512(536)]=77332480,
$$

$$
C_{scripts}=512(512)+256(128)=294912,
\qquad C_{engineering}=77627392.
$$

Half gives 38813696 controller offers per code. These are offered service
slots, not already-funded executions or completed controller traces.

Core canonical negative futures already contribute 6553600 response slots,
plus 65536 script reset responses. They are included once in the logical roster,
not another full continuation per source reset audit. The core 400 G roster may
contain exactly coincident configurations with multiple logical references;
actual continued counts resolve to one representative per exact allowed
G/input class after reset/equivalence checks. No blanket subtraction of thirteen
million presumed duplicates is supported by these selected engineering formulas.
There is no actual winner map, manifest union or physical execution count here.

### Explicit hypothetical full coverage

Assume every due slot is valid, every offered controller reaches its scan, one
scan occurs per response and controller, and each representation uses the
equal-weight mean of its two observed fixture means. Then per code:

$$
N_{scan}=45679104+38813696=84492800.
$$

| Representation | Assumed scans | Fragment steps | Mean seconds/scan | Conditional days |
|----------------|--------------:|---------------:|------------------:|-----------------:|
| REP | 84492800 | 4647104000 | 0.006388793758 | 6.247767 |
| BLOCK | 84492800 | 318030899200 | 0.399923799967 | 391.095852 |
| Sum | 168985600 | 322678003200 | Not pooled | 397.343619 |

The response-only version of that same assumption is 214.814760 days. These
are naive serial scan-cost illustrations, not lower bounds, upper bounds,
worst-case runtimes, necessary actual instruction counts, or predictions of
engineering execution. Positive all-slot coverage is an assumption, not an
observed outcome or proof of full critical-path/controller closure.

Death, invalid due slots, rejected service paths and proved canonical sharing
reduce scans. Teaching, full control, repair, resource/age upkeep, random faults,
process transport, replay and archive work add unmeasured cost. Standalone C/S
and per-call ROM construction need not match future fused full services.
Therefore omitted costs do not turn the scan illustration into a lower bound
on the real product. The 91-million raw planned rows remain required logical
coverage; they are not a promise of 91-million physical decode executions.

## Next engineering work

Keep this reference implementation and its bounded fixtures as the semantic
oracle for host optimizations. First profile bounded constructed inputs, then
evaluate immutable generic-ROM reuse, compiled validation metadata and a
faster interpreter. Cached validation must preserve malformed-ROM rejection
and trusted-boundary rules, not convert prior observations into worker state.

Evaluate one-way streaming trace commitments or packed bounded trace buffers,
with exact replay evidence and no feedback into execution. Preserve original
executed-path/debit/scalar commitments and selected compact raw records; do not
drop mandatory observations to make a benchmark faster. The
[sparse archive contract](E3_EVALUATION_CONTRACT_v0_8.md#sparse-checkpoints-and-complete-compact-raw-records)
requires reconstructable/checkable internals, not resident lists of all steps.
API/lifetime changes need independent conformance tests before replacement.

Numba or a C-compiled backend are possible later host implementations, not
installed dependencies or assumed speedups here. Any backend must preserve
exact widths, overflow/rejection behavior, per-source debits, paid prefixes,
scratch clearing and observer noninterference. Faster host execution must not
change simulated instruction tariffs or forgive work. No full engineering or
final launch is the next action on the strength of this timing note.

## Source identity at validation

These SHA-256 values identify observed source bytes, not an additional freeze:

| Source | SHA-256 |
|--------|---------|
| [benchmark_e3_components.py](benchmark_e3_components.py) | f2b573dcc1f5bd3df6a379e82d754639d14319adfb33c55b429795e57cb2a162 |
| [e3/kernels.py](e3/kernels.py) | 117e7cb7bd9aa83d16e249378e5227f27e0452e3dc5c63d243fc19eeac3a242d |
| [e3/machine.py](e3/machine.py) | 9cadee31b375011a3f15ca69aea4efeda7905114f325da4053969422bcf43645 |
| [e3/meter.py](e3/meter.py) | ff86f9793e53d471d4fbeff0f8305af60d34b524f8c0deedc2c321e335976212 |
| [e3/state.py](e3/state.py) | d23b78e26a5800857e3646c7942c35868790f12d3d801418c41cff231d92996c |
