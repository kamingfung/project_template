# Document Writing Standards

Structure and formatting rules for technical docs, reports, changelogs, and developer guides.

## Self-Contained & Terminology

- Keep each document self-contained; expand every acronym at first use.
- Reuse existing domain terms from `docs/` before coining new ones; keep one name per concept across docs, code, and PRs.
- Define new or non-obvious terms at first use and reuse canonical math symbols consistently.

## Sentences & Steps (ASD-STE100)

Write in the spirit of ASD-STE100 (Simplified Technical English) for docs, changelogs, PR descriptions, and replies:

- Use short, direct sentences in the active voice (~20 words for procedural steps, ~25 for descriptions).
- Put one imperative action per procedural step ("Run the pipeline." then "Inspect the metrics.", not both in one step).

## Structure & Evidence

- Open with a plain-language summary: the question, the answer, and what changes as a result.
- State the number, baseline, metric, and evaluation window for every improvement claim.
- Make results reproducible from the document alone: data source/pull date, branch/commit, run IDs, and rerun command.
- Link sources at first mention; never write bare references like "previous analysis showed."
- Keep volatile run results out of stable method docs; put dated results in changelogs or reports and link them.

## Formatting

- Write one paragraph per line in Markdown (no hard wrapping).
- Use numbered lists for procedures and bullets for everything else (at most two levels deep).
- Use bold only for run-in labels at the start of a bullet or paragraph, never for full sentences.
- Place display equations in `$$ ... $$` with a `where` list defining every symbol and unit directly below.
- Caption every figure and table with units and data window; refer to them by number (`Figure 1`, `Table 2`), never by position (`the chart below`).
