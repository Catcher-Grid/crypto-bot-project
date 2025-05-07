
import json
import os
from datetime import datetime, timezone

HISTORY_FILE = 'history.json'

def log_closed_trade(symbol, side, entry_price, exit_price, result):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    trade = {
        'symbol': symbol,
        'side': side,
        'entry_price': entry_price,
        'exit_price': exit_price,
        'result': result,
        'timestamp': now
    }
    history = load_history()
    history.append(trade)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def summarize_history():
    history = load_history()
    if not history:
        return "❌ Нет завершённых сделок."

    summary_lines = ["📉 История сделок:"]
    total = 0
    wins = 0
    losses = 0
    net = 0

    for h in history[-10:]:
        change = (float(h['exit_price']) - float(h['entry_price'])) / float(h['entry_price'])
        if h['side'] == 'short':
            change *= -1
        percent = change * 100
        net += percent
        total += 1
        if percent > 0:
            wins += 1
        else:
            losses += 1
        summary_lines.append(f"{h['symbol']} | {h['side'].upper()} @ {h['entry_price']} → {h['exit_price']} ({percent:.2f}%)")

    summary_lines.append("—")
    summary_lines.append(f"📊 Всего: {total} сделок")
    summary_lines.append(f"✔ Прибыльных: {wins}")
    summary_lines.append(f"✘ Убыточных: {losses}")
    summary_lines.append(f"🏁 Баланс: {net:.2f}%")

    return "\n".join(summary_lines)
