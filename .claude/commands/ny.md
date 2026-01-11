# Opprett nytt uttrekk

Du skal hjelpe brukeren med å lage et nytt uttrekk-script. Bruk AskUserQuestion-verktøyet for å samle inn nødvendig informasjon.

## Steg 1: Samle informasjon

Still følgende spørsmål til brukeren (bruk AskUserQuestion):

### Spørsmål 1: Hva ønsker du å finne ut?
Be brukeren beskrive uttrekket med egne ord. F.eks:
- "Fiberdekning i spredtbygde områder"
- "5G-dekning per fylke"
- "Antall fiber-abonnementer"

### Spørsmål 2: Hvilken datakilde?
Alternativer:
- **fbb** (fastbredbånd dekning) - for dekningsdata
- **mob** (mobildekning) - for 4G/5G dekning
- **ab** (abonnementer) - for abonnementsdata

### Spørsmål 3: Hvilke filtre trengs?
Still oppfølgingsspørsmål basert på datakilde:

For **fbb**:
- Teknologi? (fiber, ftb, kabel, radio, alle)
- Hastighet? (ingen, 100 Mbit, 1 Gbit)
- Homes Connected (HC) eller Homes Passed (HP)?
- Egen infrastruktur?

For **mob**:
- Teknologi? (4g, 5g, begge)
- Tilbyder? (telenor, telia, ice, alle)

For **ab**:
- Teknologi? (fiber, kabel, etc.)
- Privat eller bedrift?
- MDU eller SDU?

### Spørsmål 4: Populasjon
- Tettsted
- Spredtbygd
- Alle

### Spørsmål 5: Aggregeringsnivå
- Per fylke
- Per kommune
- Kun nasjonalt

## Steg 2: Lag scriptet

Når du har all informasjon:

1. Bruk `get_script_paths()` fra library for å finne riktig filnavn
2. Skriv scriptet til `uttrekk/YYYY-MM-DD/XX_navn.py`
3. Følg mønsteret fra CLAUDE.md og examples/
4. Bruk library-funksjonene (filter_teknologi, filter_hastighet, etc.)
5. Inkluder alltid:
   - Docstring med beskrivelse og kriterier
   - Nasjonal aggregering
   - validate_and_save() for lagring

## Steg 3: Kjør og valider

1. Kjør scriptet med `uv run python uttrekk/YYYY-MM-DD/XX_navn.py`
2. Sjekk at resultatene gir mening (se sanity checks i CLAUDE.md)
3. Vis resultatene til brukeren

## Viktig

- ALDRI gjett på definisjoner - spør brukeren
- Bruk ALLTID library-funksjonene
- Valider at tallene gir mening før du presenterer dem
