import streamlit as st
import pandas as pd
from auth import get_google_sheet

st.title("📊 Jubilant All-In-One: Google Sheet Data Viewer")

# STEP 1: Load from Streamlit secrets
json_key = st.secrets["google_sheets"]

# STEP 2: Google Sheet URL
sheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0"

# STEP 3: Load data
try:
    df = get_google_sheet(sheet_url, json_key)

    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        st.success("Datetime converted successfully!")
    else:
        st.warning("No 'datetime' column found.")

    st.dataframe(df)

except Exception as e:
    st.error(f"Error: {e}")
