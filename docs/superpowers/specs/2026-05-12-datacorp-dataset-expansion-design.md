# DataCorp Dataset Expansion — Design

**Date:** 2026-05-12
**Scope:** Expand the synthetic DataCorp s.r.o. dataset used by `notebooks/assignment-03c.ipynb` so it is meaningfully deeper (more linked files) and meaningfully messier (more realistic data-quality problems). Single regeneration script (`scripts/generate_datacorp.py`) remains the one source of truth.

Assignment notebook changes are explicitly out of scope and will be decided in a follow-up once the new data exists.

## Goals

- **More depth:** add side tables enabling joins, time series, hierarchies, and Excel-format quirks.
- **More mess:** plant realistic data-quality issues that reward careful work and punish naïve pipelines, calibrated to a Czechitas-course difficulty.
- **Preserve the existing pedagogical surface:** main HR table + reviews + exit interviews remain the entry point; new files extend rather than replace.

## File inventory (after this work)

| File | Status | Approx rows | Purpose |
|---|---|---|---|
| `notebooks/datacorp.csv` | expanded | ~1000 | Main HR table; +1 column (`telefon`); broader dirt |
| `notebooks/datacorp_reviews.csv` | expanded | ~150 | Performance reviews (Czech free-text); scales with headcount; adds sarcastic / wrong-person / mixed-language variants |
| `notebooks/datacorp_exit_interviews.csv` | expanded | ~70 | Exit interviews (Czech free-text); adds at least one self-contradicting interview |
| `notebooks/datacorp_salary_history.csv` | **new** | ~3000 | One row per salary event per employee |
| `notebooks/datacorp_org_chart.csv` | **new** | ~1000 | Employee → manager mapping with effective-from dates |
| `notebooks/datacorp_tickets.csv` | **new** | ~5000 | Internal IT/HR ticket export with free-text descriptions |
| `notebooks/datacorp_payroll_q3.xlsx` | **new** | ~1000 + cruft | Finance's quarterly payroll in Excel format with schema drift |

All files are written to `notebooks/`. The existing three files are overwritten in place when the script is re-run.

## Schemas

### `datacorp.csv` (extended)

Existing 14 columns: `employee_id, jmeno, prijmeni, email, oddeleni, pozice, datum_nastupu, plat, hodnoceni_vykonu, vzdelani, mesto, vek, pohlavi, typ_uvazku`.

**New column:**
- `telefon` (string): Czech mobile numbers. Three formats planted intentionally (`+420 123 456 789`, `123456789`, `123 456 789`). ~20 missing, ~5 obviously invalid (`"???"`, `"viz Slack"`).

### `datacorp_salary_history.csv`

| Column | Type | Notes |
|---|---|---|
| `employee_id` | int | Mostly valid; some IDs reference employees no longer in `datacorp.csv` |
| `datum_zmeny` | string | Mixed formats: ISO `2024-03-15`, Czech `15.03.2024`, US `03/15/2024`, year-only `"2023"` |
| `plat_pred` | numeric/string | Salary before change. Some rows use comma decimal + non-breaking space (`"45 000,50"`) |
| `plat_po` | numeric/string | Salary after change |
| `duvod` | string | One of: `raise`, `promotion`, `correction`, `acquisition_harmonization` |

Each employee has 1–6 rows. Generated chronologically per employee, then re-shuffled at file level.

### `datacorp_org_chart.csv`

| Column | Type | Notes |
|---|---|---|
| `employee_id` | int | |
| `manager_id` | int / blank | Blank for department heads |
| `platnost_od` | string (ISO) | When this reporting line became effective |

Most employees: one row. ~20%: 2–3 rows (manager changed during tenure). Some `manager_id` values reference employees who've left the company.

### `datacorp_tickets.csv`

| Column | Type | Notes |
|---|---|---|
| `ticket_id` | int | Unique |
| `reporter_id` | string | Mostly valid `employee_id`; ~50 invalid; ~10 stored as `"234."` or `" 234"` |
| `datum` | string | Mostly `YYYY-MM-DD HH:MM:SS`; ~10% with timezone offset |
| `kategorie` | string | Dirty taxonomy: ~7 surface forms collapsing to ~4 real categories (e.g., `"HW"`, `"Hardware"`, `"hardware-other"`, `"hw / sw"`, `"HARDWARE"`) |
| `priorita` | string | `P1`–`P4`. ~40% mismatched against `popis` content |
| `status` | string | `open`, `closed`, `pending` |
| `popis` | string | Czech free-text, 1–4 sentences. Tone ranges neutral → frustrated. Some reference colleagues by name |

### `datacorp_payroll_q3.xlsx`

Sheet name: `"Mzdy Q3 2025"` (Czech with diacritics). Two additional empty template sheets (`List2`, `List3`) included to mimic a real Excel export.

Top 3 rows of the main sheet are merged-header artifacts (mostly NaN). Bottom row is a `"CELKEM"` totals row.

| Column | Type | Notes |
|---|---|---|
| `os_cislo` | int | Renamed `employee_id`; students must figure out the join key |
| `jmeno_prijmeni` | string | Single combined name column |
| `oddeleni` | string | Mostly Czech; 5 rows in English (`"Engineering"` instead of `"Vývoj"`, etc.) |
| `mzda_brutto` | numeric | Matches main `plat` for ~92%; off by 1–15% for the rest |
| `bonus` | numeric | Per-quarter bonus |
| `mzda_celkem` | numeric | ≠ `mzda_brutto + bonus` for ~30 rows |
| `aktivni` | string | Mixed truthiness: `"ano"`, `"Ano"`, `"ANO"`, `"y"`, `"1"`, `"true"`, `""` |

A handful of `mzda_brutto` values are clearly EUR (~1800–3500), not CZK. No currency column.

## Cross-file relationships (intentional conflicts)

The dataset's central pedagogical move is that no single file is fully trustworthy. Conflicts are planted so students learn to reconcile, not just join.

**Salary history ↔ main `plat`:**
- ~85% of employees: `plat_po` of the latest history row matches main `plat` exactly.
- ~10%: off by 1–5k CZK (one system not updated).
- ~5%: most-recent history row is *higher* than `plat` (approved raise not yet propagated).
- ~3%: history rows exist but `plat` is NaN in the main table.
- 5 employees have salary_history rows but do not appear in `datacorp.csv` (departed).

**Org chart ↔ main:**
- ~80% of employees: exactly one row (`platnost_od` = hire date).
- ~20%: 2–3 rows reflecting manager changes.
- 3 small cycles planted (A → B → A) to teach hierarchy validation.
- ~15 `manager_id` values reference employees not in `datacorp.csv`.

**Tickets ↔ main:**
- `reporter_id` is mostly valid; ~50 invalid (contractors, ex-employees, typos).
- `kategorie` taxonomy mismatch noted above.
- `priorita` deliberately disagrees with `popis` content ~40% of the time.

**Payroll xlsx ↔ main:**
- Joins on `os_cislo` = `employee_id` (renamed).
- `oddeleni` drift (5 English values).
- `mzda_brutto` ≠ main `plat` for ~8% of rows.
- 4 rows in EUR (no currency column).
- Top merged-header rows and bottom `"CELKEM"` row must be filtered.

## Planted dirt catalog

Existing six categories of dirt (kept as-is): mixed-case `oddeleni`, missing `plat` skewed to Podpora, mixed date formats, salary outliers in low-salary departments, duplicate rows, invalid `hodnoceni_vykonu` values (0 or 6).

**New additive categories (across all files):**

7. **Phone-number formats and invalids** — `telefon` column in `datacorp.csv`.
8. **Email / name mismatch from rehires** — ~15 rows where `employee_id` was reused but `email` reflects the previous holder.
9. **Whitespace and embedded newlines** — ~30 name rows with leading/trailing spaces; 5 review texts with `\n\n` and double-space runs.
10. **Encoding mojibake** — 3 rows where Czech diacritics have been mangled (e.g., `Č` → `Ä`).
11. **Decimal separator mixing** — ~10% of `plat_po` in salary history uses Czech comma decimals with non-breaking spaces.
12. **Date format soup** — ISO, Czech, US, and year-only formats coexisting in salary history.
13. **Trailing punctuation / leading whitespace in IDs** — ~10 `reporter_id` values like `"234."` or `" 234"`.

**"Mean" additions accepted (additional traps with high pedagogical value):**

14. **Silent ID collision across files** — one `employee_id` reused for two genuinely different people in salary history (predecessor left in 2019, current holder hired 2022). Naïve aggregations silently combine them.
15. **Diacritic-folded duplicate identities** — two distinct rows for `"Petr Černý"` and `"Petr Cerny"` (different IDs, same human re-onboarded after a sanitization step); salary history split across both.
16. **Hire dates in the future** — ~5 rows with `datum_nastupu` in 2027 (data-entry typo). Breaks tenure statistics.
17. **Salary history out of chronological order** — 1 employee has a backdated correction row whose `datum_zmeny` precedes the previous raise; chronological sort shows a phantom pay cut.
18. **Plausible-but-wrong departments** — 3 employees listed under different `oddeleni` in payroll vs main HR table; neither is provably wrong without external info.
19. **Currency landmine in payroll** — 4 `mzda_brutto` values are obviously EUR, not CZK; no currency column to signal it.
20. **Sarcastic / euphemistic reviews** — 5 performance reviews that read positive but are obviously bitter to a human reader (e.g., *"Pan Novák je velmi kreativní s deadliny."*).
21. **Wrong-person reviews** — 3 reviews where the body text names a different employee than the row's `employee_id` (copy-paste mistake by a manager).
22. **Mixed-language exit interviews** — ~5 exit interviews partially in English mixed with Czech.
23. **Self-contradicting exit interview** — 1 interview that explicitly contradicts itself on the reason for leaving.
24. **Survivorship bias setup** — departed employees are absent from `datacorp.csv` but present in salary history, reviews, and exit interviews. "Average salary by department" silently excludes them, biasing results upward in high-turnover departments.

Ideas considered during brainstorming but **not** accepted into this iteration are kept in the companion parking-lot file (zero-width chars, two-digit years, locale-poisoned `plat`, PII leakage in tickets, attendance/leave/projects files, the "DataSub acquisition" scenario, etc.) so they can be picked up cheaply in a future revision.

## Code structure

`scripts/generate_datacorp.py` is restructured to:

```
Constants (name banks, cities, departments — existing)
build_main_df()                  # existing generate_employees() renamed
build_salary_history(df)         # new — references main_df IDs
build_org_chart(df)              # new
build_tickets(df)                # new
build_payroll_xlsx(df)           # new — writes xlsx directly
build_reviews(df)                # existing, extended scale + mean variants
build_exit_interviews(df)        # existing, extended scale + self-contradiction
apply_dirt_main(df)              # existing apply_dirt renamed
apply_dirt_salary_history(df)    # new
apply_dirt_org_chart(df)         # new
apply_dirt_tickets(df)           # new
apply_dirt_payroll(df)           # new
apply_dirt_reviews(df)           # new — sarcastic, wrong-person, mixed-language
apply_dirt_exit_interviews(df)   # new — self-contradiction
main()                           # orchestrates, writes 7 files
```

`build_*` functions return clean DataFrames. `apply_dirt_*` functions take a clean DataFrame and return a dirty one — same separation as today's `apply_dirt`. This keeps each function readable and lets a maintainer reason about generation logic separately from corruption logic.

## Determinism

The existing `SEED = 42` and module-level `RNG = np.random.default_rng(SEED)` continue to drive all randomness. Re-running `uv run scripts/generate_datacorp.py` produces byte-identical output. Where ordering is randomized (final `sample(frac=1)` shuffles), it uses the same seed.

## Dependencies

- Add `openpyxl` via `uv add openpyxl` to enable `DataFrame.to_excel(...)` for the payroll file.
- No other new runtime dependencies.

## Out of scope

- Modifications to `assignment-03c.ipynb` (or `03`, `03b`). Locked for a separate decision after the dataset exists.
- Slide updates.
- A canonical "answer key" notebook showing the expected cleanup.
- Per-file unit tests on the generator — light smoke checks in `main()` (row counts within tolerance) are sufficient.

## Deliverables

- Extended `scripts/generate_datacorp.py` producing 7 files.
- `pyproject.toml` + `uv.lock` updated for `openpyxl`.
- `README.md` "Datasety" table extended with the four new files (one-line descriptions each).
- All 7 files regenerated and committed under `notebooks/`.
- This design doc.
- Parking-lot companion file: `docs/superpowers/specs/2026-05-12-datacorp-dataset-expansion-parking-lot.md`.

## Success criteria

- `uv run scripts/generate_datacorp.py` runs to completion in under 10 seconds and writes 7 files into `notebooks/`.
- Re-running the script produces byte-identical files.
- Each cross-file conflict rate listed above falls within ±2 percentage points of its target (verified by smoke checks in `main()`).
- Existing `assignment-03c.ipynb` can still be executed without modification against the new files (the three existing CSVs retain their schemas; only row counts and dirt density change).
