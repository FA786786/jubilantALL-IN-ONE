import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set Streamlit title
st.title("📊 Google Sheets Viewer")

# Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE"  # Replace this with your actual sheet URL

# Load Google Sheet data
@st.cache_data
def load_sheet(sheet_url):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            st.secrets["google_sheets"], scope
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url)
        data = sheet.sheet1.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"❌ Failed to load sheet: {e}")
        return pd.DataFrame()

# Show sheet data
df = load_sheet(SHEET_URL)

if not df.empty:
    st.success("✅ Sheet loaded successfully!")
    st.dataframe(df)
else:
    st.warning("⚠️ No data found or sheet couldn't be loaded.")
