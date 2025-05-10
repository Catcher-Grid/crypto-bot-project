import requests
import pandas as pd
import os
from datetime import datetime

BINANCE_URL = "https://api.binance.com/api/v3/klines"

def fetch_ohlcv(symbol: str, interval="1h", limit=100):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    try:
        res = requests.get(BINANCE_URL, params=params)
        res.raise_for_status()
        data = res.json()

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])

        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

        return df
    except Exception as e:
        print(f"[API] Ошибка при получении данных для {symbol}: {e}")
        return pd.DataFrame()

def save_csv(pair: str, df: pd.DataFrame):
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", f"{pair}.csv")
    df.to_csv(file_path, index=False)
    print(f"[API] Сохранено: {file_path}")

def update_all():
    mapping = {
        "BTC_USDT": "BTCUSDT",
        "ETH_USDT": "ETHUSDT",
        "SOL_USDT": "SOLUSDT",
        "TRUMP_USDT": "TRUMPUSDT"
    }
    for pair, binance_symbol in mapping.items():
        print(f"[API] Загрузка данных для {pair}...")
        df = fetch_ohlcv(binance_symbol)
        if not df.empty:
            save_csv(pair, df)

if __name__ == "__main__":
    update_all()