import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    handler = logging.FileHandler(os.path.join(LOG_DIR, log_file), encoding="utf-8")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Примеры:
# strategy_logger = setup_logger("strategy", "strategy.log")
# strategy_logger.info("Запуск стратегии...")