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
  <div class="icon-card"><div class="icon">🖼️</div><div class="label">Generování obrázků<br><small style="font-weight:300;color:#666">DALL-E, Midjourney — storytelling v datech</small></div></div>
</div>

---

# Custom GPT — vlastní AI pomocníček

- Dedikovaný GPT na specifickou oblast (jen s placeným ChatGPT Plus/Pro/Go)
- Můžete mu dát **vlastní instrukce** (systémový prompt) a **vlastní dokumenty**
- Lze sdílet s kolegy nebo komunitou

**Příklady:**

- GPT pro analýzu vašich interních dat
- GPT s firemní dokumentací
- Výukový bot na konkrétní doménu

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
subtitle: "Jak GPT vlastně vevnitř funguje?"
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
