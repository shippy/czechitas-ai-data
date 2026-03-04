---
layout: section
subtitle: "Trocha teorie, než se pustíme do praxe"
---

# Úvod do AI

---

# Od strojového učení k LLM

<div style="display:flex;gap:2rem;align-items:center">
<div style="flex:3">
<div class="icon-grid">
  <div class="icon-card"><div class="icon">🤖</div><div class="label">Strojové učení (ML)<br><small style="font-weight:300;color:#666">Algoritmy trénované na datech</small></div></div>
  <div class="icon-card"><div class="icon">🧠</div><div class="label">Hluboké učení (DL)<br><small style="font-weight:300;color:#666">Neuronové sítě napodobující mozek</small></div></div>
  <div class="icon-card"><div class="icon">💬</div><div class="label">Velké jazykové modely (LLM)<br><small style="font-weight:300;color:#666">GPT, Claude, Gemini…</small></div></div>
</div>
</div>
<div style="flex:2">
<img src="/neural-network.png" class="w-full" />
</div>
</div>

<v-click>

Pro nás důležité: LLM umí **rozumět textu** a **generovat text** (i kód, SQL, vizualizace…).

</v-click>

---

# Jak se LLM trénují

<div style="display:flex;gap:2rem;align-items:center;margin-top:1rem">
<div style="flex:1">
<img src="/llm-training.png" class="w-full rounded-lg" />
</div>
<div style="flex:1">

1. **Self-supervised learning** — LLM přečte obrovské množství textu z internetu a učí se predikovat další slovo

2. **Supervised fine-tuning** — lidé ho naučí odpovídat ve formátu otázka → odpověď

3. **RLHF** — lidé hodnotí odpovědi a model se učí, co je „dobrá" odpověď

</div>
</div>

---

# Jak o LLM přemýšlet

<div style="display:flex;gap:2rem;align-items:flex-start;margin-top:1rem">
<div style="flex:1">

- LLM **přečetl celý internet** před několika měsíci a pamatuje si ho, *zhruba*

- Vy teď můžete do jeho **kontextového okna** napsat, co vás trápí

- Do kontextového okna můžou přidat obsah i **nástroje** — vyhledávání, nahraný soubor, výsledek kódu

- LLM statisticky predikuje **nejpravděpodobnější další slovo**

</div>
<div style="flex:1">
<img src="/context-window.png" class="w-full rounded-lg" />
</div>
</div>

---

# Kontextové okno

**Kontextové okno** = vše, co LLM „vidí" při generování odpovědi.

<v-clicks>

- **Systémový prompt** — instrukce, které nastavují chování (např. „Jsi datový analytik")
- **Vaše zpráva** — otázka, úkol, data
- **Nástroje** — vyhledávání, nahraný soubor, výsledek kódu
- **Předchozí konverzace** — LLM si pamatuje jen to, co je v okně

</v-clicks>

<v-click>

<div class="callout warning">⚠️ Když je konverzace příliš dlouhá, starší zprávy z okna „vypadnou" — LLM je zapomene.</div>

</v-click>

---

# Není to jen ChatGPT

<div style="display:flex;gap:2rem;align-items:flex-start">
<div style="flex:3">

| Model | Výrobce | Silné stránky |
|-------|---------|---------------|
| **ChatGPT** (GPT-5.2/5.3) | OpenAI | Nejrozšířenější, dobrý all-rounder |
| **Claude** | Anthropic | Dlouhý kontext, pečlivé instrukce |
| **Gemini** | Google | Integrace s Google ekosystémem |
| **Llama** | Meta | Open-source, lokální běh |

<v-click>

Každý model má jiné silné stránky. **Vyzkoušejte víc než jeden** — zvlášť pro datovou analýzu.

</v-click>

</div>
<div style="flex:2">
<img src="/llm-tree.png" class="w-full rounded-lg" style="margin-top:0.5rem" />
</div>
</div>

---
layout: section
subtitle: "Jak se s AI efektivně bavit"
---

# Prompt engineering

---

# GIGO: Garbage In, Garbage Out

Kvalita výstupu závisí na kvalitě vstupu.

<v-click>

**Špatný prompt:**

<div class="chat-prompt">Analyzuj data</div>

</v-click>

<v-click>

**Lepší prompt:**

<div class="chat-prompt">Jsi datový analytik. Mám dataset s 500 zaměstnanci (plat, oddělení, hodnocení). Najdi, jestli existuje statisticky významný rozdíl v platech mezi odděleními. Použij box plot a ANOVA test.</div>

</v-click>

---

# Jak psát dobré prompty

<div class="icon-grid">
  <div class="icon-card"><div class="icon">🎭</div><div class="label">Vytvořte roli<br><small style="font-weight:300;color:#666">„Jsi expert na SQL…"</small></div></div>
  <div class="icon-card"><div class="icon">🎯</div><div class="label">Buďte konkrétní<br><small style="font-weight:300;color:#666">Přesný úkol, ne vágní zadání</small></div></div>
  <div class="icon-card"><div class="icon">📐</div><div class="label">Strukturujte prompt<br><small style="font-weight:300;color:#666">Odrážky, sekce, formát</small></div></div>
  <div class="icon-card"><div class="icon">📎</div><div class="label">Přidejte kontext<br><small style="font-weight:300;color:#666">Data, příklady, omezení</small></div></div>
  <div class="icon-card"><div class="icon">📋</div><div class="label">Specifikujte výstup<br><small style="font-weight:300;color:#666">Formát, délka, jazyk</small></div></div>
  <div class="icon-card"><div class="icon">🔄</div><div class="label">Iterujte<br><small style="font-weight:300;color:#666">Follow-up otázky zpřesní výsledek</small></div></div>
</div>

---

# Zero-shot vs. few-shot

| Technika | Popis | Kdy použít |
|----------|-------|------------|
| **Zero-shot** | Žádný příklad výstupu | Jednoduché úkoly |
| **One-shot** | Jeden příklad | Specifický formát |
| **Few-shot** | Více příkladů | Složitý nebo nestandardní výstup |

<v-click>

**Příklad few-shot promptu:**

<div class="chat-prompt" style="font-size:0.85em">Klasifikuj názvy sloupců podle typu.<br>Příklady: `vek` → numerický, `jmeno` → text, `datum_nastupu` → datum<br>Klasifikuj: `plat`, `oddeleni`, `hodnoceni_score`, `email`</div>

</v-click>
