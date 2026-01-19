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

Bruk **seaborn** (anbefalt) eller matplotlib med farger fra DESIGNMAL.md.

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd

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

# Seaborn standardoppsett
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 8))

# Fjern unødvendige elementer
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### Eksempel: Horisontalt stolpediagram (fylkesfordeling)

```python
# Sorter: NASJONALT nederst, deretter etter verdi
df = df.copy()
df['_sort'] = df['fylke'].apply(lambda x: 1 if x == 'NASJONALT' else 0)
df = df.sort_values(['_sort', 'prosent'], ascending=[True, True])

# Farger: NASJONALT får egen farge
farger = [NASJONALT_FARGE if f == 'NASJONALT' else PRIMAER for f in df['fylke']]

# Seaborn barplot
sns.barplot(data=df, y='fylke', x='prosent', palette=farger, ax=ax)

# Uthev NASJONALT-label
for label in ax.get_yticklabels():
    if label.get_text() == 'NASJONALT':
        label.set_fontweight('bold')

ax.set_xlabel('Prosent (%)')
ax.set_ylabel('')
ax.set_title('Fiberdekning per fylke (andel husstander)', fontweight='bold', loc='left')
```

### Eksempel: Linjediagram (tidsserie)

```python
# Én linje
sns.lineplot(data=df, x='ar', y='verdi', marker='o', linewidth=2.5, ax=ax)

# Legg til verdier på punktene
for x, y in zip(df['ar'], df['verdi']):
    ax.annotate(f'{y:.0f}', (x, y), textcoords="offset points",
                xytext=(0, 10), ha='center', fontsize=10)

ax.set_xlabel('År')
ax.set_ylabel('Antall (tusen)')
ax.set_title('Utvikling over tid', fontweight='bold', loc='left')
```

### Eksempel: Flere linjer (tilbydere/kategorier)

```python
sns.lineplot(data=df, x='ar', y='verdi', hue='tilbyder',
             marker='o', palette=MOBILFARGER, ax=ax)

ax.legend(title='', frameon=False, loc='upper left')
ax.set_title('Mobilabonnement per tilbyder', fontweight='bold', loc='left')
```

### Eksempel: Heatmap

```python
sns.set_theme(style="white")
pivot_df = df.pivot(index='fylke', columns='kategori', values='prosent')

sns.heatmap(pivot_df, annot=True, fmt='.1f', cmap='viridis',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Prosent'})

ax.set_title('Dekning per fylke og kategori', fontweight='bold', loc='left')
```

### Eksempel: Stablet stolpediagram

```python
# Pandas plotting fungerer godt for stablet
df_plot = df.set_index('fylke')[['1 tilbyder', '2 tilbydere', '3+ tilbydere']]
df_plot.plot(kind='barh', stacked=True, ax=ax,
             color=[NASJONALT_FARGE, PRIMAER, '#2E8B57'])

ax.set_xlabel('Andel (%)')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08),
          ncol=3, frameon=False)
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
