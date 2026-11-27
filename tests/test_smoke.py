"""Smoke test: the package imports."""

import project_template


def test_import() -> None:
    assert project_template.__name__ == "project_template"
