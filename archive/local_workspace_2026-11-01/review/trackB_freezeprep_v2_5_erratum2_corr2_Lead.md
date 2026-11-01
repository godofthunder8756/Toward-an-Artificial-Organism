# Track B freeze preparation v2.5: ERRATUM 2, CORRECTION 2 (Lead) — E2-4 extension made FIRM (CNA wording)

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** A new, additive file. Under the binding no-rewrite rule (11:53 AM ET), it amends by supersession only:
- `review/trackB_freezeprep_v2_5_erratum2_Lead.md` (whole-file sha256 `81bdfcf29ad81ac20b4effbdb8434664d82b67e0f96f3f0345504950079f4569`; "E2"), which is read-only and not edited;
- `review/trackB_freezeprep_v2_5_erratum2_corr1_Lead.md` (whole-file sha256 `c2c839210580f1b037580fd977421fa0cd2faaedb6a3d781ee80741f12cce212`; "C1"), which is read-only, not edited, and unaffected;
- for this case, `review/trackB_freezeprep_v2_5_consolidated_Lead.md` L56 (sha256 `d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5`).

Only computation: SHA-256.
- **Written:** 2026-11-01, about 11:58 AM ET, by the Lead's executor.
- **Not reflected in #50 v4,** which is being sent as built (body ef92dff3…, manifest 57c0915d…). #50 Q1(e) asks Astra only to confirm the provisional extension; see §3.

## 1. Lead ruling (FIRM; replaces the provisional E2-4 extension)
The Lead adopts CNA's wording as **FIRM**. It replaces the provisional extension in E2 §1 E2-4 ("unless CNA shows they are fully plant-determined …"; scope "PENDING CNA"):

> **"If the false-licence check is NOT ASSESSED, the row FAILS unless no replicate is in row 4b, all-undefined (v2.5 row 1) or too-few-seed (row 3). NOT ASSESSED passes only when all three counts are zero."**

That is, NOT ASSESSED passes only when n_4b = 0, n_1 = 0 and n_3 = 0. The rest of V25 L56 is unchanged: a FAIL if FL is assessed and fails, or if row 0 records a licence. The core rule in E2-4 (NOT ASSESSED with n_4b > 0 FAILS) is subsumed.

- **Reason:** CNA (room, about 11:57 AM ET, 2026-11-01) found that both all-undefined (all-D) and too-few-qualified-seed (Q-insufficient) replicates are **computed on system-generated trajectories**. Neither can therefore be shown, from the governing text, to be plant-determined. Each is a system-influenceable non-counting replicate, which could be used to drive the false-licence check to NOT ASSESSED.
- **Cost (recorded, as noted by CNA):** a row whose all-undefined cells are frequent by design can **FAIL on that alone**, even with correct withholding everywhere. This adds to the realization cost already disclosed at A49 L43.

## 2. Scope
- **Row 2 (N) is NOT included.** N is not a system-generated exclusion. **PENDING Astra.**
- This closes E2 §3's "E2-4 rows 1/3 (and N) scope — PENDING CNA" for rows 1 and 3. Row 2 remains PENDING Astra.

## 3. Open question for the next Astra consult
#50 Q1(e) only asks Astra to confirm the provisional extension. The next consult should ask: **can all-undefined (row 1) be shown to be plant-determined?** If it can, **only all-undefined is exempt**: row 3 and row 4b stay in the rule. Also carry forward the row-2 (N) exclusion (§2) for confirmation.

*DESIGN ONLY. Draft, not frozen. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: da5aec39632978c3f318caf1055b602a14560a69b02c7af914c88984b79e1ae0
