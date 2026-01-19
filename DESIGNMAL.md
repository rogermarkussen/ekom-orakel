# DESIGNMAL.md

Retningslinjer for datavisualisering i ekom-orakel.

---

## Grunnprinsipper

1. **Klarhet over estetikk.** Grafen skal formidle data, ikke imponere.
2. **Minimer "chart junk".** Fjern alt som ikke representerer data.
3. **Konsistente farger.** Samme kategori = samme farge, alltid.
4. **Tilgjengelighet.** Unngå rød/grønn-kombinasjoner. Bruk mønstre som backup.
5. **Maks 5-7 kategorier.** Flere enn dette krever splitting eller annen tilnærming.

---

## Fargepaletter

### Hovedpalett (kategorisk)

Fargeblind-sikker palett basert på ColorBrewer "Set2" og "Dark2":

| Kategori | Hex | Bruk |
|----------|-----|------|
| Primær | `#4472C4` | Hovedfarge, enkle stolpediagram |
| Sekundær | `#56B4E9` | Lyseblå, sekundære verdier |
| Suksess | `#009E73` | Grønn, positive verdier |
| Advarsel | `#E69F00` | Oransje, mellomverdier |
| Fremhevet | `#D55E00` | Rødoransje, viktige verdier |
| Nøytral | `#999999` | Grå, referanselinjer |
| NASJONALT | `#1B4F72` | Mørkeblå, alltid for nasjonale tall |

### Hastighetsklasser (fast bredbånd)

Konsistent fargekoding for hastighetsklasser:

| Hastighet | Hex | Navn |
|-----------|-----|------|
| 30 Mbit | `#1B4F72` | Mørkeblå |
| 100 Mbit | `#4472C4` | Blå |
| 500 Mbit | `#2E8B57` | Grønn |
| 1000 Mbit | `#E69F00` | Gul/oransje |

```python
HASTIGHETSFARGER = {
    '30 Mbit': '#1B4F72',
    '100 Mbit': '#4472C4',
    '500 Mbit': '#2E8B57',
    '1000 Mbit': '#E69F00',
}
```

### Teknologier (bredbånd)

| Teknologi | Hex | Beskrivelse |
|-----------|-----|-------------|
| Fiber | `#4472C4` | Blå (hovedteknologi) |
| FTB | `#56B4E9` | Lyseblå (trådløs) |
| Kabel | `#009E73` | Grønn |
| DSL | `#E69F00` | Oransje |
| Annet | `#999999` | Grå |

```python
TEKNOLOGIFARGER = {
    'fiber': '#4472C4',
    'ftb': '#56B4E9',
    'kabel': '#009E73',
    'dsl': '#E69F00',
    'radio': '#CC79A7',
    'satellitt': '#999999',
    'annet': '#999999',
}
```

### Mobiloperatører

| Tilbyder | Hex | Merknad |
|----------|-----|---------|
| Telenor | `#4472C4` | Blå |
| Telia | `#9B59B6` | Lilla |
| Ice | `#E69F00` | Oransje |

```python
MOBILFARGER = {
    'telenor': '#4472C4',
    'telia': '#9B59B6',
    'ice': '#E69F00',
}
```

### Markedssegment

| Segment | Hex |
|---------|-----|
| Privat | `#4472C4` |
| Bedrift | `#2E8B57` |
| Samlet | `#1B4F72` |

```python
SEGMENTFARGER = {
    'Privat': '#4472C4',
    'Bedrift': '#2E8B57',
    'Samlet': '#1B4F72',
}
```

### Sekvensielle paletter (for heatmaps etc.)

For verdier fra lav til høy, bruk `viridis` eller `cividis` (fargeblind-sikre):

```python
import matplotlib.pyplot as plt
plt.cm.viridis  # Lav → høy
plt.cm.cividis  # Alternativ, også fargeblind-sikker
```

---

## Typografi

| Element | Størrelse | Vekt |
|---------|-----------|------|
| Tittel | 14pt | Bold |
| Undertittel | 11pt | Normal |
| Aksetitler | 11pt | Normal |
| Akselabels | 10pt | Normal |
| Legend | 10pt | Normal |
| Dataetiketter | 9pt | Normal |

### Tittelformat

- **Deklarativ:** Beskriv hovedfunnet, ikke bare datatypen
- **Metrikk i parentes:** "(andel husstander)", "(antall abonnement)", "(mill. NOK)"

Eksempler:
- "Fiberdekning per fylke (andel husstander)"
- "5G-dekning øker mest i Nordland (endring 2024-2025)"

---

## Graftyper og bruksområder

| Datatype | Anbefalt graf | Unngå |
|----------|---------------|-------|
| Fylkesfordeling (én verdi) | Horisontalt stolpediagram | Kakediagram |
| Fylkesfordeling (flere verdier) | Gruppert stolpediagram | Stablet 100% |
| Tidsserie | Linjediagram | Stolpediagram |
| Andeler av helhet | Stablet stolpediagram, kakediagram (maks 5) | Mer enn 5 kakestykker |
| Sammenligning få kategorier | Vertikalt stolpediagram | Linjediagram |
| Korrelasjon | Spredningsdiagram | Stolpediagram |

---

## Layout og elementer

### Påkrevde elementer

1. **Tittel** - Deklarativ, venstrejustert
2. **Aksetitler** - Med enheter (%, antall, mill. NOK)
3. **Datakilde** - Nederst til venstre eller i undertittel

### Legend

- **Plassering:** Utenfor grafen (under eller til høyre)
- **Bruk `bbox_to_anchor`** for konsistent plassering
- **Direkte labeling** foretrukket over legend når mulig

```python
ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.15),
    ncol=4,
    frameon=False
)
```

### NASJONALT-markering

NASJONALT skal alltid skille seg ut:
- Egen farge (`#1B4F72` mørkeblå)
- Fet skrift på label
- Plasseres øverst eller nederst (ikke midt i)

```python
for i, label in enumerate(labels):
    if label == 'NASJONALT':
        bars[i].set_color('#1B4F72')
        ax.get_yticklabels()[i].set_fontweight('bold')
```

---

## Tilgjengelighet

### Fargeblindhet

- Unngå rød + grønn sammen
- Test med simuleringsverktøy
- Bruk mønstre/skraveringer som backup

```python
# Legg til skravering for fargeblind-sikkerhet
hatches = ['', '///', '...', 'xxx', '\\\\\\']
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)
```

### Kontrast

- Tekst: minimum 4.5:1 kontrast mot bakgrunn
- Grafiske elementer: minimum 3:1

### Alt-tekst

Beskriv alltid grafen i tre deler:
1. Graftype og hva den viser
2. Hoveddataene/trenden
3. Hovedfunnet

Eksempel: "Horisontalt stolpediagram som viser fiberdekning per fylke. Oslo har høyest dekning med 98%, mens Nordland har lavest med 78%. Nasjonalt snitt er 89%."

---

## Matplotlib-innstillinger

### Standardoppsett

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Figur
fig, ax = plt.subplots(figsize=(10, 8))

# Fjern unødvendige elementer
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Grid (kun horisontalt for stolpediagram)
ax.xaxis.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

# Bakgrunn
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Tight layout
plt.tight_layout()

# Lagre med god oppløsning
plt.savefig('filnavn.png', dpi=150, facecolor='white', bbox_inches='tight')
```

### Horisontalt stolpediagram (fylkesfordeling)

```python
def lag_fylkesdiagram(df, verdikolonne, tittel, enhet='%'):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Sorter: NASJONALT øverst, deretter etter verdi
    df_sortert = df.sort_values(verdikolonne, ascending=True)
    nasjonalt = df_sortert[df_sortert['fylke'] == 'NASJONALT']
    andre = df_sortert[df_sortert['fylke'] != 'NASJONALT']
    df_sortert = pd.concat([andre, nasjonalt])

    # Farger
    farger = ['#1B4F72' if f == 'NASJONALT' else '#4472C4'
              for f in df_sortert['fylke']]

    # Plot
    bars = ax.barh(df_sortert['fylke'], df_sortert[verdikolonne], color=farger)

    # Styling
    ax.set_xlabel(f'{enhet}')
    ax.set_title(tittel, fontweight='bold', loc='left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)

    # Uthev NASJONALT
    for label in ax.get_yticklabels():
        if label.get_text() == 'NASJONALT':
            label.set_fontweight('bold')

    plt.tight_layout()
    return fig, ax
```

---

## Sjekkliste før levering

- [ ] Tittel er deklarativ og inkluderer metrikk
- [ ] Akser har titler med enheter
- [ ] NASJONALT er uthevet og plassert konsistent
- [ ] Farger følger designmalen
- [ ] Legend er utenfor grafen
- [ ] Ingen rød/grønn-kombinasjon
- [ ] Maks 5-7 kategorier
- [ ] Grid er subtilt (---, alpha=0.7)
- [ ] Bakgrunn er hvit
- [ ] DPI er minst 150

---

## Endringslogg

| Dato | Endring | Grunn |
|------|---------|-------|
| 2026-01-19 | Opprettet | Etablere konsistente retningslinjer |

---

## Kilder

- [ColorBrewer](https://colorbrewer2.org/) - Fargepaletter
- [CFPB Design System](https://cfpb.github.io/design-system/guidelines/data-visualization-guidelines) - Retningslinjer
- [Urban Institute Style Guide](http://urbaninstitute.github.io/graphics-styleguide/) - Typografi og layout
- [Seaborn Color Palettes](https://seaborn.pydata.org/tutorial/color_palettes.html) - Matplotlib-integrasjon
