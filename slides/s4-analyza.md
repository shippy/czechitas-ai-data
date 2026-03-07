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

# Fáze 1: No-code analýza (~15 min)

Vyberte si jednu otázku (nebo použijte vlastní ze sekce 2):

1. „Existuje rozdíl v platech mezi odděleními?"
2. „Souvisí délka zaměstnání s hodnocením výkonu?"
3. „Liší se platy podle vzdělání?"
4. Vaše vlastní otázka ze sekce 2

**Postup v ChatGPT:**

- Získejte první odpověď
- Zeptejte se: „Jak jsi to spočítal/a?"
- Položte aspoň jeden „what if" follow-up
- Udělejte screenshot klíčového zjištění

---

# Fáze 2: Code analýza (~15 min)

Stejná otázka, teď v Google Colabu:

- Nechte AI vygenerovat Python kód pro stejnou analýzu
- Spusťte ho, porovnejte výsledek s no-code odpovědí
- **Bonus:** Požádejte AI o vizualizaci nebo statistický test

---
layout: center
---

# Společné sdílení

- Daly no-code a code stejnou odpověď?
- Kterému způsobu víc důvěřujete? Proč?
- Změnil váš „what if" follow-up závěr?
