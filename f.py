import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from pathlib import Path

import U as U

st.set_page_config(page_title="financial analysis", page_icon="💲", layout="wide")

if "categories" not in st.seassion_state:
    st.session_state.categories = {"Uncategorised": []}

if U.categories_file.exists() and U.categories_file.is_file():
    with U.categories_file.open("r", encoding="utf-8") as f:
        st.session_state.categories = json.load(f)



def main():
    st.title("Dashboard")

    uploaded = st.file_uploader("Upload a CSV", type="csv")
    if not uploaded:
        st.info("Please upload a file to continue.")
        return

    df = U.load_transactions(uploaded)
    df = U.format_df(df)
    card_to_df = U.cards_to_dfs(df)
    if not card_to_df:
        st.info("No card-specific data found.")
        return

    U.render_tabs(df, card_to_df)


main()
