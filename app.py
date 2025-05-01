import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up page
st.set_page_config(page_title="All-in-One Sheet", layout="wide")

# Google Sheets Auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets"], scope)
client = gspread.authorize(credentials)

# Load data
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CCJXoIBKWpGWybrr6Rs81p55m3dsIYcKJhBmBDQNR0k")
worksheet = spreadsheet.worksheet("ALL IN ONE")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Identify the datetime column safely
datetime_col = None
for col in df.columns:
    if "date" in col.lower() or "time" in col.lower():
        datetime_col = col
        break

# Parse datetime if found
if datetime_col:
    df[datetime_col] = pd.to_datetime(df[datetime_col], errors="coerce")
    df.dropna(subset=[datetime_col], inplace=True)
    df = df.sort_values(by=datetime_col, ascending=False)
else:
    st.warning("No datetime-related column found in the sheet.")

# Display
st.title("📊 All-in-One Google Sheet Viewer")
st.dataframe(df)
