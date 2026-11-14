import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell
def _(mo, pd):
    companies = pd.read_csv("data/01_raw/companies.csv")
    shuttles = pd.read_csv("data/01_raw/shuttles.csv")
    mo.vstack(
        [
            mo.md("# Fleet Exploration"),
            mo.md(
                f"Loaded **{len(companies)}** companies and **{len(shuttles)}** shuttles."
            ),
            companies,
        ]
    )


if __name__ == "__main__":
    app.run()
