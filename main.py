# main.py
import streamlit as st
import pandas as pd
from src.chart_generator import generate_chart

st.set_page_config(page_title="Shred the Debt", layout="wide")

# Enhanced background and container styling
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: #E6F0FA;
        font-family: 'Segoe UI', sans-serif;
    }

    .stApp {
        padding: 2rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #1B365D;
    }

    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    [data-testid="stMetric"] div {
        color: #1B365D;
        font-size: 1.2rem;
        font-weight: 600;
    }

    /* Transparent white background for the dataframe with soft shadow */
    [data-testid="stDataFrame"] div[data-testid="stVerticalBlock"] {
        background-color: rgba(255, 255, 255, 0.92);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    }

    /* Refined link buttons */
    .stButton > button {
        background-color: #1B365D;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
    }
    .stButton > button:hover {
        background-color: #163050;
        color: #f4f4f4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load and clean data
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQs9wnOCExP42cbnSKIMFGJshEtkXKNPKEMc9_e99JTk3acOlbFLB9bu5aEOmUjt2AMxeTPqid9w46Y/pub?output=csv"

@st.cache_data
def get_gsheet_data():
    df = pd.read_csv(SHEET_CSV_URL)
    df["Amount"] = df["Amount"].astype(str).str.replace(r"[^0-9.\\-]", "", regex=True)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
    return df

df = get_gsheet_data()

# Show metrics
total_donations = df["Amount"].sum()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Donations", value=f"${total_donations:,.2f}", delta="Goal: $15,000")
with col3:
    st.link_button("Chicago Global Shapers", "https://www.chicagoshapers.org/")
with col4:
    st.link_button("DONATE HERE", "https://unduemedicaldebt.org/campaign/shred-the-debt-greater-chicago-region/#")

# Generate and display chart
fig = generate_chart(df)
st.pyplot(fig)

# Show raw data
df["Amount"] = df["Amount"].map("${:,.2f}".format)
st.dataframe(df, hide_index=True, width=800)