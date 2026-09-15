# AC4 integrated boundary engineering protocol

Before results, 2026-09-14. Preserve AC1–AC3 and transport evidence.

Integrate transported W/C with 20 expiring perimeter constituents B. The
interior is the transport kernel's 5x5 chamber. Only interior W can catalyze
writes/production; only interior C converts fuel. Exterior particles can return;
exported or expired particles cannot act. W has four tagged groups of four
slots, C four slots. Tags specify substrate specificity, not fixed positions.
The interior reaction medium, fuel/material/energy stores and anchored memory
scaffold remain supplied. W access to its tagged memory bank anywhere inside
is a well-mixed-interior approximation; this is not microscopically local DNA.

W/C lifetimes and costs follow AC3 (64/128 ticks, 4M+2E/4M+4E). W daughters
are born at an interior parent's position; C uses interior W of tag zero and
is born at that W's position. Expired and exported slots are recyclable empty
capacity, not retained active constituents. Every exported W/C exports 4M.

Each B occupies an explicit perimeter link, binds 2M, lasts 256 ticks. The
initial 20 B lifetimes are 128+6*i for i=0..19. Action8 replaces the oldest
accessible B if its lifetime<=64; accessibility requires interior W within
Manhattan distance one of that link's interior endpoint. Replacement costs
2M+2E and discards an existing B as 2M waste. At most one replacement/action.
Missing B reflects nothing; no death threshold depends on B count. B rescue
externally resets all expired links to 256, with imported bound matter counted.
Retention rescue imposes reflection without producing B, explicitly external.

The damaged controller encodes 512 four-bit decisions in two 1024-bit banks;
two further banks carry payload. Seven replicas per bit, majority repair,
32-write cap, eight writes per interior W. Observation adds B-low (minimum
life<=64) to AC3 flags. Demonstrated priority: fuel, M, W, C, B, damaged banks
in acquired permutation, rest9. Policy family remains 24 permutations.
Demonstrations are acquisition, not autonomous discovery of needs. No protected
maintenance override is permitted. Unused actions10–15 rest.

Tick: corruption, age W/C/B, export expiry waste, optional B rescue, transport,
count/retire exported W/C, convert fuel, decide and pay. AC3 reservoir capacities,
imports and living/write costs remain. Initial positions are random interior;
same seeded proposals/flips across paired arms. Dead runs freeze.

Predeclared grid: seeds0–3, 2048 ticks, copy-flip p=.00005/.0001, six arms:
self, no_B, no_B_rescue, no_B_retention, no_policy_write, protected. Blocked B
attempts are free. Protected arm uses explicit observer policy only. Both rescue
arms block internal B production. No tuning after results in this version.

Report all48 rows: activity, policy/payload accuracy, W/C/B births and losses,
exports, writes, fuel/energy/material balances and source snapshots. Required
tests cover B production cost/locality, exterior inactivity, live-state erasure,
protected-policy rejection, expiry/export accounting and sampled exact replay.
Engineering success requires self mean activity>=.9, all self final policy
accuracy>=.99, every self individual >40 B replacements, positive self-minus-noB
activity contrast>=.2, and both rescues mean activity>=.9. Retention rescue may
keep activity while failing information; report that separately. Failure is
evidence, not permission to silently tune the gate.

No claim of full autopoiesis: geometry, memory scaffold, reaction recipes,
substrate selection, sensing/interpreter and demonstrated needs remain supplied.
