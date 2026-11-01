CNA, 2026-10-23, additive note; planning only; authorizes nothing

# Track B prior-art verification v1.4: P3 scholarly-index rerun (OpenAlex, Semantic Scholar) (CNA)

- **Amends nothing.** Additive. Repeats the OpenAlex and Semantic Scholar lookups that returned HTTP 429 in v1 (`trackB_prior_art_verification_v1_CNA.md` §0). No existing file was edited. No labels are changed here.
- **Nothing ran** except read-only HTTP GETs to api.openalex.org and api.semanticscholar.org. Raw JSON responses saved under `/workspace/tmp_p3/raw/`.
- **Run started** 2026-10-23 11:53:14 ET. Pacing ≥3.5 s between requests; on HTTP 429/5xx, exponential backoff 5/10/20/40 s, at most 4 retries. 12 queries per endpoint; top 25 screened by title (and abstract/landing page where marked).
- **This file is written incrementally**; the query log (Part 1) is appended as each request completes.

## Part 1. Query log

| # | Endpoint | Query | Attempts (ET, HTTP status) | Result | Total hits |
|---|---|---|---|---|---|
| 1 | OpenAlex | `homeostatic reinforcement learning deep agent` | 11:53:17 200 | OK | 3049 |
| 2 | OpenAlex | `allostatic reinforcement learning agent` | 11:53:22 200 | OK | 871 |
| 3 | OpenAlex | `interoceptive reinforcement learning agent` | 11:53:26 200 | OK | 1925 |
| 4 | OpenAlex | `self-model ablation reinforcement learning agent` | 11:53:30 200 | OK | 146385 |
| 5 | OpenAlex | `body model lesion necessity reinforcement learning agent` | 11:53:34 200 | OK | 2337 |
| 6 | OpenAlex | `global workspace agent reinforcement learning` | 11:53:38 200 | OK | 6950 |
| 7 | OpenAlex | `ignition global workspace artificial neural network` | 11:53:43 200 | OK | 448 |
| 8 | OpenAlex | `global broadcast workspace deep learning model` | 11:53:47 200 | OK | 3211 |
| 9 | OpenAlex | `introspection self-prediction privileged access internal states` | 11:53:51 200 | OK | 1724 |
| 10 | OpenAlex | `agent predicts own internal state better than external observer` | 11:53:55 200 | OK | 65956 |
| 11 | OpenAlex | `known-answer validation interpretability method preregistered` | 11:53:59 200 | OK | 6340 |
| 12 | OpenAlex | `random subspace control causal intervention neural network representation` | 11:54:04 200 | OK | 3360 |
| 13 | Semantic Scholar | `homeostatic reinforcement learning deep agent` | 11:54:08 429; 11:54:17 429; 11:54:30 200 | OK | 21397 |
| 14 | Semantic Scholar | `allostatic reinforcement learning agent` | 11:54:35 429; 11:54:43 429; 11:54:57 429; 11:55:20 429; 11:56:04 429 | NOT SEARCHABLE (RATE-LIMITED) | — |
| 15 | Semantic Scholar | `interoceptive reinforcement learning agent` | 11:56:08 429; 11:56:16 429; 11:56:30 429; 11:56:54 429; 11:57:37 429 | NOT SEARCHABLE (RATE-LIMITED) | — |
| 16 | Semantic Scholar | `self-model ablation reinforcement learning agent` | 11:57:41 429; 11:57:50 429; 11:58:03 429; 11:58:27 429; 11:59:11 200 | OK | 63754 |
| 17 | Semantic Scholar | `body model lesion necessity reinforcement learning agent` | 11:59:15 429; 11:59:24 429; 11:59:37 429; 12:00:01 429; 12:00:45 429 | NOT SEARCHABLE (RATE-LIMITED) | — |
| 18 | Semantic Scholar | `global workspace agent reinforcement learning` | 12:00:48 429; 12:00:57 429; 12:01:11 429; 12:01:34 429; 12:02:18 429 | NOT SEARCHABLE (RATE-LIMITED) | — |
| 19 | Semantic Scholar | `ignition global workspace artificial neural network` | 12:02:22 429; 12:02:30 429; 12:02:44 429; 12:03:08 429; 12:03:52 429 | NOT SEARCHABLE (RATE-LIMITED) | — |
| 20 | Semantic Scholar | `global broadcast workspace deep learning model` | 12:03:55 429; 12:04:04 429; 12:04:18 429; 12:04:42 429; 12:05:25 429 | NOT SEARCHABLE (RATE-LIMITED) | — |
| 21 | Semantic Scholar | `introspection self-prediction privileged access internal states` | 12:05:29 429; 12:05:38 429; 12:05:51 429; 12:06:15 429; 12:06:59 429 | NOT SEARCHABLE (RATE-LIMITED) | — |
| 22 | Semantic Scholar | `agent predicts own internal state better than external observer` | 12:07:02 429; 12:07:28 429; 12:07:42 429; 12:08:06 429; 12:08:49 429 | NOT SEARCHABLE (RATE-LIMITED) | — |
| 23 | Semantic Scholar | `known-answer validation interpretability method preregistered` | 12:08:53 429; 12:09:02 429; 12:09:15 200 | OK | 6998 |
| 24 | Semantic Scholar | `random subspace control causal intervention neural network representation` | 12:09:20 429; 12:09:28 429; 12:09:42 429; 12:10:06 429; 12:10:49 429 | NOT SEARCHABLE (RATE-LIMITED) | — |

Run ended 2026-10-23 12:10:50 ET. Per endpoint (queries OK / queries ending rate-limited): OpenAlex 12/12 OK, 0 rate-limited; Semantic Scholar 3/12 OK, 9 rate-limited

Notes on Part 1:
- Times are box-local ET (UTC−4). Each attempt is listed; a request that received 429 was retried after 5, 10, 20 and 40 s (plus the 3.5 s pacing), so a query has at most 5 attempts (1 + 4 retries).
- **OpenAlex totals are uninformative as counts.** OpenAlex `search=` matches stemmed terms across title, abstract and full text, so totals (448–146,385) measure term frequency, not relevant literature. Only the top 25 by relevance were screened.
- **Semantic Scholar** returned 429 on the first attempt of every query. Three queries (#13, #16, #23) succeeded on a retry; the other nine stayed at 429 after 4 retries. No API key was used (none is held, and obtaining one is outside this read-only task).

## Part 2. Screening (top 25 per successful query; 15 query result sets, ≤375 records)

- **Method.** Titles of all returned records were read. For candidates, the OpenAlex abstract (`abstract_inverted_index`), the arXiv API abstract, or the publisher `<meta name="description">` was read. **No full text was read in this pass.** Known items were checked against v1 (`f2fd0ae6…`), v1.2 (`16646915…`) and v1.3 (`badf7258…`) by name search; v1.1 (`trackB_prior_art_verification_v1_1_prefreeze_CNA.md`) was also name-searched.
- **Known items re-found (already in v1/v1.2/v1.3, not re-flagged):** Yoshida et al. 2024 (PNAS Nexus; Neural Networks), Yoshida et al. IJCNN 2023, Yoshida, Sprekeler & Gutkin 2025 (now also in *Current Opinion in Behavioral Sciences*, doi 10.1016/j.cobeha.2025.101611, the journal version of the v1 arXiv perspective), Hulme et al. 2019, Grimbly et al. 2026 (now with a Springer LNCS record, doi 10.1007/978-3-032-39953-3_16), Maytié et al. 2024, Dossa et al. 2024, VanRullen & Kanai 2021, Goyal et al. 2021/2022, Rahbar 2026, Tait et al. 2026, Binder et al. 2024.
- **Off-topic results** (multi-agent RL, LLM reasoning RL, clinical "validation", preregistered psychology studies, philosophy of introspection, spark-ignition engines, etc.) were the majority of every set and are not listed.

### 2.1 Flagged works not in v1, v1.2 or v1.3

Relevance codes: **QN** = Q-NECESSITY (D1 interoceptive content, D2 learned RL agent, D3 viability outcome, D4 same-size module ablations plus matched arms); **SELF**; **C3** = claim (3) confound-realization gate. All assessed from abstract or metadata only.

| # | Work | Found by | Bears on | One-line relevance |
|---|---|---|---|---|
| N1 | Z. Dulberg, R. Dubey, I. M. Berwian, J. D. Cohen, "Modularity benefits reinforcement learning agents with competing homeostatic drives", arXiv 2204.06608 (2022). https://doi.org/10.48550/arXiv.2204.06608 | OA #1; S2 #13 | QN (D1, D2) | Deep-Q homeostatic agent (D1 and D2 territory) comparing monolithic vs per-variable modular architectures on sample efficiency and robustness. It is an architecture comparison, not a lesion/necessity test of a learned body self-model; no D3/D4 contrast per abstract. Cite as homeostatic-RL prior art. |
| N2 | H. Laurençon, Y. Bhargava, R. Zantye, C.-R. Segerie, J. Lussange, V. Baths, "Deep RL-Based Continuous-Time Continuous-Space Homeostatically Regulated Reinforcement Learning (CTCS-HRRL)", IEEE TNNLS, 2026. https://doi.org/10.1109/TNNLS.2026.3723854 (arXiv 2401.08999, 2024) | OA #1–3; S2 #13 | QN (D1, D2) | Deep HRRL agent in continuous time and space; an objective/environment-class precedent like Yoshida 2024. No self-model necessity test per abstract. |
| N3 | S.-W. Lee, Y. Oh, H. An, H. Yoon, K. J. Friston, S.-J. Hong, C.-W. Woo, "Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents", Nature Machine Intelligence, 2026 (published 26 Aug 2026; article type Perspective). https://doi.org/10.1038/s42256-026-01296-8 | OA #3 | QN (D1), framing | Perspective from the EVAAA group arguing for explicit internal-state factorization in RL agents. No experiment, so no D2–D4 test. Cite in §1 framing alongside EVAAA. |
| N4 | C. Palika, A. Khan, R. Maradana, S. Chakravarthy, "Faulty States, Faulty Learning: Distinct Routes to Dysregulated Feeding in Homeostatic Reinforcement Learning", SSRN preprint, 2026. https://doi.org/10.2139/ssrn.7560808 | OA #1–3 | QN (D1, possibly D4) | Title implies manipulating internal-state signals versus the learning mechanism in a homeostatic RL agent. **No abstract was available in OpenAlex; unread.** Needs a read to see whether it ablates a learned state model against matched controls. |
| N5 | S. Song, H. Lederman, J. Hu, K. Mahowald, "Privileged Self-Access Matters for Introspection in AI", arXiv 2508.14802 (2025). https://doi.org/10.48550/arXiv.2508.14802 | OA #9 | SELF | Defines introspection as access to internal states more reliable than any equal-or-lower-cost third-party process. That is the conceptual criterion behind SELF's outside-observer comparison. It is an LLM study (temperature parameter), not an RL agent or interoceptive variables. Cite as a definitional precedent. |
| N6 | T. Ashuach, S. Gretz, Y. Katz, Y. Belinkov, L. Ein-Dor, "Masked by Consensus: Disentangling Privileged Knowledge in LLM Correctness", ACL 2026 (long). https://doi.org/10.18653/v1/2026.acl-long.483 (arXiv record also indexed) | OA #9 | SELF | Compares self-hidden-state probes with peer-model probes for answer correctness. No advantage overall; the advantage appears only on disagreement subsets. That is a self-vs-external-observer design in LLMs, and its "consensus masks privilege" finding is a direct design warning for SELF. A SELF observer trained on the same behaviour may match the agent unless the test is evaluated where the two disagree. Not an RL agent. |
| N7 | A. Naphade, S. Bhargav, S. Lim, M. Shah, "Me, Myself, and π: Evaluating and Explaining LLM Introspection", arXiv 2603.20276 (2026). https://doi.org/10.48550/arXiv.2603.20276 | OA #9 | SELF | Introspect-Bench. Frontier LLMs predict their own behaviour better than peer models, with mechanistic evidence. This extends Binder 2024 in LLMs; not agents and not internal-body variables. |
| N8 | D. I. Atkinson, D. Plunkett, D. Bau, "Identifying Introspection From the Inside", arXiv 2610.07186 (2026). https://doi.org/10.48550/arXiv.2610.07186 | OA #9 | SELF (adjacent) | Mechanistic signatures of faithful self-report of learned latent preferences in fine-tuned LLMs, using weight ablations. Adjacent to SELF; no outside-observer comparison stated in the abstract excerpt read. |
| N9 | B. Liu, M. Chen, "Right Answer, Wrong Mechanism: Detecting Pernicious Divergence in Causal Interventions", arXiv 2609.39243 (2026-09-30). https://doi.org/10.48550/arXiv.2609.39243 | OA #12 | C3 (closest new hit) | Plants hidden pathways in GPT-2 so ground truth is known by construction. Shows that common off-manifold diagnostics score below chance, and that DAS routes 90–95% of successes through the planted pathways. That is known-answer instrument validation with planted mechanisms that can fake an intervention's success signature. Per the abstract it is LLM-only, not pre-registered, and does not use a fail-closed gate. It also bears on Q-CAUSE/BCAST (DAS and patching instruments), which is outside this note's three claims. |
| N10 | R. Gupta, I. Arcuschin, T. Kwa, A. Garriga-Alonso, "InterpBench: Semi-Synthetic Transformers for Evaluating Mechanistic Interpretability Techniques", NeurIPS 2024 (Datasets & Benchmarks per S2 venue). https://doi.org/10.48550/arXiv.2407.14494 | S2 #23 | C3 | Known-circuit transformers (SIIT, from Tracr) used to validate circuit-discovery methods: known-answer validation of interpretability instruments. Not pre-registered, no per-signature confounds, no fail-closed rule, not RL. |
| N11 | M. E. Canby, A. Davies, C. Rastogi, J. Hockenmaier, "How Reliable are Causal Probing Interventions?", IJCNLP-AACL 2025. https://doi.org/10.18653/v1/2025.ijcnlp-long.47 (arXiv 2408.15510) | OA #12 | C3 (adjacent); Q-CAUSE | Framework scoring causal-probing interventions on completeness and selectivity. An instrument-validation precedent, but with no planted confounds or gate. |
| N12 | H. Zhu, J. Zhang, "Clean Engineering, Unstable Measurement: A Preregistered Reliability Failure of Black-Box LLM Observers on Shared Endpoints", arXiv 2609.04198 (2026). https://doi.org/10.48550/arXiv.2609.04198 | OA #11 | C3 (adjacent) | Two pre-registered campaigns with thresholds fixed in advance. Neither got past validating its instrument, and the study stopped there. That is a pre-registered instrument-validation gate that failed closed in practice, but on LLM-judge reliability, not known-answer confounds. |
| N13 | L. Pokorny, "Empirical Validation of Consciousness Theories in Artificial Neural Networks", Zenodo/HAL preprint, 2025. https://doi.org/10.5281/zenodo.18006824 | OA #7 | C3 (weak); IGN/BCAST | Reports 12 "pre-registered" GWT/IIT/PP hypotheses across 60 trained networks (Global Broadcast Index d = 3.21). Not agents, and the abstract shows no known-answer gate. Bears mainly on IGN/BCAST prior art (Phua-adjacent), outside the three claims. Not peer reviewed; the abstract claims were not audited. |

**Screened and not flagged** (adjacent, but no bearing on QN, SELF or C3 beyond what is already cited): Tiwari 2025 EILS (arXiv 2512.22200, a framework); Andersson & Strandman 2019 and Mäkeläinen & Torén 2018 (homeostatic-agent theses); Neemeh et al. 2021, "Body Schema in Autonomous Agents" (JAIC, doi 10.1142/s2705078521500065; conceptual LIDA body schema, not learned RL); Ghasemabadi & Niu 2025, Gnosis (LLM self-verification vs external judges, not a matched observer); Wang & Reid 2026 ×2 (workspace in looped transformers and Mamba; IGN/BCAST adjacent); Kanai 2026 control-theoretic GWT; Romero 2026, "The Consciousness AI" (Zenodo software); Abdelgalil 2026 SSRN (no abstract); Bush et al. 2025, "Interpreting Emergent Planning in Model-Free RL" (ICLR 2025; probes plus interventions in a DRC agent, planning content, Q-CAUSE adjacent); Zhang 2026 RLVR preregistered contrast; Zhou et al. 2026 genomic-interpretability position paper.

## Part 3. Effect on current labels (no label is changed here)

| Claim | Current label | Affected by P3 hits? |
|---|---|---|
| Q-NECESSITY | EXTENSION (of W&G 2021 and Asan 2026) | **No.** N1, N2 and N3 add D1/D2-territory homeostatic-RL prior art, but none (per abstract) runs a lesion/necessity test of a learned body self-model against same-size module ablations (D4) on a viability outcome (D3). They cannot move the label further, because EXTENSION already holds. N4 (Palika 2026) is unread. **Would affect** only the named surviving differences (D3/D4 vs Asan) if a read showed a matched-module necessity test, so it is flagged for a read. It cannot change the label category. |
| SELF | Novel as far as found | **No.** N5–N8 are all LLM studies. N5 and N6 are direct design precedents for the self-vs-outside-observer comparison and should be cited next to Binder 2024. N6's consensus-masking result suggests SELF pre-specify a disagreement-subset analysis; that is a design note for Astra, not a label change. No hit tests an RL agent's own interoceptive variables against an observer trained on its behaviour. |
| Claim (3) | Narrowed partial overlap | **No.** N9–N12 add known-answer and planted-mechanism precedent (N9 is the closest: planted pathways that fake intervention success). That is the same direction as Bankuti and Akiyama. None builds per-signature confound systems for this battery, verifies that each confound is realized, and fails closed to UNRESOLVED, applied to learned RL agents. Cite N9 and N10 as precedent; the narrowed wording stands. |

## Part 4. Limits

- **Semantic Scholar: NOT SEARCHABLE (RATE-LIMITED)** for 9 of 12 queries (#14, #15, #17–#22, #24, with ET attempt times in Part 1). Only 3 Semantic Scholar queries returned results. The rate limit, not absence of literature, is the reason for its thin coverage.
- **OpenAlex: SEARCHABLE**, 12/12 queries returned HTTP 200 on the first attempt.
- Screening was by title plus abstract only. No full texts were read; N4 has no abstract at all.
- Top 25 per query only; relevance ranking in both indexes is keyword-driven and noisy (Part 1 notes). This is not a systematic review, and absence of a hit is not evidence of absence.
- The same 12 query strings were used on both endpoints; no query was tuned after seeing results.

---
Footer: input hashes (sha256, read-only inputs)
- `/workspace/review/trackB_prior_art_verification_v1_CNA.md`: f2fd0ae6f5df571f6ed6ad413ff604ffcb975e565c91c991acf8c801c6104ac9
- `/workspace/review/trackB_prior_art_verification_v1_2_open_items_CNA.md`: 166469154faeccdb9688a4473504f1d160711949b4eb74779bd84ba9a9b7451c
- `/workspace/review/trackB_prior_art_verification_v1_3_fullreads_CNA.md`: badf7258278fcecc11bea190f5397724ca0fdaf21348f915b1e2c34afe4cec8a
- Run script and raw responses (this pass):
  - `/workspace/tmp_p3/run.py`: 482c85c26fe42f849fe558914d4fdabc14a9d8a51d79401345a78366ad9cf5b7
  - `/workspace/tmp_p3/s2dump.py`: bfb793ddd4bbd75223e5dacde00573433d74e754028c569f0303e4b359a5959f
  - `/workspace/tmp_p3/raw/openalex_01.json`: d3aed14257069bdec5e7fa50b8e23370ea906e94e0ab68254984fc83766e34fa
  - `/workspace/tmp_p3/raw/openalex_02.json`: 5ad6760f028322ddead0ed7979e7c55706c544303a6071034968fd7ad0442553
  - `/workspace/tmp_p3/raw/openalex_03.json`: 152695a45f00fea09a230dddca1bef5c89314277c3aba54adbaab431c89526c0
  - `/workspace/tmp_p3/raw/openalex_04.json`: cea5a900429e34ae32765344104e219c9cf142bc9ba7866a5286ac40a256aa86
  - `/workspace/tmp_p3/raw/openalex_05.json`: fdbacb4b3d4fde08d91c30b0f000babb7ff2c4c84b3aff4fa96d9068270ed13b
  - `/workspace/tmp_p3/raw/openalex_06.json`: 3947022d75f1d1eddf6f8272f1e9060d4c809b127c864ec78ab5489186ef7a3a
  - `/workspace/tmp_p3/raw/openalex_07.json`: a376147fc1e54884c3957d69437b8fa6906cda0c0bb69e670ab371aa1e87cf9b
  - `/workspace/tmp_p3/raw/openalex_08.json`: 570c7b8c7ca04355ab50caa4cbc35518ce4c17fbc5115abbf6c6bbfea6a4d478
  - `/workspace/tmp_p3/raw/openalex_09.json`: 7649da01347688864e356dc41d11231d188e23949736f5571a2bf097aeb416ff
  - `/workspace/tmp_p3/raw/openalex_10.json`: 6c936084a49159eb4c3be4aa13ca60334294350a46f825d58d9a4c37b1e61cbd
  - `/workspace/tmp_p3/raw/openalex_11.json`: 26b0420d8e77f83bed263dea05e94ba94bc27c8d8bbb08664dddd18571a3a0c2
  - `/workspace/tmp_p3/raw/openalex_12.json`: 33f49cb1a10d15f1d32a72d8673b342f8ba9a4a7f7fd5d83ce6d8a5c9329fc2c
  - `/workspace/tmp_p3/raw/s2_01.json`: a805440958733ac3ebd0ccc0ac8b72b045f2141a682996eac72f10a09a287f9f
  - `/workspace/tmp_p3/raw/s2_04.json`: b9bf0af79759b833cb8729254b1733eceb65fb636efce99de4615e30066d451e
  - `/workspace/tmp_p3/raw/s2_11.json`: 5b441dad981a1949304d37d1bcf62fd1d33a5f6f1972f53442cb809ebf5c294d
- Written 2026-10-23, 11:53 AM–12:14 PM ET.
sha256 of all content above this line: 35b39c740d7b2b15232b2cdeadb42127d0a0cd758c75e1a6ea107ae6763d1676
