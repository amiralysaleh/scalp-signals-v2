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
    try:
        if os.path.exists(SIGNALS_FILE):
            with open(SIGNALS_FILE, 'r') as f:
                content = f.read()
                if not content.strip():
                    return []
                return json.loads(content)
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {SIGNALS_FILE}, returning empty list")
        return []
    except Exception as e:
        print(f"Error loading signals: {e}")
        return []

def save_signals(signals):
    """ذخیره سیگنال‌ها"""
    try:
        os.makedirs(os.path.dirname(SIGNALS_FILE), exist_ok=True)
        with open(SIGNALS_FILE, 'w') as f:
            json.dump(signals, f, indent=2)
    except Exception as e:
        print(f"Error saving signals: {e}")

def save_signal(signal):
    """افزودن سیگنال جدید"""
    try:
        signals = load_signals()
        signals.append(signal)
        save_signals(signals)
        print(f"Signal saved: {signal['symbol']} {signal['type']}")
    except Exception as e:
        print(f"Error saving signal: {e}")

def get_current_price(symbol):
    """دریافت قیمت فعلی از KuCoin"""
    url = f"{KUCOIN_BASE_URL}{KUCOIN_TICKER_ENDPOINT}"
    params = {"symbol": symbol}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('data') and data['data'].get('price'):
            return float(data['data']['price'])
        print(f"No price data returned for {symbol}")
        return None
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

def update_signal_status():
    """به‌روزرسانی وضعیت سیگنال‌ها"""
    try:
        signals = load_signals()
        if not signals:
            return

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
    except Exception as e:
        print(f"Error updating signal status: {e}")

def report_signals_status():
    """ارسال گزارش وضعیت سیگنال‌ها"""
    try:
        update_signal_status()
        signals = load_signals()
        
        active_signals = [s for s in signals if s.get('status') == 'active']
        target_reached = [s for s in signals if s.get('status') == 'target_reached']
        stop_loss_signals = [s for s in signals if s.get('status') == 'stop_loss']

        message = "📊 گزارش وضعیت سیگنال‌ها 📊\n\n"
        message += f"🟢 سیگنال‌های فعال: {len(active_signals)}\n"
        message += f"✅ سیگنال‌های موفق: {len(target_reached)}\n"
        message += f"❌ سیگنال‌های ناموفق: {len(stop_loss_signals)}\n\n"

        if active_signals:
            message += "🔹 سیگنال‌های فعال:\n"
            for signal in active_signals:
                current_price = get_current_price(signal['symbol'])
                if current_price is not None:
                    price_diff = ((current_price - float(signal['entry_price'])) / float(signal['entry_price'])) * 100
                    price_diff_str = f"{price_diff:.2f}%"
                    if price_diff > 0:
                        price_diff_str = f"+{price_diff_str}"
                    message += f"- {signal['symbol']} ({signal['type']}): قیمت فعلی {current_price} ({price_diff_str})\n"
                else:
                    message += f"- {signal['symbol']} ({signal['type']}): قیمت نامعلوم\n"

        send_telegram_message(message)
        print("Report sent successfully")
    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Track and report signal status')
    parser.add_argument('--report', action='store_true', help='Generate and send a status report')
    args = parser.parse_args()
    
    try:
        if args.report:
            report_signals_status()
        else:
            update_signal_status()
    except Exception as e:
        print(f"Error in main execution: {e}")
