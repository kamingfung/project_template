"""Unit tests for data_processing nodes."""

import pandas as pd
import pytest

from project_template.pipelines.data_processing.nodes import (
    create_model_input_table,
    preprocess_companies,
    preprocess_shuttles,
)


def test_preprocess_companies_parses_types_without_mutating_input(
    sample_companies: pd.DataFrame,
) -> None:
    """Ratings become floats, iata_approved becomes bool, and input is unchanged."""
    original = sample_companies.copy()

    result = preprocess_companies(companies=sample_companies)

    pd.testing.assert_frame_equal(sample_companies, original)
    assert result["iata_approved"].tolist() == [True, False, True]
    assert result["company_rating"].iloc[0] == pytest.approx(0.95)
    assert pd.isna(result["company_rating"].iloc[2])


def test_preprocess_companies_empty_dataframe() -> None:
    """Empty input returns an empty DataFrame with expected columns."""
    empty = pd.DataFrame(
        columns=[
            "id",
            "company_rating",
            "company_location",
            "total_fleet_count",
            "iata_approved",
        ]
    )

    result = preprocess_companies(companies=empty)

    assert result.empty
    assert list(result.columns) == list(empty.columns)


def test_preprocess_shuttles_parses_price_and_booleans(
    sample_shuttles: pd.DataFrame,
) -> None:
    """Prices become floats and t/f flags become booleans."""
    original = sample_shuttles.copy()

    result = preprocess_shuttles(shuttles=sample_shuttles)

    pd.testing.assert_frame_equal(sample_shuttles, original)
    assert result["price"].tolist() == [1200.0, 750.0, 3100.0]
    assert result["d_check_complete"].tolist() == [True, False, True]
    assert result["moon_clearance_complete"].tolist() == [False, False, True]


def test_create_model_input_table_joins_and_drops_missing_ratings(
    sample_companies: pd.DataFrame,
    sample_shuttles: pd.DataFrame,
) -> None:
    """Joined table drops rows where company_rating is NaN."""
    companies_clean = preprocess_companies(companies=sample_companies)
    shuttles_clean = preprocess_shuttles(shuttles=sample_shuttles)

    result = create_model_input_table(
        shuttles=shuttles_clean,
        companies=companies_clean,
    )

    assert len(result) == 2
    assert set(result["shuttle_id"].tolist()) == {101, 102}
    assert result["company_rating"].isna().sum() == 0
