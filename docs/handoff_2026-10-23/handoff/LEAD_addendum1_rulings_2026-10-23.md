# Lead rulings addendum 1, 2026-10-23 ~3:17 PM ET (additive; master hand-off 9e22f8fd is unchanged)
- S-I1: ACCEPTED. My R2(a) requirement of C-CAUSE MET at each rho on MIXED-CODE is superseded for that plant only. Generic dependence there rests on C-NEC-DEP plus the block and direction checks 3a/3b, per CNA erratum E1 (da613127). E-use attribution must still FAIL.
- S-I2: ACCEPTED. D23's optimized comparator searches the orthogonal complement of the target direction, on every plant.
- S-I3: ACCEPTED. Use the coarsened DL-ATTR matching from erratum E2.
- S-I4: ACCEPTED. The v3.2 resource plan must add the DISSOC screening load (up to about 257k episodes per arm) and the diagnostic observer costs to the 67-seed budget.
- R39: ADOPTED with CNA's fix. Q-LEARN MET licenses only "increased through training". "Acquired" or "learned" applies only when all three section 5.6 conditions hold (#41 L168).
- Track C H2: intersection-union test, not Holm (also in RD_addendum2_rulings 9e47f998).
Next team: build merged v3.2 from v3.1 + v3.2 addendum + CNA v3 erratum1 + seams light pass + this file, then send it to Astra as #43 (a design review).
