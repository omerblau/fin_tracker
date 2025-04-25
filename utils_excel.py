# utils_excel.py
from pathlib import Path
import pandas as pd
import shutil
import re


def init_dirs(
    csv_output_dir: str | Path, input_dir: str | Path, converted_inputs_dir: str | Path
) -> tuple[Path, Path, Path]:

    csv_output_dir, input_dir, converted_inputs_dir = map(Path, (csv_output_dir, input_dir, converted_inputs_dir))
    for d in (csv_output_dir, input_dir, converted_inputs_dir):
        d.mkdir(parents=True, exist_ok=True)
    return csv_output_dir, input_dir, converted_inputs_dir


def is_excel_file(path: str | Path) -> bool:
    return Path(path).suffix.lower() in {".xlsx", ".xls"}


_illegal = re.compile(r'[<>:"/\\|?*\']')  # any char you don’t want in a filename


def xlsx_to_csvs(xlsx_path: str | Path, out_dir: str | Path) -> list[Path]:
    """
    Convert *all* sheets in an Excel workbook to individual CSVs.

    Returns a list of the CSV paths that were written.
    Raises FileNotFoundError if the workbook is missing.
    """
    xlsx_path = Path(xlsx_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_paths: list[Path] = []
    try:
        with pd.ExcelFile(xlsx_path) as xls:
            for sheet in xls.sheet_names:
                csv_paths.append(_save_sheet_as_csv(xls, sheet, out_dir))
        return csv_paths

    # Let the caller decide what to do with these
    except FileNotFoundError:
        raise  # bubble up – the caller can catch
    except Exception as exc:
        raise RuntimeError(f"Failed while processing {xlsx_path}") from exc


def _save_sheet_as_csv(xls: pd.ExcelFile, sheet_name: str, out_dir: Path) -> Path:
    """Helper: save one sheet; assume *xls* is already open."""
    df = pd.read_excel(xls, sheet_name=sheet_name)
    stem = Path(xls.io).stem  # original filename, no extension
    safe = _illegal.sub("-", sheet_name)  # strip bad chars

    csv_path = out_dir / f"{stem}_{safe}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    return csv_path


def move_file(src: str | Path, dst_dir: str | Path, *, overwrite: bool = False) -> Path:

    src_path = Path(src).expanduser().resolve(strict=True)  # strict → raises if missing
    if not src_path.is_file():
        raise FileNotFoundError(f"{src_path} is not a regular file")

    dst_dir = Path(dst_dir).expanduser().resolve()
    dst_dir.mkdir(parents=True, exist_ok=True)

    dst_path = dst_dir / src_path.name
    if dst_path.exists() and not overwrite:
        raise FileExistsError(f"{dst_path} already exists (use overwrite=True to replace)")

    # shutil.move handles cross-device moves and preserves metadata where possible.
    shutil.move(str(src_path), str(dst_path))
    return dst_path


def process_inputs(input_dir: str | Path, csv_output_dir: str | Path, archive_dir: str | Path) -> list[Path]:

    input_dir, csv_output_dir, archive_dir = map(Path, (input_dir, csv_output_dir, archive_dir))
    
    for d in (input_dir, csv_output_dir, archive_dir):
        d.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []

    for excel_path in input_dir.iterdir():
        if not excel_path.is_file():
            continue
        if not is_excel_file(excel_path):
            print(f"Skipping non-Excel: {excel_path.name}")
            continue
        try:
            written += xlsx_to_csvs(excel_path, csv_output_dir)
            move_file(excel_path, archive_dir)
        except Exception as exc:
            print(f"⚠️  Problem with {excel_path.name}: {exc}")

    return written


# CLI entry-point
if __name__ == "__main__":
    created = process_inputs("inputs", "csvs", "converted_inputs")
    print(f"✅ {len(created)} CSV files generated.")
