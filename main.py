from modules.beta_ranker import analyze_priorities

print("[MAIN] Анализ приоритетов по β...")
analyze_priorities()

from strategy import execute_strategy
import json
import time

with open('config.json') as f:
    config = json.load(f)

symbols = config.get("symbols", ["BTC_USDT"])
interval_sec = 300

def main_loop():
    print("[MAIN] Запуск ИИ-бота с мульти-мониторингом пар:", symbols)
    while True:
        for symbol in symbols:
            print(f"\n[MAIN] Анализ пары: {symbol}")
            execute_strategy(symbol)
            print("-" * 40)
        print(f"[MAIN] Пауза {interval_sec} секунд перед следующим циклом...\n")
        time.sleep(interval_sec)

if __name__ == '__main__':
    main_loop()