import streamlit as st
import pandas as pd

st.title("Datetime Column Processor")

# --- Load Data (Replace with your actual data source) ---
# Example: from CSV
try:
    df = pd.read_csv("your_data.csv")  # Change this to your actual data source
    st.success("Data loaded successfully.")
except FileNotFoundError:
    st.error("Data file not found.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- Show Available Columns ---
st.write("Available columns:", df.columns.tolist())
st.write(df.head())

# --- Rename common alternatives to 'datetime' ---
datetime_candidates = ['timestamp', 'date', 'time']
for alt in datetime_candidates:
    if alt in df.columns and 'datetime' not in df.columns:
        df.rename(columns={alt: 'datetime'}, inplace=True)
        st.info(f"Renamed column '{alt}' to 'datetime'.")

# --- Convert 'datetime' column to datetime format ---
if 'datetime' in df.columns:
    try:
        df['datetime'] = pd.to_datetime(df['datetime'])
        st.success("Datetime column parsed successfully.")
        st.write(df.head())
    except Exception as e:
        st.error(f"Error parsing datetime: {e}")
else:
    st.error("'datetime' column not found in the dataset.")

