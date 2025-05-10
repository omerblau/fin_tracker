import streamlit as st

import utils as U

st.set_page_config(page_title="financial analysis", page_icon="💰", layout="wide")


def main():
    st.title("Dashboard")

    st.info("Drop XLSX from leumi's website to conver to CSV.")
    uploaded = st.file_uploader("", type=["xlsx"])

    if not uploaded:
        st.info("Drop a file to continue")
        return

    filename = uploaded.name
    if filename.endswith(".xlsx"):
        df = U.xl_to_csv_max(uploaded)
        df = U.format_df_max(df)
        print(df)
        st.write(df)
        st.session_state["df"] = df


main()
