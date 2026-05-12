# Assignment-03c Task 4 — Design

**Date:** 2026-05-12
**Scope:** Add a fourth task to `notebooks/assignment-03c.ipynb` that uses structured outputs over the new `datacorp_payroll_q3.xlsx` file to reconcile finance's quarterly payroll against the main HR record. Existing tasks 1–3 stay intact.

This is the natural follow-up to the dataset expansion specced in `2026-05-12-datacorp-dataset-expansion-design.md`. The earlier expansion deferred assignment changes; this design picks them up.

## Goals

- **Exercise the new payroll xlsx file.** It is the most pedagogically rich of the four new files (Excel quirks + currency landmine + schema drift + arithmetic errors).
- **Keep structured outputs as the notebook's spine.** Task 4 applies the LLM as a *reconciliation judge*, not a text extractor — same Pydantic-driven pattern, new domain.
- **Stay within today's notebook arc.** No changes to tasks 1–3; no new helper modules; no fundamental restructuring.

## Student-facing flow

The new section slots into `notebooks/assignment-03c.ipynb` between the existing "Úkol 3" cells and the "Bonusový úkol" cell.

### Sub-step 4a — Load the xlsx

A markdown cell explains: Finance sent a Q3 payroll spreadsheet. It opens in Excel just fine, but `pd.read_excel` will trip on merged header rows and a totals line. Students are asked to load `datacorp_payroll_q3.xlsx` (sheet `Mzdy Q3 2025`) and produce a clean DataFrame.

Expected solution shape:

```python
payroll = pd.read_excel(
    "datacorp_payroll_q3.xlsx",
    sheet_name="Mzdy Q3 2025",
    skiprows=3,
)
payroll = payroll[payroll["os_cislo"].apply(lambda x: str(x).replace(".0", "").isdigit())]
payroll["os_cislo"] = payroll["os_cislo"].astype(int)
```

Hint text in the surrounding markdown calls out: "horní 3 řádky jsou hlavičkové artefakty, a poslední řádek je `CELKEM`".

### Sub-step 4b — Sample 50 rows with a known seed

A pre-filled code cell:

```python
payroll_sample = payroll.sample(50, random_state=42).reset_index(drop=True)
print(f"Sampled {len(payroll_sample)} payroll rows for LLM reconciliation.")
```

A short comment explains that `random_state=42` is deliberately fixed so the assignment surfaces a known number of EUR-currency landmines and wrong-department rows. The exact `random_state` value will be validated during implementation (see Pre-flight Verification below) and may be adjusted if 42 produces fewer than 1 of each anomaly type.

### Sub-step 4c — Pydantic reconciliation model

Pre-filled in a code cell:

```python
from enum import Enum
from pydantic import BaseModel, Field


class Zavaznost(str, Enum):
    OK = "ok"
    DROBNA = "drobná"
    STREDNI = "střední"
    VAZNA = "vážná"


class Nesoulad(BaseModel):
    pole: str = Field(description="Název pole, ve kterém je nesoulad (např. 'oddeleni', 'mzda_brutto').")
    hodnota_hr: str
    hodnota_payroll: str
    pravdepodobna_pricina: str = Field(description="Stručné vysvětlení, proč nesoulad nejspíš vznikl.")


class Verdikt(BaseModel):
    stejna_osoba: bool = Field(description="Týkají se obě řádky téhož zaměstnance?")
    nesoulady: list[Nesoulad]
    zavaznost: Zavaznost
    doporuceni: str = Field(description="Jedna věta — co s tím udělat.")
```

We deliberately do *not* ask students to write this model from scratch — task 2 already had them define one. The lesson here is in *using* a nested Pydantic + Enum model in a non-trivial domain.

### Sub-step 4c — LLM call

Pre-filled scaffolding:

```python
async def reconcile_row(payroll_row: pd.Series, hr_row: pd.Series) -> Verdikt:
    user_block = (
        f"HR záznam (zdroj: datacorp.csv, plat v CZK):\n"
        f"  employee_id={hr_row['employee_id']} jmeno={hr_row['jmeno']} prijmeni={hr_row['prijmeni']} "
        f"oddeleni={hr_row['oddeleni']} plat={hr_row['plat']}\n\n"
        f"Mzdový záznam (zdroj: datacorp_payroll_q3.xlsx):\n"
        f"  os_cislo={payroll_row['os_cislo']} jmeno_prijmeni={payroll_row['jmeno_prijmeni']} "
        f"oddeleni={payroll_row['oddeleni']} mzda_brutto={payroll_row['mzda_brutto']} "
        f"bonus={payroll_row['bonus']} mzda_celkem={payroll_row['mzda_celkem']} "
        f"aktivni={payroll_row['aktivni']}"
    )
    async with SEM:
        return await async_client.create(
            messages=[
                {"role": "system", "content": (
                    "Jsi pomocný auditor. Porovnáš dva záznamy o jednom zaměstnanci ze dvou systémů "
                    "(HR a mzdové oddělení) a vrátíš strukturovaný verdikt. Mzdy v CZK obvykle spadají "
                    "do rozsahu 25 000 – 150 000. Pokud vidíš číslo mimo tento rozsah, zvaž, jestli "
                    "není v jiné měně."
                )},
                {"role": "user", "content": user_block},
            ],
            response_model=Verdikt,
        )


merged = payroll_sample.merge(
    datacorp, left_on="os_cislo", right_on="employee_id", how="left",
)
verdicts = await asyncio.gather(*[
    reconcile_row(payroll_sample.loc[i], merged.loc[i])
    for i in payroll_sample.index
])
payroll_sample["verdikt"] = verdicts
```

The CZK-range hint in the system prompt is deliberate — it nudges the LLM toward catching the EUR landmine. The bonus task at the end of the notebook will encourage students to try removing this hint and observe the effect.

### Sub-step 4d — Analyze

Empty starter cell with TODO comments:

```python
# 1. Spočítejte: kolik verdiktů má každou hodnotu Zavaznost? (.value_counts na .zavaznost)
# 2. Vypište řádky, kde LLM označil verdict jako 'vážná'. Co je v nich za anomálii?
# 3. V plném datasetu (před samplem) jsou 4 řádky v EUR a 3 plausible-wrong-department řádky.
#    Kolik z nich se trefilo do našeho 50-řádkového samplu? Kolik jich LLM odhalil?
```

### Markdown — diskusní otázky

A final markdown cell with 3 reflection questions (no code):

1. Které chyby LLM odhalí spolehlivě, a které ne? Proč?
2. Co by se stalo, kdyby system prompt neobsahoval nápovědu o rozsahu CZK?
3. Jak by se dala metoda škálovat na celý dataset (1000 řádků) bez zbytečného plýtvání tokeny?

## Pydantic model — pedagogical rationale

The `Verdikt` model is meaningfully richer than today's `ExitReason` (4 flat fields):

- **Nested list of objects** (`nesoulady: list[Nesoulad]`) — first time in the notebook a model contains a sub-model collection.
- **Enum-typed field** (`zavaznost: Zavaznost`) — students see `enum.Enum` used as a Pydantic type, complementing `Literal[...]` from task 2.
- **Field descriptions on every non-trivial field** — reinforces the bonus-task hint about `Field(description=...)`.

Students who copy the model verbatim still learn from reading it. Students who customize it for the bonus task have a richer starting point.

## Setup-cell changes

The notebook's first code cell currently downloads three CSVs on Colab. Add a fourth download for the xlsx and add `openpyxl` to the pip install line. Specifically:

- Change the existing `%pip install` to include `openpyxl`.
- Add a fourth curl line:
  ```
  !curl -s https://raw.githubusercontent.com/shippy/czechitas-ai-data/refs/heads/main/notebooks/datacorp_payroll_q3.xlsx > datacorp_payroll_q3.xlsx
  ```

The third code cell (data loading) needs no change — it loads only the three CSVs that tasks 1–3 use. The payroll xlsx is loaded inside task 4 specifically, which is the point of sub-step 4a.

## Pre-flight verification

Before committing, the implementer must:

1. Generate the canonical dataset by running `uv run scripts/generate_datacorp.py`.
2. Load the resulting `datacorp_payroll_q3.xlsx`, drop the header artifacts and totals row.
3. Run `payroll.sample(50, random_state=42)` and count:
   - How many rows have `mzda_brutto` between 1 500 and 4 000 (the EUR landmines).
   - How many rows have an `oddeleni` value that disagrees with the matching `datacorp.csv` row.
4. If either count is 0, try `random_state` values 1–10 in order and pick the first that gives ≥1 of each. Document the chosen value in the notebook comment.
5. Execute the full notebook end-to-end against the OpenAI API and confirm:
   - The setup, tasks 1, 2, 3 cells still run (no regressions).
   - Task 4 completes in under 90 seconds wall-clock.
   - At least one EUR row is flagged as `vazna` by the LLM.
   - The Pydantic schema is accepted by `instructor` without errors.

## Cost envelope

50 LLM calls × small reasoning model (gpt-5.4-mini, which the notebook already uses) ≈ $0.05–$0.10 per student per run. Affordable in a class setting of 10–30 students. Course participants get their own API keys, so cost is per-student, not pooled.

## Deliverables

- Modified `notebooks/assignment-03c.ipynb` with 7 new cells (1 markdown intro, 4 code cells, 1 markdown hint, 1 markdown discussion) inserted between current Úkol 3 and Bonusový úkol sections.
- Setup cell updated to download the xlsx and install `openpyxl`.
- This design doc.
- No other file changes.

## Out of scope

- Updating the assignment-03c "pomocníček" GPT (referenced in the notebook intro) — that content lives outside this repo.
- Adding tasks 5+.
- Touching `assignment-03.ipynb` or `assignment-03b.ipynb` (already deprecated).
- Refactoring tasks 1–3.
- Creating a separate "answer key" notebook.

## Success criteria

- `notebooks/assignment-03c.ipynb` opens in VS Code and Colab without errors.
- Setup cell downloads 4 dataset files (3 csv + 1 xlsx) successfully on Colab.
- Tasks 1–3 produce the same outputs they did before (verified by manual review of cells after a clean run).
- Task 4 runs end-to-end in under 90 seconds, processes 50 sampled rows, produces `Verdikt` objects, and flags at least one EUR-currency row as `vazna`.
- The Pydantic model uses nested list + enum and accepts `Field(description=...)` annotations.
