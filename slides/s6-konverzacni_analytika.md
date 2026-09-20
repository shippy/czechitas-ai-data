---
layout: section
subtitle: "Když se s daty bavíte přirozeným jazykem"
---

# Konverzační analytika

---

# Co je konverzační analytika

Rozhraní, kde se **business uživatel ptá na data v přirozeném jazyce** a dostává odpověď — bez psaní SQL, bez čekání na analytika.

<div class="icon-grid cols-2" style="margin-top:1.5rem">
  <div class="icon-card"><div class="icon">💬</div><div class="label">Otázka v jazyce, ne v kódu<br><small style="font-weight:300;color:#666">„Jak se vyvíjely tržby podle regionu za Q1?"</small></div></div>
  <div class="icon-card"><div class="icon">🔗</div><div class="label">Napojení na governed data<br><small style="font-weight:300;color:#666">Ne na volný text — na řízený, ověřený datový zdroj firmy</small></div></div>
  <div class="icon-card"><div class="icon">📊</div><div class="label">Vizualizace + vysvětlení<br><small style="font-weight:300;color:#666">Odpověď obsahuje graf, tabulku i shrnutí v textu</small></div></div>
  <div class="icon-card"><div class="icon">🔁</div><div class="label">Konverzace, ne dotaz<br><small style="font-weight:300;color:#666">Můžete se ptát dál, nástroj si pamatuje kontext</small></div></div>
</div>

---

# Jak to funguje "pod kapotou"

1. Uživatel položí otázku v přirozeném jazyce
2. Nástroj ji převede na SQL/DAX dotaz nad firemními daty
3. Dotaz se spustí nad **řízeným** zdrojem (ne nad čímkoliv)
4. Výsledek se vrátí jako tabulka, graf a textové shrnutí

<div class="callout warning">⚠️ Přesnost silně závisí na tom, jak dobře je definovaná sémantická vrstva pod nástrojem — metriky, terminologie, business pravidla (pamatujete z ranní sekce?)</div>

---

# Kde se s tím dnes setkáte

| Nástroj | Firma | Kde běží |
|---|---|---|
| **Power BI Copilot** | Microsoft | uvnitř Power BI / Fabric |
| **Databricks Genie** | Databricks | nad lakehouse daty (Unity Catalog) |
| **Amazon Q in QuickSight** | AWS | uvnitř QuickSight |
| **Looker + Gemini** | Google | uvnitř Looker/BigQuery |

<v-click>

Všechny řeší stejný problém: **"poslední míli" datové demokratizace** — byznys se pořád musí ptát analytika, i když má dashboard.

</v-click>

---

# Není to "jen chatbot nad databází"

<div class="icon-grid cols-2">
  <div class="icon-card"><div class="icon">📖</div><div class="label">Business slovník<br><small style="font-weight:300;color:#666">Nástroj se učí terminologii firmy — synonyma, zkratky, výjimky</small></div></div>
  <div class="icon-card"><div class="icon">✅</div><div class="label">Ověřené odpovědi<br><small style="font-weight:300;color:#666">Analytici mohou "podepsat" správné odpovědi na časté otázky</small></div></div>
  <div class="icon-card"><div class="icon">🔒</div><div class="label">Governance<br><small style="font-weight:300;color:#666">Respektuje přístupová práva — kdo co smí vidět</small></div></div>
  <div class="icon-card"><div class="icon">🤔</div><div class="label">Nedeterministické<br><small style="font-weight:300;color:#666">Stejná otázka může dát mírně jinou odpověď — i výrobci to takto popisují</small></div></div>
</div>

---

# Kde jsou limity

- Vyžaduje **zralou datovou infrastrukturu** (řízený katalog dat) — bez ní konfigurace selže nebo dá nespolehlivé odpovědi
- Přesnost odpovědí je z velké části daná **kvalitou datového modelu**, ne jen kvalitou AI
- Pořád jde o **nedeterministický systém** — stejná otázka, mírně jiná odpověď podruhé
- Nenahrazuje analytika u komplexních/nejednoznačných otázek — zvládá hlavně opakované, dobře definované dotazy

<div class="callout warning">⚠️ Konverzační analytika je nadstavba nad dobrými daty, ne náhrada za jejich přípravu — proto jsme dnes strávili tolik času na EDA a čištění.</div>

---
layout: section
---

# Demo: Databricks Genie