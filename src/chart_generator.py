# src/chart_generator.py
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import requests
import io

# Define image links for each company
shapers = {
    "AHEAD": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/shredthedebt_gs/head_pngs/alexis_ahead.png",
    "Deloitte": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/shredthedebt_gs/head_pngs/hannah_deloitte.png",
    "Accenture": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/shredthedebt_gs/head_pngs/stephanie_accenture.png",
    "KPMG": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/shredthedebt_gs/head_pngs/daniel_kpmg.png",
    "SBG+": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/shredthedebt_gs/head_pngs/macaila_sbg%2B.png",
    "Point B": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/shredthedebt_gs/head_pngs/frankie_pointb.png",
    "EY": "https://raw.githubusercontent.com/ogtorox/shredthedebt_gs/main/shredthedebt_gs/head_pngs/mohit_ey.png"
}

# Define bar colors for each company
colors = {
    "AHEAD": "skyblue",
    "Deloitte": "lightgreen",
    "Accenture": "purple",
    "KPMG": "blue",
    "SBG+": "red",
    "Point B": "royalblue",
    "EY": "green"
}

def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return mpimg.imread(io.BytesIO(response.content), format='png')

def generate_chart(df):
    company_donations = df.groupby("Company", as_index=False)["Amount"].sum()
    bar_colors = [colors.get(company, "gray") for company in company_donations["Company"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(company_donations["Company"], company_donations["Amount"], color=bar_colors)
    ax.set_xlabel("Total Donations ($)")
    bar_max = company_donations["Amount"].max()
    ax.set_xlim(0, bar_max + 1000)
    ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

    # Add headshots at end of bars
    for bar, company in zip(bars, company_donations["Company"]):
        image_url = shapers.get(company)
        if image_url:
            try:
                img = fetch_image(image_url)
                oi = OffsetImage(img, zoom=0.2)
                ab = AnnotationBbox(
                    oi,
                    (bar.get_width() + 150, bar.get_y() + bar.get_height() / 2),
                    xybox=(-50, 0),
                    xycoords='data',
                    boxcoords="offset points",
                    frameon=False
                )
                ax.add_artist(ab)
            except Exception as e:
                print(f"Error loading image for {company}: {e}")

    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    plt.tight_layout()
    return fig
# hi
