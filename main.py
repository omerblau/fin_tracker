# main.py
from pathlib import Path
from utils_excel import process_inputs  # step 1  (Excel → CSV)
from utils_csv import clean_csv_dir  # step 2  (clean CSVs)





def main() -> None:
    # ── 1.  Excel → CSVs  ─────────────────────────────────────────────
    input_dir = Path("inputs")
    csv_output_dir = Path("csvs")  # holds *raw* CSVs
    workbook_archive = Path("converted_inputs")  # where .xlsx originals go

    raw_csvs = process_inputs(input_dir, csv_output_dir, workbook_archive)

    print(f"📄 {len(raw_csvs)} raw CSV files generated.")

    # ── 2.  Clean the CSVs  ───────────────────────────────────────────
    cleaned_csvs = clean_csv_dir(
        src_dir=csv_output_dir,  # read the raw CSVs we just produced
        cleaned_dir="clean_csvs",  # cleaned versions end up here
        archive_dir="csv_archive",  # raw CSVs are archived here
    )

    print(f"✅ {len(cleaned_csvs)} cleaned CSV files ready for analysis.")


if __name__ == "__main__":
    main()
