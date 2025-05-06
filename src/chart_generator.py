import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import requests
import io
import matplotlib.ticker as mtick
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Define company-to-image mapping
shapers = {
    "AHEAD": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/head_pngs/alexis_ahead.png",
    "Deloitte": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/head_pngs/hannah_deloitte.png",
    "Accenture": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/head_pngs/stephanie_accenture.png",
    "KPMG": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/head_pngs/daniel_kpmg.png",
    "SBG+": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/head_pngs/macaila_sbg%2B.png",
    "Point B": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/head_pngs/frankie_pointb.png",
    "EY": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/head_pngs/mohit_ey.png"
}


# Fetch image from URL
def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return mpimg.imread(io.BytesIO(response.content), format='png')

# Use published CSV link from Google Sheets
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQs9wnOCExP42cbnSKIMFGJshEtkXKNPKEMc9_e99JTk3acOlbFLB9bu5aEOmUjt2AMxeTPqid9w46Y/pub?output=csv"

@st.cache_data
def get_gsheet_data():
    df = pd.read_csv(SHEET_CSV_URL)

    # Clean and format Amount column
    df["Amount"] = df["Amount"].astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    return df

# Load and group data
df = get_gsheet_data()
company_donations = df.groupby("Company", as_index=False)["Amount"].sum()


# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(company_donations["Company"], company_donations["Amount"], color="skyblue")
ax.set_xlabel("Total Donations ($)")
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

# Add images at the end of bars
for bar, company in zip(bars, company_donations["Company"]):
    image_url = shapers.get(company)
    if image_url:
        try:
            img = fetch_image(image_url)
            oi = OffsetImage(img, zoom=0.10)  # 👈 adjust zoom here for all images
            ab = AnnotationBbox(
                oi,
                (bar.get_width() + 100, bar.get_y() + bar.get_height() / 2),
                xybox=(10, 0),
                xycoords='data',
                boxcoords="offset points",
                frameon=False
            )
            ax.add_artist(ab)
        except Exception as e:
            print(f"Error loading image for {company}: {e}")


fig.patch.set_alpha(0.0)  # make the figure background transparent
ax.patch.set_alpha(0.0)   # make the axes background transparent
plt.tight_layout()

# Streamlit metrics
total_donations = df["Amount"].sum()
df["Amount"] = df["Amount"].map("${:,.2f}".format)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Donations", value=f"${total_donations:,.2f}", delta="Goal: $15,000")
with col3:
    st.link_button("Chicago Global Shapers", "https://www.chicagoshapers.org/")
with col4:
    st.link_button("DONATE HERE", "https://unduemedicaldebt.org/campaign/shred-the-debt-greater-chicago-region/#")

with st.container():
    st.pyplot(fig)
    st.dataframe(df, hide_index=True, width=800)
