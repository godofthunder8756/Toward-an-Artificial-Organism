# Block V Pre-execution Protocol Clarification Addendum

**Underlying preregistration:** 10.17605/OSF.IO/JZ4ED  
**Status:** must be publicly timestamped before any Block V confirmatory seed is executed.  
**Confirmatory data generated:** none.

## Why this addendum is necessary

A post-registration, pre-execution audit found two implementation-level ambiguities in the frozen Block V protocol. Choosing either after seeing confirmatory outcomes would create researcher degrees of freedom. Execution was therefore suspended before the first registered seed was run.

## Clarification 1 — H5.1 matched self-irrelevant control

The frozen H5.1 manifest requires an absolute S2-minus-S1 mean accuracy difference no greater than 0.05 on matched self-irrelevant controls, but `confirmatory_variants.json` does not define the exact self-irrelevant task.

**Frozen operationalisation for execution:** use the same held-out seed, external difficulty schedule, latent internal-state generation and base decision/verification task as the corresponding decisive family, but disable the optional confidence-sensitive checking or additional-computation action. The self-monitor is still computed and logged, but it has no causal route to alter the task action. The primary specificity metric remains accuracy and the frozen <=0.05 criterion is unchanged.

This operationalisation directly instantiates the H5.1 wording that monitoring should improve behaviour primarily when its output can alter subsequent computation or action.

## Clarification 2 — H5.6 metric precedence

The frozen H5.6 manifest says S2 must exceed each bypass by >=0.10 mean “accuracy or utility”, leaving a post-outcome choice between two metrics.

**Frozen operationalisation for execution:** utility is the primary H5.6 metric because both decisive task families contain preregistered costs for checking or additional computation. Accuracy remains a secondary descriptive outcome. RETAIN requires >=0.10 mean utility advantage over every preregistered bypass in both decisive families and >=18/20 seeds favouring S2. REDUCE applies if H_EXTERNAL remains within 0.05 mean utility of S2 in both families and reproduces the downstream control benefit.

This choice is made before any confirmatory outcome exists and removes the possibility of choosing whichever metric is more favourable after execution.

## Everything else remains frozen

No hypothesis, confirmatory seed, held-out variant value, architecture, misinformation level, impairment range, manifest hash or other decision threshold is changed.

## Execution gate

**Do not execute any Block V confirmatory seed until this clarification has been publicly timestamped.**
