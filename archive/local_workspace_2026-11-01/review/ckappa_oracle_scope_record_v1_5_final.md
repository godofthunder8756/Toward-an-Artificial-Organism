# C-κ oracle-only scope record v1.5_final (final pre-seal amendment; not sealed, nothing run)

Constitutive agent, 2026-10-22 (ET). Additive: every existing file is left unchanged. This applies the Research Lead's final ruling of 2:12 AM ET.

## 0. Precedence (frozen)
1. **Order:** v1.5_final (this file) > precedence note `ckappa_oracle_scope_precedence_note_v1_4.md` (`052505434dd7da07f7e37402468363fe92487cfc01ad511423eb675e9ffec853`) > v1.4 (`160ddfd5825dc36e230b06334d874deee080001dca6de4bff4e49d5b105ba7fb`) > v1.3 (`f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5`) > v1.2 (`7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d`) > v1.1 (`e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c`). The verbatim E36-1..14 text (v1.3 §1) governs over all of them.
2. **Non-governing in full.** These are hashed in the manifest and marked as non-governing:
   - v1.4_N (`3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359`);
   - `ckappa_oracle_scope_v1_4_N_closure_note.md` (`4ad1d217aaab0bd45d2be6fd3e24872a4b22407d0c8abc2fa36a5a1ac7c45c9c`).
3. **Frozen values that follow from this order:**
   - `rcond=1e-8` with the rank check before each fit (v1.4 N3);
   - whole-fixture O7 RESTRICTED COMPARATOR NOT ADMISSIBLE (v1.4 N4(ii));
   - 4×10⁹ bytes;
   - §6 seeds 36100–36109.
4. **Checked against:** the Delegate's delta check `ckappa_oracle_scope_record_v1_4_delta_check_RD.md` (`6a1c8168ad9c14543a80fb224006b60ebb24ab9b129f4e28ae5c3485b32f57d4`).

## 1. B1. Rank-unresolved reference (inserted into v1.4 N1)
Insert between v1.4 N1 step 2 (REFERENCE COVERAGE NOT MET) and step 3 (ZERO RESPONSE). Text quoted verbatim from the Delegate's check:

> "REFERENCE RANK UNRESOLVED: any fold's O6 B or B_μ design is rank-UNRESOLVED; no pooled §5 statistic is formed."

The resulting N1 order is:
1. PIPELINE INVALID
2. REFERENCE COVERAGE NOT MET
3. REFERENCE RANK UNRESOLVED
4. ZERO RESPONSE
5. HEADROOM NOT MET
6. BOUNDARY
7. MET or AVAILABLE

The first match wins. The rule applies separately to ALL and MARG, both of which use the same O6 B and B_μ fits (E36-3).

## 2. N-a. Hard timeout at 595 s
- The wrapper's hard timeout is **595 s − (now − T0)**, so the wrapper writes `post_run_index.json` inside the 600 s cumulative cap.
- A kill at the hard timeout is reported as CAP REACHED.
- The v1.4 n3 values are unchanged: a 60 s reserve, a soft deadline at 540 s, and a projection halt if T_rem > 540 s − T_elapsed.

## 3. N-b. Reproducible per-array hashes
- `results.json` holds one record for each drawn array: Q, Q₂, and the O4, O6 and O7 direction arrays. Each record gives the name, the shape, the dtype (`<f8`) and the sha256 of the array's C-contiguous little-endian raw bytes.
- `drawn_arrays.npz` is written alongside it. NumPy embeds a timestamp in `.npz` files, so the `.npz` file hash is not a reproducibility check.
- The precedence note's `outputs/drawn_array_hashes.json` carries the same records.

## 4. O7 σ at valid prefixes when NOT ADMISSIBLE (descriptive only)
- If O7 reads RESTRICTED COMPARATOR NOT ADMISSIBLE under v1.4 N4(ii), the package still computes and reports the singular values (σ₁ and σ_i/σ₁) of O7's stacked forecast Jacobian over the **valid-baseline prefixes only**, taken about O7's own baseline chart.
- This is **descriptive only.** It triggers no stop: the N4(i) σ₃ stop does not apply to it. It forms no predictions and does not change the admissibility label.
- A resolved third direction in it is reported as an integrity note in `REPORT.md`.

## 5. Manifest item 1
Add sha256 of this file. List the governing order and the two non-governing files exactly as in §0.

Nothing executes before the standing-approval application is filed and the manifest is sealed. The claim ceiling is unchanged: oracle-only.
