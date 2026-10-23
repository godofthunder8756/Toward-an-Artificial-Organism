# Paper C figure visual QA V1

Status: `PASS`

## Scope

Four publication figures generated from the frozen 261-row primary raw file were inspected at their native raster dimensions and in a combined grayscale contact sheet. This inspection covered clipping, overlap, missing labels, unreadable axes, dependence on color alone, and consistency between the displayed claim and the manuscript caption.

## Results

| Figure | Native PNG | Visual result | Numeric/claim boundary |
|---|---:|---|---|
| Figure 1 — instrument sequence | 1800 × 920 | PASS | Shows 39/39, 30/30, 43 artifacts, sealed predictions, and 261 rows; it does not present instrument-development checks as endpoint results |
| Figure 2 — endpoint trajectories | 1800 × 1480 | PASS | Shows 16 slug values and equal-weight slug medians at all nine points; caption limits the primary contrast to d0 versus d192 and labels intermediate points descriptive |
| Figure 3 — detection ratio outcomes | 1700 × 980 | PASS | Directly labels E1 out-of-table, E2 not separable, E3 floor/ceiling failure, and E4 undefined; DR is not presented as sufficient for validity |
| Figure 4 — prediction scorecard | 1700 × 920 | PASS | Shows probabilities assigned to the realized outcomes and explicitly rejects use as a predictor-ranking benchmark |

## Corrections made during QA

1. Stage numbers 1–4 in Figure 1 were initially hidden by a style precedence error; explicit white text styling fixed the defect.
2. The top-axis labels in Figure 3 initially overlapped the subtitle; the plotting region and labels were moved downward.
3. The corrected versions were regenerated from the same frozen raw bytes before the figure manifest and manuscript target hashes were fixed.

## Accessibility and reproduction

- Every outcome is encoded with direct text labels; color is not the sole carrier of meaning.
- Lines, marker shapes, and labels remain distinguishable in the grayscale contact sheet.
- No clipped text, overlap, missing panel, or illegible axis remained after correction.
- The SVG sources are retained beside the PNG publication assets.
- `PAPERC_FIGURE_MANIFEST_V1.json` pins the raw source, generator, data receipt, and all eight SVG/PNG assets.

## Exact QA artifacts

- Figure manifest SHA-256: `88b099b5d060ec0fcffbf5316fd8f9e03142080c4464b801916e97084f73cfec`
- Figure data SHA-256: `27aacee62542eef1f384f70da2f29e40e2042e8ee66f88683a1a9d29dd13b496`
- Grayscale contact sheet SHA-256: `1694767eddb80dda3d6164a29837368ad485852ceb7944197ee0618b06416c34`
- Preflight receipt SHA-256: `b937011037a208f215c034d0888d8c94a87d38e0d26b8431b79542b5506107f6` (60/60 checks, including every displayed slug value and median at all nine evaluation points)

This QA is a production-readiness check for the figure set. It does not grant publication authority and does not replace independent numerical review.
