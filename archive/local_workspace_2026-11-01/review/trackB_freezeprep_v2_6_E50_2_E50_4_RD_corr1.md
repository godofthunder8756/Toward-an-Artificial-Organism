# Track B freeze preparation v2.6 E50-2/E50-4 (RD): CORRECTION 1

- **Author:** Research Delegate (RD)
- **Date/time:** 2026-11-01 12:13 EST (America/New_York, from `date`)
- **Status:** DESIGN/TEXT ONLY. This is an additive correction; the target file is not rewritten (binding rule: "NEVER rewrite a read-only file").
- **Target:** `/workspace/review/trackB_freezeprep_v2_6_E50_2_E50_4_RD.md`, whole sha256 `8a36920898f8a2aece46189631f4c5592719f0c4e5a566cf5687ba1dbc28fc73`, footer `c29401c458a408ebd73a93f94c89a91f3a6da2f6464bbee84b1724a95fbc3520`.

## K-1 Citation precision in §2, "Scope" line (no content change)

The target says: "Scope: networks only (M L1129 "Network instruments only."). Scalar plants keep t_s = 0 and x_ref = x_lo (M L1127)."

The frozen M (merged v3.6, `ab80afa5…`) does not yet contain those words:
- M L1127 reads "t_s = 5τ in plants (residual e^−5 < 1%); 20 steps in networks".
- M L1129 reads "2 × the median absolute deviation of ‖x_ref − median x_ref‖ in null-input runs on the fitting partition, with no probe input".

The quoted words are the **proposed replacement wording** in V25 §6.1 (`d101438d…`, L180 for M L1127 and L181 for M L1129; R6 at V25 L25).

**Corrected line:** "Scope: networks only, per the proposed V25 §6.1 replacement for M L1129 (V25 L181: prefixed "Network instruments only."). Scalar plants would have t_s = 0 and x_ref = x_lo per the proposed V25 L180 replacement for M L1127. Both are pending adoption, since frozen M L1127 still reads "t_s = 5τ in plants"."

The citation of "t_s = 20 steps (M L1127)" for networks in §2.1 is correct as it stands: frozen M L1127 says "20 steps in networks".

No other change.

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: a43bae6449f461b90062469947ea5511092954524ec7ec768a58d097c5f274e2
