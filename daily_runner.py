# File: daily_runner.py

from strategies.mean_reversion import get_signals as get_mean_reversion_signals, plot_signals as plot_mean_reversion_signals
from data.fetch_data import try_multiple_symbols
from strategies.momentum_strategy import get_momentum_signals, plot_signals as plot_momentum_signals

start_date = "2024-01-01"
end_date = "2025-06-01"
exchange_symbols = {
    "NYSE": ["F"]
}

def run_daily_momentum():
    for exchange, sym_list in exchange_symbols.items():
        print(f"\n[Momentum] Trying symbols for {exchange}...")
        chosen_symbol, series = try_multiple_symbols(sym_list, start_date, end_date)
        if series is not None:
            signal_df = get_momentum_signals(series)
            print(signal_df.tail())
            plot_momentum_signals(signal_df, chosen_symbol)

def run_daily_mean_reversion():
    for exchange, sym_list in exchange_symbols.items():
        print(f"\n[Mean Reversion] Trying symbols for {exchange}...")
        chosen_symbol, series = try_multiple_symbols(sym_list, start_date, end_date)
        if series is not None:
            signal_df = get_mean_reversion_signals(series)
            print(signal_df.tail())
            plot_mean_reversion_signals(signal_df, chosen_symbol)

if __name__ == "__main__":
    run_daily_momentum()
    run_daily_mean_reversion()

