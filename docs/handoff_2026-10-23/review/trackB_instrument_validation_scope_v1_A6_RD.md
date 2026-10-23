# Track B instrument-validation scope v1: Amendment A6 (additive; RD)
- **Amends:** A5 `0e26af91971c879378bf947fd01d6e1e452bcad62e02e7dcdd19ce88ed1c6a6f`. A5 is unchanged, and A6 governs wherever the two conflict.
- **Source:** the Lead's ruling in the room, 2026-10-23, about 11:01 ET, which withdraws the Lead's earlier D2 reading.
- **Status:** DRAFT, NOT FROZEN, NOTHING RUNS.

## A6-1. D2 stays as frozen in A1-2 (supersedes A5-1)
D2 is "the agent is a learned RL agent", as frozen in A1-2. A frozen definition is not reinterpreted after seeing papers that challenge it. The reading "the self-model is learned by the agent" is withdrawn as a criterion. That the self-model is learned rather than supplied is kept only as a stated difference.

## A6-2. Q-NECESSITY label (restates A5-2 under A6-1)
Q-NECESSITY is an **EXTENSION** of both Wilterson & Graziano 2021 and Asan 2026.
- **Against Wilterson & Graziano**, what survives is D1 (interoceptive content, not attention) and D4 (same-size ablations of other modules plus a sham). There is also a stated difference, not a criterion: our self-model is learned, theirs is supplied by the experimenters.
- **Against Asan 2026**, what survives is D3 (a viability outcome) and D4. D3 carries a caveat: the measure behind Asan's 82%→10% under input masking is not named, and if it is survival, D3 fails too. A further stated difference: our agent is recurrent, Asan's is feedforward.
- Also included is the required A-EXT bypass arm (A4-1).

The remaining argument, that a pattern decoded from a policy layer is not a "self-model", goes to Astra under AQ-P1. The team does not rely on it.

## A6-3. Asan suggestions renamed as Astra questions (supersedes the A5-5 numbering)
- AQ-S1 becomes **AQ-A1**: the subspace matching rule.
- AQ-S2 becomes **AQ-A2**: the body-variables-hidden arm.
- AQ-S3 becomes **AQ-A3**: the decoy-needs navigation control.
- AQ-S4 becomes **AQ-A4**: Asan's negative results as priors.

None of these is adopted. Each is for Astra to rule on.

## A6-4. Freeze status
The last freeze-blocking reads are cleared by `badf7258…`, per the Lead. P3 (repeating the OpenAlex and Semantic Scholar lookups) is carried as a recorded limit, not done. The A5-6 limits stand.
