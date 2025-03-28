import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import requests
import io
import matplotlib.ticker as mtick
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Companies and image paths (assuming you have these saved locally or hosted somewhere)
#companies = ["AHEAD", "Deloitte", "Accenture", "KPMG", "SBG+", "Point B", "Assurety", "EY"]
companies = ["Alexis L.", "Hannah C.", "Stephanie G.", "Daniel K.", "Macaila B.", "Frankie G.", "Shahaan M.", "Mohit S."]
shapers = {
    "AHEAD": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/alexis_ahead.jpg",
    "Deloitte": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/hannah_deloitte.jpg",
    "Accenture": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/stephanie_accenture.jpg",
    "KPMG": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/daniel_kpmg.jpg",
    "SBG+": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/macaila_sbg%2B.jpg",
    "Point B": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/frankie_pointb.jpg",
    "Assurety": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/shahaan_assurety.jpg",
    "EY": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/mohit_ey.jpg"
}

# Fetch images (unchanged)
def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return mpimg.imread(io.BytesIO(response.content), format='jpg')

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1g3fjjdVelmp2idBj4ijUqzyx6ampCM-vK-fa7Ya97Fw'  # ← Replace this with your actual Sheet ID
RANGE_NAME = 'Data!A1:D1000'  # ← Adjust if your sheet/tab has a different name or range

@st.cache_resource
def get_gsheet_data():
    credentials_dict = {
        "type": st.secrets["google"]["type"],
        "project_id": st.secrets["google"]["project_id"],
        "private_key_id": st.secrets["google"]["private_key_id"],
        "private_key": st.secrets["google"]["private_key"],
        "client_email": st.secrets["google"]["client_email"],
        "client_id": st.secrets["google"]["client_id"],
        "auth_uri": st.secrets["google"]["auth_uri"],
        "token_uri": st.secrets["google"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["google"]["client_x509_cert_url"]
    }

    creds = service_account.Credentials.from_service_account_info(
        credentials_dict, scopes=SCOPES
    )

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        st.error("No data found in the sheet.")
        return pd.DataFrame()

    headers = values[0]
    data = values[1:]
    df = pd.DataFrame(data, columns=headers)

    df["Amount"] = (
        df["Amount"]
        .astype(str)
        .str.replace(r"[^0-9.\-]", "", regex=True)
    )

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Amount"] = df["Amount"].fillna(0)

    return df

df = get_gsheet_data()

# Aggregate donations by company
company_donations = df.groupby("Company", as_index=False)["Amount"].sum()

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(company_donations["Company"], company_donations["Amount"], color="skyblue")
ax.set_xlabel("Total Donations ($)")
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

# Total donation amount
total_donations = df["Amount"].sum()
df["Amount"] = df["Amount"].map("${:,.2f}".format)

# Streamlit Layout
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Donations", value=f"${total_donations:,.2f}", delta=f"Goal: $15,000")
with col3:
    st.link_button("Chicago Global Shapers", "https://www.chicagoshapers.org/")
with col4:
    st.link_button("DONATE HERE", "https://unduemedicaldebt.org/campaign/shred-the-debt-greater-chicago-region/#")

with st.container():
    st.pyplot(fig)
    st.dataframe(df, hide_index=True, width=800)