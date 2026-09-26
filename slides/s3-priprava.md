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
- Dvojitá kognitivní zátěž: **správný** skript (dělá, co má) a **zdokumentovaný** postup (jde zpětně zkontrolovat)
- Sklon k reaktivnímu přemýšlení — „data se chovají takto, tak musím dát do skriptu toto"
- Dokumentace jako „nutné zlo" — každý důležitý krok by měl být zdokumentován, což se ne vždycky děje…

---

# Příprava dat s AI

- AI může připravit EDA skript
- AI může připravit **správný a zdokumentovaný** transformační skript, případně zkontrolovat váš skript
- Od reaktivního k **proaktivnímu** přemýšlení — „data se teď chovají takto, jak by se potenciálně mohla chovat v budoucnu?" (AI může navrhnout what-if scénáře)
- AI může dokumentovat kód za běhu, případně připravit přímo analytickou dokumentaci
- **Human-in-the-loop** je potřeba — ve finále zodpovídáte za správnost vy, ne AI :)

---
layout: section
---

# Pojďme si to ukázat (demo)

---

# Demo: Agent nad složkou DataCorp

Namíříme agenta (Claude Cowork / ChatGPT Work) na soubor s pokladními daty kavárny CoffeeCloud:

<v-clicks>

1. „Projdi soubory ve složce a shrň problémy s kvalitou dat."
2. „Navrhni čisticí kroky — zatím nic neměň."
3. Návrhy **schvalujeme / odmítáme** — agent provádí jen to schválené
4. Výstup: **vyčištěný CSV + log provedených změn**

</v-clicks>

<v-click>

<div class="callout">👀 Sledujte: co agent rozhodl sám, aniž se zeptal?</div>

</v-click>

---
layout: section
subtitle: "AI jako pomocník při přípravě dat · ~20 minut"
---

# Samostatná práce 3: Příprava dat

---

# Samostatná práce 3 (~20 min)

<div class="flex justify-between items-start gap-8">

<div>

Namiřte svého agenta (Claude Cowork / ChatGPT Work) na složku s DataCorp daty:

1. Stáhněte si data jako ZIP (QR vpravo) a rozbalte
2. Nechte agenta **navrhnout čisticí kroky** — nesouhlasíte? Iterujte
3. Nechte ho kroky **provést** → `datacorp_clean.csv` + `cleaning_log.md`
4. Přidejte počítaný sloupec `kategorie_mzdy`:
   - do 35 000 Kč včetně → „malá mzda"
   - do 95 000 Kč včetně → „střední mzda"
   - jinak → „velká mzda"
5. **Ručně ověřte 2–3 opravy** proti původním datům

</div>

<QRCode url="https://github.com/shippy/czechitas-ai-data/releases/download/datacorp-data/datacorp-data.zip" :size="150">Data ke stažení</QRCode>

</div>

---

# Posuďte + fallback

<v-clicks>

- **Věříte logu změn?** Proč ano? Proč ne?
- Co agent rozhodl **potichu za vás**?
- Co byste nechaly **schvalovat vždy**?

</v-clicks>

<v-click>

<div class="callout">🛟 Nefunguje vám agent? Fallback: Google Colab + Data Science Agent — nahrajte CSV a zadejte stejné zadání. Nebo pracujte ve dvojici.</div>

</v-click>

---

# Zapište postup jako skill `data-transformer`

Tenhle postup budete opakovat u každého dalšího čištění dat:

| Prvek skillu | Obsah |
|---|---|
| **Kdy použít** | Mám dataset s nečistotami a agenta, který ho může vyčistit |
| **Kroky** | 1) Shrň problémy z EDA · 2) Nech agenta navrhnout čisticí kroky — zatím nic neměnit · 3) Sporné kroky vyjasni (iteruj) · 4) Proveď → vyčištěná data + log změn · 5) Ověř 2–3 opravy proti původním datům |
| **Výstup** | Vyčištěný CSV + `cleaning_log.md` (co, proč, kolik řádků) |
| **Na co si dát pozor** | Co agent rozhodl potichu — hraniční hodnoty, mazání řádků, doplňování chybějících |

Posuďte - **Fungoval postup i na jiném zadání? Co jste musely doplnit?**

---
layout: section
---

# Samostatná práce 3 — konec
