# auto-uttrekk

Automatisert dataanalyse av bredbånds- og mobildekning i Norge med Claude Code.

## Hva er dette?

Et AI-assistert analyseverktøy som besvarer spørsmål om norsk telekomdekning. Claude fungerer som en autonom dataanalytiker som skriver og kjører Polars/DuckDB-scripts basert på naturlig språk.

## Datakilder

| Fil | Beskrivelse | Nivå |
|-----|-------------|------|
| `adr.parquet` | Adresseregister med husstander/personer | Adresse |
| `fbb.parquet` | Fastbredbåndsdekning (fiber, FTB, kabel, etc.) | Adresse |
| `mob.parquet` | Mobildekning (4G/5G) | Adresse |
| `ab.parquet` | Bredbåndsabonnementer | Adresse |
| `ekom.parquet` | Ekommarkedsstatistikk (2000-2025) | Nasjonalt |

## Bruk

```bash
# Installer avhengigheter
uv sync

# Start Claude Code
claude

# Eksempler på spørringer:
# "Hvor mange husstander har fiberdekning i Nordland?"
# "Vis 5G-dekning per fylke"
# "Markedsandeler for mobilabonnement"

# For å lage et nytt uttrekk med script og Excel-fil:
/ny
```

## Mappestruktur

```
lib/           # Parquet-datafiler (ikke endre)
library/       # Python-hjelpefunksjoner
uttrekk/       # Genererte scripts og resultater (YYYY-MM-DD/)
examples/      # Eksempel-scripts
```

## Teknologi

- **Claude Code** - AI-assistent for dataanalyse
- **Polars** - Rask databehandling i Python
- **DuckDB** - SQL-spørringer direkte mot Parquet
- **uv** - Python-pakkehåndtering
