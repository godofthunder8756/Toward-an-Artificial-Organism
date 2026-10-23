# Graded joint recurrent reversion, phase B

Phase B is the confirmatory phase on fresh seeds 200–209. The denominator is 10. Seeds are not removed from it. Phase A is not pooled with these seeds.

- Code version: graded-reversion-v1
- Protocol sha256: `1a5e62bd034c579eed70d477251650aefdf1cd395834184bc564f5a16689bfa3`
- Freeze commit: `9808759ffd4dfd417014b22c6b63512c22a61c9f`
- Approval: Aidan Ahern, 2026-10-20, 10:38 PM ET, Grok Bot chat.

## Precedence

1. E1: E1 REPLICATED (10/10 CAND seeds with A-FIT on TEST, A-LEARN, and integrity).
2. Invalid seeds: 0/10.
3. Success count: 9/10 seeds passed (directional 9/10, materiality 10/10; eligibility failures 0/10).

The deciding step is `success`. The success count is applied to the label.

Seeds that miss M are below the declared materiality threshold.

## Verdict

**Label:** GRADED JOINT RECURRENT REVERSION EXCEEDS MATCHED RANDOM PERTURBATION (PREFIX FUNCTION): REPLICATED

**Claim:**

In W2, interpolation of the complete hidden-to-hidden matrix toward its initialization during updates 5–8, with trained input weights, biases and a fresh readout held fixed, increased oracle-referenced prefix-function loss over the predeclared dose grid. In at least eight of ten fresh seeds, the trapezoidal excess exceeded that of every one of 32 block-norm-matched random paths and reached at least one quarter of the paired prefix-loss advantage over F-INIT. The intact trained cores also outperformed the prefix-blind reference. This supports a bounded causal contribution of the trained hidden-to-hidden parameters to accurate prefix-dependent prediction under the specified intervention and fixed surrounding computation. It does not establish monotonicity, selectivity over continuation processing, localized content, necessity, or a uniquely identified mechanism.

## Transfer replication

TRANSFER SHOWN (10/10).

Because eligibility includes a per-seed transfer pass, a primary REPLICATED label implies at least 8/10 transfer passes.

## Secondary (block-wise)

Secondary results are correlated with the primary and with each other. They are not independent replications. They do not substitute for the primary.

- Secondary (block-wise): GRADED JOINT REVERSION CRITERION NOT MET 0/10 seeds passed (directional 7/10, materiality 0/10; eligibility failures 0/10).
- Secondary (block-wise): GRADED JOINT REVERSION CRITERION NOT MET 0/10 seeds passed (directional 5/10, materiality 0/10; eligibility failures 0/10).
- Secondary (block-wise): GRADED JOINT REVERSION CRITERION NOT MET 5/10 seeds passed (directional 7/10, materiality 8/10; eligibility failures 0/10).

## Per-seed primary

| seed | valid | E1 | transfer | L_prefix(F-TRAINED) | B_prefix | B_prefix/PD | C_prefix | C_prefix/PD | AUC_REV | max random AUC | D | M | eligible | joint |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 200 | true | true | true | 0.00070378581 | 0.013362511 | 0.9655955 | 0.013134836 | 0.94914336 | 0.0051487194 | 0.0072314631 | false | true | true | false |
| 201 | true | true | true | 0.0013671183 | 0.013893334 | 1.0039536 | 0.012471504 | 0.90120994 | 0.0039252812 | 0.0032816682 | true | true | true | true |
| 202 | true | true | true | 0.00086224176 | 0.012812005 | 0.92581507 | 0.01297638 | 0.93769309 | 0.0047287814 | 0.0046592216 | true | true | true | true |
| 203 | true | true | true | 0.00090199693 | 0.012752043 | 0.92148214 | 0.012936625 | 0.93482032 | 0.0056139301 | 0.0036530939 | true | true | true | true |
| 204 | true | true | true | 0.00090354057 | 0.013624973 | 0.98456135 | 0.012935082 | 0.93470878 | 0.0059935246 | 0.0050995308 | true | true | true | true |
| 205 | true | true | true | 0.00096186946 | 0.013230086 | 0.95602622 | 0.012876753 | 0.93049384 | 0.0062433453 | 0.0038110522 | true | true | true | true |
| 206 | true | true | true | 0.00055303544 | 0.01442539 | 1.0424008 | 0.013285587 | 0.96003681 | 0.004681303 | 0.0043306018 | true | true | true | true |
| 207 | true | true | true | 0.00070829758 | 0.013065696 | 0.94414714 | 0.013130325 | 0.94881733 | 0.0051768103 | 0.0038656392 | true | true | true | true |
| 208 | true | true | true | 0.00088652447 | 0.012432634 | 0.89840113 | 0.012952098 | 0.93593839 | 0.005168081 | 0.0048555871 | true | true | true | true |
| 209 | true | true | true | 0.00067298274 | 0.014052229 | 1.0154356 | 0.013165639 | 0.95136924 | 0.0058764732 | 0.0055265693 | true | true | true | true |

## Per-seed secondary

| seed | block | AUC_REV | max random AUC | D | M | eligible | joint |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 200 | r | 0.0004549638 | 0.00020481968 | true | false | true | false |
| 200 | z | 0.00043647873 | 0.00037644333 | true | false | true | false |
| 200 | n | 0.0046781073 | 0.0060230078 | false | true | true | false |
| 201 | r | 0.00012447812 | 0.00024348152 | false | false | true | false |
| 201 | z | 0.00045675663 | 0.00044676498 | true | false | true | false |
| 201 | n | 0.0033661578 | 0.0028533386 | true | false | true | false |
| 202 | r | 0.00029747354 | 0.00021533302 | true | false | true | false |
| 202 | z | 0.00061293423 | 0.00036302398 | true | false | true | false |
| 202 | n | 0.0038169881 | 0.0036899904 | true | true | true | true |
| 203 | r | 0.00056952385 | 0.00030108166 | true | false | true | false |
| 203 | z | 0.00013664396 | 0.00063253802 | false | false | true | false |
| 203 | n | 0.0046160904 | 0.0036935323 | true | true | true | true |
| 204 | r | 0.00030139441 | 0.00014505874 | true | false | true | false |
| 204 | z | 0.00019276606 | 0.0004353096 | false | false | true | false |
| 204 | n | 0.0054560499 | 0.0043314119 | true | true | true | true |
| 205 | r | 0.00053956292 | 0.00033590713 | true | false | true | false |
| 205 | z | 0.00026797771 | 0.0002954544 | false | false | true | false |
| 205 | n | 0.0054860678 | 0.0031713537 | true | true | true | true |
| 206 | r | 0.0004136542 | 0.00017114974 | true | false | true | false |
| 206 | z | 0.00055764463 | 0.00033988595 | true | false | true | false |
| 206 | n | 0.0034013512 | 0.0032573917 | true | false | true | false |
| 207 | r | 0.00014398273 | 6.9298779e-05 | true | false | true | false |
| 207 | z | 0.00030203441 | 0.00042235551 | false | false | true | false |
| 207 | n | 0.0047219928 | 0.0049551002 | false | true | true | false |
| 208 | r | 0.00012584338 | 0.00022113988 | false | false | true | false |
| 208 | z | 0.00048286405 | 0.00041473295 | true | false | true | false |
| 208 | n | 0.0043226274 | 0.0045804631 | false | true | true | false |
| 209 | r | 0.00022570725 | 0.00028205063 | false | false | true | false |
| 209 | z | 0.00026326804 | 0.00035576745 | false | false | true | false |
| 209 | n | 0.0052808093 | 0.0046186772 | true | true | true | true |

## Descriptive L_cont, XOR, and E_total

L_cont, the XOR component, and E_total are descriptive. They do not gate the label. Vector success does not establish an XOR-specific effect.

Basic intervention dependence is the measured forecast change and the measured prefix-function loss change under the specified weight changes.

| seed | L_cont AUC | L_prefix XOR AUC | intact TEST E_XOR | endpoint TEST E_XOR | endpoint ΔE_total | endpoint ΔL_prefix | saturation | nondecreasing steps | max abs forecast change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 200 | 0.0156157 | 0.0036467012 | 0.00061173419 | 0.029184048 | 0.063084652 | 0.010037129 | 0.54477973 | 5 | 0.33793972 |
| 201 | 0.010668263 | 0.0025818901 | 0.0010543267 | 0.03386876 | 0.052695828 | 0.0087392295 | 0.42727389 | 5 | 0.35884859 |
| 202 | 0.010576921 | 0.003260648 | 0.00065777487 | 0.023856251 | 0.0475226 | 0.010181623 | 0.45785036 | 5 | 0.29497556 |
| 203 | 0.023609677 | 0.0040363939 | 0.00092902728 | 0.079820458 | 0.13044925 | 0.011457594 | 0.50436943 | 5 | 0.50997889 |
| 204 | 0.017325357 | 0.004282823 | 0.00087260053 | 0.035738467 | 0.07980998 | 0.01192876 | 0.5305401 | 5 | 0.36454972 |
| 205 | 0.011926092 | 0.0044282915 | 0.0013731029 | 0.030520028 | 0.056641428 | 0.011782958 | 0.57667691 | 5 | 0.33158797 |
| 206 | 0.014307474 | 0.0031830566 | 0.00050210185 | 0.040809285 | 0.067352091 | 0.0097951166 | 0.48754473 | 5 | 0.3871044 |
| 207 | 0.013966319 | 0.0036036943 | 0.00081845094 | 0.025713387 | 0.051514649 | 0.01094648 | 0.47426957 | 5 | 0.3675917 |
| 208 | 0.015800044 | 0.0035925928 | 0.00055307202 | 0.03558912 | 0.064449561 | 0.010493499 | 0.50748608 | 5 | 0.45131424 |
| 209 | 0.017743389 | 0.0041231807 | 0.00075213397 | 0.036454617 | 0.076851806 | 0.012291779 | 0.48335813 | 5 | 0.34725484 |

## Development history

Phase A (seeds 100–109) is development-only and is not confirmatory. It is not pooled with seeds 200–209 and it is not support for the claim above. The confirmatory criterion was frozen before any phase A result existed. The phase A files are in `graded_reversion_phaseA_exploratory`.
