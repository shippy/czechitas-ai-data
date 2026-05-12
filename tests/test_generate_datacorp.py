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


def test_salary_history_date_formats() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_salary_history.csv", dtype=str)
    iso = df["datum_zmeny"].str.match(r"^\d{4}-\d{2}-\d{2}$").sum()
    czech = df["datum_zmeny"].str.match(r"^\d{2}\.\d{2}\.\d{4}$").sum()
    us = df["datum_zmeny"].str.match(r"^\d{2}/\d{2}/\d{4}$").sum()
    year_only = df["datum_zmeny"].str.match(r"^\d{4}$").sum()
    assert iso > 100 and czech > 100 and us > 50 and year_only > 5


def test_salary_history_decimal_mixing() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_salary_history.csv", dtype=str)
    comma_decimals = df["plat_po"].astype(str).str.contains(",").sum()
    assert comma_decimals >= 100


def test_salary_history_references_departed() -> None:
    history = pd.read_csv(NOTEBOOKS / "datacorp_salary_history.csv")
    main = pd.read_csv(NOTEBOOKS / "datacorp.csv")
    departed_ids = set(history["employee_id"]) - set(main["employee_id"])
    assert len(departed_ids) >= 5


def test_org_chart_shape_and_cycles() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_org_chart.csv")
    assert set(df.columns) == {"employee_id", "manager_id", "platnost_od"}
    assert 1000 <= len(df) <= 1400  # ~1000 + multi-row history rows
    # detect at least one cycle
    latest = df.sort_values("platnost_od").drop_duplicates("employee_id", keep="last")
    parent = dict(zip(latest["employee_id"], latest["manager_id"]))
    cycles = 0
    for emp_id, mgr in parent.items():
        if pd.isna(mgr):
            continue
        if parent.get(mgr) == emp_id:
            cycles += 1
    assert cycles >= 2  # 3 planted, expect to detect at least 2


def test_tickets_shape() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_tickets.csv", dtype=str)
    assert set(df.columns) == {
        "ticket_id", "reporter_id", "datum", "kategorie", "priorita", "status", "popis",
    }
    assert 4500 <= len(df) <= 5500


def test_tickets_taxonomy_dirty() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_tickets.csv", dtype=str)
    cats = set(df["kategorie"].unique())
    hw_variants = {c for c in cats if c.lower().startswith("hardware") or c.upper() == "HW" or "hw" in c}
    assert len(hw_variants) >= 3


def test_tickets_dirty_reporter_ids() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_tickets.csv", dtype=str)
    punctuated = df["reporter_id"].astype(str).str.contains(r"\.|^\s|\s$", regex=True).sum()
    assert punctuated >= 5
