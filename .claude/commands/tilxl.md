# Eksporter til Excel

Eksporter spørringsresultat til en Excel-fil.

## Bruk

- `/tilxl` - Eksporter forrige spørring fra samtalen
- `/tilxl <spørring>` - Kjør ny spørring, vis resultat, spør om korrekt, eksporter

## Instruksjoner

### Uten argument: Eksporter forrige spørring

1. Finn forrige DuckDB-spørring fra samtalen
2. Opprett mappe og eksporter (se steg under)

### Med argument: Ny spørring

1. **Kjør spørringen** med DuckDB og vis resultatet
2. **Spør brukeren:** "Er dette resultatet korrekt?"
3. **Hvis ja:** Fortsett til eksport
4. **Hvis nei:** La brukeren korrigere

### Eksport-steg

1. **Opprett mappe hvis nødvendig:**
   ```bash
   mkdir -p uttrekk/YYYY-MM-DD
   ```

2. **Lag beskrivende filnavn** - Kort og beskrivende, f.eks:
   - `fbb_hastighet_fylke.xlsx`
   - `fiber_konkurranse.xlsx`
   - `teknologi_dekning.xlsx`

3. **Eksporter til Excel:**
   ```bash
   duckdb -c "
   LOAD spatial;
   COPY (
       <spørringen her>
   ) TO 'uttrekk/YYYY-MM-DD/filnavn.xlsx' WITH (FORMAT GDAL, DRIVER 'xlsx');
   "
   ```

4. **Bekreft** - Vis filstien til brukeren

## Eksempel

```bash
# Med argument:
/tilxl fiberdekning per fylke

# Uten argument (etter en spørring):
/tilxl
```

## Viktig

- Bruk alltid dagens dato for mappen
- Hold filnavnet kort (maks 3-4 ord med understrek)
- Ikke inkluder dato i filnavnet (det ligger i mappestien)
- Ved ny spørring: ALLTID vis resultatet og spør om det er korrekt før eksport
