import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from pathlib import Path


categories_file = Path("categories.json")


def save_categories():
    with categories_file.open("w", encoding="utf-8") as f:
        json.dump(st.session_state.categories, f)


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


def format_df(df):
    cleaned = df.copy()
    cleaned.columns = [col.strip() for col in cleaned.columns]
    cleaned["תאריך עסקה"] = pd.to_datetime(cleaned["תאריך עסקה"], format="%d-%m-%Y")
    return cleaned


def cards_to_dfs(df):
    card_to_df = {}
    if df is not None:
        cards = df["4 ספרות אחרונות של כרטיס האשראי"].unique().tolist()

        for card in cards:
            card_df = df[df["4 ספרות אחרונות של כרטיס האשראי"] == card].copy()
            card_df = card_df.drop("4 ספרות אחרונות של כרטיס האשראי", axis=1)
            card_to_df[card] = card_df

    return card_to_df


def st_rtl(text: str, tag: str = "p") -> None:
    """Render `text` inside an RTL, right-aligned HTML element of type `tag`."""
    html = f"""
    <{tag} dir="rtl" style="text-align: right; margin: 0;">
      {text}
    </{tag}>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_tabs(df: pd.DataFrame, card_to_df: dict[str, pd.DataFrame]) -> None:
    """Draws one tab for All vs. each credit-card slice."""
    cards = list(card_to_df.keys())
    tab_labels = ["All Cards"] + [f"Card: {c}" for c in cards]
    tabs = st.tabs(tab_labels)

    for idx, tab in enumerate(tabs):
        with tab:
            if idx == 0:
                st_rtl("כל הכרטיסים", tag="h2")
                # st.subheader("כל הכרטיסים")
                st.write(df)
            else:
                card = cards[idx - 1]
                st_rtl((f"כרטיס המסתיים ב-{card}"), tag="h2")
                # st.subheader(f"כרטיס המסתיים ב-{card}")
                st.write(card_to_df[card])
