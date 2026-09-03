---
layout: section
subtitle: "Techniky pro vyhodnocení dat a podpůrná asistence AI"
---

# Sekce 4: Samotná analýza

---

# Od průzkumu k odpovědím

V sekci 2 jste se ptaly: **„Co v datech je?"**

Teď se ptáte: **„Je X pravda?"**

To je zásadně jiný režim — ne otevřený průzkum, ale ověřování hypotéz.

---

# Typy analytických otázek

| Typ | Příklad (DataCorp) | Co potřebujete |
|-----|---------------------|----------------|
| **Deskriptivní** | „Jaký je medián platu podle oddělení?" | Agregace, seskupení |
| **Diagnostická** | „Proč má oddělení X nižší hodnocení?" | Porovnání, drill-down |
| **Prediktivní** | „Kdo pravděpodobně odejde?" | Modelování (bonus) |

Většina datových analytiček žije v deskriptivních + diagnostických otázkách. Na ty se dnes zaměříme.

---

# Kde AI pomáhá

AI je skvělé na **mechaniku** analýzy:

- Správný group-by
- Správný typ grafu
- Správný statistický test
- Kód, který byste jinak psaly 20 minut

---

# Kde AI zavádí

AI je nebezpečné, když **vypráví příběh** z výsledků:

- Sebevědomě vysvětlí vzorec, i když je to náhoda
- Nabídne kauzální vysvětlení, i když jde jen o korelaci
- Vydá první odpověď za finální odpověď

---
layout: center
---

# Zlaté pravidlo

Vždy se zeptejte:

**„Jak jsi to spočítal/a?"**

a

**„Co by mohlo tento závěr vyvrátit?"**

---

# Jak ověřit, co AI spočítalo

<v-clicks>

- **Zkontrolujte kód** — požádejte AI: „Vysvětli mi krok po kroku, co tento kód dělá"
- **Spot-check čísla** — vezměte 2–3 řádky a spočítejte ručně, jestli sedí
- **Porovnejte výstupy** — zkuste stejný dotaz v jiném modelu nebo jinak formulovaný
- **Ověřte okrajové případy** — co když je hodnota nulová, chybějící nebo extrémní?

</v-clicks>

<v-click>

<div class="callout">💡 Nemusíte rozumět každému řádku kódu. Stačí umět ověřit, že výsledek dává smysl.</div>

</v-click>

---

# Proč nestačí první odpověď

<div class="chat-prompt">Existuje rozdíl v platech mezi odděleními?</div>

<v-click>
<div class="chat-response">Ano! Marketing má o <strong>15 000 Kč</strong> nižší medián než Vývoj.</div>
</v-click>

<v-click>
<div class="chat-prompt">Změní se to, když vezmu v úvahu senioritu?</div>
</v-click>

<v-click>
<div class="chat-response">Rozdíl se zmenší na <strong>4 000 Kč</strong> a není statisticky významný.</div>
</v-click>

<v-click>

> **První odpověď nebyla špatná — byla neúplná. Úkolem analytičky je dostat se za první odpověď.**

</v-click>

---
layout: section
subtitle: "~30 minut + 5 minut společné sdílení"
---

# Samostatná práce 4: Analýza dat

---

# Vyzkoušejte si: assignment-03c

<div class="flex justify-around items-start mt-8">

<QRCode url="https://colab.research.google.com/github/shippy/czechitas-ai-data/blob/main/notebooks/assignment-03c.ipynb" :size="200">Notebook v Google Colab</QRCode>

<QRCode url="https://chatgpt.com/g/g-67cab661ae5c8191b0d8419c76d3959b-czechitas-ai-in-data-analytics-2025-12" :size="200">GPT pomocníček</QRCode>

</div>

<div class="callout mt-8">💡 Bylo toho moc? Nevadí — zeptejte se GPT pomocníčka nebo nás!</div>

---

# Fáze 1: Strukturovaná extrakce (~15 min)

V notebooku jsou tři textové datasety: hlavní `datacorp.csv`, **performance reviews** a **exit interviews**. Cílem je vytáhnout z volného textu strukturované informace pomocí Pydantic modelu.

- **Úkol 1**: Zpracujte všechny exit interviews — pro každý záznam hlavní důvod odchodu, sentiment a jednověté shrnutí.
- **Úkol 2**: Navrhněte si vlastní Pydantic model pro performance reviews (sentiment, silné/slabé stránky, doporučená akce…) a zpracujte všechny.

→ Notebook má hotovou ukázku — kopírujte vzor a upravujte.

---

# Fáze 2: Změřte svou extrakci (~15 min)

Dataset je syntetický — správné odpovědi známe (`datacorp_ground_truth_*.csv`). Porovnejte svou extrakci z Fáze 1 s realitou:

- **Úkol 3.1**: Accuracy + confusion matrix důvodů odchodu — kde se váš model plete?
- **Úkol 3.2**: Bias sonda — jak úspěšný je model u anglických a sarkastických textů?
- **Úkol 3.3**: „Změnila by naměřená chybovost nějaký závěr, který byste prezentovaly vedení?"

**Bonus, pokud zbude čas:** Úkol 4 (rekonciliace mzdového listu z Excelu) — viz konec notebooku.

---
layout: center
---

# Společné sdílení

- Čí extrakce skórovala nejlépe — a co rozhodlo? Prompt? Popisy polí? Model?
- Kde model selhával — sarkasmus? Angličtina?
- Co s tím říká governance slide ze sekce 2?

---
layout: section
---

# Demo: Agent v terminálu

Třetí stupeň žebříku

---

# Agent v terminálu: Claude Code / Codex CLI

Pustíme agenta nad složkou `notebooks/` a zadáme:

<div class="chat-prompt">Zrekonciliuj datacorp_payroll_q3.xlsx proti datacorp.csv a napiš report.</div>

<v-click>

Sledujte:

- **Co agent čte** — které soubory si otevřel sám?
- **Co spouští** — jaké příkazy a kód?
- **Co kontrolujeme** — a čemu nevěříme?

</v-click>

<v-click>

<div class="callout">💡 Stejné dovednosti dohledu jako u Cowork — jen víc autonomie. Třetí stupeň žebříku.</div>

</v-click>
