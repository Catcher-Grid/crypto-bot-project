import json
import os

HISTORY_FILE = "history.json"

def get_trade_summary():
    if not os.path.exists(HISTORY_FILE):
        return "⚠️ История сделок не найдена."

    with open(HISTORY_FILE) as f:
        trades = json.load(f)

    if not trades:
        return "📭 Сделки отсутствуют."

    total_profit = 0
    count_win = 0
    count_loss = 0

    for trade in trades:
        pnl = trade.get("pnl", 0)
        total_profit += pnl
        if pnl > 0:
            count_win += 1
        else:
            count_loss += 1

    return (
        f"📈 Сводка по сделкам (dry-run):\n"
        f"• Всего: {len(trades)}\n"
        f"• Прибыльных: {count_win}\n"
        f"• Убыточных: {count_loss}\n"
        f"• Итого PnL: {round(total_profit, 2)} USDT"
    )

if __name__ == "__main__":
    print(get_trade_summary())

def log_closed_trade(trade: dict):
    from datetime import datetime

    trade['timestamp'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []

        history.append(trade)

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Не удалось записать сделку в историю: {e}")