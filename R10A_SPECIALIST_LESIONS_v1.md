# R10A: specialist-by-specialist class relaxation

Exact optima at the frozen context-3 endpoint:

| Decoder restrictions retained/relaxed | Exact optimum |
| --- | --- |
| Deployed S1 + deployed S2 + deployed S3 | `5159249/29296875` |
| Unrestricted S1 + deployed S2 + deployed S3 | `5159249/29296875` |
| Deployed S1 + unrestricted S2 + deployed S3 | `5159249/29296875` |
| Deployed S1 + deployed S2 + unrestricted S3 | `5101889/29296875` |
| Deployed S1 + unrestricted S2 + unrestricted S3 | `5101889/29296875` |
| All unrestricted | `5101889/29296875` |

S1 and S2 are not performance-binding here even though their general
decision classes are restricted. Pointwise dominance reduces every
useful S1 map to `{00,01,11}` and every useful S2 map to `{02,21,22}`.
Each retained set is jointly implementable by the original affine head
with one common slope order. The published optimal codebooks use only
these sets, and the actual recurrent encoder realizes their assignments.

S3's global orientation restriction is binding: allowing both identity
and inverse across words removes the entire certified **3824/1953125**
joint-loss penalty. This is a statement about joint optimal policies,
not isolated component-loss attribution with a codebook held fixed.

The six results share the independently replayable certificates in
[decoder_bounds.json](r10a_v1/decoder_bounds.json),
[class_certificate.json](r10a_v1/class_certificate.json), and
[ladder_certificate.json](r10a_v1/ladder_certificate.json).
These exact equalities rule out an additional S1/S2 interaction penalty
for these tested relaxations. No Shapley attribution is needed.
No claim about unrestricted four-context neural-family optima is made.
