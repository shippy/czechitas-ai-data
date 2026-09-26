---
layout: section
subtitle: "Kam se podívat dál"
---

# Bonus: Témata k naťuknutí

---

# AI nástroje pro analytičky

<div class="icon-grid cols-2">
  <div class="icon-card"><div class="icon">📊</div><div class="label">Excel / Sheets Copilot<br><small style="font-weight:300;color:#666">Analýza dat, generování funkcí</small></div></div>
  <div class="icon-card"><div class="icon">📈</div><div class="label">Power BI Copilot<br><small style="font-weight:300;color:#666">Generování a vysvětlování DAX kódu</small></div></div>
  <div class="icon-card"><div class="icon">💻</div><div class="label">Programovací editory<br><small style="font-weight:300;color:#666">VSCode + Copilot, Cursor, Windsurf</small></div></div>
  <div class="icon-card"><div class="icon">🖥️</div><div class="label">Desktop agenti<br><small style="font-weight:300;color:#666">Claude Cowork, ChatGPT Work — agent nad vašimi soubory</small></div></div>
</div>

---

# Projects — trvalý kontext

- ChatGPT i Claude: **složka konverzací** se sdílenými soubory a instrukcemi
- Hodí se na opakovanou agendu — měsíční report, jeden dataset
- Nahrazuje dřívější Custom GPTs

**Příklady:**

- projekt na měsíční HR report — stejné instrukce, nová data
- projekt s firemní dokumentací jako trvalým kontextem

---

# Model-Context Protocol (MCP)

Definuje **interface pro nástroje** (JIRA, Google Drive, databáze…), které může AI „agenticky" použít.

<v-clicks>

- Editor nebo chatbot se připojí k MCP serveru
- Server zpřístupní nástroje (čtení souborů, SQL dotazy, API volání…)
- AI rozhodne, kdy a jak nástroj použít

</v-clicks>

<v-click>

Více informací: [modelcontextprotocol.io](https://modelcontextprotocol.io/)

</v-click>

---
layout: section
subtitle: "Když se s daty bavíte přirozeným jazykem"
---

# Bonus - Konverzační analytika

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

---
layout: section
subtitle: "Samostudium — projděte si doma, na kurzu neprezentujeme"
---

# Bonus: Transformery

---

# Transformer — architektura

<div style="display:flex;gap:2rem;align-items:flex-start;margin-top:0.5rem">
<div style="flex:1">

- Architektura založená na **neuronové síti**
- Výstup na základě **kontextu**, ve kterém se slovo nachází (**attention**)
- Klíčový paper: *„Attention is all you need"* (2017)

</div>
<div style="flex:1">
<img src="/transformer-architecture.png" class="h-80 mx-auto" />
</div>
</div>

---

# Krok 1: Tokenizace

Text se rozloží na **tokeny** — kousky slov, které model umí zpracovat.

<img src="/tokenization.png" class="w-140 mx-auto mt-8" />

<v-click>

Jeden token ≈ 3–4 znaky. Slovo „indivisible" se rozloží na víc tokenů.

</v-click>

---

# Krok 2: Embedding

Tokeny se převedou do **vektorového prostoru** — každé slovo má souřadnice.

<div style="display:flex;gap:2rem;align-items:center;margin-top:1rem">
<div style="flex:1">
<img src="/embedding-vectors.png" class="w-full" />
</div>
<div style="flex:1">

- Podobná slova mají **blízké vektory**
- Slavný příklad: *king - man + woman ≈ queen*
- Model tak „rozumí" vztahům mezi slovy

</div>
</div>

---

# Krok 3: Positional encoding

Model si zapamatuje **pozice tokenů** — ví, že „pes kousl člověka" ≠ „člověk kousl psa".

---

# Krok 4: Self-attention

Model analyzuje **okolní slova** a rozhodne, která jsou pro daný token důležitá.

<v-click>

Např. ve větě *„Bankovní karta byla zablokována"* — slovo „zablokována" se silně váže na „karta", ne na „bankovní".

</v-click>

---

# Krok 5: Generování výstupu

Model vygeneruje **nejpravděpodobnější další token** — a opakuje celý proces.

<v-click>

Celý cyklus: **tokenizace → embedding → positional encoding → self-attention → predikce** — dokola, token po tokenu.

</v-click>

---

# Encoder vs. Decoder

<div style="display:flex;gap:2rem;align-items:center;margin-top:1rem">
<div style="flex:1">
<img src="/encoder-decoder.png" class="w-full rounded-lg" />
</div>
<div style="flex:1">

| | Encoder (BERT) | Decoder (GPT) |
|---|---|---|
| **Směr** | Kouká oběma směry | Kouká jen dopředu |
| **Use-case** | Analýza textu, klasifikace | Generování textu, kódu |

<v-click>

GPT = **G**enerative **P**retrained **T**ransformer — stojí na decoderech navázaných za sebou.

</v-click>

</div>
</div>
