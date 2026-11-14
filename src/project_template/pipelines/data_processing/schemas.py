"""Pandera schemas for the data_processing pipeline."""

import pandera.pandas as pa

MODEL_INPUT_SCHEMA = pa.DataFrameSchema(
    columns={
        "shuttle_id": pa.Column(int, checks=pa.Check.ge(1)),
        "shuttle_type": pa.Column(str, nullable=False),
        "passenger_capacity": pa.Column(int, checks=pa.Check.ge(1)),
        "price": pa.Column(float, checks=pa.Check.ge(0.0)),
        "company_id": pa.Column(int, checks=pa.Check.ge(1)),
        "company_rating": pa.Column(float, checks=pa.Check.in_range(0.0, 1.0)),
        "iata_approved": pa.Column(bool),
    },
    coerce=True,
)
