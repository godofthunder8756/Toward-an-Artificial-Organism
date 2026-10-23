# Changelog — Zenodo 22863692 Publication Candidate RC1 → RC2

**Reserved DOI:** `10.5281/zenodo.22863692`  
**Scientific version:** v1.0  
**Publication candidate:** RC2  
**Publication state:** `NOT_UPLOADED / NOT_PUBLISHED`  
**Novelty status:** `NOVELTY = UNADJUDICATED`

This changelog defines the bounded remediation delta from the preserved RC1 publication candidate to RC2. It is not a publication receipt and does not, by itself, certify that the RC2 build passed verification. Final completion is established by the RC2 human-review receipt and final SHA-256 manifest.

## Immutable RC1 baseline

RC2 does not overwrite, reinterpret, or replace the historical RC1 objects.

| RC1 object | SHA-256 |
|---|---|
| `SITC_CAUSAL_ASSAY_v1.0_EN.pdf` | `26236bfdbd053d1317902b31fe000e988fe73f3a874f119657528bdf8f2a685e` |
| `SITC_CAUSAL_ASSAY_v1.0_HU.pdf` | `5c215ca3fa84fdde99bdf1600387a2247be26387be896496e702b5df7035d4d0` |
| `SITC_PUBLIC_REPRODUCIBILITY_PACKAGE_v1.0.zip` | `b453a6e2fb5a084338ee2083798c6a177b676bcdba5e6a714f9e14913129b963` |
| `ZENODO_22863692_HUMAN_REVIEW_RECEIPT.json` | `2bae95622dd9527600ffed4b0eecea16f084664efd2f622c4951cb5e68f2633b` |
| `ZENODO_22863692_FINAL_SHA256_MANIFEST.txt` | `c5f3d58c3ba45db2d296d450e5ecb2ede32ac9c90cf46439c354e3311628f947` |

The Claude and Grok audit files are also preserved byte-for-byte as external review evidence:

- Claude: `fa56be19d5d0df1fba18528eb7449e19ab48f02bb8d0e1231f38e96564dd0d29`
- Grok: `8863127fcd9cb6af192d3efa99389e6ef2d456739ad62797ea263af5060e31d7`

## Scientific invariants

RC2 changes presentation, public-package scope, verification language, licensing, and public reference-code hygiene. It does not change:

- the frozen D2 scientific preregistration or its acceptance criteria;
- the historical outcome-bearing campaign;
- the normalized historical evidence or its classification;
- the registered S1–S6, P_CLAMP, or Q_CLAMP definitions;
- the deterministic reference mechanism used in the accepted campaign;
- any threshold, intervention, ordering rule, or post hoc classification;
- the reserved DOI;
- the claim exclusions;
- the status `NOVELTY = UNADJUDICATED`.

## Canonical claim

RC2 uses the exact frozen maximum supported claim everywhere:

> In the registered finite construction, a relationally self-indexed temporal state causally influenced future-directed choice through the separately intervened prospective-evaluation path.

The RC1 paraphrase beginning “In a constructed finite system …” is removed from all load-bearing RC2 locations because it is not text-identical to the frozen boundary.

## RC2 changes

### 1. Framing narrowed to an engineered reference assay

- Reframes the paper as validation of a preregistered causal assay on a finite, transparent, deliberately engineered reference construction.
- Defines `SELF` as an engineered relational tag, the history carrier as an explicit state variable, and prospective evaluation as a deterministic registered computation.
- States that the observed causal dependencies follow from controlled interventions on this constructed causal graph.
- Removes any implication that the campaign discovered spontaneous machine selfhood or an autonomous self-model.
- Keeps the contribution claim at the level of assay design, intervention discipline, integrity controls, and public reference reproducibility.

**Affected outputs:** RC2 EN/HU PDFs; `README_EN.md`; `README_HU.md`; `PUBLICATION_METADATA.json`; Zenodo description drafts.

### 2. S1–S6 and clamp roles separated

Adds an explicit evidentiary-role table rather than presenting every component as an equally independent finding:

| Component | RC2 role |
|---|---|
| S1 | Target self/other attribution contrast and implementation-conformance check |
| S2 | State substitution/interchange check |
| S3 | Attribution-ablation check |
| S4 | Prospective-coupling ablation and specificity check |
| S5 | Deterministic serialization/restoration check |
| S6 | Origin-exclusion and infrastructure negative control |
| P_CLAMP | Direct mediator intervention positive control |
| Q_CLAMP | Deliberately direct, single-shot downstream selector control |

The revised interpretation states that several results are algebraically entailed by the registered equations. Their evidentiary value is implementation conformance, routing validation, negative-control behavior, or exact restoration, as applicable. S5 is not evidence of selfhood. S6 is limited to the implementation in which true origin is not supplied to the core. Q_CLAMP is identified as probe-free and deliberately tautological with respect to the supplied downstream scores.

**Added path:** `evidence/EVIDENTIARY_ROLE_TABLE.md`.

### 3. Observation and replication language corrected

RC2 reports the nested structure explicitly:

- per process: 88 cases, 292 traces, and 74,752 stored probe records;
- each trace contains 256 repeated read-only records that are identical by design;
- per process: 276 trace configurations and 88 decision tuples, as separately reported by the audit;
- six deterministic fresh-process executions: 528 case instances, 1,752 trace instances, and 448,512 stored probe records.

The `448,512` total is retained only where immediately decomposed. It is not described as 448,512 independent observations. The six executions are described as within-implementation deterministic reproducibility plus execution-order and opaque-token invariance, not independent scientific replication.

**Affected paths:** `evidence/SITC_STATISTICS_AND_EFFECT_SIZE_REPORT.md`; `evidence/SITC_CAUSAL_CONTRAST_REPORT.md`; `PUBLICATION_METADATA.json`; RC2 EN/HU Methods, Results, and Limitations.

### 4. Algebraic reduction and factor roles added

Adds a concise reduction of the registered scoring equations and states which factors can alter the observed choice in each panel.

- The goal term cancels in the main contrast but remains relevant in the specifically identified S2 and S4 specificity cells.
- Reversing presentation order cannot alter an argmax over independently scored options in this implementation.
- The sign of event content cancels in panels governed only by squared terms.
- The 96 S1 registered cases instantiate two distinct arithmetic margin classes, `16` and `64`.

The registered historical design remains unchanged. Algebraically inert factors are described as invariance controls and are not counted as separate positive effects.

**Added path:** `evidence/ALGEBRA_AND_INDEPENDENT_UNITS.md`.

### 5. Prior-art review expanded

The focused comparison is expanded to include:

- Vig et al. (2020), causal mediation analysis;
- Meng et al./ROME (2022), causal tracing and restore-and-recover logic;
- Geiger et al., interchange interventions and causal abstraction;
- relevant activation-patching methods literature;
- the already included autobiographical-memory, self/other attribution, and prospection literature.

RC2 distinguishes prior art for individual components from the exact packaged assay/protocol combination. It does not claim novelty for either the architecture or the combination. Bibliographic metadata must be verified before the final build.

**Affected path:** `prior_art/SITC_PRIOR_ART_REVIEW.md` and the Related Work sections of both manuscripts.

### 6. Public verification scope made explicit

RC2 distinguishes four operations:

1. verification of the frozen normalized projection and accompanying receipt assertions;
2. execution of the public reference implementation;
3. a fresh independent rerun of that public reference implementation;
4. reconstruction of the historical original six-process campaign.

The compact public package supports operation 1 and documents a route for operation 2. Operation 3 is separate external evidence when performed. The package does not support operation 4 because the six large historical raw arrays are excluded and represented only by historical hashes and receipts. `public_verify.py` emits explicit machine-readable fields confirming that it did not execute the reference implementation, load the historical raw arrays, reconstruct the historical campaign, or replay historical process provenance.

**Added path:** `integrity/PUBLIC_VERIFICATION_SCOPE.md`.  
**Affected paths:** `code/public_verify.py`; `code/run_public_reference.py`; `README_EN.md`; `README_HU.md`; `PUBLICATION_METADATA.json`; manuscript Reproducibility and Limitations sections.

### 7. Prospectivity claim bounded

RC2 describes the protocol as prospectively frozen within the project’s recorded hash-and-receipt chain. It also states that no independent third-party timestamp or public preregistration service anchored the freeze before execution. No retrospective timestamp is added.

**Documented in:** `integrity/PUBLIC_VERIFICATION_SCOPE.md`, `PACKAGE_SCOPE_AND_EXCLUSIONS.md`, the bilingual READMEs, metadata, and both manuscripts.

### 8. D0 freeze-envelope gap resolved without architecture leakage

The exact hash-bound `SITC_D0_ARCHITECTURE.md` is not added to the public package. It contains unpublished cross-project architecture language and is outside the authorized publication surface.

RC2 discloses:

- filename: `SITC_D0_ARCHITECTURE.md`;
- SHA-256: `f6c5ffb09c062b3421e33ebfdf2b732aeddaee679a89422cee21f902d5a32020`;
- byte count: 3,919;
- status: preserved privately as hash-bound historical provenance;
- reason: withheld to avoid disclosure of unpublished architecture.

No redacted or rewritten D0 is represented as the exact frozen artifact. RC2 describes the ZIP as a verification/reference package rather than a complete historical freeze reconstruction.

**Added path:** `protocol/WITHHELD_HASH_BOUND_ARTIFACTS.md`.

### 9. Public code surface reduced and made portable

RC2 replaces the historical campaign-specific public binder/plan surface with a minimal public reference derivative. The public derivative retains only what is needed to inspect and rerun the finite reference assay:

- finite state and scoring mechanism;
- S1–S6 and P/Q clamp construction;
- normalized evidence generation;
- normalized-evidence verification;
- a documented public-reference run route.

RC2 removes from the public ZIP unnecessary campaign/future-development paths, references to absent worker or semantic-audit modules, operating-system-specific path assumptions, and live-repository binding requirements. The derivative is labeled as a public reference implementation and is not described as the byte-identical historical campaign runner. Only hashes needed to bind the public core, experiment, and extracted scorer to frozen scientific sources remain in provenance. The private/master implementation is unchanged.

The reference package keeps `sitc_core.py` and `sitc_experiment.py` byte-identical to the accepted campaign sources. It adds a package-relative `sitc_plan.py`, a bounded `sitc_score.py` extraction, and publication-specific verifier/runner scripts. Their provenance record distinguishes exact source copies, extracted scientific logic, and newly written adapters.

**Added/retained paths:** `code/sitc_core.py`; `code/sitc_experiment.py`; `code/sitc_plan.py`; `code/sitc_score.py`; `code/run_public_reference.py`; `code/public_verify.py`; `code/README.md`; `code/REFERENCE_CODE_PROVENANCE.json`.  
**Excluded from RC2 ZIP:** historical campaign-specific binder and plan modules; their unnecessary filenames and hashes are not exposed by the new RC2 provenance record.

### 10. Duplicate-byte licensing ambiguity removed

RC2 keeps one canonical copy of the preregistration and freeze receipt under `protocol/`, licensed CC BY 4.0. It removes byte-identical copies from `code/` so the same bytes are not implicitly assigned both MPL-2.0 and CC BY 4.0 through directory rules.

The mixed-license rule remains:

- manuscripts, documentation, protocol, and public evidence: CC BY 4.0;
- source code, verifier, and minimal reference implementation: MPL-2.0.

A file-level license map assigns every packaged path exactly once and is mechanically audited.

**Affected paths:** `protocol/SITC_D2_PREREGISTRATION_v1.0.0.json`; `protocol/SITC_D2_FREEZE_RECEIPT.json`; `LICENSES/CC-BY-4.0.txt`; `LICENSES/MPL-2.0.txt`; `LICENSES/LICENSE_MAP.json`; bilingual READMEs.

### 11. Terminology and title audited for operational meaning

RC2 retains terms such as “self-indexed,” “self-history,” “future-directed,” and “prospective evaluation” only where they are operationally defined. The manuscript explains that these are engineering labels for a relational ownership tag, an explicit event-state carrier, deterministic option scoring, and current choice in a finite construction. The title and subtitle are narrowed where needed to foreground the engineered reference-assay setting.

No terminology is used to imply consciousness, subjective experience, personhood, AGI, human-equivalent selfhood, spontaneous self-model emergence, or architectural novelty.

**Affected outputs:** RC2 EN/HU PDFs; bilingual READMEs; citation and Zenodo metadata.

### 12. English/Hungarian equivalence re-established

The English manuscript is revised first and remains authoritative. The Hungarian companion is regenerated or revised from the final English scientific content. A post-render substantive-equivalence audit checks the canonical claim, qualifications, counts, limitations, novelty status, and forbidden claim upgrades in both PDFs.

The PDFs remain separate publication objects; they are not inserted into the reproducibility ZIP. Both are supplied together with the ZIP for external re-audit and are bound by the outer receipt and final manifest.

**Added path:** `integrity/EN_HU_SUBSTANTIVE_EQUIVALENCE.md`.

### 13. Publication metadata and identity envelope repaired

RC2 reviews `CITATION.cff` resource type, reserved-DOI wording, version naming, publication state, and the Zenodo description. Every public surface states `NOT_UPLOADED / NOT_PUBLISHED` until actual publication. The reserved DOI is not represented as resolving or published.

The RC2 external-review envelope contains five separately hash-bound objects:

- `SITC_CAUSAL_ASSAY_v1.0_RC2_EN.pdf`;
- `SITC_CAUSAL_ASSAY_v1.0_RC2_HU.pdf`;
- `SITC_PUBLIC_REPRODUCIBILITY_PACKAGE_v1.0_RC2.zip`;
- `ZENODO_22863692_RC2_HUMAN_REVIEW_RECEIPT.json`;
- `ZENODO_22863692_RC2_FINAL_SHA256_MANIFEST.txt`.

The receipt and manifest also bind the preserved external audits, this remediation matrix, and this changelog. RC2 generates entirely new SHA-256 values; it does not reuse RC1 hashes for changed objects.

### 14. External-audit response added

Adds a finding-by-finding response covering Claude C-1 and M-1 through M-8, plus Grok Critical 1–2 and Material 3–7. Each entry records severity, disposition, evidence, bounded remediation, and resulting path. No critical or material finding is silently omitted, accepted, or rejected.

**Added path:** `EXTERNAL_AUDIT_REMEDIATION_MATRIX.md`.

## Claim boundary retained

RC2 explicitly states that the work does not establish:

- phenomenal consciousness;
- subjective experience;
- personhood;
- AGI;
- human-equivalent selfhood;
- spontaneous emergence of a self-model;
- architectural novelty.

## Final RC2 verification gate

Before RC2 can be labeled ready for external re-audit, the build must pass all of the following without changing frozen scientific criteria:

- exact canonical-claim search across both manuscripts, READMEs, metadata, citation data, and Zenodo descriptions;
- rendered inspection of both PDFs, including DOI and publication-state wording;
- English/Hungarian substantive-equivalence audit;
- public ZIP inventory and clean extraction;
- normalized-evidence verifier execution;
- fresh public-reference execution where supported, reported as a new run rather than historical reconstruction;
- unit/count reconciliation and repeated-probe disclosure;
- file-by-file license-map audit;
- scan for local paths, live-Git dependence, M1/future-development names, and unpublished architecture;
- verification that exact D0 content is absent while its withholding disclosure is present;
- new SHA-256 manifest and human-review receipt covering the complete RC2 envelope.

Failure of any gate leaves the status at `REMEDIATION_REQUIRED`. This changelog does not authorize upload, publication, or reservation of another DOI.
