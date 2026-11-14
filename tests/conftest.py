"""Shared pytest fixtures for project_template tests."""

import pandas as pd
import pytest


@pytest.fixture
def sample_companies() -> pd.DataFrame:
    """Return a small raw companies DataFrame."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "company_rating": ["95%", "80%", None],
            "company_location": ["USA", "Canada", "Germany"],
            "total_fleet_count": [12, 6, 4],
            "iata_approved": ["t", "f", "t"],
        }
    )


@pytest.fixture
def sample_shuttles() -> pd.DataFrame:
    """Return a small raw shuttles DataFrame."""
    return pd.DataFrame(
        {
            "id": [101, 102, 103],
            "shuttle_location": ["USA", "Canada", "Germany"],
            "shuttle_type": ["Type V5", "Type A2", "Type F5"],
            "passenger_capacity": [4, 1, 10],
            "d_check_complete": ["t", "f", "t"],
            "moon_clearance_complete": ["f", "f", "t"],
            "price": ["$1,200.00", "$750.00", "$3,100.00"],
            "company_id": [1, 2, 3],
        }
    )
