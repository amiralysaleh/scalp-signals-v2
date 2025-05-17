# لیست ارزهای دیجیتال برای بررسی - نمادهای سازگار با KuCoin
CRYPTOCURRENCIES = [
    "BTC-USDT", "ETH-USDT", "BNB-USDT", "SOL-USDT", "XRP-USDT",
    "ADA-USDT", "DOGE-USDT", "SHIB-USDT", "DOT-USDT", 
    "LTC-USDT", "AVAX-USDT", "LINK-USDT", "UNI-USDT", "ATOM-USDT",
    "XMR-USDT", "TRX-USDT", "NEAR-USDT", "MATIC-USDT", "ALGO-USDT",
    "FTM-USDT", "SUI-USDT", "INJ-USDT", "AAVE-USDT", "TON-USDT",
    "BCH-USDT", "ZEC-USDT", "ICP-USDT", "VET-USDT", "QNT-USDT",
    "DYDX-USDT", "FIL-USDT", "EGLD-USDT", "HBAR-USDT", "GRT-USDT",
    "AXS-USDT", "SAND-USDT", "MANA-USDT", "1INCH-USDT", "KCS-USDT",
    "RUNE-USDT", "CRV-USDT", "LRC-USDT", "ENJ-USDT", "YFI-USDT",
    "SNX-USDT", "CRO-USDT", "FLOW-USDT", "COMP-USDT", "CHZ-USDT",
    "AR-USDT", "THETA-USDT", "KAVA-USDT", "ZIL-USDT", "XTZ-USDT",
    "KSM-USDT", "CAKE-USDT", "SUSHI-USDT", "OMG-USDT", "REN-USDT",
    "BNT-USDT", "RSR-USDT", "BAL-USDT", "CELR-USDT", "LPT-USDT",
    "STMX-USDT", "ANKR-USDT", "COTI-USDT", "REEF-USDT", "OCEAN-USDT",
    "DODO-USDT", "CTSI-USDT", "POLS-USDT", "API3-USDT", "RLC-USDT",
    "ALPHA-USDT", "LINA-USDT", "BAND-USDT", "KLAY-USDT", "WAVES-USDT",
    "NKN-USDT", "ARDR-USDT", "BTS-USDT", "STRAX-USDT", "XEM-USDT",
    "VTHO-USDT", "STORJ-USDT", "BLZ-USDT", "SC-USDT", "FUN-USDT",
    "WIN-USDT", "DENT-USDT", "HOT-USDT", "PERL-USDT", "TOMO-USDT",
    "ELF-USDT", "DOCK-USDT", "NULS-USDT", "MFT-USDT", "KEY-USDT",
    "VIDT-USDT", "PHA-USDT", "ORN-USDT", "AKRO-USDT", "LIT-USDT"
]

# جایگزین کردن نمادهای غیر پشتیبانی شده
# بررسی دقیق نمادهای پشتیبانی شده در KuCoin
KUCOIN_SUPPORTED_PAIRS = {
    "MATIC-USDT": "POLY-USDT",  # جایگزین برای MATIC که پشتیبانی نمی‌شود
}

# تنظیمات استراتژی اسکالپینگ
SCALPING_SETTINGS = {
    'rsi_period': 14,
    'rsi_overbought': 65,
    'rsi_oversold': 35,
    'ema_short': 8,
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
KLINE_SIZE = 500   # تعداد کندل‌ها
SIGNALS_FILE = "data/signals.json"
