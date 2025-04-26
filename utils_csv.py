# utils_csv.py
from pathlib import Path
from typing import Iterable, List

import pandas as pd
from utils_file import move_file  # generic helper you created earlier


_HEBREW_COLUMNS_TO_DROP: set[str] = {
    "סוג עסקה",
    "מטבע חיוב",
    "סכום עסקה מקורי",
    "מטבע עסקה מקורי",
    "תאריך חיוב",
    "הערות",
    "מועדון הנחות",
    "מפתח דיסקונט",
    "אופן ביצוע ההעסקה",
    "תיוגים",
    'שער המרה ממטבע מקור/התחשבנות לש"ח',
}


def drop_unwanted_columns(df: pd.DataFrame, columns_to_drop: Iterable[str] = _HEBREW_COLUMNS_TO_DROP) -> pd.DataFrame:
    """Remove any columns whose name is in *columns_to_drop* (case-sensitive)."""
    return df.drop(columns=[c for c in columns_to_drop if c in df.columns], errors="ignore")


# ──────────────────────────────────────────────────────────────
# 1.  tiny file-system helpers (internal use)
# ──────────────────────────────────────────────────────────────
def _ensure_dirs(*dirs: Path) -> None:
    """`mkdir -p` for every Path in *dirs* (idempotent)."""
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def _process_one_csv(
    csv_path: Path, cleaned_dir: Path, archive_dir: Path, *, header_rows: int, footer_rows: int, overwrite: bool
) -> Path | None:
    """
    Clean *csv_path*, write to *cleaned_dir*, move original to *archive_dir*.
    Returns the cleaned file’s Path (or `None` if skipped/error).
    """
    out_path = cleaned_dir / csv_path.name
    if out_path.exists() and not overwrite:
        print(f"Skipping existing file: {out_path.name}")
        return None

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig", skiprows=header_rows, skipfooter=footer_rows, engine="python")
        df = drop_unwanted_columns(df)
        df.to_csv(out_path, index=False, encoding="utf-8-sig")

        move_file(csv_path, archive_dir, overwrite=overwrite)
        return out_path

    except Exception as exc:
        print(f"⚠️  Error processing {csv_path.name}: {exc}")
        return None


# ──────────────────────────────────────────────────────────────
# 2.  public API
# ──────────────────────────────────────────────────────────────
def clean_csv_dir(
    src_dir: str | Path,
    *,
    cleaned_dir: str | Path = "clean_csvs",
    archive_dir: str | Path = "csv_archive",
    header_rows: int = 3,
    footer_rows: int = 3,
    overwrite: bool = True,
) -> List[Path]:
    """
    • Reads every *.csv* in *src_dir*
    • Removes header/footer rows & drops unwanted Hebrew columns
    • Writes cleaned files to *cleaned_dir*
    • Moves originals to *archive_dir*

    Returns a list of cleaned CSV paths.
    """
    src_dir = Path(src_dir)
    cleaned_dir = Path(cleaned_dir)
    archive_dir = Path(archive_dir)
    _ensure_dirs(cleaned_dir, archive_dir)

    written: List[Path] = []

    for csv_path in src_dir.glob("*.csv"):
        cleaned = _process_one_csv(
            csv_path, cleaned_dir, archive_dir, header_rows=header_rows, footer_rows=footer_rows, overwrite=overwrite
        )
        if cleaned:
            written.append(cleaned)

    return written


# ──────────────────────────────────────────────────────────────
# 3.  ad-hoc CLI entry-point
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cleaned = clean_csv_dir(src_dir="converted_inputs")
    print(f"✅ Cleaned {len(cleaned)} CSV files.")
