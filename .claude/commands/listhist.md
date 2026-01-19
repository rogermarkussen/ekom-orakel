# List historiske spørringer

Vis alle verifiserte spørringer fra QUERY_LOG.md, eller kjør en spesifikk spørring.

## Bruk

- `/listhist` - Vis alle spørringer som tabell
- `/listhist 3` - Kjør spørring nummer 3

## Instruksjoner

### Uten argument: Vis indeks

1. Les **kun de første 30 linjene** av QUERY_LOG.md (indeksen ligger øverst)
2. Finn tabellen under "## Indeks"
3. Vis tabellen direkte til brukeren

Indeksen har formatet:
```
| # | Kategori | Beskrivelse | Verifisert |
|---|----------|-------------|------------|
| 1 | Ekom | Kontantkort-utvikling 2018-2024 | 2026-01-19 |
...
```

### Med argument: Kjør spørring

1. Les QUERY_LOG.md og finn spørring nummer N under "## Logg"
2. Spørringene er nummerert i rekkefølge (### er spørring-overskrift)
3. Kjør SQL-spørringen med DuckDB
4. Vis resultatet (husk regel 12: tabell først for fylkesfordeling)

## Ved /loggpush - oppdater indeksen

Når nye spørringer legges til i QUERY_LOG.md, **må indeksen øverst også oppdateres**:

1. Legg til ny rad i indeks-tabellen
2. Bruk neste ledige nummer
3. Hold indeksen synkronisert med logg-seksjonen

## Viktig

- Les kun toppen av filen for `/listhist` uten argument (effektivitet)
- Indeksen er sannhetskilden for oversikten
- Marker `<!-- INDEKS-SLUTT -->` viser hvor indeksen slutter
