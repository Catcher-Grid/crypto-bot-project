import requests

def send_telegram_message(token, chat_id, message):
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code != 200:
            print(f"[TELEGRAM] Ошибка: {response.text}")
        else:
            print("[TELEGRAM] Уведомление отправлено.")
    except Exception as e:
        print(f"[TELEGRAM] Ошибка при отправке: {e}")