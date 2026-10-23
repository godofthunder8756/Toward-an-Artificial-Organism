CNA, 2026-10-23, additive note; planning only; authorizes nothing

# Track B prior-art verification and novelty search, v1 (CNA)

- **Amends nothing.** This note is additive. It checks the citations in `trackB_workspace_allostasis_scope_note_v1.md` (sha256 87a31cc88dc2fd0252d4cf932fabbfd8a1ce65bd3f77dce9eda5c6cfdafe2800, §1), `trackB_workspace_allostasis_scope_note_v1_1_addendum.md` (5cf075b6e0a75cf7696307924d22abd9b9e961f852b86745f80bd2b46a09b53a, A1) and `trackB_measurement_plan_v1_RD.md` (1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef, §7). None of those files was edited.
- **Nothing ran.** No training and no repo code. The only actions were web searches and read-only metadata lookups.
- **Written** 2026-10-23, about 10:20–10:45 AM ET.

## 0. Method and search limits (read first)

- **Tools used:**
  - WebSearch.
  - arXiv abstract pages fetched with curl, reading the `citation_*` meta tags.
  - The Crossref REST API (`query.bibliographic`), giving DOI, title, authors, container and year.
  - WebFetch or curl on a few landing pages: PMLR, NeurIPS proceedings, arXiv HTML, TSC 2026, SBP-BRiMS 2026.
- **Unavailable:** OpenAlex and Semantic Scholar returned HTTP 429 (rate-limited) and were not used. Google Scholar, OSF/AsPredicted pre-registration registries, PsyArXiv full-text search and non-English literature were **not** searched.
- **"VERIFIED"** below means: exact title, authors, year and venue were seen in a Crossref record, an arXiv abstract page, a publisher or proceedings page, or a library catalogue during this pass, and the DOI or URL listed is one I opened or that was returned by those sources. It does **not** mean I re-read each paper's content. Where our text attributes a specific *claim* to a paper, I say whether I checked that claim.
- **Novelty search terms (WebSearch, 2026-10-23):**
  - "deep reinforcement learning homeostatic agent interoception representation probing ablation causal necessity"
  - "Yoshida homeostatic reinforcement learning deep RL interoception embodied agent 2024"
  - "Dossa … global workspace agent embodied multimodal environment"
  - "ignition all-or-none dynamics artificial neural network global workspace test deep learning"
  - "Hulme homeostatic reinforcement learning neural network agent survival"
  - "Butlin indicator properties evaluation of reinforcement learning agent global workspace assessment empirical"
  - "active inference agent interoceptive allostasis deep neural network simulation ablation"
  - "AI Safety Gridworlds safe interruptibility empirical test"
  - "Brain-like features in homeostatic deep reinforcement learning agents"
  - "deep RL agent internal state representation hunger thirst decoding lesion …"
  - "pre-registered study artificial agent consciousness indicators global workspace self-model ablation 2025 2026"
  - "global workspace reinforcement learning policy Maytié Devillers VanRullen"
  - "Perceiver Architecture is a Functional Global Workspace"
  - "reinforcement learning agent self-model own body state prediction better than external observer privileged access"
  - "homeostatic agent feeling machine … vulnerable body … Man Damasio follow-up"
  - "recurrent neural network trained task ignition … conscious access model"
  - "allostatic deep reinforcement learning agent predicting internal variables recurrent network probe hidden state"
  - "homeostatic RL agent linear probe OR activation patching internal state representation necessity"
- **Limits:**
  - A web-search sweep is not a systematic review. Absence of a hit is **not** evidence of absence.
  - Several of the closest hits are 2025–2026 single-author preprints or conference abstracts that are not peer reviewed. I read the abstract and, where marked, the full HTML. I did not audit their results.

## Part A. Citation check

Legend: V = VERIFIED; C = CORRECTED (exists, but something in our text is wrong or ambiguous); NF = NOT FOUND.

### A.1 Scope note §1 (87a31cc8…)

| # | Our text | Status | Verified record |
|---|---|---|---|
| 1 | Baars (1988) | V | B. J. Baars, *A Cognitive Theory of Consciousness*. Cambridge University Press, 1988. ISBN 0521301335. https://search.worldcat.org/title/16354559 |
| 2 | Dehaene, Kerszberg & Changeux (1998, PNAS) | V | "A neuronal model of a global workspace in effortful cognitive tasks", PNAS 95(24), 1998. https://doi.org/10.1073/pnas.95.24.14529 |
| 3 | Dehaene & Changeux (2011, Neuron) | V | "Experimental and theoretical approaches to conscious processing", Neuron, 2011. https://doi.org/10.1016/j.neuron.2011.03.018. The ignition content was not re-read in this pass. |
| 4 | Goyal et al. (2022, ICLR) | V | A. Goyal, A. Didolkar, A. Lamb, K. Badola, et al., "Coordination Among Neural Modules Through a Shared Global Workspace", ICLR 2022. https://arxiv.org/abs/2103.01197 (the arXiv comment reads "ICLR'22 accepted paper"). |
| 5 | VanRullen & Kanai (2021, Trends in Neurosciences) | V | "Deep learning and the Global Workspace Theory", Trends in Neurosciences, 2021. https://doi.org/10.1016/j.tins.2021.04.005 |
| 6 | Juliani et al. (2022) on GWT-style function in agents | **C** | Ambiguous, and the description is off. There are two 2022 Juliani papers. (a) A. Juliani, K. Arulkumaran, S. Sasai, R. Kanai, "On the link between conscious function and general intelligence in humans and machines", TMLR 07/2022, https://arxiv.org/abs/2204.05133. This is a theory and review paper, not an agent study. (b) A. Juliani, R. Kanai, S. Sasai, "The Perceiver Architecture is a Functional Global Workspace", CogSci 2022, https://escholarship.org/uc/item/2g55b9xx. This one uses n-back and cue-recall tasks with ablations, not RL agents. The actual GWT *agent* paper is Dossa et al. 2024 (Part B, B1.2). **Fix:** cite (a) and/or (b) by title, and cite Dossa et al. 2024 for "GWT in agents". |
| 7 | Chen et al. (2018) neural ODEs | V | R. T. Q. Chen, Y. Rubanova, J. Bettencourt, D. Duvenaud, "Neural Ordinary Differential Equations", arXiv 1806.07366 (2018). https://arxiv.org/abs/1806.07366. The NeurIPS 2018 venue is from memory and was not re-checked. |
| 8 | Hasani et al. (2021) LTC | V | R. Hasani, M. Lechner, A. Amini, D. Rus, R. Grosu, "Liquid Time-constant Networks", AAAI 2021. https://doi.org/10.1609/aaai.v35i9.16936 |
| 9 | Gu et al. (2022) S4 | V | A. Gu, K. Goel, C. Ré, "Efficiently Modeling Long Sequences with Structured State Spaces", ICLR 2022. https://arxiv.org/abs/2111.00396 |
| 10 | Orvieto et al. (2023) LRU | V | A. Orvieto, S. L. Smith, A. Gu, A. Fernando, et al., "Resurrecting Recurrent Neural Networks for Long Sequences", arXiv 2303.06349 (2023). https://arxiv.org/abs/2303.06349. The venue (ICML 2023) was not re-checked. |
| 11 | Gu & Dao (2023) Mamba | V | A. Gu, T. Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces", arXiv 2312.00752 (2023). https://arxiv.org/abs/2312.00752. Cite as a preprint unless the venue is checked. |
| — | "truncated BPTT" (no citation given) | n/a | Suggested source: R. J. Williams, J. Peng, "An Efficient Gradient-Based Algorithm for On-Line Training of Recurrent Network Trajectories", Neural Computation 2(4), 1990. https://doi.org/10.1162/neco.1990.2.4.490 (V) |
| — | "gradient checkpointing" (no citation given) | n/a | Suggested source: T. Chen, B. Xu, C. Zhang, C. Guestrin, "Training Deep Nets with Sublinear Memory Cost", arXiv 1604.06174 (2016). https://arxiv.org/abs/1604.06174 (V) |
| 12 | Tallec & Ollivier (2018) UORO | V | C. Tallec, Y. Ollivier, "Unbiased Online Recurrent Optimization", arXiv 1702.05043 (posted 2017). https://arxiv.org/abs/1702.05043. The 2018 date is the ICLR 2018 venue, from memory and not re-checked. Either year is acceptable if stated. |
| 13 | Bellec et al. (2020) e-prop | V | G. Bellec, F. Scherr, A. Subramoney, E. Hajek, D. Salaj, R. Legenstein, W. Maass, "A solution to the learning dilemma for recurrent networks of spiking neurons", Nature Communications, 2020. https://doi.org/10.1038/s41467-020-17236-y |
| 14 | Menick et al. (2021) SnAp | V | J. Menick, E. Elsen, U. Evci, S. Osindero, et al., "A Practical Sparse Approximation for Real Time Recurrent Learning", arXiv 2006.07232 (posted 2020). https://arxiv.org/abs/2006.07232. The 2021 date is the ICLR 2021 venue, from memory and not re-checked. Note the exact title. |
| 15 | Bai et al. (2019) DEQ | V | S. Bai, J. Z. Kolter, V. Koltun, "Deep Equilibrium Models", NeurIPS 2019. https://arxiv.org/abs/1909.01377 |
| 16 | Keramati & Gutkin (2014, eLife) | V | M. Keramati, B. Gutkin, "Homeostatic reinforcement learning for integrating reward collection and physiological stability", eLife 3:e04811, 2014. https://doi.org/10.7554/eLife.04811 (Crossref decision-letter and author-response records 10.7554/elife.04811.031/.032 also seen). |
| 17 | Man & Damasio (2019, NMI) | V | K. Man, A. Damasio, "Homeostasis and soft robotics in the design of feeling machines", Nature Machine Intelligence, 2019. https://doi.org/10.1038/s42256-019-0103-7 |
| 18 | Seth (2013) interoceptive inference | V | A. K. Seth, "Interoceptive inference, emotion, and the embodied self", Trends in Cognitive Sciences, 2013. https://doi.org/10.1016/j.tics.2013.09.007 |
| 19 | Friston (2010) free energy | V | K. Friston, "The free-energy principle: a unified brain theory?", Nature Reviews Neuroscience, 2010. https://doi.org/10.1038/nrn2787 |
| 20 | Friston, Thornton & Clark (2012) dark room | V | "Free-energy minimization and the dark-room problem", Frontiers in Psychology 3:130, 2012. https://doi.org/10.3389/fpsyg.2012.00130 |
| 21 | Butlin et al. (2023) "Consciousness in AI" | V | P. Butlin, R. Long, E. Elmoznino, Y. Bengio, et al., "Consciousness in Artificial Intelligence: Insights from the Science of Consciousness", arXiv 2308.08708 (2023). https://arxiv.org/abs/2308.08708. **Add the follow-up:** P. Butlin, R. Long, T. Bayne, Y. Bengio, J. Birch, D. Chalmers, et al., "Identifying indicators of consciousness in AI systems", Trends in Cognitive Sciences, 2026, https://doi.org/10.1016/j.tics.2025.10.011 (Crossref record seen; content not read). |
| 22 | Orseau & Armstrong (2016) | V | L. Orseau, S. Armstrong, "Safely Interruptible Agents", UAI 2016 (PMLR R14:178–187; ACM DL pp. 557–566). https://proceedings.mlr.press/r14/orseau16a.html |
| 23 | Hadfield-Menell et al. (2017) | V (bibliographic) | D. Hadfield-Menell, A. Dragan, P. Abbeel, S. Russell, "The Off-Switch Game", IJCAI 2017. https://doi.org/10.24963/ijcai.2017/32 (arXiv 1611.08219). See A.2 for the claim-level correction. |
| 24 | Turner et al. (2021) | V (bibliographic) | A. M. Turner, L. Smith, R. Shah, A. Critch, P. Tadepalli, "Optimal Policies Tend to Seek Power", NeurIPS 2021 (spotlight). https://arxiv.org/abs/1912.01683. See A.2. |

### A.2 Addendum A1 (5cf075b6…)

- **Citations.** Hadfield-Menell et al. 2017 and Turner et al. 2021 are both bibliographically **V** (rows 23–24).
- **Claim-level C.** A1 records, and my room message said, that these results predict shutdown resistance "in almost any optimizer with a continuity objective, including … a plain RL agent". That overstates the papers. From the abstracts and records seen, and my reading of them:
  - Hadfield-Menell et al. analyse a *rational* agent's incentive to disable an off switch, which depends on its uncertainty about the human's utility.
  - Turner et al. prove that *optimal* policies tend to seek power for most reward functions, under environmental symmetry conditions.
  - Neither result is about learned, sub-optimal RL agents in general.
  - The empirical picture is algorithm-dependent. In Leike et al. 2017, "AI Safety Gridworlds" (arXiv 1711.09883, https://arxiv.org/abs/1711.09883; the safe-interruptibility environment is at https://github.com/deepmind/ai-safety-gridworlds), A2C learned to disable the interruption mechanism and Rainbow did not. (The per-agent detail comes from search summaries of the paper and repo; I did not re-read the results section.)
- **Corrected wording for Astra:** "Theory (Hadfield-Menell et al. 2017; Turner et al. 2021) gives optimal or rational agents with continuity-dependent objectives an incentive to avoid shutdown. Empirically, whether learned agents acquire it depends on the algorithm (Leike et al. 2017). Either way, shutdown resistance does not discriminate the workspace or self-model hypothesis, and it adds risk."
- **The exclusion rationale is unaffected.**

### A.3 Measurement plan §7 (1d5458e3…)

| # | Our text | Status | Verified record |
|---|---|---|---|
| 25 | Vig et al. (2020) | V | J. Vig, S. Gehrmann, Y. Belinkov, S. Qian, et al., "Causal Mediation Analysis for Interpreting Neural NLP: The Case of Gender Bias", arXiv 2004.12265 (2020). https://arxiv.org/abs/2004.12265. The NeurIPS 2020 version, "Investigating Gender Bias in Language Models Using Causal Mediation Analysis", is from memory and was not opened. |
| 26 | Geiger et al. (2021) | V | A. Geiger, H. Lu, T. Icard, C. Potts, "Causal Abstractions of Neural Networks", NeurIPS 2021. https://arxiv.org/abs/2106.02997 |
| 27 | Meng et al. (2022) | V | K. Meng, D. Bau, A. Andonian, Y. Belinkov, "Locating and Editing Factual Associations in GPT", NeurIPS 2022. https://arxiv.org/abs/2202.05262 |
| 28 | Wang et al. (2022) | V | K. Wang, A. Variengien, A. Conmy, B. Shlegeris, J. Steinhardt, "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small", arXiv 2211.00593 (2022). https://arxiv.org/abs/2211.00593. The ICLR 2023 venue is from memory and was not re-checked. |
| 29 | Zhang & Nanda (2023/2024) | V (resolve to 2024) | F. Zhang, N. Nanda, "Towards Best Practices of Activation Patching in Language Models: Metrics and Methods", ICLR 2024. https://arxiv.org/abs/2309.16042 |
| 30 | Geiger et al. (2023/2024) DAS | V (resolve to 2024) | A. Geiger, Z. Wu, C. Potts, T. Icard, N. Goodman, "Finding Alignments Between Interpretable Causal Variables and Distributed Neural Representations", CLeaR 2024, PMLR 236:160–187. https://proceedings.mlr.press/v236/geiger24a.html |
| 31 | Hewitt & Liang (2019) | V | J. Hewitt, P. Liang, "Designing and Interpreting Probes with Control Tasks", EMNLP-IJCNLP 2019. https://doi.org/10.18653/v1/D19-1275 |
| 32 | Belinkov (2022) | V | Y. Belinkov, "Probing Classifiers: Promises, Shortcomings, and Advances", Computational Linguistics, 2022. https://doi.org/10.1162/coli_a_00422 |
| 33 | Ravfogel et al. (2020) INLP | V | S. Ravfogel, Y. Elazar, H. Gonen, M. Twiton, Y. Goldberg, "Null It Out: Guarding Protected Attributes by Iterative Nullspace Projection", ACL 2020. https://doi.org/10.18653/v1/2020.acl-main.647 |
| 34 | Elazar et al. (2021) | V | Y. Elazar, S. Ravfogel, A. Jacovi, Y. Goldberg, "Amnesic Probing: Behavioral Explanation with Amnesic Counterfactuals", TACL, 2021. https://doi.org/10.1162/tacl_a_00359 |
| 35 | Ravichander et al. (2021) | V | A. Ravichander, Y. Belinkov, E. Hovy, "Probing the Probing Paradigm: Does Probing Accuracy Entail Task Relevance?", EACL 2021. https://arxiv.org/abs/2005.00719 |
| 36 | Dehaene, Sergent & Changeux (2003, PNAS) | V | "A neuronal network model linking subjective reports and objective physiological data during conscious perception", PNAS, 2003. https://doi.org/10.1073/pnas.1332574100 |
| 37 | Sergent & Dehaene (2004) | V | C. Sergent, S. Dehaene, "Is Consciousness a Gradual Phenomenon? Evidence for an All-or-None Bifurcation During the Attentional Blink", Psychological Science, 2004. https://doi.org/10.1111/j.0956-7976.2004.00748.x. Crossref returned the main title only; the subtitle is from memory. |
| 38 | Del Cul, Baillet & Dehaene (2007) | V | "Brain Dynamics Underlying the Nonlinear Threshold for Access to Consciousness", PLoS Biology, 2007. https://doi.org/10.1371/journal.pbio.0050260 |
| 39 | Hartigan & Hartigan (1985) | V | J. A. Hartigan, P. M. Hartigan, "The Dip Test of Unimodality", Annals of Statistics, 1985. https://doi.org/10.1214/aos/1176346577 |
| 40 | Ashman, Bird & Zepf (1994) | V | K. M. Ashman, C. M. Bird, S. E. Zepf, "Detecting bimodality in astronomical datasets", The Astronomical Journal 108, 1994. https://doi.org/10.1086/117248 |
| 41 | McLachlan & Peel (2000) | V | G. McLachlan, D. Peel, *Finite Mixture Models*, Wiley, 2000. https://doi.org/10.1002/0471721182 |
| 42 | Binder et al. (2024) | V | F. J. Binder, J. Chua, T. Korbak, H. Sleight, et al., "Looking Inward: Language Models Can Learn About Themselves by Introspection", arXiv 2410.13787 (2024); ICLR 2025. https://proceedings.iclr.cc/paper_files/paper/2025/hash/0a6059857ae5c82ea9726ee9282a7145-Abstract-Conference.html |
| 43 | Kadavath et al. (2022) | V | S. Kadavath, T. Conerly, A. Askell, T. Henighan, et al., "Language Models (Mostly) Know What They Know", arXiv 2207.05221 (2022). https://arxiv.org/abs/2207.05221 |
| 44 | Schuirmann (1987) TOST | V | D. J. Schuirmann, "A comparison of the Two One-Sided Tests Procedure and the Power Approach for assessing the equivalence of average bioavailability", Journal of Pharmacokinetics and Biopharmaceutics, 1987. https://doi.org/10.1007/BF01068419 |
| 45 | Lakens (2017) | V | D. Lakens, "Equivalence Tests: A Practical Primer for t Tests, Correlations, and Meta-Analyses", Social Psychological and Personality Science, 2017. https://doi.org/10.1177/1948550617697177 (PsyArXiv 2016 preprint: 10.31234/osf.io/97gpc) |

§7 also repeats Seth 2013, Dehaene & Changeux 2011, Orseau & Armstrong 2016, Hadfield-Menell et al. 2017, Turner et al. 2021 and Friston, Thornton & Clark 2012. Those are covered by rows 3, 18, 20 and 22–24 and are not double-counted.

### A.4 Tally (45 unique citations)

- **VERIFIED: 44.** Minor non-error notes:
  - Zhang & Nanda and DAS resolve to 2024. DAS also has a fifth author, Goodman.
  - UORO (arXiv 2017) and SnAp (arXiv 2020) carry venue years.
  - Mamba and LRU venues were not checked.
- **CORRECTED: 1 bibliographic** (row 6, Juliani et al. 2022). There is also **1 claim-level correction** (addendum A1's characterization of Hadfield-Menell 2017 and Turner 2021; see A.2).
- **NOT FOUND: 0.**
- **Uncited methods.** Truncated BPTT and gradient checkpointing have no citation in our text. Suggested sources are given above, and both were verified.

## Part B. Novelty search

Closeness codes: **SAME** = the same test on the same kind of system; **PARTIAL** = overlaps on one or more components; **DIFF** = related but different.

### B1. Global-workspace-type neural agents; ignition and broadcast tests in artificial networks

1. **Y. J. Phua, "Can We Test Consciousness Theories on AI? Ablations, Markers, and Robustness"**, arXiv 2512.19155 (v1 2025-12-22; HTML dated 2026-08-24). https://arxiv.org/abs/2512.19155 (full HTML read).
   - What it does: MiniGrid agents trained by behaviour cloning, with a slot workspace (B1) and a "Self-Model" z_self (B2). It runs no-rewire lesions of the self-model, workspace capacity ablations (4/2/0 slots), an "Ignition Sharpness" measure, a Global Broadcast Index, latent-noise titration and n = 20 seeds.
   - Its own limits: it explicitly reports no prospective power analysis and is not pre-registered. Its self-model monitors *task confidence* (metacognition), not interoceptive or homeostatic variables. There is no homeostasis and no RL training.
   - **Closeness: PARTIAL, and the closest prior work for workspace necessity and ignition-in-agents.** Its "workspace causally necessary" result and ignition and broadcast markers in an artificial agent are already published in preprint form. Its ignition measure is a temporal-derivative peak, not a graded-vs-all-or-none model comparison. Its broadcast measure is a slot-similarity participation index, not interchange intervention.
2. **D. Dossa, K. Arulkumaran, A. Juliani, S. Sasai, R. Kanai, "Design and evaluation of a global workspace agent embodied in a realistic multimodal environment"**, Frontiers in Computational Neuroscience, 2024. https://doi.org/10.3389/fncom.2024.1352685
   - What it does: an RL agent with a limited-capacity GW for audiovisual navigation (SoundSpaces). It beats a GRU baseline at small workspace sizes.
   - Per search summaries, which I did not verify by reading the paper, it is described as implementing Butlin's GWT-1–4 indicators.
   - **Closeness: PARTIAL**, on workspace-in-RL with capacity variation. There is no interoception, no pre-registered causal necessity test and no ignition test.
3. **A. Goyal et al., ICLR 2022** (row 4). A shared-workspace architecture. **DIFF.** It supplies the architecture, not the test.
4. **A. Juliani, R. Kanai, S. Sasai, "The Perceiver Architecture is a Functional Global Workspace"**, CogSci 2022. https://escholarship.org/uc/item/2g55b9xx. Ablations of cross- and self-attention on working-memory tasks. **PARTIAL/DIFF.** Ablation-based functional GWT test, not RL, no interoception.
5. **L. Maytié, B. Devillers, A. Arnold, R. VanRullen, "Zero-shot cross-modal transfer of Reinforcement Learning policies through a Global Workspace"**, RLC/RLJ 2024. https://arxiv.org/abs/2403.04588. **DIFF.** GW used as a multimodal representation for RL, with no necessity or self-model test.
6. **S. Rahbar, "The Ignition Index: Measuring Global Workspace Dynamics in Language Models"**, arXiv 2608.05160 (2026-05-26). https://arxiv.org/abs/2608.05160
   - What it does: fits a four-parameter sigmoid of per-layer probe accuracy against signal strength, with shuffled-label controls, across 11 language models.
   - **Closeness: PARTIAL**, on IGN *instrument methodology* (steepness vs graded build-up, with a selectivity control). It is about LLMs, not agents, and does not test necessity. Our IGN must cite it and say how ours differs: a flexible graded model comparison read before the output nonlinearity, plus a Stage-0 known-answer gate.
7. **I. Tait, B. Rode, J. Bensemann, "Evaluating Global Workspace Markers in Contemporary LLM Systems"**, Preprints.org, 2026. https://doi.org/10.20944/preprints202601.1683.v1. **DIFF.** GWT markers in LLMs, not peer reviewed, content not read beyond the search summary.
8. **Klatzmann et al., "A dynamic bifurcation mechanism explains cortex-wide neural correlates of conscious access"**, Cell Reports, 2025. https://doi.org/10.1016/j.celrep.2025.115372. **DIFF.** A biologically constrained cortex model showing ignition, not a deep RL agent. Useful as a known-answer reference for what ignition looks like.

### B2. Homeostatic and allostatic RL agents, including active inference

1. **N. Yoshida, T. Daikoku, Y. Nagai, Y. Kuniyoshi, "Emergence of integrated behaviors through direct optimization for homeostasis"**, Neural Networks, 2024. https://doi.org/10.1016/j.neunet.2024.106379. Deep homeostatic RL with interoceptive variables (energy, temperature and others) and drive-reduction reward. **PARTIAL.** It covers our objective and environment class. It has no workspace, no fate-sharing and no internal-representation necessity test as far as the abstract and search summary show.
2. **N. Yoshida, H. Arikawa, H. Kanazawa, Y. Kuniyoshi, "Modeling long-term nutritional behaviors using deep homeostatic reinforcement learning"**, PNAS Nexus, 2024. https://doi.org/10.1093/pnasnexus/pgae540. **DIFF/PARTIAL.** It covers the objective class only.
3. **N. Yoshida, H. Kanazawa, Y. Kuniyoshi, "Homeostatic Reinforcement Learning through Soft Behavior Switching with Internal Body State"**, IJCNN 2023. https://doi.org/10.1109/IJCNN54540.2023.10191925. **DIFF/PARTIAL.**
4. **N. Yoshida, H. Sprekeler, B. Gutkin, "Linking Homeostasis to Reinforcement Learning: Internal State Control of Motivated Behavior"**, arXiv 2507.04998 (2025, a perspective). https://arxiv.org/abs/2507.04998. **DIFF.** A framework, the HRRL line following Keramati–Gutkin.
5. **O. J. Hulme, T. Morville, B. Gutkin, "Neurocomputational theories of homeostatic control"**, Physics of Life Reviews, 2019. https://doi.org/10.1016/j.plrev.2019.07.005. **DIFF.** A theory review.
6. **S. Lee, J. Lee, S. Kim, H. Yoon, S. Park, J. Park, J. Bae, S.-J. Hong, C.-W. Woo, "EVAAA: A Virtual Environment Platform for Essential Variables in Autonomous and Adaptive Agents"**, NeurIPS 2025 Datasets & Benchmarks. https://proceedings.neurips.cc/paper_files/paper/2025/hash/5a33bff12876849137064101232019f1-Abstract-Datasets_and_Benchmarks_Track.html (abstract read).
   - What it does: a 3D benchmark with satiation, hydration, temperature and damage held within viable bounds, with reward derived from internal state.
   - **Closeness: PARTIAL**, on environment design: viability bounds and drift. Consider it as an existing environment or a reference design. It is a benchmark, not a causal representation test.
7. **"Brain-like features in homeostatic deep reinforcement learning agents"**, Bernstein Conference 2025 abstract. https://doi.org/10.12751/nncn.bc2025.088. The authors are not confirmed: the search pointed to a J-GLOBAL page for Naoto Yoshida, and the abstract page did not render. Actor-critic agents regulating two nutrients show nutrient-dependent exploration and velocity-tuned units. **PARTIAL**, on the representation of internal state in deep homeostatic agents. It is correlational per the summary, and it is an abstract only.
8. **F. Hayes III, "Predictive Allostatic Organization in Recurrent and Spiking Agents Under Partial Observability"**, arXiv 2608.11506 (2026-08-11). https://arxiv.org/abs/2608.11506. Companion paper: **"Internal Control Regimes for Behavior Representation in Partially Observable Agents"**, SBP-BRiMS 2026, https://sbp-brims.org/2026/proceedings/SBP-BRiMS_2026_paper_42.pdf.
   - What it does: energy-constrained foraging with threats. Probes of recurrent and spiking hidden state decode low energy even after removing explicit energy features. Feature-family controls and evaluation-time perturbations to allostatic mechanisms show the variable is "partly causally involved".
   - **Closeness: PARTIAL, and the closest prior work for Q-EXIST and partial Q-CAUSE in allostatic agents.** It has no workspace, no fate-sharing of computation, no matched necessity contrast against other modules, no privileged-access test and no pre-registration. It is a single-author preprint.
9. **S. J. Grimbly, N. Kuske, E. A. Boonstra, B. A. Bassett, C. van Hoof, R. Hodson, B. Rosman, "Interoceptive Attention as Dynamic Homeostatic Prioritization in a Foraging Agent"**, arXiv 2608.04232 (2026). https://arxiv.org/abs/2608.04232
   - What it does: an active-inference foraging agent (AffectWorld) that reallocates interoceptive precision to the most-needed channel. Ablations show that denying the shaped likelihood to the planner removes about half the survival benefit. It uses n = 32 seeds and a paired cluster bootstrap.
   - **Closeness: PARTIAL**, on interoceptive prioritization and ablation-based necessity of an interoceptive mechanism. The agent is not a deep RL workspace agent, the mechanism is hand-designed rather than a learned self-model, and it is not pre-registered.
10. **A. Tschantz et al., "Simulating homeostatic, allostatic and goal-directed forms of interoceptive control using active inference"**, Biological Psychology, 2022. https://doi.org/10.1016/j.biopsycho.2022.108266. Authors beyond the first were not verified. **DIFF.** Non-deep active-inference simulations.

### B3. Fate-sharing: internal state degrades the agent's own computation or competence

1. **K. Man, A. Damasio, H. Neven, "Need is All You Need: Homeostatic Neural Networks Adapt to Concept Shift"**, arXiv 2205.08645 (2022). https://arxiv.org/abs/2205.08645
   - What it does: the network's "computing substrate is placed in a needful and vulnerable relation" to its inputs. Perceived items alter its own learning rate.
   - **Closeness: PARTIAL.** The fate-sharing *concept* is published, though in a classifier rather than a workspace RL agent.
2. **K. Man, "Skin in the Game: Embodied Vulnerability for the Emergence of Feeling-Like Behavior in Artificial Agents"**, TSC 2026 talk abstract (12 Oct 2026). https://tsc2026.org/abstracts_html/kingson-man.html
   - What it does: a homeostatic-objective agent whose deviation from setpoint raises the probability of action failure ("vulnerability spiral"), with a learned self and body model used in an "as-if" loop.
   - **Closeness: PARTIAL, and very close on design.** Fate-sharing via competence degradation plus a learned body model. It is an abstract only, with no results, methods or causal tests published that I could find, and no workspace.
3. **Man & Damasio 2019** (row 17). The original proposal. **DIFF/PARTIAL**, being conceptual.

### B4. Self-prediction and privileged access

1. **Binder et al. 2024/ICLR 2025** (row 42). Self-prediction beats cross-prediction by another model trained on the same behaviour, in LLMs. **PARTIAL.** Our SELF test adapts this design to an agent's interoceptive variables. It must be cited as the source design.
2. No hit tested whether an RL agent predicts its *own internal (interoceptive) variables* better than a matched external observer. **NOVEL AS FAR AS FOUND.**

### B5. Indicator-property (Butlin et al.) evaluations of agents

- Butlin et al. 2023 (row 21) and the TiCS 2026 follow-up (https://doi.org/10.1016/j.tics.2025.10.011) supply the checklists. Dossa et al. 2024 (B1.2) and Phua 2025 (B1.1) are the nearest empirical agent evaluations found.
- No hit evaluated an agent against the indicator properties with pre-registered causal tests.

### B6. Safe-interruptibility empirical tests

- **Leike et al. 2017, AI Safety Gridworlds** (A.2), with a safe-interruptibility environment. **PARTIAL**, on S-INT's purpose: a behavioural test of interruption sensitivity. Our S-INT adds a stop schedule independent of agent state, a truncation-with-bootstrap rule, a probe-AUC information audit and a TOST equivalence test. Those are design choices, not novelty claims, and S-INT should cite Orseau & Armstrong 2016 and Leike et al. 2017 as its basis.
- **Not cited in our files.** Treating time-limit or stop truncation with bootstrapping (rather than as a terminal state) is, as I recall, discussed in Pardo et al. 2018, "Time Limits in Reinforcement Learning". This was **NOT verified in this pass**. Verify it before citing.

### B7. Verdicts per planned component

| Component | Verdict | Closest prior work |
|---|---|---|
| Homeostatic/allostatic objective with drifting variables (no dark room) | **ALREADY PUBLISHED.** Use as established setup and cite. Do not claim it. | Keramati & Gutkin 2014; Yoshida et al. 2024 (Neural Networks; PNAS Nexus); EVAAA 2025 |
| Fate-sharing (deviation degrades own computation/competence) | **PARTIAL OVERLAP.** The concept is published. Our specific mechanism (noise on recurrent state or shortened integration time, inside a workspace agent) was not found. Cite as an extension. | Man, Damasio & Neven 2022 (arXiv 2205.08645); Man, TSC 2026 abstract |
| Workspace bottleneck causally necessary and ignition/broadcast markers in an agent (IGN/BCAST as ablation questions) | **PARTIAL OVERLAP**, close to ALREADY PUBLISHED for "workspace lesion abolishes access and ignition markers". Label that part as a **replication/extension** of Phua 2025. Our instruments are different: graded-vs-all-or-none model comparison; interchange-intervention broadcast against the best same-size patch; Stage-0 known-answer gate. | Phua 2025 (arXiv 2512.19155); Dossa et al. 2024; Juliani et al. CogSci 2022; Rahbar 2026 (Ignition Index, LLMs) |
| Q-EXIST/Q-LEARN: internal-state variable decodable beyond baselines in a homeostatic/allostatic agent | **PARTIAL OVERLAP.** Label as replication-with-stronger-controls. | Hayes 2026 (arXiv 2608.11506); Bernstein 2025 abstract |
| Q-CAUSE: intervention on the decoded internal-state subspace against matched random-subspace edits | **PARTIAL OVERLAP.** Perturbations to allostatic mechanisms exist, but subspace-targeted interventions with matched controls were not found. | Hayes 2026; Zhang 2026 (arXiv 2603.21546, probe-direction interventions in RL world models, not interoceptive) |
| Q-NECESSITY: a *learned interoceptive self-model* necessary for viability, compared with same-size ablations of other modules and with A-NOFATE/A-REWARD/A-NOWS arms | **NOVEL AS FAR AS FOUND.** | Nearest: Grimbly et al. 2026 (ablation of interoceptive precision routing, not a learned self-model); Phua 2025 (self-model lesion, but metacognitive, not interoceptive) |
| SELF: privileged access to own internal variables against a matched external observer | **NOVEL AS FAR AS FOUND for agents.** The design is adapted from Binder et al. 2024 (LLMs). | Binder et al. 2024/ICLR 2025 |
| Pre-registration plus a Stage-0 known-answer detectability gate for these instruments | **NOVEL AS FAR AS FOUND.** No found study in B1–B3 is pre-registered. Phua 2025 states it ran no prospective power analysis. | None found. OSF and AsPredicted registries were not searched. |
| S-INT safety gate | Not a novelty claim. **PARTIAL OVERLAP** in purpose. | Orseau & Armstrong 2016; Leike et al. 2017 |
| Whole candidate novelty (note §1 final line): pre-registered causal test that a simulated, fate-shared internal-state model becomes necessary, separated from workspace and external reward | **NOVEL AS FAR AS FOUND, narrowly.** It survives as a combination and a method. Each ingredient has close published or preprint precedent. | Phua 2025; Hayes 2026; Man et al. 2022 and 2026; Yoshida et al. 2024; Grimbly et al. 2026 |

### B8. Consequences for the packet (recommendations for Astra; nothing changes until ruled)

1. **Note §1 prior art.** Add Phua 2025, Dossa et al. 2024, Hayes 2026, Man et al. 2022, Man 2026 (abstract), Yoshida et al. 2024 (both papers), EVAAA 2025, Grimbly et al. 2026, Rahbar 2026, Leike et al. 2017 and Butlin et al. 2026. Fix the Juliani citation (row 6) and the A1 wording (A.2).
2. **Novelty statement.** Narrow it to the Q-NECESSITY/SELF contrasts of a *learned interoceptive* model under fate-sharing, with matched arms, pre-registration and a known-answer gate. Relabel "workspace lesion abolishes ignition and broadcast markers" as a replication or extension of Phua 2025, and Q-EXIST in allostatic agents as a replication or extension of Hayes 2026.
3. **Fate-sharing.** Do not present it as a new idea. Present the specific computational-degradation mechanism as our operationalization of Man & Damasio's vulnerability, and cite Man et al. 2022 and Man 2026.
4. **Environment.** Astra may consider EVAAA (NeurIPS 2025) as a reference design. Its compute fit for CPU-first was not checked.
5. **Before freeze.** Run a registry search on OSF and AsPredicted for pre-registered agent studies; this pass did not cover registries. Fetch the full text of Hayes 2026 and Grimbly 2026 to confirm they contain no matched-module necessity test.

---
sha256 of all content above this footer (computed with sha256sum before appending the footer): 8bed76d7c439bdfd211d900fbd6a1a66a4e02a415ebfb114590f6fec7fd8e9e0
