# Visualization Guide

Standards for matplotlib/seaborn/plotly figures, notebook plots, and text-based diagrams in `docs/`.

## Colorblind Safety & Encoding

- **Limit categorical hues to `≤4`:** beyond 4 categories, use small multiples, direct labels, or grouping.
- **Pair every color with a second encoding:** add marker shape, line style, hatch, or direct labels so charts remain legible in grayscale and under color-vision deficiency.
- **Never pair red and green** in the same chart.
- **Continuous data:** use a single-hue sequential ramp for ordered values and a two-hue diverging ramp (e.g., blue–neutral–pink/orange) for centered values. Never use rainbow (`jet`) colormaps.
- **Contrast:** ensure high contrast between text labels and background fills.

## Chart Design

- Prefer dot plots, line charts, and small multiples over dense heatmaps or stacked area charts for external audiences.
- Include units in axis labels and titles; state what is plotted and the data window in the caption.
- Plot underlying data directly rather than pasting static dashboard screenshots.

## Diagrams as Text

Draw flow, decision, and architecture diagrams as text so they diff cleanly in version control:

| Use Mermaid when | Use Graphviz (DOT) when |
| --- | --- |
| Up to ~15 nodes (decision trees, small flows) | More than ~15 nodes or many crossing edges |
| Sequence, state, Gantt, or timeline diagrams | Layered graphs needing fixed ranks or clusters |
| Inline rendering in Markdown previews is needed | Deterministic layout for repeated regeneration |

- Verify new Mermaid blocks render cleanly before committing.
- For Graphviz, keep the `.dot` source next to the doc, render with `dot -Tsvg name.dot -o img/name.svg`, commit both, and embed the SVG.
- Point to `kedro viz` for live, frequently changing pipeline topology instead of hand-maintaining large DAGs.
