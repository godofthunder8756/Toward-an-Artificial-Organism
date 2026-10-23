# W-REL bounded exact check — implementation manifest

This file is the freeze. World parameters, thresholds and procedures are the ones in the spec FINAL. They are not retuned from results. The spec file is byte-identical to the approved FINAL; its §8 placeholders are left as they stand. Identifiers completed at this freeze are recorded here, not inside the spec.

## Identifiers

- Spec file: `c4_reliability_exact_check_spec_FINAL.md`
- Spec SHA256 (authoritative): `ae626b65cae383121e6a902fe79c119b90ff46ffb8fe7cc39fafe27fc502adef`
- Admission v3.2 SHA256: `f35b6f9d1aa9ce67dd359ec74be2d8ffb5c58085aedf2599da46d56100884207`
- Approval record SHA256: `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`
- Approval: Aidan Ahern, 2026-10-21, 8:58 AM ET. Verbatim answer in the approval record: "Yes, approve the theory-only study".
- Freeze commit: the git commit that adds this manifest. That commit SHA is not written into this file.

## Frozen item order (spec §5.1)

1. ITEM-1 A-SYM
2. ITEM-2 VALUES-H0
3. ITEM-3 VALUES-H1
4. ITEM-4 CONF
5. ITEM-5 CG
6. ITEM-6 MF
7. ITEM-7 PM
8. ITEM-8 A-SEP
9. ITEM-9 REPLAY

## Exact run command

Working directory: `c4_reliability_exact_check_v1`

```text
python3 -m wrel.run_all
```

One CPU process. No GPU. No neural network. Caps: 4 hours total wall clock, 1 hour per named item including retries, 8 GB resident memory. Exact rational arithmetic. Horizons and grids are not shortened in place. Outputs: `outputs/ITEM-1.json` through `outputs/ITEM-9.json` and `outputs/SUMMARY.json`.

## Contract

- Thresholds are the spec §4.6 constants. No margin, donor rule, cost, rate, horizon or variant is changed after seeing a result.
- Study rates, the study cost grid and the study hazard are referenced only in `wrel/run_all.py`. They are not executed by import.
- If a quotient map or a decoder is not a function, the run reports UNRESOLVED-DESIGN or NOT EVALUABLE. No ad hoc transition or decoder extension is applied.
- ORIGIN, ROLE and REDUCTION stay separate. This check does not edit a ledger and does not state a C4, consciousness or sentience conclusion.

## Pre-freeze executions (toy inputs only; none is an ITEM quantity)

All of the following use noise rates S = (1/7, 1/9), E = (1/9, 1/7), hazard 1/6, unless a line says otherwise. None uses w = 1/20, e = 1/5, h = 1/20, or the study cost grid {1/100, 1/50, 1/25} × {3/50, 1/10}.

- `python3 tests/test_toy.py` at cost (1/8, 1/3). The file also builds a PM closure at cost (1/11, 1/4) with donors (0, 0), and compares the MB pattern on a forced-RECHECK policy at cost (1/8, 1/3). That forced policy is not an optimal controller.
- One-off probe: `evaluate_pm` on the same toy world, cost (1/11, 1/4), machine donors (0, 0).
- Timing probes: `cg_forward` at T = 8 and `mf_forward` at T = 3 and T = 4, toy world, cost (1/11, 1/4).
- Horizon-prefix check: H0 solver at T = 6 against a T = 3 solver, H1 solver at T = 4 against T = 2, CG prefix values, and the replay H0 value against the T = 6 solver, toy world, cost (1/8, 1/3).
- Earlier implementation-session probes, same toy world and cost (1/8, 1/3): H0 timing at T = 10, H1 timing at T = 5, ITEM-1 at history length 3, PM closure at T = 3 and T = 4.

No study-rate quantity was executed before this freeze.

## File hashes

The runner refuses to start if any line below no longer matches the file.

SHA256 c4_reliability_exact_check_spec_FINAL.md ae626b65cae383121e6a902fe79c119b90ff46ffb8fe7cc39fafe27fc502adef
SHA256 c4_reliability_assessment_admission_v3_2.md f35b6f9d1aa9ce67dd359ec74be2d8ffb5c58085aedf2599da46d56100884207
SHA256 c4_reliability_APPROVAL_RECORD.md be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687
SHA256 wrel/__init__.py c885a13c50c88bff07f01bc1689c1fbc365ee220a24368f2ccdd2e51efc5d00b
SHA256 wrel/util.py fb6e90009996bdb096af368c54e2be8e908cc94aa10717aab93011a31cc1b019
SHA256 wrel/world.py d171a774f03b615910408223235b35708241048372fcaf86819edde1af9e18d7
SHA256 wrel/mb.py 28043859a87725f01fc653edabbf0702921029aa7aa8cd8c065c5c8759a470f2
SHA256 wrel/labels.py 9c01f0639269735a30225daa92dd1d243b15e21eb8f9877df3ac0d08767a42c2
SHA256 wrel/item1.py bc6ae605c33af702bd9a45d6fe711b6f80178dc977f60a9c79d2e14a660735ea
SHA256 wrel/pm.py 8baf7b838d9ac0dbae65a87c231203d9d43e5421607ec090e6d046a5883d76ea
SHA256 wrel/agents.py d80a54c8caed776b77ceca6a6ec1bd183b6effd7401676ed6e5f5a0baa053ce1
SHA256 wrel/sep.py cb41128f6c3018e5038a0f899834fff7c1f77d8424f1ea53f14c11abbb7c96ab
SHA256 wrel/controls.py 7caaee02f8f13feb132fd5bea9a25237d57352d6ac2ed1ae49f096ae4fc5bae3
SHA256 wrel/replay.py ffc96591cca4538477166d0c7d4257315037420d296c402fc639b36789fb6ac8
SHA256 wrel/run_all.py a42c39ddfe773870dab48923eda570f061c2f8815ede895840ad2b3cb4ecc129
SHA256 tests/test_toy.py 67bd1ed727c86b1499d6c4b613b6455683c81fa73aa45fb9e16a786f729a3701
