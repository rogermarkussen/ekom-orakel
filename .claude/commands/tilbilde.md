# Eksporter til bilde

Eksporter spørringsresultat til en PNG-fil.

## Bruk

- `/tilbilde` - Eksporter forrige spørring fra samtalen
- `/tilbilde <spørring>` - Kjør ny spørring, vis resultat, spør om korrekt, eksporter

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

2. **Lag beskrivende filnavn** - Samme som Excel, men med `.png`

3. **Eksporter til bilde med Python:**
   ```python
   import matplotlib.pyplot as plt
   import matplotlib
   matplotlib.use('Agg')

   # Kjør spørring og hent data
   # data = [...] fra DuckDB
   # columns = [...] kolonnenavn

   fig, ax = plt.subplots(figsize=(10, len(data) * 0.4 + 1))
   ax.axis('tight')
   ax.axis('off')

   table = ax.table(
       cellText=data,
       colLabels=columns,
       loc='center',
       cellLoc='left'
   )
   table.auto_set_font_size(False)
   table.set_fontsize(9)
   table.scale(1.2, 1.5)

   # Style header
   for j, col in enumerate(columns):
       table[(0, j)].set_facecolor('#4472C4')
       table[(0, j)].set_text_props(color='white', weight='bold')

   # Highlight NASJONALT row
   for i, row in enumerate(data):
       if row[0] == 'NASJONALT':
           for j in range(len(columns)):
               table[(i+1, j)].set_facecolor('#D9E2F3')

   plt.savefig('uttrekk/YYYY-MM-DD/filnavn.png', bbox_inches='tight', dpi=150)
   ```

4. **Bekreft** - Vis filstien til brukeren

## Viktig

- Bruk alltid dagens dato for mappen
- Hold filnavnet kort (maks 3-4 ord med understrek)
- Ved ny spørring: ALLTID vis resultatet og spør om det er korrekt før eksport
