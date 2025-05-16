import requests
import pandas as pd
import numpy as np
import json
import os
import time
from datetime import datetime
import pytz
import ta
import traceback
from config import *
from signal_generator import generate_signals
from telegram_sender import send_telegram_message
from signal_tracker import save_signal

def fetch_kline_data(symbol, size=100, type="30min"):
    """دریافت داده‌های کندل از Lbank"""
    url = f"{BASE_URL}{KLINE_ENDPOINT}"
    params = {
        "symbol": symbol.lower(),  # تبدیل به حروف کوچک
        "size": size,
        "type": type
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # گزارش اطلاعات دیباگ
        print(f"API Request for {symbol}: {url} with params {params}")
        print(f"API Response status: {response.status_code}")
        
        # بررسی دقیق‌تر ساختار پاسخ
        if "result" not in data:
            print(f"Missing 'result' in API response for {symbol}: {data}")
            return None
        
        if not data["result"]:
            print(f"API returned false result for {symbol}: {data}")
            return None
        
        if "data" not in data:
            print(f"Missing 'data' in API response for {symbol}: {data}")
            return None
        
        if not data["data"] or len(data["data"]) == 0:
            print(f"Empty data array for {symbol}: {data}")
            return None
        
        # در اینجا داده‌ها به درستی دریافت شده‌اند
        print(f"Received {len(data['data'])} candles for {symbol}")
        
        # تبدیل داده‌ها به دیتافریم pandas
        try:
            df = pd.DataFrame(data["data"], columns=["timestamp", "open", "high", "low", "close", "volume"])
            df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            return df
        except Exception as e:
            print(f"Error converting data to DataFrame for {symbol}: {e}")
            print(f"Data sample: {data['data'][:2]}")
            return None
            
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        print(f"Exception details: {traceback.format_exc()}")
        return None

def prepare_dataframe(df):
    """اضافه کردن اندیکاتورهای تکنیکال به دیتافریم"""
    if df is None or len(df) < 50:
        return None
    
    try:
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
        
        # افزودن سطوح حمایت و مقاومت ساده
        df['resistance'] = df['high'].rolling(window=10).max()
        df['support'] = df['low'].rolling(window=10).min()
        
        return df
    except Exception as e:
        print(f"Error preparing DataFrame: {e}")
        print(f"Exception details: {traceback.format_exc()}")
        return None

def main():
    print("Starting cryptocurrency analysis...")
    signals_sent = 0
    
    # بررسی متغیرهای محیطی
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("WARNING: Telegram credentials are missing. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
    else:
        print(f"Telegram Bot Token: {bot_token[:5]}...{bot_token[-5:] if bot_token else 'None'}")
        print(f"Telegram Chat ID: {chat_id}")
    
    # پیام شروع به تلگرام
    current_time = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
    send_result = send_telegram_message(f"🔍 شروع اسکن ارزهای دیجیتال - {current_time}")
    if not send_result:
        print("Failed to send initial Telegram message. Check your bot token and chat ID.")
    
    # بررسی همه ارزهای موجود در لیست
    for crypto in CRYPTOCURRENCIES:
        print(f"Analyzing {crypto}...")
        
        try:
            # دریافت داده‌ها
            df = fetch_kline_data(crypto, size=KLINE_SIZE, type=TIMEFRAME)
            if df is None:
                print(f"Skipping {crypto} due to data retrieval issues")
                continue
            
            # آماده‌سازی دیتافریم با اندیکاتورها
            prepared_df = prepare_dataframe(df)
            if prepared_df is None:
                print(f"Skipping {crypto} due to data preparation issues")
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
                        print(f"Signal sent and saved for {crypto}: {signal['type']}")
                    else:
                        print(f"Failed to send signal for {crypto}")
            else:
                print(f"No signals generated for {crypto}")
                
        except Exception as e:
            print(f"Error during analysis of {crypto}: {e}")
            print(f"Exception details: {traceback.format_exc()}")
        
        # توقف کوتاه برای جلوگیری از محدودیت API
        time.sleep(1)
    
    # پیام پایان به تلگرام
    send_telegram_message(f"✅ اسکن تکمیل شد. {signals_sent} سیگنال ارسال شد.")
    print(f"Analysis complete. {signals_sent} signals sent.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error in main function: {e}")
        print(f"Exception details: {traceback.format_exc()}")
        send_telegram_message(f"❌ خطای سیستمی: {e}")
