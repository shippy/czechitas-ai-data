---
layout: section
subtitle: "Co se po mně vlastně chce?"
---

# Sekce 1: Porozumění zadání

---

# Porozumění zadání analýzy

Každý datový nebo AI projekt má svůj životní cyklus.
V tomto kurzu budeme vycházet z logiky tradiční metodologie **CRISP-DM**, která strukturuje analytickou práci od pochopení business cíle až po nasazení výsledků. Dnes z ní použijeme hlavně první fáze.

<div class="icon-grid cols-2" style="margin-top:1.5rem">
  <div class="icon-card"><div class="icon">💼</div><div class="label">Business Understanding<br><small style="font-weight:300;color:#666">Jaký problém má analýza skutečně řešit? Jaké rozhodnutí má podpořit?</small></div></div>
  <div class="icon-card"><div class="icon">🔢</div><div class="label">Data Understanding<br><small style="font-weight:300;color:#666">Jak tento problém převést do měřitelné a analyticky uchopitelné podoby?</small></div></div>
</div>

---

# Jak se naučíme přemýšlet, ještě než se podíváme na data?

**V této fázi rozvíjíme schopnost:**
- strukturovat analytický problém
- pracovat s nejistotou a neúplnými informacemi
- definovat datové požadavky
- formulovat pracovní hypotézy ještě před seznámením se s daty

---

# Framework pro strukturování problému

| | Business otázka | Datová otázka | Metrika | Potřebná data |
|---|---|---|---|---|
| Příklad | „Zákazníci nakupují méně." | „Snížil se meziročně průměrný počet objednávek na aktivního zákazníka?" | Počet objednávek v období / počet zákazníků s alespoň jednou objednávkou | orders, (order_id, customer_id, order_date), customers |
| Nebo | „Zákazníci nakupují méně." | „Snížila se průměrná útrata na zákazníka za období?" | Celkový obrat / počet aktivních zákazníků | orders (order_amount) |

---

# Jak může AI pomoci zpřesnit zadání

<div class="icon-grid">
  <div class="icon-card"><div class="icon">❓</div><div class="label">Vygenerovat doplňující otázky</div></div>
  <div class="icon-card"><div class="icon">📏</div><div class="label">Navrhnout metriky</div></div>
  <div class="icon-card"><div class="icon">💡</div><div class="label">Formulovat hypotézy</div></div>
  <div class="icon-card"><div class="icon">⚠️</div><div class="label">Identifikovat rizika interpretace</div></div>
  <div class="icon-card"><div class="icon">🔍</div><div class="label">Odhalit, jaká data chybí</div></div>
  <div class="icon-card"><div class="icon">✏️</div><div class="label">Přepsat vágní zadání do struktury</div></div>
</div>

---
layout: section
subtitle: "Seznamování a zpřesňování zadání · ~30 minut"
---

# Samostatná práce 1: Porozumění zadání

---

# Seznamte se!
- Jak se jmenuju?
- Odkud jsem?
- Co dělám, pracuju už v IT nebo datech?
- Proč tady jsem, co si chci z kurzu odnést

---

# Zadání

**Use-case: DataCorp s.r.o. - Analýza odměňování a výkonu zaměstnanců**

HR Business Partner: *„V rámci přípravy podkladů pro vedení potřebujeme vyhodnotit, zda současné mzdové nastavení napříč odděleními odpovídá jejich personální struktuře. Zaměřte se zejména na to, zda případné rozdíly v odměňování lze vysvětlit faktory jako délka zaměstnání, vzdělání nebo výkon zaměstnance."*

Dostanete dataset se záznamy jednotlivých zaměstnanců:
- zařazení do oddělení
- výše mzdy
- délka zaměstnání ve firmě
- dosažené vzdělání
- hodnocení výkonu

---

# Úkol

**Zpřesnění analytického zadání (ještě před otevřením dat)**

1) Jak byste samy postupovaly pro zpřesnění zadání?
   
2) Použijte ChatGPT jako sparring partnera:
- Nechte si pomoci vygenerovat doplňující otázky, navrhnout metriky, formulovat hypotézy

3) Porovnejte výstup ChatGPT s vaším návrhem
- Co AI doplnila? Kde naopak přemýšlí příliš obecně?

---
layout: section
---

# Samostatná práce 1 — konec
