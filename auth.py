import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def get_google_sheet(sheet_url, json_key):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(json_key, scopes=scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df
