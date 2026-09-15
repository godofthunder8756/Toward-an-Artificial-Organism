# AC10 results: integrated constituent ablations

2026-09-15. All 72 prospective conditions retained and audited. Every
prespecified gate passes. The broader autonomy goal remains active and
incomplete.

## What was tested

In the integrated AC9 v2 priority organism, each produced constituent was removed
or substituted for the first time **inside** the same live body that carries
acquired memory entries, W-gated renewal, C-powered execution and a B enclosure.
Protocol, gates and the engineering record were written before the first final
seed (`AC10_PROTOCOL_v1.md`, hashed in the pre-run snapshot). The `keep` arm calls
the frozen `ac9.step` object itself; all 8 inherited sources in the snapshot are
byte-identical to the AC9 controls v3 freeze.

Seeds 1300–1303, two developmental sensory histories, nine arms, 2048 ticks.

| arm | mean activity | vs keep | complete | both routes | export > 0 | died | bound entries | occupied at end | route loss tick | death tick |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| keep | 1.000 | 0.000 | 8/8 | 8/8 | 0/8 | 0/8 | 42.0 | 42.0 | – | – |
| no_W | 0.122 | −0.878 | 0/8 | 0/8 | 0/8 | 8/8 | 0.0 | 0.0 | – | 248–252 |
| no_C | 0.105 | −0.895 | 0/8 | 0/8 | 8/8 | 8/8 | 39.4 | 2.6 | 171–182 | 200–232 |
| no_B | 0.355 | −0.645 | 0/8 | 0/8 | 8/8 | 8/8 | 94.5 | 0.0 | 195–279 | 472–1153 |
| permeant | 0.225 | −0.775 | 0/8 | 0/8 | 8/8 | 8/8 | 60.4 | 0.0 | 131–145 | 226–1535 |
| no_B_retention | 1.000 | 0.000 | 8/8 | 8/8 | 0/8 | 0/8 | 42.0 | 42.0 | – | – |
| B_rescue | 1.000 | 0.000 | 8/8 | 8/8 | 0/8 | 0/8 | 42.0 | 42.0 | – | – |
| no_W_late | 0.373 | −0.627 | 0/8 | 0/8 | 0/8 | 8/8 | 42.0 | 0.0 | 599–609 | 761–767 |
| no_B_late | 0.627 | −0.373 | 1/8 | 0/8 | 8/8 | 7/8 | 43.1 | 0.0 | 647–857 | 826–1926 |

## Main findings

**1. W production is required for acquired organization to exist at all.** With
the W-producing reaction disabled, no individual ever allocates an entry
(`memory_bound` 0 in 8/8) — neither the region's writing machinery nor the
entries it enables can be created. The inherited core W endowment expires at
tick 63 in 8/8, and all eight individuals terminate at 248–252, far before the
horizon. Without W, memory renewal has no subject and no object.

**2. C production is required for continued execution.** With the C-producing
reaction disabled, conversion is confined to the inherited converter endowment
(28–33 units total, zero in every assay window) and all eight individuals die at
200–232 once usable energy runs out. The acquisition of entries begins
(39.4 bound on average) and then cannot be sustained (2.6 sites occupied at the
endpoint, routes lost at 171–182).

**3. B production and retention are required for the acquired organization, but
not for activity.** With B production disabled, every individual exports
constituents (8/8), loses both routes within 195–279 ticks and dies long after
that (472–1153). Activity over the whole horizon falls only to 0.355 because
random port sampling keeps acting after the learned routes are gone. With
retention disabled while B is still produced (`permeant`), route loss is the
earliest observed (131–145) and activity falls to 0.225.

**4. The enclosure's causal contribution is its retention function, not its
matter.** `no_B_retention` forces blocking with no B production at all: the
enclosure's matter reaches **zero boundary constituents in 8/8** while activity,
completion, entry count and route retention are indistinguishable from keep.
`B_rescue` reaches the same endpoint from the other direction, supplying matter
externally (160 units in 8/8, zero internal B births) and again retaining both
routes with zero export. Blocking and matter are therefore substitutes here, and
the function — retention — is what the acquired organization depends on.

**5. The requirement is a maintenance requirement, not only an acquisition
requirement.** Suppressing W production only after development still destroys the
acquired organization (routes lost at 599–609, roughly ninety ticks after
onset) and kills all eight individuals at 761–767. Late B loss likewise loses
the routes (647–857) and kills 7/8, though later and more variably. The acquired
organization is not a one-time achievement that thereafter survives on its own.

## Gates

All nine prespecified gates pass as written in the protocol: G1 (keep 8/8
complete, 8/8 routes, zero export), G2–G5 (each ablation's structural
condition plus mean activity at least 0.20 below keep), G6–G7 (both substitutes
restore zero export and full route retention with zero enclosure matter in the
rescue case), G8–G9 (pre-onset production present, post-onset production absent,
routes lost).

## What this establishes, and its limits

Supported, model-relative: in this integrated body each produced constituent is
causally required for maintaining the acquired organization, the enclosure's
requirement is specifically its retention function rather than its mass, and
activity is a poor proxy for organization — several arms keep acting long after
the acquired routes are destroyed, because random sampling remains viable. The
requirement persists after development, so the organization is continuously
maintained rather than created once.

Not established, and not claimed:

- No autonomous need acquisition. The priorities remain demonstrated
  permutations; these ablations remove or substitute constituents, they do not
  show the organism discovering a new dependency.
- No full autopoiesis, intrinsic normativity, subjectivity or rich
  developmental individuality.
- The acquired program bank `traces[0,:126]` was fully intact
  (`policy_accuracy` 1.000 in all 72 rows): over this horizon and flip rate the
  controller's own table is not the vulnerable endpoint that discriminates
  between arms, so these results say nothing new about program-information
  maintenance. The discriminating organization is the entry set.
- `permeant` is a compound intervention: removing retention collapses the
  constituent economy, so it does not by itself isolate retention. The
  mechanistic isolation is the single-step transport test in `test_ac10.py` plus
  `no_B_retention`, which holds function while enclosure matter goes to zero.
- Endpoints are descriptive over eight independently developed individuals
  (four seeds × two histories). Same-author engineering evidence, not
  independent confirmation.
- No external matter, energy or correct answer was supplied, and every
  conserved quantity still balances; only `B_rescue`'s labelled external input
  appears, and it is counted separately from production.

## Verification

- 21 mechanism test methods (`test_ac10.py`), including: the keep arm is the
  frozen function object and reproduces the frozen v2 rows field-for-field
  including state digests; single-step surgery isolation (the W ablation removes
  exactly the W reaction's 4 material and 2 energy, the C ablation exactly the C
  reaction's 4 and 4, the B ablation nothing else); retention-kernel and
  external-restoration semantics; complete-state erasure noninterference for all
  nine arms; exact replay; and the frozen ledger identity for every arm.
- `audit_ac10.py`: 72 unique conditions, ledger identities, assay bounds, arm
  invariants and source hashes valid; 8 inherited sources identical to the AC9
  v3 freeze.
- `replay_ac10.py`: 11/11 sampled conditions reproduce exactly, including state
  digests.
- Runtime: the whole 72-condition grid takes about 14 s on this host.

## Next experiment

The remaining listed requirement is the one this study deliberately did not
address: a controller that **acquires** the need to allocate or relinquish
maintenance resources under an intervention chosen after development, with no
protected copy and no externally fixed correct state. Closer alternatives to
exclude first: a fixed schedule matched for spending, and random or reactive
allocation given the same observation stream.

[Protocol](AC10_PROTOCOL_v1.md), [runner](ac10.py), [tests](test_ac10.py),
[data](ac10_results_v1/results.json), [audit](audit_ac10.py),
[replay](replay_ac10.py), [engineering](ac10_engineering_v1/).
