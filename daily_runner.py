# File: daily_runner.py

from strategies.momentum_strategy import main as run_daily_momentum
from strategies.mean_reversion import main as run_daily_mean_reversion
from ml.train_predictor import main as run_model

if __name__ == "__main__":
    run_daily_momentum()
    run_daily_mean_reversion()
    run_model()
