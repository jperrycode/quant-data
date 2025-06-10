# File: utils/logging_config.py

import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("quant")
logger.setLevel(logging.INFO)

log_path = "logs/strategy.log"
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
