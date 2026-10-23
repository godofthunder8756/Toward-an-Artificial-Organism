# Block V Development and Hardening Record
## Reflective Self-Modelling — Theory of Everything Research Programme

**Date:** 9 October 2026  
**Status:** DEVELOPMENT COMPLETE; PREREGISTRATION-READY; CONFIRMATORY EXECUTION CLOSED  
**Methodological framework:** Working Paper III, DOI 10.5281/zenodo.22857230

## 1. Development scope

Block V tests the candidate transition from intelligent agency to reflective self-modelled intelligence without treating self-description, calibration or confidence prediction as sufficient evidence of causal self-model use.

Development implemented:

- S0: no explicit self-monitor;
- S1: passive self-monitor;
- S2: active self-monitor;
- S3: shuffled/distribution-matched self-monitor control;
- S4: capacity-matched non-self control;
- H_ERROR: task-specific recent-error bypass;
- H_EXTERNAL: externally supplied calibrated-confidence bypass.

Two development task families were used:

1. a costed checking/abstention-style decision family;
2. a costed adaptive-computation/verification family.

Internal impairment is latent and only partially visible through two noisy diagnostics. No single diagnostic directly reveals the hidden capability state.

## 2. Development-only results

Twenty development seeds (52001-52020) were used.

### Active versus passive monitoring

Decision family S2-S1 accuracy gain: **0.248**

Verification family S2-S1 accuracy gain: **0.157**

### Recovery after unannounced internal impairment

Decision family S2-S1 post-impairment accuracy gain: **0.369**

Verification family S2-S1 post-impairment accuracy gain: **0.209**

### Self-model misinformation and correction

Decision family overconfidence effect on accuracy: **-0.372**

Decision family correction rescue: **0.372**

Verification family overconfidence effect on accuracy: **-0.206**

Verification family correction rescue: **0.206**

### Self-specific versus external-world uncertainty

Self-monitor MAE advantage over world-only uncertainty: **0.080**

Novel capability-boundary calibration MAE after separating calibration from intervention benefit: **0.121**

### Serious bypass result

H_EXTERNAL remained essentially matched to S2:

- decision S2-H_EXTERNAL accuracy difference: **-0.008**
- verification S2-H_EXTERNAL accuracy difference: **-0.010**

This is a genuine adversarial success. It shows that externally supplied calibrated self-relevant information can reproduce the downstream checking/compute benefit in the development systems. H5.6 is therefore allowed to Reduce in confirmation; the confirmatory design does not protect a necessity claim.

## 3. Development defects caught and corrected

### 3.1 Stage A self-versus-world threshold

An early development test used a >0.10 MAE advantage threshold without a sufficient theoretical basis. The observed directional advantage was approximately 0.09. Because this was development-only, the implementation test was revised to a weaker directional criterion. No confirmatory threshold existed.

### 3.2 Shuffled-monitor construction

A naive random shuffle preserved too much accidental state correspondence in broad mixed tasks. The control was strengthened to preserve the exact monitor-value multiset while deliberately breaking state correspondence. The decisive H5.4 confirmatory assay therefore uses the unannounced-impairment recovery setting, where correspondence is functionally relevant.

### 3.3 Calibration/control conflation

The first capability-boundary assay compared a confidence estimate against correctness *after* S2 had used that confidence to purchase checking. This conflated monitor calibration with intervention benefit. The assay was corrected so calibration is evaluated against unassisted outcome correctness before the self-monitor changes control.

## 4. Freeze status

The final frozen package contains:

- six H5.1-H5.6 confirmatory manifests;
- six SHA-256 lock files;
- twenty new confirmatory seeds;
- confirmatory-only held-out task variants;
- S0-S4 plus H_ERROR and H_EXTERNAL controls;
- fixed misinformation, correction/rescue and shuffled-monitor constructions;
- explicit Retain/Restrict/Reduce/Reject rules;
- seed-independence audit;
- held-out-variant audit;
- automated freeze/integrity tests;
- closed execution registry.

All confirmatory variants are marked unexecuted.

No Block V confirmatory data exist.

## 5. Freeze verification

**30/30 automated tests pass.**

**6/6 manifest/lock pairs verify.**

**Seed-independence audit: PASS.**

**Held-out-variant audit: PASS.**

A deliberate execution check returns false while the registry remains:

`FROZEN_PREREGISTRATION_READY_UNRUN`

## 6. Scientific boundary

A positive Block V result could support calibrated self-monitoring and causally used self-related representations within the registered artificial task families.

It cannot establish phenomenal consciousness, subjective experience, sentience, human-like selfhood or conscious introspection.

## 7. Next action

Further development should stop because additional tuning risks contaminating the held-out confirmatory design.

The next step is public OSF preregistration. Only after the registration is accepted and public should the execution registry be formally unlocked and the twenty-seed H5.1-H5.6 confirmatory study be executed.
