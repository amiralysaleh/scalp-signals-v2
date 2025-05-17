# لیست ارزهای دیجیتال برای بررسی
CRYPTOCURRENCIES = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "SHIBUSDT", "DOTUSDT", "MATICUSDT",
    "LTCUSDT", "AVAXUSDT", "LINKUSDT", "UNIUSDT", "ATOMUSDT",
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

# تنظیمات API
BINANCE_BASE_URL = "https://api.binance.com"
BINANCE_KLINE_ENDPOINT = "/api/v3/klines"
BINANCE_TICKER_ENDPOINT = "/api/v3/ticker/price"

# تایم فریم و تعداد کندل‌ها
TIMEFRAME = "30m"  # تایم فریم 30 دقیقه
KLINE_SIZE = 100   # تعداد کندل‌ها
SIGNALS_FILE = "data/signals.json"
