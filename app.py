import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("Jubilant All-in-One App")

try: df['datetime'] = pd.to_datetime(df['datetime'])
    # --- SETUP GOOGLE SHEETS ---
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["google_sheets"], scopes=scope)
    client = gspread.authorize(creds)

    # --- OPEN SHEET ---
    sheet_url = "https://docs.google.com/spreadsheets/d/1CCJXoIBKWpGWybrr6Rs81p55m3dsIYcKJhBmBDQNR0k/edit?usp=sharing"
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # --- DISPLAY RAW DATA ---
    st.subheader("Raw Sheet Data")
    st.write(df)

    # --- FIND DATETIME COLUMN ---
    datetime_column = None
    for col in df.columns:
        if col.strip().lower() in ["datetime", "date"]:
            datetime_column = col
            break

    if datetime_column:
        df[datetime_column] = pd.to_datetime(df[datetime_column], errors="coerce")
        st.subheader(f"Parsed {datetime_column} column")
        st.write(df[[datetime_column]])

        if df[datetime_column].notnull().any():
            st.success("✅ Datetime parsing successful.")
        else:
            st.warning("⚠️ All datetime values are invalid (NaT). Check the data format in Google Sheet.")
    else:
        st.error("❌ No 'datetime' or 'date' column found in the sheet.")

except Exception as e:
    st.error(f"Something went wrong:\n\n{str(e)}")
