"""Smoke tests for scripts/generate_datacorp.py.

These tests verify that the generator produces files with the expected
shape and conflict rates. They do NOT pin every value — only the
properties the assignment relies on.
"""

import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = REPO_ROOT / "notebooks"


@pytest.fixture(scope="session", autouse=True)
def regenerate_dataset() -> None:
    """Run the generator once per test session."""
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "generate_datacorp.py")],
        check=True,
    )


def test_main_table_row_count() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp.csv")
    assert 990 <= len(df) <= 1030


def test_telefon_column_present_and_dirty() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp.csv", dtype=str)
    assert "telefon" in df.columns
    formats_seen = set()
    for v in df["telefon"].dropna():
        if v.startswith("+420"):
            formats_seen.add("intl")
        elif " " in v:
            formats_seen.add("spaced")
        elif v.isdigit():
            formats_seen.add("digits")
    assert len(formats_seen) >= 3, f"expected >=3 phone formats, saw {formats_seen}"
    invalids = df["telefon"].isin(["???", "viz Slack"]).sum()
    assert invalids >= 1


def test_future_hire_dates_present() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp.csv", dtype=str)
    futures = df["datum_nastupu"].astype(str).str.contains("2027").sum()
    assert futures >= 3


def test_name_whitespace_dirt_present() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp.csv", dtype=str)
    leading = df["jmeno"].str.match(r"^\s").sum() + df["prijmeni"].str.match(r"^\s").sum()
    trailing = df["jmeno"].str.match(r".*\s$").sum() + df["prijmeni"].str.match(r".*\s$").sum()
    assert (leading + trailing) >= 5


def test_salary_history_shape() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_salary_history.csv", dtype=str)
    assert set(df.columns) == {"employee_id", "datum_zmeny", "plat_pred", "plat_po", "duvod"}
    assert 2500 <= len(df) <= 4000
    assert df["duvod"].isin({"raise", "promotion", "correction", "acquisition_harmonization"}).any()
