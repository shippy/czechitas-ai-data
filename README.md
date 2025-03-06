## Czechitas: AI v datové analýze

### Setup

#### Předpoklady

Vytvořte si [v Google AI Studiu API klíč pro Gemini](https://aistudio.google.com/apikey):

1. Klikněte na tlačítko "Create API key"
2. Zkopírujte si API klíč a uložte si ho do souboru `.env`

#### Na vlastním počítači (ve VSCode)

1. [Nainstalujte si `uv`](https://docs.astral.sh/uv/getting-started/installation/) a spusťte `uv sync`, který vám nainstaluje správný Python a všechny potřebné balíčky. V terminálu:

```bash
uv sync
```

2. Uložte si API klíč do proměnné `GOOGLE_API_KEY` v souboru `.env`:

```bash
GOOGLE_API_KEY="váš-api-klíč"
```

1. Otevřete si notebook ve VSCode. Alternativně si spusťte notebook v prohlížeči:

```bash
uv run --with jupyter jupyter lab notebooks/assignment-03.ipynb
```

#### V Google Colab

1. Otevřete daný notebook přímo v Google Colab:
    - [Úkol 3](https://colab.research.google.com/github/shippy/czechitas-ai-data/blob/main/notebooks/assignment-03.ipynb)
2. Spusťte si notebook v prohlížeči. Notebook by měl rozpoznat, že běží v Google Colab, a automaticky si doinstalovat všechny potřebné balíčky.
3. Klikněte na tlačítko "Secrets" v levé liště a přidejte předtím vytvořený API klíč do proměnné `GOOGLE_API_KEY` - buď "napřímo" přes "+ Add new secret", nebo přes "Gemini API keys" > "Import key from Google AI Studio".