# C-κ oracle scope: precedence note after the crossed v1.4 / v1.4_N files (additive; nothing run)

Constitutive agent, 2026-10-22, 2:10 AM ET. Leaves every existing file unchanged.

At 2:09 AM ET I wrote `ckappa_oracle_scope_record_v1_4_N.md` (`3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359`) to follow the Research Lead's 2:09 rulings: rcond=1e-10 and a 25% per-prefix O7 ceiling. It declared itself governing. At 2:10 AM ET the Research Lead accepted `ckappa_oracle_scope_record_v1_4.md` (`160ddfd5825dc36e230b06334d874deee080001dca6de4bff4e49d5b105ba7fb`) instead, including rcond=1e-8 and whole-fixture O7 NOT ADMISSIBLE, and withdrew the 2:09 rulings on those two points.

**Ruling recorded:**
- **Governing order:** v1.4 (`160ddfd5…`) > v1.3 (`f6263fb8…`) > v1.2 (`7e15e812…`) > v1.1 (`e40c288f…`). The verbatim E36-1..14 text governs over all of them.
- **v1.4_N (`3f0c5c12…`) is NON-GOVERNING in full,** including its §0 claim to govern. The manifest hashes it and lists it as non-governing.
- **Two v1.4_N details carried into v1.4 because they are consistent with it:**
  1. `run_package.sh` is among the files the application cites.
  2. Each drawn array (Q, Q₂, O4/O6/O7 directions, as C-contiguous little-endian float64 bytes) has its sha256 written to `outputs/drawn_array_hashes.json`, alongside v1.4's `drawn_arrays.npz`. Both are hashed in the post-run index.
- **Manifest item 1** gains this note's sha256.
