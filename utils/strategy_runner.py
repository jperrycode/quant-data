# File: utils/strategy_runner.py

import os
from data.fetch_data import try_multiple_symbols

def run_strategy(strategy_name, signal_fn, plot_fn, filename_suffix, exchange_symbols, start_date, end_date, logger):
    os.makedirs("signals", exist_ok=True)

    for exchange, symbols in exchange_symbols.items():
        logger.info(f"[{strategy_name}] Trying symbols for {exchange}...")
        symbol, series = try_multiple_symbols(symbols, start_date, end_date)
        if series is not None:
            signal_df = signal_fn(series)

            json_path = f"signals/{symbol}_{filename_suffix}.json"
            signal_df.to_json(json_path, orient="records", lines=True)
            logger.info(f"[{strategy_name}] Saved signals to {json_path}")

            signal_counts = signal_df['signal'].value_counts().to_dict()
            logger.info(f"[{strategy_name}] Signal distribution: {signal_counts}")

            plot_fn(signal_df, symbol)
