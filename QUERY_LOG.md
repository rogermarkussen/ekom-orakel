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
