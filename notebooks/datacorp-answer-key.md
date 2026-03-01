# DataCorp s.r.o. — Answer Key

Tento soubor je **pouze pro lektory**. Neměl by být dostupný studentům (žije jen na větvi `results`).

## Záměrně zasazené problémy v datech (dirt)

Studenti by je měli objevit v sekci 2 (EDA) a opravit v sekci 3 (čištění dat).

| Problém | Detail | Jak ověřit |
|---------|--------|------------|
| Nekonzistentní `oddeleni` | "Marketing" (51×), "marketing" (15×), "Mktg" (5×) | `df['oddeleni'].value_counts()` |
| Chybějící `plat` | 40 celkem, z toho 25 v Podpoře | `df['plat'].isna().sum()` |
| Smíšené formáty datumů | 103× DD.MM.YYYY, 407× YYYY-MM-DD | `df['datum_nastupu'].str.contains(r'^\d{2}\.')` |
| Odlehlé hodnoty platů | 2× v Podpoře (~226k, ~247k), 2× v HR (~231k, ~236k) | `df[df['plat'] > 150000]` |
| Duplicitní řádky | 10 přesných duplikátů | `df.duplicated().sum()` |
| Neplatné `hodnoceni_vykonu` | 8 hodnot mimo rozsah 1–5 (hodnoty 0 nebo 6) | `df['hodnoceni_vykonu'].isin([0, 6]).sum()` |

## Záměrně zasazené analytické signály

Studenti by je měli najít v sekci 4 (analýza).

### 1. Reálný rozdíl v platech mezi odděleními

Mediány platů po odděleních:

| Oddělení | Medián platu |
|----------|-------------|
| Vývoj | ~77 000 Kč |
| Finance | ~71 000 Kč |
| Obchod | ~63 000 Kč |
| HR | ~56 000 Kč |
| Marketing | ~55 000 Kč |
| Podpora | ~40 500 Kč |

Rozdíl Vývoj vs Podpora je reálný — odráží rozdílnou kvalifikaci a trh práce.

### 2. Zdánlivý rozdíl Marketing vs Obchod

Obchod má vyšší mediánový plat než Marketing (~63k vs ~55k). **Ale:** Obchod má extra bonus za senioritu (`tenure * 800`), takže po kontrole na délku zaměstnání se rozdíl výrazně zmenší. Toto je klíčový moment pro výuku — "první odpověď není finální."

### 3. Korelace tenure ↔ výkon

Slabá pozitivní korelace (r ≈ 0.2–0.3). Hodnocení výkonu = `3.0 + 0.15 * roky_tenure + šum`. Studenti by měli najít trend, ale ne příliš silný.

### 4. Vzdělání ↔ plat (s výjimkami)

VŠ Mgr. dostává bonus ~8 000 Kč, PhD ~12 000 Kč. **Ale:** V Obchodu existují výjimky — ~15 % SŠ obchodníků má plat 70–95k (úspěšní obchodní zástupci). Studenti by měli najít celkový trend i výjimky.

### 5. Vysoká fluktuace v Podpoře

Podpora má průměrnou délku zaměstnání ~2 roky (ostatní oddělení ~3–4.5 roku). Potvrzeno výstupními rozhovory — většina odchází kvůli platu a chybějícímu kariérnímu růstu.

## Nestrukturovaná data

### Hodnocení výkonu (`datacorp_reviews.csv`, 79 řádků)

- Propojeno přes `employee_id`
- Sentiment koreluje s `hodnoceni_vykonu`, ale ne dokonale
- ~15 % zaměstnanců s vysokým skóre má smíšený/kritický review (šéf dává dobré hodnocení, ale píše upřímnou zpětnou vazbu)
- Extrakční cíl (Pydantic): sentiment, silné stránky, slabé stránky, doporučená akce

### Výstupní rozhovory (`datacorp_exit_interviews.csv`, 35 řádků)

- 20 z Podpory, 15 z ostatních oddělení
- Podpora: důvody clustered kolem "plat" (40 %) a "růst" (30 %)
- Ostatní oddělení: důvody rozloženy rovnoměrněji
- Extrakční cíl (Pydantic): kategorie důvodu odchodu, sentiment, doporučil/a by firmu
