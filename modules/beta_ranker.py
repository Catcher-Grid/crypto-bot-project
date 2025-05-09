import pandas as pd
from modules.beta_analysis import calculate_beta
from modules.telegram_utils import send_telegram_message
from datetime import datetime

# Пары, которые будем анализировать
TRADING_PAIRS = ["BTC_USDT", "ETH_USDT", "SOL_USDT", "TRUMP_USDT"]

def fetch_market_data(pair: str, limit: int = 100):
    try:
        df = pd.read_csv(f"data/{pair}.csv")
        return df.tail(limit)
    except Exception as e:
        print(f"[BETA] Ошибка загрузки данных {pair}: {e}")
        return pd.DataFrame()

def analyze_priorities():
    print("[BETA] Старт анализа приоритетов по β")
    btc_data = fetch_market_data("BTC_USDT")
    if btc_data.empty:
        print("[BETA] Нет данных по BTC.")
        return

    market_return = btc_data["close"].pct_change().dropna()
    market_trend = market_return.sum()
    trend_str = "восходящий 📈" if market_trend > 0 else "нисходящий 📉"

    message = f"📊 Приоритет альтов по β (BTC тренд: {trend_str})\n\n"
    betas = {}

    for pair in TRADING_PAIRS:
        if pair == "BTC_USDT":
            continue
        df = fetch_market_data(pair)
        if df.empty:
            continue
        asset_return = df["close"].pct_change().dropna()
        beta = calculate_beta(asset_return, market_return)
        betas[pair] = round(beta, 2)

    sorted_pairs = sorted(betas.items(), key=lambda x: -x[1])
    for pair, beta in sorted_pairs:
        message += f"{pair}: β = {beta}\n"

    send_telegram_message(message)
    print("[BETA] Отчёт отправлен в Telegram.")

if __name__ == "__main__":
    analyze_priorities()