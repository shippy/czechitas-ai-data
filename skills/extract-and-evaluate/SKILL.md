---
name: extract-and-evaluate
description: Použij, když je potřeba z nestrukturovaného textu (recenze, rozhovory, tickety) vytáhnout strukturovaná data — a změřit, jak spolehlivě.
---

# Strukturovaná extrakce s měřením přesnosti

## Postup

1. Prohlédni **vzorek textů** (5–10 kusů) a navrhni schéma: jaká pole, jaké kategorie (uzavřený výčet, ne volný text), jaké popisy polí.
2. Definuj schéma formálně (např. Pydantic model s `Literal` kategoriemi a `Field(description=...)`).
3. Extrahuj všechny záznamy.
4. **Změř přesnost**: na označeném vzorku (ground truth, nebo ručně označ 20–30 záznamů) spočítej accuracy a confusion matrix.
5. Prozkoumej chyby: jsou náhodné, nebo systematické (jiný jazyk, sarkasmus, nejednoznačné kategorie)? Podle toho iteruj prompt/schéma/model.

## Výstup

Strukturovaný dataset + naměřená chybovost (ne odhad od oka) + poznámka, kde model systematicky selhává.

## Na co si dát pozor

- Extrakci bez změřené chybovosti nenasazuj — „vypadá to dobře" není měření.
- Neshoda u nejednoznačných kategorií (neutrální vs. smíšené) může být chyba definice, ne modelu.
- Systematická chyba u podskupiny (jazyk, styl) = bias — u dat o lidech zvlášť závažné.
