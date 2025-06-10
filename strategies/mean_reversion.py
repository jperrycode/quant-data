# File: strategies/mean_reversion.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from QuantLib import TARGET, Date as QLDate
from data.fetch_data import try_multiple_symbols
from utils.strategy_runner import run_strategy
from utils.logging_config import logger

__package__ = 'strategies'

def get_signals(price_series: pd.Series, window: int = 10, threshold: float = 1.0) -> pd.DataFrame:
    calendar = TARGET()
    valid_dates = [
        d for d in price_series.index
        if isinstance(d, (pd.Timestamp, datetime.datetime)) and 1901 <= d.year <= 2199
        and calendar.isBusinessDay(QLDate(d.day, d.month, d.year))
    ]
    price_series = price_series.loc[valid_dates]
    price_series = pd.to_numeric(price_series, errors='coerce')

    ma = price_series.rolling(window=window).mean()
    delta = price_series - ma

    def classify(value):
        if value > threshold:
            return "SELL"
        elif value < -threshold:
            return "BUY"
        return "HOLD"

    signals = delta.apply(lambda d: classify(d) if np.isscalar(d) else classify(d[0]))

    return pd.DataFrame({
        "price": price_series,
        "ma": ma,
        "signal": signals
    })

def plot_signals(df: pd.DataFrame, symbol: str):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['price'], label='Price')
    plt.plot(df.index, df['ma'], label='Moving Average')

    buy_signals = df[df['signal'] == 'BUY']
    sell_signals = df[df['signal'] == 'SELL']

    plt.scatter(buy_signals.index, buy_signals['price'], label='BUY', marker='^', color='green')
    plt.scatter(sell_signals.index, sell_signals['price'], label='SELL', marker='v', color='red')

    plt.title(f"Mean Reversion Signals for {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    run_strategy(
        strategy_name="Mean Reversion",
        signal_fn=get_signals,
        plot_fn=plot_signals,
        filename_suffix="mean_reversion",
        exchange_symbols={"NYSE": ["F"]},
        start_date="2024-01-01",
        end_date="2025-06-01",
        logger=logger
    )

if __name__ == "__main__":
    main()
