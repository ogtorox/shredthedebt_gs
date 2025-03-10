import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from faker import Faker
import requests
import io
import matplotlib.ticker as mtick

fake = Faker()

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

# Desired number of entries & cap
number_of_entries = 100
total_cap = 2664.10

# Fetch images (unchanged)
def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return mpimg.imread(io.BytesIO(response.content), format='jpg')

# Random donation generator
def random_donation_amount(remaining_budget):
    max_possible = min(500, remaining_budget)
    return round(random.triangular(1.50, max_possible, 5.45), 2)

# Random helpers
def random_name():
    return fake.name()

def random_company():
    return random.choice(companies)

# Generate fake data respecting total cap
def generate_fake_data(num_entries=number_of_entries, total_cap=3000):
    data = []
    remaining_budget = total_cap

    for _ in range(num_entries):
        if remaining_budget < 1.50:
            break

        donation = random_donation_amount(remaining_budget)
        donation = min(donation, remaining_budget)

        data.append({
            "Name": random_name(),
            "Donation": donation,
            "Shaper/Company": random_company(),
        })

        remaining_budget -= donation
        if remaining_budget <= 0:
            break

    return pd.DataFrame(data)

# Create DataFrame
df = generate_fake_data(number_of_entries, total_cap)

# Aggregate donations by company
company_donations = df.groupby("Shaper/Company", as_index=False)["Donation"].sum()

# Plot with matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(company_donations["Shaper/Company"], company_donations["Donation"], color="skyblue")
ax.set_xlabel("Total Donations ($)")
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

# Total donation amount to be displayed against goal
total_donations = df["Donation"].sum()
df["Donation"] = df["Donation"].map("${:,.2f}".format)

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