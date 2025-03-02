import requests

def get_donation_data():
    response = requests.get("https://unduemedicaldebt.org/campaign/shred-the-debt-greater-chicago-region.json")
    data = response.json()
    return data

print(get_donation_data)