"""
Datalasting og filstier for uttrekk.

Eksempel:
    from library.loader import load_data, get_script_paths

    # Last alle data som LazyFrames
    adr, fbb, mob, ab = load_data()

    # Hent stier for script og resultat
    script_path, excel_path = get_script_paths("fiber_dekning")
"""

from datetime import date
from pathlib import Path

import polars as pl

# Stier
DATA_DIR = Path("lib")
UTTREKK_DIR = Path("uttrekk")


def load_dataset(name: str) -> pl.LazyFrame:
    """
    Last ett datasett som LazyFrame.

    Args:
        name: Navn på datasett (adr, fbb, mob, ab)

    Returns:
        LazyFrame for lazy evaluation
    """
    path = DATA_DIR / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Datasett ikke funnet: {path}")
    return pl.scan_parquet(path)


def load_data() -> tuple[pl.LazyFrame, pl.LazyFrame, pl.LazyFrame, pl.LazyFrame]:
    """
    Last alle datakilder som LazyFrames.

    Returns:
        Tuple med (adr, fbb, mob, ab)
    """
    return (
        load_dataset("adr"),
        load_dataset("fbb"),
        load_dataset("mob"),
        load_dataset("ab"),
    )


def get_today_dir() -> Path:
    """Hent eller opprett dagens uttrekksmappe."""
    today = date.today().isoformat()
    today_dir = UTTREKK_DIR / today
    today_dir.mkdir(parents=True, exist_ok=True)
    return today_dir


def get_next_number() -> int:
    """Finn neste ledige uttrekksnummer for dagens dato."""
    today_dir = get_today_dir()
    existing = list(today_dir.glob("*.py"))
    if not existing:
        return 1
    numbers = []
    for f in existing:
        try:
            num = int(f.stem.split("_")[0])
            numbers.append(num)
        except (ValueError, IndexError):
            continue
    return max(numbers, default=0) + 1


def get_script_paths(name: str) -> tuple[Path, Path]:
    """
    Generer stier for script og resultat.

    Args:
        name: Beskrivende navn (f.eks. "fiber_dekning")

    Returns:
        (script_path, excel_path) - f.eks. uttrekk/2026-01-10/01_fiber_dekning.py
    """
    today_dir = get_today_dir()
    num = get_next_number()
    prefix = f"{num:02d}_{name}"
    return today_dir / f"{prefix}.py", today_dir / f"{prefix}.xlsx"


def check_values(lf: pl.LazyFrame, column: str) -> list:
    """
    Vis unike verdier i en kolonne.

    Nyttig for å verifisere filterverdier før uttrekk.
    """
    values = lf.select(column).unique().sort(column).collect().to_series().to_list()
    print(f"Verdier i {column}: {values}")
    return values
