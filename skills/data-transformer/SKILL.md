---
name: data-transformer
description: Použij, když je potřeba vyčistit dataset s identifikovanými problémy — navrhne čisticí kroky, po schválení je provede a vede log změn.
---

# Čištění a transformace dat

## Postup

1. Shrň problémy nalezené v EDA (nebo je nejdřív zjisti — viz skill `eda-profiler`).
2. Navrhni **čisticí kroky — zatím nic neměň**. U každého kroku: co, proč, kolik řádků zasáhne.
3. Sporné kroky (mazání řádků, doplňování chybějících hodnot, hraniční případy) **nech explicitně schválit**.
4. Po schválení kroky proveď → vyčištěná data + **log změn**.
5. Nabídni ověření: 2–3 konkrétní opravené řádky před/po pro ruční kontrolu.

## Výstup

Vyčištěný soubor (CSV) + `cleaning_log.md`: co se změnilo, proč, kolik řádků před/po každém kroku.

## Na co si dát pozor

- Nikdy neměň data bez schválení kroků — zvlášť mazání a imputace.
- Hraniční hodnoty u kategorizací (≤ vs. <) vždy uveď explicitně v logu.
- „Běží bez chyby" není totéž co „dělá, co má".
