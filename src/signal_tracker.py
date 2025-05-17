import json
import os
import requests
import argparse
from datetime import datetime
import pytz
from config import SIGNALS_FILE, KUCOIN_BASE_URL, KUCOIN_TICKER_ENDPOINT
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

def get_current_price(symbol):
    """دریافت قیمت فعلی از KuCoin"""
    url = f"{KUCOIN_BASE_URL}{KUCOIN_TICKER_ENDPOINT}"
    params = {"symbol": symbol}

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get('data') and data['data'].get('price'):
            return float(data['data']['price'])
        else:
            print(f"No price data returned for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Track and report signal status')
    parser.add_argument('--report', action='store_true', help='Generate and send a status report')
    args = parser.parse_args()
    
    if args.report:
        report_signals_status()
    else:
        update_signal_status()
