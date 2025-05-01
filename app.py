import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Setup Streamlit title
st.title("Jubilant All-in-One App")

# Load credentials from secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["google_sheets"], scopes=scope)
client = gspread.authorize(creds)

# Load your Google Sheet
sheet_url = 'https://docs.google.com/spreadsheets/d/1CCJXoIBKWpGWybrr6Rs81p55m3dsIYcKJhBmBDQNR0k/edit?gid=0'
sheet = client.open_by_url(sheet_url).sheet1
data = sheet.get_all_records()

# Ensure df is properly created from Google Sheets data
df = pd.DataFrame(data)

# Display the raw data for debugging purposes
st.subheader("Raw Data")
st.write(df)

# Check if 'datetime' or 'date' column exists, and convert it
datetime_column = None
for col in df.columns:
    if col.strip().lower() in ['datetime', 'date']:
        datetime_column = col
        break

if datetime_column:
    # Convert the column to datetime, with error handling
    df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')
    st.subheader(f"Parsed {datetime_column}")
    st.write(df[[datetime_column]])
else:
    st.error("❌ No 'datetime' or 'date' column found in the sheet.")

# Proceed with other logic if datetime is parsed
if datetime_column and df[datetime_column].notnull().any():
    st.success("✅ Datetime column parsed successfully.")
else:
    st.warning("⚠️ Datetime parsing failed or no valid dates found.")
