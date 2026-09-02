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

```python {1-2|4-7|9|all}
from pydantic import BaseModel
from typing import Literal

class Counter(BaseModel):
    count: int
    kind: Literal["puppy", "kitten"]
    members: list[str]

a = Counter(count=1, kind="puppy", members=["Punťa"])
```

<v-clicks>

- **`BaseModel`** — sdruží více dat vedle sebe a **zkontroluje typy při vytvoření**
- **Typy** — `int` (číslo), `str` (text), `list[str]` (seznam textů)
- **`Literal`** — výčet povolených hodnot (zde jen `"puppy"` nebo `"kitten"`)

</v-clicks>

<v-click>

<div class="callout">💡 Přesně tohle použijeme pro structured outputs — model musí vrátit data v této struktuře.</div>

</v-click>

---

# Přístup k AI přes API

- Přístup k „čistému" modelu — jen s naším zadáním (system prompt)
- Typicky přes **SDK** v konkrétním programovacím jazyku (např. Python)
- Vyžaduje tzv. **API klíč** pro danou službu

```python {1|2|3-6|all}
import instructor
client = instructor.from_provider("openai/gpt-5.4-mini")
cover_letter = client.create(
    messages=[
        {"role": "user",
         "content": "Napiš mi motivační dopis do Bradavic."}
    ], response_model=str)
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

user = client.create(
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

---

# Jak číst a ověřit vygenerovaný kód

<v-clicks>

- Čtěte **shora dolů** — u každého bloku si řekněte, kterých sloupců se dotýká
- **Jeden krok přepočítejte ručně** — stačí 2–3 řádky dat
- Nevěříte řádku? Zeptejte se: „Vysvětli, co tenhle řádek dělá a proč."
- Chtějte **souhrn změn** — počty řádků před a po každém kroku

</v-clicks>

<v-click>

<div class="callout">💡 Nemusíte umět kód napsat — musíte ho umět zkontrolovat. Zodpovědnost za výsledek zůstává na vás.</div>

</v-click>
