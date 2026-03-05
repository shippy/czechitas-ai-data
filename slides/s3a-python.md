---
layout: section
subtitle: "Google Colab a základy Pythonu pro práci s AI"
---

# Intermezzo: Colab a Python

---

# Google Colab (Notebook)

- Online prostředí pro psaní a spouštění Pythonového kódu
- **Není potřeba nic instalovat** — stačí prohlížeč a Google účet
- Kód se píše do tzv. „buněk" — lze jednoduše zkoušet, co funguje, a iterovat

<v-click>

<div class="callout">💡 Hlavní výhody AI v datové analýze se projevují při vlastním programování. Python je nejčastější, ale nikoliv jediný jazyk.</div>

</v-click>

<v-click>

Pokud jste nikdy neviděly programovací jazyk — nevadí! Zkuste to i tak.

</v-click>

---

# Rychlý úvod do Pythonu (1): Proměnné a podmínky

```python {1|2|3-4|all}
x = 1                        # proměnná x teď obsahuje 1
y = get_value_from_llm()     # proměnná y obsahuje výsledek funkce
if x == 0:                   # následující řádek proběhne jen, pokud x je 0
    print(y)
```

<v-clicks>

- **Proměnná** — pojmenované místo v paměti, kam si uložíte hodnotu
- **Funkce** — kus kódu, který můžete zavolat jménem (a dostat z něj výsledek)
- **Podmínka (`if`)** — kód na odsazeném řádku se provede, jen pokud je podmínka splněna

</v-clicks>

---

# Rychlý úvod do Pythonu (2): Seznamy a cykly

```python {1|2-3|5|7}
a = [1, 2, 3]
for item in a:
    print(item + 1)           # -> 2  3  4

b = [item + 1 for item in a]  # totéž, ale do proměnné

b.append(5)                   # přidám objekt do seznamu b
```

<v-clicks>

- **Seznam (`list`)** — umožňuje přiřadit více hodnot do jedné proměnné
- **For cyklus** — projde seznam jednu položku po druhé
- **List comprehension** (řádek 5) — zkrácený zápis cyklu, který vytvoří nový seznam
- **`.append()`** — metoda, která přidá prvek na konec seznamu

</v-clicks>

---

# Rychlý úvod do Pythonu (3): Struktury a typy

```python {1|2-5|7}
from typing import Literal
class Counter:
    count: int
    kind: Literal["puppy", "kitten"]
    members: list[str]

a = Counter(count=1, kind="puppy", members=["Punťa"])
```

<v-clicks>

- **Třída (`class`)** — sdruží více dat vedle sebe (a dá jim typy)
- **Typy** — `int` (číslo), `str` (text), `list[str]` (seznam textů)
- **`Literal`** — výčet povolených hodnot (zde jen `"puppy"` nebo `"kitten"`)

</v-clicks>

<v-click>

<div class="callout">💡 Tyto koncepty se nám budou hodit pro structured outputs a práci s AI přes API.</div>

</v-click>

---

# Přístup k AI přes API

- Přístup k „čistému" modelu — jen s naším zadáním (system prompt)
- Typicky přes **SDK** v konkrétním programovacím jazyku (např. Python)
- Vyžaduje tzv. **API klíč** pro danou službu

```python {1|2|3-7|all}
from openai import OpenAI
client = OpenAI()
cover_letter = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "user",
         "content": "Napiš mi motivační dopis do Bradavic."}
    ])
```

---

# Structured Outputs

- Definice toho, **jak chci, aby vypadal výstup** modelu
- Garance místo toho, abyste byly dány napospas náladám modelu
- Pydantic umožňuje přidat popis a validaci polí

```python {1|2-4|6-7|all}
from pydantic import BaseModel, Field
class User(BaseModel):
    name: str = Field(..., description="All parts of name")
    age: float

user = client.chat.completions.create(
    "Jmenuji se Šimon a je mi 33 let", response_model=User)
# => User(name="Šimon", age=33.0)
```

---

# K čemu se to hodí?

<v-clicks>

- **Syntetická data** — vygenerovat dataset se známou strukturou
- **Klasifikace** — delšího textu i jednotlivých řádků
- **Extrakce informací** — vytáhnout strukturovaná data z nestrukturovaného textu
- **Generování textu** — s dodržením všech náležitostí (formát, jazyk, tón)

</v-clicks>

<v-click>

<div class="callout">💡 Bylo toho moc? Nevadí — zeptejte se GPT pomocníčka nebo nás!</div>

</v-click>

---

# Bonus: Async (paralelní zpracování)

Když zpracováváme **desítky nebo stovky** záznamů, nechceme čekat na každý zvlášť:

```python {1-4|6-8|all}
import asyncio
SEM = asyncio.Semaphore(5)          # max 5 požadavků najednou
async def extract(text):
    async with SEM:                 # "počkej, až budeš na řadě"
        return await async_client.chat.completions.create(...)

results = await asyncio.gather(*[   # spustí vše najednou
    extract(row["text"]) for _, row in df.iterrows()
])
```

<v-clicks>

- **`async/await`** — „tohle může běžet na pozadí, zatímco čekám na odpověď"
- **`Semaphore`** — omezuje počet souběžných požadavků (abychom nepřetížili API)
- **`asyncio.gather`** — spustí všechny úkoly najednou a počká na výsledky

</v-clicks>

<v-click>

<div class="callout">💡 Nemusíte tomu rozumět do detailu — stačí vědět, že to existuje, a zkopírovat vzor z notebooku.</div>

</v-click>
