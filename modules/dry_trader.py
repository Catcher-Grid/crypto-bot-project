import json
from modules.trade_history import log_closed_trade

POSITIONS_FILE = "positions.json"
TP_SL_FILE = "tp_sl_config.json"

def reset_positions():
    with open(POSITIONS_FILE, "w") as f:
        json.dump([], f)
    print("[DRY] Позиции сброшены.")

def update_tp_sl(key, value):
    try:
        with open(TP_SL_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"tp": 2.0, "sl": -3.0}

    data[key] = value

    with open(TP_SL_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[CONFIG] {key.upper()} обновлён до {value}%")

def get_tp_sl_config():
    try:
        with open(TP_SL_FILE) as f:
            return json.load(f)
    except:
        return {"tp": 2.0, "sl": -3.0}