# R10A: exact endpoint gap decomposition

All values below use the context-3 **population** risk, not finite-stream
means. The learned quantity averages the 16 original frozen R9 models.
The [full-class certificate](R10A_R9_CLASS_CERTIFICATE_v1.md) includes
the recurrent encoder, not just a relaxed lookup.

| Quantity | Exact value | Decimal |
| --- | --- | ---: |
| L_Bayes | `96/625` | 0.1536000000 |
| L_R10 | `5101889/29296875` | 0.1741444779 |
| L_R9_CLASS | `5159249/29296875` | 0.1761023659 |
| L_learned_R9 | `2003/6000` | 0.3338333333 |

| Excess-risk component | Exact value | Decimal | Fraction of total excess |
| --- | --- | ---: | ---: |
| Capacity: R10 - Bayes | `601889/29296875` | 0.0205444779 | 11.39882256% |
| Deployed class expressivity: R9_CLASS - R10 | `3824/1953125` | 0.0019578880 | 1.08630738% |
| Within-class shortfall: learned - R9_CLASS | `73936391/468750000` | 0.1577309675 | 87.51487006% |

The components sum exactly to
`L_learned_R9 - L_Bayes = 5407/30000`.

The known readout restriction is real, but explains only **1.0863%**
of total excess risk at this endpoint. The frozen learned model is far
from the best point the existing architecture can already express.
The witness also rules out an unavoidable encoder-representability
penalty beyond this class optimum.

The residual named `Delta_learning` is **not all optimizer failure**.
It includes representation acquisition, credit assignment, sample
efficiency, finite-training variation and held-out-context extension.
The [context audit](R10A_GENERALIZATION_BOUND_v1.md) exhibits
train-indistinguishable, materially different held-out extensions.
No exact causal allocation of this residual among those mechanisms is
identified by these population optima.

Machine-readable exact fractions and percentages are in
[class_certificate.json](r10a_v1/class_certificate.json).
Verdict B remains unchanged. No new neural experiment is run.
