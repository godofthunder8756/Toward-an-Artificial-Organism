# Resume guide: Toward an Artificial Organism

## Current stopping point

The latest completed study is AC9 controls v3. It tests whether the useful
organization is tied to the physical location of acquired memory, rather than
to a developmental label or a protected software cache.

`ac9_controls_results_v3/results.json` contains 64 rows: four seeds, two
histories, and eight conditions. The primary result is:

- `keep`: 8/8 complete activity and 8/8 retain the acquired routes.
- `block_old`: 0/8 retain the occupied memory region; activity is 7/8.
- `block_other`: the unoccupied-region block does not remove the routes.
- `swap_block_old`: relocating the entire physical region preserves function,
  but blocking the relocated occupied region removes it (7/8 route loss).
- `read_disabled`: the memory remains physically present, but productive
  contacts fall to about one half, showing that material burden alone is not
  the functional result.
- `protected_block_old`: an external protected copy keeps behavior while the
  actual allocated entries decay; this is an explicit scaffold control, not an
  autonomous result.
- `fixed_correct`: externally supplied correct entries work, establishing a
  favorable fixed-allocation control rather than developmental autonomy.

The result supports a bounded claim: acquired functional organization is
maintenance-dependent when the organization is physically located in the
occupied compartment. It does not yet establish full autonomy, general
autopoiesis, subjectivity, or a rich developmental repertoire.

## Exact resume commands

Use the compatible interpreter (the default Python 3.14 environment does not
have NumPy):

```powershell
cd C:\Users\ahern\Documents\GitHub\Toward-an-Artificial-Organism
py -3.12-arm64 -B ac9_controls_v3.py
py -3.12-arm64 -B audit_ac9_controls_v3.py
```

The v3 result directory is frozen. Do not overwrite it; create a new
versioned protocol and result directory for any changed experiment. Run the
existing unit tests before extending the model:

```powershell
py -3.12-arm64 -B -m unittest -q test_ac1 test_ac2 test_ac3 test_ac4 test_ac4_transport test_ac5 test_ac5_program test_ac6 test_ac7 test_ac8 test_ac9 test_ac9_memory
```

## What to do next

1. Add and audit the missing integrated constituent ablations (especially
   W/C production and boundary transport) without changing the frozen AC9
   laws.
2. Add a new, broader developmental function with more than the present four
   routing classes and two unknown bits. Keep random-fallback survival and
   acquired-function retention as separate endpoints.
3. Test whether a controller can acquire the need to allocate or relinquish
   maintenance resources under an intervention chosen after development.
4. Preserve exact replays, source hashes, ledgers, and negative controls. Any
   successful result must survive protected-memory, relocation, inert-burden,
   and read-disabled comparisons.

Do not resume the stopped E3 v0.11 experiment or reinterpret the current
results as proof of full autopoiesis. The next breakthrough must show that the
system's own maintained organization changes its maintenance decisions under
counterfactual damage or scarcity, with no protected copy or externally fixed
correct state.

