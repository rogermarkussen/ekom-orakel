# List historiske spørringer

Vis alle verifiserte spørringer fra QUERY_LOG.md, eller kjør en spesifikk spørring.

## Bruk

- `/listhist` - Vis alle spørringer som tabell
- `/listhist 3` - Kjør spørring nummer 3

## Instruksjoner

### Uten argument: Vis tabell

1. Les QUERY_LOG.md
2. Parse alle spørringer under "## Logg"-seksjonen
3. Presenter som tabell:

| # | Kategori | Beskrivelse | Verifisert |
|---|----------|-------------|------------|

Hvor:
- **#** = Radnummer (1, 2, 3...)
- **Kategori** = Teksten etter "###" (f.eks. "Ekom", "Dekning", "Konkurranse")
- **Beskrivelse** = Kort oppsummering av hva spørringen finner (maks 50 tegn)
- **Verifisert** = Datoen spørringen ble verifisert

### Med argument: Kjør spørring

1. Les QUERY_LOG.md og finn spørring nummer N
2. Kjør SQL-spørringen med DuckDB
3. Vis resultatet (husk regel 12: tabell først for fylkesfordeling)

## Eksempel output (uten argument)

```
| # | Kategori    | Beskrivelse                              | Verifisert |
|---|-------------|------------------------------------------|------------|
| 1 | Ekom        | Kontantkort-utvikling 2018-2024          | 2026-01-19 |
| 2 | Abonnement  | Fordeling etter adressetype              | 2026-01-19 |
| 3 | Dekning     | Fastbredbånd per hastighetsklasse        | 2026-01-19 |
```

## Viktig

- Ikke inkluder kommenterte seksjoner (inne i `<!-- -->`)
- Vis kun faktisk loggede spørringer
- Hold beskrivelsen kort og informativ
