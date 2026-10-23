CNA, 2026-10-23, additive note; planning only; authorizes nothing

# Track B prior-art verification v1.1: pre-freeze registry search and full-text reads (CNA)

- **Amends nothing.** This note is additive to `trackB_prior_art_verification_v1_CNA.md` (sha256 f2fd0ae6f5df571f6ed6ad413ff604ffcb975e565c91c991acf8c801c6104ac9). Neither that file nor any other existing file was edited.
- **Nothing ran.** No training and no repo code. The only actions were read-only HTTP GETs: arXiv PDFs and abstract pages, the OSF API v2, the OSF/SHARE trove search, Crossref, PMLR, AsPredicted public pages, plus one WebSearch.
- **Written** 2026-10-23, about 10:28–10:50 AM ET. All registry results are as of that window.
- **Scope.** The Lead's narrowed novelty claims: (1) Q-NECESSITY of a learned interoceptive self-model against matched same-size ablations of other modules and matched arms; (2) SELF, where the agent predicts its own internal variables better than a matched outside observer, adapted from Binder et al. 2024; (3) pre-registration plus a Stage-0 known-answer gate.

## Bottom line

- **Hayes and Grimbly did not run our Q-NECESSITY test.** Hayes ran only evaluation-time perturbations of engineered mechanisms and says so (§6.1). Grimbly ablated a hand-specified precision router in an active-inference agent (§4). Neither used a learned interoceptive self-model with same-size ablations of other modules. Neither paper needs to be dropped from our claims or relabelled as a replication.
- **Verdicts:**
  - (1) **STILL NOVEL AS FAR AS FOUND.** Narrowed, with a new design-level overlap: Craggs 2026 (OSF jz4ed), a pre-registered study that has not yet been run.
  - (2) **STILL NOVEL AS FAR AS FOUND.**
  - (3) **PARTIAL OVERLAP.** Pre-registered causal tests of self-models and homeostasis in simulated artificial agents already exist on OSF (Craggs 2026 Blocks I–V; Faeth 2026). Only the *Stage-0 known-answer detectability gate for these instruments* survives as novel as far as found.
- **Registries:** OSF was searched (37 queries, Part A). AsPredicted is **NOT SEARCHABLE** by keyword (A.3).
- **Pardo et al. 2018: VERIFIED** (Part E).

## Part A. Registry search

### A.1 OSF Registries: method

- **The OSF API v2 has no full-text search.** `https://api.osf.io/v2/search/?q=…` and `/v2/search/registrations/?q=…` both returned HTTP 404 `{"detail":"Not found."}`. Two routes were used instead:
  - **TROVE:** the SHARE/trove index behind osf.io/registries, `https://share.osf.io/trove/index-card-search?cardSearchText=<q>&cardSearchFilter[resourceType]=Registration&page[size]=25&acceptMediatype=application/json`. The total is the `meta.total` field. Trove appears to AND terms, so multi-word queries are narrow.
  - **API:** `https://api.osf.io/v2/registrations/?filter[<title|description>][icontains]=<q>&page[size]=100`. The total is `links.meta.total`. Only the first 100 results per query were inspected.
- **Screening.** Hits were screened by title, and by description where a title looked relevant. Raw outputs are in `/workspace/tmp_pa2/osf_out.txt` and `osf_results.json` (shas in the footer).

### A.2 OSF queries and hit counts

| Route | Query | Total | Relevant hits |
|---|---|---|---|
| TROVE | homeostatic reinforcement learning | 1 | 0 (EEG/ERP methods registration) |
| TROVE | allostatic agent | 0 | — |
| TROVE | interoceptive agent | 4 | 0 human-subject |
| TROVE | interoception artificial agent | 0 | — |
| TROVE | homeostatic agent | 2 | see A.2.1 |
| TROVE | global workspace agent | 0 | — |
| TROVE | global workspace reinforcement learning | 0 | — |
| TROVE | global workspace artificial | 3 | 6au93 (LLM, see below) |
| TROVE | self-model artificial agent | 23 | jz4ed, 8cfqw/cae2h, 97dgx, t6rgd (see below) |
| TROVE | self-model ablation | 13 | jz4ed |
| TROVE | causal necessity internal state artificial agent | 0 | — |
| TROVE | ablation deep reinforcement learning | 1 | 0 |
| TROVE | reinforcement learning ablation | 1 | 0 |
| TROVE | deep reinforcement learning | 33 | 0 relevant (engineering/finance RL; 64dtx is a pre-registered MARL benchmark, off-topic) |
| TROVE | artificial consciousness indicators | 0 | — |
| TROVE | consciousness artificial intelligence | 96 (25 read) | 0 empirical agent studies (theory/framework deposits) |
| TROVE | machine consciousness | 55 (25 read) | sz4dy (ADAN, see below) |
| TROVE | introspection language model | 3 | 0 agent studies |
| TROVE | privileged access self-prediction | 1 | 0 |
| TROVE | active inference agent simulation | 1 | v9nmw (see below) |
| TROVE | Theory of Everything Research Programme | 8 | Craggs Blocks I–V (see below) |
| TROVE | Craggs dependency architecture | 6 | same set |
| TROVE | maintenance self-model artificial agent preregistration | 1 | jz4ed |
| API | title: homeostatic | 20 | hv7c2 |
| API | title: homeostasis | 29 | 69zny |
| API | title: allostatic | 40 | 75w9d (wearables, not agents) |
| API | title: allostasis | 2 | 0 |
| API | title: interocept | 345 (100 read) | 0 (human interoception) |
| API | title: global workspace | 0 | — |
| API | title: reinforcement learning | 130 (100 read) | 0 artificial-agent necessity studies (mostly human RL tasks) |
| API | title: self-model | 8 | 8cfqw, cae2h |
| API | title: artificial agent | 20 | 0 (human–agent interaction) |
| API | title: consciousness in AI | 0 | — |
| API | title: machine consciousness | 2 | 0 empirical |
| API | title: artificial consciousness | 0 | — |
| API | description: reinforcement learning agent | 6 | 0 relevant |
| API | description: global workspace | 6 | 9yv73 (human TMS-EEG), 6au93 |
| API | description: homeostatic | 105 (100 read) | b4asn, hv7c2 |
| API | description: interoceptive | 442 (100 read) | 0 artificial-agent |
| API | description: allostatic | 94 | 0 artificial-agent |
| API | title: Research Programme | 17 | Craggs Blocks I–V |

#### A.2.1 Relevant OSF registrations

Each entry was read from its OSF API record (title, description, registration responses where noted). Files and code were **not** opened.

1. **K. Craggs, "Preregistration: Block V Reflective Self-Modelling – Theory of Everything Research Programme"**, OSF Preregistration, registered 2026-10-09. https://osf.io/jz4ed. Full registration responses were read.
   - **What it registers:** S0 no self-monitor, S1 passive, S2 active, **S3 shuffled/distribution-matched self-monitor control** and **S4 capacity-matched non-self control**, plus bypasses H_ERROR and H_EXTERNAL. It has 20 frozen seeds and frozen Retain/Restrict/Reduce/Reject thresholds. H5.3 directly manipulates a self-estimate and then rescues it. H5.5 compares self-monitor MAE against "world-only uncertainty".
   - **What the self-model represents:** "facts about its own competence, uncertainty, resources or limitations".
   - **Status:** "Data does not yet exist" (Q 344-4). The execution registry was "FROZEN_PREREGISTRATION_READY_UNRUN", with a pre-execution clarification dated 10 October 2026. **No results found.**
   - **Not determinable from the record:** whether agents are deep RL or learned networks at all, and whether "resources" is interoceptive or homeostatic. The record describes "deterministic software" and decision/verification task families.
   - **Closeness: PARTIAL**, and the closest registry hit for claims (1) and (3). It pre-registers a self-model causal-necessity design with a capacity-matched non-self control and a distribution-matched sham, which is the same logic as our same-size ablation and sham. It is a competence/metacognitive self-model, not a learned interoceptive model in a homeostatic RL agent, and it has not been run.
   - **Related deposit:** Craggs 2026, Zenodo DOI 10.5281/zenodo.22857230, cited in the record. It was not opened.
2. **K. Craggs, Block I B2 "Causal Maintenance Network"**, OSF Preregistration, 2026-10-02. https://osf.io/gqanp. Description read.
   - **What it registers:** passive, external, feed-forward internal, reciprocal internal and **budget-matched brute-force internal bypass** architectures; targeted ablation; "equal-budget irrelevant rescue".
   - **Closeness: PARTIAL** on pre-registered self-maintenance necessity in an artificial system with budget-matched controls. No agent RL or interoceptive self-model is evident from the description.
   - **Sibling registrations** (titles only): Blocks I B1 g3te5, I H1.5 jrcnb, II euf2j, III 8zwm7 and IV rehw5.
3. **J. D. Faeth, "When Internal Signals Mislead: Sensing and Preference in Artificial Homeostasis"**, OSF Simulation Study Template, 2026-09-30. https://osf.io/69zny. Description read.
   - **What it registers:** a pre-registered AffectWorld study, the same platform as Grimbly 2026, comparing coupled selective-sensing agents against preference-reweighting agents under biased interoceptive signals. It uses 64 seeds and a seed-paired estimand.
   - **Closeness: PARTIAL** on claim (3): pre-registration in a homeostatic agent. It runs no self-model necessity test, no SELF test and no known-answer gate.
4. **B. A. Vasile, "HHCA: Heterogeneous Homeostatic Control Architecture – Phase I"**, Open-Ended Registration, 2026-09-27. https://osf.io/hv7c2. Its tags are agent monitoring, AI control and AI safety. Per its description, it is a "locked Phase I protocol" with no results. **DIFF** (control architecture; content not opened).
5. **J. Tkemaladze, "Ze-AL v4 Stage-0…allostatic load (pre-registered simulation)"**, 2026-05-09. https://osf.io/75w9d. It uses a "Stage-0" simulation gate for wearable allostatic-load estimators. **DIFF**: not agents. It is the only other "Stage-0"-labelled pre-registered simulation found, and it is in a different domain.
6. **P. Upadhyay, "Operationalizing Self-Modeling Organization (Ψ) in Artificial Systems"**, 2026-09-16 (https://osf.io/cae2h) and 2026-09-20 (https://osf.io/8cfqw). It describes a "perturbation-versus-matched-control benchmark" for whether an AI system tracks itself, apparently aimed at LLMs (target venue cs.CL). **DIFF/PARTIAL**: no interoceptive or homeostatic agent, content not opened.
7. **Others:**
   - DIFF and theory-only, not opened: sz4dy ADAN (machine-consciousness architecture, tags include homeostasis and GWT), b4asn FRONT 3.3 ("homeostatic AI … robotic self-model"), 6au93 (GW emergence in LLMs), v9nmw (active inference vs AlphaZero), 9yv73 (human TMS-EEG).
   - b4asn's description lists "mechanical self-preservation" protocols. That is noted for the safety record only; nothing there changes X1–X5.

### A.3 AsPredicted: **NOT SEARCHABLE** (public keyword search)

- **Homepage (https://aspredicted.org/, fetched 2026-10-23):** "Public Pre-registrations (lookup an AsPredicted referenced in published paper by # only)". It also says a "Pre-registration remains private until an author makes it public", and private ones may stay private forever (https://aspredicted.org/messages/private_forever.php).
- **List page:** `see_list.php?action=1` returns "To access this page you need to log in."
- **Search URL:** `search.php?q=reinforcement` returns HTTP 200 but only the homepage template. No search endpoint exists.
- **No login was attempted.**
- **Proxy only:** one WebSearch, "aspredicted.org reinforcement learning agent pre-registration ablation neural network", returned AsPredicted #88,320, #260,282 and #119,703. All are human-subject decision studies; none are artificial-agent studies. This is not a registry search.

## Part B. Full-text reads

All three PDFs were downloaded from arxiv.org/pdf and converted with `pdftotext -layout` (poppler). Every page was read. Page numbers are the PDF's printed page numbers.

### B.1 Hayes 2026

- **Record:**
  - Title: "Predictive Allostatic Organization in Recurrent and Spiking Agents Under Partial Observability".
  - Author: Frederick Hayes III, Independent Researcher.
  - arXiv 2608.11506, **v1**, submitted Tue 11 Aug 2026 23:40 UTC (7:40 PM ET). **v1 is the only version.**
  - Bibliographic details unchanged from v1: **VERIFIED**.
- **Architecture:**
  - A 7×7 foraging gridworld with 3 resources, 3 threats, a 40-step horizon and an internal energy variable.
  - A trace-augmented GRU ("Trace-GRU") and several spiking policies with "membrane state, spike summaries, recurrent current, gain, threshold modulation, gate variables, operating temperature" (§3.2, p. 9).
- **Training:** mixed. "Several spiking operating points are evaluated, including behavior-cloned and reinforcement-learning-trained variants" (§3.2, p. 9). The training algorithm for Trace-GRU is not stated in the text I read.
- **Is the internal model learned or hand-designed?** Neither fits cleanly. No separate interoceptive self-model exists. Energy is an observation input, and allostatic modulation is an engineered mechanism:
  - "Energy, trace, and allostatic modulation are engineered components, not blank-slate discoveries" (§6.1, p. 22).
  - Low energy is decoded from hidden state by probes, including after energy features are removed (internal dynamics without energy: AUC ≈ 0.927; §4.3, p. 15).
- **What was intervened on:**
  - Evaluation-time zeroing or disabling: trace, contact trace, state reset, energy-neutral observation, contact sensor, allostatic modulation, oscillatory gating, recurrent current, membrane persistence, and temperature (§3.4, p. 11).
  - "These perturbations alter deployed mechanisms without retraining the models" (§3.4, p. 11).
  - "No allostatic modulation": mean ΔFSE −0.038 (Table B8, p. 30).
- **Same-size ablations of other modules or matched arms?** No. Perturbations are of heterogeneous mechanisms, with no size or capacity matching, no retrained ablation arms and no sham intervention. Permutation-label baselines are used for probes only (§3.4, p. 11).
- **Was necessity for behaviour tested?** Only deployed dependence:
  - "Evaluation-time perturbations test deployed dependence, not retrained necessity" (Table 3, p. 21).
  - "they are not equivalent to retraining ablations and may create out-of-distribution policy states. The results therefore support claims about deployed dependence, not necessity for learning from scratch" (§6.1, p. 23).
  - Future work: "replace evaluation-time perturbations with matched retraining ablations" (§6.2, p. 23).
- **Pre-registered?** No. "All headline results come from a frozen evaluation sequence established after pilot development" (§3.3, p. 10) describes an internal freeze. No registry, OSF, AsPredicted or "preregist*" string appears in the full text (grep).
- **SELF test?** None. There is no comparison of the agent's own prediction of its internal variables against an outside observer.
- **Consequence:** this is PARTIAL prior work for Q-EXIST and deployed-dependence Q-CAUSE, as v1 already said. It is **not** our Q-NECESSITY.

### B.2 Grimbly et al. 2026

- **Record:**
  - Title: "Interoceptive Attention as Dynamic Homeostatic Prioritization in a Foraging Agent".
  - Authors (10): **St John Grimbly, Nicolas Kuske, Evert A. Boonstra, Bruce A. Bassett, Charel van Hoof, Rowan Hodson, Benjamin Rosman, Ryan Smith, Mark Solms, Jonathan P. Shock**.
  - arXiv 2608.04232 [cs.AI], **v1**, 4 Aug 2026 (the only version).
  - The supplement states: "the 12-page SAB 2026 camera-ready paper … is reproduced without alteration and followed by these sections" (Supp., p. 13).
  - **CORRECTED** against v1 B2.9, which listed only the first 7 authors. Add Smith, Solms and Shock, and the SAB 2026 venue.
- **Architecture:**
  - An active-inference POMDP agent in AffectWorld, a 6×6 grid with 3 need channels plus an inert control and an EFE planner with H = 3.
  - "a fixed body-transition prior B … and a learned observation likelihood A" (§2.1, p. 4). A is learned online by Dirichlet counts.
- **Training:** not RL, and the paper says so explicitly. "Reinforcement learning, for instance, can be given interoceptive state and a homeostatic reward. We use active inference…" (§1, p. 2). No neural networks are used.
- **Is the interoceptive mechanism learned or hand-designed?** Hand-designed:
  - "The κ-routing here is hand-specified, and whether a learned router converges to the same need-aligned policy is the natural follow-up" (§4, p. 10).
  - Only the likelihood A (what each interoceptive reading reports) is learned. The selector is a fixed argmax over the agent's own posterior (§2.2, p. 5).
- **What was ablated:**
  - uniform-κ vs attentive vs anti-aligned at the same budget (Table 1, p. 7);
  - selector variants (Fig. 4, p. 8);
  - an inference-only ablation that withholds the shaped likelihood from the planner ("loses 20 pp"; §3.3, p. 8);
  - a planning-only mirror ablation (§3.3, pp. 8–9);
  - fixed-channel controls (§3.4, p. 9).
- **Same-size or matched?** Matched on precision budget only: "differ only in κ allocation … all three agents are compared at an identical budget" (§2.3, pp. 6–7). There are no same-size ablations of *other* modules. A matched preference-reweighting comparator is explicitly left to future work (§5, pp. 10–11).
- **Was necessity for behaviour tested?** Yes, for a hand-specified precision-routing mechanism, using survival as the outcome. The inference-only ablation and the anti-aligned control show that the mechanism is needed for the survival gain. This is mechanism necessity, not necessity of a learned self-model.
- **Pre-registered?** No. No registry or "preregist*" string appears. Holm correction covers 3 primary contrasts; "The remaining sweeps in this supplement are exploratory" (Supp. B, p. 15). L01 was excluded on "a post-hoc behavioural criterion" (Supp. B, p. 14).
- **SELF test?** None.
- **Related:** a pre-registered follow-on on the same AffectWorld platform by a different author exists (Faeth 2026, OSF 69zny; A.2.1 item 3).

### B.3 Phua 2025

- **Record:**
  - Title: "Can We Test Consciousness Theories on AI? Ablations, Markers, and Robustness".
  - Author: Yin Jun Phua, Institute of Science Tokyo.
  - arXiv 2512.19155 [cs.AI], **v1**, 22 Dec 2025 (PDF dated December 23, 2025). The abstract page lists only v1.
  - **VERIFIED.** v1 cited an "HTML dated 2026-08-24". The arXiv HTML link is also v1 (`html/2512.19155v1`), so there is no later version.
- **Architecture:**
  - MiniGrid with a CNN encoder; A0 feedforward MLP; A1 GRU-64; B1 4-slot × 16-d workspace bus with fixed-slot write and flattened readout.
  - B2 = B1 + Self-Model z_self (64-d), which reads "64-d recurrent carrier + 16-d workspace broadcast + 7 action logits + 2 uncertainty scalars" (§4.1, pp. 5–6).
- **Training:** imitation, not RL. "Agents were trained using Behavior Cloning (BC) from an expert oracle" (§4.3, p. 7). z_self gets a supervised auxiliary loss to predict the agent's own correctness (§4.3.2, p. 8).
- **Is the self-model learned or hand-designed?** It is learned, but it models *task confidence*, not interoceptive or homeostatic variables. There is no body or homeostasis.
- **What was ablated:**
  - No-rewire z_self lesion (zeroed; Type-2 AUROC 0.92 → 0.50 with first-order accuracy 88.5% → 88.2%; §5.1.2, p. 11).
  - Workspace capacity 4/2/0 slots (§4.5, p. 11; §5.2, pp. 14–16).
  - Latent noise titration (§5.3).
  - Blind (noise/permutation) ablations and a PCA baseline matched to z_self's effective dimensionality (§5.1.2, p. 13).
  - Pilot "matched 'BC-only' compressor controls that replace z_self with a 64-d bottleneck" (n = 5; §5.3.2, p. 19; Fig. 4).
- **Same-size or matched?** Partly. The 64-d compressor controls are size-matched *replacements of the self-model* in the robustness experiment, as a pilot. Same-size ablations of *other* modules, used as a necessity contrast, were not run. "parameter-matched variants" are listed as future work (§6.6, p. 22).
- **Was necessity for behaviour tested?**
  - Workspace: yes, for access and report ("workspace capacity is causally necessary for information access within this setup"; §6.1, p. 20).
  - Self-model: necessary for metacognitive calibration, and by design *not* for first-order behaviour.
- **Pre-registered?** No. "We did not run a prospective power analysis" (§6.6, p. 21). "All hyperparameters were fixed before evaluation" (§4.3.3, p. 9) is not a registration. No registry string appears.
- **SELF test?** None against an outside observer. The confidence head predicts the agent's own correctness, but there is no observer model trained on the same behaviour.
- **Minor:** Phua's reference list gives the Wilterson & Graziano 2021 PNAS title as "…Controlling attention without consciousness". Crossref (DOI 10.1073/pnas.2102421118) gives "The attention schema theory in a neural network agent: Controlling visuospatial attention using a descriptive model of attention". Use the Crossref title if we cite it.

## Part C. Verdicts

| Claim | Verdict | Reasoning |
|---|---|---|
| (1) Q-NECESSITY of a learned interoceptive self-model vs matched same-size ablations of other modules and matched arms | **STILL NOVEL AS FAR AS FOUND** (narrowed) | **Hayes:** no separate self-model; engineered allostatic mechanisms; evaluation-time, unmatched perturbations; the author disclaims "retrained necessity". **Grimbly:** hand-specified router, active inference rather than RL, budget-matched only, no other-module ablations. **Phua:** a learned self-model, but metacognitive rather than interoceptive, BC rather than RL, and the lesion shows it is *not* needed for behaviour. **Craggs Block V (OSF jz4ed)** pre-registers the *design logic* (capacity-matched non-self control, distribution-matched sham, bypasses) for a competence self-model, is unrun, and its substrate is unknown. Cite it as the closest design precedent and differentiate on interoceptive content, learned RL agent, homeostatic viability outcome and same-size ablation of *other* modules. |
| (2) SELF (own-variable prediction beats a matched outside observer), adapted from Binder et al. 2024 | **STILL NOVEL AS FAR AS FOUND** | No full text or registry hit has an observer model trained on the same agent's behaviour. The nearest are Phua's own-correctness confidence head, with no observer, and Craggs H5.5's self-monitor vs world-only uncertainty MAE, which compares against a world-uncertainty estimator rather than an outside observer of the agent. Both should be cited as related. |
| (3) Pre-registration + Stage-0 known-answer gate | **PARTIAL OVERLAP** | Pre-registration as such is **not** novel. Pre-registered causal self-model and self-maintenance simulations (Craggs Blocks I–V, Sep–Oct 2026) and a pre-registered artificial-homeostasis agent study (Faeth 2026, AffectWorld) already exist on OSF. Craggs also uses development-only pilots to set thresholds, which resembles a gate but is not a known-answer detectability check. The surviving part, as far as found, is the **Stage-0 known-answer detectability gate validating the instruments (planted dependency, matched null, imitating confound) before any agent result is read**. The only other "Stage-0" pre-registered simulation (Ze-AL 75w9d) concerns wearable estimators. |

- **Did Hayes or Grimbly already run our Q-NECESSITY test? No.**
  - Hayes tested deployed dependence of engineered mechanisms without matched arms (§6.1, p. 23).
  - Grimbly tested necessity of a hand-specified precision router in a non-RL active-inference agent, matched on budget only (§2.3; §4, p. 10).
  - Neither claim needs to be dropped or relabelled as a replication.
- **Recommended wording changes.** These are recommendations only; nothing changes until the Lead and Astra rule.
  - Claim (3) should read: "pre-registered, with a Stage-0 known-answer instrument gate". Cite Craggs 2026 (jz4ed, gqanp) and Faeth 2026 (69zny) as existing pre-registered artificial-agent work.
  - Claim (1) should cite Craggs Block V as the closest design precedent. Hayes 2026 should be cited as having called for "matched retraining ablations", which our design supplies.
  - Add Wilterson & Graziano 2021 (PNAS, https://doi.org/10.1073/pnas.2102421118; bibliographic record VERIFIED via Crossref, content **not read**) to the self-model-in-agents prior art. It is an attention-schema model in a neural-network agent. Whether it ablated the schema and measured behaviour must be read before freeze (see D).

## Part D. Remaining limits

1. **OSF coverage.** The trove index ANDs terms, and the API `icontains` filters match only title or description substrings. Only the first 100 results per API query and 25 per trove query were screened. Registration files, code and attached PDFs were not opened, including Craggs' manifests and the Zenodo programme document. Whether the Craggs agents are learned or RL is therefore **unknown**.
2. **AsPredicted is not searchable.** Private AsPredicted pre-registrations, and public ones never cited in a paper, cannot be found. Other registries were not searched: Zenodo, ResearchBox/AsCollected, ClinicalTrials, and the PCI-RR and journal Registered Reports pipelines. Neither were conference workshop proposals.
3. **Unrun registrations.** Craggs Block V and Faeth may post results before our freeze. Re-check jz4ed, gqanp and 69zny immediately before freeze.
4. **Unread primary sources.**
   - Wilterson & Graziano 2021 is a possible self-model-necessity-in-agent precedent.
   - Dossa et al. 2024 was not read in full in either pass.
   - Hayes' companion SBP-BRiMS 2026 paper was not re-read.
   - Binder et al. 2024 was not re-read to confirm exactly how the cross-prediction design should transfer.
5. **What "full read" covers.** It means pdftotext of the full arXiv PDF. Figures were read only through their captions and text. Code repositories (fehayes/predictive-allostatic-organization; sgrimbly/attention-aif-sab2026-snapshot) were not inspected. I did not audit any paper's results.
6. **General.** Absence of a hit is not evidence of absence. This is a targeted search, not a systematic review.

## Part E. Added item (parent request): Pardo et al. 2018

- **Status: VERIFIED.**
- **Title:** "Time Limits in Reinforcement Learning".
- **Authors:** Fabio Pardo, Arash Tavakoli, Vitaly Levdik, Petar Kormushev.
- **Venue:** Proceedings of the 35th International Conference on Machine Learning (ICML 2018), PMLR vol. 80, pp. 4045–4054.
- **URLs:** https://proceedings.mlr.press/v80/pardo18a.html (PMLR page: `citation_conference_title` "International Conference on Machine Learning", first page 4045, last page 4054) and https://arxiv.org/abs/1712.00378 (arXiv comments: "ICML 2018, NIPS 2017 Deep RL Symposium").
- **Checked:** bibliographic details only. The claim we would cite it for, bootstrapping from the final state at time-limit or stop truncation rather than treating it as terminal, is from memory of the paper and was not re-read here. It matches the paper's known thesis, but read §3 before quoting it.
- **Effect on v1:** B6 changes from "NOT verified" to bibliographically VERIFIED.

## Footer: inputs read (sha256)

- `/workspace/review/trackB_prior_art_verification_v1_CNA.md`: f2fd0ae6f5df571f6ed6ad413ff604ffcb975e565c91c991acf8c801c6104ac9
- `/workspace/tmp_pa/c1.txt`: 512200bfa9f81c3df96089123d9b4feaa9adf99c303d1a96aaa8b0e4a6cf1bc9
- `/workspace/tmp_pa/c2.txt`: c106458b235a5699639b8fcffcff6ee3a3afb548feedafab8d203997dd7d9297
- `/workspace/tmp_pa/c3.txt`: 41185ab0a51ae4a9967f169ebd4396364cbacd1d9697701b1e625fd305a60485
- `/workspace/tmp_pa/c4.txt`: df2c5af725fc6f1203762fd3d298a70404a8353c2d50a3f8a7256daf5c3c7efb
- `/workspace/tmp_pa/cr.py`: 59cbe092d0087d6d117e251a29991311a4a3f42643aa8b7825ff53d7120e8ad6
- `/workspace/tmp_pa/q.py`: d723f588dccf7be2441a319a28f87d9bb6208575e3b30383a9219e5f450ca907
- `/workspace/tmp_pa/r1.txt` (first 3,000 bytes read): ce7e68814a3799fbf1fa8488fe6a2a2ef5a17520127e637e28246144ac85efbd
- `/workspace/tmp_pa/r2.txt`: 9cb9ce87559eee4b44edf42107f8a0a29132d2e6db991f74f0325609e131ed3d
- `/workspace/tmp_pa2/2608.11506.pdf` (Hayes v1): 7e5dfbaee0695f85792eabee2d614e302fdf8e61a0da77ef962024b0f7256f21
- `/workspace/tmp_pa2/2608.04232.pdf` (Grimbly v1): 593a06b7e82cef55c53a11f5d6b4cbfed6bbea8ee34d26d5c847717783d5431a
- `/workspace/tmp_pa2/2512.19155.pdf` (Phua v1): c7f72e5a774aa2c3f94a3aa22b2f931ba0581c7ebb3d898bbf477f003dec57d8
- `/workspace/tmp_pa2/2608.11506.txt`: 5d6a84ac2a779c920e38683e71915a77805faa012c8622df0764961af975634e
- `/workspace/tmp_pa2/2608.04232.txt`: b1befe773eda9b1050b988eec435a4efec176334286306d3f45647f4bd9e9eea
- `/workspace/tmp_pa2/2512.19155.txt`: c40be0fdc1f11b63c40adb96f7a568a8b7f78081b0da2a630e40f48b30dbabd0
- `/workspace/tmp_pa2/2608.11506.abs.html`: d4ea146af035f61775121791557e25cbe017437da37cbc43c289f720f02147d7
- `/workspace/tmp_pa2/2608.04232.abs.html`: 80e6021d07d2bbafaca0f4a8fea58b2a9d68b6c622401fbae4d16f508f9a3e3d
- `/workspace/tmp_pa2/2512.19155.abs.html`: 9007c0631bf72b40d84e4478b92dd7100356140c3aba3b7b270123307b062570
- `/workspace/tmp_pa2/osf.py` (query script): 6b1d26d1b9feeb08348d9b05f43b59951f922c9d3bdfee9807cc621a20930cfe
- `/workspace/tmp_pa2/osf_out.txt`: ea4c5e6858cdf55c6637ae810646401a2038a49056bd9d7ed56877baedf07ea4
- `/workspace/tmp_pa2/osf_results.json`: 863bf22bbdd640d891409f04ffc4a0c8e8728da58efda4ac0010451ed932af31
- `/workspace/tmp_pa2/reg_jz4ed.json`: d3191f02ce46d641a61c906a01348f6b3cecddba52203e01fd673dcd4af9074b
- `/workspace/tmp_pa2/reg_69zny.json`: 53e45b7be8eb7b7cda64c1e5f29d0f3c76f1ca56de3e1a95d36bb230a20eafa5
- `/workspace/tmp_pa2/jz4ed_resp.txt`: e6cafb013cdbe0e540cadcc54307a72c90f79d834801c17374e0a112fb60e3ed
- `/workspace/tmp_pa2/pardo.abs.html`: 64c5eceef7b67f480de970808798f45526ce5ef6d9e7f1557718468251db26e0
- `/workspace/tmp_pa2/pmlr.html`: 19a78dc82a2a6818b547fa891c0119250fbbc4d3fbb159a5a328c73a0f1976e5
- `/workspace/tmp_pa2/asp.html` (AsPredicted homepage): a7cc9a69ee2ed28bc4565f75d9f72291f16641e8af8bb39d2eb484d6646ebc96
- **Read live, not saved:** OSF API records for gqanp, hv7c2, 75w9d, 8cfqw, cae2h, b4asn, 9yv73, zrnu6, 6au93, sz4dy and v9nmw; the AsPredicted private_forever, see_list and search pages; the Crossref record for 10.1073/pnas.2102421118.
---
sha256 of all content above this line (computed with sha256sum before appending this line): 46f988e84eb6d9a5393ed4f69ee249bb92b408a1fbcf1e377d774b01352a7845
