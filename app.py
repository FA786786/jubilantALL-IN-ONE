import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Set up Google Sheets credentials
json_key = st.secrets["google_sheets"]
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
credentials = Credentials.from_service_account_info(json_key, scopes=scopes)
client = gspread.authorize(credentials)

# Google Sheet URL or ID
sheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE"
sheet = client.open_by_url(sheet_url).sheet1

# Load data into DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Optional: parse datetime if column exists
if 'datetime' in df.columns:
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Display in Streamlit
st.title("Google Sheet Viewer")
st.dataframe(df)
