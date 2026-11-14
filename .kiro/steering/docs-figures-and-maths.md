---
inclusion: fileMatch
fileMatchPattern: "docs/**/*"
---

# Documentation Figures and Maths

Conventions follow the Springer Nature article template (`sn-jnl.cls`, v3.1), so a
model doc can be lifted into a paper without reworking its figures or notation.

## Figures

- Generate every figure from a committed script next to it (`assets/make_figures.py`), never by hand or from a notebook.
- Emit one file per figure. Never a subfigure grid — SN requires each image to come from a single vector source.
- Emit `.svg` only. Add `.pdf` (or EPS, if a journal demands plain LaTeX) at the point something actually consumes it — an unread binary in the repo is weight, not preparation.
- Set figure size, fonts, and colors in the script's rcParams, not per-embed. Markdown carries no width argument.
- Write the alt text as the figure caption — a full sentence saying what the figure shows, not "Figure 1".
- Set `pdf.fonttype: 42` and `svg.fonttype: "none"` so text stays selectable and re-typesettable.
- Illustrate the real computation. If a figure shows a solve, run the solver and assert its constraints hold before saving.

## Language

- Write American English: `-ize`/`-ization` not `-ise`/`-isation`, `-or` not `-our`, `modeled` not `modelled`, `center` not `centre`.
- `analysis`, `analyses` and `basis` are already American — do not "correct" them.
- Prose must match the spelling of the identifier it describes: a doc about `regularization_weeks` writes "regularization", never "regularisation".

## Maths in Markdown

- Use `$...$` inline and `$$...$$` for display.
- Introduce every symbol at or before first use.
- Add a symbol table when a section carries more than six symbols.
- Give one symbol exactly one meaning per document. Check collisions before adding notation — the same letter for two quantities is the most common defect in these docs.
- Prefer a subscripted variant over reusing a letter: `$W_{\lambda}$` for a parameter when `$W$` is already a set.
- Wrap words and units inside maths in `\text{}`: `$P_{\text{prune}}$`, not `$P_{prune}$`.
- Expand an acronym at first use in prose, even a standard one (KKT, CVD).

## Maths in LaTeX export

- Use `equation` or `align`; never `$$...$$`, which SN's class does not number.
- Label every display equation `\label{eqN}` and cross-reference with `\ref{}`.
- In `align`, put `\nonumber` on every line except the last, and `\label{}` only on the line without it.
- Use `\left( ... \right)` for delimiters that wrap tall content.
- Use `\sum\limits_{i=1}^{n}` when limits must sit above and below in inline maths.
- Use `\lVert x \rVert` for norms, not `||x||`.
- Reach for `\mathbb`, `\mathcal`, `\mathscr` for sets and spaces; `sn-jnl.cls` loads `amsmath`, `amssymb`, `amsfonts`, `mathrsfs`.

## Citations

- Cite the source of any formulation you did not invent: the method, the algorithm, and the library that implements it.
- Number references in order of first appearance and mark them inline as `[n]`, which maps onto SN's `\cite{}` without renumbering.
- **Verify every reference against a primary source before writing it.** A plausible-looking but wrong volume, year, or page is worse than no citation, and a fabricated one is a serious defect. Search for it; do not write it from memory.
- Give a section number only when you have checked it against that edition's table of contents, and say which edition the numbering refers to.
- Include a DOI where one exists. Omit it rather than guess the suffix.
- Check before committing that every marker resolves and every entry is cited — an uncited entry means the claim it supported was deleted.

## Results Belong in the Changelog

- Never put results in `docs/`: accuracy or error tables, before/after deltas, confidence intervals, win counts, run IDs, row counts. They go in `changelogs/epics/<TICKET-ID>-*.md`, because a data refresh changes them and nothing flags the doc as stale.
- A dated, "illustrative, re-run before quoting" snapshot is still a result. The label does not make it safe to keep in a doc.
- The doc keeps the method, the decision rule and its qualitative basis ("kept because no alternative beat it out of sample"), plus a link to the changelog section and the script that reproduces it.
- Numbers that define the method do belong in the doc: parameters, thresholds, bin edges, constants.
- Figures that illustrate a computation stay in the doc. Regenerate every figure in the same run, so they cannot contradict each other.

## Anti-Patterns

- **Hand-drawn maths.** A figure whose curve is sketched rather than computed will drift from the code and cannot be re-derived.
- **The orphan asset.** An `.svg` in the repo with no generator beside it; nobody can regenerate or restyle it.
- **Symbol reuse.** `$P$` as both a total and a date within one section.
- **The undefined constant.** A symbol appearing only in an equation, never in prose or a table.
- **The unexpanded acronym.** QP, KKT, LICQ used in prose before the words behind them appear once.
- **The remembered citation.** A reference written from recall rather than checked; the page range is where this fails first.
- **The dated snapshot.** A results table in a model doc labeled with a date and "illustrative". It reads as current long after a data refresh has changed every number in it; the table belongs in the changelog.
- **The mixed dialect.** Prose spelling "regularisation" beside a `regularization_weeks` parameter it is describing.
