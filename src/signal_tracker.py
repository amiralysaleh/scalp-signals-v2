import json
import os
import requests
import pandas as pd
import argparse
from datetime import datetime
import pytz
from config import SIGNALS_FILE, BASE_URL, TICKER_ENDPOINT
from telegram_sender import send_telegram_message

def load_signals():
    """بارگذاری سیگنال‌های ذخیره شده"""
    if os.path.exists(SIGNALS_FILE):
        with open(SIGNALS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_signals(signals):
    """ذخیره‌سازی سیگنال‌ها"""
    # اطمینان از وجود دایرکتوری
    os.makedirs(os.path.dirname(SIGNALS_FILE), exist_ok=True)
    
    with open(SIGNALS_FILE, 'w') as f:
        json.dump(signals, f, indent=2)

def save_signal(signal):
    """افزودن یک سیگنال جدید به لیست سیگنال‌ها"""
    signals = load_signals()
    signals.append(signal)
    save_signals(signals)
    print(f"Signal saved: {signal['symbol']} {signal['type']}")

def get_current_price(symbol):
    """دریافت قیمت فعلی یک ارز"""
    url = f"{BASE_URL}{TICKER_ENDPOINT}"
    params = {"symbol": symbol}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data["result"] and "ticker" in data:
            return float(data["ticker"]["latest"])
        else:
            print(f"No price data returned for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

def update_signal_status():
    """بررسی وضعیت سیگنال‌های فعال و به‌روزرسانی آن‌ها"""
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
    
    return signals

def report_signals_status():
    """گزارش وضعیت تمام سیگنال‌های فعال"""
    signals = update_signal_status()
    
    active_signals = [s for s in signals if s['status'] == 'active']
    target_reached = [s for s in signals if s['status'] == 'target_reached']
    stop_loss_signals = [s for s in signals if s['status'] == 'stop_loss']
    
    # فیلتر برای سیگنال‌های اخیر (24 ساعت گذشته)
    now = datetime.now(pytz.timezone('Asia/Tehran'))
    
    # ساخت پیام گزارش
    message = "📊 گزارش وضعیت سیگنال‌ها 📊\n\n"
    
    message += f"🟢 سیگنال‌های فعال: {len(active_signals)}\n"
    for signal in active_signals:
        current_price = get_current_price(signal['symbol']) or "نامشخص"
        message += f"{signal['symbol']} ({signal['type']}) - قیمت فعلی: {current_price}\n"
    
    message += f"\n✅ سیگنال‌های موفق (رسیدن به هدف): {len(target_reached)}\n"
    for signal in target_reached[-5:]:  # نمایش 5 مورد آخر
        message += f"{signal['symbol']} ({signal['type']}) - سود: {calculate_profit(signal)}\n"
    
    message += f"\n❌ سیگنال‌های ناموفق (استاپ لاس): {len(stop_loss_signals)}\n"
    for signal in stop_loss_signals[-5:]:  # نمایش 5 مورد آخر
        message += f"{signal['symbol']} ({signal['type']}) - ضرر: {calculate_profit(signal)}\n"
    
    # ارسال گزارش به تلگرام
    send_telegram_message(message)
    print("Signal status report sent")

def calculate_profit(signal):
    """محاسبه سود یا ضرر برای یک سیگنال بسته شده"""
    if 'closed_price' not in signal:
        return "نامشخص"
        
    entry_price = float(signal['current_price'])
    exit_price = float(signal['closed_price'])
    
    if signal['type'] == 'خرید':
        profit_percent = (exit_price - entry_price) / entry_price * 100
    else:  # فروش
        profit_percent = (entry_price - exit_price) / entry_price * 100
        
    return f"{profit_percent:.2f}٪"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Track and report crypto signals')
    parser.add_argument('--report', action='store_true', help='Generate and send status report')
    args = parser.parse_args()
    
    if args.report:
        report_signals_status()
