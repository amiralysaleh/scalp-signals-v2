from datetime import datetime
import pytz
import pandas as pd
import ta
from config import SCALPING_SETTINGS

def calculate_atr(df, window=14):
    """محاسبه میانگین محدوده واقعی"""
    return ta.volatility.AverageTrueRange(
        df['high'], df['low'], df['close'], window=window
    ).average_true_range()

def calculate_signal_score(reasons):
    """سیستم امتیازدهی پیشرفته"""
    score_map = {
        'rsi': 1.0, 'ema': 1.5, 'macd': 1.5, 
        'volume': 1.2, 'bollinger': 1.3,
        'support': 1.4, 'resistance': 1.4,
        'higher_tf': 2.0
    }
    return sum(score_map.get(key, 0) for key in reasons)

def generate_signals(df, symbol, higher_tf_confirmed=False):
    """نسخه پیشرفته تولید سیگنال"""
    if df is None or len(df) < 50:
        return []

    # محاسبه اندیکاتورهای پیشرفته
    df['atr'] = calculate_atr(df)
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    buy_reasons, sell_reasons = [], []
    current_price = latest['close']
    atr = latest['atr']

    # فیلتر نوسان
    volatility_ok = (atr / current_price * 100) > SCALPING_SETTINGS['min_volatility']
    
    # شرایط خرید
    if latest['rsi'] < SCALPING_SETTINGS['rsi_oversold'] and prev['rsi'] < latest['rsi']:
        buy_reasons.append('rsi')
    
    if (prev['ema_short'] <= prev['ema_medium'] and 
        latest['ema_short'] > latest['ema_medium']):
        buy_reasons.append('ema')
    
    if (prev['macd'] <= prev['macd_signal'] and 
        latest['macd'] > latest['macd_signal']):
        buy_reasons.append('macd')
    
    if latest['close'] <= latest['bb_lower'] * 1.01:
        buy_reasons.append('bollinger')
    
    if latest['volume_change'] > SCALPING_SETTINGS['volume_change_threshold']:
        buy_reasons.append('volume')
    
    if latest['close'] <= latest['support'] * 1.01:
        buy_reasons.append('support')
    
    if higher_tf_confirmed:
        buy_reasons.append('higher_tf')

    # شرایط فروش (معکوس شرایط خرید)
    if latest['rsi'] > SCALPING_SETTINGS['rsi_overbought'] and prev['rsi'] > latest['rsi']:
        sell_reasons.append('rsi')
    
    if (prev['ema_short'] >= prev['ema_medium'] and 
        latest['ema_short'] < latest['ema_medium']):
        sell_reasons.append('ema')
    
    if (prev['macd'] >= prev['macd_signal'] and 
        latest['macd'] < latest['macd_signal']):
        sell_reasons.append('macd')
    
    if latest['close'] >= latest['bb_upper'] * 0.99:
        sell_reasons.append('bollinger')
    
    if latest['close'] >= latest['resistance'] * 0.99:
        sell_reasons.append('resistance')

    # تولید سیگنال‌ها
    signals = []
    current_time = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")
    
    # محاسبه داینامیک حد سود و ضرر
    profit_ratio = 1.5 * (atr / current_price)
    loss_ratio = 1.0 * (atr / current_price)
    
    buy_score = calculate_signal_score(buy_reasons)
    sell_score = calculate_signal_score(sell_reasons)
    
    if (len(buy_reasons) >= 4 and buy_score >= SCALPING_SETTINGS['score_threshold'] 
        and volatility_ok):
        signals.append({
            'symbol': symbol,
            'type': 'buy',
            'entry_price': f"{current_price:.8f}",
            'target_price': f"{current_price * (1 + profit_ratio):.8f}",
            'stop_loss': f"{current_price * (1 - loss_ratio):.8f}",
            'time': current_time,
            'reasons': ", ".join(buy_reasons),
            'score': buy_score,
            'status': 'active'
        })
    
    if (len(sell_reasons) >= 4 and sell_score >= SCALPING_SETTINGS['score_threshold']
        and volatility_ok):
        signals.append({
            'symbol': symbol,
            'type': 'sell',
            'entry_price': f"{current_price:.8f}",
            'target_price': f"{current_price * (1 - profit_ratio):.8f}",
            'stop_loss': f"{current_price * (1 + loss_ratio):.8f}",
            'time': current_time,
            'reasons': ", ".join(sell_reasons),
            'score': sell_score,
            'status': 'active'
        })
    
    return signals
