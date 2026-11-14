"""Nodes for the data_processing pipeline."""

import logging

import pandas as pd

from project_template.pipelines.data_processing.schemas import MODEL_INPUT_SCHEMA

logger = logging.getLogger(__name__)


def preprocess_companies(companies: pd.DataFrame) -> pd.DataFrame:
    """Parse boolean flags and percentage ratings in raw company records."""
    return companies.assign(
        iata_approved=lambda df: _is_true(df["iata_approved"]),
        company_rating=lambda df: _parse_percentage(df["company_rating"]),
    )


def preprocess_shuttles(shuttles: pd.DataFrame) -> pd.DataFrame:
    """Parse boolean flags and currency prices in raw shuttle records."""
    return shuttles.assign(
        d_check_complete=lambda df: _is_true(df["d_check_complete"]),
        moon_clearance_complete=lambda df: _is_true(df["moon_clearance_complete"]),
        price=lambda df: _parse_money(df["price"]),
    )


def create_model_input_table(
    shuttles: pd.DataFrame,
    companies: pd.DataFrame,
) -> pd.DataFrame:
    """Join preprocessed shuttles and companies and drop rows missing company ratings."""
    rated_companies = companies.dropna(subset=["company_rating"])
    dropped_count = len(companies) - len(rated_companies)
    if dropped_count:
        logger.warning(
            "Dropped %d of %d company row(s) with missing company_rating.",
            dropped_count,
            len(companies),
        )
    return (
        shuttles.merge(
            rated_companies,
            left_on="company_id",
            right_on="id",
            suffixes=("_shuttle", "_company"),
            validate="many_to_one",
        )
        .rename(columns={"id_shuttle": "shuttle_id"})
        .pipe(MODEL_INPUT_SCHEMA.validate)
    )


def _is_true(series: pd.Series) -> pd.Series:
    return series.eq("t")


def _parse_percentage(series: pd.Series) -> pd.Series:
    return (
        series.astype("string")
        .str.replace("%", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
        .div(100.0)
    )


def _parse_money(series: pd.Series) -> pd.Series:
    return (
        series.astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .pipe(pd.to_numeric, errors="coerce")
    )
