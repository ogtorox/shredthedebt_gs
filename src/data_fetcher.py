# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import time

# # Constants
# CAMPAIGN_URL = 'https://unduemedicaldebt.org/campaign/shred-the-debt-greater-chicago-region/'
# REFRESH_INTERVAL = 30  # seconds

# @st.cache_data(ttl=REFRESH_INTERVAL)
# def fetch_donations():
#     """Scrape the recent donations from the campaign page."""
#     response = requests.get(CAMPAIGN_URL)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     donations = []
#     for entry in soup.select('.recentDonationList .listgrid'):
#         amount = entry.select_one('.amount').text.strip()
#         name = entry.select_one('.name')
#         name = name.text.strip() if name else 'Anonymous'
#         status = entry.select_one('.justdonated')
#         status = status.text.strip() if status else ''

#         donations.append({
#             'amount': amount,
#             'name': name,
#             'status': status
#         })
#     return donations

# # Page Config
# st.set_page_config(page_title="Shred the Debt - Live Donations", page_icon="💸")
# st.title("💸 Shred the Debt - Greater Chicago Region")
# st.subheader("🎉 Live Donations Feed")

# # Donations Display
# donations = fetch_donations()

# with st.container():
#     for donation in donations:
#         st.write(f"💰 {donation['amount']} - {donation['name']} ({donation['status']})")

# # Auto-refresh Trick using Streamlit Magic
# st.write("🔄 This page refreshes every 30 seconds.")
# time.sleep(REFRESH_INTERVAL)
# st.rerun()

import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")

df = conn.read(
worksheet="Sheet1",
ttl="10m",
usecols=[0, 1],
nrows=3
)