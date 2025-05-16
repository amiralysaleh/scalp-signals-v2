import requests
import pandas as pd
import numpy as np
import json
import os
import time
from datetime import datetime, timedelta
import pytz
import ta
import traceback
from config import *
from signal_generator import generate_signals
from telegram_sender import send_telegram_message
from signal_tracker import save_signal

def fetch_ohlc_data(coin_id, days=1, points=100):
    """دریافت داده‌های OHLC از CoinGecko"""
    url = f"{BASE_URL}{OHLC_ENDPOINT.format(id=coin_id)}"
    params = {
        "vs_currency": "usd",
        "days": days,
        "precision": "full"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if not isinstance(data, list):
            print(f"Invalid API response for {coin_id}: {data}")
            return None
            
        # تبدیل داده‌ها به دیتافریم
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
        
        # محاسبه حجم (با داده‌های مصنوعی برای نمونه)
        df["volume"] = (df["high"] - df["low"]) * 1000
        
        return df.iloc[-points:]  # بازگشت آخرین نقاط داده
    
    except Exception as e:
        print(f"Error fetching data for {coin_id}: {e}")
        print(f"Exception details: {traceback.format_exc()}")
        return None

def prepare_dataframe(df):
    """اضافه کردن اندیکاتورهای تکنیکال به دیتافریم"""
    if df is None or len(df) < 50:
        return None
    
    try:
        # افزودن شاخص‌های تکنیکال
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
        bollinger = ta.volatility.BollingerBands(df['close'], window=SCALPING_SETTINGS['bb_period'], window_dev=SCALPING_SETTINGS['bb_std'])
        df['bb_upper'] = bollinger.bollinger_hband()
        df['bb_middle'] = bollinger.bollinger_mavg()
        df['bb_lower'] = bollinger.bollinger_lband()
        
        # محاسبه تغییرات حجم
        df['volume_change'] = df['volume'].pct_change()
        
        return df
    except Exception as e:
        print(f"Error preparing DataFrame: {e}")
        return None

def get_current_price(coin_id):
    """دریافت قیمت فعلی از CoinGecko"""
    url = f"{BASE_URL}{TICKER_ENDPOINT}"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get(coin_id, {}).get("usd", None)
    except Exception as e:
        print(f"Error fetching price for {coin_id}: {e}")
        return None

def main():
    print("Starting cryptocurrency analysis with CoinGecko API...")
    signals_sent = 0
    
    for crypto in CRYPTOCURRENCIES:
        print(f"Analyzing {crypto['name']} ({crypto['symbol'].upper()})...")
        
        try:
            # دریافت داده‌های OHLC
            df = fetch_ohlc_data(crypto['id'], days=TIMEFRAME_DAYS, points=DATA_POINTS)
            if df is None:
                continue
                
            # آماده‌سازی دیتافریم
            prepared_df = prepare_dataframe(df)
            if prepared_df is None:
                continue
                
            # تولید سیگنال‌ها
            signals = generate_signals(prepared_df, crypto['symbol'].upper())
            
            # ارسال سیگنال‌ها
            if signals:
                for signal in signals:
                    current_price = get_current_price(crypto['id'])
                    if current_price:
                        signal['current_price'] = f"{current_price:.8f}"
                    
                    message = (
                        f"🚨 سیگنال {signal['type']} برای {signal['symbol']}\n\n"
                        f"💰 قیمت فعلی: {signal['current_price']}\n"
                        f"🎯 قیمت هدف: {signal['target_price']}\n"
                        f"🛑 حد ضرر: {signal['stop_loss']}\n\n"
                        f"📊 دلایل سیگنال:\n{signal['reasons']}\n\n"
                        f"⏱️ زمان: {signal['time']}"
                    )
                    
                    if send_telegram_message(message):
                        signals_sent += 1
                        save_signal(signal)
            
            # رعایت محدودیت نرخ API
            time.sleep(1.5)
            
        except Exception as e:
            print(f"Error analyzing {crypto['name']}: {e}")
    
    print(f"Analysis complete. {signals_sent} signals sent.")

if __name__ == "__main__":
    main()
