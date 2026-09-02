# Curriculum Refresh 2026 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the agent-ladder curriculum refresh (spec §5–§8) so the materials are demoable on a call on 2026-09-03.

**Architecture:** Four workstreams: (1) ground-truth export from the synthetic-data generator without perturbing existing outputs, (2) notebook 03c Fáze 2 rewritten as an eval, (3) slide edits across all nine Slidev files, (4) README/prereq + housekeeping. Task 1 blocks Task 2; slides and README tasks are independent of both and of each other.

**Tech Stack:** Python (pandas, numpy RNG), Jupyter/nbformat, Slidev markdown, uv.

**Spec:** `docs/superpowers/specs/2026-09-02-curriculum-refresh-design.md`

## Global Constraints

- All student-facing text is **Czech**, feminine plural address (match existing slides: "zkuste", "samy", "analytičky").
- **No new RNG draws** in `scripts/generate_datacorp.py` before or between existing draws — shipped CSVs must stay byte-identical (verified in Task 1).
- Slides must build: `cd slides && npm run build` exits 0.
- Vendor-neutral wording in exercises: "váš agent (Claude Cowork / ChatGPT Work)", intents not button screenshots.
- Ground-truth reason labels (Czech, used in generator export AND notebook Literal, must match exactly): `plat`, `kariérní růst`, `work-life balance`, `vedení`, `jiné`.
- Review sentiment labels: `pozitivní`, `smíšené`, `negativní`. Exit sentiment stays `pozitivní`/`neutrální`/`negativní` (soft-eval only).
- Commit after each task with a conventional message + the standard co-author trailer.

---

### Task 0: Baseline determinism check

**Files:** none modified.

- [ ] **Step 1:** On a clean tree, run `uv run scripts/generate_datacorp.py`.
- [ ] **Step 2:** Run `git status --porcelain notebooks/`. Expected: empty (regeneration reproduces committed files byte-for-byte).
- [ ] **Step 3 (contingency):** If files differ, STOP and record which; the no-new-draws constraint is then moot — regenerate everything, note "datasets regenerated" in the final report, and `git checkout -- notebooks/` before starting Task 1 so the diff attribution stays clean.

### Task 1: Ground-truth export from generator

**Files:**
- Modify: `scripts/generate_datacorp.py` (functions `build_reviews`, `apply_dirt_reviews`, `build_exit_interviews`, `apply_dirt_exit_interviews`, `build_payroll_xlsx`, `apply_dirt_payroll`, `main`)
- Creates at runtime: `notebooks/datacorp_ground_truth_exits.csv`, `notebooks/datacorp_ground_truth_reviews.csv`, `notebooks/datacorp_ground_truth_payroll.csv`

**Interfaces (produced, consumed by Task 2):**
- `datacorp_ground_truth_exits.csv`: columns `employee_id:int, true_reason:{plat|kariérní růst|work-life balance|vedení|jiné}, true_bitter:bool, language:{cs|mixed-en}, is_contradiction:bool`
- `datacorp_ground_truth_reviews.csv`: columns `employee_id:int, rok:int, true_sentiment:{pozitivní|smíšené|negativní}, is_sarcastic:bool, is_wrong_person:bool`
- `datacorp_ground_truth_payroll.csv`: columns `os_cislo:int, error_types:str` (`;`-joined subset of `mzda_off,arithmetic,eur,oddeleni_en,oddeleni_wrong`, or `ok`)

Mechanism: builders/dirt functions add `_gt_*` columns alongside existing ones (recording values already computed — the chosen `reason`, `is_bitter`, which template list, dirt indices). `main()` splits `_gt_*` columns out into the ground-truth CSVs and drops them before writing the public files, preserving original column order. Reason mapping (generator key → export label): `salary→plat, growth→kariérní růst, work_life_balance→work-life balance, management→vedení, other→jiné`.

- [ ] **Step 1:** In `build_exit_interviews`, extend `exit_rows.append({...})` with `"_gt_reason": REASON_LABELS[reason], "_gt_bitter": bool(is_bitter)`. Add module-level `REASON_LABELS` dict per the mapping above.
- [ ] **Step 2:** In `apply_dirt_exit_interviews`, initialize `df["_gt_language"] = "cs"`, `df["_gt_contradiction"] = False`; inside the existing loops set `df.at[i, "_gt_language"] = "mixed-en"` for `en_idx` rows and, for `contra_idx`, `df.loc[contra_idx, ["_gt_reason", "_gt_contradiction"]] = ["plat", True]`.
- [ ] **Step 3:** In `build_reviews`, record the template family when it is chosen: `_gt_sentiment` = `pozitivní` for `REVIEW_TEMPLATES_POSITIVE`, `smíšené` for MIXED (including the planted-signal overwrite), `negativní` for NEGATIVE; append it to `review_rows`.
- [ ] **Step 4:** In `apply_dirt_reviews`, initialize `_gt_sarcastic`/`_gt_wrong_person` to False; in the existing loops set sarcastic rows to `_gt_sentiment="negativní", _gt_sarcastic=True` and wrong-person rows to `_gt_sentiment="smíšené", _gt_wrong_person=True`.
- [ ] **Step 5:** In `apply_dirt_payroll`, initialize `df["_gt_errors"] = [[] for _ in df.index]` and append the tag inside each existing dirt loop (`mzda_off`, `arithmetic`, `eur`, `oddeleni_en`, `oddeleni_wrong`; the `aktivni` truthiness loop is noise, not an error — skip it). At function end: `df["_gt_errors"] = df["_gt_errors"].apply(lambda l: ";".join(l) if l else "ok")`.
- [ ] **Step 6:** In `main()`, after building each of `exits`, `reviews`, `payroll`: split ground truth (`gt = df[[keys + _gt_cols]].rename(columns=strip _gt_ prefix per the interface schema)`), write the three ground-truth CSVs, and drop `_gt_*` from the public frames before the existing `to_csv`/`write_payroll_xlsx` calls. `write_payroll_xlsx` must receive the frame without `_gt_*` columns.
- [ ] **Step 7:** Run `uv run scripts/generate_datacorp.py`. Then `git status --porcelain notebooks/` must show ONLY the three new `datacorp_ground_truth_*.csv` files as untracked; all tracked files unmodified. If any tracked file changed, a new RNG draw or column-order change slipped in — fix before proceeding.
- [ ] **Step 8:** Sanity-check contents: exits GT has ~70 rows, 5 `mixed-en`, 1 contradiction; reviews GT has ~150 rows, 5 sarcastic, 3 wrong-person; payroll GT `ok` share roughly 85–90 %.
- [ ] **Step 9:** Commit generator + three CSVs: `feat: emit ground-truth labels from DataCorp generator`.

### Task 2: Notebook 03c — Fáze 2 eval rewrite

**Files:**
- Modify: `notebooks/assignment-03c.ipynb`

**Interfaces:** Consumes Task 1 CSV schemas verbatim. The Colab bootstrap cell (cell 2) must also `curl` the three ground-truth CSVs from the same raw-GitHub pattern (branch `main` — note they exist on the feature branch only until merge; for tomorrow's test, temporarily point at `curriculum-refresh-2026` and leave a `# TODO: switch to main on merge` comment).

- [ ] **Step 1:** Align the example model: `ExitReason.primary_reason` becomes `Literal["plat", "kariérní růst", "work-life balance", "vedení", "jiné"]`.
- [ ] **Step 2:** Add the three ground-truth curl lines to the Colab setup cell.
- [ ] **Step 3:** Replace the Úkol 3 markdown + empty cell with an "Úkol 3: Změřte svou extrakci (eval)" section containing pre-built scoring cells (students run and read; they don't write the scoring):

```python
gt = pd.read_csv("datacorp_ground_truth_exits.csv")
ei = exit_interviews.copy()
ei["pred_reason"] = [r.primary_reason for r in ei["structured"]]
ei["pred_sentiment"] = [r.sentiment for r in ei["structured"]]
merged = ei.merge(gt, on="employee_id")
print(f"Accuracy důvodu odchodu: {(merged.pred_reason == merged.true_reason).mean():.0%}")
pd.crosstab(merged.true_reason, merged.pred_reason)
```

```python
# Bias sonda: liší se úspěšnost podle jazyka textu?
merged.groupby("language").apply(
    lambda g: pd.Series({"n": len(g), "accuracy": (g.pred_reason == g.true_reason).mean()})
)
```

```python
# Totéž pro reviews — sarkasmus a záměna osoby
gt_r = pd.read_csv("datacorp_ground_truth_reviews.csv")
reviews["pred_sentiment"] = [r.sentiment for r in reviews["structured"]]  # vyžaduje pole `sentiment` ve vašem modelu
merged_r = reviews.merge(gt_r, on=["employee_id", "rok"])
print(merged_r.groupby("is_sarcastic").apply(lambda g: (g.pred_sentiment == g.true_sentiment).mean()))
```

Markdown around the cells: dataset je syntetický, správné odpovědi známe; tip that Úkol 2's model should include `sentiment: Literal["pozitivní", "smíšené", "negativní"]` for the eval to work; closing question **"Změnila by naměřená chybovost nějaký závěr, který byste prezentovaly vedení?"**; note that `neutrální` vs `smíšené` mismatches are themselves discussion material.
- [ ] **Step 4:** Update the intro markdown cell (course-flow description) and the discussion-questions cell to reference the eval; keep Úkol 4 (payroll) labeled as bonus mirroring the lecturer demo.
- [ ] **Step 5:** Validate: `uv run --with nbformat python -c "import nbformat; nbformat.validate(nbformat.read('notebooks/assignment-03c.ipynb', as_version=4))"`; also dry-run the merge logic against the real GT CSVs with mocked predictions (small script in scratchpad) to prove column names join cleanly.
- [ ] **Step 6:** Commit: `feat: rewrite 03c Fáze 2 as eval against ground truth`.

### Task 3: Slides s0 — ladder, smoke test, prompt refresh

**Files:** Modify `slides/s0-teorie.md`, `slides/s0-intro.md`

- [ ] **Step 1:** In `s0-teorie.md`, replace the 🎭 "Vytvořte roli" card in the "Jak psát dobré prompty" grid with `🧭 Definujte úspěch — "Hotovo vypadá takto: …"`, and after that slide add a new slide **"Kdy sáhnout po přemýšlivém modelu"**: rychlé modely na mechaniku (souhrny, formátování, kód podle vzoru); thinking/reasoning modely na vícekrokové úlohy (odvození metriky, rekonciliace, ověření závěru); přemýšlivý model = pomalejší a dražší, ale ukáže postup — chtějte ho vidět.
- [ ] **Step 2:** At the end of `s0-teorie.md` add two slides:

**"Žebřík agentnosti — mapa dneška"** (table): `1. Chat + příloha | ChatGPT / Claude v prohlížeči | Sekce 1–2` / `2. Agent nad vašimi soubory | Claude Cowork · ChatGPT Work | Sekce 3 a 5` / `3. Agent v terminálu | Claude Code · Codex | Demo odpoledne`, plus callout: "Čím výš, tím víc AI udělá sama — a tím pečlivěji kontrolujete, co udělala. Otázky zůstávají stejné: Co udělala? Co ověřím? Za co ručím já?"

**"Než začneme: otestujte si výbavu (5 minut)"**: 1. otevřete desktopovou aplikaci (ChatGPT s Work / Claude Cowork); 2. stáhněte testovací složku (QRCode to `https://github.com/shippy/czechitas-ai-data/tree/main/precourse`); 3. zadejte: „Shrň mi data v této složce do tří odrážek." Callout: „Nefunguje? Nevadí — fallback je Google Colab (ukážeme v sekci 3), nebo pracujte ve dvojici."
- [ ] **Step 3:** Build check + commit: `slides: agent ladder, smoke test, prompt-engineering refresh (s0)`.

### Task 4: Slides s2 — agent reframe + governance block

**Files:** Modify `slides/s2-data.md`

- [ ] **Step 1:** After the "Dvě poučení" slide add **"Tohle byl celou dobu agent"**: ChatGPT/Claude s nahraným CSV nepočítá „z hlavy" — píše a spouští Python v sandboxu; klikněte na „Zobrazit kód"; právě jste dělaly první stupeň žebříku: zadaly cíl, AI jednala, vy jste kontrolovaly.
- [ ] **Step 2:** Replace the "Než nahrajete data do AI" slide with two slides: **"HR data = vysoce riziková doména"** (AI Act Annex III — AI hodnotící zaměstnance je vysoce rizikové použití; GDPR — mzdy/hodnocení/exit interviews jsou osobní údaje zaměstnanců; bias — model může systematicky hůř číst některé skupiny či jazyky, změříme v sekci 4; dnes: fiktivní data, v praxi: IT/DPO) and **"Co smím nahrát kam"** — 3×3 table (rows: veřejná či fiktivní data ✅✅✅ / interní neosobní ⚠️✅✅ / osobní údaje zaměstnanců ❌⚠️(DPA + anonymizace)⚠️; columns: osobní účet Free/Plus, firemní plán Team/Enterprise, API) + footer „Vždy: anonymizace, firemní pravidla, při nejistotě se zeptejte."
- [ ] **Step 3:** Build check + commit: `slides: agent reframe and HR governance block (s2)`.

### Task 5: Slides s3 rewrite + s3a fixes

**Files:** Modify `slides/s3-priprava.md`, `slides/s3a-python.md`

- [ ] **Step 1 (s3):** Keep the intro/GIGO/traditional-vs-AI slides but drop "jak rychle běží" phrasing (optimality → správnost + dokumentace). Replace the CoffeeCloud demo slide with **"Demo: Agent nad složkou DataCorp"** (lecturer, Cowork/Work): 1. „Projdi soubory ve složce a shrň problémy s kvalitou dat"; 2. „Navrhni čisticí kroky — zatím nic neměň"; 3. schvalujeme/odmítáme, agent provádí; 4. výstup = vyčištěný CSV + log změn. Sledujte: co agent rozhodl sám?
- [ ] **Step 2 (s3):** Replace the three SP3 zadání slides with two: **"Samostatná práce 3 (~20 min)"**: namiřte svého agenta na složku s DataCorp daty (stáhněte si repo/zip — QR na repo); nechte navrhnout čisticí kroky a iterujte; nechte provést → `datacorp_clean.csv` + `cleaning_log.md`; přidejte sloupec `kategorie_mzdy` (≤ 35 000 „malá mzda", ≤ 95 000 „střední mzda", jinak „velká mzda"); ručně ověřte 2–3 opravy proti původním datům. **"Posuďte + fallback"**: Věříte logu? Co agent rozhodl potichu za vás? Co byste nechaly schvalovat vždy? Fallback: Colab + Data Science Agent (nahrajte CSV, stejné zadání), nebo dvojice.
- [ ] **Step 3 (s3a):** Fix the broken `Counter` slide — code becomes:

```python
from pydantic import BaseModel
from typing import Literal

class Counter(BaseModel):
    count: int
    kind: Literal["puppy", "kitten"]
    members: list[str]

a = Counter(count=1, kind="puppy", members=["Punťa"])
```

with bullets updated (`BaseModel` sdruží data, zkontroluje typy při vytvoření — přesně to použijeme pro structured outputs). Delete the "Bonus: Async" slide entirely. Add **"Jak číst a ověřit vygenerovaný kód"**: čtěte shora dolů a u každého bloku řekněte, kterých sloupců se dotýká; jeden krok přepočítejte ručně na 2–3 řádcích; nevěříte řádku → „Vysvětli, co dělá a proč"; chtějte souhrn změn (počty řádků před/po).
- [ ] **Step 4:** Build check + commit: `slides: file-agent SP3 rewrite, fix Counter example, drop async (s3, s3a)`.

### Task 6: Slides s4 — eval SP4 + terminal demo block

**Files:** Modify `slides/s4-analyza.md`

- [ ] **Step 1:** Delete the three slides "Způsob 1: No-code", "Způsob 2: Code", "Kdy který způsob?" and the section slide "Ukázka: Stejná otázka, dva způsoby" (superseded by ladder framing).
- [ ] **Step 2:** Rewrite the "Fáze 2" slide as **"Fáze 2: Změřte svou extrakci (~15 min)"**: dataset je syntetický — správné odpovědi známe (`datacorp_ground_truth_*.csv`); Úkol 3.1 accuracy + confusion matrix důvodů odchodu; Úkol 3.2 bias sonda — úspěšnost u anglických a sarkastických textů; Úkol 3.3 „Změnila by naměřená chybovost nějaký závěr pro vedení?" Bonus row stays (payroll rekonciliace).
- [ ] **Step 3:** Update the "Společné sdílení" slide: čí extrakce skórovala nejlépe — a co rozhodlo (prompt? popisy polí? model?); kde model selhával (sarkasmus? angličtina?); co s tím říká governance slide ze sekce 2?
- [ ] **Step 4:** Append demo section at end of file: section slide **"Demo: Agent v terminálu"** + one content slide: Claude Code / Codex CLI nad složkou `notebooks/`; zadání „Zrekonciliuj datacorp_payroll_q3.xlsx proti datacorp.csv a napiš report"; sledujte: co agent čte, co spouští, co lektor kontroluje, čemu nevěří; stejné dovednosti dohledu jako u Cowork — jen víc autonomie; třetí stupeň žebříku.
- [ ] **Step 5:** Build check + commit: `slides: SP4 eval phase and terminal-agent demo (s4)`.

### Task 7: Slides s5, s6, slides.md

**Files:** Modify `slides/s5-prezentace.md`, `slides/s6-bonus.md`, `slides/slides.md`

- [ ] **Step 1 (s5):** In the SP5 úkol slide add the traceability rule as the final steps: nechte agenta (Cowork/Work) napsat manažerské shrnutí; než ho pustíte dál, **každé číslo dohledejte** ve své analýze; číslo bez zdroje škrtněte nebo označte „neověřeno". Add a short demo slide **"Demo: AI jako oponent"** (lektor simuluje pushback HR Business Partnera: „Nemůže to být jen senioritou?" apod.).
- [ ] **Step 2 (s6):** Replace Custom GPT slide with **"Projects — trvalý kontext"** (ChatGPT i Claude: složka konverzací se sdílenými soubory a instrukcemi; hodí se na opakovanou agendu — měsíční report, jeden dataset; nahrazuje dřívější Custom GPTs). In the tools grid replace the 🖼️ image-gen card with `🖥️ Desktop agenti — Claude Cowork, ChatGPT Work — agent nad vašimi soubory`. Change the Transformers section slide subtitle to "Samostudium — projděte si doma, na kurzu nepresentujeme". Remove the trailing feedback-QR slide from `s6-bonus.md` (slides.md already has it).
- [ ] **Step 3 (slides.md):** Update the Osnova table: add row `— | Demo: agent v terminálu | Šimon` after Sekce 4 and mark bonus row `⭐ | Bonus: Nástroje (transformery = samostudium) | —`.
- [ ] **Step 4:** Build check + commit: `slides: SP5 traceability, bonus refresh, osnova (s5, s6, index)`.

### Task 8: README, precourse folder, housekeeping deletions

**Files:**
- Create: `precourse/test-data.csv` (20 rows, any simple sales-like synthetic table), `precourse/README.md`
- Modify: `README.md`
- Delete: `notebooks/assignment-03.ipynb`, `notebooks/assignment-03b.ipynb`, `notebooks/guardian_100.csv` (only 03b references it)

- [ ] **Step 1:** `precourse/README.md` (Czech): checklist — placený účet ChatGPT (Plus a výš) NEBO Claude (Pro a výš); desktopová aplikace (ChatGPT desktop s Work / Claude Cowork); **Windows pozor:** Cowork vyžaduje Hyper-V (Windows Pro/Enterprise/Education — na Windows Home nepoběží → použijte ChatGPT, nebo počítejte s Colab fallbackem); Google účet (Colab); testovací úkol: otevřete aplikaci, namiřte ji na tuto složku, zadejte „Shrň mi data v této složce do tří odrážek" — pokud dostanete shrnutí, jste připravené.
- [ ] **Step 2:** Generate `precourse/test-data.csv` deterministically (small Python snippet, seeded) — e.g. 20 řádků: datum, produkt, ks, cena.
- [ ] **Step 3:** `README.md`: add "Předpoklady pro účastnice" section linking `precourse/`; update Datasety table with the three ground-truth CSVs ("správné odpovědi pro eval v SP4 — negenerují se studentkám, jen pro Fázi 2"); remove the deprecated-notebooks note; add note that the pomocníček GPT slug must be refreshed per cohort.
- [ ] **Step 4:** Delete the two deprecated notebooks + `guardian_100.csv`.
- [ ] **Step 5:** Commit: `chore: precourse checklist, README prereqs, drop deprecated notebooks`.

### Task 9: Final verification

- [ ] **Step 1:** `cd slides && npm run build` — exits 0.
- [ ] **Step 2:** `uv run scripts/generate_datacorp.py && git status --porcelain` — only expected state.
- [ ] **Step 3:** nbformat validation of 03c (same command as Task 2 Step 5).
- [ ] **Step 4:** Re-read spec §5–§8 against the diff; list any gaps in the final report instead of silently skipping.

## Self-review notes

- Spec coverage: §5 Blok 0→T3, S1 wording→(folded into T3? — no: S1 "ChatGPT→vaše AI" wording — **added to Task 7 Step 1 scope? NO — assign: Task 4 covers s2 only.** Fix: include `slides/s1-zadani.md` wording sweep in Task 7 Step 1 (one substitution pass, "ChatGPT" → "vaše AI" where it addresses the tool generically).
- §6 items: 1→T5, 3→T8, 4→T7, 5→T8, 6→out of scope per cohort. §7→T1, §8→T8+T3.
- Type consistency: GT column names (`true_reason`, `language`, `is_sarcastic`, `rok`) match between Task 1 interface and Task 2 code cells. Reason labels identical in T1 mapping and T2 Literal.
- Open spec questions resolved by default for tomorrow: SP5 traceability = strict rule (Q2); guardian_100.csv deleted (Q3); pomocníček update = README note only (Q4); Markéta sign-off (Q1) = pending, flag on the call.
