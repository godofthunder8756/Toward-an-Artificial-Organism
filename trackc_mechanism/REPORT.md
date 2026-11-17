# Track C swap, option W: what the hidden state carries after a meal

**Overall: READ_OUT.** W1 (G2_10800) NO_DIFFERENCE_DETECTED; W2 (G2_14400) NO_DIFFERENCE_DETECTED; W3 (G_10800) NO_DIFFERENCE_DETECTED. Holm-adjusted p: W1 1.0000, W2 1.0000, W3 1.0000.

W4 (link, G2_10800): NOT_LINKED; rho 0.15, permutation p 0.4910, n 23.

Kind information is what the hidden state adds, in bits per sample, about which variable was eaten 2-5 steps ago, beyond the current observation and the reading history.

| set | usable | kind bits D / Y / P | derived ahead | sign p | Wilcoxon p | median difference | label | carries D / P | h-alone accuracy D / P | baseline accuracy D / P | meal bits D / P | trajectories matched D / Y / P |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G2_10800 | 23 | 0.204 / -0.018 / 0.191 | 13/23 | 0.6776 | 0.2861 | 0.038 | NO_DIFFERENCE_DETECTED | CARRIES / CARRIES | 0.741 / 0.808 | 0.830 / 0.870 | 0.482 / 0.445 | 28 / 28 / 28 |
| G2_14400 | 25 | 0.198 / -0.021 / 0.174 | 15/25 | 0.4244 | 0.3666 | 0.032 | NO_DIFFERENCE_DETECTED | CARRIES / CARRIES | 0.769 / 0.799 | 0.865 / 0.876 | 0.493 / 0.472 | 28 / 28 / 28 |
| G_10800 | 25 | 0.217 / -0.012 / 0.188 | 14/25 | 0.6900 | 0.8325 | 0.014 | NO_DIFFERENCE_DETECTED | CARRIES / CARRIES | 0.731 / 0.814 | 0.835 / 0.870 | 0.496 / 0.466 | 28 / 28 / 28 |
| G2_7200 | 15 | 0.152 / -0.026 / 0.332 | 5/15 | 0.3018 | 0.2078 | -0.101 | NO_DIFFERENCE_DETECTED | CARRIES / CARRIES | 0.681 / 0.835 | 0.748 / 0.835 | 0.534 / 0.417 | 28 / 28 / 28 |

G2_10800: kind on all seeds 18/28 (p 0.1849, NO_DIFFERENCE_DETECTED); meal 18/23 (p 0.0106, DERIVED_AHEAD); h-alone accuracy 8/23 (p 0.2100, NO_DIFFERENCE_DETECTED); baseline bits 1/23 (p 0.0000, PAID_AHEAD); penalty 10 13/23 (p 0.6776, NO_DIFFERENCE_DETECTED), 100 12/23 (p 1.0000, NO_DIFFERENCE_DETECTED); link NOT_LINKED (rho 0.15); within-arm rank correlation of kind bits with specificity derived 0.03, paid 0.40; kind bits by steps since the meal (derived | paid): 1: 0.30 | 0.30, 2: 0.24 | 0.27, 3: 0.17 | 0.18, 4: 0.13 | 0.15, 5: 0.12 | 0.11, 6: -0.00 | -0.00, 7: -0.00 | -0.00, 8: -0.00 | -0.00, 9: -0.00 | -0.00, 10: -0.00 | -0.00.

G2_14400: kind on all seeds 16/28 (p 0.5716, NO_DIFFERENCE_DETECTED); meal 16/25 (p 0.2295, NO_DIFFERENCE_DETECTED); h-alone accuracy 10/25 (p 0.4244, NO_DIFFERENCE_DETECTED); baseline bits 1/25 (p 0.0000, PAID_AHEAD); penalty 10 15/25 (p 0.4244, NO_DIFFERENCE_DETECTED), 100 15/25 (p 0.4244, NO_DIFFERENCE_DETECTED); link NOT_LINKED (rho 0.17); within-arm rank correlation of kind bits with specificity derived 0.08, paid 0.12; kind bits by steps since the meal (derived | paid): 1: 0.26 | 0.29, 2: 0.22 | 0.24, 3: 0.18 | 0.18, 4: 0.14 | 0.12, 5: 0.09 | 0.09, 6: -0.00 | -0.00, 7: -0.00 | -0.00, 8: -0.00 | -0.00, 9: -0.00 | -0.00, 10: -0.00 | -0.00.

G_10800: kind on all seeds 16/28 (p 0.5716, NO_DIFFERENCE_DETECTED); meal 14/25 (p 0.6900, NO_DIFFERENCE_DETECTED); h-alone accuracy 5/25 (p 0.0041, PAID_AHEAD); baseline bits 0/25 (p 0.0000, PAID_AHEAD); penalty 10 12/25 (p 1.0000, NO_DIFFERENCE_DETECTED), 100 14/25 (p 0.6900, NO_DIFFERENCE_DETECTED); link NOT_LINKED (rho -0.10); within-arm rank correlation of kind bits with specificity derived 0.12, paid 0.17; kind bits by steps since the meal (derived | paid): 1: 0.35 | 0.33, 2: 0.24 | 0.26, 3: 0.21 | 0.20, 4: 0.16 | 0.15, 5: 0.14 | 0.10, 6: -0.00 | -0.00, 7: -0.00 | -0.00, 8: -0.00 | -0.00, 9: -0.00 | -0.00, 10: -0.00 | -0.00.

G2_7200: kind on all seeds 8/28 (p 0.0357, PAID_AHEAD); meal 12/15 (p 0.0352, DERIVED_AHEAD); h-alone accuracy 4/15 (p 0.1185, NO_DIFFERENCE_DETECTED); baseline bits 0/15 (p 0.0001, PAID_AHEAD); penalty 10 7/15 (p 1.0000, NO_DIFFERENCE_DETECTED), 100 6/15 (p 0.6072, NO_DIFFERENCE_DETECTED); link NOT_LINKED (rho 0.17); within-arm rank correlation of kind bits with specificity derived -0.01, paid 0.34; kind bits by steps since the meal (derived | paid): 1: 0.39 | 0.46, 2: 0.25 | 0.41, 3: 0.16 | 0.33, 4: 0.12 | 0.27, 5: 0.09 | 0.20, 6: -0.00 | -0.00, 7: -0.00 | -0.00, 8: -0.00 | -0.00, 9: -0.00 | -0.00, 10: -0.00 | -0.00.
