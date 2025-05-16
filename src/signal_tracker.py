import json
import os
import requests
from datetime import datetime
import pytz
from config import BASE_URL, TICKER_ENDPOINT, SIGNALS_FILE
from telegram_sender import send_telegram_message

def load_signals():
    """بارگذاری سیگنال‌های ذخیره شده"""
    if os.path.exists(SIGNALS_FILE):
        with open(SIGNALS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_signals(signals):
    """ذخیره‌سازی سیگنال‌ها"""
    os.makedirs(os.path.dirname(SIGNALS_FILE), exist_ok=True)
    with open(SIGNALS_FILE, 'w') as f:
        json.dump(signals, f, indent=2)

def get_current_price(coin_id):
    """دریافت قیمت فعلی از CoinGecko"""
    url = f"{BASE_URL}{TICKER_ENDPOINT}"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get(coin_id, {}).get("usd", None)
    except Exception as e:
        print(f"Error fetching price for {coin_id}: {e}")
        return None

def update_signal_status():
    """بررسی وضعیت سیگنال‌های فعال"""
    signals = load_signals()
    updated = False
    
    for signal in signals:
        if signal['status'] != 'active':
            continue
            
        # پیدا کردن coin_id بر اساس symbol
        coin_id = next(
            (c['id'] for c in CRYPTOCURRENCIES 
            if c['symbol'].upper() == signal['symbol'].lower()), None)
        
        if not coin_id:
            continue
            
        current_price = get_current_price(coin_id)
        if current_price is None:
            continue
            
        target_price = float(signal['target_price'])
        stop_loss = float(signal['stop_loss'])
        
        if signal['type'] == 'خرید':
            if current_price >= target_price:
                signal['status'] = 'target_reached'
                updated = True
            elif current_price <= stop_loss:
                signal['status'] = 'stop_loss'
                updated = True
        elif signal['type'] == 'فروش':
            if current_price <= target_price:
                signal['status'] = 'target_reached'
                updated = True
            elif current_price >= stop_loss:
                signal['status'] = 'stop_loss'
                updated = True
        
        if updated:
            signal['closed_at'] = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
            signal['closed_price'] = str(current_price)
    
    if updated:
        save_signals(signals)
    
    return signals

def report_signals_status():
    """گزارش وضعیت سیگنال‌ها"""
    signals = update_signal_status()
    
    active = [s for s in signals if s['status'] == 'active']
    reached = [s for s in signals if s['status'] == 'target_reached']
    stopped = [s for s in signals if s['status'] == 'stop_loss']
    
    message = "📊 گزارش وضعیت سیگنال‌ها\n\n"
    message += f"🟢 فعال: {len(active)}\n"
    message += f"✅ موفق: {len(reached)}\n"
    message += f"❌ ناموفق: {len(stopped)}\n\n"
    
    if signals:
        message += "آخرین سیگنال‌ها:\n"
        for s in signals[-5:]:
            status_icon = "🟢" if s['status'] == 'active' else "✅" if s['status'] == 'target_reached' else "❌"
            message += f"{status_icon} {s['symbol']} ({s['type']}) - {s['status']}\n"
    
    send_telegram_message(message)

if __name__ == "__main__":
    report_signals_status()
