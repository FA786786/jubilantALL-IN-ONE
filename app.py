import pandas as pd
import numpy as np
import ta

# === Load your data ===
# df = pd.read_csv("your_data.csv")  # Must contain datetime, open, high, low, close, volume
# Ensure datetime is parsed
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)

# === Generate 15-min OHLCV ===
df_15 = df.resample('15T').agg({
    'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
}).dropna()

# === Calculate ATR on 15-min ===
df_15['atr_15'] = ta.volatility.AverageTrueRange(
    high=df_15['high'], low=df_15['low'], close=df_15['close'], window=14).average_true_range()

# Merge 15-min data into original
for col in ['high', 'low', 'close', 'open', 'atr_15']:
    df[f'{col}_15'] = df_15[col].reindex(df.index, method='ffill')

# === Mother Candle Breakout ===
df['mother_body'] = (df['high_15'].shift(1) - df['low_15'].shift(1)) > df['atr_15'].shift(1)
df['inside_candle'] = (df['high_15'].shift(2) < df['high_15'].shift(1)) & (df['low_15'].shift(2) > df['low_15'].shift(1))
df['breakout'] = df['close_15'] > df['high_15'].shift(1)
df['mother_breakout'] = df['mother_body'] & df['inside_candle'] & df['breakout']

# === VWAP Calculation ===
df['cum_vol_price'] = (df['close'] * df['volume']).cumsum()
df['cum_vol'] = df['volume'].cumsum()
df['vwap'] = df['cum_vol_price'] / df['cum_vol']

# VWAP Reversal Logic
df['vwap_downtrend'] = (df['vwap'].shift(3) > df['vwap'].shift(2)) & (df['vwap'].shift(2) > df['vwap'].shift(1))
df['vwap_flat_or_up'] = df['vwap'].shift(1) <= df['vwap']
df['bullish_candle'] = df['close'] > df['open']
df['above_vwap'] = df['close'] > df['vwap']
df['vwap_reversal_up'] = df['vwap_downtrend'] & df['vwap_flat_or_up'] & df['bullish_candle'] & df['above_vwap']

df['vwap_uptrend'] = (df['vwap'].shift(3) < df['vwap'].shift(2)) & (df['vwap'].shift(2) < df['vwap'].shift(1))
df['vwap_flat_or_down'] = df['vwap'].shift(1) >= df['vwap']
df['bearish_candle'] = df['close'] < df['open']
df['below_vwap'] = df['close'] < df['vwap']
df['vwap_reversal_down'] = df['vwap_uptrend'] & df['vwap_flat_or_down'] & df['bearish_candle'] & df['below_vwap']

# === EQ + FUT Buy/Sell Logic ===
df['vol_avg'] = df['volume'].rolling(10).mean()
df['eq_buy_fut_buy'] = (df['close'] > df['open']) & (df['close'] > df['close'].shift(1)) & (df['volume'] > df['vol_avg']) & (df['open'] > df['open'].shift(1))
df['eq_sell_fut_sell'] = (df['close'] < df['open']) & (df['close'] < df['close'].shift(1)) & (df['volume'] > df['vol_avg']) & (df['open'] < df['open'].shift(1))

# === Entry Logic ===
df['long_entry'] = df['mother_breakout'] | df['vwap_reversal_up'] | df['eq_buy_fut_buy']
df['short_entry'] = df['vwap_reversal_down'] | df['eq_sell_fut_sell']

# === SL and Target ===
df['lowestLow'] = df['low'].rolling(5).min()
df['highestHigh'] = df['high'].rolling(5).max()
df['longTGT'] = df['close'] + (df['close'] - df['lowestLow']) * 1.5
df['shortTGT'] = df['close'] - (df['highestHigh'] - df['close']) * 1.5

# === Exit Logic ===
df['long_exit'] = df['low'] <= df['lowestLow']
df['short_exit'] = df['high'] >= df['highestHigh']

# === Final Trade Signals with SL/TGT ===
df['signal'] = np.select(
    [df['long_entry'], df['short_entry'], df['long_exit'], df['short_exit']],
    ['BUY', 'SELL', 'EXIT_LONG', 'EXIT_SHORT'],
    default=''
)

# === Optional: Export or Display ===
df_signals = df[df['signal'] != ''][['open', 'high', 'low', 'close', 'volume', 'signal', 'longTGT', 'shortTGT', 'lowestLow', 'highestHigh']]
print(df_signals.tail(20))
