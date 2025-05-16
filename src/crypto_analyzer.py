import requests
import pandas as pd
import numpy as np
import json
import os
import time
from datetime import datetime
import pytz
import ta
from config import *
from signal_generator import generate_signals
from telegram_sender import send_telegram_message
from signal_tracker import save_signal

def fetch_kline_data(symbol, size=100, type="30min"):
    """دریافت داده‌های کندل از Lbank"""
    url = f"{BASE_URL}{KLINE_ENDPOINT}"
    params = {
        "symbol": symbol,
        "size": size,
        "type": type
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data["result"] and len(data["data"]) > 0:
            # تبدیل داده‌ها به دیتافریم pandas
            df = pd.DataFrame(data["data"], columns=["timestamp", "open", "high", "low", "close", "volume"])
            df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            return df
        else:
            print(f"No data returned for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def prepare_dataframe(df):
    """اضافه کردن اندیکاتورهای تکنیکال به دیتافریم"""
    if df is None or len(df) < 50:
        return None
    
    # افزودن شاخص‌های تکنیکال
    # RSI
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=SCALPING_SETTINGS['rsi_period']).rsi()
    
    # میانگین‌های متحرک نمایی
    df['ema_short'] = ta.trend.ema_indicator(df['close'], window=SCALPING_SETTINGS['ema_short'])
    df['ema_medium'] = ta.trend.ema_indicator(df['close'], window=SCALPING_SETTINGS['ema_medium'])
    df['ema_long'] = ta.trend.ema_indicator(df['close'], window=SCALPING_SETTINGS['ema_long'])
    
    # MACD
    macd = ta.trend.MACD(
        df['close'], 
        window_fast=SCALPING_SETTINGS['macd_fast'], 
        window_slow=SCALPING_SETTINGS['macd_slow'], 
        window_sign=SCALPING_SETTINGS['macd_signal']
    )
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()
    
    # باندهای بولینگر
    bollinger = ta.volatility.BollingerBands(
        df['close'], 
        window=SCALPING_SETTINGS['bb_period'], 
        window_dev=SCALPING_SETTINGS['bb_std']
    )
    df['bb_upper'] = bollinger.bollinger_hband()
    df['bb_middle'] = bollinger.bollinger_mavg()
    df['bb_lower'] = bollinger.bollinger_lband()
    
    # محاسبه تغییرات حجم
    df['volume_change'] = df['volume'].pct_change()
    
    # افزودن سطوح حمایت و مقاومت ساده (میانگین کمترین و بیشترین قیمت‌های اخیر)
    df['resistance'] = df['high'].rolling(window=10).max()
    df['support'] = df['low'].rolling(window=10).min()
    
    return df

def main():
    print("Starting cryptocurrency analysis...")
    signals_sent = 0
    
    # پیام شروع به تلگرام
    current_time = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
    send_telegram_message(f"🔍 شروع اسکن ارزهای دیجیتال - {current_time}")
    
    # بررسی همه ارزهای موجود در لیست
    for crypto in CRYPTOCURRENCIES:
        print(f"Analyzing {crypto}...")
        
        # دریافت داده‌ها
        df = fetch_kline_data(crypto, size=KLINE_SIZE, type=TIMEFRAME)
        if df is None:
            continue
        
        # آماده‌سازی دیتافریم با اندیکاتورها
        prepared_df = prepare_dataframe(df)
        if prepared_df is None:
            continue
            
        # تولید سیگنال‌ها
        signals = generate_signals(prepared_df, crypto)
        
        # اگر سیگنالی وجود داشت، ارسال به تلگرام
        if signals:
            for signal in signals:
                message = (
                    f"🚨 سیگنال {signal['type']} برای {signal['symbol']}\n\n"
                    f"💰 قیمت فعلی: {signal['current_price']}\n"
                    f"🎯 قیمت هدف: {signal['target_price']}\n"
                    f"🛑 حد ضرر: {signal['stop_loss']}\n\n"
                    f"📊 دلایل سیگنال:\n{signal['reasons']}\n\n"
                    f"⏱️ زمان: {signal['time']}"
                )
                success = send_telegram_message(message)
                if success:
                    signals_sent += 1
                    # ذخیره سیگنال برای پیگیری
                    save_signal(signal)
        
        # توقف کوتاه برای جلوگیری از محدودیت API
        time.sleep(1)
    
    # پیام پایان به تلگرام
    send_telegram_message(f"✅ اسکن تکمیل شد. {signals_sent} سیگنال ارسال شد.")
    print(f"Analysis complete. {signals_sent} signals sent.")

if __name__ == "__main__":
    main()
