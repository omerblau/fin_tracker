import numpy as np
import pandas as pd
import os

if __name__ == "__main__":

    csv_output_dir = "./csvs"
    input_dir = "./inputs"
    converted_inputes_dir = "./converted_inputes"

    os.makedirs(csv_output_dir, exist_ok=True)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(converted_inputes_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        excel_file_path = os.path.join(input_dir, filename)
        # Skip non-xlsx files if any
        if not filename.lower().endswith((".xlsx", ".xls")):
            print(f"Skipping non-excel file: {filename}")
            continue

        print(f"Processing file: {filename}")
        base_filename = os.path.splitext(os.path.basename(excel_file_path))[0]

        try:
            # Use 'with' statement to ensure the file is closed automatically
            with pd.ExcelFile(excel_file_path) as xls:
                sheet_names = xls.sheet_names
                print(f"Found sheets: {sheet_names}")

                # Loop through each sheet
                for sheet_name in sheet_names:
                    print(f"Processing sheet: '{sheet_name}'...")
                    try:
                        # Read the current sheet using the 'xls' object, skipping rows
                        df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=3, skipfooter=3)

                        # Construct the output CSV filename
                        safe_sheet_name = sheet_name.replace('"', "").replace("'", "").replace("/", "-")
                        csv_filename = f"{base_filename}_{safe_sheet_name}.csv"
                        csv_full_path = os.path.join(csv_output_dir, csv_filename)

                        # Save the DataFrame to CSV
                        df.to_csv(csv_full_path, index=False, encoding="utf-8-sig")
                        print(f"Saved sheet '{sheet_name}' to '{csv_full_path}'")

                    except Exception as e:
                        print(f"Error processing sheet '{sheet_name}': {e}")

            # --- File is guaranteed to be closed here ---

            # Move the file *after* the 'with' block has finished
            converted_inputes_path = os.path.join(converted_inputes_dir, filename)
            os.rename(excel_file_path, converted_inputes_path)
            print(f"Moved '{excel_file_path}' to '{converted_inputes_path}'")

        except FileNotFoundError:
            print(f"Error: Input file not found at {excel_file_path} (might have been moved already?)")
        except Exception as e:
            # Catch potential errors during file opening or moving
            print(f"Error processing file '{filename}': {e}")

    print("\nFinished processing all files.")
