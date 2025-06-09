# File: strategies/momentum_strategy.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from QuantLib import TARGET, Date as QLDate
from data.fetch_data import try_multiple_symbols
import logging

__package__ = 'strategies'

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/momentum.log",
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("momentum")

def get_momentum_signals(price_series: pd.Series, window: int = 10, upper: float = 0.02, lower: float = -0.02) -> pd.DataFrame:
    calendar = TARGET()
    valid_dates = [
        d for d in price_series.index
        if isinstance(d, (pd.Timestamp, datetime.datetime)) and 1901 <= d.year <= 2199
        and calendar.isBusinessDay(QLDate(d.day, d.month, d.year))
    ]
    price_series = price_series.loc[valid_dates]
    price_series = pd.to_numeric(price_series, errors='coerce')

    roc = price_series.pct_change(periods=window)

    def classify(roc_val):
        if roc_val > upper:
            return "BUY"
        elif roc_val < lower:
            return "SELL"
        return "HOLD"

    signals = roc.apply(classify)

    return pd.DataFrame({
        "price": price_series,
        "roc": roc,
        "signal": signals
    })

def plot_signals(df: pd.DataFrame, symbol: str):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['price'], label='Price')

    buy_signals = df[df['signal'] == 'BUY']
    sell_signals = df[df['signal'] == 'SELL']

    plt.scatter(buy_signals.index, buy_signals['price'], label='BUY', marker='^', color='green')
    plt.scatter(sell_signals.index, sell_signals['price'], label='SELL', marker='v', color='red')

    plt.title(f"Momentum Strategy (ROC) Signals for {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 3))
    plt.plot(df.index, df['roc'], label='Rate of Change')
    plt.axhline(y=0.02, color='green', linestyle='--', linewidth=1)
    plt.axhline(y=-0.02, color='red', linestyle='--', linewidth=1)
    plt.title("Rate of Change")
    plt.xlabel("Date")
    plt.ylabel("ROC")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    exchange_symbols = {
        "NYSE": ["F"]
    }
    start_date = "2024-01-01"
    end_date = "2025-06-01"

    for exchange, sym_list in exchange_symbols.items():
        logger.info(f"Trying symbols for {exchange}...")
        chosen_symbol, series = try_multiple_symbols(sym_list, start_date, end_date)
        if series is not None:
            signal_df = get_momentum_signals(series)
            logger.info(f"\n{signal_df.tail()}")

            os.makedirs("signals", exist_ok=True)
            signal_df.to_json(f"signals/{chosen_symbol}_momentum.json", orient="records", lines=True)

            plot_signals(signal_df, chosen_symbol)
