## Czechitas: AI v datové analýze

### Předpoklady pro účastnice

Před kurzem si projděte checklist ve složce [`precourse/`](precourse/README.md) — placený účet ChatGPT/Claude, desktopová aplikace, Google účet a krátký testovací úkol, kterým si ověříte, že vám všechno funguje.

### Datasety

#### DataCorp s.r.o. (HR dataset)

Syntetický dataset fiktivní české firmy "DataCorp s.r.o." — zaměstnanecká data pro výuku životního cyklu datové analýzy.

| Soubor | Obsah |
|--------|-------|
| `notebooks/datacorp.csv` | Hlavní strukturovaný dataset (~1000 řádků, 15 sloupců) — záměrně obsahuje chyby v datech |
| `notebooks/datacorp_reviews.csv` | Textové hodnocení výkonu (~150 záznamů) — nestrukturovaný text v češtině, některé záměrně sarkastické nebo přiřazené ke špatné osobě |
| `notebooks/datacorp_exit_interviews.csv` | Výstupní rozhovory (~70 záznamů) — nestrukturovaný text, místy v angličtině |
| `notebooks/datacorp_salary_history.csv` | Historie platových změn (~3000 řádků) — různé formáty datumů, občasné rozpory s hlavním datasetem |
| `notebooks/datacorp_org_chart.csv` | Organizační struktura (~1000+ řádků) — některé manažerské vazby tvoří cykly nebo míří na neexistující zaměstnance |
| `notebooks/datacorp_tickets.csv` | Interní IT/HR tickety (~5000 záznamů) — volný text, nekonzistentní kategorie, někdy špatná priorita |
| `notebooks/datacorp_payroll_q3.xlsx` | Mzdový list Q3 z Finance — Excel s nesourodým schématem, několika řádky v EUR a součtovým řádkem |
| `notebooks/datacorp_ground_truth_exits.csv` | Správné odpovědi pro eval v samostatné práci 4 (Fáze 2) — skutečné důvody odchodu, jazyk a rozpory v exit interviews |
| `notebooks/datacorp_ground_truth_reviews.csv` | Správné odpovědi pro eval v samostatné práci 4 (Fáze 2) — skutečný sentiment hodnocení, sarkasmus a záměny osob |
| `notebooks/datacorp_ground_truth_payroll.csv` | Správné odpovědi pro eval v samostatné práci 4 (Fáze 2) — typy chyb v jednotlivých řádcích mzdového listu |

Regenerace datasetu: `uv run scripts/generate_datacorp.py`

### Prezentace (slides)

Slides používají [Slidev](https://sli.dev/) a jsou ve složce `slides/`. Pro lokální spuštění:

```bash
cd slides
npm install
npm run dev
```

Pro build statické verze (výstup do `dist/`):

```bash
npm run build
```

### Setup

#### Předpoklady

Od lektora získejte klíč k OpenAI API nebo si jej [vlastnoručně opatřete ze stránek OpenAI](https://platform.openai.com/api-keys).

#### V Google Colab

1. Otevřete daný notebook přímo v Google Colab:
    - [Úkol 3c](https://colab.research.google.com/github/shippy/czechitas-ai-data/blob/main/notebooks/assignment-03c.ipynb)
2. Spusťte si notebook v prohlížeči. Notebook by měl rozpoznat, že běží v Google Colab, a automaticky si doinstalovat všechny potřebné balíčky.
3. Klikněte na tlačítko "Secrets" v levé liště a přidejte předtím vytvořený API klíč do proměnné `OPENAI_API_KEY` - přes "+ Add new secret"


#### Na vlastním počítači (ve VSCode)

1. [Nainstalujte si `uv`](https://docs.astral.sh/uv/getting-started/installation/) a spusťte `uv sync`, který vám nainstaluje správný Python a všechny potřebné balíčky. V terminálu:

```bash
uv sync
```

2. Uložte si API klíč do proměnné `OPENAI_API_KEY` v souboru `.env`:

```bash
OPENAI_API_KEY="váš-api-klíč"
```

1. Otevřete si notebook ve VSCode. Alternativně si spusťte notebook v prohlížeči:

```bash
uv run --with jupyter jupyter lab notebooks/assignment-03c.ipynb
```

### Údržba mezi kohortami

Odkaz na GPT pomocníčka (slug `chatgpt.com/g/...`) je specifický pro každou kohortu — před novým během kurzu ho aktualizujte v `notebooks/assignment-03c.ipynb` a ve slides (`slides/s4-analyza.md`, `slides/s6-bonus.md`).
