# لیست ارزهای دیجیتال برای بررسی - نمادهای سازگار با KuCoin
CRYPTOCURRENCIES = [
    "BTC-USDT", "ETH-USDT", "BNB-USDT", "SOL-USDT", "XRP-USDT",
    "ADA-USDT", "DOGE-USDT", "SHIB-USDT", "DOT-USDT", 
    "LTC-USDT", "AVAX-USDT", "LINK-USDT", "UNI-USDT", "ATOM-USDT",
    "TRX-USDT", "NEAR-USDT", "MATIC-USDT", "APT-USDT",
    "PEPE-USDT", "ICP-USDT", "ETC-USDT", "XLM-USDT", "HBAR-USDT",
    "INJ-USDT", "VET-USDT", "CRO-USDT", "OP-USDT", "ALGO-USDT",
    "GRT-USDT", "SUI-USDT", "AAVE-USDT", "FTM-USDT", "FLOW-USDT",
    "AR-USDT", "EGLD-USDT", "AXS-USDT", "CHZ-USDT", "SAND-USDT",
    "MANA-USDT", "NEO-USDT", "KAVA-USDT", "XTZ-USDT", "KCS-USDT",
    "MINA-USDT", "GALA-USDT", "ZIL-USDT", "ENJ-USDT", "1INCH-USDT",
    "HOT-USDT", "COMP-USDT", "ZEC-USDT", "RVN-USDT", "BAT-USDT",
    "DASH-USDT", "WAXP-USDT", "LRC-USDT", "QTUM-USDT", "ICX-USDT",
    "ONT-USDT", "WAVES-USDT", "KSM-USDT", "CHR-USDT",
    "ANKR-USDT", "OCEAN-USDT", "IOST-USDT", "SC-USDT", "RSR-USDT",
    "DCR-USDT", "SYS-USDT", "GLMR-USDT", "BICO-USDT", "COTI-USDT",
    "SKL-USDT", "BAL-USDT", "LPT-USDT", "CELR-USDT", "DGB-USDT",
    "XYO-USDT", "API3-USDT", "OMG-USDT", "POWR-USDT", "SXP-USDT",
    "REQ-USDT", "VTHO-USDT", "XEM-USDT", "NKN-USDT", "CTSI-USDT",
    "STPT-USDT", "FLUX-USDT", "PUNDIX-USDT", "STRAX-USDT", "AUDIO-USDT",
    "ARDR-USDT", "STEEM-USDT", "CVC-USDT", "SNT-USDT", "DENT-USDT",
    "HIVE-USDT", "LOOM-USDT", "ARK-USDT", "TLM-USDT", "RLC-USDT",
    "NMR-USDT", "SLP-USDT", "AGLD-USDT", "FORTH-USDT", "REI-USDT",
    "PHA-USDT", "AERGO-USDT", "CLV-USDT", "TRAC-USDT", "LTO-USDT",
    "MLN-USDT", "RIF-USDT", "GHST-USDT", "DUSK-USDT", "BAND-USDT",
    "ORBS-USDT", "UOS-USDT", "ERN-USDT", "MDT-USDT", "KMD-USDT",
    "WNCG-USDT", "QKC-USDT"
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
