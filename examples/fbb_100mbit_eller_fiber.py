"""
Uttrekk: Andel husstander med tilgang til ftb over 100 Mbit eller fiber (egen infrastruktur).

Kriterier:
- egen = true (tilbyder eier infrastrukturen)
- OG enten:
  - tek = "ftb" (fast trådløst bredbånd) OG ned >= 100000, ELLER
  - tek = "fiber"

Metode:
1. Filtrer fbb for egen infrastruktur OG (ftb med >=100 Mbit ELLER fiber)
2. Hent unike adresse-IDer
3. Join mot adr og aggreger husstander per fylke
"""

from pathlib import Path

import polars as pl

RESULTAT_DIR = Path("resultater")

# Les data lazy
adr = pl.scan_parquet("lib/adr.parquet")
fbb = pl.scan_parquet("lib/fbb.parquet")

# Finn unike adrid med ftb >100 Mbit eller fiber, kun egen infrastruktur
kvalifisert_adrid = (
    fbb.filter(
        pl.col("egen")
        & (
            ((pl.col("tek") == "ftb") & (pl.col("ned") >= 100_000))
            | (pl.col("tek") == "fiber")
        )
    )
    .select("adrid")
    .unique()
    .with_columns(pl.lit(True).alias("har_dekning"))
)

# Join mot adr og aggreger per fylke
per_fylke = (
    adr.join(kvalifisert_adrid, on="adrid", how="left")
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

# Nasjonalt aggregat
nasjonalt = per_fylke.select(
    pl.lit("NASJONALT").alias("fylke"),
    pl.col("totalt_hus").sum(),
    pl.col("hus_med_dekning").sum(),
).with_columns(
    (pl.col("hus_med_dekning") / pl.col("totalt_hus") * 100).round(1).alias("prosent")
)

# Kombiner, print og lagre
resultat = pl.concat([per_fylke, nasjonalt])
with pl.Config(tbl_rows=20):
    print(resultat)

resultat.write_excel(RESULTAT_DIR / "fbb_100mbit_eller_fiber.xlsx")
print(f"\nLagret til {RESULTAT_DIR / 'fbb_100mbit_eller_fiber.xlsx'}")
