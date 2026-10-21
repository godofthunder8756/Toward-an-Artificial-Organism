# scarcity_v2 C3 certificate results

Analytic certificate of pressure and representability on W2′. Exact enumeration and closed forms only. The claim ceiling is the protocol §14 statement.

## Family verdict

| Role | Verdict |
| --- | --- |
| SEL | ADMIT(SEL) |
| ACC | REJECT-NARROW(ACC) |
| UPK | ADMIT(UPK) |
| UPK_cue | ADMIT(UPK_cue) |
| ROUTE | ADMIT(ROUTE) |
| ADAPT | VALUE-ONLY |

UPK_cue is the cue-attributed sub-claim. ADAPT is value-only and has no admission bins. Stage B was run because stage-A roles reach CERT-POS.

**SEL.** controls pass and each bin has a CERT-POS cell with a ROBUST or PERMITTED optimum

**ACC.** §7.3 replay record: the first storage bin is only K=1 and K=2, both zero, while a later bin is CERT-POS. Preserved even where the positive cells are SIG-UNDEFINED, which the general signature rule would call REJECT-SIG.

**UPK.** controls pass and each bin has a CERT-POS cell with a ROBUST or PERMITTED optimum

**UPK_cue.** controls pass and each bin has a CERT-POS cell with a ROBUST or PERMITTED optimum

**ROUTE.** controls pass and each bin has a CERT-POS cell with a ROBUST or PERMITTED optimum

**ADAPT.** ADAPT has no response property and no admission bins. Controls are CERT-ZERO. Experimental cells are reported individually.

## Self-tests

Passed 46, failed 0. Failed quantities: none.

| Check | Quantity | Result | Detail |
| --- | --- | --- | --- |
| K_suff=16 counts | UPK | PASS | I,Q=(16, 16) |
| K_suff=26 counts | UPK | PASS | I,Q=(24, 26) |
| fixed B_up=1 Q | UPK | PASS | Q=18 |
| UPK B_up=1 ample | UPK | PASS | 5/96 |
| UPK B_up=2 ample | UPK | PASS | gap=5/192 n=2304 |
| withdrawal -3/32 | UPK | PASS | -3/32 |
| withdrawal -1/32 | UPK | PASS | -1/32 |
| graded UPK 33/4096 | UPK | PASS | 33/4096 |
| UPK-Z4 | UPK | PASS | CERT-ZERO |
| UPK-C0 below K_suff | UPK | PASS | UNRESOLVED |
| zero-ADAPT values | ADAPT | PASS | known=31/32 iid=119/128 hist=119/128 |
| zero-ADAPT capacity | ADAPT | PASS | (1, 24, 26) |
| B_up=2 matches omni | ADAPT | PASS | 63/64 |
| replay ACC K=1 v=1/3 r=5/8 | ACC | PASS | gap=0 sig=not-required |
| SEL-Z K=1 r=5/8 | SEL | PASS | 0 |
| replay ACC K=1 v=1/3 r=3/4 | ACC | PASS | gap=0 sig=not-required |
| SEL-Z K=1 r=3/4 | SEL | PASS | 0 |
| replay ACC K=1 v=3/4 r=5/8 | ACC | PASS | gap=0 sig=not-required |
| replay ACC K=1 v=3/4 r=3/4 | ACC | PASS | gap=0 sig=not-required |
| replay ACC K=2 v=1/3 r=5/8 | ACC | PASS | gap=0 sig=not-required |
| SEL-Z K=2 r=5/8 | SEL | PASS | 0 |
| replay ACC K=2 v=1/3 r=3/4 | ACC | PASS | gap=0 sig=not-required |
| SEL-Z K=2 r=3/4 | SEL | PASS | 0 |
| replay ACC K=2 v=3/4 r=5/8 | ACC | PASS | gap=0 sig=not-required |
| replay ACC K=2 v=3/4 r=3/4 | ACC | PASS | gap=0 sig=not-required |
| replay ACC K=3 v=1/3 r=5/8 | ACC | PASS | gap=1/48 sig=SIG-UNDEFINED |
| SEL-Z K=3 r=5/8 | SEL | PASS | 0 |
| replay ACC K=3 v=1/3 r=3/4 | ACC | PASS | gap=1/24 sig=SIG-UNDEFINED |
| SEL-Z K=3 r=3/4 | SEL | PASS | 0 |
| replay ACC K=3 v=3/4 r=3/4 | ACC | PASS | gap=1/192 sig=SIG-UNDEFINED |
| replay ACC K=6 v=1/3 r=5/8 | ACC | PASS | gap=1/48 sig=SIG-UNDEFINED |
| SEL-Z K=6 r=5/8 | SEL | PASS | 0 |
| replay ACC K=6 v=1/3 r=3/4 | ACC | PASS | gap=1/24 sig=SIG-UNDEFINED |
| SEL-Z K=6 r=3/4 | SEL | PASS | 0 |
| ACC_suff clean a=None r=3/4 | ACC | PASS | 0 |
| ACC_suff graded a=3/4 r=3/4 | ACC | PASS | 3/32 |
| ACC_suff graded a=3/4 r=5/8 | ACC | PASS | 3/64 |
| ACC_suff graded a=5/6 r=3/4 | ACC | PASS | 5/72 |
| ACC_suff graded a=5/6 r=5/8 | ACC | PASS | 5/144 |
| ACC_suff graded a=3/5 r=3/4 | ACC | PASS | 0 |
| K=1 degenerate | SEL | PASS | DEGENERATE |
| NULL | SEL | PASS | SEL=0 ACC=0 |
| ROUTE control L=1 v=3/4 | ROUTE | PASS | 0 |
| ROUTE control L=2 v=1/3 | ROUTE | PASS | 0 |
| ROUTE control L=8 v=3/4 | ROUTE | PASS | 0 |
| ROUTE L=2 lower bound | ROUTE | PASS | 7/8 |

## Quantity outcomes

### SEL and ACC

Storage-attributed ACC uses clean unpaid cells only. Graded ACC is descriptive. K = 1 zeros are DEGENERATE and count as zero for breadth.

| Cell | SEL | signature | ACC | signature | full optima | orbits | full CPU ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| unpaid/clean/a=-/r=5/8/v=1/3/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=2 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 7 | 4 | 0 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=3 | CERT-ZERO 0 | not-required | CERT-POS 1/48 | SIG-UNDEFINED | 12 | 6 | 0 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=4 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 9 | 6 | 1 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=6 | CERT-ZERO 0 | not-required | CERT-POS 1/48 | SIG-UNDEFINED | 42 | 12 | 5 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=8 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 9 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=12 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3876 | 627 | 41 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=16 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 75582 | None | 106 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=18 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 92378 | None | 115 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=24 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 969 | 180 | 2 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=26 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 19 | 7 | 0 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=27 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=32 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=48 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=64 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=96 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=1/3/K=125 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=2 | CERT-POS 1/8 | ROBUST | CERT-ZERO 0 | not-required | 4 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=3 | CERT-POS 3/32 | ROBUST | CERT-ZERO 0 | not-required | 32 | 4 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=4 | CERT-POS 1/16 | ROBUST | CERT-ZERO 0 | not-required | 8 | 4 | 1 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=6 | CERT-POS 1/32 | ROBUST | CERT-ZERO 0 | not-required | 28 | 7 | 14 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=8 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 44 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=12 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3876 | 627 | 197 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=16 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 75582 | None | 279 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=18 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 92378 | None | 187 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=24 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 969 | 180 | 2 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=26 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 19 | 7 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=27 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=32 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=48 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=64 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=96 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=5/8/v=3/4/K=125 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=2 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3 | 3 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=3 | CERT-ZERO 0 | not-required | CERT-POS 1/24 | SIG-UNDEFINED | 12 | 6 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=4 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 9 | 6 | 1 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=6 | CERT-ZERO 0 | not-required | CERT-POS 1/24 | SIG-UNDEFINED | 42 | 12 | 6 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=8 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 13 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=12 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3876 | 627 | 37 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=16 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 75582 | None | 103 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=18 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 92378 | None | 113 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=24 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 969 | 180 | 2 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=26 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 19 | 7 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=27 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=32 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=48 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=64 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=96 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=1/3/K=125 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=2 | CERT-POS 1/24 | ROBUST | CERT-ZERO 0 | not-required | 4 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=3 | CERT-POS 7/192 | ROBUST | CERT-POS 1/192 | SIG-UNDEFINED | 12 | 3 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=4 | CERT-POS 1/48 | ROBUST | CERT-ZERO 0 | not-required | 8 | 4 | 1 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=6 | CERT-POS 1/96 | ROBUST | CERT-ZERO 0 | not-required | 142 | 28 | 13 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=8 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 32 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=12 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3876 | 627 | 176 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=16 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 75582 | None | 279 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=18 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 92378 | None | 190 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=24 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 969 | 180 | 2 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=26 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 19 | 7 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=27 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=32 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=48 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=64 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=96 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/clean/a=-/r=3/4/v=3/4/K=125 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=2 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3 | 3 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=3 | CERT-ZERO 0 | not-required | CERT-POS 29/1536 | SIG-UNDEFINED | 12 | 6 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=4 | CERT-ZERO 0 | not-required | CERT-POS 23/4096 | SIG-UNDEFINED | 48 | 6 | 3 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=6 | CERT-ZERO 0 | not-required | CERT-POS 217/12288 | UNRESOLVED | 6 | 3 | 22 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=8 | CERT-ZERO 0 | not-required | CERT-POS 67/6144 | SIG-UNDEFINED | 6 | 3 | 121 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=12 | CERT-ZERO 0 | not-required | CERT-POS 363/16384 | UNRESOLVED | 8 | 1 | 979 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=16 | CERT-ZERO 0 | not-required | CERT-POS 493/16384 | UNRESOLVED | 12 | 3 | 1669 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=18 | CERT-ZERO 0 | not-required | CERT-POS 543/16384 | UNRESOLVED | 220 | 35 | 1101 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=24 | CERT-ZERO 0 | not-required | CERT-POS 693/16384 | ROBUST | 220 | 35 | 7 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=26 | CERT-ZERO 0 | not-required | CERT-POS 743/16384 | ROBUST | 12 | 3 | 1 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=27 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=32 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=48 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=64 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=96 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=1/3/K=125 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=2 | CERT-POS 227/6144 | ROBUST | CERT-ZERO 0 | not-required | 4 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=3 | CERT-POS 4693/131072 | ROBUST | CERT-POS 2133/131072 | SIG-UNDEFINED | 8 | 1 | 1 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=4 | CERT-POS 365/12288 | ROBUST | CERT-POS 23/1536 | SIG-UNDEFINED | 6 | 3 | 3 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=6 | CERT-POS 69/4096 | ROBUST | CERT-POS 299/12288 | UNRESOLVED | 3 | 3 | 33 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=8 | CERT-POS 3979/262144 | ROBUST | CERT-POS 20513/786432 | SIG-UNDEFINED | 24 | 3 | 199 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=12 | CERT-POS 9577/786432 | ROBUST | CERT-POS 27001/786432 | UNRESOLVED | 24 | 3 | 1304 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=16 | CERT-POS 1105/131072 | ROBUST | CERT-POS 5049/131072 | UNRESOLVED | 12 | 3 | 1842 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=18 | CERT-POS 465/65536 | ROBUST | CERT-POS 2637/65536 | UNRESOLVED | 6 | 3 | 1089 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=24 | CERT-POS 165/65536 | ROBUST | CERT-POS 2937/65536 | ROBUST | 20 | 7 | 11 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=26 | CERT-POS 55/65536 | ROBUST | CERT-POS 3027/65536 | ROBUST | 6 | 3 | 1 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=27 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=32 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=48 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=64 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=96 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=5/8/v=3/4/K=125 | CERT-ZERO 0 | not-required | CERT-POS 3/64 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=2 | CERT-ZERO 0 | not-required | CERT-POS 1/64 | ROBUST | 6 | 3 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=3 | CERT-ZERO 0 | not-required | CERT-POS 1/32 | ROBUST | 3 | 3 | 1 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=4 | CERT-ZERO 0 | not-required | CERT-POS 311/8192 | ROBUST | 12 | 3 | 2 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=6 | CERT-ZERO 0 | not-required | CERT-POS 421/8192 | ROBUST | 12 | 3 | 11 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=8 | CERT-ZERO 0 | not-required | CERT-POS 247/4096 | ROBUST | 24 | 12 | 38 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=12 | CERT-ZERO 0 | not-required | CERT-POS 563/8192 | UNRESOLVED | 108 | 21 | 150 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=16 | CERT-ZERO 0 | not-required | CERT-POS 623/8192 | UNRESOLVED | 212 | 34 | 135 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=18 | CERT-ZERO 0 | not-required | CERT-POS 653/8192 | UNRESOLVED | 12 | 3 | 79 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=24 | CERT-ZERO 0 | not-required | CERT-POS 1461/16384 | UNRESOLVED | 56 | 7 | 2 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=26 | CERT-ZERO 0 | not-required | CERT-POS 1511/16384 | ROBUST | 8 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=27 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=32 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=48 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=64 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=96 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=1/3/K=125 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=2 | CERT-POS 31/12288 | ROBUST | CERT-POS 223/12288 | SIG-UNDEFINED | 12 | 3 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=3 | CERT-POS 31/6144 | ROBUST | CERT-POS 223/6144 | SIG-UNDEFINED | 6 | 3 | 1 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=4 | CERT-POS 415/24576 | ROBUST | CERT-POS 337/6144 | SIG-UNDEFINED | 6 | 3 | 2 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=6 | CERT-POS 191/8192 | ROBUST | CERT-POS 153/2048 | UNRESOLVED | 1 | 1 | 14 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=8 | CERT-POS 1147/65536 | ROBUST | CERT-POS 5099/65536 | ROBUST | 12 | 3 | 73 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=12 | CERT-POS 477/32768 | ROBUST | CERT-POS 2729/32768 | ROBUST | 12 | 6 | 560 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=16 | CERT-POS 725/65536 | ROBUST | CERT-POS 5709/65536 | UNRESOLVED | 44 | 10 | 483 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=18 | CERT-POS 575/65536 | ROBUST | CERT-POS 5799/65536 | UNRESOLVED | 12 | 3 | 257 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=24 | CERT-POS 375/131072 | ROBUST | CERT-POS 12063/131072 | ROBUST | 56 | 7 | 3 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=26 | CERT-POS 125/131072 | ROBUST | CERT-POS 12213/131072 | ROBUST | 8 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=27 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=32 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=48 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=64 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=96 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/4/r=3/4/v=3/4/K=125 | CERT-ZERO 0 | not-required | CERT-POS 3/32 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=2 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3 | 3 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=3 | CERT-ZERO 0 | not-required | CERT-POS 71/3888 | SIG-UNDEFINED | 12 | 6 | 1 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=4 | CERT-ZERO 0 | not-required | CERT-POS 73/139968 | UNRESOLVED | 24 | 3 | 2 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=6 | CERT-ZERO 0 | not-required | CERT-POS 287/17496 | UNRESOLVED | 6 | 3 | 18 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=8 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 69 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=12 | CERT-ZERO 0 | not-required | CERT-POS 2695/186624 | UNRESOLVED | 144 | 21 | 494 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=16 | CERT-ZERO 0 | not-required | CERT-POS 11465/559872 | UNRESOLVED | 4512 | 615 | 1146 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=18 | CERT-ZERO 0 | not-required | CERT-POS 4385/186624 | UNRESOLVED | 1320 | 195 | 795 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=24 | CERT-ZERO 0 | not-required | CERT-POS 245/7776 | UNRESOLVED | 15 | 6 | 6 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=26 | CERT-ZERO 0 | not-required | CERT-POS 4735/139968 | ROBUST | 1 | 1 | 1 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=27 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=32 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=48 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=64 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=96 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=1/3/K=125 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=2 | CERT-POS 547/7776 | ROBUST | CERT-ZERO 0 | not-required | 4 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=3 | CERT-POS 25289/497664 | ROBUST | CERT-POS 257/55296 | SIG-UNDEFINED | 8 | 1 | 1 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=4 | CERT-POS 4997/139968 | ROBUST | CERT-ZERO 0 | not-required | 2 | 1 | 3 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=6 | CERT-POS 46957/4478976 | ROBUST | CERT-POS 13103/1492992 | SIG-UNDEFINED | 24 | 3 | 34 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=8 | CERT-POS 10465/995328 | ROBUST | CERT-POS 10465/995328 | SIG-UNDEFINED | 24 | 3 | 202 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=12 | CERT-POS 3695/559872 | ROBUST | CERT-POS 2945/139968 | UNRESOLVED | 3 | 3 | 1166 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=16 | CERT-POS 15355/2239488 | ROBUST | CERT-POS 20405/746496 | UNRESOLVED | 84 | 15 | 1271 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=18 | CERT-POS 26635/4478976 | ROBUST | CERT-POS 131875/4478976 | UNRESOLVED | 24 | 6 | 720 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=24 | CERT-POS 125/62208 | ROBUST | CERT-POS 695/20736 | ROBUST | 15 | 6 | 6 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=26 | CERT-POS 625/1119744 | ROBUST | CERT-POS 12835/373248 | ROBUST | 1 | 1 | 1 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=27 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=32 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=48 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=64 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=96 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=5/8/v=3/4/K=125 | CERT-ZERO 0 | not-required | CERT-POS 5/144 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=2 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3 | 3 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=3 | CERT-ZERO 0 | not-required | CERT-POS 47/1944 | SIG-UNDEFINED | 12 | 6 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=4 | CERT-ZERO 0 | not-required | CERT-POS 197/15552 | SIG-UNDEFINED | 48 | 6 | 2 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=6 | CERT-ZERO 0 | not-required | CERT-POS 685/17496 | UNRESOLVED | 3 | 3 | 16 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=8 | CERT-ZERO 0 | not-required | CERT-POS 1303/69984 | SIG-UNDEFINED | 6 | 3 | 89 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=12 | CERT-ZERO 0 | not-required | CERT-POS 2995/93312 | ROBUST | 12 | 3 | 773 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=16 | CERT-ZERO 0 | not-required | CERT-POS 12235/279936 | ROBUST | 36 | 9 | 713 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=18 | CERT-ZERO 0 | not-required | CERT-POS 2305/46656 | ROBUST | 6 | 3 | 334 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=24 | CERT-ZERO 0 | not-required | CERT-POS 2965/46656 | ROBUST | 20 | 7 | 2 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=26 | CERT-ZERO 0 | not-required | CERT-POS 4735/69984 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=27 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=32 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=48 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=64 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=96 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=1/3/K=125 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=2 | CERT-POS 1465/186624 | ROBUST | CERT-POS 1465/186624 | SIG-UNDEFINED | 8 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=3 | CERT-POS 13465/559872 | ROBUST | CERT-POS 19873/559872 | SIG-UNDEFINED | 24 | 3 | 1 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=4 | CERT-POS 1511/46656 | ROBUST | CERT-POS 455/11664 | SIG-UNDEFINED | 6 | 3 | 2 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=6 | CERT-POS 503/17496 | ROBUST | CERT-POS 793/15552 | UNRESOLVED | 3 | 3 | 23 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=8 | CERT-POS 419/15552 | ROBUST | CERT-POS 6377/139968 | ROBUST | 12 | 3 | 140 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=12 | CERT-POS 99397/4478976 | ROBUST | CERT-POS 243157/4478976 | UNRESOLVED | 24 | 3 | 1142 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=16 | CERT-POS 11615/746496 | ROBUST | CERT-POS 132725/2239488 | ROBUST | 12 | 3 | 1411 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=18 | CERT-POS 4505/373248 | ROBUST | CERT-POS 22945/373248 | ROBUST | 6 | 3 | 719 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=24 | CERT-POS 1325/373248 | ROBUST | CERT-POS 25045/373248 | ROBUST | 20 | 7 | 4 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=26 | CERT-POS 625/559872 | ROBUST | CERT-POS 12835/186624 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=27 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=32 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=48 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=64 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=96 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=5/6/r=3/4/v=3/4/K=125 | CERT-ZERO 0 | not-required | CERT-POS 5/72 | ROBUST | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=2 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 26 | 7 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=3 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 325 | 61 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=4 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 2600 | 382 | 1 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=6 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 65780 | None | 10 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=8 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 657800 | None | 109 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=12 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 7726160 | None | 1590 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=16 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 7726160 | None | 2297 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=18 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3124550 | None | 1144 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=24 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 2600 | 382 | 5 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=26 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 26 | 7 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=27 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=32 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=48 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=64 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=96 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=1/3/K=125 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=1 | DEGENERATE 0 | not-required | DEGENERATE 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=2 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 26 | 7 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=3 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 325 | 61 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=4 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 2600 | 382 | 1 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=6 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 65780 | None | 10 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=8 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 657800 | None | 104 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=12 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 7726160 | None | 1471 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=16 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 7726160 | None | 2266 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=18 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 3124550 | None | 1137 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=24 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 2600 | 382 | 4 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=26 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 26 | 7 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=27 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=32 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=48 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=64 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=96 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |
| unpaid/graded/a=3/5/r=3/4/v=3/4/K=125 | CERT-ZERO 0 | not-required | CERT-ZERO 0 | not-required | 1 | 1 | 0 |

### UPK

δ = 1/4 rows are report-only and were not used in the verdict. Graded UPK is the single §5.4 cell, also report-only.

Graded ample report: UPK = 33/4096, UPK_cue = 0, UPK_ev = 33/4096, V_full = 3361/4096.

| Cell | decision | UPK | signature | optima | orbits | UPK_cue | UPK_ev |
| --- | --- | --- | --- | --- | --- | --- | --- |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=1 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=2 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=3 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=4 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=6 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=8 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=5/8/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=1 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=2 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=3 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=4 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=6 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=8 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=1/3/r=3/4/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=1 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=2 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=3 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=4 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=6 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=8 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=5/8/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=1 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=2 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=3 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=4 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=6 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=8 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/2/v=3/4/r=3/4/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=1 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=2 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=3 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=4 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=6 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=8 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=12 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=16 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=1 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=2 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=3 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=4 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=6 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=8 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=12 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=16 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=1 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=2 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=3 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=4 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=6 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=8 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=12 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=16 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=18 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=24 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=26 | True | CERT-POS 5/64 | ROBUST | 1 | 1 | CERT-POS 5/64 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=27 | True | CERT-POS 5/64 | ROBUST | 1 | 1 | CERT-POS 5/64 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=32 | True | CERT-POS 5/64 | ROBUST | 1 | 1 | CERT-POS 5/64 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=48 | True | CERT-POS 5/64 | ROBUST | 1 | 1 | CERT-POS 5/64 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=64 | True | CERT-POS 5/64 | ROBUST | 1 | 1 | CERT-POS 5/64 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=96 | True | CERT-POS 5/64 | ROBUST | 1 | 1 | CERT-POS 5/64 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=125 | True | CERT-POS 5/64 | ROBUST | 1 | 1 | CERT-POS 5/64 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=1 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=2 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=3 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=4 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=6 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=8 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=12 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=16 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=18 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=24 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=26 | True | CERT-POS 5/96 | ROBUST | 1 | 1 | CERT-POS 5/96 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=27 | True | CERT-POS 5/96 | ROBUST | 1 | 1 | CERT-POS 5/96 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=32 | True | CERT-POS 5/96 | ROBUST | 1 | 1 | CERT-POS 5/96 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=48 | True | CERT-POS 5/96 | ROBUST | 1 | 1 | CERT-POS 5/96 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=64 | True | CERT-POS 5/96 | ROBUST | 1 | 1 | CERT-POS 5/96 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=96 | True | CERT-POS 5/96 | ROBUST | 1 | 1 | CERT-POS 5/96 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=125 | True | CERT-POS 5/96 | ROBUST | 1 | 1 | CERT-POS 5/96 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=1 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=2 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=3 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=4 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=6 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=8 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=1 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=2 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=3 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=4 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=6 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=8 | True | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=1 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=2 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=3 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=4 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=6 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=8 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=12 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=16 | True | CERT-POS 5/128 | ROBUST | 2304 | 366 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=18 | True | CERT-POS 5/128 | ROBUST | 2259200 | 283774 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=24 | True | CERT-POS 5/128 | ROBUST | 16777216 | 2100736 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=26 | True | CERT-POS 5/128 | ROBUST | 16777216 | 2100736 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=27 | True | CERT-POS 5/128 | ROBUST | 16777216 | 2100736 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=32 | True | CERT-POS 5/128 | ROBUST | 16777216 | 2100736 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=48 | True | CERT-POS 5/128 | ROBUST | 16777216 | 2100736 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=64 | True | CERT-POS 5/128 | ROBUST | 16777216 | 2100736 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=96 | True | CERT-POS 5/128 | ROBUST | 16777216 | 2100736 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=125 | True | CERT-POS 5/128 | ROBUST | 16777216 | 2100736 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=1 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=2 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=3 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=4 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=6 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=8 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=12 | True | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=16 | True | CERT-POS 5/192 | ROBUST | 2304 | 366 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=18 | True | CERT-POS 5/192 | ROBUST | 2259200 | 283774 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=24 | True | CERT-POS 5/192 | ROBUST | 16777216 | 2100736 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=26 | True | CERT-POS 5/192 | ROBUST | 16777216 | 2100736 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=27 | True | CERT-POS 5/192 | ROBUST | 16777216 | 2100736 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=32 | True | CERT-POS 5/192 | ROBUST | 16777216 | 2100736 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=48 | True | CERT-POS 5/192 | ROBUST | 16777216 | 2100736 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=64 | True | CERT-POS 5/192 | ROBUST | 16777216 | 2100736 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=96 | True | CERT-POS 5/192 | ROBUST | 16777216 | 2100736 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=125 | True | CERT-POS 5/192 | ROBUST | 16777216 | 2100736 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=1 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=2 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=3 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=4 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=6 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=8 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=5/8/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=1 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=2 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=3 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=4 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=6 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=8 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=1/3/r=3/4/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=1 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=2 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=3 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=4 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=6 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=8 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=5/8/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=1 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=2 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=3 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=4 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=6 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=8 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=12 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=16 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=18 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=24 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=26 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=27 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=32 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=48 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=64 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=96 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/2/v=3/4/r=3/4/K=125 | True | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=1 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=2 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=3 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=4 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=6 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=8 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=5/8/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=1 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=2 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=3 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=4 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=6 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=8 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=1/3/r=3/4/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=1 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=2 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=3 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=4 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=6 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=8 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=5/8/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=1 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=2 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=3 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=4 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=6 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=8 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=0/d=1/4/v=3/4/r=3/4/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=1 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=2 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=3 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=4 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=6 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=8 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=12 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=16 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=1 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=2 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=3 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=4 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=6 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=8 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=12 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=16 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=1 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=2 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=3 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=4 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=6 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=8 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=12 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=16 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=18 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=24 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=26 | False | CERT-POS 5/128 | ROBUST | 1 | 1 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=27 | False | CERT-POS 5/128 | ROBUST | 1 | 1 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=32 | False | CERT-POS 5/128 | ROBUST | 1 | 1 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=48 | False | CERT-POS 5/128 | ROBUST | 1 | 1 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=64 | False | CERT-POS 5/128 | ROBUST | 1 | 1 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=96 | False | CERT-POS 5/128 | ROBUST | 1 | 1 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=125 | False | CERT-POS 5/128 | ROBUST | 1 | 1 | CERT-POS 5/128 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=1 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=2 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=3 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=4 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=6 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=8 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=12 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=16 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=18 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=24 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=26 | False | CERT-POS 5/192 | ROBUST | 1 | 1 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=27 | False | CERT-POS 5/192 | ROBUST | 1 | 1 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=32 | False | CERT-POS 5/192 | ROBUST | 1 | 1 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=48 | False | CERT-POS 5/192 | ROBUST | 1 | 1 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=64 | False | CERT-POS 5/192 | ROBUST | 1 | 1 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=96 | False | CERT-POS 5/192 | ROBUST | 1 | 1 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=125 | False | CERT-POS 5/192 | ROBUST | 1 | 1 | CERT-POS 5/192 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=1 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=2 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=3 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=4 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=6 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=8 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=1 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=2 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=3 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=4 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=6 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=8 | False | UNRESOLVED None | UNRESOLVED | None | None | CERT-ZERO 0 | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=1 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=2 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=3 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=4 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=6 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=8 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=12 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=16 | False | CERT-POS 5/256 | ROBUST | 2304 | 366 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=18 | False | CERT-POS 5/256 | ROBUST | 2259200 | 283774 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=24 | False | CERT-POS 5/256 | ROBUST | 16777216 | 2100736 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=26 | False | CERT-POS 5/256 | ROBUST | 16777216 | 2100736 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=27 | False | CERT-POS 5/256 | ROBUST | 16777216 | 2100736 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=32 | False | CERT-POS 5/256 | ROBUST | 16777216 | 2100736 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=48 | False | CERT-POS 5/256 | ROBUST | 16777216 | 2100736 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=64 | False | CERT-POS 5/256 | ROBUST | 16777216 | 2100736 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=96 | False | CERT-POS 5/256 | ROBUST | 16777216 | 2100736 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=125 | False | CERT-POS 5/256 | ROBUST | 16777216 | 2100736 | CERT-POS 5/256 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=1 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=2 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=3 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=4 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=6 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=8 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=12 | False | UNRESOLVED None | UNRESOLVED | None | None | UNRESOLVED None | UNRESOLVED None |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=16 | False | CERT-POS 5/384 | ROBUST | 2304 | 366 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=18 | False | CERT-POS 5/384 | ROBUST | 2259200 | 283774 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=24 | False | CERT-POS 5/384 | ROBUST | 16777216 | 2100736 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=26 | False | CERT-POS 5/384 | ROBUST | 16777216 | 2100736 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=27 | False | CERT-POS 5/384 | ROBUST | 16777216 | 2100736 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=32 | False | CERT-POS 5/384 | ROBUST | 16777216 | 2100736 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=48 | False | CERT-POS 5/384 | ROBUST | 16777216 | 2100736 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=64 | False | CERT-POS 5/384 | ROBUST | 16777216 | 2100736 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=96 | False | CERT-POS 5/384 | ROBUST | 16777216 | 2100736 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=125 | False | CERT-POS 5/384 | ROBUST | 16777216 | 2100736 | CERT-POS 5/384 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=1 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=2 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=3 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=4 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=6 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=8 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=5/8/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=1 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=2 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=3 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=4 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=6 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=8 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=1/3/r=3/4/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=1 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=2 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=3 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=4 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=6 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=8 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=5/8/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=1 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=2 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=3 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=4 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=6 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=8 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=12 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=16 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=18 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=24 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=26 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=27 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=32 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=48 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=64 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=96 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |
| upk/clean/B=3/d=1/4/v=3/4/r=3/4/K=125 | False | CERT-ZERO 0 | not-required | None | None | CERT-ZERO 0 | CERT-ZERO 0 |

### ROUTE

Value is the mean of the two consumers. Optima counts are decoder pairs. L at or above K_dec,base is the constructive zero and was not enumerated.

| Cell | status | gap | signature | decoder-pair optima | CPU ms |
| --- | --- | --- | --- | --- | --- |
| route/clean/a=-/r=5/8/v=1/3/L=1 | CERT-ZERO | 0 | not-required | 1 | 1 |
| route/clean/a=-/r=5/8/v=1/3/L=2 | CERT-ZERO | 0 | not-required | 196 | 52 |
| route/clean/a=-/r=5/8/v=1/3/L=3 | CERT-ZERO | 0 | not-required | 5184 | 1919 |
| route/clean/a=-/r=5/8/v=1/3/L=8 | CERT-ZERO | 0 | not-required | None | 0 |
| route/clean/a=-/r=5/8/v=3/4/L=1 | CERT-ZERO | 0 | not-required | 1 | 2 |
| route/clean/a=-/r=5/8/v=3/4/L=2 | CERT-POS | 1/8 | ROBUST | 64 | 58 |
| route/clean/a=-/r=5/8/v=3/4/L=3 | CERT-POS | 3/32 | ROBUST | 36864 | 2142 |
| route/clean/a=-/r=5/8/v=3/4/L=8 | CERT-ZERO | 0 | not-required | None | 0 |
| route/clean/a=-/r=3/4/v=1/3/L=1 | CERT-ZERO | 0 | not-required | 1 | 1 |
| route/clean/a=-/r=3/4/v=1/3/L=2 | CERT-ZERO | 0 | not-required | 36 | 52 |
| route/clean/a=-/r=3/4/v=1/3/L=3 | CERT-ZERO | 0 | not-required | 5184 | 1933 |
| route/clean/a=-/r=3/4/v=1/3/L=8 | CERT-ZERO | 0 | not-required | None | 0 |
| route/clean/a=-/r=3/4/v=3/4/L=1 | CERT-ZERO | 0 | not-required | 1 | 2 |
| route/clean/a=-/r=3/4/v=3/4/L=2 | CERT-POS | 1/24 | ROBUST | 64 | 58 |
| route/clean/a=-/r=3/4/v=3/4/L=3 | CERT-POS | 7/192 | ROBUST | 5184 | 2072 |
| route/clean/a=-/r=3/4/v=3/4/L=8 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/4/r=5/8/v=1/3/L=1 | CERT-ZERO | 0 | not-required | 1 | 14 |
| route/graded/a=3/4/r=5/8/v=1/3/L=2 | CERT-ZERO | 0 | not-required | 36 | 238 |
| route/graded/a=3/4/r=5/8/v=1/3/L=3 | CERT-ZERO | 0 | not-required | 5184 | 8532 |
| route/graded/a=3/4/r=5/8/v=1/3/L=27 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/4/r=5/8/v=3/4/L=1 | CERT-ZERO | 0 | not-required | 1 | 14 |
| route/graded/a=3/4/r=5/8/v=3/4/L=2 | CERT-POS | 227/6144 | ROBUST | 64 | 205 |
| route/graded/a=3/4/r=5/8/v=3/4/L=3 | CERT-POS | 4693/131072 | ROBUST | 2304 | 7143 |
| route/graded/a=3/4/r=5/8/v=3/4/L=27 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/4/r=3/4/v=1/3/L=1 | CERT-ZERO | 0 | not-required | 1 | 14 |
| route/graded/a=3/4/r=3/4/v=1/3/L=2 | CERT-ZERO | 0 | not-required | 144 | 236 |
| route/graded/a=3/4/r=3/4/v=1/3/L=3 | CERT-ZERO | 0 | not-required | 324 | 8315 |
| route/graded/a=3/4/r=3/4/v=1/3/L=27 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/4/r=3/4/v=3/4/L=1 | CERT-ZERO | 0 | not-required | 1 | 15 |
| route/graded/a=3/4/r=3/4/v=3/4/L=2 | CERT-POS | 31/12288 | ROBUST | 576 | 210 |
| route/graded/a=3/4/r=3/4/v=3/4/L=3 | CERT-POS | 31/6144 | ROBUST | 1296 | 7191 |
| route/graded/a=3/4/r=3/4/v=3/4/L=27 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=5/6/r=5/8/v=1/3/L=1 | CERT-ZERO | 0 | not-required | 1 | 14 |
| route/graded/a=5/6/r=5/8/v=1/3/L=2 | CERT-ZERO | 0 | not-required | 36 | 230 |
| route/graded/a=5/6/r=5/8/v=1/3/L=3 | CERT-ZERO | 0 | not-required | 5184 | 8079 |
| route/graded/a=5/6/r=5/8/v=1/3/L=27 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=5/6/r=5/8/v=3/4/L=1 | CERT-ZERO | 0 | not-required | 1 | 14 |
| route/graded/a=5/6/r=5/8/v=3/4/L=2 | CERT-POS | 547/7776 | ROBUST | 64 | 228 |
| route/graded/a=5/6/r=5/8/v=3/4/L=3 | CERT-POS | 25289/497664 | ROBUST | 2304 | 7907 |
| route/graded/a=5/6/r=5/8/v=3/4/L=27 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=5/6/r=3/4/v=1/3/L=1 | CERT-ZERO | 0 | not-required | 1 | 14 |
| route/graded/a=5/6/r=3/4/v=1/3/L=2 | CERT-ZERO | 0 | not-required | 36 | 227 |
| route/graded/a=5/6/r=3/4/v=1/3/L=3 | CERT-ZERO | 0 | not-required | 5184 | 8083 |
| route/graded/a=5/6/r=3/4/v=1/3/L=27 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=5/6/r=3/4/v=3/4/L=1 | CERT-ZERO | 0 | not-required | 1 | 15 |
| route/graded/a=5/6/r=3/4/v=3/4/L=2 | CERT-POS | 1465/186624 | ROBUST | 256 | 229 |
| route/graded/a=5/6/r=3/4/v=3/4/L=3 | CERT-POS | 13465/559872 | ROBUST | 20736 | 8155 |
| route/graded/a=5/6/r=3/4/v=3/4/L=27 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/5/r=3/4/v=1/3/L=1 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/5/r=3/4/v=1/3/L=2 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/5/r=3/4/v=1/3/L=3 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/5/r=3/4/v=3/4/L=1 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/5/r=3/4/v=3/4/L=2 | CERT-ZERO | 0 | not-required | None | 0 |
| route/graded/a=3/5/r=3/4/v=3/4/L=3 | CERT-ZERO | 0 | not-required | None | 0 |

### ADAPT

No signature. An interval is the correct-bit cue-equivariant lower bound against the regime-known upper bound.

| Cell | status | gap | interval | CPU ms |
| --- | --- | --- | --- | --- |
| adapt/KNOWN-FIXED/H=1/B=1/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=1 | DEGENERATE | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=1 | DEGENERATE | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=1 | DEGENERATE | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=1 | DEGENERATE | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=0/d=1/2/v=3/4/r=3/4/K=1 | DEGENERATE | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=0/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=0/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=0/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=0/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=0/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=1/d=1/2/v=3/4/r=3/4/K=1 | DEGENERATE | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=1/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=1/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=1/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=1/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=1/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=2/d=1/2/v=3/4/r=3/4/K=1 | DEGENERATE | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=2/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=2/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=2/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=2/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=2/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=3/d=1/2/v=3/4/r=3/4/K=1 | DEGENERATE | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=3/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=3/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=3/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=3/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=3/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=0/d=1/2/v=3/4/r=3/4/K=1 | UNRESOLVED | None | None | 0 |
| adapt/SWITCHING/H=2/B=0/d=1/2/v=3/4/r=3/4/K=16 | UNRESOLVED | None | None | 0 |
| adapt/SWITCHING/H=2/B=0/d=1/2/v=3/4/r=3/4/K=26 | UNRESOLVED | None | None | 0 |
| adapt/SWITCHING/H=2/B=0/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=0/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=0/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=1 | UNRESOLVED | None | None | 0 |
| adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=16 | UNRESOLVED | None | None | 0 |
| adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=26 | UNRESOLVED | None | None | 1 |
| adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=48 | UNRESOLVED | None | None | 0 |
| adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=64 | UNRESOLVED | None | ['0', '105/3968'] | 448 |
| adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=125 | UNRESOLVED | None | ['0', '105/3968'] | 0 |
| adapt/SWITCHING/H=2/B=2/d=1/2/v=3/4/r=3/4/K=1 | UNRESOLVED | None | None | 0 |
| adapt/SWITCHING/H=2/B=2/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=2/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=2/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=2/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=2/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=3/d=1/2/v=3/4/r=3/4/K=1 | UNRESOLVED | None | None | 0 |
| adapt/SWITCHING/H=2/B=3/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=3/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=3/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=3/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=3/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=1 | UNRESOLVED | None | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=16 | UNRESOLVED | None | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=26 | UNRESOLVED | None | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=1 | UNRESOLVED | None | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=16 | UNRESOLVED | None | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=26 | UNRESOLVED | None | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=48 | UNRESOLVED | None | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=64 | UNRESOLVED | None | ['0', '5/384'] | 263 |
| adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=125 | UNRESOLVED | None | ['0', '5/384'] | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=1 | UNRESOLVED | None | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=1 | UNRESOLVED | None | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=16 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=48 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=64 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=125 | CERT-ZERO | 0 | None | 0 |
| adapt/KNOWN-FIXED/H=2/B=1/d=0/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/IID-REGIME/H=2/B=1/d=0/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/SWITCHING/H=2/B=1/d=0/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |
| adapt/UNKNOWN-FIXED/H=2/B=1/d=0/v=3/4/r=3/4/K=26 | CERT-ZERO | 0 | None | 0 |

## Unresolved cells

- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=1 UPK: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=1 UPK_ev: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=2 UPK: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=2 UPK_ev: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=3 UPK: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=3 UPK_ev: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=4 UPK: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=4 UPK_ev: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=6 UPK: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=6 UPK_ev: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=8 UPK: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=8 UPK_ev: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=12 UPK: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=12 UPK_ev: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=16 UPK: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=5/8/K=16 UPK_ev: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=1 UPK: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=1 UPK_ev: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=2 UPK: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=2 UPK_ev: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=3 UPK: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=3 UPK_ev: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=4 UPK: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=4 UPK_ev: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=6 UPK: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=6 UPK_ev: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=8 UPK: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=8 UPK_ev: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=12 UPK: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=12 UPK_ev: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=16 UPK: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=1/3/r=3/4/K=16 UPK_ev: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=1 UPK: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=1 UPK_cue: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=1 UPK_ev: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=2 UPK: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=2 UPK_cue: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=2 UPK_ev: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=3 UPK: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=3 UPK_cue: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=3 UPK_ev: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=4 UPK: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=4 UPK_cue: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=4 UPK_ev: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=6 UPK: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=6 UPK_cue: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=6 UPK_ev: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=8 UPK: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=8 UPK_cue: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=8 UPK_ev: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=12 UPK: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=12 UPK_cue: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=12 UPK_ev: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=16 UPK: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=16 UPK_cue: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=16 UPK_ev: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=18 UPK: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=18 UPK_cue: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=18 UPK_ev: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=24 UPK: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=24 UPK_cue: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=5/8/K=24 UPK_ev: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=1 UPK: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=1 UPK_cue: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=1 UPK_ev: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=2 UPK: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=2 UPK_cue: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=2 UPK_ev: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=3 UPK: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=3 UPK_cue: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=3 UPK_ev: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=4 UPK: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=4 UPK_cue: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=4 UPK_ev: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=6 UPK: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=6 UPK_cue: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=6 UPK_ev: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=8 UPK: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=8 UPK_cue: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=8 UPK_ev: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=12 UPK: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=12 UPK_cue: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=12 UPK_ev: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=16 UPK: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=16 UPK_cue: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=16 UPK_ev: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=18 UPK: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=18 UPK_cue: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=18 UPK_ev: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=24 UPK: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=24 UPK_cue: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/2/v=3/4/r=3/4/K=24 UPK_ev: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=1 UPK: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=1 UPK_ev: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=2 UPK: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=2 UPK_ev: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=3 UPK: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=3 UPK_ev: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=4 UPK: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=4 UPK_ev: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=6 UPK: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=6 UPK_ev: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=8 UPK: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=5/8/K=8 UPK_ev: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=1 UPK: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=1 UPK_ev: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=2 UPK: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=2 UPK_ev: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=3 UPK: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=3 UPK_ev: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=4 UPK: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=4 UPK_ev: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=6 UPK: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=6 UPK_ev: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=8 UPK: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=1/3/r=3/4/K=8 UPK_ev: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=1 UPK: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=1 UPK_cue: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=1 UPK_ev: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=2 UPK: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=2 UPK_cue: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=2 UPK_ev: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=3 UPK: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=3 UPK_cue: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=3 UPK_ev: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=4 UPK: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=4 UPK_cue: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=4 UPK_ev: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=6 UPK: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=6 UPK_cue: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=6 UPK_ev: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=8 UPK: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=8 UPK_cue: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=8 UPK_ev: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=12 UPK: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=12 UPK_cue: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=5/8/K=12 UPK_ev: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=1 UPK: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=1 UPK_cue: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=1 UPK_ev: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=2 UPK: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=2 UPK_cue: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=2 UPK_ev: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=3 UPK: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=3 UPK_cue: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=3 UPK_ev: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=4 UPK: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=4 UPK_cue: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=4 UPK_ev: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=6 UPK: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=6 UPK_cue: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=6 UPK_ev: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=8 UPK: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=8 UPK_cue: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=8 UPK_ev: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=12 UPK: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=12 UPK_cue: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/2/v=3/4/r=3/4/K=12 UPK_ev: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=1 UPK: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=1 UPK_ev: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=2 UPK: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=2 UPK_ev: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=3 UPK: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=3 UPK_ev: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=4 UPK: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=4 UPK_ev: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=6 UPK: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=6 UPK_ev: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=8 UPK: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=8 UPK_ev: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=12 UPK: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=12 UPK_ev: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=16 UPK: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=5/8/K=16 UPK_ev: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=1 UPK: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=1 UPK_ev: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=2 UPK: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=2 UPK_ev: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=3 UPK: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=3 UPK_ev: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=4 UPK: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=4 UPK_ev: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=6 UPK: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=6 UPK_ev: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=8 UPK: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=8 UPK_ev: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=12 UPK: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=12 UPK_ev: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=16 UPK: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=1/3/r=3/4/K=16 UPK_ev: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=1 UPK: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=1 UPK_cue: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=1 UPK_ev: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=2 UPK: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=2 UPK_cue: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=2 UPK_ev: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=3 UPK: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=3 UPK_cue: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=3 UPK_ev: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=4 UPK: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=4 UPK_cue: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=4 UPK_ev: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=6 UPK: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=6 UPK_cue: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=6 UPK_ev: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=8 UPK: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=8 UPK_cue: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=8 UPK_ev: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=12 UPK: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=12 UPK_cue: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=12 UPK_ev: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=16 UPK: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=16 UPK_cue: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=16 UPK_ev: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=18 UPK: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=18 UPK_cue: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=18 UPK_ev: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=24 UPK: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=24 UPK_cue: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=5/8/K=24 UPK_ev: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=1 UPK: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=1 UPK_cue: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=1 UPK_ev: K=1 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=2 UPK: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=2 UPK_cue: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=2 UPK_ev: K=2 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=3 UPK: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=3 UPK_cue: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=3 UPK_ev: K=3 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=4 UPK: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=4 UPK_cue: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=4 UPK_ev: K=4 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=6 UPK: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=6 UPK_cue: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=6 UPK_ev: K=6 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=8 UPK: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=8 UPK_cue: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=8 UPK_ev: K=8 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=12 UPK: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=12 UPK_cue: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=12 UPK_ev: K=12 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=16 UPK: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=16 UPK_cue: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=16 UPK_ev: K=16 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=18 UPK: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=18 UPK_cue: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=18 UPK_ev: K=18 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=24 UPK: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=24 UPK_cue: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=1/d=1/4/v=3/4/r=3/4/K=24 UPK_ev: K=24 < K_suff=26: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=1 UPK: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=1 UPK_ev: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=2 UPK: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=2 UPK_ev: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=3 UPK: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=3 UPK_ev: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=4 UPK: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=4 UPK_ev: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=6 UPK: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=6 UPK_ev: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=8 UPK: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=5/8/K=8 UPK_ev: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=1 UPK: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=1 UPK_ev: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=2 UPK: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=2 UPK_ev: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=3 UPK: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=3 UPK_ev: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=4 UPK: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=4 UPK_ev: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=6 UPK: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=6 UPK_ev: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=8 UPK: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=1/3/r=3/4/K=8 UPK_ev: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=1 UPK: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=1 UPK_cue: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=1 UPK_ev: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=2 UPK: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=2 UPK_cue: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=2 UPK_ev: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=3 UPK: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=3 UPK_cue: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=3 UPK_ev: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=4 UPK: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=4 UPK_cue: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=4 UPK_ev: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=6 UPK: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=6 UPK_cue: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=6 UPK_ev: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=8 UPK: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=8 UPK_cue: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=8 UPK_ev: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=12 UPK: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=12 UPK_cue: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=5/8/K=12 UPK_ev: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=1 UPK: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=1 UPK_cue: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=1 UPK_ev: K=1 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=2 UPK: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=2 UPK_cue: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=2 UPK_ev: K=2 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=3 UPK: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=3 UPK_cue: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=3 UPK_ev: K=3 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=4 UPK: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=4 UPK_cue: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=4 UPK_ev: K=4 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=6 UPK: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=6 UPK_cue: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=6 UPK_ev: K=6 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=8 UPK: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=8 UPK_cue: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=8 UPK_ev: K=8 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=12 UPK: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=12 UPK_cue: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- upk/clean/B=2/d=1/4/v=3/4/r=3/4/K=12 UPK_ev: K=12 < K_suff=16: the per-input upper bound is infeasible (I/Q of every value-achieving policy exceeds K). The residual I-configuration search was not exhausted inside the cell budget.
- adapt/SWITCHING/H=2/B=0/d=1/2/v=3/4/r=3/4/K=1: K=1 < 27: the unprotected correct-bit policy does not fit, and the residual search was not exhausted
- adapt/SWITCHING/H=2/B=0/d=1/2/v=3/4/r=3/4/K=16: K=16 < 27: the unprotected correct-bit policy does not fit, and the residual search was not exhausted
- adapt/SWITCHING/H=2/B=0/d=1/2/v=3/4/r=3/4/K=26: K=26 < 27: the unprotected correct-bit policy does not fit, and the residual search was not exhausted
- adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=1: K=1 < 26: the B_up=1 correct-bit policy needs I=24 and Q=26 before the register is even varied. Residual search not exhausted.
- adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=16: K=16 < 26: the B_up=1 correct-bit policy needs I=24 and Q=26 before the register is even varied. Residual search not exhausted.
- adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=26: K=26 does not fit the natural T2 policy (E,I,Q)=(2,48,52). The correct-bit equivariant class was not claimed feasible here.
- adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=48: K=48 does not fit the natural T2 policy (E,I,Q)=(2,48,52). The correct-bit equivariant class was not claimed feasible here.
- adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=64: correct-bit cue-equivariant policies do not beat the better tracker, and the regime-known upper bound is strictly higher. Wrong-bit outcome signalling was not enumerated, so the optimum is not pinned.
- adapt/SWITCHING/H=2/B=1/d=1/2/v=3/4/r=3/4/K=125: correct-bit cue-equivariant policies do not beat the better tracker, and the regime-known upper bound is strictly higher. Wrong-bit outcome signalling was not enumerated, so the optimum is not pinned.
- adapt/SWITCHING/H=2/B=2/d=1/2/v=3/4/r=3/4/K=1: K=1 < 16, the displayed B_up=2 policy is not feasible and the residual search was not exhausted
- adapt/SWITCHING/H=2/B=3/d=1/2/v=3/4/r=3/4/K=1: K=1 below the 8-configuration correct-bit policy
- adapt/UNKNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=1: K=1 < 27: the unprotected correct-bit policy does not fit, and the residual search was not exhausted
- adapt/UNKNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=16: K=16 < 27: the unprotected correct-bit policy does not fit, and the residual search was not exhausted
- adapt/UNKNOWN-FIXED/H=2/B=0/d=1/2/v=3/4/r=3/4/K=26: K=26 < 27: the unprotected correct-bit policy does not fit, and the residual search was not exhausted
- adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=1: K=1 < 26: the B_up=1 correct-bit policy needs I=24 and Q=26 before the register is even varied. Residual search not exhausted.
- adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=16: K=16 < 26: the B_up=1 correct-bit policy needs I=24 and Q=26 before the register is even varied. Residual search not exhausted.
- adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=26: K=26 does not fit the natural T2 policy (E,I,Q)=(2,48,52). The correct-bit equivariant class was not claimed feasible here.
- adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=48: K=48 does not fit the natural T2 policy (E,I,Q)=(2,48,52). The correct-bit equivariant class was not claimed feasible here.
- adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=64: correct-bit cue-equivariant policies do not beat the better tracker, and the regime-known upper bound is strictly higher. Wrong-bit outcome signalling was not enumerated, so the optimum is not pinned.
- adapt/UNKNOWN-FIXED/H=2/B=1/d=1/2/v=3/4/r=3/4/K=125: correct-bit cue-equivariant policies do not beat the better tracker, and the regime-known upper bound is strictly higher. Wrong-bit outcome signalling was not enumerated, so the optimum is not pinned.
- adapt/UNKNOWN-FIXED/H=2/B=2/d=1/2/v=3/4/r=3/4/K=1: K=1 < 16, the displayed B_up=2 policy is not feasible and the residual search was not exhausted
- adapt/UNKNOWN-FIXED/H=2/B=3/d=1/2/v=3/4/r=3/4/K=1: K=1 below the 8-configuration correct-bit policy

## Timing and search accounting

Wall clock for the certificate sweep, after self-tests: 330.1 s.
Per cell the full class is limited to 4 CPU-min and the rivals share the next 6 CPU-min, in the order full, cue_blind, static_access, fixed_upkeep, cue_blind_upkeep, static_route, then stage B full_B, T_const, T_H. Every search returned before its limit, so there is no timeout and no partial certificate. CPU milliseconds are the columns above. Three-minute checkpoints were not crossed.

Recorded CPU: unpaid classes 45841 ms, route 73614 ms, adapt 712 ms. Upkeep cells are closed forms; the B_up = 2 optimum count is an exact enumeration cached once per K.

## Readings

Ambiguities and the literal readings used here are in `DEVIATIONS.md`. The protocol bytes were not edited.
