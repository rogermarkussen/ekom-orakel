"""
Uttrekk: Andel husstander med fiberdekning per fylke.

Kriterier:
- tek = "fiber" (alle fibertyper)

Metode:
1. Filtrer fbb for fiber
2. Hent unike adresse-IDer
3. Join mot adr og summer husstander per fylke
"""

import polars as pl

from utils import add_national_aggregate, load_data, print_and_save

adr, fbb, _mob, _ab = load_data()

# Finn unike adrid med fiber
fiber_adrid = (
    fbb.filter(pl.col("tek") == "fiber")
    .select("adrid")
    .unique()
    .with_columns(pl.lit(True).alias("har_fiber"))
)

# Join med adresser og aggreger per fylke
per_fylke = (
    adr.join(fiber_adrid, on="adrid", how="left")
    .with_columns(
        pl.when(pl.col("har_fiber"))
        .then(pl.col("hus"))
        .otherwise(0)
        .alias("hus_med_fiber")
    )
    .group_by("fylke")
    .agg(
        pl.col("hus").sum().alias("totalt_hus"),
        pl.col("hus_med_fiber").sum().alias("hus_med_fiber"),
    )
    .with_columns(
        (pl.col("hus_med_fiber") / pl.col("totalt_hus") * 100).round(1).alias("prosent")
    )
    .sort("fylke")
    .collect()
)

# Legg til nasjonalt og lagre
resultat = add_national_aggregate(per_fylke)
print_and_save(
    resultat,
    "fiberdekning_per_fylke.xlsx",
    metric_col="hus_med_fiber",
    total_col="totalt_hus",
)
