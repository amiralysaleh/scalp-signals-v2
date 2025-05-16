# لیست ارزهای دیجیتالی که می‌خواهیم بررسی کنیم
CRYPTOCURRENCIES = [
    "btcusdt", "ethusdt", "bnbusdt", "solusdt", "xrpusdt",
    "adausdt", "dogeusdt", "shibusdt", "dotusdt", "maticusdt",
    "ltcusdt", "avaxusdt", "linkusdt", "uniusdt", "atomusdt",
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
    'volume_change_threshold': 1.5,  # افزایش 50٪ در حجم
    'profit_target_percent': 1.5,    # هدف سود 1.5٪
    'stop_loss_percent': 0.7,        # استاپ لاس 0.7٪
}

# تنظیمات API
BASE_URL = "https://api.lbank.info/v2"
KLINE_ENDPOINT = "/kline.do"
TICKER_ENDPOINT = "/ticker.do"

# تنظیمات تایم فریم
TIMEFRAME = "30min"  # تایم فریم 30 دقیقه‌ای
KLINE_SIZE = 100     # تعداد کندل‌ها برای دریافت

# مسیر فایل‌های داده
SIGNALS_FILE = "data/signals.json"
