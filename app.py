import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("Jubilant All-in-One App: Data Verification & Parsing")

try:
    # --- SETUP GOOGLE SHEETS CONNECTION ---
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["google_sheets"], scopes=scope)
    client = gspread.authorize(creds)

    # --- OPEN SHEET & FETCH DATA ---
    sheet_url = "https://docs.google.com/spreadsheets/d/1CCJXoIBKWpGWybrr6Rs81p55m3dsIYcKJhBmBDQNR0k/edit?usp=sharing"
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()

    # --- CONVERT TO DATAFRAME ---
    df = pd.DataFrame(data)

    # Step 1: Show Raw Data
    st.subheader("Step 1: Google Sheet Data")
    if df.empty:
        st.error("❌ Sheet is empty. Please check if data is filled in.")
    else:
        st.success(f"✅ Loaded {len(df)} rows from sheet.")
        st.dataframe(df)

    # Step 2: Column Name Check
    st.subheader("Step 2: Column Check")
    st.write("Available columns:", list(df.columns))

    datetime_column = None
    for col in df.columns:
        if col.strip().lower() in ['datetime', 'date']:
            datetime_column = col
            break

    if datetime_column:
        st.success(f"✅ Found datetime column: {datetime_column}")
        
        # Step 3: Try converting to datetime
        df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')

        st.subheader("Step 3: Parsed Datetime Column")
        st.write(df[[datetime_column]])

        if df[datetime_column].notnull().any():
            st.success("✅ Datetime conversion successful.")
        else:
            st.warning("⚠️ Datetime column found, but all values are invalid (NaT). Check the format.")
    else:
        st.error("❌ No 'datetime' or 'date' column found in your sheet.")

except Exception as e:
    st.error(f"🚨 Error: {e}")
