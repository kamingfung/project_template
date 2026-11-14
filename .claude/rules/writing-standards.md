---
paths:
  - "docs/**/*.md"
  - "changelogs/**/*.md"
---

# Document Writing Standards

## Self-Contained & Terminology

- Keep each document self-contained; expand every acronym at first use.
- Reuse existing domain terms from `docs/` before coining new ones; keep one name per concept across docs, code, and PRs.
- Define new or non-obvious terms at first use and reuse canonical math symbols consistently.

## Sentences & Steps (ASD-STE100)

- Write short, direct sentences in the active voice (~20 words for procedural steps, ~25 for descriptions).
- Put one imperative action per procedural step ("Run the pipeline." then "Inspect the metrics.").

## Structure & Evidence

- Open with a plain-language summary: the question, the answer, and what changes.
- State the number, baseline, metric, and evaluation window for every improvement claim.
- Include everything needed to reproduce results: data source/pull date, branch/commit, run IDs, and rerun command.
- Link sources at first mention; never write bare references like "previous analysis showed."
- Keep volatile run results out of stable method docs; put dated results in changelogs or reports and link them.

## Formatting

- Write one paragraph per line in markdown (no hard wrapping).
- Use numbered lists for procedures and bullets for everything else (at most two levels deep).
- Use bold only for run-in labels at the start of a bullet or paragraph, never for full sentences.
- Place display equations in `$$ ... $$` with a `where` list defining every symbol and unit directly below.
- Caption every figure and table with units and data window; refer to them by number (`Figure 1`, `Table 2`), never by position.

Full guide: [docs/developer_guides/writing_standards.md](../../docs/developer_guides/writing_standards.md).
