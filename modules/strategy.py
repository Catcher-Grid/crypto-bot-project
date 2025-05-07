from market_analysis import analyze_market
from telegram_utils import send_telegram_message
from dry_trader import open_position, check_position
from datetime import datetime, timezone
import os
import json

with open('config.json') as f:
    config = json.load(f)

tg_enabled = config['telegram']['enabled']
tg_token = config['telegram']['bot_token']
tg_chat_id = config['telegram']['chat_id']

def log_action(symbol, signal, action):
    log_folder = 'logs'
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, 'trade_log.txt')
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{now}] {symbol} | Сигнал: {signal.upper()} | Действие: {action}"
    with open(log_file, 'a') as f:
        f.write(line + "\n")
    print(f"[DEBUG] Лог добавлен: {line}")
    if tg_enabled:
        try:
            send_telegram_message(tg_token, tg_chat_id, line)
        except Exception as e:
            print(f"[DEBUG] Ошибка отправки в Telegram: {e}")

def execute_strategy(symbol='BTC_USDT'):
    signal, latest_price = analyze_market(symbol)

    result = check_position(symbol, latest_price)
    if result:
        log_action(symbol, 'exit', result)

    if signal == 'long':
        action = open_position(symbol, 'long', latest_price)
        log_action(symbol, signal, action)

    elif signal == 'short':
        action = open_position(symbol, 'short', latest_price)
        log_action(symbol, signal, action)

    elif signal == 'none':
        action = f"Нет торгового сигнала по {symbol}. Ждём..."
        log_action(symbol, signal, action)

    else:
        action = f"Ошибка или нет данных по {symbol}. Торговля пропущена."
        log_action(symbol, signal, action)