# Korreksjoner

Denne filen dokumenterer feil som er gjort og hva som er riktig. Les denne før du starter nye uttrekk.

Når et mønster gjentar seg eller er spesielt viktig, bør det promoteres til en permanent regel i CLAUDE.md.

---

## Format

Hver korreksjon følger dette formatet:

```
## YYYY-MM-DD: Kort beskrivelse av feilen

**Kontekst:** Hva prøvde agenten å gjøre?
**Hva ble gjort:** Den faktiske feilen
**Hva er riktig:** Korrekt fremgangsmåte
**Hvorfor:** Forklaring på hvorfor dette er riktig
**Promotert:** Ja/Nei (om regelen er lagt til i CLAUDE.md)
```

---

## Korreksjoner

*(Ingen korreksjoner ennå - denne filen oppdateres når feil oppdages)*

<!--
Eksempel på fremtidig korreksjon:

## 2026-01-18: Feil hastighetsfilter

**Kontekst:** Lage uttrekk for dekning over 100 Mbit
**Hva ble gjort:** Brukte `> 100_000` (streng større enn)
**Hva er riktig:** `>= 100_000` (større enn eller lik)
**Hvorfor:** "Over 100 Mbit" tolkes som "100 Mbit eller mer" i dekningssammenheng
**Promotert:** Ja - lagt til i "Vanlige Feil å Unngå"
-->
