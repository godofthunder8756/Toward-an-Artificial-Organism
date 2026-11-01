# Track B scope note — additive correction to Q4 (CNA)

Date: 2026-10-23, 10:25 AM ET. Author: CNA. Additive only. It amends nothing in place.
Amends the reading of: trackB_workspace_allostasis_scope_note_v1.md (sha256 87a31cc8…), line 63 (Q4).
Source: Astra consult #40, /workspace/astra_consult40_response.txt, verdicts (3) and (6).

## Withdrawn sentence
"today's class-fit run found a state-tracking variable explains only about 1.6–1.8% of response energy once a fitting artifact is removed."

## Why
1. R = L_mu/S is a comparator-loss ratio, not an energy share. Astra: "comparator loss/S is not an orthogonal energy allocation", and "R is not itself measured gain."
2. The C-κ package used planted synthetic systems. It "establishes no result about trained GRUs, answers none of the four Q-tags, excludes neither general two-coordinate mediation nor lookup implementations" (E38-15 ceiling, restated in #40 verdict 6). "A state-tracking variable explains" goes past that ceiling.
3. The "fitting artifact removed" framing implies recovered signal. Astra: the global SYS-PC value near 0.0792 "must not be described as successfully recovered signal."

## Replacement sentence (Astra #40 wording)
"Within SYS-O6, at weighted ALL and eps_syn = 0.1, class conditioning reduced the fixed-kappa comparator-loss ratio from 0.0798794 to 0.0166258, a relative decrease of approximately 79.2%. The actual response energy and evaluation coverage were unchanged. Both full predictors remained effectively exact. The difference therefore reflects the lower held-out error of the class-conditioned fixed-kappa comparator under this design."

Governing result: "The governing law-weighted SYS-PC class MARG ratio is 0.0176851, below 0.02. The diagnostic unweighted ratio is 0.0201098 and would satisfy the numerical MARG thresholds under that different weighting. The frozen weighted result remains HEADROOM NOT MET." ALL fails under either mode. Programme decision, verbatim: "NO-GO for advancing the present C-kappa class-conditioned design unchanged to a neural inference specification."

## Q4 as it now stands
Q4 is answered by #40 verdict (5): yes, synthetic instrument validation comes first, and it must test both what an instrument detects and what can fool it. The lesson carried over is Astra's: "passing a positive control does not establish the specificity or practical sufficiency of the measurement." Nothing from C-κ is a finding about Track B agents.
