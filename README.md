## Czechitas: AI v datové analýze

### Setup

#### Předpoklady

Od lektora získejte klíč k OpenAI API nebo si jej [vlastnoručně opatřete ze stránek OpenAI](https://platform.openai.com/api-keys).

#### V Google Colab

1. Otevřete daný notebook přímo v Google Colab:
    - [Úkol 3](https://colab.research.google.com/github/shippy/czechitas-ai-data/blob/main/notebooks/assignment-03.ipynb)
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
uv run --with jupyter jupyter lab notebooks/assignment-03.ipynb
```
