# File: data/fetch_data_real.py

import yfinance as yf
import pandas as pd
import os
import time
from datetime import datetime

def log_error(message: str):
    with open("data/log.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")

def get_price_series(symbol: str, start: str, end: str, cache: bool = True, retries: int = 3) -> pd.Series:
    os.makedirs("data", exist_ok=True)
    cache_file = f"data/cache_{symbol}_{start}_{end}.csv"

    if cache and os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file, index_col=0, parse_dates=[0], date_format="%Y-%m-%d", dayfirst=False)
            df = df[~df.index.astype(str).str.contains("Ticker", na=False)]
        except Exception as e:
            os.remove(cache_file)
            raise RuntimeError(f"Corrupt cache removed: {cache_file}, reason: {e}")
    else:
        for attempt in range(retries):
            try:
                df = yf.download(symbol, start=start, end=end, auto_adjust=False)
                print(f"Downloaded columns for {symbol}: {list(df.columns)}")
                if 'Close' in df.columns and not df['Close'].empty:
                    df = df[['Close']].astype(float).squeeze()
                    df.index.name = "Date"
                    df.to_csv(cache_file, date_format="%Y-%m-%d")
                    break
                else:
                    raise ValueError(f"No usable 'Close' column found. Columns: {df.columns}")
            except Exception as e:
                error_msg = f"Attempt {attempt+1}/{retries} failed for {symbol}: {e}"
                print(error_msg)
                log_error(error_msg)
                time.sleep(1)
        else:
            final_msg = f"Failed to fetch {symbol} after {retries} retries."
            log_error(final_msg)
            raise RuntimeError(final_msg)

    series = df['Close'].copy()
    series.index = pd.to_datetime(series.index, format="%Y-%m-%d", errors="coerce")
    series.index = series.index.tz_localize("UTC").tz_convert("America/New_York").normalize()
    return series

def try_multiple_symbols(symbols, start_date, end_date):
    for symbol in symbols:
        try:
            prices = get_price_series(symbol, start_date, end_date)
            if prices is not None and not prices.empty:
                print(f"\n{symbol} price sample:")
                print(prices.head())
                return symbol, prices
        except Exception as e:
            print(f"Failed to fetch {symbol}: {e}")
    print("No valid data found for any symbols.")
    return None, None
