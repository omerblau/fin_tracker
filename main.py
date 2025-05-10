# main.py
import streamlit as st

import utils as U

st.set_page_config(page_title="financial analysis", page_icon="💰", layout="wide")


def main():
    st.title("Dashboard")

    uploaded = st.file_uploader("drop the max file below", type=["xlsx"])
    if not uploaded:
        st.info("Drop transaction file from Max to start!")
        return

    filename = uploaded.name
    if filename.endswith(".xlsx"):
        df, transactions_date = U.xl_to_csv_max(uploaded)
        df = U.format_df_max(df)
        st.write(df)

    csrds_dfs = U.transactions_to_cards(df)
    st.write(csrds_dfs["1294"])


main()
