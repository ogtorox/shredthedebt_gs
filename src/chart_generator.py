import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from faker import Faker
import requests
import io

fake = Faker()

# Companies and image paths (assuming you have these saved locally or hosted somewhere)
companies = ["AHEAD", "McKinsey", "Deloitte", "Accenture", "KPMG", "SBG+", "Point B", "Assurety", "EY"]
shapers = {
    "AHEAD": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/alexis_ahead.jpg",
    # "McKinsey": "logos/mckinsey.png",
    "Deloitte": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/hannah_deloitte.jpg",
    "Accenture": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/stephanie_accenture.jpg",
    "KPMG": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/daniel_kpmg.jpg",
    "SBG+": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/macaila_sbg%2B.jpg",
    "Point B": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/frankie_pointb.jpg",
    "Assurety": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/shahaan_assurety.jpg",
    "EY": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/mohit_ey.jpg"
}

# definition to fetch URLs using requests
def fetch_image(url):
    response = requests.get(url)  
    response.raise_for_status()   
    return mpimg.imread(io.BytesIO(response.content), format='jpg')


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


fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(company_donations["Company"], company_donations["Donation"], color="skyblue")
ax.set_xlabel("Total Donations ($)")

for i, row in company_donations.iterrows():
    company = row["Company"]
    donation = row["Donation"]

    logo_url = shapers.get(company)
    if logo_url:
        img = fetch_image(logo_url)  # This loads a numpy array image

        # Get bar height (dynamic based on matplotlib rendering)
        bar_height = ax.patches[i].get_height()

        # Calculate aspect ratio and scaled width to match bar height
        aspect_ratio = img.shape[1] / img.shape[0]
        width = bar_height * aspect_ratio

        # Now fit the image into the bar height properly
        ax.imshow(img, extent=[donation + 10, donation + 10 + width, i - bar_height/2, i + bar_height/2])


#total donation amount to eb displayed against goal
total_donations = df["Donation"].sum()

df["Donation"] = df["Donation"].map("${:,.2f}".format)

st.metric(label="Total Donations", value=f"${total_donations:,.2f}", delta=f"Goal: $15,000")
st.pyplot(fig)
st.table(df)