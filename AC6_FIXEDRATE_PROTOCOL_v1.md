# AC6 fixed exploration controls, before results

2026-09-15. Do not modify frozen AC6. Test the simpler alternative to adding
learned probe regulation: fixed probabilities1/512,1/1024,1/2048,1/4096 plus
frozen maintenance. Seeds400–407,8192 ticks, identical noise/support schedule
and all physical/learning laws. Total40 rows; common uniform exploration draws
thresholded at each rate ensure paired inputs. Every configuration is retained.

The one-bit commitment still updates from crossing feedback; only its exploration
probability is fixed. These are controls for future adaptive exploration, not
nonlearning organisms in every respect. No new acquired state is introduced.

Repeat AC6 survival>=7/8,activity>=.9, late support omission>=.8 with activity>=.9,
late return maintenance>=.8, support B0 births<=half frozen, and structural
accuracy>=.99 among completing individuals. Additionally report paired total
material spending difference versus frozen with descriptive95% bootstrap intervals
(10000 resamples, seed20260914). Net efficiency requires a negative mean spending
difference with interval upper bound<0, alongside viability/behavior criteria.
Report energy, exports and phase-specific data; lower spending through death is
not success. Material endpoint measures gross consumed precursor, not biological
efficiency or a complete free-energy budget.

Source hashes before run, incremental rows, full inventory audit, exact runner
equivalence at probability1/512 and exact sampled replays after results. This
is a small engineering grid, not independent confirmation or exhaustive proof
about fixed rates. A passing rate would need fresh validation; do not attribute
its behavior to learned exploration. A failure only narrows this tested grid.
