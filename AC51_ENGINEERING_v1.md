# AC51 engineering: the effect size is bounded by value concentration, not spread or stress

2026-09-15. Engineering follow-up to AC50. **No protocol, no final seeds, no claim.** Answers the question
AC50 left open: can the ~11% production effect be enlarged?

## What was tested

AC50 froze the stable graded self-funded world (heterogeneous site value), with an ~11% effect. Three
levers for enlarging it were measured, all on the frozen AC50 world (period 4, drain 2, stress ×3,
regime-dependent values, the AC50 optima):

1. **Stress** (more sites die): ratio stays 1.06–1.12 across stress ×3–×12 (0 dead throughout). No
   enlargement — the order's control is diluted as stress outpaces the 1-renewal/tick capacity.
2. **Value spread** (10× → 50×): saturates (1.16 → 1.17). The ~90% of "common" sites that survive under
   every order dominate the denominator.
3. **Value concentration** (one region worth ~100× the rest): **ratio 1.11 → 1.35–1.38**, 0 dead.

| value structure | learner | keeper | ratio |
| --- | ---: | ---: | ---: |
| graded 10× `(5,4,3,2,1,0.5)` | 8929 | 8028 | 1.112 |
| concentrated 100:1 `(100,1,1,1,1,1)` | 62438 | 46229 | 1.351 |
| concentrated 100:0.01 `(100,0.01×5)` | 60024 | 43371 | 1.384 |

## Why concentration works, and what it means

The effect is the order's priority deciding *which* sites survive. Under a graded spread, the sites the
order can't influence (the ~90% that survive under every order) still carry comparable value, so they
dominate the denominator and cap the ratio. Concentrating the value makes the *differentiating* sites —
the critical region the good order keeps and the stale order loses — dominate the numerator, so the
order's choice shows up at ~38%.

This is a **principled** enlargement, not tuning: heterogeneous sites with a skewed value distribution is
the realistic case (a few critical constituents, many marginal ones), and it is exactly the regime where
the order's maintenance priority is load-bearing. It does push the endpoint toward a "keep the critical
region" shape, so a frozen successor (AC51) should re-check the gradedness of the endpoint (how many
critical sites survive, 0–4, not a binary) before claiming.

## Artifacts

Inline measurement (this file records it). Related: `AC50_RESULTS_v1.md` (the 11% base),
`AC50_heterogeneous.py` (the world), `AC49_ENGINEERING_v1.md` (the value-spread saturation).
