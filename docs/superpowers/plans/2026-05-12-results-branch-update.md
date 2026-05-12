# Results Branch Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the `results` branch up to date with `main`, fill in canonical solutions for the new Úkol 4 cells in `assignment-03c.ipynb`, and refresh `notebooks/datacorp-answer-key.md` to cover the expanded dataset's dirt categories.

**Architecture:** Three sequential commits on the `results` branch — (1) merge `main` with manual JSON stitching of the notebook conflict, (2) replace Úkol 4 empty starter cells with canonical solutions, (3) extend the instructor answer key with new dirt categories + Úkol 4 expected results. Implementation per the spec at `docs/superpowers/specs/2026-05-12-results-branch-update-design.md`.

**Tech Stack:** git, Python (for ipynb JSON manipulation), pandas (for verifying answer-key counts). No new dependencies.

---

## File structure

| File | Action | Responsibility |
|---|---|---|
| `notebooks/assignment-03c.ipynb` (on `results`) | Modify | Merge results' Úkoly 1–3 solutions + main's Úkol 4 scaffolding + canonical Úkol 4 solutions |
| `notebooks/datacorp-answer-key.md` (on `results`) | Modify | Extend with 18 new dirt categories + Úkol 4 expected behavior |
| All other files inherited from `main` via merge | Inherit | Generator, tests, new dataset files, new spec docs |

## Cell mapping reference

**Pre-merge — `results` branch `assignment-03c.ipynb` (21 cells):**

| Idx | Type | Content |
|---|---|---|
| 0 | md | Title |
| 1 | md | ## Setup |
| 2 | code | Colab/local bootstrap (downloads 3 CSVs, OLD — missing xlsx + openpyxl) |
| 3 | code | Imports + clients |
| 4 | md | ## Čtení dat |
| 5 | code | pd.read_csv lines |
| 6 | code | reviews.head() |
| 7 | code | exit_interviews.head() |
| 8 | md | ## Ukázka |
| 9 | code | ExitReason model |
| 10 | md | ## Úkol 1 |
| **11** | **code** | **Úkol 1 SOLUTION** |
| 12 | md | ## Úkol 2 |
| **13** | **code** | **Úkol 2 SOLUTION (ReviewAnalysis)** |
| 14 | md | ## Úkol 3 |
| **15** | **code** | **Úkol 3 setup (seaborn + extract structured)** |
| **16** | **code** | **Úkol 3.1 solution** |
| **17** | **code** | **Úkol 3.2 solution** |
| **18** | **code** | **Úkol 3.3 solution** |
| 19 | md | Bonus |
| 20 | code | Bonus starter |

**Pre-merge — `main` branch `assignment-03c.ipynb` (25 cells):**

| Idx | Type | Content |
|---|---|---|
| 0–9 | mix | Identical to results 0–9 |
| 2 | code | Colab bootstrap (NEW — includes xlsx download + openpyxl in pip) |
| 10 | md | ## Úkol 1 |
| **11** | **code** | **Empty starter** |
| 12 | md | ## Úkol 2 |
| **13** | **code** | **Empty starter (ReviewAnalysis with `...`)** |
| 14 | md | ## Úkol 3 |
| **15** | **code** | **Empty starter (`# Zde řešte úkol 3.`)** |
| **16** | **md** | **## Úkol 4: Rekonciliace mzdového listu (NEW)** |
| **17** | **code** | **Úkol 4a empty starter (`payroll = ...`)** |
| **18** | **code** | **Úkol 4b sample (filled, `random_state=5`)** |
| **19** | **code** | **Úkol 4c Pydantic model (filled)** |
| **20** | **code** | **Úkol 4c LLM call (filled)** |
| **21** | **code** | **Úkol 4d analyze starter** |
| **22** | **md** | **Diskusní otázky (NEW)** |
| 23 | md | Bonus |
| 24 | code | Bonus starter |

**Post-merge target — `results` branch `assignment-03c.ipynb` (28 cells):**

| Idx | Source | Content |
|---|---|---|
| 0–9 | identical | Title, setup md, **main's setup code** (with xlsx download), imports, Čtení dat, head() previews, Ukázka |
| 10 | identical | ## Úkol 1 markdown |
| 11 | **results** | Úkol 1 SOLUTION |
| 12 | identical | ## Úkol 2 markdown |
| 13 | **results** | Úkol 2 SOLUTION |
| 14 | identical | ## Úkol 3 markdown |
| 15 | **results** | Úkol 3 setup |
| 16 | **results** | Úkol 3.1 solution |
| 17 | **results** | Úkol 3.2 solution |
| 18 | **results** | Úkol 3.3 solution |
| 19 | **main** | ## Úkol 4 markdown intro |
| 20 | **main** → Task 2 | Úkol 4a empty starter (will be filled with canonical solution in Task 2) |
| 21 | **main** | Úkol 4b sample (`random_state=5`) |
| 22 | **main** | Úkol 4c Pydantic model |
| 23 | **main** | Úkol 4c LLM call |
| 24 | **main** → Task 2 | Úkol 4d analyze starter (will be filled in Task 2) |
| 25 | **main** | Diskusní otázky markdown |
| 26 | identical | Bonus markdown |
| 27 | identical | Bonus starter |

---

## Task 1: Merge main into results, resolve notebook conflict

**Files:**
- Modify: `notebooks/assignment-03c.ipynb`
- Inherit (auto-merge): everything else from `main`

- [ ] **Step 1: Switch to results branch, ensure clean tree**

```bash
cd /Users/simon/Documents/czechitas-ai-data
git fetch origin
git checkout results
git pull origin results
git status  # must be clean
```

Expected: on branch results, clean.

- [ ] **Step 2: Start the merge**

```bash
git merge origin/main
```

Expected: conflict on `notebooks/assignment-03c.ipynb`. Other files merge cleanly (new dataset files, generator, tests, README, spec docs, etc.). Note the conflict message and any other unexpected conflicts.

If conflicts appear in files OTHER than `notebooks/assignment-03c.ipynb`, stop and report. The plan assumes only the notebook conflicts; if `datacorp-answer-key.md` or others conflict, the merge strategy needs adjustment.

- [ ] **Step 3: Snapshot the two source notebooks before resolving**

```bash
git show origin/main:notebooks/assignment-03c.ipynb > /tmp/03c-main.ipynb
git show :2:notebooks/assignment-03c.ipynb > /tmp/03c-results.ipynb  # :2 = ours (results)
```

Verify both files parse:

```bash
python -c "import json; json.load(open('/tmp/03c-main.ipynb')); json.load(open('/tmp/03c-results.ipynb')); print('both valid')"
```

Expected: `both valid`.

- [ ] **Step 4: Stitch the merged notebook**

Run this Python script:

```python
import json
from pathlib import Path

main_nb = json.loads(Path("/tmp/03c-main.ipynb").read_text())
results_nb = json.loads(Path("/tmp/03c-results.ipynb").read_text())

assert len(main_nb["cells"]) == 25, f"main has {len(main_nb['cells'])} cells, expected 25"
assert len(results_nb["cells"]) == 21, f"results has {len(results_nb['cells'])} cells, expected 21"

def cell_starts_with(cell, prefix):
    src = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
    return src.lstrip().startswith(prefix)

# Sanity checks
assert cell_starts_with(main_nb["cells"][2], "try:"), "main cell 2 is not the bootstrap"
assert cell_starts_with(main_nb["cells"][16], "## Úkol 4"), "main cell 16 is not Úkol 4 md"
assert cell_starts_with(main_nb["cells"][17], "# Načtěte"), "main cell 17 is not 4a starter"
assert cell_starts_with(main_nb["cells"][21], "# 1. Spočítejte"), "main cell 21 is not 4d analyze"
assert cell_starts_with(main_nb["cells"][22], "### Diskusní"), "main cell 22 is not discussion md"
assert cell_starts_with(results_nb["cells"][11], "results ="), "results cell 11 is not Úkol 1 sol"
assert cell_starts_with(results_nb["cells"][13], "class ReviewAnalysis"), "results cell 13 is not Úkol 2 sol"
assert cell_starts_with(results_nb["cells"][15], "import seaborn"), "results cell 15 is not Úkol 3 setup"

merged_cells = (
    main_nb["cells"][0:11]            # 0-10: identical, take main (has xlsx download in cell 2)
    + [results_nb["cells"][11]]       # 11: Úkol 1 solution from results
    + [main_nb["cells"][12]]          # 12: Úkol 2 markdown
    + [results_nb["cells"][13]]       # 13: Úkol 2 solution from results
    + [main_nb["cells"][14]]          # 14: Úkol 3 markdown
    + results_nb["cells"][15:19]      # 15-18: Úkol 3 setup + 3.1 + 3.2 + 3.3 from results
    + main_nb["cells"][16:23]         # 19-25: Úkol 4 intro + 4a + 4b + model + LLM + analyze + discussion
    + main_nb["cells"][23:25]         # 26-27: Bonus md + bonus starter
)

assert len(merged_cells) == 28, f"merged has {len(merged_cells)} cells, expected 28"

# Use main's notebook metadata (kernelspec, language_info) as baseline
merged_nb = dict(main_nb)
merged_nb["cells"] = merged_cells

Path("notebooks/assignment-03c.ipynb").write_text(
    json.dumps(merged_nb, indent=1, ensure_ascii=False) + "\n"
)
print(f"Merged notebook written: {len(merged_cells)} cells")
```

Save the script to `/tmp/stitch_03c.py` and run with `uv run python /tmp/stitch_03c.py`.

Expected: `Merged notebook written: 28 cells`. All assertions pass.

- [ ] **Step 5: Verify the merged notebook structure**

```bash
jq -r '.cells | to_entries[] | "\(.key) \(.value.cell_type): \(.value.source | if type == "array" then join("") else . end | .[0:70] | gsub("\n"; " "))"' notebooks/assignment-03c.ipynb
```

Expected output (first column is index, then type + first 70 chars):

```
0 markdown: # Úkol 3c: Structured Outputs nad DataCorp daty …
1 markdown: ## Setup …
2 code: try:     from google.colab import userdata …  (must include datacorp_payroll_q3.xlsx curl)
3 code: import asyncio import instructor import os from rich import print …
4 markdown: ## Čtení dat
5 code: import pandas as pd  datacorp = pd.read_csv …
6 code: reviews.head()
7 code: exit_interviews.head()
8 markdown: ## Ukázka …
9 code: from pydantic import BaseModel, Field …
10 markdown: ## Úkol 1 …
11 code: results = await asyncio.gather …  (Úkol 1 solution)
12 markdown: ## Úkol 2 …
13 code: class ReviewAnalysis(BaseModel):     sentiment: …  (Úkol 2 solution)
14 markdown: ## Úkol 3 …
15 code: import seaborn as sns import matplotlib.pyplot …  (Úkol 3 setup)
16 code: # 3.1: Které oddělení má nejvíc negativních …
17 code: # 3.2: Koreluje sentiment review s výší platu …
18 code: # 3.3: Jaké jsou nejčastější důvody odchodu? …
19 markdown: ## Úkol 4: Rekonciliace mzdového listu (xlsx) …
20 code: # Načtěte 'datacorp_payroll_q3.xlsx' …  (empty starter, filled in Task 2)
21 code: # Vzorek 50 řádků s pevně daným seedem …
22 code: from enum import Enum from pydantic import BaseModel, Field …
23 code: async def reconcile_row(payroll_row: pd.Series, hr_row: pd.Series) …
24 code: # 1. Spočítejte: kolik verdiktů má každou hodnotu Zavaznost …  (empty starter, filled in Task 2)
25 markdown: ### Diskusní otázky …
26 markdown: ## Bonusový úkol …
27 code: # Zde řešte bonusový úkol.
```

Confirm cell 2 includes the new xlsx curl line:

```bash
grep "datacorp_payroll_q3.xlsx" notebooks/assignment-03c.ipynb && echo "xlsx curl present"
```

- [ ] **Step 6: Stage the resolution and commit the merge**

```bash
git add notebooks/assignment-03c.ipynb
git status  # should show all conflicts resolved
git commit  # opens an editor with the default merge message; close to accept
```

Or non-interactively:

```bash
git commit --no-edit
```

Expected: merge commit created on `results` with parents `<results-tip>` and `<main-tip>`. Inspect:

```bash
git log --oneline -3
```

The HEAD commit should be the merge commit.

- [ ] **Step 7: Clean up scratch files**

```bash
rm -f /tmp/03c-main.ipynb /tmp/03c-results.ipynb /tmp/stitch_03c.py
```

---

## Task 2: Fill in Úkol 4 canonical solutions (cells 20 and 24)

**Files:**
- Modify: `notebooks/assignment-03c.ipynb` (cells 20 and 24)

- [ ] **Step 1: Update cell 20 (Úkol 4a — load xlsx)**

Run:

```python
import json
from pathlib import Path

path = Path("notebooks/assignment-03c.ipynb")
nb = json.loads(path.read_text())
assert len(nb["cells"]) == 28
assert nb["cells"][20]["cell_type"] == "code"
src20 = nb["cells"][20]["source"]
src20_str = src20 if isinstance(src20, str) else "".join(src20)
assert "Načtěte" in src20_str, "cell 20 isn't the 4a starter"

new_20 = '''payroll = pd.read_excel(
    "datacorp_payroll_q3.xlsx",
    sheet_name="Mzdy Q3 2025",
    skiprows=3,
)
payroll = payroll[payroll["os_cislo"].apply(lambda x: str(x).replace(".0", "").isdigit())]
payroll["os_cislo"] = payroll["os_cislo"].astype(int)
print(f"Payroll rows after cleanup: {len(payroll)}")
payroll.head()
'''
nb["cells"][20]["source"] = new_20.splitlines(keepends=True)
nb["cells"][20]["outputs"] = []
nb["cells"][20]["execution_count"] = None

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print("Cell 20 updated.")
```

Save as `/tmp/fill_4a.py` and run with `uv run python /tmp/fill_4a.py`.

Expected: `Cell 20 updated.`

- [ ] **Step 2: Update cell 24 (Úkol 4d — analyze)**

Run:

```python
import json
from pathlib import Path

path = Path("notebooks/assignment-03c.ipynb")
nb = json.loads(path.read_text())
assert nb["cells"][24]["cell_type"] == "code"
src24 = nb["cells"][24]["source"]
src24_str = src24 if isinstance(src24, str) else "".join(src24)
assert "Spočítejte" in src24_str, "cell 24 isn't the analyze starter"

new_24 = '''# 1. Distribuce závažnosti
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
'''
nb["cells"][24]["source"] = new_24.splitlines(keepends=True)
nb["cells"][24]["outputs"] = []
nb["cells"][24]["execution_count"] = None

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print("Cell 24 updated.")
```

Save as `/tmp/fill_4d.py` and run with `uv run python /tmp/fill_4d.py`.

Expected: `Cell 24 updated.`

- [ ] **Step 3: Verify**

```bash
python -c "import json; json.load(open('notebooks/assignment-03c.ipynb'))"
```

Expected: no exception.

```bash
jq -r '.cells[20,24].source | if type == "array" then join("") else . end' notebooks/assignment-03c.ipynb | head -40
```

Expected: cell 20 starts with `payroll = pd.read_excel(`; cell 24 starts with `# 1. Distribuce závažnosti`.

- [ ] **Step 4: Commit**

```bash
git add notebooks/assignment-03c.ipynb
git commit -m "results: solve Úkol 4 (load xlsx + analyze cells)"
rm -f /tmp/fill_4a.py /tmp/fill_4d.py
```

---

## Task 3: Refresh `notebooks/datacorp-answer-key.md`

**Files:**
- Modify: `notebooks/datacorp-answer-key.md`

The existing file has two sections at the top: "Záměrně zasazené problémy v datech" (6 dirt rows) and "Záměrně zasazené analytické signály" (analytical findings). The 6-dirt table needs count refreshes; everything else stays.

Then add two new sections at the bottom: "Další záměrně zasazené problémy (rozšíření 2026-05)" and "Úkol 4 — očekávané výsledky".

- [ ] **Step 1: Update the existing 6-dirt table with refreshed counts**

The actual counts on the regenerated dataset (verified on main):

| Problém | Detail (refreshed) |
|---|---|
| Nekonzistentní `oddeleni` | "Marketing" (119×), "marketing" (16×), "Mktg" (5×) |
| Chybějící `plat` | 41 celkem, z toho 25 v Podpoře |
| Smíšené formáty datumů | 101× DD.MM.YYYY, 910× YYYY-MM-DD |
| Odlehlé hodnoty platů | ~4 v Podpoře / HR (>200 000 Kč) |
| Duplicitní řádky | ~5 exact duplicates (overlap with later dirt reduces from planted 10) |
| Neplatné `hodnoceni_vykonu` | ~5 hodnot mimo rozsah 1–5 (hodnoty 0 nebo 6) |

Use the Edit tool (NOT a Python script — markdown edits should be line-level). The 6 cells of the existing table are:

```markdown
| Nekonzistentní `oddeleni` | "Marketing" (51×), "marketing" (15×), "Mktg" (5×) | `df['oddeleni'].value_counts()` |
| Chybějící `plat` | 40 celkem, z toho 25 v Podpoře | `df['plat'].isna().sum()` |
| Smíšené formáty datumů | 103× DD.MM.YYYY, 407× YYYY-MM-DD | `df['datum_nastupu'].str.contains(r'^\d{2}\.')` |
| Odlehlé hodnoty platů | 2× v Podpoře (~226k, ~247k), 2× v HR (~231k, ~236k) | `df[df['plat'] > 150000]` |
| Duplicitní řádky | 10 přesných duplikátů | `df.duplicated().sum()` |
| Neplatné `hodnoceni_vykonu` | 8 hodnot mimo rozsah 1–5 (hodnoty 0 nebo 6) | `df['hodnoceni_vykonu'].isin([0, 6]).sum()` |
```

Replace with the refreshed versions:

```markdown
| Nekonzistentní `oddeleni` | "Marketing" (119×), "marketing" (16×), "Mktg" (5×) | `df['oddeleni'].value_counts()` |
| Chybějící `plat` | 41 celkem, z toho 25 v Podpoře | `df['plat'].isna().sum()` |
| Smíšené formáty datumů | 101× DD.MM.YYYY, 910× YYYY-MM-DD | `df['datum_nastupu'].str.contains(r'^\d{2}\.')` |
| Odlehlé hodnoty platů | ~4 v Podpoře / HR (>200 000 Kč) | `df[df['plat'] > 150000]` |
| Duplicitní řádky | ~5 exact duplicates (z 10 plánovaných; novější dirt některé přepsala) | `df.duplicated().sum()` |
| Neplatné `hodnoceni_vykonu` | ~5 hodnot mimo rozsah 1–5 (hodnoty 0 nebo 6) | `df['hodnoceni_vykonu'].isin([0, 6]).sum()` |
```

- [ ] **Step 2: Append the new dirt-categories section + Úkol 4 expected results**

Find the end of the "Záměrně zasazené analytické signály" section (the existing "## 5. Vysoká fluktuace v Podpoře" subsection is at the end based on the existing file's content; verify with `tail` or by reading). Append directly after the last existing content:

```markdown

## Další záměrně zasazené problémy (rozšíření 2026-05)

Po rozšíření datasetu na ~1000 zaměstnanců a 4 nové soubory přibylo 18 dalších kategorií chyb v datech. Studenti by je měli postupně objevit při práci s `salary_history`, `org_chart`, `tickets`, a `payroll_q3.xlsx`.

| # | Problém | Detail | Jak ověřit |
|---|---------|--------|------------|
| 7 | Telefonní formáty (`datacorp.csv`) | 3 varianty (`+420 NNN NNN NNN`, `NNNNNNNNN`, `NNN NNN NNN`) + ~20 NaN + 5 neplatných (`???`, `viz Slack`) | `df['telefon'].str.match(...).value_counts()` |
| 8 | Email / jméno nesoulad | ~15 řádků, kde `employee_id` byl recyklován po reonboardingu | `df['email'].str.contains(df['jmeno'])` |
| 9 | Mezery a `\n` ve jménech | ~30 řádků s leading/trailing whitespace v `jmeno` nebo `prijmeni` | `df['jmeno'].str.match(r'^\s\|\s$')` |
| 10 | Encoding mojibake | 3 řádky, kde diakritika je rozbitá (`Č`→`Ä` apod.) | `df['prijmeni'].str.contains('Ä')` |
| 11 | Smíchané desetinné oddělovače | ~10% řádků v `salary_history.plat_po` má comma-decimal s non-breaking space | `df['plat_po'].astype(str).str.contains(',')` |
| 12 | Datumová polévka (`salary_history`) | ISO + Czech (DD.MM.YYYY) + US (MM/DD/YYYY) + jen rok | `df['datum_zmeny'].str.match(...)` |
| 13 | Tečky/whitespace v `tickets.reporter_id` | ~10 řádků s `"234."` nebo `" 234"` | `df['reporter_id'].astype(str).str.match(r'\.\|^\s\|\s$')` |
| 14 | Silent ID collision (`salary_history`) | 1 záměrná kolize: 3 řádky jednoho zaměstnance přepsané na ID jiného | manuální kontrola |
| 15 | Diakritika-složené duplikáty | 1 dvojice (`Černý` ↔ `Cerny`) s odlišnými `employee_id` (~6014) | `df['prijmeni'].str.contains('Cerny')` |
| 16 | Datumy nástupu v budoucnosti | 5 řádků s datem v 2027–2028 | `df['datum_nastupu'].str.contains('2027\|2028')` |
| 17 | Backdated correction (`salary_history`) | 2 řádky, jejichž `datum_zmeny` předchází předchozí změnu — chronologický sort ukáže "fantomový pokles platu" | sort by employee+date, hledat klesající `plat_po` |
| 18 | Plausible-wrong departments (`payroll`) | 3 řádky s `oddeleni` jiným než v `datacorp.csv`, ani jedno není provably wrong | merge na os_cislo, porovnej `oddeleni` |
| 19 | EUR currency landmine (`payroll`) | 4 řádky s `mzda_brutto` v ~1500–4000 (zjevně EUR, ne CZK) | `df['mzda_brutto'].between(1500, 4000)` |
| 20 | Sarkastické reviews | 5 reviews s `*kreativní*` / `*radost*` / `*originální*` — ironicky míněné | `df['review_text'].str.contains(r'\*\w+\*')` |
| 21 | Wrong-person reviews | 3 reviews, kde text se týká jiné osoby než `employee_id` | manuální čtení 161 reviews |
| 22 | Mixed-language exit interviews | 5 fragmentů kombinujících češtinu a angličtinu | `df['interview_text'].str.contains(r'\bbetter\|opportunity\b')` |
| 23 | Self-contradicting exit interview | 1 záznam s rozporem (např. "platově byl spokojen" + "odchází kvůli penězům") | manuální čtení |
| 24 | Survivorship bias | ~15 zaměstnanců odešlo — jsou v `salary_history`, `reviews`, `exit_interviews`, ale ne v `datacorp.csv` | `set(history.employee_id) - set(main.employee_id)` |

## Úkol 4 — očekávané výsledky

**Plný dataset:** 4 řádky v EUR + 3 řádky se špatným oddělením.

**Vzorek 50 řádků s `random_state=5`:** 1 EUR řádek + 1 wrong-dept řádek (zaměstnanec 498: payroll=Vývoj, HR=Obchod).

**Očekávané chování LLM (gpt-5.4-mini se system promptem zmiňujícím CZK rozsah 25 000–150 000):**
- Oba landminy (EUR + wrong-dept) by měly být označeny jako `vážná`.
- Často také flagne řádky s `mzda_celkem ≠ mzda_brutto + bonus` (30 takových řádků v plném datasetu, typicky 1–2 ve vzorku) — to není záměrná chyba ze spec, ale legitimní finding.
- Aritmetické nesoulady padají často do `střední`, zřídka do `vážná`.
- `stejna_osoba` by mělo být téměř vždy `true` (merged frame párujeme přesně přes `os_cislo == employee_id`).

**Bez nápovědy o CZK rozsahu (diskusní otázka 2):** EUR landmine je často přehlédnut. To je očekávané a je smysl této otázky — ukázat, jak system prompt vede LLM k pozornosti.

**Škálování (diskusní otázka 3):** plnou populaci ~1000 řádků lze zlevnit přes
1. cheaper-first model (např. nano) pro pre-filtering podezřelých řádků
2. batch API call (více řádků v jednom requestu)
3. lokální rule-based heuristiky (range check na `mzda_brutto`, oddělení matchup) jako první vrstva
```

Use the Edit / Write tool to append this content to the end of the file.

- [ ] **Step 3: Verify the file parses as Markdown and contains the new sections**

```bash
grep -c "^## " notebooks/datacorp-answer-key.md  # count h2 sections
```

Expected: at least 4 (original 2 + 2 new).

```bash
grep "Úkol 4 — očekávané výsledky" notebooks/datacorp-answer-key.md
grep "Další záměrně zasazené problémy" notebooks/datacorp-answer-key.md
```

Both should match exactly one line.

- [ ] **Step 4: Commit**

```bash
git add notebooks/datacorp-answer-key.md
git commit -m "results: refresh answer key for expanded dataset and Úkol 4"
```

- [ ] **Step 5: Push the results branch**

```bash
git push origin results
```

Expected: 3 new commits pushed (the merge + Úkol 4 solutions + answer-key refresh). No PR is opened — `results` is a long-lived parallel branch.

```bash
git log --oneline -4
```

Should show the three new commits at the top.

---

## Self-review notes

- **Spec coverage:** Tasks 1–3 directly mirror the spec's three commits.
- **Cell mapping:** The plan reflects the *actual* cell layout (results has 21 cells with Úkol 3 split into 4 cells; main has 25 cells post-Úkol 4). The spec assumed a simpler split — this plan corrects it.
- **Refreshed dirt counts** in Task 3 Step 1 come from running the count script on the regenerated dataset (rows=1011, Marketing=119/marketing=16/Mktg=5, missing plat=41, Czech dates=101, ISO=910, duplicates=5, invalid hodnoceni=5, salary outliers=5). Numbers may shift by ±1 if the implementer regenerates with a slightly different state, but the order of magnitude is correct.
- **No code changes outside the notebook and answer key.** Tests on `main` cover the generator; no new tests needed here.
- **Risk:** if `git merge origin/main` produces conflicts beyond `assignment-03c.ipynb` (e.g., README, generator, datacorp.csv binary diff), the plan needs revision. Task 1 Step 2 explicitly checks for this and instructs the implementer to stop and report.
