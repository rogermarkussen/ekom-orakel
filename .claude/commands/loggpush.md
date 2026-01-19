# Logg, commit og push

Logg alle verifiserte spørringer og korreksjoner fra sesjonen, deretter commit og push.

## Steg 1: Logg sesjonen

Gå gjennom samtalen og identifiser:

1. **Verifiserte spørringer** - DuckDB-spørringer der brukeren bekreftet at resultatet var korrekt
   - Legg disse til i QUERY_LOG.md

2. **Korreksjoner** - Feil som ble gjort og rettet (f.eks. exit code 1, feil resultat)
   - Legg disse til i CORRECTIONS.md

Ikke logg noe som allerede er logget tidligere i sesjonen.

## Steg 2: Analyser endringene

```bash
git status
git diff --staged
git diff
```

## Steg 3: Stage endringer

```bash
git add -A
```

## Steg 4: Lag commit-melding

Basert på endringene, lag en kort og forklarende commit-melding på norsk:

- Første linje: Kort oppsummering (maks 50 tegn)
- Bruk imperativ form ("Legg til", "Fiks", "Oppdater", "Fjern")
- Hvis nødvendig, legg til en blank linje og mer kontekst

Eksempler:
- "Legg til spørringslogging for konsistens"
- "Fiks feil i hastighetsfilter"
- "Oppdater CLAUDE.md med nye regler"

## Steg 5: Commit og push

```bash
git commit -m "Din melding"
git push
```

## Viktig

- Ikke inkluder filer som inneholder sensitiv informasjon
- Sjekk at alle tester/validering passerer før push
- Hvis push feiler pga. remote-endringer, kjør `git pull --rebase` først
