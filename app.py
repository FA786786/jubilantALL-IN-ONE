import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set page config
st.set_page_config(page_title="All-in-One Sheet Viewer", layout="wide")

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets"], scope)
client = gspread.authorize(credentials)

# Open the sheet
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1CCJXoIBKWpGWybrr6Rs81p55m3dsIYcKJhBmBDQNR0k/edit?usp=sharing")
worksheet = spreadsheet.worksheet("ALL IN ONE")

# Get data into dataframe
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Parse 'Date' or 'datetime' column safely
datetime_column = "Date" if "Date" in df.columns else "datetime"
if datetime_column in df.columns:
    try:
        df[datetime_column] = pd.to_datetime(df[datetime_column], errors="coerce")
    except Exception as e:
        st.error(f"Error converting {datetime_column} to datetime: {e}")

# Optional: drop rows or columns here
# df.drop(columns=['UnwantedColumn'], inplace=True)  # example
# df.dropna(subset=[datetime_column], inplace=True)

# Show dataframe
st.title("All-in-One Sheet Viewer")
st.dataframe(df)
