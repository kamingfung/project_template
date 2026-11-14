"""Nodes for the data_processing pipeline."""

import pandas as pd

from project_template.pipelines.data_processing.schemas import MODEL_INPUT_SCHEMA


def preprocess_companies(companies: pd.DataFrame) -> pd.DataFrame:
    """Parse boolean flags and percentage ratings in raw company records."""
    df = companies.copy()
    df["iata_approved"] = _is_true(df["iata_approved"])
    df["company_rating"] = _parse_percentage(df["company_rating"])
    return df


def preprocess_shuttles(shuttles: pd.DataFrame) -> pd.DataFrame:
    """Parse boolean flags and currency prices in raw shuttle records."""
    df = shuttles.copy()
    df["d_check_complete"] = _is_true(df["d_check_complete"])
    df["moon_clearance_complete"] = _is_true(df["moon_clearance_complete"])
    df["price"] = _parse_money(df["price"])
    return df


def create_model_input_table(
    shuttles: pd.DataFrame,
    companies: pd.DataFrame,
) -> pd.DataFrame:
    """Join preprocessed shuttles and companies and drop rows missing company ratings."""
    rated_companies = companies.dropna(subset=["company_rating"])
    merged = shuttles.merge(
        rated_companies,
        left_on="company_id",
        right_on="id",
        suffixes=("_shuttle", "_company"),
    )
    result = merged.rename(columns={"id_shuttle": "shuttle_id"})
    return MODEL_INPUT_SCHEMA.validate(result)


def _is_true(series: pd.Series) -> pd.Series:
    return series.eq("t")


def _parse_percentage(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.replace("%", "", regex=False)
    return pd.to_numeric(cleaned, errors="coerce") / 100.0


def _parse_money(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")
