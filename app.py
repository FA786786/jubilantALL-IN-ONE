import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="All-in-One Sheet Viewer", layout="wide")

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets"], scope)
client = gspread.authorize(credentials)

# Load data from Google Sheet
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CCJXoIBKWpGWybrr6Rs81p55m3dsIYcKJhBmBDQNR0k")
worksheet = spreadsheet.worksheet("ALL IN ONE")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Handle datetime column parsing
datetime_col = None
for col in df.columns:
    if "date" in col.lower():
        datetime_col = col
        break

if datetime_col:
    df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')

# Optional: Drop rows where datetime parsing failed
df.dropna(subset=[datetime_col], inplace=True)

# Streamlit output
st.title("📊 All-in-One Google Sheet Viewer")
st.success(f"Loaded {len(df)} rows from 'ALL IN ONE'")
st.dataframe(df)
