# Lag graf

Analyser forrige datasett og lag en passende graf.

## Instruksjoner

### Steg 1: Analyser datasettet

Se på det forrige resultatet og identifiser:
- **Datatype:** Fylkesfordeling, tidsserie, kategorifordeling, sammenligning
- **Kolonner:** Hvilke er kategorier, hvilke er verdier
- **Antall datapunkter:** Få (< 10) eller mange (> 10)

### Steg 2: Foreslå graf-typer

Basert på datatypen, foreslå passende grafer:

| Datatype | Anbefalte grafer |
|----------|------------------|
| Fylkesfordeling (én verdi) | Horisontalt stolpediagram, kart |
| Fylkesfordeling (flere verdier) | Gruppert stolpediagram, heatmap |
| Tidsserie | Linjediagram, områdediagram |
| Kategorifordeling | Kakediagram, stolpediagram |
| Sammenligning få kategorier | Stolpediagram |

### Steg 3: Spør brukeren (bruk AskUserQuestion)

Still spørsmål om:

1. **Graf-type:** Hvilken type graf ønsker du?
   - Alternativer basert på analysen (f.eks. "Horisontalt stolpediagram", "Linjediagram")

2. **Hvilke kolonner:** (hvis flere verdier)
   - Hvilke kolonner skal vises i grafen?

3. **Sortering:** (for stolpediagram)
   - Alfabetisk, etter verdi (stigende/synkende), eller original rekkefølge?

4. **Inkluder NASJONALT?**
   - Ja (som egen stolpe/linje) eller nei

### Steg 4: Generer graf

Bruk matplotlib til å lage grafen:

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Eksempel: Horisontalt stolpediagram
fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(kategorier, verdier, color='#4472C4')

# Highlight NASJONALT
for i, cat in enumerate(kategorier):
    if cat == 'NASJONALT':
        bars[i].set_color('#2E5090')

ax.set_xlabel('Prosent (%)')
ax.set_title('Tittel basert på data')
ax.invert_yaxis()  # Høyest verdi øverst

# Legg til verdier på stolpene
for i, v in enumerate(verdier):
    ax.text(v + 0.5, i, f'{v}%', va='center')

plt.tight_layout()
plt.savefig('uttrekk/YYYY-MM-DD/filnavn.png', dpi=150, facecolor='white')
```

### Steg 5: Vis og spør om justeringer

1. Vis bildet til brukeren
2. Spør: "Ser dette bra ut, eller ønsker du noen justeringer?"
3. Eksempler på justeringer brukeren kan ønske:
   - Annen sortering
   - Fjerne/legge til elementer
   - Endre farger
   - Justere aksegrenser
   - Endre tittel
4. Hvis justeringer ønskes: Gjør endringene og vis på nytt
5. Gjenta til brukeren er fornøyd

## Graf-stiler

- **Farger:** Bruk Nkom-blå (#4472C4) som hovedfarge
- **NASJONALT:** Alltid mørkere nyanse eller uthevet
- **Font:** Standard matplotlib (sans-serif)
- **Bakgrunn:** Hvit
- **Legend:** ALLTID utenfor grafen (bruk `bbox_to_anchor` under eller til høyre)
- **Tittel:** Inkluder metrikken, f.eks. "(andel husstander)" eller "(antall abonnement)"

## Eksempler på gode grafer

### Fylkesfordeling (én verdi)
→ Horisontalt stolpediagram, sortert etter verdi, NASJONALT nederst

### Fylkesfordeling (flere hastighetsklasser)
→ Gruppert horisontalt stolpediagram eller heatmap

### Utvikling over tid
→ Linjediagram med år på x-aksen

### Markedsandeler
→ Kakediagram eller horisontalt stolpediagram
