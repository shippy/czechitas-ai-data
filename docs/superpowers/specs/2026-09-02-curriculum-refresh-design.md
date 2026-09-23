# Curriculum Refresh 2026 — Design Spec

- **Date:** 2026-09-02
- **Branch:** `curriculum-refresh-2026`
- **Status:** Draft for review
- **Scope:** "AI v datové analýze" one-day course (Czechitas), next cohort (date TBD; slide metadata currently says Květen 2026 — update per cohort)

## 1. Context & motivation

The course teaches the data-analysis lifecycle (CRISP-DM spine) with AI assistance. As last delivered
(May 2026), every student exercise lives in the 2024 paradigm: *upload a CSV to ChatGPT and chat*.
Since then, analyst practice has shifted toward **agentic tools** — GUI agents over local files
(Claude Cowork, ChatGPT Work) and terminal agents (Claude Code, Codex CLI) — and toward
**measuring** LLM outputs instead of eyeballing them. The course also has several sequencing bugs
and dated slides (details in §6).

What stays untouched: the CRISP-DM section spine, the DataCorp narrative with deliberately dirty
data, and the core lessons ("vaše follow-up otázky jsou ta dovednost", "důvěřuj, ale prověřuj").

## 2. Design principles

1. **The agent ladder is the day's arc.** Chat with an upload → agent over your files → agent in a
   terminal. The tool escalates as the day progresses; the DataCorp folder is the constant.
2. **The recurring lesson at every rung:** what did it do, what do I verify, what do I own. The
   higher the rung, the more autonomy the AI has and the more deliberate the verification must be.
3. **Vendor-neutral exercises.** Students bring *either* a paid ChatGPT or Claude account.
   Exercises say what to ask for, not which buttons to click. Mixed vendors are a feature:
   same exercise, different agents, compare notes in the sharing moments.
4. **Don't trust — measure.** LLM-in-the-pipeline outputs get evaluated against ground truth,
   which the synthetic dataset can emit.
5. **Swap, don't add.** Single day; every addition names its cut. Net time change ≈ zero.

## 3. Constraints

- Single-day format, ~2h of hands-on exercise time total, beginner audience (Czechitas), Czech.
- **Access model: prerequisite.** Students arrive with a paid ChatGPT or Claude subscription and
  the desktop app installed (accepted risk; see §8).
- Lecture/demo materials must survive vendor UI churn between now and delivery: describe intents
  ("point the agent at the folder and ask for..."), avoid screenshots of buttons.

## 4. The agent ladder (new framing, taught explicitly)

| Rung | Tool | Who touches it | Where in the day |
|---|---|---|---|
| 1. Chat + upload | ChatGPT / Claude chat | everyone | Sections 1–2 |
| 1.5 (reframe) | "Show code" in chat data analysis | everyone | Section 2 |
| 2. Agent over files | Claude Cowork / ChatGPT Work | everyone (prereq) | Sections 3, 5 |
| 2.5 | Colab + Gemini Data Science Agent | fallback + Section 4 env | Sections 3 (fallback), 4 |
| 3. Terminal agent | Claude Code / Codex CLI | lecturer demo only | Demo block before Section 5 |

## 5. Revised day structure

### Blok 0 — Úvod + teorie + prompt engineering (Šimon)
- Keep: bios, ML→LLM, training, context window, hallucinations, model landscape.
- **New slide: the agent ladder** — the map of the day (§4 table, visual).
- **Prompt-engineering refresh:** cut the role-prompting slide ("Jsi expert na SQL…" folklore);
  replace with: context beats persona, concrete examples, explicit success criteria, let the model
  ask clarifying questions, when to reach for a thinking/reasoning model vs. a fast one.
  Zero/few-shot slide stays.
- **Prereq smoke test (~5 min):** everyone opens their desktop app, points it at a small test
  folder, runs one canned task. Casualties identified now, not during SP3; they pair up or switch
  to the Colab fallback.

### Sekce 1 — Porozumění zadání (Markéta) — rung 1
- Keep structure and SP1 as-is. Wording "ChatGPT" → "vaše AI" throughout.

### Sekce 2 — Porozumění datům / EDA (Šimon) — rung 1 → 1.5
- Keep the 6-step conversation demo and SP2 (they work).
- **New reframe slide** after the demo: "Tohle byl celou dobu agent" — chat data analysis writes
  and runs Python in a hidden sandbox; click *show code*; you were already supervising an agent.
- **Governance block** (expands the current "Než nahrajete data do AI" slide, ~2 slides):
  HR data (mzdy, hodnocení, exit interviews) = employment domain = **EU AI Act Annex III
  high-risk** when AI evaluates workers; GDPR employee-data basics; what may go to which tool
  (consumer chat vs. Team/Enterprise vs. API); anonymization before upload. Practical, not legal
  theory: a "smíte / nesmíte / zeptejte se" table.

### Sekce 3 — Příprava dat (Markéta) — rung 2, biggest rewrite
- **Cut:** CoffeeCloud demo (breaks the DataCorp thread), "jak rychle běží?" optimality framing
  (irrelevant at 1000 rows), the "AI navrhne skript v chatu, spusťte ho někde" flow.
- **New demo:** lecturer points Cowork/Work at the DataCorp *folder*; asks it to survey data
  quality across the files and propose cleaning; narrates supervision (approve/reject steps).
- **New SP3:** students point their own desktop agent at the DataCorp folder and:
  1. have it propose cleaning steps (iterate on the proposal),
  2. have it apply them, producing a **cleaned CSV + a cleaning log** (what changed and why),
  3. include the computed `kategorie_mzdy` column (kept from the old assignment),
  4. **hand-verify 2–3 of its fixes** against the raw data.
  Assessment questions: do you trust the log? what did it silently decide for you?
- Fallback path printed on the SP3 slide: Colab Data Science Agent, or pair with a neighbor.

### Intermezzo 3a — Colab a Python (Šimon)
- Ordering is now correct (SP3 no longer requires running Python; 3a prepares SP4).
- **Fix broken slide:** `class Counter` with bare annotations + kwargs construction raises
  `TypeError`; rewrite with `pydantic.BaseModel` (which is what SP4 uses anyway).
- **Cut:** async/Semaphore slide (a plain loop with a progress bar handles 70 rows; the jump from
  "co je proměnná" to `asyncio` in five slides serves nobody).
- **Add:** "Jak číst a ověřit vygenerovaný kód" — read top-to-bottom, name what each block touches,
  spot-check one transformation, ask the model to explain a line you don't believe.
- Keep: variables/conditions, lists/loops, API + instructor, structured outputs, use-cases.

### Sekce 4 — Samotná analýza (Šimon) — Colab + API + eval
- Keep the lecture core: descriptive/diagnostic questions, where AI helps vs. misleads, zlaté
  pravidlo, "první odpověď je neúplná" example.
- **Cut:** "No-code vs. Code" demo (superseded by the ladder framing).
- **SP4 Fáze 1 (unchanged):** structured extraction from exit interviews + performance reviews
  (assignment-03c Úkoly 1–2).
- **SP4 Fáze 2 (rewritten): eval proti ground truth.**
  - `scripts/generate_datacorp.py` gains a ground-truth export (see §7).
  - Students score their extraction: accuracy / confusion matrix for exit-reason and sentiment.
  - **Bias probe:** does accuracy or sentiment shift for English-language or sarcastic reviews?
    (Both exist by design in the dataset.) Connects back to the governance block: this is *why*
    worker-evaluating AI is high-risk.
  - The old join-and-analyze questions (Úkol 3) compress to one: "does your measured error rate
    change any conclusion you'd present?"
- **Sharing moment:** whose extraction scored best; what (prompt, model, schema descriptions)
  made the difference. This is an eval-driven iteration loop in miniature.

### Demo blok — Terminálový agent (~10 min, lecturer only) — rung 3
- Takes the Transformers time slot, placed between Sekce 4 and 5.
- Claude Code (or Codex CLI) in the `notebooks/` folder, live on the **payroll reconciliation**
  task (old 03c Úkol 4): "zrekonciliuj datacorp_payroll_q3.xlsx proti datacorp.csv a napiš report".
- Narration = the point: what the agent reads, what it runs, what the lecturer checks, what they
  refuse to trust. Framed as "kam tohle směřuje" + same supervision skills as rung 2.

### Sekce 5 — Prezentace výsledků (Markéta) — rung 2
- Keep the four AI roles (oponent/překladatel/storyteller/partner) and SP5 framing.
- **Add the traceability step to SP5:** agent drafts the exec summary from the analysis; before
  presenting, the student traces **every number** in the summary back to a notebook cell or
  computation. A number with no source gets cut or flagged. ("AI zlepšuje formu, obsah je na vás"
  — now operationalized.)
- Add a 3–5 min live demo of AI-as-oponent (simulate the HR Business Partner's pushback).

### Bonus (self-study / if time remains)
- Keep: MCP slide, AI tools grid (refresh entries: desktop agents replace the image-generation
  card).
- **Replace** Custom GPT slide with Projects (ChatGPT/Claude) — persistent context + files.
- **Transformers deep-dive:** removed from live delivery, file kept as self-study appendix,
  marked as such on its section slide.

## 6. Bug/housekeeping fixes riding along

1. `slides/s3a-python.md`: broken `Counter` example (TypeError) → `BaseModel`.
2. Section ordering: no longer an issue after SP3 rewrite (Python-dependent task moved out).
3. Delete deprecated `notebooks/assignment-03.ipynb` and `assignment-03b.ipynb` (+ their
   README references, + `guardian_100.csv` if nothing else uses it).
4. Duplicate feedback-QR slide (slides.md and s6-bonus.md both end with it) → keep one.
5. Pomocníček GPT link points at the 2025-12 cohort slug → refresh per cohort (note in README).
6. Slide metadata: dates, course number (8176) — verify per cohort.

## 7. Ground truth export (generator change)

`scripts/generate_datacorp.py` must emit `notebooks/datacorp_ground_truth.csv` (or one file per
source dataset) containing, per record it already synthesizes:

- exit interviews: true primary reason (from the generator's category), true sentiment,
  language flag (cs/en).
- performance reviews: true sentiment, sarcasm flag, misassignment flag (review attached to the
  wrong employee).
- payroll Q3: per-row correctness flag + error type (wrong dept / wrong amount / EUR row).

Constraint: ground truth must not leak into the student-facing datasets; it ships as a separate
file loaded only in SP4 Fáze 2 (and it is fine that curious students can open it — the eval
happens after extraction is done).

Note: verify the generator actually derives its text from labeled categories (expected, since the
README describes deliberate sarcasm/misassignment); if any labels aren't currently retained,
retain them rather than re-labeling post hoc.

## 8. Prerequisite & fallback plan

**Pre-course checklist** (README section + email to students):
1. Paid ChatGPT (Plus+) *or* Claude (Pro+) subscription.
2. Desktop app installed (ChatGPT desktop app with Work/Codex, or Claude Cowork).
   - **Windows caveat:** Cowork's sandbox requires Hyper-V (Windows Pro/Enterprise/Education;
     **not Windows Home**). Windows Home + Claude → use ChatGPT instead, or plan on the Colab
     fallback.
3. One canned test task completed at home ("point the app at a folder with this test CSV and ask
   for a summary") — instructions + test file in the repo.
4. Google account for Colab (unchanged requirement) + OpenAI API key handling (unchanged).

**Day-of fallbacks**, printed on the SP3 slide: Colab Data Science Agent (free, browser-only) or
pairing with a neighbor. The smoke test in Blok 0 routes people to fallbacks before it matters.

## 9. Risks

| Risk | Mitigation |
|---|---|
| Prereq casualties (no subscription, Windows Home, install failures) | Blok 0 smoke test; Colab fallback; pairing; accepted residual risk per course decision |
| Vendor UI churn before delivery | Intent-based instructions, no button screenshots; lecturer dry-run 1–2 weeks before |
| Mixed vendors diverge in capability mid-exercise | Exercises specify outcomes (cleaned CSV + log), not steps; sharing moments absorb divergence |
| Eval math (confusion matrix) too heavy for beginners | Notebook pre-computes the scoring; students read it, they don't build it |
| Ground-truth refactor of generator is larger than expected | Scoped early (first implementation task); worst case, hand-label the ~70 exit interviews once |

## 10. Out of scope

- No change to course length, audience, language, or the CRISP-DM spine.
- No re-recording/re-shooting of existing visual assets except where slides change.
- No new datasets; DataCorp remains the single narrative.
- No commitment to a specific vendor; no API-key redesign.

## 11. Open questions (for review)

1. Does Markéta sign off on the Sekce 3 rewrite (it's her section and the largest teaching change)?
2. SP5 traceability: strict rule ("každé číslo má zdroj, jinak ho škrtněte") or soft guidance?
3. Keep `guardian_100.csv` for anything, or delete with the deprecated notebooks?
4. Pomocníček GPT: update instructions for the new SP3/SP4 flows — who owns that?
