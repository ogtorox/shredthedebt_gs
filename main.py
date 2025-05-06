import streamlit as st
from src.data_fetcher import get_gsheet_data
from src.chart_generator import generate_chart  # if you have a chart function

st.set_page_config(page_title="Shred the Debt", layout="wide")

# Custom background color
st.markdown(
    """
    <style>
    body {
        background-color: #fdf6f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
df = get_gsheet_data()

# Show metrics
total = df["Amount"].sum()
st.metric("Total Donations", f"${total:,.2f}", delta="Goal: $15,000")

# Show chart
fig = generate_chart(df)  # or just put your chart code here directly
st.pyplot(fig)

# Show data
st.dataframe(df, hide_index=True)
