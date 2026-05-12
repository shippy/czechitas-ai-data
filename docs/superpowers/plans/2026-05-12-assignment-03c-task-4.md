# Assignment-03c Task 4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fourth task to `notebooks/assignment-03c.ipynb` that uses structured outputs on `datacorp_payroll_q3.xlsx` for HR/payroll reconciliation, without altering existing tasks 1–3.

**Architecture:** Insert 7 new cells (1 markdown intro + 5 code + 1 markdown discussion) between the existing Úkol 3 starter cell (current index 15) and the Bonusový úkol markdown (current index 16). Update the Colab setup cell to download the xlsx and install `openpyxl`. Verify by executing the notebook end-to-end against the OpenAI API.

**Tech Stack:** Jupyter notebook (.ipynb JSON), `pandas`, `openpyxl`, `instructor` (already used by the notebook for structured outputs against OpenAI), `pydantic` v2 with `Enum`.

---

## File structure

| File | Action | Responsibility |
|---|---|---|
| `notebooks/assignment-03c.ipynb` | Modify | Update setup cell; insert 7 new task-4 cells |
| `docs/superpowers/plans/2026-05-12-assignment-03c-task-4.md` | (this file) | Plan |

No tests are added — the notebook is verified by end-to-end execution against the OpenAI API.

## Pre-implementation cell map (current state)

| Index | Type | Purpose |
|---|---|---|
| 0 | md | Title + Colab badge |
| 1 | md | ## Setup |
| 2 | code | Colab/local bootstrap (downloads CSVs, picks up `OPENAI_API_KEY`) — **MODIFY in Task 2** |
| 3 | code | Imports + `instructor` clients + test ping |
| 4 | md | ## Čtení dat |
| 5 | code | `pd.read_csv` lines |
| 6 | code | `reviews.head()` |
| 7 | code | `exit_interviews.head()` |
| 8 | md | ## Ukázka structured output |
| 9 | code | `ExitReason` model + `extract_exit_reason` |
| 10 | md | ## Úkol 1 |
| 11 | code | Úkol 1 starter |
| 12 | md | ## Úkol 2 |
| 13 | code | Úkol 2 starter |
| 14 | md | ## Úkol 3 |
| 15 | code | Úkol 3 starter |
| **16** | **md** | **## Bonusový úkol — INSERT BEFORE THIS** |
| 17 | code | Bonus starter |

## Post-implementation cell map (target state)

Insert 7 cells at index 16 (pushing the bonus cells to 23–24):

| New index | Type | Content (summary) |
|---|---|---|
| 16 | md | ## Úkol 4 intro + xlsx loading hint |
| 17 | code | sub-step 4a — empty xlsx loading starter |
| 18 | code | sub-step 4b — `payroll.sample(50, random_state=<verified>)` (pre-filled) |
| 19 | code | sub-step 4c — Pydantic `Zavaznost`/`Nesoulad`/`Verdikt` model (pre-filled) |
| 20 | code | sub-step 4c — `reconcile_row` + `asyncio.gather` loop (pre-filled) |
| 21 | code | sub-step 4d — analyze starter with TODO comments |
| 22 | md | Diskusní otázky |

---

## Task 1: Pre-flight — determine the `random_state` for sampling

**Files:**
- Read: `notebooks/datacorp_payroll_q3.xlsx`, `notebooks/datacorp.csv`
- Output: a single integer (the chosen `random_state`) recorded in this plan and used by Task 3.

The notebook's sample seed must surface at least 1 EUR-currency row AND at least 1 plausible-wrong-department row in the 50-row sample. With 4 EUR + 3 wrong-dept rows in a population of ~1011, seed 42 may or may not hit both. We pick the lowest seed in [42, 1, 2, …, 50] that satisfies both constraints.

- [ ] **Step 1: Write the verification script as a one-shot block**

Create no file; run this inline (e.g. via `uv run python -c '...'` or paste into a scratch cell):

```python
import pandas as pd

payroll = pd.read_excel(
    "notebooks/datacorp_payroll_q3.xlsx",
    sheet_name="Mzdy Q3 2025",
    skiprows=3,
)
payroll = payroll[payroll["os_cislo"].apply(lambda x: str(x).replace(".0", "").isdigit())]
payroll["os_cislo"] = payroll["os_cislo"].astype(int)

hr = pd.read_csv("notebooks/datacorp.csv")
hr_dept = dict(zip(hr["employee_id"], hr["oddeleni"]))

def score(seed: int) -> tuple[int, int]:
    s = payroll.sample(50, random_state=seed)
    eur = ((s["mzda_brutto"] >= 1500) & (s["mzda_brutto"] <= 4000)).sum()
    wrong = sum(1 for _, r in s.iterrows()
                if hr_dept.get(r["os_cislo"]) is not None
                and r["oddeleni"] != hr_dept[r["os_cislo"]]
                and r["oddeleni"] in {"Vývoj", "Marketing", "Obchod", "Podpora", "Finance", "HR"})
    return eur, wrong

for seed in [42, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
             21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
             40, 41, 43, 44, 45, 46, 47, 48, 49, 50]:
    eur, wrong = score(seed)
    print(f"seed={seed:3d}  eur={eur}  wrong_dept={wrong}")
    if eur >= 1 and wrong >= 1:
        print(f">>> Use random_state={seed}")
        break
```

- [ ] **Step 2: Run it and record the chosen seed**

Run: `uv run python -c "$(...)"` or via a one-off scratch script. Note the chosen seed in the implementer's report so the controller can pass it into Task 3.

- [ ] **Step 3: No commit yet**

Pre-flight has no code artifacts. The chosen seed flows into Task 3's pre-filled cell content.

---

## Task 2: Update the Colab setup cell

**Files:**
- Modify: `notebooks/assignment-03c.ipynb` (cell index 2)

The existing setup cell is:

```python
try:
    from google.colab import userdata
    _secret = userdata.get("OPENAI_API_KEY")
    %pip install pandas instructor openai python-dotenv rich seaborn
    !curl -s https://raw.githubusercontent.com/shippy/czechitas-ai-data/refs/heads/main/notebooks/datacorp.csv > datacorp.csv
    !curl -s https://raw.githubusercontent.com/shippy/czechitas-ai-data/refs/heads/main/notebooks/datacorp_reviews.csv > datacorp_reviews.csv
    !curl -s https://raw.githubusercontent.com/shippy/czechitas-ai-data/refs/heads/main/notebooks/datacorp_exit_interviews.csv > datacorp_exit_interviews.csv
except ImportError:
    import os
    from dotenv import load_dotenv
    _ = load_dotenv()
    _secret = os.environ.get("OPENAI_API_KEY")
```

- [ ] **Step 1: Replace cell 2's content using NotebookEdit**

Replace the source of cell 2 (cell mode `replace`) with:

```python
try:
    from google.colab import userdata
    _secret = userdata.get("OPENAI_API_KEY")
    %pip install pandas instructor openai openpyxl python-dotenv rich seaborn
    !curl -s https://raw.githubusercontent.com/shippy/czechitas-ai-data/refs/heads/main/notebooks/datacorp.csv > datacorp.csv
    !curl -s https://raw.githubusercontent.com/shippy/czechitas-ai-data/refs/heads/main/notebooks/datacorp_reviews.csv > datacorp_reviews.csv
    !curl -s https://raw.githubusercontent.com/shippy/czechitas-ai-data/refs/heads/main/notebooks/datacorp_exit_interviews.csv > datacorp_exit_interviews.csv
    !curl -s https://raw.githubusercontent.com/shippy/czechitas-ai-data/refs/heads/main/notebooks/datacorp_payroll_q3.xlsx > datacorp_payroll_q3.xlsx
except ImportError:
    import os
    from dotenv import load_dotenv
    _ = load_dotenv()
    _secret = os.environ.get("OPENAI_API_KEY")
```

Two changes: `openpyxl` added to the pip line; one new curl line for the xlsx.

- [ ] **Step 2: Verify the notebook still parses as valid JSON**

Run: `python -c "import json; json.load(open('notebooks/assignment-03c.ipynb'))"`
Expected: no exception.

- [ ] **Step 3: Commit**

```bash
git add notebooks/assignment-03c.ipynb
git commit -m "assignment-03c: download payroll xlsx and install openpyxl in setup"
```

---

## Task 3: Insert the 7 new task-4 cells

**Files:**
- Modify: `notebooks/assignment-03c.ipynb` (insert cells before current index 16 — the "## Bonusový úkol" markdown cell)

Use the NotebookEdit tool with `edit_mode: "insert"` and `cell_id` pointing at the existing Bonus markdown cell, so the new cells land *before* it. Insert in the order below; each insert places its cell directly before the bonus cell, so insert them in **reverse order** (the last cell first, the first cell last) OR insert them all by repeatedly targeting the Bonus cell and reading back the new IDs. Either approach is fine — pick one and stay consistent.

Pre-flight result: replace `__SEED__` below with the random_state value chosen in Task 1.

### Cell A — markdown intro + 4a hint

Insert this markdown cell:

```markdown
## Úkol 4: Rekonciliace mzdového listu (xlsx)

Finance vám poslalo soubor `datacorp_payroll_q3.xlsx` — kvartální mzdový list za Q3 2025. Některé řádky ale **nesedí** s tím, co máme v `datacorp.csv`: jiné oddělení, jiná částka, nebo dokonce hodnota v jiné měně. Vaším úkolem je použít structured outputs jako auditora a nechat LLM rozhodnout, co je v pořádku a co ne.

### 4a. Načtěte mzdový list

Soubor je formát `.xlsx`, ne CSV. Pozor:

- Horní 3 řádky jsou hlavičkové artefakty (z původní šablony).
- Poslední řádek je součtový (`CELKEM`), který chcete odfiltrovat.
- Pracujte s listem `Mzdy Q3 2025` (workbook obsahuje i prázdné `List2` a `List3`).

Použijte `pd.read_excel` se vhodným argumentem `skiprows=` a odfiltrujte součtový řádek.
```

### Cell B — sub-step 4a code (empty starter)

```python
# Načtěte 'datacorp_payroll_q3.xlsx' (list 'Mzdy Q3 2025').
# Použijte skiprows= pro horní hlavičkové řádky a odfiltrujte řádek CELKEM.
# Výsledek uložte do proměnné `payroll` jako čistý DataFrame.

payroll = ...
```

### Cell C — sub-step 4b code (pre-filled)

```python
# Vzorek 50 řádků s pevně daným seedem.
# Seed je záměrně zvolen tak, aby vzorek obsahoval alespoň jeden řádek v EUR
# a alespoň jeden řádek se špatným oddělením — ať vidíme, co LLM zachytí.

payroll_sample = payroll.sample(50, random_state=__SEED__).reset_index(drop=True)
print(f"Vzorek: {len(payroll_sample)} řádků")
payroll_sample.head()
```

### Cell D — sub-step 4c Pydantic model (pre-filled)

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

### Cell E — sub-step 4c LLM call (pre-filled)

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


# Spojíme vzorek payrollu s HR daty přes employee_id / os_cislo
merged = payroll_sample.merge(
    datacorp, left_on="os_cislo", right_on="employee_id", how="left",
)
verdicts = await asyncio.gather(*[
    reconcile_row(payroll_sample.loc[i], merged.loc[i])
    for i in payroll_sample.index
])
payroll_sample["verdikt"] = verdicts
print(f"Zpracováno {len(verdicts)} řádků")
```

### Cell F — sub-step 4d analyze starter

```python
# 1. Spočítejte: kolik verdiktů má každou hodnotu Zavaznost?
#    Tip: payroll_sample["verdikt"].apply(lambda v: v.zavaznost).value_counts()

# 2. Vypište řádky, kde LLM označil verdikt jako 'vážná'. Co je v nich za anomálii?

# 3. V plném datasetu jsou 4 řádky v EUR a 3 řádky se špatným oddělením.
#    Kolik z nich se trefilo do vašeho 50-řádkového vzorku?
#    Kolik z nich LLM odhalil?
```

### Cell G — discussion markdown

```markdown
### Diskusní otázky (k zamyšlení)

1. Které typy chyb LLM odhalí spolehlivě, a které ne? Proč?
2. Co by se stalo, kdyby system prompt neobsahoval nápovědu o rozsahu CZK? Vyzkoušejte.
3. Jak by se dala metoda škálovat na celý dataset (1000 řádků) bez zbytečného plýtvání tokeny? (Tip: batch, pre-filtering, levnější model na první pass.)
```

### Steps

- [ ] **Step 1: Insert Cell A (markdown intro)**

Use NotebookEdit with `edit_mode=insert`, target the bonus markdown cell's ID, set `cell_type=markdown`, content = Cell A markdown.

- [ ] **Step 2: Insert Cell B (4a empty code starter)**

NotebookEdit `edit_mode=insert`, target the bonus markdown cell's ID, `cell_type=code`, content = Cell B code.

- [ ] **Step 3: Insert Cell C (4b sample)**

NotebookEdit insert. Replace `__SEED__` with the value chosen in Task 1.

- [ ] **Step 4: Insert Cell D (Pydantic model)**

NotebookEdit insert.

- [ ] **Step 5: Insert Cell E (LLM call)**

NotebookEdit insert.

- [ ] **Step 6: Insert Cell F (analyze starter)**

NotebookEdit insert.

- [ ] **Step 7: Insert Cell G (discussion markdown)**

NotebookEdit insert, `cell_type=markdown`.

**Important:** Insertion order matters because every insert targets the bonus cell. If you insert A → B → C → D → E → F → G targeting the bonus cell each time, you'll get them stacked in **reverse** order (G ends up adjacent to the bonus cell, A is furthest from it). To get the correct order (A first, G last, all directly before bonus), insert in **reverse**: G → F → E → D → C → B → A. After each insert, the bonus cell's ID does not change; only its index does.

Alternative: insert all in forward order targeting the *previously inserted* cell each time. Pick whichever the NotebookEdit tool supports more cleanly.

- [ ] **Step 8: Verify cell layout**

Run:
```bash
jq -r '.cells | to_entries[] | "\(.key) \(.value.cell_type): \(.value.source | if type == "array" then join("") else . end | .[0:80] | gsub("\n"; " "))"' notebooks/assignment-03c.ipynb
```

Expected layout (final 9 cells, indices 14–24):
```
14 markdown: ## Úkol 3 …
15 code: # Zde řešte úkol 3.
16 markdown: ## Úkol 4: Rekonciliace mzdového listu …
17 code: # Načtěte 'datacorp_payroll_q3.xlsx' …
18 code: payroll_sample = payroll.sample …
19 code: from enum import Enum …
20 code: async def reconcile_row …
21 code: # 1. Spočítejte: kolik verdiktů …
22 markdown: ### Diskusní otázky …
23 markdown: ## Bonusový úkol …
24 code: # Zde řešte bonusový úkol.
```

If the order doesn't match, fix with additional NotebookEdit calls before moving on.

- [ ] **Step 9: Verify the notebook still parses**

Run: `python -c "import json; json.load(open('notebooks/assignment-03c.ipynb'))"`
Expected: no exception.

- [ ] **Step 10: Commit**

```bash
git add notebooks/assignment-03c.ipynb
git commit -m "assignment-03c: add Úkol 4 — payroll xlsx reconciliation with structured outputs"
```

---

## Task 4: End-to-end notebook execution against OpenAI API

**Files:**
- Read: `notebooks/assignment-03c.ipynb`
- Output: an execution log + a screenshot/listing of the verdict counts.

The notebook uses `openai/gpt-5.4-mini` via `instructor`. An OpenAI API key must be present in `.env` as `OPENAI_API_KEY`. (Per the user's global instructions, do NOT touch `.env`; assume the key is already there.)

For tasks 1, 2, 3 (the existing tasks) we need to fill in *something* before executing — they are graded as student work, so they're not pre-solved. To run end-to-end we need them to at least not crash. Two approaches:

A. **Execute only the cells up to and including task 4**, skipping the empty student cells 11, 13, 15 (tasks 1, 2, 3 starters).
B. **Fill in the empty cells with stub solutions** just for verification, then revert before commit.

Approach A is simpler. Use `jupyter nbconvert --to notebook --execute` with a `--ExecutePreprocessor.allow_errors=True` flag, or programmatically execute only the relevant cells.

Actually the cleanest path: **execute the notebook with `allow_errors=True`**, then inspect the output of cells 17–21 (the new task-4 cells). The student-starter cells will fail with `Ellipsis` or `NotImplementedError` but execution continues.

- [ ] **Step 1: Run the notebook end-to-end with allow_errors**

```bash
uv run --with jupyter --with openpyxl --with rich --with seaborn --with instructor \
  jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.allow_errors=True \
  --ExecutePreprocessor.timeout=120 \
  --output /tmp/assignment-03c-executed.ipynb \
  notebooks/assignment-03c.ipynb
```

Expected: completes within ~3 minutes. Cells 11/13/15 will have errors (the student starters use `...`). The new task-4 cells (17–21) should execute without errors.

- [ ] **Step 2: Inspect the executed task-4 cells**

Run:
```bash
jq -r '.cells[17,18,19,20,21] | .outputs[]? | (.text // .data."text/plain" // "") | if type == "array" then join("") else . end' /tmp/assignment-03c-executed.ipynb
```

Confirm:
- Cell 17 (load xlsx): user-filled `payroll = ...` triggers an error — expected; this is a student starter.
- Cell 18 (sample) cannot run because cell 17 didn't define `payroll`. **This is a problem for verification.**

**Verification workaround:** Add a temporary inline fill-in for cells 17, 11, 13, 15 inside a *separate executed copy* of the notebook. Steps 3–5 below.

- [ ] **Step 3: Create a stub-filled copy for execution only**

Make a temp copy and patch cells in-memory:

```bash
cp notebooks/assignment-03c.ipynb /tmp/assignment-03c-stubbed.ipynb
```

Programmatically edit `/tmp/assignment-03c-stubbed.ipynb` so:
- Cell 11 (Úkol 1 starter) becomes a trivial pass: `pass`
- Cell 13 (Úkol 2 starter) becomes `pass`
- Cell 15 (Úkol 3 starter) becomes `pass`
- Cell 17 (new 4a starter) becomes the canonical solution:
  ```python
  payroll = pd.read_excel(
      "datacorp_payroll_q3.xlsx",
      sheet_name="Mzdy Q3 2025",
      skiprows=3,
  )
  payroll = payroll[payroll["os_cislo"].apply(lambda x: str(x).replace(".0", "").isdigit())]
  payroll["os_cislo"] = payroll["os_cislo"].astype(int)
  ```

Use a Python helper script in `/tmp/` or `jq` + Python. One option:

```python
import json
from pathlib import Path

path = Path("/tmp/assignment-03c-stubbed.ipynb")
nb = json.loads(path.read_text())

def set_source(idx: int, src: str) -> None:
    nb["cells"][idx]["source"] = src.splitlines(keepends=True)
    nb["cells"][idx]["outputs"] = []
    nb["cells"][idx]["execution_count"] = None

set_source(11, "pass\n")
set_source(13, "pass\n")
set_source(15, "pass\n")
set_source(17, """payroll = pd.read_excel(
    "datacorp_payroll_q3.xlsx",
    sheet_name="Mzdy Q3 2025",
    skiprows=3,
)
payroll = payroll[payroll["os_cislo"].apply(lambda x: str(x).replace(".0", "").isdigit())]
payroll["os_cislo"] = payroll["os_cislo"].astype(int)
""")

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
```

Also: the stubbed notebook uses local paths. The Colab setup cell's `try: from google.colab` will raise `ImportError` and load `.env` from `python-dotenv`. The CSV/xlsx files must be present at the working directory of the kernel. The simplest approach is to symlink:

```bash
ln -sf "$(pwd)/notebooks/datacorp.csv" /tmp/datacorp.csv
ln -sf "$(pwd)/notebooks/datacorp_reviews.csv" /tmp/datacorp_reviews.csv
ln -sf "$(pwd)/notebooks/datacorp_exit_interviews.csv" /tmp/datacorp_exit_interviews.csv
ln -sf "$(pwd)/notebooks/datacorp_payroll_q3.xlsx" /tmp/datacorp_payroll_q3.xlsx
ln -sf "$(pwd)/.env" /tmp/.env
```

- [ ] **Step 4: Execute the stubbed notebook**

```bash
cd /tmp
uv run --project /Users/simon/Documents/czechitas-ai-data \
  --with jupyter --with openpyxl --with rich --with seaborn --with instructor \
  jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=180 \
  --output /tmp/assignment-03c-stubbed-executed.ipynb \
  /tmp/assignment-03c-stubbed.ipynb
cd /Users/simon/Documents/czechitas-ai-data
```

Expected: completes within ~3 minutes. NO cell errors. The async client + 50-call gather should take 30–60 s wall-clock.

- [ ] **Step 5: Verify verdict distribution**

Extract `payroll_sample["verdikt"]` distribution. Run a Python one-liner against the stubbed-executed notebook to confirm:

```bash
uv run python -c "
import json
nb = json.load(open('/tmp/assignment-03c-stubbed-executed.ipynb'))
# Cell index 20 prints 'Zpracováno 50 řádků' — confirm
for cell in nb['cells']:
    for out in cell.get('outputs', []):
        text = out.get('text', '') or out.get('data', {}).get('text/plain', '')
        if isinstance(text, list):
            text = ''.join(text)
        if 'Zpracováno' in text or 'Vzorek' in text:
            print(text.strip())
"
```

Expected output includes `Vzorek: 50 řádků` and `Zpracováno 50 řádků`.

- [ ] **Step 6: Confirm at least one EUR row was flagged as `vážná`**

Add a small verification script:

```bash
uv run python <<'EOF'
import json
nb = json.load(open('/tmp/assignment-03c-stubbed-executed.ipynb'))
# Find a cell that has produced Verdikt objects in display — easier: re-run the
# verdict-counting step against the executed notebook by reading the pickle?
# Simpler: just confirm the cell ran without errors. The deeper verification
# (verdict severity distribution) is a manual eyeball check on the executed
# stubbed notebook.
errors = [c for c in nb['cells'] if any(o.get('output_type') == 'error' for o in c.get('outputs', []))]
print(f"Cells with errors: {len(errors)}")
assert len(errors) == 0, f"Cells {[nb['cells'].index(c) for c in errors]} had errors"
print("All cells executed cleanly.")
EOF
```

If this passes, the notebook is verified end-to-end.

- [ ] **Step 7: Clean up temp files**

```bash
rm -f /tmp/assignment-03c-stubbed.ipynb /tmp/assignment-03c-stubbed-executed.ipynb /tmp/assignment-03c-executed.ipynb
rm -f /tmp/datacorp.csv /tmp/datacorp_reviews.csv /tmp/datacorp_exit_interviews.csv /tmp/datacorp_payroll_q3.xlsx /tmp/.env
```

- [ ] **Step 8: No additional commit needed**

The committed notebook from Task 3 is the final state. The verification was on a stubbed copy.

If the verification revealed issues (e.g., the LLM consistently returns malformed Verdikt objects, or the seed produces zero EUR rows in the sample), report BLOCKED with details so the controller can adjust the plan.

---

## Self-review notes

- **Spec coverage:** Tasks 1–3 cover sub-steps 4a–4d and the setup cell. Task 4 covers pre-flight verification. The discussion-questions markdown is in Task 3 Cell G.
- **Pydantic model field names** are consistent across Cell D (definition) and Cell E (LLM call).
- **`random_state` value** is determined empirically in Task 1, then substituted into Cell C in Task 3. No hardcoded seed mismatch.
- **No new tests** — the verification is end-to-end notebook execution, which exercises the OpenAI API path. This matches the spec's success criteria.
- **Risk:** if the OpenAI API returns rate-limit errors during Task 4 verification, retry with a smaller semaphore (e.g. `SEM = asyncio.Semaphore(2)`) or a smaller sample (`.head(10)` instead of `.sample(50)`). Don't commit the smaller sample — it's a verification-only adjustment.
