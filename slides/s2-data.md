---
layout: section
subtitle: "Rozumím poskytnutým datům? Mám všechna potřebná data?"
---

# Sekce 2: Porozumění datům

---

# Co je EDA?

**Exploratory Data Analysis** — první věc, kterou s daty uděláte, než začnete odpovídat na otázky.

> *"It is important to understand what you CAN DO before you learn to measure how WELL you seem to have DONE it."*
> — John Tukey, 1977

Česky: Nejdřív pochopte, co máte. Teprve potom analyzujte.

---

# EDA checklist

Než začnete analyzovat, potřebujete znát:

- **Tvar:** Kolik řádků / sloupců? Co je jeden řádek = jeden co?
- **Sloupce:** Co znamenají? Jaké mají typy (číslo, kategorie, datum, text)?
- **Kvalita:** Chybějící hodnoty? Duplicity? Nekonzistentní formáty?
- **Rozložení:** Co je typické? Co je extrém? Existují shluky?
- **Vztahy:** Které sloupce spolu mohou souviset?

---

# Proč to nepřeskakovat

„Průměrný plat je 85 000 Kč" — zní rozumně.

…dokud nezjistíte, že 20 % platů chybí — a všechny jsou z jednoho oddělení.

**Bez EDA je každá analýza potenciálně nesmysl.**

---

# Jak to měníme s AI

| Tradičně | S AI |
|----------|------|
| `df.describe()`, `df.info()` | „Popiš mi tento dataset" |
| Ruční histogramy | „Ukaž mi rozložení platů" |
| Kontrola typů sloupců | „Jaké typy mají jednotlivé sloupce?" |
| Hledání chybějících hodnot | „Kde mi chybí data?" |

AI zrychluje mechaniku — ale ten checklist se nemění.

**Vy pořád musíte vědět, na co se ptát a kdy odpověď nevoní.**

---

# Než nahrajete data do AI

<div class="icon-grid cols-2">
  <div class="icon-card"><div class="icon">🔒</div><div class="label">Co se s daty stane?<br><small style="font-weight:300;color:#666">ChatGPT Free/Plus data může použít k trénování modelu</small></div></div>
  <div class="icon-card"><div class="icon">🏢</div><div class="label">Firemní data<br><small style="font-weight:300;color:#666">Citlivá data (platy, hodnocení) nahrávejte jen přes firemní plán (Team/Enterprise)</small></div></div>
  <div class="icon-card"><div class="icon">🛡️</div><div class="label">Anonymizace<br><small style="font-weight:300;color:#666">Odstraňte jména, rodná čísla a identifikátory, než data nahrajete</small></div></div>
  <div class="icon-card"><div class="icon">⚙️</div><div class="label">Nastavení<br><small style="font-weight:300;color:#666">V ChatGPT: Settings → Data Controls → vypněte trénování na vašich datech</small></div></div>
</div>

<v-click>

Dnes pracujeme s **fiktivním datasetem** — v praxi toto řešte s IT oddělením.

</v-click>

---
layout: section
---

# Ukázka: EDA jako rozhovor

Živá ukázka v ChatGPT s datasetem DataCorp s.r.o.

---

# Krok 1

<div class="chat-prompt">Co je tohle za dataset?</div>

<v-click>
<div class="chat-response">Dataset obsahuje 500 zaměstnanců firmy DataCorp s.r.o. s 12 sloupci: <strong>plat, oddělení, hodnocení, vzdělání…</strong></div>
</v-click>

<v-click>

Všimněte si: AI vám dá obecný souhrn. To je teprve *začátek*, ne konec.

</v-click>

---

# Krok 2

<div class="chat-prompt">Jaké sloupce mám a jaké jsou jejich typy?</div>

<v-click>
<div class="chat-response">Identifikuji <strong>5 numerických</strong>, <strong>4 kategorické</strong>, <strong>2 datumové</strong> a <strong>1 textový</strong> sloupec…</div>
</v-click>

<v-click>

Inventura sloupců — kontrolujte, jestli AI správně rozpoznalo typy.

<div class="callout warning">⚠️ Pozor na české formáty datumů — AI je občas špatně interpretuje.</div>

</v-click>

---

# Krok 3

<div class="chat-prompt">Kde mi chybí data?</div>

<v-click>
<div class="chat-response">Chybějící hodnoty: <strong>plat</strong> (20 %), <strong>hodnocení</strong> (5 %), <strong>vzdělání</strong> (2 %)…</div>
</v-click>

<v-click>

Mapa chybějících hodnot — kolik, kde, a je v tom vzorec?

</v-click>

---

# Krok 4

<div class="chat-prompt">Ukaž mi rozložení platů</div>

<v-click>
<div class="chat-response">Rozložení platů je bimodální s vrcholy kolem <strong>45 000 Kč</strong> a <strong>85 000 Kč</strong>…</div>
</v-click>

<v-click>

Histogram + komentář od AI. Jsou tam odlehlé hodnoty (outliery)? Shluky?

</v-click>

---

# Krok 5

<div class="chat-prompt">Co je v datech podezřelého nebo neobvyklého?</div>

<v-click>
<div class="chat-response">Identifikuji 3 anomálie: <strong>duplicitní ID</strong>, <strong>plat 0 Kč</strong>, a <strong>datum nástupu v budoucnosti</strong>…</div>
</v-click>

<v-click>

Najde AI všechny problémy? (Spoiler: pravděpodobně ne všechny.)

</v-click>

---

# Krok 6

<div class="chat-prompt">Jaké analytické otázky by šlo z těchto dat zodpovědět?</div>

<v-click>
<div class="chat-response">Navrhuji 5 směrů: <strong>platové rozdíly</strong>, <strong>vliv vzdělání</strong>, <strong>predikce odchodu</strong>…</div>
</v-click>

<v-click>

AI navrhne směry analýzy — základ pro sekci 4.

</v-click>

---

# Dvě poučení

**1. Vaše follow-up otázky jsou ta dovednost.**

AI vám dá generický první souhrn. Hodnota je v tom, že se ptáte dál. Tam žije expertíza analytičky, ne v AI.

**2. Důvěřuj, ale prověřuj.**

AI někdy špatně přečte formát, pomíchá si škálu 1–5 s procenty, nebo přehlédne duplicity. Vždycky se dívejte, jestli odpověď dává smysl.

---
layout: section
subtitle: "~25 minut + 5 minut společné sdílení"
---

# Samostatná práce 2: Poznáváme data

---

# Zadání

Nahrajte dataset DataCorp do ChatGPT a projděte tabulku otázek:

| Krok | Otázka pro AI | Na co se zaměřte |
|------|--------------|-------------------|
| 1 | „Popiš mi tento dataset" | Uhádlo AI správně doménu? |
| 2 | „Jaké sloupce mám?" | Dávají typy smysl? |
| 3 | „Jsou v datech chybějící hodnoty?" | Kde a kolik? |
| 4 | „Rozložení číselných sloupců" | Překvapení v distribucích? |
| 5 | „Co je v datech neobvyklého?" | Našlo AI všechny anomálie? |
| 6 | „Jaké otázky by šlo zodpovědět?" | Sbíráme pro sekci 4 |

---

# Váš úkol na konec

Zapište si:

- **3 věci**, které jste se o datech dozvěděly
- **2 otázky**, které byste chtěly dále prozkoumat

→ Budeme je potřebovat v sekci 4!

---
layout: center
---

# Společné sdílení

Našlo AI u všech stejné anomálie?

Pravděpodobně ne — dobrá ukázka toho, že AI je nedeterministické a proč se vyplatí dívat se na data z více stran.
