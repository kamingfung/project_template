# Visualization Guide

Standards for matplotlib/seaborn/plotly figures, notebook plots, and text-based diagrams in `docs/`.

## 1. Colorblind-Safe Palette (Okabe–Ito)

Default to the Okabe–Ito colorblind-safe qualitative palette for categorical plots:

| Name | Hex | Relative Luminance | Recommended Role |
| --- | --- | --- | --- |
| Black / Charcoal | `#000000` | 0.00 | Text, axes, primary reference line |
| Blue | `#0072B2` | 0.15 | Series 1 (primary) |
| Vermilion | `#D55E00` | 0.19 | Series 2 / single highlight / alert |
| Bluish Green | `#009E73` | 0.28 | Series 3 |
| Reddish Purple | `#CC79A7` | 0.30 | Series 4 |
| Orange | `#E69F00` | 0.43 | Series 5 (if needed) |
| Sky Blue | `#56B4E9` | 0.41 | Fills, confidence bands, secondary series |
| Neutral Gray | `#999999` | 0.32 | Context / background series |

## 2. Categorical & Continuous Encoding Rules

- **Use at most 4 categorical hues per chart:** beyond 4 categories, switch to small multiples, direct labels, or grouping.
- **Default 4-series order:** `#0072B2` (Blue), `#D55E00` (Vermilion), `#009E73` (Bluish Green), `#CC79A7` (Reddish Purple).
- **Pair every color with a second non-color encoding:** marker shape, line style (`solid`, `dashed`, `dotted`), hatch, or direct label so charts survive grayscale printing and color-vision deficiency (CVD).
- **Never pair pure red and green** without redundant shape/label encoding.
- **Single-message highlight:** use `#D55E00` (Vermilion) for the focal series and `#999999` (Gray) for context series.
- **Continuous data:** use a single-hue sequential ramp (e.g., `viridis`, `cividis`, or light-to-dark blue) for ordered data and a colorblind-safe diverging ramp (blue–neutral–vermilion) for zero-centered data. Never use rainbow (`jet`) colormaps.
- **Chart selection:** prefer dot plots, line charts, and small multiples over dense heatmaps or stacked area charts for external audiences.
- **Labels & units:** include units in axis titles; state what is plotted and the data window in the caption; plot underlying data rather than pasting dashboard screenshots.

## 3. Diagrams as Text (Mermaid vs. Graphviz)

Draw flow, decision, and architecture diagrams as text so they diff cleanly in git:

| Use Mermaid when | Use Graphviz (DOT) when |
| --- | --- |
| Up to ~15 nodes (decision trees, priority chains, small flows) | More than ~15 nodes or many crossing edges (full pipeline DAGs, lineage) |
| Sequence, state, Gantt, or timeline diagrams | Layered graphs needing fixed ranks or bounding-box clusters |
| Inline rendering in Markdown preview is required | Generated deterministically from code |

- Verify every new Mermaid block renders before committing; split or switch to Graphviz past ~15 nodes.
- For Graphviz, keep the `.dot` source next to the doc, render with `dot -Tsvg name.dot -o img/name.svg`, commit both, and embed `![caption](img/name.svg)`.
- Point to `just viz` (`kedro viz`) for live pipeline structure instead of hand-maintaining large DAG diagrams.

Reusable Mermaid node classes:

```text
classDef source fill:#0072B2,stroke:#004D7A,color:#ffffff
classDef model  fill:#009E73,stroke:#006B4E,color:#ffffff
classDef data   fill:#56B4E9,stroke:#0072B2,color:#000000
classDef output fill:#F5F5F5,stroke:#333333,color:#000000
```
