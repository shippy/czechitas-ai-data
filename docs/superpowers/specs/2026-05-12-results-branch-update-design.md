# Results Branch Update — Design

**Date:** 2026-05-12
**Scope:** Bring the `results` branch up to date with `main` after the dataset expansion (PR #1) and assignment-03c Úkol 4 (PR #2) merges. Fill in canonical solutions for the new task 4 cells. Refresh the instructor answer key to cover the 18 new planted-dirt categories and Úkol 4 expected behavior.

## Background

The `results` branch holds instructor-facing materials:
- Solved versions of `assignment-03c.ipynb` (currently tasks 1–3 only)
- `notebooks/datacorp-answer-key.md` (instructor-only — does not exist on `main`)
- Solution notebooks for the deprecated `assignment-03.ipynb` / `assignment-03b.ipynb` (out of scope here)

`results` currently lags `main` — it doesn't yet have the dataset expansion or the Úkol 4 student cells. This work syncs it and lays solutions on top.

## Goals

- Bring `results` to the same baseline as `main`.
- Preserve the existing solved cells for tasks 1–3 — they took deliberate work and should not be lost in the merge.
- Provide canonical solutions for the two empty Úkol 4 cells (load xlsx + analyze).
- Refresh `datacorp-answer-key.md` to be a useful instructor reference for the expanded dataset.

## Out of scope

- Re-executing the notebook to commit cell outputs (would cost API calls and is not how `results` has historically stored notebooks).
- Updating the deprecated `assignment-03-solution.ipynb` / `assignment-03b-solution.ipynb`.
- Refreshing slides.
- Updating the Custom GPT helper.
- Opening a PR for `results` — historically it lives as its own long-lived branch.

## Architecture

Three sequential commits on `results`:

### Commit 1 — merge `main` into `results`, resolve notebook conflict

`git merge main` will produce a conflict on `notebooks/assignment-03c.ipynb` (both sides changed it). Other files merge cleanly:
- `notebooks/datacorp.csv`, `_reviews.csv`, `_exit_interviews.csv` — take `main`'s versions (the regenerated, expanded dataset).
- `notebooks/datacorp_payroll_q3.xlsx`, `_salary_history.csv`, `_org_chart.csv`, `_tickets.csv` — take from `main` (new files).
- `scripts/generate_datacorp.py`, `tests/`, `pyproject.toml`, `uv.lock`, `README.md`, `docs/superpowers/` — take from `main`.

For the notebook conflict, resolve manually with a Python script that reads both sides and stitches:

| Cells | Source |
|---|---|
| 0–10 (intro, setup, Úkoly 1 intro+example) | identical on both — either side |
| 11 (Úkol 1 starter / solution) | **`results`** — keep the solved version |
| 12 (Úkol 2 markdown) | identical |
| 13 (Úkol 2 solution) | **`results`** |
| 14 (Úkol 3 markdown) | identical |
| 15 (Úkol 3 solution) | **`results`** |
| 16–22 (Úkol 4 — intro, 4a, sample, model, LLM call, analyze, discussion) | **`main`** — new cells |
| 23–24 (Bonus) | identical |

The script reads both versions (results' tip and main's tip), validates the expected cell-by-cell origin, and writes the merged notebook. Then `git add` and `git commit -m` to finalize the merge.

### Commit 2 — fill in Úkol 4 canonical solutions

Replace cell 17 (empty `payroll = ...` starter) with:

```python
payroll = pd.read_excel(
    "datacorp_payroll_q3.xlsx",
    sheet_name="Mzdy Q3 2025",
    skiprows=3,
)
payroll = payroll[payroll["os_cislo"].apply(lambda x: str(x).replace(".0", "").isdigit())]
payroll["os_cislo"] = payroll["os_cislo"].astype(int)
print(f"Payroll rows after cleanup: {len(payroll)}")
payroll.head()
```

Replace cell 21 (TODO comments) with:

```python
# 1. Distribuce závažnosti
zavaznosti = payroll_sample["verdikt"].apply(lambda v: v.zavaznost.value)
print(zavaznosti.value_counts())

# 2. Vážné případy
vazne = payroll_sample[zavaznosti == "vážná"]
for _, r in vazne.iterrows():
    print(f"os_cislo={r['os_cislo']}  oddeleni(payroll)={r['oddeleni']}  mzda_brutto={r['mzda_brutto']}")
    for n in r["verdikt"].nesoulady:
        print(f"  - {n.pole}: HR={n.hodnota_hr!r} vs Payroll={n.hodnota_payroll!r} ({n.pravdepodobna_pricina})")

# 3. Ground-truth check — full dataset má 4 EUR + 3 wrong-dept rows
hr_dept = dict(zip(datacorp["employee_id"], datacorp["oddeleni"]))
cs_depts = {"Vývoj", "Marketing", "Obchod", "Podpora", "Finance", "HR"}
eur_in_sample = ((payroll_sample["mzda_brutto"] >= 1500) & (payroll_sample["mzda_brutto"] <= 4000)).sum()
wrong_in_sample = sum(
    1 for _, r in payroll_sample.iterrows()
    if hr_dept.get(r["os_cislo"]) is not None
    and r["oddeleni"] != hr_dept[r["os_cislo"]]
    and r["oddeleni"] in cs_depts
)
print(f"Ve vzorku: {eur_in_sample} EUR-řádků, {wrong_in_sample} wrong-dept řádků.")
print(f"LLM označil jako 'vážná': {(zavaznosti == 'vážná').sum()}")
```

### Commit 3 — refresh `notebooks/datacorp-answer-key.md`

The current file documents the 6 original dirt categories + analytical signals. Extend it without rewriting the existing content.

Existing top section ("Záměrně zasazené problémy v datech") — bump counts to reflect ~1011 rows where applicable. Specific changes:

- `Nekonzistentní oddeleni` row: from `"Marketing" (51×), "marketing" (15×), "Mktg" (5×)` to whatever the regenerated dataset shows. Implementer to verify with a one-liner.
- `Chybějící plat`: from `40 celkem, z toho 25 v Podpoře` to the actual counts.
- `Smíšené formáty datumů`: update counts.
- `Duplicitní řádky`: count is still ~10.
- `Neplatné hodnoceni_vykonu`: still 5–8.

Then add a new section **Další záměrně zasazené problémy (rozšíření 2026-05)** with one row per new dirt category, in the same `Problém | Detail | Jak ověřit` table format. New categories to document (numbered to match the dataset-expansion design doc):

7. Telefonní formáty (3 varianty + ~20 NaN + 5 neplatných)
8. Email/jméno nesoulad (~15 řádků, "duchové" z reonboardingu)
9. Mezery a nové řádky ve jménech (~30 řádků)
10. Encoding mojibake (3 řádky, `Č`→`Ä` apod.)
11. Smíchané desetinné oddělovače v `salary_history.plat_po` (~10%)
12. Datumová polévka v `salary_history.datum_zmeny` (ISO/Czech/US/year-only)
13. Tečky a mezery v `tickets.reporter_id`
14. Silent ID collision v salary history (1 záměrná kolize)
15. Diakritika-složené duplikáty identit (1 plánovaná dvojice)
16. Datumy nástupu v budoucnosti (5 řádků, 2027–2028)
17. Backdated correction v salary_history (out-of-order datum)
18. Plausible-wrong departments v payroll (3 řádky)
19. EUR currency landmine v payroll (4 řádky)
20. Sarkastické reviews (5 řádků s `*kreativní*` apod.)
21. Wrong-person reviews (3 řádky)
22. Mixed-language exit interviews (5 fragmentů)
23. Self-contradicting exit interview (1 řádek)
24. Survivorship bias — ~15 zaměstnanců odešlo, jsou v side-tables ale ne v `datacorp.csv`

Then add **Úkol 4 — očekávané výsledky** section:

- Plný dataset: 4 řádky v EUR (mzda_brutto ∈ [1500, 4000]) + 3 řádky se špatným oddělením.
- Vzorek (`random_state=5`): 1 EUR řádek + 1 wrong-dept řádek (zaměstnanec 498: payroll=Vývoj, HR=Obchod).
- LLM (gpt-5.4-mini) by měl označit oba jako `vážná`. Často také označí jako `střední` nebo `vážná` řádky s `mzda_celkem ≠ mzda_brutto + bonus` (30 takových v plném datasetu, ~1–2 ve vzorku).
- Bez nápovědy o rozsahu CZK v system promptu se přesnost na EUR landmines výrazně sníží — to je předmět diskusní otázky 2.

## Implementation hints

- Use a small Python script for the merge resolution. Write the merged JSON deterministically (json.dumps with `indent=1, ensure_ascii=False`) so future diffs stay readable.
- Run the cell-by-cell origin validation script BEFORE writing the merged file — bail with an error if either side's cell layout doesn't match expectations.
- Don't use `git mergetool` — manual JSON stitching is cleaner.
- After commit 1, validate the notebook parses (`python -c "import json; json.load(...)"`) before moving on.
- After commit 2, eyeball cells 17 and 21 to make sure the solutions read correctly.
- After commit 3, eyeball the answer key — counts should match what the regenerated dataset actually has.

## Deliverables

- Three commits on `results` branch as described.
- `git push origin results`. No PR — `results` is a long-lived parallel branch.

## Success criteria

- `git log results` shows three new commits beyond the merged baseline.
- `notebooks/assignment-03c.ipynb` on results has solved cells for Úkoly 1, 2, 3, 4 (cells 11, 13, 15, 17, 21) and the same Úkol 4 student-facing scaffolding (cells 16, 18, 19, 20, 22) as on main.
- `notebooks/datacorp-answer-key.md` documents 24 dirt categories (6 original + 18 new) and an "Úkol 4 — očekávané výsledky" section.
- The notebook parses as valid JSON.
- No regression on `main` — this work only touches `results`.
