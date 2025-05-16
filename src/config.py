# لیست ارزهای دیجیتال برای بررسی
CRYPTOCURRENCIES = [
    "bitcoin", "ethereum", "binancecoin", "solana", "ripple",
    "cardano", "dogecoin", "shiba-inu", "polkadot", "matic-network",
    "litecoin", "avalanche-2", "chainlink", "uniswap", "cosmos"
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
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
COINGECKO_MARKET_CHART_ENDPOINT = "/coins/{id}/market_chart"
COINGECKO_PRICE_ENDPOINT = "/simple/price"

# تایم فریم و تعداد کندل‌ها
TIMEFRAME_IN_DAYS = 1  # تعداد روزها برای دریافت داده‌های کندل (1 روز = 24 ساعت)
SIGNALS_FILE = "data/signals.json"
