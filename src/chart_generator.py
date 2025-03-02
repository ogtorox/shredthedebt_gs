import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from faker import Faker

fake = Faker()

# Companies and image paths (assuming you have these saved locally or hosted somewhere)
companies = ["AHEAD", "McKinsey", "Deloitte", "Accenture", "KPMG", "SBG+", "Point B", "Assurety", "EY"]
company_logos = {
    "AHEAD": "logos/ahead.png",
    "McKinsey": "logos/mckinsey.png",
    "Deloitte": "logos/deloitte.png",
    "Accenture": "logos/accenture.png",
    "KPMG": "logos/kpmg.png",
    "SBG+": "logos/sbgplus.png",
    "Point B": "logos/pointb.png",
    "Assurety": "logos/assurety.png",
    "EY": "logos/ey.png",
}

def random_donation_amount():
    return round(random.triangular(1.50, 500, 35.45), 2)

def random_name():
    return fake.name()

def random_company():
    return random.choice(companies)

def generate_fake_data(num_entries=20):
    data = {
        "Name": [random_name() for _ in range(num_entries)],
        "Donation": [random_donation_amount() for _ in range(num_entries)],
        "Company": [random_company() for _ in range(num_entries)],
    }
    return pd.DataFrame(data)

df = generate_fake_data(20)

# Aggregate donations by company
company_donations = df.groupby("Company", as_index=False)["Donation"].sum()

# Plot with matplotlib
fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(company_donations["Company"], company_donations["Donation"], color="skyblue")
ax.set_xlabel("Total Donations ($)")

# Add logos at the end of bars
for i, row in company_donations.iterrows():
    company = row["Company"]
    donation = row["Donation"]

    logo_path = company_logos.get(company)
    if logo_path:
        img = mpimg.imread(logo_path)
        imagebox = ax.imshow(img, aspect="auto", extent=[donation + 10, donation + 60, i - 0.3, i + 0.3])

# Display the chart in Streamlit
st.pyplot(fig)

#total donation amount to eb displayed against goal
total_donations = df["Donation"].sum()

df["Donation"] = df["Donation"].map("${:,.2f}".format)

st.metric(label="Total Donations", value=f"${total_donations:,.2f}", delta=f"Goal: $15,000")
st.table(df)