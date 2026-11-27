# P1n: the endogenous monitor against a supplied analyzer, P1i's seeds (3400-3427)

**Overall: SUPPLY_DISPLACES_MONITOR.** Cost of being endogenous while the analyzer works (P1N_1): NO_DIFFERENCE_DETECTED. Valid: True. Seeds: 28. Point: 3600. Payoff per probe trial: +1 correct, -4 wrong, 0 abstain. Share of the supplied analyzer's gain over the never-damaged net that the endogenous agent recovers: median 1.014 (n 25).

| measure | PFATE | PNOFATE | FLAGON | FLAGOFF |
| --- | --- | --- | --- | --- |
| used | 0.8050 | 0.4817 | 0.7941 | 0.6342 |
| vstar | 0.8085 | 0.6543 | 0.7983 | 0.6743 |
| used_nat | 0.9566 | 0.8880 | 0.9547 | 0.9194 |
| vstar_nat | 0.9575 | 0.9228 | 0.9556 | 0.9268 |
| used_conflict | 0.4144 | -0.5348 | 0.3765 | -0.0775 |
| acc_conflict | 0.8088 | 0.6906 | 0.7794 | 0.7775 |
| norm_d | 1.3119 | 0.1588 | 1.6869 | 0.3799 |
| used_scramble | 0.9507 | 0.5904 | n/a | 0.8496 |
| used_noise | 0.9628 | 0.6186 | n/a | 0.8946 |
| used_zero | 0.9838 | 0.7576 | n/a | 0.9625 |
| vstar_scramble | 0.9668 | 0.7016 | n/a | 0.8693 |
| vstar_noise | 0.9833 | 0.7393 | n/a | 0.9088 |
| vstar_zero | 0.9980 | 0.8425 | n/a | 0.9685 |

## Tests

- P1N_1 cost of being endogenous: payoff, FLAGON against PFATE: 11/28 (sign p 0.3449, Holm 0.3449; 0.7941 against 0.8050) NO_DIFFERENCE_DETECTED
- P1N_2 analyzer silent: payoff, PFATE against FLAGOFF: 28/28 (sign p 0.0000, Holm 0.0000; 0.8050 against 0.6342) ENDOGENOUS_AHEAD
- P1N_3 displacement: norm of the integrity direction, PFATE against FLAGOFF: 27/28 (sign p 0.0000, Holm 0.0000; 1.3119 against 0.3799) ENDOGENOUS_AHEAD
- vstar_FLAGON_vs_PFATE: 10/28 (sign p 0.1849, Holm n/a; 0.7983 against 0.8085) NO_DIFFERENCE_DETECTED
- acc_conflict_PFATE_vs_FLAGON: 21/28 (sign p 0.0125, Holm n/a; 0.8088 against 0.7794) ENDOGENOUS_AHEAD
- used_FLAGON_vs_FLAGOFF: 28/28 (sign p 0.0000, Holm n/a; 0.7941 against 0.6342) ON_AHEAD
- used_FLAGOFF_vs_PNOFATE: 25/28 (sign p 0.0000, Holm n/a; 0.6342 against 0.4817) FLAGOFF_AHEAD
- vstar_PFATE_vs_FLAGOFF: 26/27 (sign p 0.0000, Holm n/a; 0.8092 against 0.6751) ENDOGENOUS_AHEAD
- used_nat_PFATE_vs_FLAGOFF: 27/28 (sign p 0.0000, Holm n/a; 0.9566 against 0.9194) ENDOGENOUS_AHEAD
- used_nat_FLAGON_vs_PFATE: 13/28 (sign p 0.8506, Holm n/a; 0.9547 against 0.9566) NO_DIFFERENCE_DETECTED
- norm_d_FLAGON_vs_FLAGOFF: 28/28 (sign p 0.0000, Holm n/a; 1.6869 against 0.3799) ON_AHEAD
- norm_d_FLAGOFF_vs_PNOFATE: 24/28 (sign p 0.0002, Holm n/a; 0.3799 against 0.1588) FLAGOFF_AHEAD
- used_scramble_PFATE_vs_FLAGOFF: 24/28 (sign p 0.0002, Holm n/a; 0.9507 against 0.8496) ENDOGENOUS_AHEAD
- used_noise_PFATE_vs_FLAGOFF: 22/28 (sign p 0.0037, Holm n/a; 0.9628 against 0.8946) ENDOGENOUS_AHEAD
- used_zero_PFATE_vs_FLAGOFF: 14/28 (sign p 1.0000, Holm n/a; 0.9838 against 0.9625) NO_DIFFERENCE_DETECTED
