"""
Library-pakke for bredbåndsuttrekk.

Bruk:
    from library import load_data, get_script_paths, filter_hastighet, validate_and_save
"""

from library.loader import (
    DATA_DIR,
    UTTREKK_DIR,
    get_script_paths,
    get_today_dir,
    load_data,
    load_dataset,
)
from library.filters import (
    filter_egen,
    filter_hastighet,
    filter_hc,
    filter_populasjon,
    filter_teknologi,
    filter_tilbyder,
)
from library.validation import (
    FYLKER,
    add_national_aggregate,
    validate_and_save,
    validate_extraction,
)

__all__ = [
    # Loader
    "DATA_DIR",
    "UTTREKK_DIR",
    "load_data",
    "load_dataset",
    "get_script_paths",
    "get_today_dir",
    # Filters
    "filter_hastighet",
    "filter_teknologi",
    "filter_tilbyder",
    "filter_populasjon",
    "filter_hc",
    "filter_egen",
    # Validation
    "FYLKER",
    "add_national_aggregate",
    "validate_extraction",
    "validate_and_save",
]
