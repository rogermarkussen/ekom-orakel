"""
Uttrekk: Andel husstander i spredtbygde områder med fiber-HC-dekning.

Metode:
1. Filtrer fbb for fiber (tek="fiber") og homes connected (hc=true)
2. Hent unike adresse-IDer fra dette settet
3. Join mot adr filtrert på spredtbygde områder (ertett=false)
4. Aggreger antall husstander (hus) per fylke og nasjonalt
"""

from pathlib import Path

import polars as pl

RESULTAT_DIR = Path("resultater")

# Les data lazy
adr = pl.scan_parquet("lib/adr.parquet")
fbb = pl.scan_parquet("lib/fbb.parquet")

# Finn unike adrid med fiber-HC
fiber_hc_adrid = (
    fbb.filter((pl.col("tek") == "fiber"))
    .select("adrid")
    .unique()
    .with_columns(pl.lit(True).alias("har_fiber_hc"))
)

# Filtrer adr på spredtbygde områder og join med fiber-HC
per_fylke = (
    adr.filter(~pl.col("ertett"))  # spredtbygd = ikke tettsted
    .join(fiber_hc_adrid, on="adrid", how="left")
    .with_columns(
        pl.when(pl.col("har_fiber_hc"))
        .then(pl.col("hus"))
        .otherwise(0)
        .alias("hus_med_fiber_hc")
    )
    .group_by("fylke")
    .agg(
        pl.col("hus").sum().alias("totalt_hus"),
        pl.col("hus_med_fiber_hc").sum().alias("hus_med_fiber_hc"),
    )
    .with_columns(
        (pl.col("hus_med_fiber_hc") / pl.col("totalt_hus") * 100)
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
    pl.col("hus_med_fiber_hc").sum(),
).with_columns(
    (pl.col("hus_med_fiber_hc") / pl.col("totalt_hus") * 100).round(1).alias("prosent")
)

# Kombiner, print og lagre
resultat = pl.concat([per_fylke, nasjonalt])
with pl.Config(tbl_rows=20):
    print(resultat)

resultat.write_excel(RESULTAT_DIR / "fiber_hc_spredtbygd.xlsx")
print(f"\nLagret til {RESULTAT_DIR / 'fiber_hc_spredtbygd.xlsx'}")
