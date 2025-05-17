# لیست ارزهای دیجیتال برای بررسی
CRYPTOCURRENCIES = [
    "BTC-USDT", "ETH-USDT", "BNB-USDT", "SOL-USDT", "XRP-USDT",
    "ADA-USDT", "DOGE-USDT", "SHIB-USDT", "DOT-USDT", "MATIC-USDT",
    "LTC-USDT", "AVAX-USDT", "LINK-USDT", "UNI-USDT", "ATOM-USDT",
]

# تنظیمات استراتژی اسکالپینگ
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
    'volume_change_threshold': 1.5,  # تغییر حجم 50٪
    'profit_target_percent': 1.5,    # هدف سود 1.5٪
    'stop_loss_percent': 0.7,        # حد ضرر 0.7٪
}

# تنظیمات API کوکوین
KUCOIN_BASE_URL = "https://api.kucoin.com"
KUCOIN_KLINE_ENDPOINT = "/api/v1/market/candles"
KUCOIN_TICKER_ENDPOINT = "/api/v1/market/orderbook/level1"

# تایم فریم و تعداد کندل‌ها
TIMEFRAME = "30min"  # تایم فریم 30 دقیقه در کوکوین
KLINE_SIZE = 100   # تعداد کندل‌ها
SIGNALS_FILE = "data/signals.json"
