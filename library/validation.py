"""
Validering og aggregering for uttrekk.

Eksempel:
    from library.validation import add_national_aggregate, validate_and_save

    # Legg til nasjonal rad
    resultat = add_national_aggregate(per_fylke, "hus_dekning", "totalt_hus")

    # Valider og lagre
    validate_and_save(resultat, excel_path, "hus_dekning", "totalt_hus")
"""

from pathlib import Path

import polars as pl

# Norges 15 fylker
FYLKER = [
    "AGDER",
    "AKERSHUS",
    "BUSKERUD",
    "FINNMARK",
    "INNLANDET",
    "MØRE OG ROMSDAL",
    "NORDLAND",
    "OSLO",
    "ROGALAND",
    "TELEMARK",
    "TROMS",
    "TRØNDELAG",
    "VESTFOLD",
    "VESTLAND",
    "ØSTFOLD",
]


def add_national_aggregate(
    df: pl.DataFrame,
    metric_col: str,
    total_col: str,
    group_col: str = "fylke",
) -> pl.DataFrame:
    """
    Legg til nasjonal aggregatrad.

    Args:
        df: DataFrame med fylkesdata
        metric_col: Kolonne med metrikken (f.eks. "hus_dekning")
        total_col: Kolonne med total (f.eks. "totalt_hus")
        group_col: Grupperingskolonne (default "fylke")

    Returns:
        DataFrame med nasjonal rad lagt til
    """
    numeric_cols = [c for c in df.columns if c != group_col and df[c].dtype.is_numeric()]

    nasjonalt = df.select(
        pl.lit("NASJONALT").alias(group_col),
        *[pl.col(c).sum() for c in numeric_cols],
    )

    # Regn ut prosent på nytt for nasjonalt
    if "prosent" in df.columns:
        nasjonalt = nasjonalt.with_columns(
            (pl.col(metric_col) / pl.col(total_col) * 100).round(1).alias("prosent")
        )

    return pl.concat([df, nasjonalt])


def validate_extraction(
    df: pl.DataFrame,
    metric_col: str,
    total_col: str,
    group_col: str = "fylke",
) -> list[str]:
    """
    Valider uttrekksresultater.

    Returnerer liste med feil (tom liste = OK).
    """
    errors = []

    # 1. Prosenter mellom 0-100
    if "prosent" in df.columns:
        invalid = df.filter((pl.col("prosent") < 0) | (pl.col("prosent") > 100))
        if invalid.height > 0:
            errors.append(f"Ugyldige prosenter:\n{invalid}")

    # 2. Metrikk <= total
    invalid = df.filter(pl.col(metric_col) > pl.col(total_col))
    if invalid.height > 0:
        errors.append(f"Metrikk overstiger total:\n{invalid}")

    # 3. Sum av regioner = nasjonalt
    non_national = df.filter(pl.col(group_col) != "NASJONALT")
    national = df.filter(pl.col(group_col) == "NASJONALT")

    if national.height > 0:
        for col in [metric_col, total_col]:
            region_sum = non_national.select(pl.col(col).sum()).item()
            national_val = national.select(col).item()
            if region_sum != national_val:
                errors.append(
                    f"{col}: sum regioner ({region_sum:,}) != nasjonalt ({national_val:,})"
                )

    # 4. Alle fylker til stede
    if group_col == "fylke":
        fylker_i_data = set(non_national.select(group_col).to_series().to_list())
        manglende = set(FYLKER) - fylker_i_data
        ekstra = fylker_i_data - set(FYLKER)

        if manglende:
            errors.append(f"Manglende fylker: {manglende}")
        if ekstra:
            errors.append(f"Ukjente fylker: {ekstra}")

    return errors


def validate_and_save(
    df: pl.DataFrame,
    excel_path: Path | str,
    metric_col: str,
    total_col: str,
) -> None:
    """
    Print, valider og lagre resultat.

    Kaster ValueError hvis validering feiler.
    """
    excel_path = Path(excel_path)

    # Print resultat
    with pl.Config(tbl_rows=20):
        print(df)

    # Valider
    errors = validate_extraction(df, metric_col, total_col)

    if errors:
        print("\nVALIDERING FEILET:")
        for e in errors:
            print(f"  - {e}")
        raise ValueError("Validering feilet")

    print("\n Validering OK")

    # Lagre
    excel_path.parent.mkdir(parents=True, exist_ok=True)
    df.write_excel(excel_path)
    print(f"Lagret til {excel_path}")
