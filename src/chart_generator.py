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
companies = ["AHEAD", "Deloitte", "Accenture", "KPMG", "SBG+", "Point B", "Assurety", "EY"]
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

# definition to fetch URLs using requests
def fetch_image(url):
    response = requests.get(url)  
    response.raise_for_status()   
    return mpimg.imread(io.BytesIO(response.content), format='jpg')

def random_donation_amount():
    return round(random.triangular(1.50, 500, 15.45), 2)

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

df = generate_fake_data(150)

# Aggregate donations by company
company_donations = df.groupby("Company", as_index=False)["Donation"].sum()

# Plot with matplotlib
fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(company_donations["Company"], company_donations["Donation"], color="skyblue")
ax.set_xlabel("Total Donations ($)")
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

# for i, row in enumerate(company_donations.itertuples()):
#     company = row.Company
#     donation = row.Donation

#     logo_url = shapers.get(company)
#     if logo_url:
#         img = fetch_image(logo_url)

#         # Get the actual bar height from matplotlib (this is critical)
#         bar_height = ax.patches[i].get_height()

#         # Placement logic (put image to the right of the bar)
#         img_aspect = img.shape[1] / img.shape[0]  # Width / Height (should be 1 for 80x80)

#         # Use bar height to control image size
#         image_width = bar_height * img_aspect  # Should be same since 80x80 is square
#         image_height = bar_height  # Fit vertically to the bar

#         # Place image directly after the bar ends
#         extent = [donation + 5, donation + 5 + image_width, i - bar_height/2, i + bar_height/2]

#         ax.imshow(img, extent=extent, aspect='auto', zorder=3)

#total donation amount to be displayed against goal
total_donations = df["Donation"].sum()
df["Donation"] = df["Donation"].map("${:,.2f}".format)

# col1, col2, col3 = st.columns([1, 1, 1])
tab1, tab2, tab3, tab4 = st.tabs(["Tracker", "Rules", st.link_button("Go to Chicago Global Shapers", "https://www.chicagoshapers.org/"), st.link_button("DONATE HERE", "https://unduemedicaldebt.org/campaign/shred-the-debt-greater-chicago-region/#")])
with tab1:
    col1, col2, col3, col4 = st.columns([1,2,2,1])
    with col1:
        st.metric(label="Total Donations", value=f"${total_donations:,.2f}", delta=f"Goal: $15,000") 
    # with col3:   
    # # with col3: 
    #     st.link_button("Go to Chicago Global Shapers", "https://www.chicagoshapers.org/")
    # with col4:
    #     st.link_button("DONATE HERE", "https://unduemedicaldebt.org/campaign/shred-the-debt-greater-chicago-region/#")

    with st.container():
        st.pyplot(fig)
        st.table(df.style.hide(axis="index"))
with tab2:
    st.markdown("These are the rules. Include the related associated initlas in your FIRST NAME, make sure you donation is not marked anonynmous, and your donation will be included. May the best secure bragging rights.")