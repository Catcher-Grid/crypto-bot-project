
import requests
import json
import time
import os
from trade_history import summarize_history

CONFIG_PATH = 'config.json'
POSITIONS_PATH = 'positions.json'

with open(CONFIG_PATH) as f:
    config = json.load(f)

TOKEN = config['telegram']['bot_token']
CHAT_ID = str(config['telegram']['chat_id'])
API_URL = f'https://api.telegram.org/bot{TOKEN}/'
TP_FILE = 'tp_sl_config.json'

DEFAULT_TP = 0.02
DEFAULT_SL = -0.03

def load_positions():
    if os.path.exists(POSITIONS_PATH):
        with open(POSITIONS_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_positions(data):
    with open(POSITIONS_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def send_message(text):
    try:
        payload = {'chat_id': CHAT_ID, 'text': text}
        requests.post(API_URL + 'sendMessage', data=payload)
    except Exception as e:
        print(f"[TELEGRAM] Ошибка отправки команды: {e}")

def load_tp_sl():
    if os.path.exists(TP_FILE):
        with open(TP_FILE) as f:
            return json.load(f)
    return {'tp': DEFAULT_TP, 'sl': DEFAULT_SL}

def save_tp_sl(tp, sl):
    with open(TP_FILE, 'w') as f:
        json.dump({'tp': tp, 'sl': sl}, f)

def handle_command(cmd):
    cmd = cmd.strip().lower()

    if cmd == '/status':
        pos = load_positions()
        if pos:
            lines = ['📊 Открытые позиции:']
            for symbol, data in pos.items():
                lines.append(f"{symbol} | {data['side']} @ {data['entry_price']}")
            send_message('\n'.join(lines))
        else:
            send_message("Нет открытых позиций.")

    elif cmd == '/summary':
        summary = summarize_history()
        send_message(summary)

    elif cmd == '/reset':
        save_positions({})
        send_message("✅ Все позиции сброшены (dry-run).")

    elif cmd.startswith('/set_tp'):
        try:
            new_tp = float(cmd.split()[1]) / 100
            data = load_tp_sl()
            save_tp_sl(new_tp, data['sl'])
            send_message(f"✅ TP обновлён до {new_tp*100:.2f}%")
        except:
            send_message("Ошибка: используйте /set_tp 2.5")

    elif cmd.startswith('/set_sl'):
        try:
            new_sl = float(cmd.split()[1]) / 100
            data = load_tp_sl()
            save_tp_sl(data['tp'], new_sl)
            send_message(f"✅ SL обновлён до {new_sl*100:.2f}%")
        except:
            send_message("Ошибка: используйте /set_sl -3.0")

    else:
        send_message("⚠ Неизвестная команда.")

def listen_for_commands():
    offset = None
    print("[COMMANDS] Telegram команда-бот запущен.")
    while True:
        try:
            resp = requests.get(API_URL + 'getUpdates', params={'timeout': 30, 'offset': offset})
            result = resp.json().get('result', [])
            for update in result:
                offset = update['update_id'] + 1
                if 'message' in update and 'text' in update['message']:
                    msg = update['message']
                    if str(msg['chat']['id']) == CHAT_ID:
                        print(f"[COMMAND] Получено: {msg['text']}")
                        handle_command(msg['text'])
        except Exception as e:
            print(f"[COMMANDS] Ошибка: {e}")
        time.sleep(2)

if __name__ == '__main__':
    listen_for_commands()
