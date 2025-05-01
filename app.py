import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Authenticate Google Sheets API using Streamlit Secrets
def authenticate_google_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["google_sheets"], 
        ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    return client

# Access a specific Google Sheet
def get_google_sheet(sheet_name):
    client = authenticate_google_sheets()
    sheet = client.open(sheet_name).sheet1  # Open the first sheet
    return sheet

# Load data from Google Sheets into a DataFrame
def load_data_from_sheets(sheet_name):
    sheet = get_google_sheet(sheet_name)
    data = sheet.get_all_records()  # Get all records from the sheet
    df = pd.DataFrame(data)
    return df

# Process the data: remove columns and convert datetime
def process_data(df):
    # Remove specific columns
    df = df.drop(columns=['column1', 'column2'], errors='ignore')
    
    # Convert 'datetime' column to pandas datetime
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')  # 'coerce' converts invalid dates to NaT
    return df

# Streamlit interface
def main():
    # Specify your Google Sheets sheet name
    sheet_name = 'YourSheetNameHere'  # Replace with your actual sheet name

    # Load data from Google Sheets
    df = load_data_from_sheets(sheet_name)

    # Process the data: Remove unwanted columns and convert datetime
    df = process_data(df)

    # Display the DataFrame in the Streamlit app
    st.write("Processed Data", df)

# Run the Streamlit app
if __name__ == "__main__":
    main()
