# C-kappa oracle erratum 1

Additive close-out for PR #13 at `14376f38fe09157eef85bfac1cc4a4433d49bebc`. Labelling only.

The items below are labelling only. None of them changes any result. `manifest.json`, `outputs/`, and `post_run_index.json` stay untouched. No package file is edited. Nothing is re-executed.

## (a) `phase`

`results.json` `phase: unsealed-implementation` is a hard-coded constant (`driver.py:39`). Preflight opened only the sealed `manifest.json`, refuses an unsealed one, and the M1 re-hash passed.

## (b) Leftover draft text in the sealed manifest

The sealed `manifest.json` carries leftover DRAFT/UNSEALED/placeholder text at lines 2, 4 and 11. Nothing reads it, and the fields that do govern are `sealed: true` and FILED.

## (c) Version fields

The Python and NumPy fields in `results.json` are pinned constants (`driver.py:45`). The real versions were asserted by preflight, which passed.

## (d) Elapsed time

21.8 s is package-elapsed time.

## (e) Memory figure

The VmHWM of 41 MB is not in any committed file, so it is UNVERIFIED.

## (f) Which `sigma_1`

The sigma_1 of 1.079 belongs to the g fit. The O7 Jacobian has sigma_1 1.51 and sigma_3/sigma_1 <= 7.2e-16.

## (g) `exact_reduction_to_cross_term`

`exact_reduction_to_cross_term=false` is a tolerance artifact of the frozen exact-zero test at `stages.py:796`, since the off-target coefficients are ~1e-17.

## (h) O5 law mass

The O5 law mass is unnormalized, out of a total of 128, so the s=0.5 exclusion is 8.39/128 = 6.56%.

## (i) Claim ceiling

O6 ALL MET and MARG AVAILABLE license only that an inference spec at k=4 may be drafted, with its own freeze. They say nothing about the GRU. O7's g(mu) is one explicit smooth system and is not the lookup rival (E35-2). Open design issue M-1 (orbit-symmetric cancellation of a global linear kappa row) is pending Astra consult #37.
