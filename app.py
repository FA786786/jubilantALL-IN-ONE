import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set page
st.set_page_config(page_title="🧾 All-in-One Sheet Viewer", layout="wide")

# Auth setup using Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets"], scope)
client = gspread.authorize(credentials)

# Load Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1CCJXoIBKWpGWybrr6Rs81p55m3dsIYcKJhBmBDQNR0k"
worksheet = client.open_by_url(sheet_url).worksheet("ALL IN ONE")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Try to detect and convert any date/time column
datetime_col = None
for col in df.columns:
    if 'date' in col.lower() or 'time' in col.lower():
        datetime_col = col
        break

# Safely convert to datetime if found
if datetime_col:
    df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
    df.dropna(subset=[datetime_col], inplace=True)
    df = df.sort_values(by=datetime_col, ascending=False)
    st.success(f"Using datetime column: `{datetime_col}`")
else:
    st.warning("⚠️ No datetime column found. Displaying raw data.")

# Show DataFrame
st.dataframe(df)
