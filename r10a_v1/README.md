# R10A analytic certification only

No neural training. No edits to primary or original R10 findings.
See the [endpoint answer and analytic stop](../R10A_DECISION_v1.md).

## Published artifacts

* [baseline hashes](baseline_hashes.json): original 1032-file inventory.
* [decoder bounds](decoder_bounds.json): positive/negative S3 bounds and
  unrestricted R10 recheck, with exact integer proof trees.
* [full deployed class certificate](class_certificate.json): finite
  recurrent encoder, rational heads, exact gap decomposition.
* [ladder certificate](ladder_certificate.json): one-feature/one-unit
  task-minimal correction and six specialist relaxations.
* [context bounds](context_bounds.json): exact attainable all-context
  bracket and held-out ambiguity, **not** a coupled optimum certificate.
* [independent audit](independent_audit.json): distinct mathematical review.

## Replay without optimization or training

From the repository root:

```powershell
python r10a_v1\preservation.py r10a_v1\baseline_hashes.json --check
python r10a_v1\verify_bounds.py r10a_v1\decoder_bounds.json
python r10a_v1\verify_class.py r10a_v1\class_certificate.json
python -m pytest r10a_v1 -q
```

The solver-free risk/bound replay uses exact integer/Fraction arithmetic.
Full deployed-witness replay additionally uses Torch for inference only.
No optimizer, fit, fine-tuning, training seed or scientific final is run.

The proposal and witness-generating commands require **fresh output
paths**:

```powershell
python r10a_v1\solve.py C:\chosen\fresh_bounds.json
python r10a_v1\certify_class.py r10a_v1\decoder_bounds.json C:\chosen\fresh_class.json
python r10a_v1\ladder.py r10a_v1\decoder_bounds.json C:\chosen\fresh_ladder.json
python r10a_v1\context_bounds.py r10a_v1\class_certificate.json C:\chosen\fresh_context.json
```

SciPy MILP/LP supplies candidate books/prices only. Published integer
lower bounds and constructive matching upper bounds establish exactness.
No trust in a solver's floating "optimal" status is required.

Main endpoint optimum: `5159249/29296875`.
Unrestricted optimum: `5101889/29296875`.
Single-context map counts: S1/S3 `12866`, S2 `7740507`.
Exact full-four-context counting has a finite rational-feasibility
characterization but its numeric sums remain unevaluated. The jointly
shared four-context neural-family optimum also remains unresolved.
Do not silently turn either limitation into a completion claim.
