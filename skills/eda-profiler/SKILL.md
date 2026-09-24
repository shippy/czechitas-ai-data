---
name: eda-profiler
description: Použij při prvním kontaktu s novým datasetem — projde strukturovaný EDA checklist a posoudí kvalitu dat před jakoukoli analýzou.
---

# EDA profil datasetu

## Postup

1. **Popis**: Co je jeden řádek? Kolik řádků a sloupců? Jaká doména?
2. **Sloupce a typy**: projdi každý sloupec, urči typ (číslo/kategorie/datum/text) a zkontroluj, jestli hodnoty typu odpovídají (pozor na české formáty datumů a čísel).
3. **Chybějící hodnoty**: kolik, kde — a je v tom vzorec (chybí náhodně, nebo systematicky v jedné skupině)?
4. **Rozložení**: u číselných sloupců min/max/medián, odlehlé hodnoty, shluky; u kategorií četnosti a podezřelé varianty téže hodnoty („Vývoj" vs. „vývoj").
5. **Anomálie**: duplicity, nemožné hodnoty (plat 0, datum v budoucnosti), rozpory mezi sloupci.
6. **Náměty**: jaké analytické otázky by z dat šlo zodpovědět.

## Výstup

Strukturované shrnutí bodů 1–6 + **míra jistoty** u každého zjištění (jisté / podezření / nutno ověřit).

## Na co si dát pozor

- Nezastavuj se u prvního souhrnu — čísla ověř (ukaž konkrétní podezřelé řádky).
- Anomálie, kterou nenajdeš, neznamená, že tam není — vypiš i to, co jsi NEkontroloval.
