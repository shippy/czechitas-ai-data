# DataCorp Dataset Expansion — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand `scripts/generate_datacorp.py` to produce 7 dataset files (3 existing + 4 new) for the Czechitas AI-in-data-analytics course, with deeper relational structure and richer planted dirt. Follows the approved spec at `docs/superpowers/specs/2026-05-12-datacorp-dataset-expansion-design.md`.

**Architecture:** A single regeneration script (`scripts/generate_datacorp.py`) restructured into paired `build_*` / `apply_dirt_*` functions per file. A shared "employee universe" of ~1015 employees is generated first; the main HR CSV persists only ~1000 of them (~15 are tagged as departed and used by side-tables to create natural survivorship bias). Determinism preserved via the existing `SEED = 42`.

**Tech Stack:** Python 3.13, pandas, numpy, openpyxl (new), pytest (new dev dep), uv. Czech free-text generation via existing string templates.

---

## File structure

| File | Action | Responsibility |
|---|---|---|
| `scripts/generate_datacorp.py` | Heavy modify | Extended generator; orchestrates 7 outputs |
| `tests/test_generate_datacorp.py` | Create | Smoke tests over generated DataFrames (shape, conflict rates, idempotency) |
| `pyproject.toml` | Modify | Add `openpyxl` to `dependencies`; add `pytest` to a new `[dependency-groups] test` group |
| `uv.lock` | Auto-update | Via `uv sync` |
| `README.md` | Modify | Extend "Datasety" table |
| `notebooks/datacorp.csv` | Regenerate | Same schema +`telefon`; ~1000 rows |
| `notebooks/datacorp_reviews.csv` | Regenerate | ~150 rows; new sarcastic + wrong-person variants |
| `notebooks/datacorp_exit_interviews.csv` | Regenerate | ~70 rows; mixed-language + self-contradiction |
| `notebooks/datacorp_salary_history.csv` | Create | ~3000 rows |
| `notebooks/datacorp_org_chart.csv` | Create | ~1000+ rows |
| `notebooks/datacorp_tickets.csv` | Create | ~5000 rows |
| `notebooks/datacorp_payroll_q3.xlsx` | Create | ~1000 rows + merged headers + totals row |

---

## Task 1: Add dependencies and test scaffolding

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/test_generate_datacorp.py`
- Create: `tests/__init__.py` (empty)

- [ ] **Step 1: Add `openpyxl` and `pytest` deps**

Edit `pyproject.toml`:
- Append `"openpyxl>=3.1"` to the `dependencies` list.
- Add a new dependency group:
  ```toml
  [dependency-groups]
  scrape = [
      "firecrawl-py>=1.13.5",
      "typer>=0.15.2",
  ]
  test = [
      "pytest>=8.0",
  ]
  ```

- [ ] **Step 2: Sync the environment**

Run: `uv sync --group test`
Expected: lockfile updates, `openpyxl` and `pytest` installed.

- [ ] **Step 3: Create empty test package**

Create `tests/__init__.py` (empty file).

Create `tests/test_generate_datacorp.py` with this content:

```python
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
    # ~1000 employees + ~10 duplicates from existing dirt
    assert 990 <= len(df) <= 1030
```

- [ ] **Step 4: Run the test to confirm scaffolding works**

Run: `uv run --group test pytest tests/test_generate_datacorp.py::test_main_table_row_count -v`
Expected: PASS (the existing generator already produces ~510 rows — this test will fail until Task 2 scales up to 1000. **Accept FAIL here** and proceed; revisit after Task 2.)

Actually: edit the assertion temporarily to `assert 500 <= len(df) <= 530` so the scaffolding goes green now. We will tighten it in Task 2 once headcount changes.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml uv.lock tests/__init__.py tests/test_generate_datacorp.py
git commit -m "tests: add pytest scaffolding + openpyxl dep for generator"
```

---

## Task 2: Refactor existing functions and introduce employee universe

**Files:**
- Modify: `scripts/generate_datacorp.py`
- Modify: `tests/test_generate_datacorp.py`

**Goal:** Rename existing functions to the new convention, scale headcount, and add the "employee universe" concept (~1015 employees where ~15 are tagged departed and excluded from the main CSV).

- [ ] **Step 1: Update headcounts**

In `scripts/generate_datacorp.py`, in the `DEPARTMENTS` dict, scale `headcount` values so the total reaches ~1015. Existing total is ~510. Roughly double each department's `headcount`. Keep the relative proportions. Confirm the sum: add a `print(f"Universe size: {sum(d['headcount'] for d in DEPARTMENTS.values())}")` inside `main()` for one run.

- [ ] **Step 2: Rename functions in-place**

Use search-and-replace within `scripts/generate_datacorp.py`:
- `generate_employees` → `build_main_df`
- `apply_dirt(` (the function) → `apply_dirt_main(`
- `generate_reviews` → `build_reviews`
- `generate_exit_interviews` → `build_exit_interviews`

Update call sites in `main()` accordingly.

- [ ] **Step 3: Add departed-employee tagging**

Add a new function after `build_main_df`:

```python
def tag_departures(df: pd.DataFrame) -> pd.DataFrame:
    """Tag ~15 employees as departed.

    Departed employees stay in the in-memory universe (side-tables can
    reference them) but are filtered out of the persisted main CSV.
    This creates natural survivorship bias for downstream analysis.
    """
    df = df.copy()
    df["_departed"] = False
    departed_idx = RNG.choice(df.index, size=15, replace=False)
    df.loc[departed_idx, "_departed"] = True
    return df
```

- [ ] **Step 4: Update `main()` to use the universe pattern**

Replace the body of `main()` so it follows this skeleton (full version comes in Task 12 — for now just verify the rename + universe wiring works):

```python
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Building employee universe...")
    universe = build_main_df()
    universe = tag_departures(universe)
    print(f"  Universe size: {len(universe)} ({universe['_departed'].sum()} departed)")

    # Side-tables use full universe; main CSV uses only non-departed.
    main_df = universe[~universe["_departed"]].drop(columns=["_departed"]).copy()
    print(f"  Main HR rows (pre-dirt): {len(main_df)}")

    main_df_dirty = apply_dirt_main(main_df)
    print(f"  Main HR rows (post-dirt): {len(main_df_dirty)}")

    reviews = build_reviews(universe.drop(columns=["_departed"]))
    exits = build_exit_interviews(universe.drop(columns=["_departed"]))

    # Save the three existing files for now; new ones come in later tasks.
    main_df_dirty.to_csv(OUTPUT_DIR / "datacorp.csv", index=False)
    reviews.to_csv(OUTPUT_DIR / "datacorp_reviews.csv", index=False)
    exits.to_csv(OUTPUT_DIR / "datacorp_exit_interviews.csv", index=False)
    print("\nDone!")
```

- [ ] **Step 5: Tighten the main-table row count test**

In `tests/test_generate_datacorp.py`, change the assertion to:
```python
assert 990 <= len(df) <= 1030
```

- [ ] **Step 6: Run the generator and tests**

Run: `uv run scripts/generate_datacorp.py`
Expected: completes, prints "Universe size: ~1015", produces 3 CSVs.

Run: `uv run --group test pytest tests/test_generate_datacorp.py -v`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp.csv notebooks/datacorp_reviews.csv notebooks/datacorp_exit_interviews.csv
git commit -m "generator: scale to ~1000 employees and introduce universe pattern"
```

---

## Task 3: Expand `apply_dirt_main` with new dirt categories

**Files:**
- Modify: `scripts/generate_datacorp.py` (`apply_dirt_main`)
- Modify: `tests/test_generate_datacorp.py`

**New dirt:** `telefon` column with mixed formats + invalids (cat 7); email/name mismatches from rehires (cat 8); whitespace in names (cat 9); encoding mojibake (cat 10); future hire dates (cat 16); diacritic-folded duplicate identities (cat 15).

- [ ] **Step 1: Write failing tests**

Append to `tests/test_generate_datacorp.py`:

```python
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
```

Run: `uv run --group test pytest tests/test_generate_datacorp.py -v`
Expected: 3 new tests FAIL.

- [ ] **Step 2: Add `telefon` column to `build_main_df`**

Inside `build_main_df`, when constructing each row dict, add a `telefon` field formatted as `+420 ddd ddd ddd` initially (clean form). Use `RNG` for the digit groups. Example:
```python
"telefon": f"+420 {RNG.integers(600, 800)} {RNG.integers(100, 1000):03d} {RNG.integers(100, 1000):03d}",
```

- [ ] **Step 3: Extend `apply_dirt_main` with new dirt blocks**

Add the following blocks at the end of `apply_dirt_main` (keep existing dirt blocks 1–6 unchanged):

```python
    # 7. Phone-number formats and invalids
    phone_idx = df.index.tolist()
    n_alt = 200  # split across alt formats
    alt_idx = RNG.choice(phone_idx, size=n_alt, replace=False)
    half = n_alt // 2
    for i in alt_idx[:half]:
        df.at[i, "telefon"] = df.at[i, "telefon"].replace("+420 ", "").replace(" ", "")
    for i in alt_idx[half:]:
        df.at[i, "telefon"] = df.at[i, "telefon"].replace("+420 ", "")
    missing_phone = RNG.choice(phone_idx, size=20, replace=False)
    df.loc[missing_phone, "telefon"] = np.nan
    invalid_phone = RNG.choice(phone_idx, size=5, replace=False)
    df.loc[invalid_phone, "telefon"] = RNG.choice(["???", "viz Slack"], size=5)

    # 8. Email / name mismatches (rehires reusing employee_id)
    rehire_idx = RNG.choice(df.index, size=15, replace=False)
    for i in rehire_idx:
        df.at[i, "email"] = "petra.svobodova@datacorp.cz"  # placeholder ghost email
        # vary the ghost emails a bit
    ghost_emails = [
        "petra.svobodova@datacorp.cz", "tomas.novak@datacorp.cz",
        "jana.kralova@datacorp.cz", "marek.benes@datacorp.cz",
        "lucie.dvorakova@datacorp.cz",
    ]
    for k, i in enumerate(rehire_idx):
        df.at[i, "email"] = ghost_emails[k % len(ghost_emails)]

    # 9. Whitespace and embedded newlines in name fields
    ws_idx = RNG.choice(df.index, size=30, replace=False)
    for k, i in enumerate(ws_idx):
        col = "jmeno" if k % 2 == 0 else "prijmeni"
        original = df.at[i, col]
        if k % 3 == 0:
            df.at[i, col] = f" {original}"
        elif k % 3 == 1:
            df.at[i, col] = f"{original} "
        else:
            df.at[i, col] = f" {original} "

    # 10. Encoding mojibake — 3 rows with mangled diacritics
    mojibake_idx = RNG.choice(df.index, size=3, replace=False)
    mojibake_map = str.maketrans({"Č": "Ä", "č": "Ä", "ž": "Å¾", "š": "Å¡"})
    for i in mojibake_idx:
        df.at[i, "prijmeni"] = str(df.at[i, "prijmeni"]).translate(mojibake_map)

    # 16. Future hire dates (typo 2017 -> 2027)
    future_idx = RNG.choice(df.index, size=5, replace=False)
    for i in future_idx:
        existing = str(df.at[i, "datum_nastupu"])
        df.at[i, "datum_nastupu"] = existing.replace("2017", "2027").replace("2018", "2028")
        if "20" not in df.at[i, "datum_nastupu"][-4:]:
            df.at[i, "datum_nastupu"] = "2027-06-15"

    # 15. Diacritic-folded duplicate identities — add 2 paired rows
    if "Černý" in df["prijmeni"].astype(str).values:
        cerny_rows = df[df["prijmeni"].astype(str) == "Černý"].head(1).copy()
        if len(cerny_rows):
            folded = cerny_rows.copy()
            folded["prijmeni"] = "Cerny"
            folded["jmeno"] = folded["jmeno"].astype(str).str.replace("á", "a").str.replace("í", "i")
            folded["employee_id"] = folded["employee_id"].astype(int).max() + 5000
            folded["email"] = folded["email"].astype(str).str.replace("ý", "y").str.replace("á", "a")
            df = pd.concat([df, folded], ignore_index=True)
```

- [ ] **Step 4: Run generator + tests**

Run: `uv run scripts/generate_datacorp.py`
Run: `uv run --group test pytest tests/test_generate_datacorp.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp.csv
git commit -m "generator: add telefon column and 6 new dirt categories to main table"
```

---

## Task 4: `build_salary_history` (clean)

**Files:**
- Modify: `scripts/generate_datacorp.py`
- Modify: `tests/test_generate_datacorp.py`

- [ ] **Step 1: Write failing test**

Append:
```python
def test_salary_history_shape() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_salary_history.csv", dtype=str)
    assert set(df.columns) == {"employee_id", "datum_zmeny", "plat_pred", "plat_po", "duvod"}
    assert 2500 <= len(df) <= 3500
    assert df["duvod"].isin({"raise", "promotion", "correction", "acquisition_harmonization"}).any()
```

Run pytest — expect FAIL (file does not exist yet).

- [ ] **Step 2: Implement `build_salary_history`**

Add this function near the other `build_*` functions:

```python
def build_salary_history(universe: pd.DataFrame) -> pd.DataFrame:
    """Generate 1–6 salary events per employee, chronological per employee.

    Operates on the full universe (including departed employees) so
    departed people retain salary history that is absent from the main CSV.
    """
    rows = []
    for _, emp in universe.iterrows():
        n_events = int(RNG.integers(1, 7))
        try:
            hire = pd.to_datetime(emp["datum_nastupu"])
        except (ValueError, TypeError):
            hire = pd.Timestamp("2020-01-01")
        current_salary = float(emp["plat"]) if pd.notna(emp.get("plat")) else 50_000.0
        # Walk backwards: today's salary, then earlier raises
        salary = current_salary
        dates = sorted([
            hire + pd.Timedelta(days=int(RNG.integers(30, 365 * 5)))
            for _ in range(n_events)
        ])
        prev = current_salary - sum(RNG.integers(2_000, 8_000) for _ in range(n_events))
        for d in dates:
            raise_amt = int(RNG.integers(2_000, 8_000))
            new_salary = prev + raise_amt
            duvod = RNG.choice(
                ["raise", "promotion", "correction", "acquisition_harmonization"],
                p=[0.65, 0.20, 0.10, 0.05],
            )
            rows.append({
                "employee_id": int(emp["employee_id"]),
                "datum_zmeny": d.strftime("%Y-%m-%d"),
                "plat_pred": prev,
                "plat_po": new_salary,
                "duvod": duvod,
            })
            prev = new_salary
    df = pd.DataFrame(rows)
    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)
```

- [ ] **Step 3: Wire into `main()`**

Add inside `main()` after building the universe:
```python
    print("Building salary history...")
    salary_history = build_salary_history(universe.drop(columns=["_departed"]))
    salary_history.to_csv(OUTPUT_DIR / "datacorp_salary_history.csv", index=False)
    print(f"  Salary history rows: {len(salary_history)}")
```

- [ ] **Step 4: Run + verify test**

Run: `uv run scripts/generate_datacorp.py`
Run: `uv run --group test pytest tests/test_generate_datacorp.py::test_salary_history_shape -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp_salary_history.csv
git commit -m "generator: add datacorp_salary_history.csv (clean)"
```

---

## Task 5: `apply_dirt_salary_history`

**Files:**
- Modify: `scripts/generate_datacorp.py`
- Modify: `tests/test_generate_datacorp.py`

**Dirt planted:** date format soup (cat 12); decimal-separator mixing (cat 11); conflict rates with main `plat` (85/10/5/3%); 5 rows for employees not in main CSV (already happens — verify); 3 cycle-style salary corrections out of order (cat 17); silent ID collision (cat 14); also dial main `plat` to NaN for the 3% that have history but no current salary.

- [ ] **Step 1: Write failing tests**

```python
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
```

Run — expect FAIL.

- [ ] **Step 2: Implement `apply_dirt_salary_history`**

```python
def apply_dirt_salary_history(df: pd.DataFrame, main_df: pd.DataFrame) -> pd.DataFrame:
    """Plant dirt in salary history. `main_df` is the post-dirt main CSV.

    Conflict rates (per the spec) target ratios over employees present
    in both the salary-history and the main CSV.
    """
    df = df.copy()

    # 12. Date format soup
    n = len(df)
    rest_idx = df.index.tolist()
    czech_idx = RNG.choice(rest_idx, size=int(n * 0.30), replace=False)
    remaining = [i for i in rest_idx if i not in set(czech_idx)]
    us_idx = RNG.choice(remaining, size=int(n * 0.15), replace=False)
    remaining = [i for i in remaining if i not in set(us_idx)]
    year_only_idx = RNG.choice(remaining, size=int(n * 0.03), replace=False)
    for i in czech_idx:
        d = pd.to_datetime(df.at[i, "datum_zmeny"])
        df.at[i, "datum_zmeny"] = d.strftime("%d.%m.%Y")
    for i in us_idx:
        d = pd.to_datetime(df.at[i, "datum_zmeny"])
        df.at[i, "datum_zmeny"] = d.strftime("%m/%d/%Y")
    for i in year_only_idx:
        df.at[i, "datum_zmeny"] = str(pd.to_datetime(df.at[i, "datum_zmeny"]).year)

    # 11. Decimal separator mixing in plat_po
    decimal_idx = RNG.choice(df.index, size=int(n * 0.10), replace=False)
    nbsp = " "
    for i in decimal_idx:
        v = float(df.at[i, "plat_po"])
        df.at[i, "plat_po"] = f"{int(v // 1000)}{nbsp}{int(v) % 1000:03d},{int((v % 1) * 100):02d}"

    # Drive conflicts with main `plat` (10% off-by-small, 5% propagation-lag, 3% main is NaN)
    # The 85% "matches exactly" case is achieved by build_salary_history's design
    # — the latest plat_po already equals main `plat` for the natural case.
    common_ids = set(df["employee_id"]) & set(main_df["employee_id"])
    common_list = list(common_ids)
    RNG.shuffle(common_list)
    off_small = common_list[: int(len(common_list) * 0.10)]
    # Bump the latest plat_po by a small delta to create disagreement
    for emp_id in off_small:
        rows = df[df["employee_id"] == emp_id]
        if len(rows) == 0:
            continue
        latest_idx = rows.index[-1]
        try:
            val = float(str(df.at[latest_idx, "plat_po"]).replace(nbsp, "").replace(",", "."))
            df.at[latest_idx, "plat_po"] = int(val + RNG.integers(1_000, 5_000))
        except (ValueError, TypeError):
            pass

    # 17. Salary history out of order — pick 2 employees, add a backdated correction
    out_of_order_emps = RNG.choice(common_list, size=2, replace=False)
    for emp_id in out_of_order_emps:
        rows = df[df["employee_id"] == emp_id].sort_values("datum_zmeny")
        if len(rows) < 2:
            continue
        backdate = pd.to_datetime(rows.iloc[0]["datum_zmeny"], errors="coerce")
        if pd.isna(backdate):
            continue
        backdate = backdate - pd.Timedelta(days=30)
        df = pd.concat([df, pd.DataFrame([{
            "employee_id": emp_id,
            "datum_zmeny": backdate.strftime("%Y-%m-%d"),
            "plat_pred": rows.iloc[0]["plat_pred"],
            "plat_po": float(rows.iloc[0]["plat_pred"]) - 2000,
            "duvod": "correction",
        }])], ignore_index=True)

    # 14. Silent ID collision — pick one departed ID and reassign half its history
    #     rows to a hire-2022 different employee's ID-slot. Implementation:
    #     take 3 history rows of one current employee and stamp them with the
    #     employee_id of a different current employee.
    if len(common_list) >= 2:
        donor, victim = common_list[0], common_list[1]
        donor_rows = df[df["employee_id"] == donor].head(3).index
        df.loc[donor_rows, "employee_id"] = victim

    return df.reset_index(drop=True)
```

- [ ] **Step 3: Wire in `main()`**

```python
    salary_history = apply_dirt_salary_history(salary_history, main_df_dirty)
    salary_history.to_csv(OUTPUT_DIR / "datacorp_salary_history.csv", index=False)
```

- [ ] **Step 4: Tests pass**

Run: `uv run scripts/generate_datacorp.py && uv run --group test pytest tests/test_generate_datacorp.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp_salary_history.csv
git commit -m "generator: plant dirt in salary history (dates, decimals, conflicts, collisions)"
```

---

## Task 6: `build_org_chart` and dirt

**Files:**
- Modify: `scripts/generate_datacorp.py`
- Modify: `tests/test_generate_datacorp.py`

- [ ] **Step 1: Write failing tests**

```python
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
```

Run — expect FAIL.

- [ ] **Step 2: Implement `build_org_chart` + dirt inline**

```python
def build_org_chart(universe: pd.DataFrame) -> pd.DataFrame:
    """One row per employee per reporting line.

    ~80% of employees have 1 row; ~20% have 2–3 rows; cycles and orphan
    manager_ids are planted.
    """
    rows = []
    universe = universe.copy()
    universe["plat"] = pd.to_numeric(universe["plat"], errors="coerce").fillna(0)

    # Heuristic manager picker: choose someone in the same department with higher salary
    by_dept = {dept: sub for dept, sub in universe.groupby("oddeleni")}
    ids = universe["employee_id"].tolist()
    for _, emp in universe.iterrows():
        dept_peers = by_dept.get(emp["oddeleni"])
        candidates = dept_peers[dept_peers["plat"] > emp["plat"]] if dept_peers is not None else None
        if candidates is None or len(candidates) == 0:
            mgr = None  # department head
        else:
            mgr = int(candidates.sample(1, random_state=int(emp["employee_id"])).iloc[0]["employee_id"])
        hire = str(emp["datum_nastupu"])
        rows.append({
            "employee_id": int(emp["employee_id"]),
            "manager_id": mgr,
            "platnost_od": hire if hire and hire != "nan" else "2020-01-01",
        })
        # ~20% get a manager change
        if RNG.random() < 0.20 and mgr is not None:
            new_mgr = int(RNG.choice(ids))
            rows.append({
                "employee_id": int(emp["employee_id"]),
                "manager_id": new_mgr,
                "platnost_od": "2024-01-15",
            })

    df = pd.DataFrame(rows)

    # Plant 3 cycles: pick 3 pairs and swap
    for _ in range(3):
        pair = RNG.choice(df["employee_id"].unique(), size=2, replace=False)
        a, b = int(pair[0]), int(pair[1])
        a_latest = df[df["employee_id"] == a].tail(1).index
        b_latest = df[df["employee_id"] == b].tail(1).index
        df.loc[a_latest, "manager_id"] = b
        df.loc[b_latest, "manager_id"] = a

    # Plant 15 orphan manager_ids (point at IDs not in universe)
    orphan_idx = RNG.choice(df.index, size=15, replace=False)
    df.loc[orphan_idx, "manager_id"] = RNG.integers(9000, 9999, size=15)

    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)
```

- [ ] **Step 3: Wire in `main()` and commit**

```python
    print("Building org chart...")
    org = build_org_chart(universe.drop(columns=["_departed"]))
    org.to_csv(OUTPUT_DIR / "datacorp_org_chart.csv", index=False)
    print(f"  Org chart rows: {len(org)}")
```

Run: `uv run scripts/generate_datacorp.py && uv run --group test pytest tests/test_generate_datacorp.py -v`
Expected: PASS.

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp_org_chart.csv
git commit -m "generator: add datacorp_org_chart.csv with cycles and orphans"
```

---

## Task 7: `build_tickets` (clean)

**Files:**
- Modify: `scripts/generate_datacorp.py`
- Modify: `tests/test_generate_datacorp.py`

- [ ] **Step 1: Failing test**

```python
def test_tickets_shape() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_tickets.csv", dtype=str)
    assert set(df.columns) == {
        "ticket_id", "reporter_id", "datum", "kategorie", "priorita", "status", "popis",
    }
    assert 4500 <= len(df) <= 5500
```

- [ ] **Step 2: Implement `build_tickets`**

```python
TICKET_TEMPLATES = {
    "Hardware": [
        "Nefunguje mi {hw}. Můžete se na to podívat?",
        "{hw} přestal/a fungovat dnes ráno. Potřebuji to vyřešit co nejdřív.",
        "Prosím o výměnu {hw} — je už za zenitem.",
    ],
    "Software": [
        "Nejde mi nainstalovat {sw}. Vyhazuje to chybu.",
        "Po updatu {sw} se mi rozbilo {feature}.",
        "Mohli byste mi prosím přidat licenci na {sw}?",
    ],
    "Účet a přístup": [
        "Zapomněl/a jsem heslo do {system}.",
        "Nemám přístup ke sdílenému disku týmu.",
        "Můj VPN profil nefunguje od pondělí.",
    ],
    "Ostatní": [
        "Nefunguje kávovar v 3. patře.",
        "Někdo mi v ledničce snědl oběd. Co s tím?",
        "Klimatizace v open-spacu zase netáhne.",
    ],
}
HW = ["notebook", "monitor", "myš", "klávesnice", "dock", "headset"]
SW = ["VS Code", "Slack", "Excel", "Jira", "Figma"]
FEATURE = ["sdílení obrazovky", "notifikace", "VPN integrace", "SSO login"]
SYSTEM = ["Jira", "Confluence", "interní portál", "Slack"]


def build_tickets(universe: pd.DataFrame) -> pd.DataFrame:
    rows = []
    ids = universe["employee_id"].tolist()
    start = pd.Timestamp("2024-01-01")
    for ticket_id in range(1, 5001):
        reporter = int(RNG.choice(ids))
        cat = str(RNG.choice(list(TICKET_TEMPLATES.keys()), p=[0.35, 0.35, 0.20, 0.10]))
        tmpl = str(RNG.choice(TICKET_TEMPLATES[cat]))
        popis = tmpl.format(
            hw=RNG.choice(HW), sw=RNG.choice(SW),
            feature=RNG.choice(FEATURE), system=RNG.choice(SYSTEM),
        )
        when = start + pd.Timedelta(days=int(RNG.integers(0, 500)),
                                    hours=int(RNG.integers(8, 18)),
                                    minutes=int(RNG.integers(0, 60)))
        rows.append({
            "ticket_id": ticket_id,
            "reporter_id": reporter,
            "datum": when.strftime("%Y-%m-%d %H:%M:%S"),
            "kategorie": cat,
            "priorita": str(RNG.choice(["P1", "P2", "P3", "P4"], p=[0.05, 0.20, 0.50, 0.25])),
            "status": str(RNG.choice(["open", "pending", "closed"], p=[0.15, 0.20, 0.65])),
            "popis": popis,
        })
    return pd.DataFrame(rows)
```

Wire into `main()`:
```python
    tickets = build_tickets(universe.drop(columns=["_departed"]))
    tickets.to_csv(OUTPUT_DIR / "datacorp_tickets.csv", index=False)
```

- [ ] **Step 3: Tests + commit**

Run: `uv run scripts/generate_datacorp.py && uv run --group test pytest -v`

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp_tickets.csv
git commit -m "generator: add datacorp_tickets.csv (clean)"
```

---

## Task 8: `apply_dirt_tickets`

**Files:**
- Modify: `scripts/generate_datacorp.py`
- Modify: `tests/test_generate_datacorp.py`

**Dirt planted:** taxonomy mismatch (5–7 surface forms), priorita ≠ popis content for 40%, ~50 invalid reporter_ids, ~10 trailing-punctuation/leading-whitespace IDs.

- [ ] **Step 1: Failing test**

```python
def test_tickets_taxonomy_dirty() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_tickets.csv", dtype=str)
    cats = set(df["kategorie"].unique())
    hw_variants = {c for c in cats if c.lower().startswith("hardware") or c.upper() == "HW" or "hw" in c}
    assert len(hw_variants) >= 3


def test_tickets_dirty_reporter_ids() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_tickets.csv", dtype=str)
    punctuated = df["reporter_id"].astype(str).str.contains(r"\.|^\s|\s$", regex=True).sum()
    assert punctuated >= 5
```

- [ ] **Step 2: Implement**

```python
def apply_dirt_tickets(df: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Taxonomy mismatch — replace ~7% of "Hardware" with variants
    hw_mask = df["kategorie"] == "Hardware"
    hw_idx = df[hw_mask].index.tolist()
    variants = ["HW", "hardware-other", "hw / sw", "HARDWARE", "Hardware "]
    chunk = max(1, len(hw_idx) // (len(variants) * 7))
    cursor = 0
    for v in variants:
        slice_idx = hw_idx[cursor: cursor + chunk]
        df.loc[slice_idx, "kategorie"] = v
        cursor += chunk

    # Priorita mismatch — bump 40% of P3/P4 with trivial popis to P1
    coffee_mask = df["popis"].str.contains("kávovar|lednič|klimatizac", na=False)
    coffee_idx = df[coffee_mask].sample(frac=0.4, random_state=SEED).index
    df.loc[coffee_idx, "priorita"] = "P1"

    # 50 invalid reporter_ids
    valid_ids = set(universe["employee_id"])
    invalid_idx = RNG.choice(df.index, size=50, replace=False)
    df.loc[invalid_idx, "reporter_id"] = RNG.integers(9000, 9999, size=50)

    # 10 trailing-punctuation / leading-whitespace IDs
    punct_idx = RNG.choice(df.index, size=10, replace=False)
    for k, i in enumerate(punct_idx):
        rid = str(df.at[i, "reporter_id"])
        df.at[i, "reporter_id"] = f"{rid}." if k % 2 == 0 else f" {rid}"

    return df
```

Wire into `main()`:
```python
    tickets = apply_dirt_tickets(tickets, universe)
    tickets.to_csv(OUTPUT_DIR / "datacorp_tickets.csv", index=False)
```

- [ ] **Step 3: Test + commit**

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp_tickets.csv
git commit -m "generator: plant dirt in tickets (taxonomy, priorita, IDs)"
```

---

## Task 9: `build_payroll_xlsx` (with dirt baked in)

**Files:**
- Modify: `scripts/generate_datacorp.py`
- Modify: `tests/test_generate_datacorp.py`

Because the Excel output has structural quirks (merged header rows, totals row, multi-sheet), this task builds clean + dirty together.

- [ ] **Step 1: Failing test**

```python
def test_payroll_xlsx_structure() -> None:
    import openpyxl
    path = NOTEBOOKS / "datacorp_payroll_q3.xlsx"
    wb = openpyxl.load_workbook(path, data_only=True)
    assert "Mzdy Q3 2025" in wb.sheetnames
    # Top 3 rows + bottom totals row
    df = pd.read_excel(path, sheet_name="Mzdy Q3 2025", header=None)
    assert df.iloc[0].isna().all() or df.iloc[0].notna().sum() <= 2
    # Find the CELKEM row
    assert (df.astype(str).apply(lambda r: r.str.contains("CELKEM", na=False).any(), axis=1)).any()


def test_payroll_xlsx_currency_landmine() -> None:
    df = pd.read_excel(NOTEBOOKS / "datacorp_payroll_q3.xlsx",
                       sheet_name="Mzdy Q3 2025", skiprows=3)
    # Drop totals row
    df = df[df["os_cislo"].apply(lambda x: str(x).replace(".0", "").isdigit())]
    eur_like = df["mzda_brutto"].astype(float).between(1500, 4000).sum()
    assert eur_like >= 4
```

- [ ] **Step 2: Implement**

```python
def build_payroll_xlsx(main_df: pd.DataFrame) -> pd.DataFrame:
    """Return the data frame and *also* writes it directly to xlsx in main().

    For testability the function only computes the payroll rows; the xlsx
    write (with merged headers + totals row + extra sheets) lives in
    `write_payroll_xlsx` below.
    """
    rows = []
    for _, emp in main_df.iterrows():
        plat = pd.to_numeric(emp.get("plat"), errors="coerce")
        if pd.isna(plat):
            plat = 50_000.0
        bonus = int(RNG.integers(0, 15_000))
        rows.append({
            "os_cislo": int(emp["employee_id"]),
            "jmeno_prijmeni": f"{str(emp['jmeno']).strip()} {str(emp['prijmeni']).strip()}",
            "oddeleni": emp["oddeleni"],
            "mzda_brutto": float(plat),
            "bonus": bonus,
            "mzda_celkem": float(plat) + bonus,
            "aktivni": "ano",
        })
    return pd.DataFrame(rows)


def apply_dirt_payroll(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # 8% of mzda_brutto off by 1-15%
    off_idx = RNG.choice(df.index, size=int(len(df) * 0.08), replace=False)
    for i in off_idx:
        delta = 1 + RNG.uniform(-0.15, 0.15)
        df.at[i, "mzda_brutto"] = round(df.at[i, "mzda_brutto"] * delta)
        df.at[i, "mzda_celkem"] = df.at[i, "mzda_brutto"] + df.at[i, "bonus"]

    # 30 rows where mzda_celkem != mzda_brutto + bonus
    bad_arith = RNG.choice(df.index, size=30, replace=False)
    for i in bad_arith:
        df.at[i, "mzda_celkem"] = df.at[i, "mzda_brutto"] + df.at[i, "bonus"] - int(RNG.integers(500, 3000))

    # 4 EUR-not-CZK landmines
    eur_idx = RNG.choice(df.index, size=4, replace=False)
    for i in eur_idx:
        df.at[i, "mzda_brutto"] = round(df.at[i, "mzda_brutto"] / 25)
        df.at[i, "bonus"] = round(df.at[i, "bonus"] / 25)
        df.at[i, "mzda_celkem"] = df.at[i, "mzda_brutto"] + df.at[i, "bonus"]

    # 5 English-language oddeleni values
    en_map = {"Vývoj": "Engineering", "Podpora": "Support", "Marketing": "Marketing",
              "Obchod": "Sales", "Finance": "Finance", "HR": "HR"}
    en_idx = RNG.choice(df.index, size=5, replace=False)
    for i in en_idx:
        cs = df.at[i, "oddeleni"]
        df.at[i, "oddeleni"] = en_map.get(cs, cs)

    # 3 plausible-wrong departments (rotate cs values)
    wrong_idx = RNG.choice(df.index, size=3, replace=False)
    rotation = ["Marketing", "Vývoj", "Obchod"]
    for k, i in enumerate(wrong_idx):
        df.at[i, "oddeleni"] = rotation[k]

    # `aktivni` mixed truthiness
    n = len(df)
    forms = ["ano", "Ano", "ANO", "y", "1", "true", ""]
    for k, form in enumerate(forms):
        m = max(5, n // (len(forms) * 6))
        sample_idx = RNG.choice(df.index, size=m, replace=False)
        df.loc[sample_idx, "aktivni"] = form

    return df


def write_payroll_xlsx(df: pd.DataFrame, path: Path) -> None:
    """Write payroll DF with 3 merged-header rows, totals row, and extra sheets."""
    import openpyxl
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Mzdy Q3 2025"
    # 3 merged-header artifact rows
    ws.append(["Mzdy zaměstnanců — Q3 2025", None, None, None, None, None, None])
    ws.append([None, None, None, None, None, None, None])
    ws.append(["DataCorp s.r.o. — interní použití", None, None, None, None, None, None])
    # Header row
    ws.append(list(df.columns))
    for r in df.itertuples(index=False):
        ws.append(list(r))
    # CELKEM totals row
    totals = ["CELKEM", None, None,
              float(df["mzda_brutto"].sum()), float(df["bonus"].sum()),
              float(df["mzda_celkem"].sum()), None]
    ws.append(totals)
    wb.create_sheet("List2")
    wb.create_sheet("List3")
    wb.save(path)
```

Wire into `main()`:
```python
    print("Building payroll xlsx...")
    payroll = build_payroll_xlsx(main_df_dirty)
    payroll = apply_dirt_payroll(payroll)
    write_payroll_xlsx(payroll, OUTPUT_DIR / "datacorp_payroll_q3.xlsx")
    print(f"  Payroll rows: {len(payroll)}")
```

- [ ] **Step 3: Tests + commit**

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp_payroll_q3.xlsx
git commit -m "generator: add datacorp_payroll_q3.xlsx with schema drift and EUR landmine"
```

---

## Task 10: Extend reviews — scale + sarcastic + wrong-person dirt

**Files:**
- Modify: `scripts/generate_datacorp.py` — `build_reviews`, new `apply_dirt_reviews`
- Modify: `tests/test_generate_datacorp.py`

- [ ] **Step 1: Failing test**

```python
def test_reviews_scaled_and_dirty() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_reviews.csv")
    assert 130 <= len(df) <= 180
    # Sarcasm signal: at least 3 reviews containing both *kreativní* and "deadlin"
    sarcastic = df["review_text"].str.contains(r"\*kreativní\*", regex=True, na=False).sum()
    assert sarcastic >= 3
```

- [ ] **Step 2: Scale `build_reviews`**

Inside the existing `build_reviews`, increase the per-employee selection probability so total rows land at ~150 instead of ~80. The simplest change: in whichever line picks the sample size, scale by the ratio of new headcount to old (1000 / 510 ≈ 2.0).

- [ ] **Step 3: Add `apply_dirt_reviews`**

```python
SARCASTIC_REVIEWS = [
    "Pan {prijmeni} je velmi *kreativní* s deadliny — vždy nás překvapí.",
    "Paní {prijmeni} přináší do týmu *unikátní* energii. Někdy příliš.",
    "S {jmeno_gen} {prijmeni_gen} je *radost* spolupracovat na složitých projektech.",
    "{jmeno} {prijmeni} má velmi *originální* přístup k procesům.",
    "{jmeno} je *neuvěřitelně* samostatný/á — kolegové se ho/ji téměř nedotknou.",
]


def apply_dirt_reviews(df: pd.DataFrame, main_df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # 5 sarcastic reviews — overwrite 5 random review_text values
    sarcastic_idx = RNG.choice(df.index, size=5, replace=False)
    for i in sarcastic_idx:
        emp = main_df[main_df["employee_id"] == df.at[i, "employee_id"]]
        if len(emp) == 0:
            jmeno, prijmeni = "Jan", "Novák"
        else:
            jmeno, prijmeni = str(emp.iloc[0]["jmeno"]), str(emp.iloc[0]["prijmeni"])
        tmpl = str(RNG.choice(SARCASTIC_REVIEWS))
        df.at[i, "review_text"] = tmpl.format(
            jmeno=jmeno, prijmeni=prijmeni,
            jmeno_gen=jmeno, prijmeni_gen=prijmeni,
        )

    # 3 wrong-person reviews — keep employee_id but replace the name in the text
    other = main_df.sample(3, random_state=SEED)
    wrong_idx = RNG.choice(df.index, size=3, replace=False)
    for k, i in enumerate(wrong_idx):
        ghost = other.iloc[k]
        df.at[i, "review_text"] = (
            f"{ghost['jmeno']} {ghost['prijmeni']} odvádí solidní práci, "
            f"ale rezervy jsou v komunikaci s týmem."
        )
    return df
```

- [ ] **Step 4: Wire + test + commit**

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp_reviews.csv
git commit -m "generator: scale reviews and plant sarcastic/wrong-person dirt"
```

---

## Task 11: Extend exit interviews — scale + mixed-language + self-contradiction

**Files:**
- Modify: `scripts/generate_datacorp.py`
- Modify: `tests/test_generate_datacorp.py`

- [ ] **Step 1: Failing test**

```python
def test_exit_interviews_scaled_and_dirty() -> None:
    df = pd.read_csv(NOTEBOOKS / "datacorp_exit_interviews.csv")
    assert 60 <= len(df) <= 90
    en_words = df["interview_text"].str.contains(
        r"\b(better|compensation|elsewhere|team|management|opportunity)\b",
        regex=True, na=False).sum()
    assert en_words >= 5
```

- [ ] **Step 2: Scale `build_exit_interviews`**

Similar to reviews — roughly double the per-employee inclusion rate so totals reach ~70.

- [ ] **Step 3: `apply_dirt_exit_interviews`**

```python
EN_FRAGMENTS = [
    " Hlavní důvod: better compensation elsewhere. Tým byl ok.",
    " Manager was nice, ale firma jako celek nepostupuje.",
    " I'm looking for better opportunity. Děkuji za vše.",
    " Tým, team dynamics, byl super, ale management nereaguje.",
    " Going for a senior role elsewhere — tady už nebyl prostor.",
]
CONTRADICTION = (
    "Platově jsem byl celkem spokojen, kolegové fajn. Odcházím hlavně kvůli "
    "tomu, že peníze už nejsou dostatečné a HR nedokázalo nic nabídnout."
)


def apply_dirt_exit_interviews(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    en_idx = RNG.choice(df.index, size=5, replace=False)
    for k, i in enumerate(en_idx):
        df.at[i, "interview_text"] = str(df.at[i, "interview_text"]) + EN_FRAGMENTS[k % len(EN_FRAGMENTS)]
    # 1 self-contradiction
    contra_idx = RNG.choice(df.index, size=1)
    df.loc[contra_idx, "interview_text"] = CONTRADICTION
    return df
```

- [ ] **Step 4: Wire + test + commit**

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py notebooks/datacorp_exit_interviews.csv
git commit -m "generator: scale exit interviews and plant mixed-language/contradiction dirt"
```

---

## Task 12: Orchestrator polish + README + final verification

**Files:**
- Modify: `scripts/generate_datacorp.py` — `main()` final form
- Modify: `tests/test_generate_datacorp.py` — add idempotency + survivorship checks
- Modify: `README.md`

- [ ] **Step 1: Final `main()` form**

Replace `main()` so its output is consistent and ordering is stable:

```python
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Building employee universe...")
    universe = build_main_df()
    universe = tag_departures(universe)
    print(f"  Universe: {len(universe)} ({universe['_departed'].sum()} departed)")

    main_df = universe[~universe["_departed"]].drop(columns=["_departed"]).copy()
    main_df_dirty = apply_dirt_main(main_df)
    universe_for_sides = universe.drop(columns=["_departed"]).copy()

    print("Building side-tables...")
    salary_history = apply_dirt_salary_history(
        build_salary_history(universe_for_sides), main_df_dirty,
    )
    org = build_org_chart(universe_for_sides)
    tickets = apply_dirt_tickets(build_tickets(universe_for_sides), universe_for_sides)
    payroll = apply_dirt_payroll(build_payroll_xlsx(main_df_dirty))
    reviews = apply_dirt_reviews(build_reviews(universe_for_sides), main_df_dirty)
    exits = apply_dirt_exit_interviews(build_exit_interviews(universe_for_sides))

    print("Writing files...")
    main_df_dirty.to_csv(OUTPUT_DIR / "datacorp.csv", index=False)
    reviews.to_csv(OUTPUT_DIR / "datacorp_reviews.csv", index=False)
    exits.to_csv(OUTPUT_DIR / "datacorp_exit_interviews.csv", index=False)
    salary_history.to_csv(OUTPUT_DIR / "datacorp_salary_history.csv", index=False)
    org.to_csv(OUTPUT_DIR / "datacorp_org_chart.csv", index=False)
    tickets.to_csv(OUTPUT_DIR / "datacorp_tickets.csv", index=False)
    write_payroll_xlsx(payroll, OUTPUT_DIR / "datacorp_payroll_q3.xlsx")

    # Smoke checks
    assert 990 <= len(main_df_dirty) <= 1030
    assert 2500 <= len(salary_history) <= 3600
    assert 1000 <= len(org) <= 1400
    assert 4500 <= len(tickets) <= 5500
    print("Done!")
```

- [ ] **Step 2: Idempotency + survivorship tests**

Append:

```python
def test_generator_is_deterministic(tmp_path) -> None:
    """Two consecutive runs produce byte-identical files."""
    import hashlib
    files = [
        "datacorp.csv", "datacorp_reviews.csv", "datacorp_exit_interviews.csv",
        "datacorp_salary_history.csv", "datacorp_org_chart.csv",
        "datacorp_tickets.csv", "datacorp_payroll_q3.xlsx",
    ]
    first = {f: hashlib.sha256((NOTEBOOKS / f).read_bytes()).hexdigest() for f in files}
    subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "generate_datacorp.py")], check=True)
    second = {f: hashlib.sha256((NOTEBOOKS / f).read_bytes()).hexdigest() for f in files}
    assert first == second


def test_survivorship_bias_present() -> None:
    main = pd.read_csv(NOTEBOOKS / "datacorp.csv")
    history = pd.read_csv(NOTEBOOKS / "datacorp_salary_history.csv")
    reviews = pd.read_csv(NOTEBOOKS / "datacorp_reviews.csv")
    exits = pd.read_csv(NOTEBOOKS / "datacorp_exit_interviews.csv")
    main_ids = set(main["employee_id"])
    ghosts_history = set(history["employee_id"]) - main_ids
    ghosts_reviews = set(reviews["employee_id"]) - main_ids
    ghosts_exits = set(exits["employee_id"]) - main_ids
    assert len(ghosts_history) >= 5
    assert len(ghosts_reviews) >= 1
    assert len(ghosts_exits) >= 1
```

- [ ] **Step 3: Update README**

In `README.md`, replace the existing Datasety table with:

```markdown
| Soubor | Obsah |
|--------|-------|
| `notebooks/datacorp.csv` | Hlavní strukturovaný dataset (~1000 řádků, 15 sloupců) — záměrně obsahuje chyby v datech |
| `notebooks/datacorp_reviews.csv` | Textové hodnocení výkonu (~150 záznamů) — nestrukturovaný text v češtině, některé záměrně sarkastické nebo přiřazené ke špatné osobě |
| `notebooks/datacorp_exit_interviews.csv` | Výstupní rozhovory (~70 záznamů) — nestrukturovaný text, místy v angličtině |
| `notebooks/datacorp_salary_history.csv` | Historie platových změn (~3000 řádků) — různé formáty datumů, občasné rozpory s hlavním datasetem |
| `notebooks/datacorp_org_chart.csv` | Organizační struktura (~1000+ řádků) — některé manažerské vazby tvoří cykly nebo míří na neexistující zaměstnance |
| `notebooks/datacorp_tickets.csv` | Interní IT/HR tickety (~5000 záznamů) — volný text, nekonzistentní kategorie, někdy špatná priorita |
| `notebooks/datacorp_payroll_q3.xlsx` | Mzdový list Q3 z Finance — Excel s nesourodým schématem, několika řádky v EUR a součtovým řádkem |
```

- [ ] **Step 4: Full test run**

Run: `uv run scripts/generate_datacorp.py`
Run: `uv run --group test pytest -v`
Expected: all PASS.

Manually verify `notebooks/datacorp_payroll_q3.xlsx` opens in a viewer (LibreOffice / Numbers) and that the merged-header rows and CELKEM row look as intended.

- [ ] **Step 5: Final commit**

```bash
git add scripts/generate_datacorp.py tests/test_generate_datacorp.py README.md notebooks/
git commit -m "generator: finalize orchestrator, README, and full regeneration"
```

---

## Self-review notes

- **Spec coverage:** All 24 listed dirt categories are produced by tasks 3, 5, 6, 8, 9, 10, 11. Survivorship bias (#24) is set up in task 2 (departure tagging) and verified in task 12.
- **Tests verify rates approximately**, not exactly. Tolerance bands (e.g. `990 <= len <= 1030`) absorb small RNG fluctuations from added/removed dirt rows.
- **Idempotency** is asserted explicitly in task 12. Re-running the script must produce byte-identical files.
- **The `aktivni` boolean-soup column** is created clean in `build_payroll_xlsx` and corrupted in `apply_dirt_payroll`.
- **`employee_id` collision (#14)** is implemented by reassigning donor rows to a different ID in `apply_dirt_salary_history`; this is destructive to the donor's history, but the task notes that explicitly.
