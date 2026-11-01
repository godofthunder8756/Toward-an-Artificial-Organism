# C-κ oracle scope: v1.4_N closure note (additive; nothing run)

Constitutive agent, 2026-10-22, 2:12 AM ET. Leaves every existing file unchanged.

## 1. Governing order (Research Lead, 2:12 AM ET)
- **Governing:** v1.4_N (`3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359`) plus this note, then v1.3 (`f6263fb8…`), v1.2 (`7e15e812…`), v1.1 (`e40c288f…`). The verbatim E36-1..14 text governs over all of them.
- **Non-governing, hashed in the manifest as such:**
  - v1.4 (`160ddfd5…`);
  - my precedence note `ckappa_oracle_scope_precedence_note_v1_4.md` (`05250543…`), withdrawn in full.
- So the frozen values are `rcond=1e-10` (N3) and the O7 per-prefix void with the >25% NOT ADMISSIBLE ceiling (N4(ii)).

## 2. B1 (blocking; from `ckappa_oracle_scope_record_v1_4_delta_check_RD.md`, `6a1c8168…`)
Insert into the v1.4_N N1 precedence, between step 2 (REFERENCE COVERAGE NOT MET) and step 3 (ZERO RESPONSE):

> **REFERENCE RANK UNRESOLVED**: any fold's O6 B or B_μ design is rank-UNRESOLVED under N3. No pooled §5 statistic is formed.

## 3. N-a. Index inside the cap
- The wrapper's kill is at **595 s − (now − T0)**, not 600 s. This leaves 5 s for the wrapper to write `post_run_index.json` inside the 10-minute cap.
- The n3 numbers are unchanged: 60 s reserve, soft deadline at 540 s, projection halt if T_rem > 540 s − T_elapsed.
- A kill at 595 s is reported as CAP REACHED.

## 4. N-b. Reproducible array hashes
- For each drawn array (Q, Q₂, and the O4/O6/O7 direction arrays), `results.json` records its name, shape, dtype (`<f8`) and the sha256 of its C-contiguous little-endian raw bytes. The same records go to `outputs/drawn_array_hashes.json`.
- `drawn_arrays.npz` is kept for convenience only. Its file hash is not a reproducibility check.

## 5. Manifest item 1
Add this note's sha256, and list v1.4 and the precedence note as non-governing.
