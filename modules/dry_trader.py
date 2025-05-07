
import json
import os
from datetime import datetime, timezone
from trade_history import log_closed_trade

TP_FILE = 'tp_sl_config.json'
POSITIONS_FILE = 'positions.json'

def load_tp_sl():
    if os.path.exists(TP_FILE):
        with open(TP_FILE, 'r') as f:
            return json.load(f)
    return {'tp': 0.02, 'sl': -0.03}

def load_positions():
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_positions(positions):
    with open(POSITIONS_FILE, 'w') as f:
        json.dump(positions, f, indent=2)

def open_position(symbol, side, price):
    positions = load_positions()
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    positions[symbol] = {
        'side': side,
        'entry_price': price,
        'timestamp': now
    }
    save_positions(positions)
    return f"[DRY] Открыта позиция {side.upper()} по {symbol} @ {price:.2f}"

def check_position(symbol, current_price):
    positions = load_positions()
    if symbol not in positions:
        return None

    pos = positions[symbol]
    side = pos['side']
    entry = pos['entry_price']
    result = None
    tp_sl = load_tp_sl()
    TP_PERCENT = tp_sl['tp']
    SL_PERCENT = tp_sl['sl']

    if side == 'long':
        change = (current_price - entry) / entry
    elif side == 'short':
        change = (entry - current_price) / entry
    else:
        return None

    if change >= TP_PERCENT:
        result = f"TP достигнут по {symbol} ({side}) → +{change*100:.2f}%"
    elif change <= SL_PERCENT:
        result = f"SL сработал по {symbol} ({side}) → {change*100:.2f}%"

    if result:
        log_closed_trade(symbol, side, entry, current_price, result)
        del positions[symbol]
        save_positions(positions)
        return result
    return None
