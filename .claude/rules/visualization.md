---
paths:
  - "notebooks/**"
  - "src/**/visualization/**"
  - "docs/**/*.md"
---

# Visualization Standards

## Colorblind Safety & Encoding

- Limit categorical plots to at most 4 hues; switch to small multiples, direct labels, or grouping beyond 4.
- Pair every color with a second non-color encoding (marker shape, line style, hatch, or direct label) so plots survive grayscale printing and color-vision deficiency.
- Never pair red and green in the same chart.
- Use a single-hue sequential ramp for ordered data and a two-hue diverging ramp (e.g., blue–neutral–pink/orange) for centered data; never use rainbow (`jet`) colormaps.
- Verify high contrast for text on colored fills.

## Chart Design

- Prefer dot plots, line charts, and small multiples over dense heatmaps or stacked area charts for external audiences.
- Include units in axis labels and titles; state what is plotted and the data window in the caption.
- Plot underlying data directly rather than pasting static dashboard screenshots.

## Diagrams as Text

- Draw flow, decision, and architecture diagrams in Mermaid or Graphviz so they diff cleanly in git.
- Use Mermaid for `≤15` nodes, sequence, state, and timeline diagrams; verify rendering before committing.
- Switch to Graphviz (`.dot` source + rendered `.svg` committed together) when a graph exceeds ~15 nodes or has crossing edges.
- Point to `kedro viz` for live, frequently changing pipeline topology rather than hand-maintaining large DAGs.

Full guide: [docs/developer_guides/visualization.md](../../docs/developer_guides/visualization.md).
