# Track B prior-art verification v1.6: Palika et al. 2026, legitimate full-text route search (CNA)

- **Status:** additive. It supersedes nothing. v1, v1.1 through v1.5 and every other file are unchanged.
- **Scope:** read-only HTTP GETs and web searches only. I ran no code, cloned nothing and executed nothing from the repository I found.
- **Constraints followed:** I made no attempt to get past SSRN's or bioRxiv's Cloudflare pages, and I used no mirror (no Sci-Hub or similar).
- **Run window:** 2026-10-23, 12:36 to 12:41 ET.
- **Target:** C. Palika, A. Khan, R. Maradana, V. S. Chakravarthy, "Faulty States, Faulty Learning: Distinct Routes to Dysregulated Feeding in Homeostatic Reinforcement Learning", SSRN preprint, doi:10.2139/ssrn.7560808.
- **Raw responses:** saved under `/workspace/tmp_p6/raw/`, with the route log at `/workspace/tmp_p6/routes.log`.

## 1. Result in one line

**No openly available full text of the paper was found.**

- There is no arXiv, OSF, PsyArXiv, bioRxiv, Europe PMC, Zenodo or journal-DOI version.
- Unpaywall and OpenAlex list SSRN (doi.org/10.2139/ssrn.7560808) as the only OA location, and that is the Cloudflare-blocked page.
- **One legitimate secondary source was found:** the first author's public GitHub repository, `github.com/CharithaPalika/FoodRL`. Its README says it is "the research codebase accompanying the paper" and that the paper is "Submitted to journal."
- The repository is **code and README text, not the paper's methods section.** Anything below that draws on it is labelled as code evidence and is not a full-text read.

## 2. Route log (all times ET, 2026-10-23)

### 2a. HTTP routes (curl, read-only GET)

| # | URL | HTTP | Time (ET) |
|---|---|---|---|
| 1 | `https://export.arxiv.org/api/query?search_query=ti:%22Faulty%20States%20Faulty%20Learning%22&max_results=10` | 200 | 2026-10-23 12:36:42 EDT |
| 2 | `https://export.arxiv.org/api/query?search_query=ti:dysregulated%20AND%20ti:feeding%20AND%20ti:homeostatic&max_results=10` | 200 | 2026-10-23 12:36:45 EDT |
| 3 | `https://export.arxiv.org/api/query?search_query=au:Palika&max_results=20` | 200 | 2026-10-23 12:36:48 EDT |
| 4 | `https://export.arxiv.org/api/query?search_query=au:Chakravarthy_S%20AND%20all:homeostatic&max_results=20` | 200 | 2026-10-23 12:36:51 EDT |
| 5 | `https://export.arxiv.org/api/query?search_query=abs:interoception%20AND%20abs:feeding%20AND%20abs:reinforcement&max_results=20` | 200 | 2026-10-23 12:36:55 EDT |
| 6 | `https://api.osf.io/v2/preprints/?filter%5Btitle%5D=Faulty%20States%2C%20Faulty%20Learning` | 200 | 2026-10-23 12:36:58 EDT |
| 7 | `https://api.osf.io/v2/preprints/?filter%5Btitle%5D=Dysregulated%20Feeding%20in%20Homeostatic%20Reinforcement%20Learning` | 200 | 2026-10-23 12:37:01 EDT |
| 8 | `https://api.crossref.org/works?query.title=Faulty+States+Faulty+Learning+Dysregulated+Feeding+Homeostatic+Reinforcement+Learning&rows=10&mailto=aidan@example.invalid` | 200 | 2026-10-23 12:37:05 EDT |
| 9 | `https://api.crossref.org/works?query.author=Palika+Chakravarthy&rows=20&mailto=aidan@example.invalid` | 200 | 2026-10-23 12:37:08 EDT |
| 10 | `https://api.openalex.org/works/doi:10.2139/ssrn.7560808?mailto=aidan@example.invalid` | 200 | 2026-10-23 12:37:12 EDT |
| 11 | `https://api.openalex.org/works?search=Faulty%20States%20Faulty%20Learning%20dysregulated%20feeding&mailto=aidan@example.invalid` | 200 | 2026-10-23 12:37:15 EDT |
| 12 | `https://api.unpaywall.org/v2/10.2139/ssrn.7560808?email=aidan@example.invalid` | 200 | 2026-10-23 12:37:19 EDT |
| 13 | `https://www.biorxiv.org/search/Faulty%20States%20Faulty%20Learning` | 403 | 2026-10-23 12:37:22 EDT |
| 14 | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22Faulty%20States%2C%20Faulty%20Learning%22&format=json` | 200 | 2026-10-23 12:37:26 EDT |
| 15 | `https://api.osf.io/v2/preprints/?filter%5Bprovider%5D=psyarxiv&filter%5Btitle%5D=Faulty%20States` | 200 | 2026-10-23 12:37:46 EDT |
| 16 | `https://api.osf.io/v2/users/?filter%5Bfull_name%5D=Palika` | 200 | 2026-10-23 12:37:52 EDT |
| 17 | `https://api.biorxiv.org/details/biorxiv/2026-09-01/2026-10-23/0` | 200 | 2026-10-23 12:37:56 EDT |
| 18 | `https://export.arxiv.org/api/query?search_query=abs:%22interoception-like%22&max_results=20` | 200 | 2026-10-23 12:37:59 EDT |
| 19 | `https://api.crossref.org/works/10.2139/ssrn.7560808?mailto=aidan@example.invalid` | 200 | 2026-10-23 12:38:02 EDT |
| 20 | `https://biotech.iitm.ac.in/faculty_website/CNS_LAB/Publications.html` | 200 | 2026-10-23 12:38:31 EDT |
| 21 | `https://api.github.com/search/repositories?q=faulty+states+faulty+learning` | 200 | 2026-10-23 12:38:35 EDT |
| 22 | `https://api.github.com/search/users?q=charitha+palika` | 200 | 2026-10-23 12:38:38 EDT |
| 23 | `https://zenodo.org/api/records?q=%22Faulty%20States%22%20Palika` | 200 | 2026-10-23 12:38:42 EDT |
| 24 | `https://zenodo.org/api/records?q=creators.name:Palika` | 200 | 2026-10-23 12:38:46 EDT |
| 25 | `https://api.github.com/users/CharithaPalika/repos?per_page=100` | 200 | 2026-10-23 12:38:58 EDT |
| 26 | `https://charithapalika.github.io/` | 200 | 2026-10-23 12:39:09 EDT |
| 27 | `https://api.github.com/repos/CharithaPalika/FoodRL` | 200 | 2026-10-23 12:39:12 EDT |
| 28 | `https://raw.githubusercontent.com/CharithaPalika/FoodRL/HEAD/README.md` | 200 | 2026-10-23 12:39:16 EDT |
| 29 | `https://api.github.com/repos/CharithaPalika/FoodRL/git/trees/HEAD?recursive=1` | 200 | 2026-10-23 12:39:21 EDT |
| 30 | `https://api.github.com/repos/CharithaPalika/CharithaPalika.github.io/git/trees/HEAD?recursive=1` | 200 | 2026-10-23 12:39:25 EDT |
| 31 | `https://raw.githubusercontent.com/CharithaPalika/FoodRL/HEAD/models/model.py` | 200 | 2026-10-23 12:39:37 EDT |
| 32 | `https://raw.githubusercontent.com/CharithaPalika/FoodRL/HEAD/analysis/latent_analysis.py` | 200 | 2026-10-23 12:39:40 EDT |
| 33 | `https://raw.githubusercontent.com/CharithaPalika/FoodRL/HEAD/results/plots_latent_ablation/model_metadata.json` | 200 | 2026-10-23 12:39:44 EDT |
| 34 | `https://api.github.com/repos/CharithaPalika/FoodRL/commits?per_page=5` | 200 | 2026-10-23 12:39:47 EDT |
| 35 | `https://raw.githubusercontent.com/CharithaPalika/FoodRL/HEAD/agents/ppo.py` | 200 | 2026-10-23 12:40:02 EDT |
| 36 | `https://raw.githubusercontent.com/CharithaPalika/FoodRL/HEAD/latent_ablations.ipynb` | 200 | 2026-10-23 12:40:06 EDT |
| 37 | `https://raw.githubusercontent.com/CharithaPalika/FoodRL/HEAD/results/plots_inference_normal/model_metadata.json` | 200 | 2026-10-23 12:40:09 EDT |

### 2b. Web searches (WebSearch tool), about 12:38 to 12:39 ET

- **W1:** `"Faulty States, Faulty Learning" dysregulated feeding homeostatic reinforcement learning`
  - Only the SSRN DOI came back for the paper itself.
- **W2:** `Palika Chakravarthy IIT Madras homeostatic reinforcement learning interoception feeding 2026`
  - Again only the SSRN DOI for the paper.
  - It also surfaced a related paper by the same group, Khan, Palika & Chakravarthy, "NutriRL", RLJ 2026 (rlj.cs.umass.edu/2026/papers/Paper78.pdf). That is **not** the target paper.
- **W3:** `Charitha Palika interoception-like internal state reinforcement learning feeding preprint pdf`
  - Only the SSRN DOI for the target paper.
- **W4:** `V. Srinivasa Chakravarthy Computational Neuroscience Lab IIT Madras publications 2026`
  - Found the lab publications page, fetched as route 20. It does not list the paper.

### 2c. Per-route outcome

- **arXiv API** (title phrase, title keywords, au:Palika, Chakravarthy + homeostatic, abstract "interoception-like"): 0 results on all six queries.
- **OSF and PsyArXiv** (api.osf.io title filters, with the provider filter set to psyarxiv): 0 preprints.
  - The OSF user search for "Palika" returned only an unrelated user, "Olympia Palikara".
- **bioRxiv:**
  - The site search returned **HTTP 403 with a Cloudflare "Just a moment..." page**. I did not try to get around it.
  - api.biorxiv.org has no title search. I fetched one date-window details page as a check that the API was reachable; that is not a full search.
  - bioRxiv is therefore **partly searched**. Europe PMC, which indexes bioRxiv and medRxiv preprints, returned 0 hits for the exact title.
- **Crossref** (title and author queries): only 10.2139/ssrn.7560808. No other DOI carries the same title. The Crossref `relation` field is empty, so no journal or other version is linked.
- **OpenAlex** (DOI and search): W7219685942. The only location is SSRN, and `best_oa_location` is doi.org/10.2139/ssrn.7560808.
  - `any_repository_has_fulltext: true` refers to that same SSRN location.
- **Unpaywall:** `is_oa: true`, with the only `oa_location` at doi.org/10.2139/ssrn.7560808 (SSRN, host RELX).
- **Zenodo:** no record of the paper. There are other Palika records: a BG–DBS model, and BG–cerebellum arbitration.
- **Author and lab pages:**
  - The personal page, charithapalika.github.io, links only a CV PDF. I did not fetch the CV.
  - The CNS Lab publications page does not list the paper.
- **GitHub:** the repository `CharithaPalika/FoodRL` exists and is public. Its last commit was 2026-08-25 06:22 UTC (02:22 ET), and its README names the paper. I fetched the README, `models/model.py`, `agents/ppo.py`, `analysis/latent_analysis.py`, `latent_ablations.ipynb`, two `model_metadata.json` files and the file tree.

## 3. What the code repository shows (code evidence, not paper methods)

### 3.1 Architecture

- **Feedforward (MLP), not recurrent.**
- `models/model.py` builds every trunk with `_mlp(...)` ("plain 2-layer MLP trunk", plus optional bottleneck layers).
- A search of `models/model.py` and `agents/ppo.py` for gru, lstm, rnn, recurr or hidden_state found **no matches**.
- The algorithm is PPO with a shared actor-critic, `hidden=256` and `separate_branches: true`.
- **Bottlenecks** (from `results/plots_inference_normal/model_metadata.json`): `"trunk_phy": {"dim": 16}, "critic_head": {"dim": 16}`.
- The partial observability comes from delayed nutrient dynamics. The README says the policy receives "a physiological vector with regulated nutrients plus sleep/wake timing" and food embeddings.
- The "shadow" appetite signals (hunger, fullness, CCK, ghrelin, GLP-1, PYY) are "intentionally hidden from the policy and do not affect reward." The decoding targets are those hidden signals.

### 3.2 The representation-level ("faulty states") intervention

`latent_ablations.ipynb`, cell 0, verbatim:

> "Each **condition** applies an affine transform to the physiology bottleneck `z_phy`: z' = amp · z + bias … `amp` → multiplicative gain (0 = full ablation, >1 = amplified). `bias` → additive offset (− = under-eat, + = over-eat)."

- The configured setting is `BOTTLENECK_NAME = 'trunk_phy'`, with seeds `[42, 64, 0]` and 20 inferences per seed pooled (n=60 per condition).
- The saved conditions are `bias=-1`, `baseline` and `bias=+1.5`, plus a one-axis sweep.

### 3.3 Neuron-level ablation (results only)

- The result files under `results/plots_neuron_ablation/` are named:
  - `top_{4,8,10,15,16}`
  - `bottom_{4,10,15,16}`
  - `random_{4,8,15,16}_n{1,2,3}`
- That pattern suggests that, in at least some analyses, **neurons were ablated in top-k/bottom-k order (ranked by correlation) and compared against random-k neuron sets of the same count.** From the file layout, those random sets are most likely drawn from the same 16-unit bottleneck.
- **The notebook that generated these files is not in the repository,** so which module the sets came from and how the arms were matched cannot be verified.

### 3.4 Other modules

- The repository contains a same-size (16-unit) `critic_head` bottleneck, and in separate-branch mode it supports a `trunk_food` bottleneck.
- I found **no code or result file that ablates another module of matched size** (critic_head, trunk_food, or a non-physiological layer) as a control arm for the `trunk_phy` intervention.
- I found no random-subspace arm and no external-estimate (A-EXT-style) bypass arm.

### 3.5 Outcome measures (relevant to D3)

- Per-condition results report:
  - `return_mean`
  - `food_items_mean`
  - `kcal_mean`
  - `avg_distance_mean` (distance to the nutrient target band)
  - `avg_signed_err_mean` (under- or over-eating)
- The notebooks add day-wise calories and per-step reward, distance and signed error.
- These are **regulation and feeding-phenotype measures over fixed-length episodes**: `max_steps: 432`, which is 3 days of 144 steps.
- I found no survival or termination-based viability score.

## 4. Answer to the D4 question

**Not answerable from the paper. Full text is still unread.**

- The code is consistent with D4 surviving against Palika, but it does not establish it.
- **On the code alone:**
  - The representation-level manipulation targets the 16-unit `trunk_phy` bottleneck, using gain and bias perturbation.
  - There is evidence of a *within-bottleneck* random-k-neurons-of-equal-count comparison. That is a partial matched-size control.
  - There is no evidence of a matched ablation of *other modules* of the same size, and no matched arms (random subspace, other module, external estimate) showing that the interoceptive representation specifically is necessary.
- **If the paper matches the code,** our D4 (matched-size ablation of other modules, with matched arms) would survive against Palika, with one caveat. Palika's random-k-neurons comparison is a partial overlap with the "random subspace" part of our arms. It does not overlap with the other-module or external-estimate parts.
- **If the paper's methods report analyses missing from the repository,** for example a critic_head or trunk_food ablation used as a control, D4 could fail against Palika. Only a full-text read can settle which is the case.

### 4.1 Other notes (implications only; no label changes)

- **D3:** Palika's outcomes are feeding-regulation and phenotype measures (distance to target, signed error, kcal, items, return) over fixed 432-step episodes. There is no viability or termination score.
  - This is consistent with the "partly shared" reading in v1.5 §2.2.
  - If confirmed by the paper, D3 in its fixed-horizon viability-score form would survive against Palika.
- **Architecture:** the code is **feedforward**, not recurrent.
  - If confirmed by the paper, "our agent is recurrent" would be a stated difference against Palika as well as against Asan.
  - This corrects the v1.5 §2.2 inference that Palika is "recurrent-relevant because the environment is partially observable". Partial observability in Palika is handled without recurrence. (I am stating this as a correction to that inference; v1.5 is not edited.)
- **D2 framing:** in the code, the interoceptive representation is a designed bottleneck layer (`trunk_phy`, dim 16) on a separate physiology branch. What emerges without supervision is its *content* (the hidden appetite signals), not the module itself.
  - This bears on how "emergent" is phrased when comparing, and changes nothing in D2 as frozen in A1.

## 5. Labels (unchanged)

- **Q-NECESSITY:** EXTENSION. Unchanged. Under the drop rule, nothing here can change the category.
- **D4 vs Palika:** "not evident from the abstract; unverified". Unchanged.
  - Proposed wording for the Lead or Delegate to consider, *not applied*: "not evident from the abstract; the authors' public code (FoodRL) shows no other-module matched-size ablation, only a within-bottleneck random-k-neurons comparison; the paper's full text is unverified."
- **SELF and claim (3):** not affected.

## 6. Still open

- **Full text of Palika 2026.** The only OA location is SSRN, which is Cloudflare-blocked.
- **The generating notebook for `results/plots_neuron_ablation/`,** which is absent from the repository.
- **Further legitimate options,** not taken here because both need a human to act:
  1. Aidan could open the SSRN page in an ordinary browser session.
  2. Aidan could email the corresponding author (schakra@ee.iitm.ac.in, per the NutriRL paper) or the first author (charithapalika@gmail.com) to ask for the preprint.
- **Recommendation:** ask Astra at #42 to treat D4 vs Palika as unverified, pending the full text.

## 7. Input hashes (sha256)

- `3fde80d859a640d9f55c21edc05439743ae5fb49714fb89e5e5d16d338eced75` /workspace/review/trackB_prior_art_verification_v1_5_P3_altroutes_CNA.md
- `d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d` /workspace/review/trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md
- `f88079d00d34a23eaac432c57c6ff783a6cd115e1941e085eb24f45dbe03483e` /workspace/tmp_p6/raw/arxiv_abs_interocep.xml
- `1423ff08118e3c411782c130d6f43077be9dd3a4e1b48ac7d0e11eaa96a6091d` /workspace/tmp_p6/raw/arxiv_abs_interocep2.xml
- `044d79ea68208db0071aee0bbf0de3fcbe09b6f3fd6b39c5a542bf799e7f0c2f` /workspace/tmp_p6/raw/arxiv_auth_chakravarthy.xml
- `feb4a2dd2a20791b098cb2d5724bd3ba49f4ca05e695decbef49abc9f37bcfb1` /workspace/tmp_p6/raw/arxiv_auth_palika.xml
- `160bdc8736be5c8473d64230683e97fbc99c6742716917d325bafafcd26fc2a3` /workspace/tmp_p6/raw/arxiv_title.xml
- `794230d4a88c08c761e107057c617a13296ccd5f8b2709107305433bc2a87b3b` /workspace/tmp_p6/raw/arxiv_title2.xml
- `7758cb930901e22c15f91b8946fe424feb8717431f0432a7f47e43bcd7ecd001` /workspace/tmp_p6/raw/biorxiv_search.html
- `6ad6e368c1a114f9708250ac20cc29100a66509657b2f5adafc8847d7bbe17ac` /workspace/tmp_p6/raw/cnslab_pubs.html
- `55c4e501298811e4eac64be645d895febedb254d8b6c0ca9077c421d26a37b96` /workspace/tmp_p6/raw/crossref_author.json
- `855a1b5e7c531e86bccf9f554ddfe9a87fa6ec75e85fa691ac176014997ab69f` /workspace/tmp_p6/raw/crossref_ssrn_relation.json
- `475eaebbe09243c56a80ed1866eb33b7bfc5fbdcd9c537a475fc2be1ee3ec7f8` /workspace/tmp_p6/raw/crossref_title.json
- `c52b87d92ec59c6383363816b115e83fcc4d76e92bda9d15d50686f3f8cdb39f` /workspace/tmp_p6/raw/europepmc.json
- `b02b91b0064081ef03d50669cf6b1bec03d2e98bc60130ba7382b9f14a06b0d3` /workspace/tmp_p6/raw/foodrl_commits.json
- `bc591aefa66db5766664e19585d1d8944ae7cfd045e0df5a206c994bf67fe9e4` /workspace/tmp_p6/raw/foodrl_infer_meta.json
- `ddc7f42bde9be1818b39c0c87b3a807418c3640e2d239ca22a8610d6ff568293` /workspace/tmp_p6/raw/foodrl_latent_ablations.ipynb
- `ec01249e779c9c0e244d8a59b6eb48f8dfcb292ba9f033d0fb979f07ca0fda78` /workspace/tmp_p6/raw/foodrl_latent_analysis.py
- `6fa3d9e73d7a374002dac19f6865d00596b7a2e829a2e33e030d5fffb8b07b1d` /workspace/tmp_p6/raw/foodrl_model.py
- `cc8ab494e452fbce6b5411a94136fc7a68d493d721c8b67165723457e846a705` /workspace/tmp_p6/raw/foodrl_neuron_meta.json
- `7b51bb03d4ca349e3b59d1388a879ddb05f5f75509d265defedaa19738965801` /workspace/tmp_p6/raw/foodrl_ppo.py
- `f810847dabb9269b2db7493fccf6b1ba8f95ef452e011364672f68ca25be17c9` /workspace/tmp_p6/raw/foodrl_readme.md
- `05b3d90dccb3546262e6d9d56573ca1615a671db95e1aa2ea83d1fb990d87390` /workspace/tmp_p6/raw/foodrl_repo.json
- `05039cc60ce20c706068b5e7d8cb1462c0250ef29e5c2aad30812a837ae54be5` /workspace/tmp_p6/raw/foodrl_tree.json
- `aa0e7bf7082a48fa34829dcdfff6c0aa36d1dc3f9c4f882ea161a20a2c1f6a79` /workspace/tmp_p6/raw/ghio_tree.json
- `b9e25fcc032a2e4b0291f3686779b7b3269ddb25328f4314a60b8f2580c64433` /workspace/tmp_p6/raw/github_palika_repos.json
- `2ea0dcf99c56d872d795d4f84920e12dcc3cc06cd4ab59cd5ab57b4efbd1c85e` /workspace/tmp_p6/raw/github_search.json
- `fab48c51914520473d57c97749999898f548e9742536fec1c0a2f4fb96b1b136` /workspace/tmp_p6/raw/github_users.json
- `7af8afcdfb21109fd419210143f72e0793dde48e166d2badc21311d1b7d64c19` /workspace/tmp_p6/raw/medrxiv_biorxiv_api.json
- `16b81cc48edbc3e739909463e0c76f651527a01d031b34de4b5a35040ec95b8b` /workspace/tmp_p6/raw/openalex_doi.json
- `60c62167423398bfe0b110d0c7d19b0957a2069ead8dd687127642910ab419cc` /workspace/tmp_p6/raw/openalex_search.json
- `f03e09d29551b7007d724400b83e052b35221b1b84eb24b8a7a9c32b170c8c97` /workspace/tmp_p6/raw/osf_contrib_palika.json
- `337a5845bf62ccbe2bee6d47834c9d6317bc033ab935af60bc66d75c688ef71a` /workspace/tmp_p6/raw/osf_title.json
- `337a5845bf62ccbe2bee6d47834c9d6317bc033ab935af60bc66d75c688ef71a` /workspace/tmp_p6/raw/osf_title2.json
- `92eabfd89a17f3dbc87cece0bc7857006d39cd691addac7334f529e7631d0793` /workspace/tmp_p6/raw/personal_page.html
- `337a5845bf62ccbe2bee6d47834c9d6317bc033ab935af60bc66d75c688ef71a` /workspace/tmp_p6/raw/psyarxiv_osf.json
- `ec864229197573c43bc14f00629faca63542668859be3ad20f8e1aae894d4c68` /workspace/tmp_p6/raw/unpaywall.json
- `a915305a0bdf32fe2b3afd7c9753a4969078f9c996a4ff7941cdb8c3078e907b` /workspace/tmp_p6/raw/zenodo.json
- `b9aa4ea092dd5fe9c9ceab3bafda46b0056645a1a026523e56aec351a48b850b` /workspace/tmp_p6/raw/zenodo2.json
- `cf436fbdbfa4ffe96afc98a611633e53d46cdc8eb93ac106425843a2bc76227c` /workspace/tmp_p6/routes.log
be61452b4d0cacd208dfae964e74b02ada69d63d1736f30661ab7f9147a0097b
