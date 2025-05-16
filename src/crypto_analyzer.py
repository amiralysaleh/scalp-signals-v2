import requests
import pandas as pd
import numpy as np
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

def fetch_kline_data(symbol_id, days=1):
    """دریافت داده‌های کندل از CoinGecko"""
    url = f"{COINGECKO_BASE_URL}{COINGECKO_MARKET_CHART_ENDPOINT}".format(id=symbol_id)
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "minute"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            print(f"Error fetching data for {symbol_id}: {data}")
            return None

        # تبدیل داده‌ها به DataFrame
        prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
        volumes = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])

        df = pd.merge(prices, volumes, on="timestamp")
        df.columns = ["timestamp", "close", "volume"]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["open"] = df["close"].shift(1)
        df["high"] = df["close"].rolling(2).max()
        df["low"] = df["close"].rolling(2).min()
        df.dropna(inplace=True)

        return df
    except Exception as e:
        print(f"Error fetching data for {symbol_id}: {e}")
        print(f"Details: {traceback.format_exc()}")
        return None

def prepare_dataframe(df):
    """اضافه کردن اندیکاتورهای تکنیکال به دیتافریم"""
    if df is None or len(df) < 50:
        return None

    try:
        # افزودن شاخص‌های تکنیکال
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=SCALPING_SETTINGS['rsi_period']).rsi()
        df['ema_short'] = ta.trend.ema_indicator(df['close'], window=SCALPING_SETTINGS['ema_short'])
        df['ema_medium'] = ta.trend.ema_indicator(df['close'], window=SCALPING_SETTINGS['ema_medium'])
        df['ema_long'] = ta.trend.ema_indicator(df['close'], window=SCALPING_SETTINGS['ema_long'])

        macd = ta.trend.MACD(
            df['close'],
            window_fast=SCALPING_SETTINGS['macd_fast'],
            window_slow=SCALPING_SETTINGS['macd_slow'],
            window_sign=SCALPING_SETTINGS['macd_signal']
        )
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()

        bollinger = ta.volatility.BollingerBands(
            df['close'],
            window=SCALPING_SETTINGS['bb_period'],
            window_dev=SCALPING_SETTINGS['bb_std']
        )
        df['bb_upper'] = bollinger.bollinger_hband()
        df['bb_middle'] = bollinger.bollinger_mavg()
        df['bb_lower'] = bollinger.bollinger_lband()

        df['volume_change'] = df['volume'].pct_change()
        df['resistance'] = df['high'].rolling(window=10).max()
        df['support'] = df['low'].rolling(window=10).min()

        return df
    except Exception as e:
        print(f"Error preparing DataFrame: {e}")
        print(f"Details: {traceback.format_exc()}")
        return None

def main():
    print("🚀 Starting cryptocurrency analysis...")
    signals_sent = 0

    for crypto in CRYPTOCURRENCIES:
        print(f"Analyzing {crypto}...")
        try:
            df = fetch_kline_data(crypto, days=TIMEFRAME_IN_DAYS)
            if df is None:
                print(f"Skipping {crypto} due to data issues.")
                continue

            prepared_df = prepare_dataframe(df)
            if prepared_df is None:
                print(f"Skipping {crypto} due to preparation issues.")
                continue

            signals = generate_signals(prepared_df, crypto)
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
                        save_signal(signal)
                        print(f"Signal sent and saved for {crypto}: {signal['type']}")
                    else:
                        print(f"Failed to send signal for {crypto}")
            else:
                print(f"No signals generated for {crypto}")

        except Exception as e:
            print(f"Error during analysis of {crypto}: {e}")
            print(f"Details: {traceback.format_exc()}")

        time.sleep(1)

    send_telegram_message(f"✅ اسکن تکمیل شد. {signals_sent} سیگنال ارسال شد.")
    print(f"Analysis complete. {signals_sent} signals sent.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        print(f"Details: {traceback.format_exc()}")
        send_telegram_message(f"❌ خطای سیستمی: {e}")
