import requests
import pandas as pd

def fetch_ohlcv(symbol='BTC_USDT', interval='15m', limit=500):
    url = f'https://api.gateio.ws/api/v4/futures/usdt/candlesticks?contract={symbol}&interval={interval}&limit={limit}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        raw = response.json()
        parsed = [{
            'timestamp': int(r[0]),
            'open': float(r[5]),
            'high': float(r[3]),
            'low': float(r[4]),
            'close': float(r[2]),
            'volume': float(r[1])
        } for r in raw]
        return pd.DataFrame(parsed)
    except Exception as e:
        print(f"[ERROR] Ошибка при получении OHLCV: {e}")
        return None

def calculate_indicators(df, rsi_period=14, ema_fast=9, ema_slow=21):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(rsi_period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['EMA_FAST'] = df['close'].ewm(span=ema_fast, adjust=False).mean()
    df['EMA_SLOW'] = df['close'].ewm(span=ema_slow, adjust=False).mean()
    return df

def generate_signal(df):
    df = df.dropna()
    if df.empty:
        return 'none'
    latest = df.iloc[-1]
    if latest['RSI'] < 30 and latest['EMA_FAST'] > latest['EMA_SLOW']:
        return 'long'
    elif latest['RSI'] > 70 and latest['EMA_FAST'] < latest['EMA_SLOW']:
        return 'short'
    else:
        return 'none'

def analyze_market(symbol='BTC_USDT'):
    df = fetch_ohlcv(symbol)
    if df is not None:
        df = calculate_indicators(df)
        signal = generate_signal(df)
        if not df.dropna().empty:
            latest = df.dropna().iloc[-1]
            print(f"[ANALYSIS] {symbol}: RSI={latest['RSI']:.2f}, EMA_FAST={latest['EMA_FAST']:.2f}, EMA_SLOW={latest['EMA_SLOW']:.2f}")
            return signal, latest['close']
        else:
            print(f"[ANALYSIS] {symbol}: недостаточно данных.")
            return 'none', None
    else:
        return 'error', None