# Track B freeze preparation v2.5: ERRATUM 2, CORRECTION 3 (Lead) — final NOT ASSESSED rule (row 2 included); exact Fisher–Yates bias figures

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** A new, additive file. Under the binding no-rewrite rule (11:53 AM ET), it amends by supersession only:
- `review/trackB_freezeprep_v2_5_erratum2_Lead.md` (sha256 `81bdfcf29ad81ac20b4effbdb8434664d82b67e0f96f3f0345504950079f4569`; "E2");
- `review/trackB_freezeprep_v2_5_erratum2_corr1_Lead.md` (sha256 `c2c839210580f1b037580fd977421fa0cd2faaedb6a3d781ee80741f12cce212`; "C1");
- `review/trackB_freezeprep_v2_5_erratum2_corr2_Lead.md` (sha256 `5100f4de826dacbd422be92e056f58578fc9a5c332353885ebb0f50f62cf8092`; "C2").

All three files are read-only and not edited. C2 was already chmod 444 when the Lead's update arrived, so this correction is a new file. Only computation: SHA-256 and exact integer arithmetic.
- **Written:** 2026-11-01, about 11:59 AM ET, by the Lead's executor.
- **Not reflected in #50 v4,** which is being sent as built (body ef92dff3…, manifest 57c0915d…).

## 1. NOT ASSESSED rule — FINAL wording (supersedes C2 §1–§3 and E2 E2-4's extension; supersedes V25 L56 for this case)
> **"NOT ASSESSED passes only when n1 = n2 = n3 = n4b = 0; otherwise the row FAILS."**

Here n1 = all-undefined (all-D, v2.5 row 1), n2 = N (row 2), n3 = too-few-qualified-seed (Q-insufficient, row 3) and n4b = BOUNDARY/UNRESOLVED (row 4b). The rest of V25 L56 is unchanged: a FAIL if FL is assessed and fails, or if row 0 records a licence.

- **Row 2 (N) IS included.** This reverses C2 §2 ("Row 2 (N) is NOT included … PENDING Astra"). Reason (CNA, room, about 11:58 AM ET): N depends on the system too, and an N replicate already scores real_i = 0, so including it penalises nothing honest.
- **Reason for rows 1 and 3** (unchanged from C2, CNA about 11:57 AM ET): they are computed on system-generated trajectories and cannot be shown, from the governing text, to be plant-determined.
- **Cost (recorded in C2, still applies):** a row whose all-undefined cells are frequent by design can FAIL on that alone.
- **Open question for the next Astra consult (replaces C2 §3):** can any of rows **1, 2, 3 or 4b** be shown to be plant-determined, and so narrowed back out of the rule? #50 Q1(e) asks only about the earlier provisional extension.

## 2. Fisher–Yates bias figures — settled (closes the C1 / E2 §3 question "CNA to confirm")
CNA's exact rational recomputation over m = 2…508 agrees with C1. **The frozen text states the exact maxima:**
- absolute |P(idx = i) − 1/m|: **5.3999 × 10⁻²⁰, at m = 257**;
- relative |m·P(idx = i) − 1|: **2.6455 × 10⁻¹⁷, at m = 504**.

It **keeps 2^−64 (5.4210 × 10⁻²⁰) and 508/2^64 (2.7539 × 10⁻¹⁷) as the stated bounds**. The 5.42 × 10⁻²⁰ in E2 E2-1 is read as the 2^−64 bound, not as a maximum. Executor re-check (exact integers, r = 2^64 mod m; powers of two give 0): absolute max 5.3999e-20 at m = 257; relative max 2.6455e-17 at m = 504. Both agree.

## 3. Status
| Item | Status |
|---|---|
| NOT ASSESSED rule scope (rows 1, 2, 3, 4b) | FIRM (this file); narrowing is an open question for the next Astra consult |
| E2-1 absolute figure (5.42e-20 vs 5.40e-20) | CLOSED (§2) |

*DESIGN ONLY. Draft, not frozen. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 8d420ab1b9fbee4745cedf430b3e9cfc57feb3230617fb290faa40afa0122b2f
