# Commit og push

Lag en forklarende commit-melding, commit endringene og push til remote.

## Steg 1: Analyser endringene

Kjør følgende kommandoer for å forstå hva som er endret:

```bash
git status
git diff --staged
git diff
```

## Steg 2: Stage endringer

Hvis det er ustaged endringer som bør inkluderes:

```bash
git add -A
```

## Steg 3: Lag commit-melding

Basert på endringene, lag en kort og forklarende commit-melding på norsk:

- Første linje: Kort oppsummering (maks 50 tegn)
- Bruk imperativ form ("Legg til", "Fiks", "Oppdater", "Fjern")
- Hvis nødvendig, legg til en blank linje og mer kontekst

Eksempler:
- "Legg til spørringslogging for konsistens"
- "Fiks feil i hastighetsfilter"
- "Oppdater CLAUDE.md med nye regler"

## Steg 4: Commit og push

```bash
git commit -m "Din melding"
git push
```

## Viktig

- Ikke inkluder filer som inneholder sensitiv informasjon
- Sjekk at alle tester/validering passerer før push
- Hvis push feiler pga. remote-endringer, kjør `git pull --rebase` først
