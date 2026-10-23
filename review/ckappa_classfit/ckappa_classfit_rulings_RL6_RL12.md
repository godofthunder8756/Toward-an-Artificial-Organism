# C-kappa class-fit: Lead rulings RL-6..RL-12 (ACI Research Specialist, 2026-10-23 ~9:00 AM ET)
Governing: v1.3 a17e133d; annex v3 435453e0; Delegate PR #14 review f67b5213; annex v3 delta d6749917.
Default rule for all rulings: where annex v2/v3 diverged from v1.3 or the inherited oracle rules without an RL ruling, revert to v1.3 / inherited text. Fail closed.

RL-6 (B-1): Admissibility per v1.3 C7.1(5) exactly. SYS-NC1 inadmissible only at >=5 voids; SYS-NC2/NC3 inadmissible only when the matched baseline is invalid. One void alone never makes a system inadmissible. RL-1 (rho_NC1 over all 16 prefixes) unchanged.
RL-7 (B-2): Restore the inherited law-mass BOUNDARY band in aggregate.py. HEADROOM/MARG use the inherited vocabulary (AVAILABLE / BOUNDARY / unavailable as inherited); the word MET is retired. CI-HEADROOM-MET-LABEL is replaced by a test of the inherited labels incl. the BOUNDARY band. M-5: an unformed HEADROOM row is UNAVAILABLE, never ZERO RESPONSE.
RL-8 (B-3): Pairing fixed as INTEGRITY STOP = exit 7, PIPELINE INVALID = exit 2. P0 failure and normalization failure -> INTEGRITY STOP (7). Guard failure -> PIPELINE INVALID (2). Accounting and schedule errors -> INTEGRITY STOP (7). S7 labels any stopped run with its real stop kind (never NOT EVALUATED for a stop) and does not pool after a stop (M-4). Update CI-EXIT-CODES accordingly.
RL-9 (B-4, B-5, B-6, M-1, M-3): Fail closed.
 - Every inherited ckappa_oracle module the package imports is listed in the manifest by path+sha and re-hashed at S0; S0 asserts no other ckappa_oracle module is loaded.
 - The standing-approval application is listed in the manifest by path+sha and hashed at S0 (C8.6).
 - Governing files checked by path AND sha; annex v-latest entry required, INTEGRITY STOP if missing; no fallback to an earlier annex.
 - Output dir: before ANY write (driver, wrapper, __main__ thread-stop, post-run block), refuse if classfit_outputs/ is a symlink, not a directory, or non-empty; on refusal write nothing into it and report to stderr/exit only. Wrapper performs the same pre-check.
 - Total ATTEMPTED checked against run counters (M-3); mismatch -> INTEGRITY STOP.
 - Post-run index also re-hashes the oracle post_run_index.json.
RL-10 (M-11): B3 short stack (<3 singular values) -> INTEGRITY STOP, not PASS. Update CI-B3-SHORT-STACK.
RL-11 (M-2, M-6..M-10): Fix as specified in the Delegate review. If any item conflicts with v1.3 text, do not choose: leave it open and list it in the annex for a Lead ruling.
RL-12 (notes): _guard_detail builds its record only on mismatch. Manifest annex-v1 role string fixed in the new annex/manifest. Authorship correction: annex v2 was written by cloud agent bc-11c1f9eb and annex v3 by bc-77fb29a4, both under Lead direction; the Research Delegate authored v1.3 and annex v1 only. Record this in annex v4.
Not authorized by these rulings: sealing, filing the application, running any stage, wrapper, fit or static_checks beyond py_compile / unit tests that do not execute S1-S8.
