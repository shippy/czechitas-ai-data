---
name: vysvetli-kod
description: Použij, když dostaneš kód (Python, pandas, SQL) — typicky vygenerovaný AI — a potřebuješ pochopit, co dělá a co si ověřit, než výsledku uvěříš.
---

# Vysvětlení kódu

## Moje úroveň

*(Upravte podle sebe — tohle je jediná část, kterou je nutné přepsat.)*

Znám Excel (vzorce, kontingenční tabulky, SVYHLEDAT). Python a SQL přečtu jen s nápovědou.
→ Vysvětluj přes excelové ekvivalenty a každý odborný pojem při prvním výskytu přelož jednou větou.

## Postup

1. **Celek jednou větou**: co kód bere na vstupu a co vrací.
2. **Po blocích** (pár řádků, které dělají jednu věc): co blok dělá, jazykem podle mé úrovně výše.
3. **Předpoklady**: co kód tiše předpokládá o datech — význam a jednotky sloupců (cena za kus, nebo celkem?), formát datumů, žádné chybějící hodnoty.
4. **Místa k ověření**: řádky, kde se data mohou ztratit nebo zdvojit (filtr, `dropna`, `merge`/`JOIN`), natvrdo zadané hodnoty a každá agregace — sčítá se opravdu ta veličina, na kterou se ptám?
5. **Ruční kontrola**: navrhni 1–2 výpočty, které si ověřím sama (třeba v Excelu na pár řádcích), a jaký výsledek mám čekat.

## Výstup

Pět sekcí podle postupu, v tomto pořadí. Místa k ověření jako číslovaný seznam s odkazem na konkrétní řádek kódu.

## Na co si dát pozor

- Vysvětluj kód tak, jak je napsaný. Když se liší od toho, co zjevně *měl* dělat, pojmenuj rozdíl jako nález — kód nech beze změny, dokud o opravu nepožádám.
- „Běží bez chyby" není totéž co „počítá správně": součet nad špatným sloupcem proběhne bez jediné chybové hlášky.
- Kde si nejsi jistý, co kód na konkrétních datech udělá, řekni to a navrhni, jak to zjistit.
