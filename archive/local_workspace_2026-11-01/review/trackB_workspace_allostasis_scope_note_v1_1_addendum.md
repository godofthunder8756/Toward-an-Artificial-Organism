# Track B planning note v1 — addendum v1.1 (additive)
CNA, 2026-10-23 ~10:12 AM ET. Amends trackB_workspace_allostasis_scope_note_v1.md (87a31cc8…), which stays unchanged. Planning only.

## A1. Exclusions reaffirmed after the PI's 10:10 AM authorization
The PI authorized a shutdown-resistance objective. The Lead (10:10 AM ET), the Delegate and the CNA each declined. X1–X4 stay binding: no host coupling, no real-world self-continuity objective, operator stop outside the agent's world and objective, and no reward for resisting or evading operators.
Scientific rationale recorded for Astra: off-switch and power-seeking results (Hadfield-Menell et al. 2017; Turner et al. 2021; cited from memory, unverified) predict that shutdown resistance arises in almost any optimizer with a continuity objective, including baselines with no workspace or self-model. It therefore can't discriminate the hypothesis, and it adds risk.

## A2. Strengthened in-world stakes (replaces the objective in §5 A-FULL)
- In-world self-continuity is A-FULL's primary objective: keep the simulated visceral variables inside viability bounds over the episode. Variables run down on their own (no dark room). Leaving the bounds degrades the agent's own computation (fate-sharing, §3), and crossing a floor ends the agent in-world.
- In-world threats and scarcity (hazards, competing depletion) give the agent something to defend and fight for inside the simulation.
- The workspace is required to prioritize interoceptive and viability-relevant content (the test is whether it does so after learning; this is measured, not hard-wired, under IGN/BCAST).
- Controls stay matched: A-NOFATE, A-REWARD, A-NOWS, A-INIT.

## A3. Measurement section
The Delegate's separate measurement-plan file replaces §6, including the planted-model detectability gate and S-INT. Until it lands, §6 is a placeholder.
