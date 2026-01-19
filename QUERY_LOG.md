# Verifiserte Spørringer

Denne filen logger DuckDB-spørringer som brukeren har bekreftet gir korrekte resultater. Bruk disse som referanse for lignende spørsmål.

Når en spørring er spesielt nyttig eller representerer et vanlig mønster, bør den promoteres til "DuckDB Query Patterns" i CLAUDE.md.

---

## Format

```
## Kategori: Kort beskrivelse

**Spørsmål:** Brukerens opprinnelige spørsmål
**Verifisert:** YYYY-MM-DD
**Promotert:** Nei

​```sql
-- SQL-spørringen som ga korrekt svar
SELECT ...
​```

**Resultat:** Kort oppsummering av hva spørringen returnerte
**Notater:** Eventuelle viktige detaljer om tolkning eller begrensninger
```

---

## Logg

### Ekom: Kontantkort-utvikling over tid

**Spørsmål:** "Gi meg utviklingen av kontantkort fra 2018 - 2024 på helårsbasis"
**Verifisert:** 2026-01-19
**Promotert:** Nei

```sql
SELECT
    ar as år,
    ROUND(SUM(svar) / 1000, 0) as tusen_ab
FROM 'lib/ekom.parquet'
WHERE hk = 'Mobiltjenester'
  AND dk = 'Mobiltelefoni'
  AND hg = 'Abonnement'
  AND n1 = 'Kontantkort'
  AND tp = 'Sum'
  AND sk IN ('Sluttbruker', 'Ingen')
  AND delar = 'Helår'
  AND ar BETWEEN 2018 AND 2024
GROUP BY ar
ORDER BY ar
```

**Resultat:** Nedgang fra 755k (2018) til 401k (2024), -47% over perioden
**Notater:** n1 = 'Kontantkort' for kontantkort, n1 = 'Fakturert' for fakturerte abonnement

---

### Abonnement: Fordeling etter adressetype

**Spørsmål:** "Kan du gi meg antall ab som du finner på adresser med hus"
**Verifisert:** 2026-01-19
**Promotert:** Nei

```sql
-- Hovedspørring: Antall ab på adresser med hus
SELECT COUNT(*) as antall_ab
FROM 'lib/ab.parquet' ab
JOIN 'lib/adr.parquet' a ON ab.adrid = a.adrid
WHERE ab.adrid > 0 AND a.hus > 0

-- Utvidet: Fordeling per kategori
SELECT
    CASE
        WHEN ab.adrid = 0 THEN 'Ikke koblet (adrid=0)'
        WHEN a.hus > 0 THEN 'Adresse med hus'
        ELSE 'Adresse uten hus'
    END as kategori,
    COUNT(*) as antall_ab
FROM 'lib/ab.parquet' ab
LEFT JOIN 'lib/adr.parquet' a ON ab.adrid = a.adrid
GROUP BY kategori
ORDER BY antall_ab DESC
```

**Resultat:** 2 207 941 ab på adresser med hus (87%), 315 817 på adresser uten hus, 12 460 ikke koblet
**Notater:** Filtrer på adrid > 0 for koblede ab. Adresser uten hus kan være næringsbygg, fritidsboliger, etc.

---

### Dekning: Fastbredbånd per hastighetsklasse per fylke

**Spørsmål:** "gi meg nå en tabell som har fylker og nasjonalt i første kolonne og de andre kolonnene skal være hastighet 30, 100, 500, 1000. Dette skal være basert på dekningen for alle tek og det skal være basert på husstander"
**Verifisert:** 2026-01-19
**Promotert:** Nei

```sql
WITH dekning AS (
    SELECT
        adrid,
        MAX(ned) as maks_ned
    FROM 'lib/fbb.parquet'
    GROUP BY adrid
),
per_adresse AS (
    SELECT
        a.fylke,
        a.hus,
        COALESCE(d.maks_ned, 0) as maks_ned
    FROM 'lib/adr.parquet' a
    LEFT JOIN dekning d ON a.adrid = d.adrid
),
per_fylke AS (
    SELECT
        fylke,
        SUM(CASE WHEN maks_ned >= 30000 THEN hus ELSE 0 END) as hus_30,
        SUM(CASE WHEN maks_ned >= 100000 THEN hus ELSE 0 END) as hus_100,
        SUM(CASE WHEN maks_ned >= 500000 THEN hus ELSE 0 END) as hus_500,
        SUM(CASE WHEN maks_ned >= 1000000 THEN hus ELSE 0 END) as hus_1000,
        SUM(hus) as totalt_hus
    FROM per_adresse
    GROUP BY fylke
),
resultat AS (
    SELECT
        fylke as Fylke,
        ROUND(hus_30 * 100.0 / totalt_hus, 1) as "30 Mbit",
        ROUND(hus_100 * 100.0 / totalt_hus, 1) as "100 Mbit",
        ROUND(hus_500 * 100.0 / totalt_hus, 1) as "500 Mbit",
        ROUND(hus_1000 * 100.0 / totalt_hus, 1) as "1000 Mbit"
    FROM per_fylke

    UNION ALL

    SELECT
        'NASJONALT' as Fylke,
        ROUND(SUM(hus_30) * 100.0 / SUM(totalt_hus), 1),
        ROUND(SUM(hus_100) * 100.0 / SUM(totalt_hus), 1),
        ROUND(SUM(hus_500) * 100.0 / SUM(totalt_hus), 1),
        ROUND(SUM(hus_1000) * 100.0 / SUM(totalt_hus), 1)
    FROM per_fylke
)
SELECT * FROM resultat
ORDER BY CASE WHEN Fylke = 'NASJONALT' THEN 1 ELSE 0 END, Fylke
```

**Resultat:** Nasjonal dekning: 30 Mbit 99.7%, 100 Mbit 99.1%, 500 Mbit 97.1%, 1000 Mbit 96.2%. Oslo høyest, Nordland lavest.
**Notater:** Bruker MAX(ned) per adresse for å finne beste tilgjengelige hastighet. Hastigheter i kbps (30 Mbit = 30000 kbps).

### Dekning: Alle teknologier per fylke (fbb + mob)

**Spørsmål:** "Kan du gi meg den fylkesfordelte dekning på alle teknologier (inkludert mob) - en tek pr kolonne - basert på husstander"
**Verifisert:** 2026-01-19
**Promotert:** Nei

```sql
WITH tek_per_adresse AS (
    SELECT adrid, tek FROM 'lib/fbb.parquet'
    UNION
    SELECT adrid, tek FROM 'lib/mob.parquet'
),
dekning AS (
    SELECT
        a.fylke,
        a.adrid,
        a.hus,
        MAX(CASE WHEN t.tek = 'fiber' THEN 1 ELSE 0 END) as har_fiber,
        MAX(CASE WHEN t.tek = 'ftb' THEN 1 ELSE 0 END) as har_ftb,
        MAX(CASE WHEN t.tek = 'kabel' THEN 1 ELSE 0 END) as har_kabel,
        MAX(CASE WHEN t.tek = 'radio' THEN 1 ELSE 0 END) as har_radio,
        MAX(CASE WHEN t.tek = 'satellitt' THEN 1 ELSE 0 END) as har_satellitt,
        MAX(CASE WHEN t.tek = '4g' THEN 1 ELSE 0 END) as har_4g,
        MAX(CASE WHEN t.tek = '5g' THEN 1 ELSE 0 END) as har_5g
    FROM 'lib/adr.parquet' a
    LEFT JOIN tek_per_adresse t ON a.adrid = t.adrid
    GROUP BY a.fylke, a.adrid, a.hus
),
per_fylke AS (
    SELECT
        fylke,
        SUM(har_fiber * hus) as hus_fiber,
        SUM(har_ftb * hus) as hus_ftb,
        SUM(har_kabel * hus) as hus_kabel,
        SUM(har_radio * hus) as hus_radio,
        SUM(har_satellitt * hus) as hus_satellitt,
        SUM(har_4g * hus) as hus_4g,
        SUM(har_5g * hus) as hus_5g,
        SUM(hus) as totalt_hus
    FROM dekning
    GROUP BY fylke
),
resultat AS (
    SELECT
        fylke as Fylke,
        ROUND(hus_fiber * 100.0 / totalt_hus, 1) as Fiber,
        ROUND(hus_ftb * 100.0 / totalt_hus, 1) as FTB,
        ROUND(hus_kabel * 100.0 / totalt_hus, 1) as Kabel,
        ROUND(hus_radio * 100.0 / totalt_hus, 1) as Radio,
        ROUND(hus_satellitt * 100.0 / totalt_hus, 1) as Satellitt,
        ROUND(hus_4g * 100.0 / totalt_hus, 1) as "4G",
        ROUND(hus_5g * 100.0 / totalt_hus, 1) as "5G"
    FROM per_fylke

    UNION ALL

    SELECT
        'NASJONALT',
        ROUND(SUM(hus_fiber) * 100.0 / SUM(totalt_hus), 1),
        ROUND(SUM(hus_ftb) * 100.0 / SUM(totalt_hus), 1),
        ROUND(SUM(hus_kabel) * 100.0 / SUM(totalt_hus), 1),
        ROUND(SUM(hus_radio) * 100.0 / SUM(totalt_hus), 1),
        ROUND(SUM(hus_satellitt) * 100.0 / SUM(totalt_hus), 1),
        ROUND(SUM(hus_4g) * 100.0 / SUM(totalt_hus), 1),
        ROUND(SUM(hus_5g) * 100.0 / SUM(totalt_hus), 1)
    FROM per_fylke
)
SELECT * FROM resultat
ORDER BY CASE WHEN Fylke = 'NASJONALT' THEN 1 ELSE 0 END, Fylke
```

**Resultat:** Nasjonalt: Fiber 91.0%, FTB 96.1%, Kabel 34.1%, Radio 0.0%, Satellitt 55.5%, 4G 100.0%, 5G 99.7%
**Notater:** Kombinerer fbb og mob teknologier. Satellitt-tallene varierer mye mellom fylker (0-100%) pga. rapporteringsforskjeller.

---

<!--
Eksempel på fremtidig loggføring:

## Dekning: Fiberdekning per fylke

**Spørsmål:** "Hvor mange husstander har fiber i hvert fylke?"
**Verifisert:** 2026-01-19
**Promotert:** Ja - finnes i DuckDB Query Patterns

```sql
SELECT
    a.fylke,
    SUM(CASE WHEN har_fiber THEN a.hus ELSE 0 END) as hus_fiber,
    SUM(a.hus) as totalt_hus,
    ROUND(SUM(CASE WHEN har_fiber THEN a.hus ELSE 0 END) * 100.0 / SUM(a.hus), 1) as prosent
FROM (
    SELECT a.adrid, a.fylke, a.hus,
           EXISTS(SELECT 1 FROM 'lib/fbb.parquet' f
                  WHERE f.adrid = a.adrid AND f.tek = 'fiber') as har_fiber
    FROM 'lib/adr.parquet' a
) a
GROUP BY a.fylke
ORDER BY prosent DESC
```

**Resultat:** 15 fylker med fiberdekning fra 87% til 97%
**Notater:** Inkluderer både HC og HP. For kun HC, legg til `AND f.hc = true`
-->
