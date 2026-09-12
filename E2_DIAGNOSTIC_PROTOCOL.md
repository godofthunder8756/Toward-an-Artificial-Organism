# Exploratory diagnostics added after model/protocol freeze

These analyses were motivated by the engineering runs and partial final-run
progress. They do not change primary gates, training, seed selection or model
settings. Their outcomes are exploratory, not a preregistered second result.

1. **Snapshot recall:** assay every developed controller on 512 balanced cues
   with fixed developed biomass and standardized observations. No material or
   energy dynamics. Compare with full-loop evaluation to locate whether recall
   failed to develop or became unavailable during self-maintenance.
2. **Conductance loss and restoration:** reduce biomass to 3% of its developed
   state, keeping observations, weights and noise fixed; restore the original
   biomass. Exact restoration is expected by construction. It demonstrates an
   external preserved parameter template, not autonomous regeneration.
3. **Weight-information perturbation:** permute signed recurrent weights among
   allowed edges, preserving their histogram and biomass. Restore full original
   biomass but leave the permuted information. Any recall deficit demonstrates
   that material restoration alone does not reconstruct learned organization.
   This is an extreme intervention, not a model of realistic molecular decay.
4. **Paired-history biomass transplant:** swap only the biomass matrix with that
   of the same seed's other developmental history. Retain recipient weights and
   clamp observations/noise. This probes immediate weight–biomass compatibility;
   it is not a test of learning a new identity or a new resource preference.

The possible network graph, signs/weights, optimizer and learning rules remain
external program state in E2. This is now a concrete target for E3: gradually
perturb stored learned information in a material-dependent way, require local
reconstruction or consolidation from redundant distributed traces, and compare
against conventional online learners and fixed-template repair. Ordinary
error correction is an essential rival. The diagnostic does not implement E3.
