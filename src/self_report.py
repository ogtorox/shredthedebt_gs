import streamlit as st
import pandas as pd

# URL of your public Google Sheet (published CSV link for self-reported data)
SELF_REPORT_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQs9wnOCExP42cbnSKIMFGJshEtkXKNPKEMc9_e99JTk3acOlbFLB9bu5aEOmUjt2AMxeTPqid9w46Y/pub?output=csv"

def render_donation_form():
    st.markdown("### Self-Report Your Donation")
    
    with st.form("donation_form"):
        name = st.text_input("Your name")
        company = st.selectbox("Your company", ["AHEAD", "Deloitte", "Accenture", "KPMG", "SBG+", "Point B", "EY"])
        amount = st.number_input("Donation amount ($)", min_value=1.0, step=1.0)
        confirm = st.checkbox("I confirm I have donated and have the receipt")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if confirm:
                # Log locally or eventually push to a service/backend
                st.success("Thank you for your donation! It has been logged and is pending verification with our team.")
            else:
                st.error("❗You must confirm your donation to submit.❗")