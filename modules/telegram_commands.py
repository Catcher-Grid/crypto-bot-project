import json
import time
from modules.telegram_utils import send_telegram_message
from modules.trade_history import get_trade_summary
from modules.dry_trader import reset_positions, update_tp_sl
from modules.telegram_plan import handle_todo_command

CONFIG_PATH = "config.json"
TP_SL_CONFIG_PATH = "tp_sl_config.json"
POSITIONS_PATH = "positions.json"

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def handle_status():
    try:
        with open(POSITIONS_PATH) as f:
            positions = json.load(f)
        if not positions:
            send_telegram_message("🚫 Нет открытых позиций.")
        else:
            message = "📊 *Открытые позиции:*
"
            for pos in positions:
                message += f"{pos['symbol']} — {pos['side']} по {pos['entry_price']} USDT
"
            send_telegram_message(message, parse_mode="Markdown")
    except Exception as e:
        send_telegram_message(f"[Ошибка] Невозможно получить позиции: {e}")

def handle_summary():
    try:
        summary = get_trade_summary()
        send_telegram_message(summary)
    except Exception as e:
        send_telegram_message(f"[Ошибка] Невозможно получить сводку: {e}")

def handle_reset():
    reset_positions()
    send_telegram_message("♻️ Все позиции сброшены (dry-run).")

def handle_tp_sl(text):
    parts = text.split()
    if len(parts) != 2:
        send_telegram_message("⚠️ Используй: /set_tp 2.5 или /set_sl -3.0")
        return
    try:
        value = float(parts[1])
        if "/set_tp" in text:
            update_tp_sl("tp", value)
            send_telegram_message(f"✅ TP обновлён: {value}%")
        elif "/set_sl" in text:
            update_tp_sl("sl", value)
            send_telegram_message(f"✅ SL обновлён: {value}%")
    except ValueError:
        send_telegram_message("⚠️ Неверный формат числа.")

def handle_command(text):
    if text == "/status":
        handle_status()
    elif text == "/summary":
        handle_summary()
    elif text == "/reset":
        handle_reset()
    elif text.startswith("/set_tp") or text.startswith("/set_sl"):
        handle_tp_sl(text)
    elif text == "/todo":
        handle_todo_command()
    else:
        send_telegram_message("🤖 Неизвестная команда.")