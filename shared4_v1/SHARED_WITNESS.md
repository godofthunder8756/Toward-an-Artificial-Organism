# Stage A: one coupled four-context R9 witness

Baseline repository HEAD: `e5bb8523c38b608143249e94a625628ad4f006e8`.
This is **analytic construction only**: no neural training, gradients, SGD,
hyperparameter sweeps, prior-artifact edits, or Stage B.

## Verified result

One actual `Arm("R9", 56)` uses the **same finite parameters** in contexts
0, 1, 2, and 3. The exact population mean joint loss is
**1031759/4687500 = 0.220108586667**. All four context joint losses equal
that number. Specialist population losses, also identical in every context:

| Specialist | Exact loss | Decimal | Prospective gate |
|---|---:|---:|---|
| S1 | 1/5 | 0.20000000 | **fails** strict `< 0.2` |
| S2 | 219259/1562500 | 0.14032576 | passes `< 0.18` |
| S3 | 8/25 | 0.32000000 | passes `< 0.5` |

The prior truly shared upper bound `8921732/29296875 = 0.304528452267`
improves by `3297651/39062500 = 0.084419865600`.
The singleton `0.176102...` result is **not** a shared four-context upper
bound and is not substituted here.

The selected joint gate is the exact R10 value plus `1/100`:
`21579431/117187500 = 0.184144477867`. The new upper bound does not meet
it. **The gate remains unresolved: an upper bound above the threshold
does NOT prove Case B, infeasibility, or a shared-class lower bound.**
No Stage-B model, experiment, or training plan is constructed.

## Actual finite architecture

The common recurrent trunk receives only the scheduled public input,
never context or any private reading. Eight units form a gain-32 signed
shift register. Sixteen units form the four cross-reading ANDs for each
neighbor factor pair `(0,1), (1,2), (2,3), (3,0)`. Thus 24 of 56 units
provide eight raw bits and sixteen neighbor products; other units are zero.
For an AND containing final bit 7, the current-input coefficient is 64,
the previous signed-bit coefficient is 32, and the bias is -64. Other ANDs
use two previous signed-bit coefficients 32 and bias -32.

The eight words are partitioned into four banks of two. For context `c`,
words `2c` and `2c+1` implement these local-bit action maps:

```
word 2c:   S1=(0,1), S2=(0,2), S3=(0,0)
word 2c+1: S1=(0,1), S2=(2,1), S3=(1,1)
```

Each word has **one global polynomial coefficient vector**, compiled into
one row of `W`. Its own bank's negative conditional risk, scaled by 100,
is the utility, with word tie penalty `-word/1000`. Additive `U` gives
offset 0 in that word's bank context and -1000 otherwise. There is no
context-dependent `W`, hidden-state context input, or history lookup.
At inference the encoder is precisely **`W h8 + U context + b`**.

The heads are actual affine layers on word-onehot8, context-onehot4, and
their **own** bit. Word coefficients and additive context offsets implement
the bank policies; own-bit slopes are shared globally per head. Policies
on unused word/context combinations are also defined by these same layers,
not arbitrarily overwritten. All sparse weights, including every parameter
shape and zero-fill rule, are persisted in `shared_witness.json`.
The diagnostic 256-by-4 mapping is verification output, never inference input.
Independent evaluators can call `shared4_v1.shared_witness.build_model()`
without arguments. It returns a fresh, unmodified actual `Arm("R9", 56)`
loaded from that JSON; its `state_dict()` can be loaded strictly into another
fresh Arm for evaluation. No solver or analytic assignment table is invoked.

## Bounded analytic attempt

1. One 20-second-limit analytic facility MILP selects at most two policies
   from the reduced 27-map alphabet. It finishes optimal in that finite
   class and supplies the two policies above. This is **not** whole-R9
   optimality.
2. One 90-second-limit analytic MILP holds the shared affine heads fixed
   and permits all eight global quadratic utilities plus additive context
   offsets. It considers 81 count beliefs per context only as proposal
   constraints; any accepted coefficients would have to compile into the
   actual recurrent network and pass rational and runtime checks.
   The solver times out **without an incumbent**. No improvement, lower
   bound, or infeasibility conclusion is inferred. The verified bank
   construction remains the best witness obtained in this bounded attempt.

There are no optimization restarts, neural fits, or Stage-B actions.
The solver outcome and scope are recorded in the JSON.

## Certification and reproduction

Population evaluation enumerates **256 public histories × 16 truths ×
2 private readings per specialist × 4 contexts**, using integer masses
and exact rational losses. Separately, posterior-based truth enumeration
checks the rotated conditional-risk polynomials and population totals.
The runtime also checks all eight private-bit triples for all histories
and contexts; words are private-bit-independent and each head implements
its own-bit policy.

The gain-32 signed features have exact-real error below `1e-26`:
each relevant final preactivation has magnitude greater than 31, giving
error at most `2 exp(-62)`; `exp(3)>20` and `exp(2)>3` imply the stated
rational bound. The smallest exact rational score gap is `1/1000`.
The saved certificate subtracts a conservative signed-feature error,
float32 coefficient representation error, and sequential float32 dot
product/addition bound. Both exact-real and conservative float32 margins
are strictly positive. Exhaustive actual float32 trunk evaluation further
confirms that all 24 features are the intended signed bits/products.

From the repository root:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest -q shared4_v1\test_shared_witness.py
```

Tests load persisted weights and never run either MILP or use gradients.
To reproduce the bounded constructor into a **fresh** output path:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python shared4_v1\shared_witness.py --seconds 90 --output C:\chosen\fresh_shared_witness.json
```

Only the four files in `shared4_v1` are deliverables. Older R10/R10A code
and results are read-only imports/evidence, not modified.
