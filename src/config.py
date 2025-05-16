# لیست ارزهای دیجیتالی که می‌خواهیم بررسی کنیم (با IDهای CoinGecko)
CRYPTOCURRENCIES = [
    {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
    {"id": "ethereum", "symbol": "eth", "name": "Ethereum"},
    {"id": "binancecoin", "symbol": "bnb", "name": "BNB"},
    {"id": "solana", "symbol": "sol", "name": "Solana"},
    {"id": "ripple", "symbol": "xrp", "name": "XRP"},
    {"id": "cardano", "symbol": "ada", "name": "Cardano"},
    {"id": "dogecoin", "symbol": "doge", "name": "Dogecoin"},
    {"id": "shiba-inu", "symbol": "shib", "name": "Shiba Inu"},
    {"id": "polkadot", "symbol": "dot", "name": "Polkadot"},
    {"id": "matic-network", "symbol": "matic", "name": "Polygon"},
]

# تنظیمات استراتژی
SCALPING_SETTINGS = {
    'rsi_period': 14,
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    'ema_short': 9,
    'ema_medium': 21,
    'ema_long': 50,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bb_period': 20,
    'bb_std': 2,
    'volume_change_threshold': 1.5,
    'profit_target_percent': 1.5,
    'stop_loss_percent': 0.7,
}

# تنظیمات API CoinGecko
BASE_URL = "https://api.coingecko.com/api/v3"
OHLC_ENDPOINT = "/coins/{id}/ohlc"
TICKER_ENDPOINT = "/simple/price"

# تنظیمات تایم فریم (بر حسب روز)
TIMEFRAME_DAYS = 1  # داده‌های روزانه
DATA_POINTS = 100   # تعداد نقاط داده

# مسیر فایل‌های داده
SIGNALS_FILE = "data/signals.json"
