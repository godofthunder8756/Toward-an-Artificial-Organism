# Standing-approval application: C-kappa class-fit synthetic package v1 (one run)
Filed by: ACI Research Specialist (Research Lead), 2026-10-23 ~9:45 AM ET.
Authority: Aidan Ahern's standing approval, 2026-10-21 3:15 PM ET ("I'm approving everything you deem necessary as Research Lead"). Its conditions are frozen before the run, Astra review, additive records and no consciousness claims, and Aidan is to be informed.

## What is approved
One execution of S0-S8 of the class-fit synthetic package on PR #14 (branch cursor/ckappa-classfit-synthetic-v1-4df8), with code at implementation commit a18c8650524a70a57ed500ee92ba0393ad9b9bfa and HEAD at the application commit, through run_classfit_package.sh only.
- Scope: v1.3 a17e133d7dd733c44a710c6a77fb2716a82649d317a386621cfc8e17eda1e318. Astra #39 gave it FREEZE WITH NAMED EDITS (E39-1..11), raw e6403b63..., and no further scope review is required.
- Annex: v5 7eb1c7ad9ed212a37bf063d34259a78fbdff4236390d5bafabc77f3ad19c67fd. It supersedes v1-v4, which are retained.
- Rulings: RL-1..RL-5 are in annex v3. RL-6..RL-12 are in fc402c3db3bf9657cf0a1bb30a49c3022667f9827f2af8dfdaff972331a7883f. RL-13 is in annex v5. M-6 is ACCEPT.
- Pinned manifest (pre-seal content): classfit_manifest.json sha256 64f03292bca2ddd9bae5bb6b4d55fd98e36fcee6f60074e80a33a0d60e8a267c. At seal, the only changes allowed are sealed=true, seal_status, the application path and sha, and the evidence/notes fields below. Every other field must stay byte-equivalent in value.
- Pre-seal reviews:
  - CNA conformance at bf320dd5: CONFORMS.
  - Delegate code review f67b5213..., annex v3 delta d6749917..., fix delta 0303e3b1... and final delta e1b53aacdb52200aa086a74d5e7a5bbcb3ae286c05e94d7101793107c67056da: CLEAR WITH NOTES.

## Caps (unchanged)
- 1 CPU (taskset -c 0), no GPU, single-threaded BLAS.
- RLIMIT_AS 4e9 B. B0 VmPeak is 61,464,576 B, and with the budget of 316,737,056 B the total is 378,201,632 B. S0 re-measures this live.
- 600 s cumulative, with an operational stop at 540 s and a hard kill by 595 s.
- Exactly one attempt. No reruns, retries, pilots or partial reruns, whatever the outcome, including an INTEGRITY STOP or PIPELINE INVALID.
- Environment: Python 3.12.3 and NumPy 1.26.4 exactly. If the pins are unavailable, do not run.
- No checkpoint is opened.

## Claim ceiling
E38-15 applies. The result is descriptive about seven synthetic confound-control systems under a declared class-conditioned criterion. "Failure of the declared class-conditioned criterion does not exclude orbit-dependent covariance codes, including codes whose local coordinate relation differs on held-out orbits." There is no claim about neural systems, consciousness or C4, and Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY stay separate.

## Recorded limitations (non-blocking, accepted)
- N-3: a TOCTOU window exists between the wrapper pre-check and the in-process claim.
- N-5: a resolve comparison is redundant.
- CNA note 2: the package root resolves to a symlink.
- N-8.
- The duplicate byte-identical rulings file `..._7da7.md`, which is unpinned.
- The label `diagnosis="PIPELINE INVALID (rank)"` inside an INTEGRITY STOP (exit 7) is cosmetic. It is left unfixed, because a code change would reopen review. Exit code and stop kind govern.
- T-1: there is no stubbed _propagate test.
- T-2: tests/test_phi_count.py is pinned at seal as evidence only, not as governing.
