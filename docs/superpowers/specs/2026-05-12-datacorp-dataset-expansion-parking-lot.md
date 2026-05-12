# DataCorp Dataset Expansion — Parking Lot

**Date:** 2026-05-12
**Companion to:** `2026-05-12-datacorp-dataset-expansion-design.md`

Ideas that came up during brainstorming but were **not** accepted into the current design. Kept here so future revisions can reach for them without rediscovering them from scratch. Each entry lists the idea, why it was rejected for this iteration, and a sketch of how to implement it later.

## Dirt ideas considered and parked

### Zero-width characters in IDs
A handful of `employee_id` values in salary history contain a zero-width space (`​`) — invisible in any viewer but breaks string joins.
**Why parked:** Produces frustration without teaching a generalizable skill. Students will either google the answer or give up. Reserve for a much more advanced cohort.
**Future implementation:** Inject `​` into ~5 ID strings in `apply_dirt_salary_history`. Document the trap in a "hard mode" supplement.

### Two-digit years in dates
Dates like `15.03.24` — ambiguous between 1924 and 2024. Pandas defaults vary by version and locale.
**Why parked:** Real but rare; pedagogical payoff is low compared to the four date-format mixing already in the spec (items 12 in the design's dirt catalog).
**Future implementation:** Add a 5th format to the salary-history date soup. Two-digit-year rows should distribute across plausible decades to make the trap visible.

### Timezone-naïve datetimes mixed with timezone-aware ones
~10% of ticket `datum` values with timezone offsets (`+02:00`), the rest naïve.
**Why parked:** Adds parsing pain without an analytical lesson at this course's level; pandas datetime tz handling is itself a deep topic.
**Future implementation:** Append `+02:00` or `+01:00` (mixed CET/CEST) to 10% of ticket `datum` strings in `apply_dirt_tickets`. Students would need `pd.to_datetime(..., utc=True)` to handle cleanly.

### Locale-poisoned `plat` column in `datacorp.csv`
A *few* `plat` values exported with Czech locale (`"55 000,00"` with non-breaking space) — one such row turns the entire `plat` column into object dtype, breaking everything downstream.
**Why parked:** Too punishing for a single bad row to ruin every analysis. Already represented less aggressively in salary history (item 11 of the dirt catalog) where the blast radius is smaller.
**Future implementation:** Plant 2–3 such values in `apply_dirt_main`. Pair with a "why is `plat.mean()` failing?" hint in the assignment.

### Boolean-ish strings
Mixed truthiness column (`aktivni`) with values like `"ano"`, `"Ano"`, `"ANO"`, `"y"`, `"1"`, `"true"`, `""`.
**Status:** **Accepted** in the current design (column `aktivni` in `datacorp_payroll_q3.xlsx`). Documented here for completeness with the original brainstorm set.

### Bonus eaten by the salary (payroll arithmetic disagreement)
`mzda_celkem` ≠ `mzda_brutto + bonus` for some rows, no comment.
**Status:** **Accepted** in the current design.

### PII leakage in tickets
2 ticket descriptions containing what looks like a colleague's salary or a password — realistic privacy hazard.
**Why parked:** Real but raises pedagogical questions outside the scope of "structured outputs": data handling and PII redaction would deserve its own lesson rather than being smuggled in as a trap.
**Future implementation:** Add 2 ticket `popis` entries with embedded "salary disclosure" or "password" text. Pair with an explicit assignment task: "What do you do with this?" Belongs in a later course iteration that covers data ethics.

### Leading-zero ID stripping
Tickets with reporter_id as `"007"`, `"042"`. `pd.read_csv` without `dtype=str` turns them into `7`, `42` and joins fail.
**Why parked:** Already covered by item 13 (trailing punctuation, leading whitespace in IDs) in the design's dirt catalog, which forces the same defensive habit.
**Future implementation:** Replace ~5 short integer IDs in `apply_dirt_tickets` with zero-padded strings.

## File ideas considered and parked

### Attendance / timekeeping log
Daily punch-in/punch-out per employee. ~250 rows × ~1000 employees = ~250k rows.
**Why parked:** Massive in size, low per-row information density, repetitive cleanup work. Pedagogical payoff doesn't justify the bulk.
**Future implementation:** `datacorp_attendance.csv` with `employee_id, datum, prichod, odchod, hodiny`. Realistic dirt: forgotten clock-outs (NaN), 23:59 clock-outs (system auto-close), holidays mixed in.

### 1:1 meeting notes
A third Czech free-text source of manager↔report private conversations.
**Why parked:** Redundant with reviews and exit interviews for the structured-outputs lesson. Adds review fatigue without adding a new analytical skill.
**Future implementation:** `datacorp_one_on_ones.csv` with `employee_id, datum, manager_id, poznamky`. Could pair with org_chart to validate manager_id consistency.

### Project assignments (many-to-many)
Employees ↔ projects with `% allocation`, start/end dates, skill tags.
**Why parked:** M:N joins are a tangent from the AI-in-analytics theme of the course. Better suited to a SQL or pandas-focused course.
**Future implementation:** `datacorp_project_assignments.csv` with `employee_id, project_id, alokace_pct, datum_od, datum_do` plus a separate `datacorp_projects.csv` lookup. Natural dirt: rows summing to >100% allocation per employee.

### Leave / PTO log
Per-employee leave requests, types, approval status.
**Why parked:** Similar profile to attendance — bulk without pedagogical density.
**Future implementation:** `datacorp_leave.csv` with `employee_id, datum_od, datum_do, typ, schvaleno`. Dirt: overlapping leaves, leaves spanning year boundaries, manager-rejected requests still showing as "approved" in some rows.

## Larger structural ideas parked

### "DataCorp acquired DataSub a.s." entity-resolution scenario
A second parallel HR system to reconcile against DataCorp's: different schemas, English column names, EUR salaries, different department taxonomy, some people appearing in both with subtle differences.
**Why parked:** Was presented as Option B during brainstorming; user chose A+C instead. Strong fit for a future course iteration that wants to teach LLM-assisted entity resolution and fuzzy matching as primary skills.
**Future implementation:** Add `notebooks/datasub_*.csv` files generated from a parallel set of name banks and department names. Plant overlap on ~10% of identities with subtle differences. Add an "integration spreadsheet" with a partially-filled mapping and one wrong mapping.
