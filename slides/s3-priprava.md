---
layout: section
subtitle: "(Pre)processing, čištění, transformace dat"
---

# Sekce 3: Příprava dat

---
layout: center
---

## Otázka na vás - proč si data obecně připravujeme? :)

---

# Proč si data obecně připravujeme?

<v-click>

Aby naše analýza byla co nejpřesnější, vypovídající a odpovídala požadavkům zadavatele analýzy.

</v-click>

<v-click>

Opět platí zlaté **GIGO: Garbage In, Garbage Out**

</v-click>

<v-click>

Příprava dat zahrnuje:

- **Čištění dat** — nully, prázdné stringy, špatně formátované hodnoty…
- **Transformace dat** — přizpůsobení dat naší analýze: změna struktury, přidání sloupce, sloučení tabulek…

</v-click>

---

# Tradiční cesta přípravy dat (bez AI)

- Manuální EDA a tvorba čisticího / transformačního skriptu
- Dvojitá kognitivní zátěž: **správný** skript (dělá, co má) a **optimální** skript (běží efektivně)
- Sklon k reaktivnímu přemýšlení — „data se chovají takto, tak musím dát do skriptu toto"
- Dokumentace jako „nutné zlo" — každý důležitý krok by měl být zdokumentován, což se ne vždycky děje…

---

# Příprava dat s AI

- AI může připravit EDA skript
- AI může připravit **správný a optimální** transformační skript, případně zoptimalizovat váš skript
- Od reaktivního k **proaktivnímu** přemýšlení — „data se teď chovají takto, jak by se potenciálně mohla chovat v budoucnu?" (AI může navrhnout what-if scénáře)
- AI může dokumentovat kód za běhu, případně připravit přímo analytickou dokumentaci
- **Human-in-the-loop** je potřeba — ve finále zodpovídáte za správnost vy, ne AI :)

---
layout: section
---

# Pojďme si to ukázat (demo)

---

# Demo: Čištění dat pokladního systému

**Zadání:**

Pokladní systém sítě CoffeeCloud při exportu poškodil část dat. Potřebujeme mít připravena data pro analýzu tržeb. Nezajímá nás místo zakoupení / transakce.

**Analytický úkol:**

- Doplnění chybějících hodnot tam, kde se to dá
- Označení chybějících hodnot placeholderem `MISSING` tam, kde bez kontextu nemůžeme doplnit
- Pokud chybí datum transakce → nevyhodnotitelný záznam, zbavíme se jich
- Přidání sloupce `Validation`: hodnoty `"fixed"` nebo `"OK"`
- Ve výsledku chceme mít jen potřebné sloupce

---
layout: section
subtitle: "AI jako pomocník při přípravě dat · ~20 minut"
---

# Samostatná práce 3: Příprava dat

---

# Zadání

Připravte náš dataset DataCorp na základě předchozích zjištění pro další analýzu:

**Úkol 1 - nechte AI navrhnout úpravy:**
- obecný dotaz: ,,co bys v datech opravil, aby byla data použitelná pro další analýzu?"
- v další iteraci nechte AI návrhnout what-if scénáře

Nesouhlasíte s první verzí výstupu? Něco vám tam chybí? Iterujte.

Posuďte - **věříte výstupu / souhlasíte s ním? Proč ano? Proč ne?**

---

# Zadání 

Připravte náš dataset DataCorp na základě předchozích zjištění pro další analýzu:

**Úkol 2 - nechte AI navrhnout transformační skript (python) a zkuste si ho nad daty vyzkoušet**
- použijte vyiterované poznatky od AI z úkolu 1 v této sekci
- existuje požadavek do dat přidat počítaný sloupec `kategorie_mzdy`. Pokud je mzda nižší nebo rovna 35.000 Kč, je to ,,malá mzda", pokud je vyšší než 35.000 Kč a nižší nebo rovna 95.000 Kč, je to ,,střední mzda", pokud je vyšší než 95.000 Kč, je to ,,velká mzda"
- nechte AI do skriptu zaimplementovat jeden vybraný what-if scénář
- Pamatujte: chceme správný, optimální a zdokumentovaný kód

Posuďte - **Jak hodnotíte vygenerovaný skript? Dělá, co má? Jak rychle běží?**

---

# Zadání 

Připravte náš dataset DataCorp na základě předchozích zjištění pro další analýzu:

**Bonusový úkol - zkuste si sami napsat transformační skript, který data připraví do chtěné podoby (python / sql - co vám je příjemnější) a nechte si od AI váš skript zvalidovat z pohledu správnosti a optimálnosti**
- platí stejné požadavky jako v předchozím úkolu v této sekci

Posuďte - **Jak hodnotíte návrh na zlepšení skriptu? Přijde vám užitečný?**

---
layout: section
---

# Samostatná práce 3 — konec
