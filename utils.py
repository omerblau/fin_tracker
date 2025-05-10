import streamlit as st
import pandas as pd


def xl_to_csv_max(file):
    try:
        sheets = pd.read_excel(file, sheet_name=None, engine="openpyxl")

        first_sheet = next(iter(sheets.values()))
        st.session_state["month_year"] = first_sheet.iloc[1, 0]

        cleaned_dfs = []

        for df in sheets.values():
            headers = df.iloc[2]  # row 3 is header (index 2)
            cleaned_df = df.iloc[3:-3].reset_index(drop=True)
            cleaned_df.columns = headers
            cleaned_dfs.append(cleaned_df)

        combined_df = pd.concat(cleaned_dfs, ignore_index=True, sort=False)
        return combined_df

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


def format_df_max(df):
    cleaned = df.copy()
    cleaned.columns = [col.strip() for col in cleaned.columns]
    cleaned = cleaned.drop(
        [
            "סוג עסקה",
            "מטבע חיוב",
            "מטבע עסקה מקורי",
            "סכום עסקה מקורי",
            "מועדון הנחות",
            "מפתח דיסקונט",
            "תיוגים",
            "אופן ביצוע ההעסקה",
            "הערות",
            "תאריך חיוב",
            'שער המרה ממטבע מקור/התחשבנות לש"ח',
        ],
        axis=1,
    )
    cleaned["תאריך עסקה"] = pd.to_datetime(cleaned["תאריך עסקה"], format="%d-%m-%Y")
    return cleaned
