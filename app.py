import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Streamlit page config
st.set_page_config(page_title="ALL IN ONE Viewer", layout="wide")

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets"], scope)
client = gspread.authorize(credentials)

# Open your Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1CCJXoIBKWpGWybrr6Rs81p55m3dsIYcKJhBmBDQNR0k"
worksheet = client.open_by_url(sheet_url).worksheet("ALL IN ONE")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Automatically detect any date/time column
datetime_col = None
for col in df.columns:
    if 'date' in col.lower() or 'time' in col.lower():
        datetime_col = col
        break

# Try to convert and sort by detected datetime column
if datetime_col:
    try:
        df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')
        df = df.dropna(subset=[datetime_col])
        df = df.sort_values(by=datetime_col, ascending=False)
        st.success(f"Using datetime column: `{datetime_col}`")
    except Exception as e:
        st.warning(f"Could not parse datetime column `{datetime_col}`: {e}")
else:
    st.warning("⚠ No datetime column found in your sheet.")

# Show the data
st.dataframe(df)
