import json
import os
import requests
from datetime import datetime
import pytz
from config import SIGNALS_FILE, COINGECKO_BASE_URL, COINGECKO_PRICE_ENDPOINT
from telegram_sender import send_telegram_message

def load_signals():
    """بارگذاری سیگنال‌های ذخیره‌شده"""
    if os.path.exists(SIGNALS_FILE):
        with open(SIGNALS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_signals(signals):
    """ذخیره سیگنال‌ها"""
    os.makedirs(os.path.dirname(SIGNALS_FILE), exist_ok=True)
    with open(SIGNALS_FILE, 'w') as f:
        json.dump(signals, f, indent=2)

def save_signal(signal):
    """افزودن سیگنال جدید"""
    signals = load_signals()
    signals.append(signal)
    save_signals(signals)
    print(f"Signal saved: {signal['symbol']} {signal['type']}")

def get_current_price(symbol_id):
    """دریافت قیمت فعلی از CoinGecko"""
    url = f"{COINGECKO_BASE_URL}{COINGECKO_PRICE_ENDPOINT}"
    params = {
        "ids": symbol_id,
        "vs_currencies": "usd"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if symbol_id in data:
            return float(data[symbol_id]["usd"])
        else:
            print(f"No price data returned for {symbol_id}")
            return None
    except Exception as e:
        print(f"Error fetching price for {symbol_id}: {e}")
        return None

def update_signal_status():
    """به‌روزرسانی وضعیت سیگنال‌ها"""
    signals = load_signals()
    updated = False

    for signal in signals:
        if signal['status'] != 'active':
            continue

        current_price = get_current_price(signal['symbol'])
        if current_price is None:
            continue

        target_price = float(signal['target_price'])
        stop_loss = float(signal['stop_loss'])

        if signal['type'] == 'خرید':
            if current_price >= target_price:
                signal['status'] = 'target_reached'
                signal['closed_price'] = str(current_price)
                signal['closed_at'] = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
                updated = True
            elif current_price <= stop_loss:
                signal['status'] = 'stop_loss'
                signal['closed_price'] = str(current_price)
                signal['closed_at'] = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
                updated = True
        elif signal['type'] == 'فروش':
            if current_price <= target_price:
                signal['status'] = 'target_reached'
                signal['closed_price'] = str(current_price)
                signal['closed_at'] = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
                updated = True
            elif current_price >= stop_loss:
                signal['status'] = 'stop_loss'
                signal['closed_price'] = str(current_price)
                signal['closed_at'] = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
                updated = True

    if updated:
        save_signals(signals)

def report_signals_status():
    """ارسال گزارش وضعیت سیگنال‌ها"""
    update_signal_status()
    signals = load_signals()
    active_signals = [s for s in signals if s['status'] == 'active']
    target_reached = [s for s in signals if s['status'] == 'target_reached']
    stop_loss_signals = [s for s in signals if s['status'] == 'stop_loss']

    message = "📊 گزارش وضعیت سیگنال‌ها 📊\n\n"
    message += f"🟢 سیگنال‌های فعال: {len(active_signals)}\n"
    message += f"✅ سیگنال‌های موفق: {len(target_reached)}\n"
    message += f"❌ سیگنال‌های ناموفق: {len(stop_loss_signals)}\n"

    send_telegram_message(message)
