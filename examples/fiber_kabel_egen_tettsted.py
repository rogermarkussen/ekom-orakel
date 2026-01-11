"""
Uttrekk: Andel husstander i tettsted med fiber- eller kabeldekning (egen infrastruktur).

Kriterier:
- tek = "fiber" ELLER tek = "kabel"
- egen = true
- Populasjon: ertett = true (tettsted)

Metode:
1. Filtrer fbb for fiber/kabel med egen infrastruktur
2. Hent unike adresse-IDer
3. Join mot adr filtrert på tettsted
4. Aggreger husstander per fylke
"""

import polars as pl

from utils import add_national_aggregate, load_data, print_and_save

adr, fbb, _mob, _ab = load_data()

# Finn unike adrid med fiber eller kabel, kun egen infrastruktur
kvalifisert = (
    fbb.filter(pl.col("egen") & pl.col("tek").is_in(["fiber", "kabel"]))
    .select("adrid")
    .unique()
    .with_columns(pl.lit(True).alias("har_dekning"))
)

# Join mot adr (kun tettsted) og aggreger per fylke
per_fylke = (
    adr.filter(pl.col("ertett"))  # kun tettsted
    .join(kvalifisert, on="adrid", how="left")
    .with_columns(
        pl.when(pl.col("har_dekning"))
        .then(pl.col("hus"))
        .otherwise(0)
        .alias("hus_med_dekning")
    )
    .group_by("fylke")
    .agg(
        pl.col("hus").sum().alias("totalt_hus"),
        pl.col("hus_med_dekning").sum().alias("hus_med_dekning"),
    )
    .with_columns(
        (pl.col("hus_med_dekning") / pl.col("totalt_hus") * 100)
        .round(1)
        .alias("prosent")
    )
    .sort("fylke")
    .collect()
)

# Legg til nasjonalt og lagre
resultat = add_national_aggregate(per_fylke)
print_and_save(
    resultat,
    "fiber_kabel_egen_tettsted.xlsx",
    metric_col="hus_med_dekning",
    total_col="totalt_hus",
)
