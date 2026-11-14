# Document Writing Standards

Structure and formatting rules for technical documentation, model docs, experiment reports, and developer guides.

## 1. One Self-Contained Document

- Keep one document per model, report, experiment, or guide; do not force readers to stitch fragments across files.
- Start Markdown files longer than two screens with a Table of Contents matching the section headings.
- Store static images in an adjacent `img/` folder, one file per figure (never composite multi-chart images).
- Write for a reader who sees only this document: expand every acronym at first use and state the scope in the opening paragraph.

## 2. Terminology

- **Reuse before coining:** search existing `docs/` and code before inventing a new name.
- **Define at first use:** define every new or non-obvious term in one sentence or equation and link to its canonical definition.
- **One concept, one name:** use the exact same term across docs, docstrings, comments, PR descriptions, and slides; when the code identifier differs from the domain term, state the mapping once (`promotion ("cohort" in code)`).
- **Never redefine an existing term** with a different meaning.
- **Consistent math notation:** give each symbol one meaning per document and reuse canonical symbols across related docs.

## 3. Sentences & Steps (ASD-STE100)

Write in the spirit of ASD-STE100 (Simplified Technical English) across docs, changelogs, PR descriptions, and chat replies:

- Write short, direct sentences in the active voice (~20 words for procedural steps, ~25 for descriptions).
- Give each procedural step one imperative action: `"Run the backtest."` then `"Compare the error metric."`, not both in one sentence.

## 4. Document Structure (Front Matter, Body, Back Matter)

- **Front matter:**
  - Descriptive title stating subject and document type.
  - Plain-language executive summary (~150–200 words, no formulas or tables) directly under the title stating the question, the answer, and what changes as a result.
  - Ownership line: author/team, date, and issue/PR link.
- **Body:**
  - Use at most three heading levels; number top-level sections (`## 1. Overview`) so cross-references survive edits.
  - Include everything needed to reproduce results in Method/Setup: dataset names and pull dates, parameter values, branch/commit SHA, MLflow run IDs, metric formulas, and the exact rerun command.
  - Present results before discussion; state limitations and next steps in the closing section.
  - Every improvement claim must state the **number**, the **baseline**, the **metric**, and the **evaluation window**.
- **Back matter:**
  - Close technical/model reports with: `Data availability`, `Code availability`, `Contributors`, and `Related documents` (write `Not applicable` rather than omitting).
  - Keep volatile experiment tables and dated snapshots in changelogs or PR descriptions rather than stable method docs; place large tables/plots in an appendix after the back matter.

## 5. Figures, Tables, Equations & Formatting

- **Figures:** one chart per figure; caption states what is plotted, the unit, and the data window; refer by number (`Figure 1`), never by position (`the chart below`); follow [visualization.md](visualization.md).
- **Tables:** lead-in sentence or caption above; units in column headers; consistent decimal precision per column; footnotes directly below.
- **Equations:** display math in `$$ ... $$`, inline math in `$ ... $`; number only equations referenced in prose; define every symbol with units in a `where` list directly below.
- **Lists & emphasis:** numbered lists for ordered procedures, bullets for unordered items (`<=2` nesting levels); bold only for run-in labels at the start of a bullet or paragraph; one paragraph per line (no hard line wraps); quote file paths, flags, and parameter keys in backticks.
- **Cross-references:** link sources (issues, PRs, runs, docs) at first mention; never write bare claims like `"previous analysis showed"`.

## 6. Requirements by Document Type

| Document type | Primary home | Key requirement |
| --- | --- | --- |
| Model / pipeline doc | `docs/` | Overview, method, parameters mirroring YAML, reproducibility commands, back matter |
| Experiment / PR summary | PR description or `changelogs/` | Hypothesis, arms, metric, baseline vs. branch result table, decision |
| Developer guide | `docs/developer_guides/*.md` | Imperative voice, one rule per bullet, good/bad example only where ambiguous |
