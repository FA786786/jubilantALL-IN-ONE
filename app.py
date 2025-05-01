import streamlit as st
import yfinance as yf
import pandas as pd
from backtesting import Backtest
from strategy import OneInAllStrategy
import plotly.graph_objs as go
from gsheet import log_trade_to_sheets
from zerodha import place_order

# --- Streamlit UI ---
st.title("📊 One-in-All Trade System: Entry, SL, TGT, Exit")

symbol = st.text_input("Enter stock symbol (e.g., RELIANCE.NS):", "RELIANCE.NS")
start_date = st.date_input("Start date:", pd.to_datetime("2024-01-01"))
end_date = st.date_input("End date:", pd.to_datetime("today"))

if st.button("Run Backtest"):
    # Download data from Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date, interval="5m")
    data.dropna(inplace=True)

    # --- Check and Convert datetime column ---
    if 'Datetime' not in data.columns:
        st.error("The data does not contain a 'Datetime' column")
    else:
        # Ensure the 'Datetime' column exists and is properly converted
        try:
            data['Datetime'] = pd.to_datetime(data['Datetime'], errors='coerce')
            # Handle any NaT (invalid) values in the 'Datetime' column
            if data['Datetime'].isna().sum() > 0:
                st.warning(f"Found {data['Datetime'].isna().sum()} invalid 'Datetime' values.")
                data = data.dropna(subset=['Datetime'])
            st.success("Datetime conversion successful")
        except Exception as e:
            st.error(f"Error converting 'Datetime' column: {e}")
    
    # Perform backtesting with the strategy
    bt = Backtest(data, OneInAllStrategy, cash=100000, commission=0.002)
    stats = bt.run()
    
    # Display Backtest Results
    st.subheader("Backtest Results")
    st.write(stats)

    # Plot the Equity Curve using Plotly
    st.subheader("Equity Curve")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stats['_equity_curve'].index, y=stats['_equity_curve']['Equity'], mode='lines', name='Equity'))
    st.plotly_chart(fig)

    # Triggering Alerts, Logging Trades to Google Sheets, and Placing Orders
    if stats["Buy"] > 0:
        st.write("🚨 Buy Signal Triggered!")
        log_trade_to_sheets(symbol, 'BUY', "1000", "1100", pd.to_datetime('today').strftime('%Y-%m-%d'))
        place_order(symbol, 'BUY', 1)

    if stats["Sell"] > 0:
        st.write("🚨 Sell Signal Triggered!")
        log_trade_to_sheets(symbol, 'SELL', "1000", "900", pd.to_datetime('today').strftime('%Y-%m-%d'))
        place_order(symbol, 'SELL', 1)
