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
---

# Ukázka: Stejná otázka, dva způsoby

„Existuje rozdíl v platech mezi odděleními?"

---

# Způsob 1: No-code (ChatGPT)

1. Nahrát vyčištěný dataset
2. Zeptat se přímo
3. AI vytvoří graf + shrnutí
4. Follow-up: „Je ten rozdíl statisticky významný?"
5. Follow-up: „Změní se, když vezmu v úvahu délku zaměstnání?"

→ Odpověď se vyvíjí s každým follow-upem

---

# Způsob 2: Code (Google Colab)

1. Stejná otázka: „Napiš mi Python kód, který tohle zodpoví"
2. Spustit v Colabu, podívat se na výstup
3. Co tím získáme:
   - **Reprodukovatelnost** — můžu to spustit znovu zítra
   - **Transparentnost** — vidím přesně, co se počítalo
   - **Sdílitelnost** — můžu poslat notebook šéfovi

---

# Kdy který způsob?

| No-code (ChatGPT) | Code (Colab) |
|--------------------|--------------|
| Rychlý průzkum | Cokoliv, co musíte obhájit |
| Sanity check | Cokoliv, co se opakuje |
| „Stojí tohle za zkoumání?" | Cokoliv, co předáváte dál |

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

# Fáze 2: Propojení a analýza (~15 min)

Strukturovaná data z Fáze 1 spojte s hlavním datasetem přes `employee_id` a odpovězte:

- **Úkol 3.1**: Které oddělení má nejvíc negativních exit interviews?
- **Úkol 3.2**: Koreluje sentiment review s výší platu nebo hodnocením výkonu?
- **Úkol 3.3**: Jaké jsou nejčastější důvody odchodu? Vytvořte graf.

**Bonus, pokud zbude čas:** Úkol 4 (rekonciliace mzdového listu z Excelu) nebo úprava Pydantic modelu — viz konec notebooku.

---
layout: center
---

# Společné sdílení

- Která z tří otázek měla překvapivou odpověď?
- Vrátil LLM někdy nesmyslnou strukturu? Co s tím?
- Jak moc záleží na system promptu — kdo zkusil změnit instrukci a co se stalo?
