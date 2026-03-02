---
layout: section
subtitle: "(Pre)processing, čištění, transformace dat"
---

# Sekce 3: Příprava dat

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

# Samostatná práce 3

---

# Zadání

**Use-case: Veterinární klinika se 3 pobočkami ve Středočeském kraji**

~5 000 klientů, ~8 000 zvířat, ~40 000 návštěv, 4 roky dat (od roku 2022)

Majitel říká: *„Zdá se mi, že klienti chodí méně často a kliniky nejsou tak vytížené jako dřív. Zjisti, co se děje v datech."*

**Úkol:** Využijte AI pro přípravu a vyčištění dat.

---
layout: section
---

# Samostatná práce 3 — konec
