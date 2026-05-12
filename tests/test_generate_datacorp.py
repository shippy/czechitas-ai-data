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
