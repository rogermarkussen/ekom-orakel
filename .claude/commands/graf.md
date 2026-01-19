# Lag graf

Analyser forrige datasett og lag en passende graf. **Les alltid DESIGNMAL.md for farger og stil.**

## Instruksjoner

### Steg 1: Les designmalen

Hent fargepaletter og retningslinjer fra `DESIGNMAL.md`:
- Hastighetsfarger
- Teknologifarger
- Mobilfarger
- Segmentfarger
- NASJONALT-markering

### Steg 2: Analyser datasettet

Se på det forrige resultatet og identifiser:
- **Datatype:** Fylkesfordeling, tidsserie, kategorifordeling, sammenligning
- **Kolonner:** Hvilke er kategorier, hvilke er verdier
- **Antall datapunkter:** Få (< 10) eller mange (> 10)
- **Kategorityper:** Hastigheter, teknologier, tilbydere, segmenter?

### Steg 3: Velg graf-type

| Datatype | Anbefalt graf | Unngå |
|----------|---------------|-------|
| Fylkesfordeling (én verdi) | Horisontalt stolpediagram | Kakediagram |
| Fylkesfordeling (flere verdier) | Gruppert stolpediagram | Stablet 100% |
| Tidsserie | Linjediagram | Stolpediagram |
| Andeler (maks 5) | Kakediagram, stablet stolpe | Mer enn 5 stykker |
| Sammenligning få kategorier | Vertikalt stolpediagram | Linjediagram |

### Steg 4: Spør brukeren (bruk AskUserQuestion)

Still spørsmål om:

1. **Graf-type:** Hvilken type graf ønsker du?
   - Alternativer basert på analysen

2. **Hvilke kolonner:** (hvis flere verdier)
   - Hvilke kolonner skal vises?

3. **Sortering:** (for stolpediagram)
   - Etter verdi (synkende), alfabetisk, eller original

4. **Inkluder NASJONALT?**
   - Ja (øverst, uthevet) eller nei

### Steg 5: Generer graf

Bruk matplotlib med farger fra DESIGNMAL.md:

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Fargepaletter fra DESIGNMAL.md
HASTIGHETSFARGER = {
    '30 Mbit': '#1B4F72',
    '100 Mbit': '#4472C4',
    '500 Mbit': '#2E8B57',
    '1000 Mbit': '#E69F00',
}

TEKNOLOGIFARGER = {
    'fiber': '#4472C4',
    'ftb': '#56B4E9',
    'kabel': '#009E73',
    'dsl': '#E69F00',
    'radio': '#CC79A7',
    'satellitt': '#999999',
    'annet': '#999999',
}

MOBILFARGER = {
    'telenor': '#4472C4',
    'telia': '#9B59B6',
    'ice': '#E69F00',
}

SEGMENTFARGER = {
    'Privat': '#4472C4',
    'Bedrift': '#2E8B57',
    'Samlet': '#1B4F72',
}

PRIMAER = '#4472C4'
NASJONALT_FARGE = '#1B4F72'

# Standardoppsett
fig, ax = plt.subplots(figsize=(10, 8))

# Fjern unødvendige elementer
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Subtil grid
ax.xaxis.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

# Hvit bakgrunn
fig.patch.set_facecolor('white')
ax.set_facecolor('white')
```

### Eksempel: Horisontalt stolpediagram (fylkesfordeling)

```python
# Sorter: NASJONALT øverst, deretter etter verdi synkende
df_sortert = df.sort_values('prosent', ascending=True)
nasjonalt = df_sortert[df_sortert['fylke'] == 'NASJONALT']
andre = df_sortert[df_sortert['fylke'] != 'NASJONALT']
df_sortert = pd.concat([andre, nasjonalt])

# Farger: NASJONALT får egen farge
farger = [NASJONALT_FARGE if f == 'NASJONALT' else PRIMAER
          for f in df_sortert['fylke']]

bars = ax.barh(df_sortert['fylke'], df_sortert['prosent'], color=farger)

# Uthev NASJONALT-label
for label in ax.get_yticklabels():
    if label.get_text() == 'NASJONALT':
        label.set_fontweight('bold')

ax.set_xlabel('Prosent (%)')
ax.set_title('Fiberdekning per fylke (andel husstander)', fontweight='bold', loc='left')
```

### Eksempel: Gruppert stolpediagram (flere hastighetsklasser)

```python
import numpy as np

hastigheter = ['30 Mbit', '100 Mbit', '500 Mbit', '1000 Mbit']
x = np.arange(len(fylker))
width = 0.2

for i, hast in enumerate(hastigheter):
    offset = (i - len(hastigheter)/2 + 0.5) * width
    bars = ax.barh(x + offset, df[hast], width,
                   label=hast, color=HASTIGHETSFARGER[hast])

ax.set_yticks(x)
ax.set_yticklabels(fylker)

# Legend utenfor grafen
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
          ncol=4, frameon=False)
```

### Eksempel: Linjediagram (tidsserie)

```python
for tilbyder in tilbydere:
    ax.plot(df['ar'], df[tilbyder],
            marker='o', linewidth=2,
            label=tilbyder, color=MOBILFARGER.get(tilbyder.lower(), PRIMAER))

ax.set_xlabel('År')
ax.set_ylabel('Antall abonnement (mill.)')
ax.set_title('Mobilabonnement per tilbyder', fontweight='bold', loc='left')
ax.legend(loc='upper left', frameon=False)
```

### Steg 6: Lagre

```python
plt.tight_layout()
plt.savefig('uttrekk/YYYY-MM-DD/filnavn.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close()
```

### Steg 7: Vis og iterer

1. Vis bildet til brukeren
2. Spør: "Ser dette bra ut, eller ønsker du justeringer?"
3. Eksempler på justeringer:
   - Annen sortering
   - Fjerne/legge til elementer
   - Justere aksegrenser
   - Endre tittel
4. **Oppdater DESIGNMAL.md** hvis brukeren gir tilbakemelding som bør gjelde fremtidige grafer

---

## Sjekkliste

- [ ] Farger hentet fra DESIGNMAL.md
- [ ] Tittel er deklarativ med metrikk i parentes
- [ ] NASJONALT uthevet (farge + fet label)
- [ ] Legend utenfor grafen (`bbox_to_anchor`)
- [ ] Spines fjernet (top, right)
- [ ] Subtil grid (---, alpha=0.7)
- [ ] Hvit bakgrunn
- [ ] DPI = 150
- [ ] Maks 5-7 kategorier

---

## Oppdater designmalen

Når brukeren gir tilbakemelding som representerer en generell preferanse:
1. Oppdater relevant seksjon i DESIGNMAL.md
2. Legg til i endringsloggen med dato og grunn
