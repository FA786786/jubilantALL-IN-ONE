from backtesting import Strategy
import pandas as pd
import numpy as np
import ta

class OneInAllStrategy(Strategy):
    def init(self):
        close = pd.Series(self.data.Close)
        high = pd.Series(self.data.High)
        low = pd.Series(self.data.Low)
        open_ = pd.Series(self.data.Open)
        volume = pd.Series(self.data.Volume)

        # Calculate ATR
        self.atr = ta.volatility.AverageTrueRange(high, low, close, window=14).average_true_range()

        # Calculate VWAP
        typical_price = (high + low + close) / 3
        self.vwap = (typical_price * volume).cumsum() / volume.cumsum()

        # Calculate volume average
        self.vol_avg = volume.rolling(window=10).mean()

        # Store for use in next()
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def next(self):
        i = len(self.data.Close) - 1

        # Mother Candle Breakout
        mother_body = (self.high[i-1] - self.low[i-1]) > self.atr[i-1]
        inside_candle = self.high[i-2] < self.high[i-1] and self.low[i-2] > self.low[i-1]
        breakout = self.close[i] > self.high[i-1]
        mother_breakout = mother_body and inside_candle and breakout

        # VWAP Reversal Logic
        vwap_downtrend = self.vwap[i-3] > self.vwap[i-2] > self.vwap[i-1]
        vwap_flat_or_up = self.vwap[i-1] <= self.vwap[i]
        bullish_candle = self.close[i] > self.open[i]
        above_vwap = self.close[i] > self.vwap[i]
        vwap_reversal_up = vwap_downtrend and vwap_flat_or_up and bullish_candle and above_vwap

        vwap_uptrend = self.vwap[i-3] < self.vwap[i-2] < self.vwap[i-1]
        vwap_flat_or_down = self.vwap[i-1] >= self.vwap[i]
        bearish_candle = self.close[i] < self.open[i]
        below_vwap = self.close[i] < self.vwap[i]
        vwap_reversal_down = vwap_uptrend and vwap_flat_or_down and bearish_candle and below_vwap

        # EQ + FUT Buy/Sell
        eq_buy_fut_buy = (self.close[i] > self.open[i] and
                          self.close[i] > self.close[i-1] and
                          self.volume[i] > self.vol_avg[i] and
                          self.open[i] > self.open[i-1])

        eq_sell_fut_sell = (self.close[i] < self.open[i] and
                            self.close[i] < self.close[i-1] and
                            self.volume[i] > self.vol_avg[i] and
                            self.open[i] < self.open[i-1])

        # Entry Signals
        long_entry = mother_breakout or vwap_reversal_up or eq_buy_fut_buy
        short_entry = vwap_reversal_down or eq_sell_fut_sell

        # SL & Target Calculation
        lowest_low = min(self.low[i-4:i+1])
        highest_high = max(self.high[i-4:i+1])
        long_tgt = self.close[i] + (self.close[i] - lowest_low) * 1.5
        short_tgt = self.close[i] - (highest_high - self.close[i]) * 1.5

        # Entry Conditions
        if long_entry:
            self.buy(sl=lowest_low, tp=long_tgt)
        elif short_entry:
            self.sell(sl=highest_high, tp=short_tgt)
