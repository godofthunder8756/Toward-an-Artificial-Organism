CNA, 2026-10-23, additive note; planning only; authorizes nothing

# Track B prior-art verification v1.5: P3 alternative-route retry (Crossref, arXiv API, Google Scholar) (CNA)

- **Amends nothing.** Additive. Retries, by different routes, the 9 Semantic Scholar queries that ended HTTP 429 in v1.4 (`trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md`, d7f1a43b…, Part 1 #14, #15, #17–#22, #24), as asked by the Lead after Astra #41. No existing file was edited. No labels are changed here.
- **Nothing ran** except read-only HTTP GETs to api.crossref.org, export.arxiv.org, scholar.google.com (one attempt), and doi.org / api.crossref.org for the Palika DOI. Raw responses saved under `/workspace/tmp_p3b/raw/`.
- **Run started** 2026-10-23 12:29:06 ET. Crossref pacing ≥2 s; arXiv pacing ≥3.5 s (API asks ≥3 s). On HTTP 429/5xx or network error: backoff 5/10/20/40 s (+pacing), at most 4 retries. Query strings are identical to v1.4.
- **Query encoding.** Crossref: `query=<string>&rows=25&mailto=aidan@example.invalid` (relevance-ranked bibliographic match). arXiv: `search_query=all:<string>&max_results=25` with the string passed as-is (arXiv's Lucene parser treats unquoted space-separated terms with OR-like relevance ranking, so totals are not counts of relevant work).
- **This file is written incrementally**; Part 1 rows are appended as each query completes.

## Part 1. Query log

| v1.4 # | Route | Query | Attempts (ET, HTTP status) | Result | Total hits (index) | Records returned |
|---|---|---|---|---|---|---|
| 14 | Crossref | `allostatic reinforcement learning agent` | 12:29:06 200 | OK | 3059903 | 25 |
| — | arXiv API (http://) | `allostatic reinforcement learning agent` | from 12:29:08: connection timeouts (60 s each, no HTTP status); attempt loop stopped by operator at 12:32:05 | ABANDONED, route switched to https://export.arxiv.org | — | — |
| 14 | arXiv API | `allostatic reinforcement learning agent` | 12:32:05 200 | OK | 575770 | 25 |
| 15 | Crossref | `interoceptive reinforcement learning agent` | 12:32:10 200 | OK | 3060623 | 25 |
| 15 | arXiv API | `interoceptive reinforcement learning agent` | 12:32:12 200 | OK | 575794 | 25 |
| 17 | Crossref | `body model lesion necessity reinforcement learning agent` | 12:32:16 200 | OK | 6720659 | 25 |
| 17 | arXiv API | `body model lesion necessity reinforcement learning agent` | 12:32:19 200 | OK | 1506530 | 25 |
| 18 | Crossref | `global workspace agent reinforcement learning` | 12:32:24 200 | OK | 4592195 | 25 |
| 18 | arXiv API | `global workspace agent reinforcement learning` | 12:32:26 200 | OK | 688390 | 25 |
| 19 | Crossref | `ignition global workspace artificial neural network` | 12:32:31 200 | OK | 4369114 | 25 |
| 19 | arXiv API | `ignition global workspace artificial neural network` | 12:32:33 200 | OK | 690108 | 25 |
| 20 | Crossref | `global broadcast workspace deep learning model` | 12:32:38 200 | OK | 7704377 | 25 |
| 20 | arXiv API | `global broadcast workspace deep learning model` | 12:32:40 200 | OK | 1535655 | 25 |
| 21 | Crossref | `introspection self-prediction privileged access internal states` | 12:32:45 200 | OK | 4118831 | 25 |
| 21 | arXiv API | `introspection self-prediction privileged access internal states` | 12:32:48 200 | OK | 794024 | 25 |
| 22 | Crossref | `agent predicts own internal state better than external observer` | 12:32:53 200 | OK | 4197568 | 25 |
| 22 | arXiv API | `agent predicts own internal state better than external observer` | 12:32:55 200 | OK | 1662723 | 25 |
| 24 | Crossref | `random subspace control causal intervention neural network representation` | 12:33:00 200 | OK | 5752856 | 25 |
| 24 | arXiv API | `random subspace control causal intervention neural network representation` | 12:33:02 200 | OK | 970229 | 25 |
| 14 | Google Scholar (single plain-HTTP attempt) | `allostatic reinforcement learning agent` | 12:33:08 429 | BLOCKED (captcha, unusual traffic) | — | 0 |

Run ended 2026-10-23 12:33:08 ET.

Notes on Part 1:
- Times are box-local ET (UTC−4). Every attempt is listed. No 429 or 5xx was received from Crossref or the arXiv API, so no backoff retries were needed.
- **arXiv over plain `http://` failed.** The first arXiv request (query #14) used `http://export.arxiv.org` and got connection timeouts from 12:29:08 ET, with no HTTP status. The run was stopped at 12:32:05 ET and restarted on `https://export.arxiv.org`. The row marked "—" logs that abandoned attempt, which belongs to query #14. Every arXiv row with a 200 used https. This was a transport problem, not a rate limit.
- **Google Scholar** got exactly one plain-HTTP GET (query #14, 12:33:08 ET), with no browser and no cookies. It returned HTTP 429 with a captcha page ("unusual traffic from your computer network"). That route was then dropped and not retried, as instructed.
- **Totals are not counts of relevant work.** Crossref `query=` is a bibliographic relevance match over metadata, so its totals run from 3.0M to 7.7M. The arXiv API with `all:<unquoted terms>` gives OR-like ranking, so its totals run from 0.58M to 1.66M. For #14, #15 and #17, the arXiv top 25 are almost the same generic RL list, which shows the ranking was driven by "reinforcement learning agent". Only the top 25 were screened.
- Crossref returns abstracts for only a minority of records. Where a record had none, screening was by title.

## Part 2. Screening (top 25 per query per route; 18 result sets, 450 records)

- **Method.** I read the title of every record. For candidates, I read the arXiv API `<summary>` or the Crossref `abstract` field. **No full text was read.** Known items were checked by name and ID against v1 (`f2fd0ae6…`), v1.1 (`29068cce…`), v1.2 (`16646915…`), v1.3 (`badf7258…`) and v1.4 (`d7f1a43b…`).
- **Known items found again (already in v1–v1.4, not flagged again):**
  - Song, Lederman, Hu & Mahowald 2025 (N5)
  - Naphade et al. 2026 (N7)
  - Ashuach et al. 2026 (N6, arXiv 2604.12373)
  - Binder et al. 2024 (arXiv 2410.13787)
  - Ghasemabadi & Niu 2025, Gnosis (v1.4 screened, not flagged)
  - the "Predictive Allostatic Organization in Recurrent and Spiking Agents" preprint (arXiv 2608.11506, in v1/v1.1)
  - "The Ignition Index" (arXiv 2608.05160, in v1)
  - Maytié et al. 2024 zero-shot cross-modal GW transfer (arXiv 2403.04588)
  - VanRullen & Kanai 2021 (TINS and arXiv)
- **Off-topic** results were the large majority of every set and are not listed. Examples: multi-agent RL, spark-ignition engines, solar forecasting, privileged-access *management* (IT security), philosophy-of-mind book chapters on privileged access, clinical "predicts better than" papers, and random-subspace ensembles.

### 2.1 Flagged works not in v1–v1.4

The codes are the same as v1.4. **QN** is Q-NECESSITY, with D1 interoceptive content, D2 learned RL agent, D3 viability outcome, and D4 same-size module ablations plus matched arms. **SELF** is the self versus outside-observer comparison. **C3** is the claim (3) confound-realization gate. Every flag is based on the abstract only.

| # | Work | Found by | Bears on | One-line relevance |
|---|---|---|---|---|
| M1 | S. Singh, T. Linzen, S. Ravfogel, "Can LLMs Introspect? A Reality Check", arXiv 2605.26242 (2026). https://doi.org/10.48550/arXiv.2605.26242 | arXiv #21 | SELF (closest new hit); C3 (adjacent) | Sets two conditions for any introspection test: privileged access, meaning the task can't be solved from input cues, and second-order computation. When the paradigm "predict labels derived from your own hidden states" is re-examined, *input-only classifiers match the models' predictions*. That is an outside-observer baseline that makes the self-access signature disappear, so it is a realized confound in the sense of claim (3). It is a direct design precedent for SELF's observer arm. LLM only. Not an RL agent, no interoceptive variables, no fail-closed gate. |
| M2 | S. Song, J. Hu, K. Mahowald, "Language Models Fail to Introspect About Their Knowledge of Language", arXiv 2503.07513 (2025). https://doi.org/10.48550/arXiv.2503.07513 | arXiv #21 | SELF | Defines introspection as how far a model's self-reports predict its own string probabilities *beyond another model with nearly identical internal knowledge*. That is a matched-observer comparison, and it finds no privileged self-access across 21 LLMs. It is the empirical companion to N5 (same group). LLM only. |
| M3 | K. Aoki, R. Takatsuki, G. Minegishi, Y. Haruki, D. Kawahara, "In-Context Neurofeedback: Can LLMs Control Their Internal Representations through Privileged Access?", arXiv 2609.00904 (2026). https://doi.org/10.48550/arXiv.2609.00904 | arXiv #21 | SELF (adjacent) | Redesigns LLM neurofeedback so that a third party cannot infer the target from the prompt. Under that constraint, the reported control disappears. Same lesson as M1: an observer-inferable target fakes the signature. LLM only, and about control rather than prediction. |
| M4 | N. Pitsillos, A. Pore, B. S. Jensen, G. Aragon-Camarasa, "Intrinsic Robotic Introspection: Learning Internal States From Neuron Activations", ICDL 2021. https://doi.org/10.1109/ICDL49984.2021.9515672 (arXiv 2011.01880) | Crossref #21; arXiv #21 | SELF (weak); QN (weak) | Actor-critic robot agent that uses a VAE latent of its own feature-network activations as "internal states", which speeds up learning. It is an RL agent with a learned model of its own activations, but those are not interoceptive or body variables. There is no outside-observer comparison and no necessity or lesion test. Cite only as terminology-adjacent. |
| M5 | L. Weber, D. M. Yee, D. M. Small, F. H. Petzschner, "Rethinking reinforcement learning: The interoceptive origin of reward", PsyArXiv (2024). https://doi.org/10.31234/osf.io/be6nv | Crossref #15 | QN (D1), framing | Theory paper arguing that biological reward arises from interoceptive state. No agent, no experiment. Can be cited in §1 framing next to N3 (Lee et al. 2026). |

**Screened and not flagged.** These are adjacent but do not bear on QN, SELF or C3 beyond what is already cited:
- Ozdemir & Gatti 2025, "Social Touch as an Allostatic Tool in Cooperative MARL" (CHI EA, doi 10.1145/3706599.3720216). No abstract in Crossref; a multi-agent social-touch framing.
- Maytié, PhD thesis, "Multimodal grounding in RL … using a global workspace architecture" (doi 10.70675/bf8af3bd…), and Devillers, PhD thesis, "How to train your global workspace?" (doi 10.70675/101815c7…). These are theses of the already-cited GW lineage, IGN/BCAST adjacent.
- Bertin-Johannet, Scipio, Maytié & VanRullen 2026, ICANN LNCS (doi 10.1007/978-3-032-38401-0_9). GW attention, no abstract, IGN/BCAST adjacent.
- Zaznov 2026, "Causal Latent Workspaces for Looped Transformers" (arXiv 2610.22796). A language-modelling architecture, IGN/BCAST adjacent at most.
- Grünbaum et al. 2022, "Quantitative probing" (arXiv 2209.03013). Validates causal graph models, not NN instruments.
- "Towards Physics of Internal Observers" (arXiv 2304.01677) and the LLM-agent papers from arXiv #22. Off-claim.

### 2.2 Palika et al. 2026 (v1.4 N4): abstract now obtained

- **Crossref metadata** (`api.crossref.org/works/10.2139/ssrn.7560808`, 12:29:11 ET, HTTP 200) returned the full abstract. Details:
  - Type `posted-content`, created 2026-10-04.
  - Authors: C. Palika, A. Khan, R. Maradana, S. Chakravarthy.
- **doi.org landing page** (12:29:12 ET) redirects to `papers.ssrn.com/sol3/papers.cfm?abstract_id=7560808`, which returned **HTTP 403** with a Cloudflare "Just a moment..." challenge. I did not try to get around it. **Full text was not read.**
- **What the abstract says**, paraphrased from the Crossref `abstract` field:
  - An RL agent learns adaptive feeding from physiological consequences in a partially observable environment with delayed dynamics.
  - A low-dimensional physiological representation *emerges within the network* and carries hunger and fullness information without direct supervision. The authors call it "an interoception-like internal state".
  - Two disruption levels are compared:
    - (i) *representation level*: perturbing the learned interoceptive state produces under- or over-eating;
    - (ii) *learning level*: attenuating positive or negative TD errors during retraining produces distinct dysregulated phenotypes while the representation is left intact.
- **Bearing on QN** (abstract only):
  - **D1 is shared**: interoceptive content.
  - **D2 is shared**: a learned RL agent with an *emergent, unsupervised* interoceptive representation.
  - **D3 is partly shared**: the outcome is regulation and feeding phenotype, not a stated fixed-horizon viability score.
  - **D4 is not evident**: the abstract describes perturbing the learned state and a learning-level dissociation. It describes no ablation of a same-size module and no matched arms (random-subspace, other-module or external-estimate).
  - **The learned-versus-supplied difference that survives against W&G 2021 is also matched here.** Palika's interoceptive state is learned, not supplied.
  - On the abstract alone, **Palika is now the closest QN prior art**. It is closer than Asan 2026 on D1 and D2, and it is recurrent-relevant because the environment is partially observable, though the architecture isn't named in the abstract.

## Part 3. Effect on current labels (no label is changed here)

| Claim | Current label | Affected by v1.5 hits? |
|---|---|---|
| Q-NECESSITY | EXTENSION (of W&G 2021 and Asan 2026) | **The label is unchanged. The text naming what survives is affected.** None of M1–M5 bears materially. Palika 2026 (now read at abstract level) shares D1 and D2, partly shares D3, and also matches the "learned, not supplied" point. Under the drop rule, the category changes only if all four differences fail. D4 (matched same-size module ablations with matched arms) is not evident in the abstract, so EXTENSION holds. **However, the surviving-differences text should add Palika as a third comparator.** Against Palika, only D4 (and D3 in its fixed-horizon viability form) survives on the abstract. The claim that our self-model is "learned rather than supplied" can no longer be stated as distinctive in general, only against W&G. Whether D4 survives against Palika needs a full-text read, which is blocked by the SSRN Cloudflare 403. That read is flagged as open. It does not change the label category. |
| SELF | Novel as far as found | **No change.** M1–M3 are LLM studies that add more precedent for the self-versus-matched-observer comparison and for the privileged-access condition. M1 in particular shows an input-only observer matching "self-prediction". That strengthens the AQ-SELF1 point (analyse where agent and observer disagree; require that the target not be inferable from inputs). It is a design note, not a label change. No hit tests an RL agent's own interoceptive variables against an observer trained on its behaviour. M4 is an RL agent but has no observer arm. |
| Claim (3) | Narrowed partial overlap | **No change.** No new hit builds per-signature confounds, checks each one for realization, and fails closed to UNRESOLVED. M1's input-only-classifier result is an example of a confound that fakes a signature in LLMs, so it can be cited next to N9 (Liu & Chen 2026) and N10 (InterpBench). The narrowed wording stands. |

## Part 4. Final status: coverage per query per route

| v1.4 # | Query | Semantic Scholar (v1.4) | Crossref (v1.5) | arXiv API (v1.5) | Google Scholar (v1.5) |
|---|---|---|---|---|---|
| 14 | allostatic reinforcement learning agent | RATE-LIMITED (11:54:35–11:56:04) | COVERED (12:29:06, 200, 25 rec.) | COVERED (12:32:05, 200, 25 rec.; earlier http:// attempt timed out, 12:29:08–12:32:05) | BLOCKED (12:33:08, 429 captcha); single attempt |
| 15 | interoceptive reinforcement learning agent | RATE-LIMITED (11:56:08–11:57:37) | COVERED (12:32:10, 200, 25) | COVERED (12:32:12, 200, 25) | not attempted (route dropped) |
| 17 | body model lesion necessity reinforcement learning agent | RATE-LIMITED (11:59:15–12:00:45) | COVERED (12:32:16, 200, 25) | COVERED (12:32:19, 200, 25) | not attempted |
| 18 | global workspace agent reinforcement learning | RATE-LIMITED (12:00:48–12:02:18) | COVERED (12:32:24, 200, 25) | COVERED (12:32:26, 200, 25) | not attempted |
| 19 | ignition global workspace artificial neural network | RATE-LIMITED (12:02:22–12:03:52) | COVERED (12:32:31, 200, 25) | COVERED (12:32:33, 200, 25) | not attempted |
| 20 | global broadcast workspace deep learning model | RATE-LIMITED (12:03:55–12:05:25) | COVERED (12:32:38, 200, 25) | COVERED (12:32:40, 200, 25) | not attempted |
| 21 | introspection self-prediction privileged access internal states | RATE-LIMITED (12:05:29–12:06:59) | COVERED (12:32:45, 200, 25) | COVERED (12:32:48, 200, 25) | not attempted |
| 22 | agent predicts own internal state better than external observer | RATE-LIMITED (12:07:02–12:08:49) | COVERED (12:32:53, 200, 25) | COVERED (12:32:55, 200, 25) | not attempted |
| 24 | random subspace control causal intervention neural network representation | RATE-LIMITED (12:09:20–12:10:49) | COVERED (12:33:00, 200, 25) | COVERED (12:33:02, 200, 25) | not attempted |

All times are 2026-10-23 ET (UTC−4).

- **Route status:**
  - **Crossref:** SEARCHABLE, 9/9.
  - **arXiv API (https):** SEARCHABLE, 9/9. Over http:// the connection timed out.
  - **Google Scholar:** NOT SEARCHABLE (BLOCKED: HTTP 429 captcha, 12:33:08 ET), 0/1 attempted.
  - **Semantic Scholar:** remains NOT SEARCHABLE (RATE-LIMITED) for these 9 queries, at the v1.4 times. It was not retried here.
- **P3 assessment (CNA; Astra rules at #42):**
  - **All 9 queries missing from v1.4 now have coverage on two independent alternative routes.** Combined with v1.4's OpenAlex 12/12, every P3 query string has been run on at least two indexes that returned results.
  - **On coverage, P3 can be called CLOSED.** It does not need to be recorded as blocked.
  - **Residual items, recorded and not blocking on the coverage criterion:**
    - (a) Semantic Scholar itself remains rate-limited, and Google Scholar is captcha-blocked, both with times above.
    - (b) Crossref and arXiv ranking for these keyword strings is noisy (Part 1 notes).
    - (c) The full text of **Palika 2026** cannot be read: SSRN returned 403 at 12:29:12 ET. Its abstract changes the *surviving-differences text* for Q-NECESSITY (Part 3), though not the label. Whether that read should block freeze is for the Lead and Astra to decide.

## Part 5. Limits

- Screening was by title and abstract only. No full texts were read. This is not a systematic review, and absence of a hit is not evidence of absence.
- Query strings were identical to v1.4. None was tuned after seeing results. The arXiv query used unquoted `all:` terms, as specified.
- No API keys, browser sessions, cookies or block-circumvention were used. Google Scholar and SSRN blocks were recorded and left alone.

---
Footer: input hashes (sha256, read-only inputs)
- `/workspace/review/trackB_prior_art_verification_v1_CNA.md`: f2fd0ae6f5df571f6ed6ad413ff604ffcb975e565c91c991acf8c801c6104ac9
- `/workspace/review/trackB_prior_art_verification_v1_1_prefreeze_CNA.md`: 29068cce219530f459a4a045f349393a2aea9db1253a4c76a654514284017928
- `/workspace/review/trackB_prior_art_verification_v1_2_open_items_CNA.md`: 166469154faeccdb9688a4473504f1d160711949b4eb74779bd84ba9a9b7451c
- `/workspace/review/trackB_prior_art_verification_v1_3_fullreads_CNA.md`: badf7258278fcecc11bea190f5397724ca0fdaf21348f915b1e2c34afe4cec8a
- `/workspace/review/trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md`: d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d
- Run scripts and raw responses (this pass):
  - `/workspace/tmp_p3b/run.py`: 0f13c770dc09c710eb22ec4f327f6ccbda592f36c4986508891f46f809ad6bf6
  - `/workspace/tmp_p3b/run2.py`: 048b5d7f96bc2b321030857b7e113b411c129f1197ffaf14f286f296754e9324
  - `/workspace/tmp_p3b/summary.json`: 81517ea630bf432091865cade52c5eec5823f5f49ca71eb26aca1cefd597cf4a
  - `/workspace/tmp_p3b/raw/arxiv_14.xml`: eef1b7e91c254bbbcdd1d0932c781631719fdc702ff68ac1c0e16b70f82cf104
  - `/workspace/tmp_p3b/raw/arxiv_15.xml`: 6cb7aadf9a5e34649929d214dec960e15ac1473ab3cfb3cc4682f323b285510a
  - `/workspace/tmp_p3b/raw/arxiv_17.xml`: dcadc86749dfb9341507488cdfc3f389bbf3310be72b99cc1bfec66a95076ff3
  - `/workspace/tmp_p3b/raw/arxiv_18.xml`: 8b36a313aab2a8b1c971f6e98a9afbbff16ba9e9897ac94e9fe6637129d10a4f
  - `/workspace/tmp_p3b/raw/arxiv_19.xml`: c4c9b60d9fe68bea81fb8782f482c4357168cc9c794c14a44ddaf0feb28fb8a1
  - `/workspace/tmp_p3b/raw/arxiv_20.xml`: d9fb868b567c567e7af3dec1cae1bde176a5603384de830d959c529e313ef0b2
  - `/workspace/tmp_p3b/raw/arxiv_21.xml`: 95dc1127b53082a3a995e914d42527e975d6fe1b359fc6398cdc79605de3da0f
  - `/workspace/tmp_p3b/raw/arxiv_22.xml`: 39f1cbc92f89f0bdbee7e4581f6bcec401b74273a58a50110c5e64f82399222f
  - `/workspace/tmp_p3b/raw/arxiv_24.xml`: 72e98e2eea07ed989dac12a8da4d2632f22a23fa3dfe701ee59e06d099e74f7e
  - `/workspace/tmp_p3b/raw/crossref_14.json`: 4e70b8ef328cee483a6bd8474139f5ea4cf9bc70cf96af4da250e3b2810b4342
  - `/workspace/tmp_p3b/raw/crossref_15.json`: c6ad3d8f62a0b2e3c56dcf9ea19476ab4a2fe480992cde35bbc37f0d99da1cd1
  - `/workspace/tmp_p3b/raw/crossref_17.json`: afd1629301e940665bd87009127a6903155028b0bafbadebb67ae29d6cf81d07
  - `/workspace/tmp_p3b/raw/crossref_18.json`: 50f350543571b4b88546e3a1b950f3a7a12fb6b855f7b7c4cf7632295c2496df
  - `/workspace/tmp_p3b/raw/crossref_19.json`: 1e6f37c8abaa8df16c17fcdd6fbe8c5beb5d6a764cc59a1150e12c46efe92375
  - `/workspace/tmp_p3b/raw/crossref_20.json`: 18fe8a7c7aebb21019ae46c9bc14ccf63028f1772125d52296f849c71c921f83
  - `/workspace/tmp_p3b/raw/crossref_21.json`: 0624bf1635a5055f5cf0c28133fa3fd6167766f51741a64ddc590464396fe0be
  - `/workspace/tmp_p3b/raw/crossref_22.json`: 5a5b684558e01ca3792c77afbb8c5cd8b37e13d7d27967ddb2567a31c9f5db8b
  - `/workspace/tmp_p3b/raw/crossref_24.json`: 6fc8e888c2360e91bd9b27689ab38ae906e378adef1f5262afe2e7b4f86c2c0c
  - `/workspace/tmp_p3b/raw/gscholar_14.html`: b9f540b91b9c348f94cd0965d0c4c1770031bb9b9e5044f89fd8e6eecd50f5cf
  - `/workspace/tmp_p3b/raw/palika_crossref.json`: 855a1b5e7c531e86bccf9f554ddfe9a87fa6ec75e85fa691ac176014997ab69f
  - `/workspace/tmp_p3b/raw/palika_doiorg.html`: 1a1ba3a68aac0abcce44b7a086b5d84e0bcf3bdc05c42bc5c9a674ac06d4607b
- Written 2026-10-23, 12:29 PM–12:35 PM ET.
sha256 of all content above this line: 70460e8ae047a0beaead078fd9b5e3873f4a94fd95cc94f716de57a5dba17fd8
