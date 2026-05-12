# DataCorp s.r.o. — Answer Key

Tento soubor je **pouze pro lektory**. Neměl by být dostupný studentům (žije jen na větvi `results`).

## Záměrně zasazené problémy v datech (dirt)

Studenti by je měli objevit v sekci 2 (EDA) a opravit v sekci 3 (čištění dat).

| Problém | Detail | Jak ověřit |
|---------|--------|------------|
| Nekonzistentní `oddeleni` | "Marketing" (119×), "marketing" (16×), "Mktg" (5×) | `df['oddeleni'].value_counts()` |
| Chybějící `plat` | 41 celkem, z toho 25 v Podpoře | `df['plat'].isna().sum()` |
| Smíšené formáty datumů | 101× DD.MM.YYYY, 910× YYYY-MM-DD | `df['datum_nastupu'].str.contains(r'^\d{2}\.')` |
| Odlehlé hodnoty platů | ~4 v Podpoře / HR (>200 000 Kč) | `df[df['plat'] > 150000]` |
| Duplicitní řádky | ~5 exact duplicates (z 10 plánovaných; novější dirt některé přepsala) | `df.duplicated().sum()` |
| Neplatné `hodnoceni_vykonu` | ~5 hodnot mimo rozsah 1–5 (hodnoty 0 nebo 6) | `df['hodnoceni_vykonu'].isin([0, 6]).sum()` |

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

### Výstupní rozhovory (`datacorp_exit_interviews.csv`, ~70 řádků po rozšíření)

- ~40 z Podpory, ~30 z ostatních oddělení
- Podpora: důvody clustered kolem "plat" (40 %) a "růst" (30 %)
- Ostatní oddělení: důvody rozloženy rovnoměrněji
- Extrakční cíl (Pydantic): kategorie důvodu odchodu, sentiment, doporučil/a by firmu

## Další záměrně zasazené problémy (rozšíření 2026-05)

Po rozšíření datasetu na ~1000 zaměstnanců a 4 nové soubory přibylo 18 dalších kategorií chyb v datech. Studenti by je měli postupně objevit při práci s `salary_history`, `org_chart`, `tickets`, a `payroll_q3.xlsx`.

| # | Problém | Detail | Jak ověřit |
|---|---------|--------|------------|
| 7 | Telefonní formáty (`datacorp.csv`) | 3 varianty (`+420 NNN NNN NNN`, `NNNNNNNNN`, `NNN NNN NNN`) + ~20 NaN + 5 neplatných (`???`, `viz Slack`) | `df['telefon'].str.match(...).value_counts()` |
| 8 | Email / jméno nesoulad | ~15 řádků, kde `employee_id` byl recyklován po reonboardingu | `df['email'].str.contains(df['jmeno'])` |
| 9 | Mezery a `\n` ve jménech | ~30 řádků s leading/trailing whitespace v `jmeno` nebo `prijmeni` | `df['jmeno'].str.match(r'^\s|\s$')` |
| 10 | Encoding mojibake | 3 řádky, kde diakritika je rozbitá (`Č`→`Ä` apod.) | `df['prijmeni'].str.contains('Ä')` |
| 11 | Smíchané desetinné oddělovače | ~10% řádků v `salary_history.plat_po` má comma-decimal s non-breaking space | `df['plat_po'].astype(str).str.contains(',')` |
| 12 | Datumová polévka (`salary_history`) | ISO + Czech (DD.MM.YYYY) + US (MM/DD/YYYY) + jen rok | `df['datum_zmeny'].str.match(...)` |
| 13 | Tečky/whitespace v `tickets.reporter_id` | ~10 řádků s `"234."` nebo `" 234"` | `df['reporter_id'].astype(str).str.match(r'\.|^\s|\s$')` |
| 14 | Silent ID collision (`salary_history`) | 1 záměrná kolize: 3 řádky jednoho zaměstnance přepsané na ID jiného | manuální kontrola |
| 15 | Diakritika-složené duplikáty | 1 dvojice (`Černý` ↔ `Cerny`) s odlišnými `employee_id` (~6014) | `df['prijmeni'].str.contains('Cerny')` |
| 16 | Datumy nástupu v budoucnosti | 5 řádků s datem v 2027–2028 | `df['datum_nastupu'].str.contains('2027|2028')` |
| 17 | Backdated correction (`salary_history`) | 2 řádky, jejichž `datum_zmeny` předchází předchozí změnu — chronologický sort ukáže "fantomový pokles platu" | sort by employee+date, hledat klesající `plat_po` |
| 18 | Plausible-wrong departments (`payroll`) | 3 řádky s `oddeleni` jiným než v `datacorp.csv`, ani jedno není provably wrong | merge na os_cislo, porovnej `oddeleni` |
| 19 | EUR currency landmine (`payroll`) | 4 řádky s `mzda_brutto` v ~1500–4000 (zjevně EUR, ne CZK) | `df['mzda_brutto'].between(1500, 4000)` |
| 20 | Sarkastické reviews | 5 reviews s `*kreativní*` / `*radost*` / `*originální*` — ironicky míněné | `df['review_text'].str.contains(r'\*\w+\*')` |
| 21 | Wrong-person reviews | 3 reviews, kde text se týká jiné osoby než `employee_id` | manuální čtení 161 reviews |
| 22 | Mixed-language exit interviews | 5 fragmentů kombinujících češtinu a angličtinu | `df['interview_text'].str.contains(r'\bbetter|opportunity\b')` |
| 23 | Self-contradicting exit interview | 1 záznam s rozporem (např. "platově byl spokojen" + "odchází kvůli penězům") | manuální čtení |
| 24 | Survivorship bias | ~15 zaměstnanců odešlo — jsou v `salary_history`, `reviews`, `exit_interviews`, ale ne v `datacorp.csv` | `set(history.employee_id) - set(main.employee_id)` |

## Úkol 4 — očekávané výsledky

**Plný dataset:** 4 řádky v EUR + 3 řádky se špatným oddělením.

**Vzorek 50 řádků s `random_state=5`:** 1 EUR řádek + 1 wrong-dept řádek (zaměstnanec 498: payroll=Vývoj, HR=Obchod).

**Očekávané chování LLM (gpt-5.4-mini se system promptem zmiňujícím CZK rozsah 25 000–150 000):**
- Oba landminy (EUR + wrong-dept) by měly být označeny jako `vážná`.
- Často také flagne řádky s `mzda_celkem ≠ mzda_brutto + bonus` (30 takových řádků v plném datasetu, typicky 1–2 ve vzorku) — to není záměrná chyba ze spec, ale legitimní finding.
- Aritmetické nesoulady padají často do `střední`, zřídka do `vážná`.
- `stejna_osoba` by mělo být téměř vždy `true` (merged frame párujeme přesně přes `os_cislo == employee_id`).

**Bez nápovědy o CZK rozsahu (diskusní otázka 2):** EUR landmine je často přehlédnut. To je očekávané a je smysl této otázky — ukázat, jak system prompt vede LLM k pozornosti.

**Škálování (diskusní otázka 3):** plnou populaci ~1000 řádků lze zlevnit přes
1. cheaper-first model (např. nano) pro pre-filtering podezřelých řádků
2. batch API call (více řádků v jednom requestu)
3. lokální rule-based heuristiky (range check na `mzda_brutto`, oddělení matchup) jako první vrstva
