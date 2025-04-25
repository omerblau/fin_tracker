# main.py
from pathlib import Path
from utils_excel import process_inputs


def main() -> None:
    # Define the three working directories (as Path or str, either is fine)
    input_dir = Path("inputs")
    csv_output_dir = Path("csvs")
    archive_dir = Path("converted_inputs")

    # One-liner that does: mkdir -p, convert all workbooks, move originals
    created_csvs = process_inputs(input_dir, csv_output_dir, archive_dir)

    # From here on, work with the freshly generated CSVs
    print(f"✅ {len(created_csvs)} CSV files ready for further processing.")


if __name__ == "__main__":
    main()
