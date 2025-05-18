from datetime import datetime
import pytz
from config import SCALPING_SETTINGS

def generate_signals(df, symbol):
    """تولید سیگنال‌های خرید و فروش بر اساس استراتژی اسکالپ"""
    if df is None or len(df) < 2:
        return []

    signals = []
    latest_row = df.iloc[-1]
    prev_row = df.iloc[-2]
    current_price = latest_row['close']

    # ----- استراتژی خرید -----
    buy_reasons = []

    # RSI: شرایط خرید در حالت oversold
    if latest_row['rsi'] < SCALPING_SETTINGS['rsi_oversold'] and prev_row['rsi'] < latest_row['rsi']:
        buy_reasons.append(f"RSI در ناحیه oversold ({latest_row['rsi']:.2f}) و در حال بهبود")

    # EMA: کراس به بالا
    if (prev_row['ema_short'] <= prev_row['ema_medium'] and 
        latest_row['ema_short'] > latest_row['ema_medium']):
        buy_reasons.append(f"کراس EMA کوتاه‌مدت به بالای EMA میان‌مدت")

    # MACD: کراس به بالا
    if (prev_row['macd'] <= prev_row['macd_signal'] and 
        latest_row['macd'] > latest_row['macd_signal']):
        buy_reasons.append(f"کراس MACD به بالای خط سیگنال")

    # Bollinger Bands: لمس باند پایین
    if latest_row['close'] <= latest_row['bb_lower'] * 1.01:
        buy_reasons.append(f"قیمت نزدیک/زیر باند پایین بولینگر")

    # افزایش حجم معاملات
    if latest_row['volume_change'] > SCALPING_SETTINGS['volume_change_threshold']:
        buy_reasons.append(f"افزایش قابل توجه حجم معاملات ({latest_row['volume_change']:.2f}X)")

    # سطح حمایت
    if latest_row['close'] <= latest_row['support'] * 1.01:
        buy_reasons.append(f"قیمت در نزدیکی/روی سطح حمایت ({latest_row['support']:.4f})")

    # ----- استراتژی فروش -----
    sell_reasons = []

    # RSI: شرایط فروش در حالت overbought
    if latest_row['rsi'] > SCALPING_SETTINGS['rsi_overbought'] and prev_row['rsi'] > latest_row['rsi']:
        sell_reasons.append(f"RSI در ناحیه overbought ({latest_row['rsi']:.2f}) و در حال کاهش")

    # EMA: کراس به پایین
    if (prev_row['ema_short'] >= prev_row['ema_medium'] and 
        latest_row['ema_short'] < latest_row['ema_medium']):
        sell_reasons.append(f"کراس EMA کوتاه‌مدت به پایین EMA میان‌مدت")

    # MACD: کراس به پایین
    if (prev_row['macd'] >= prev_row['macd_signal'] and 
        latest_row['macd'] < latest_row['macd_signal']):
        sell_reasons.append(f"کراس MACD به پایین خط سیگنال")

    # Bollinger Bands: لمس باند بالا
    if latest_row['close'] >= latest_row['bb_upper'] * 0.99:
        sell_reasons.append(f"قیمت نزدیک/بالای باند بالایی بولینگر")

    # سطح مقاومت
    if latest_row['close'] >= latest_row['resistance'] * 0.99:
        sell_reasons.append(f"قیمت در نزدیکی/روی سطح مقاومت ({latest_row['resistance']:.4f})")

    # ایجاد سیگنال‌ها
    current_time = datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")

    # کاهش تعداد دلایل مورد نیاز از 3 به 2 برای افزایش احتمال تولید سیگنال
    if len(buy_reasons) >= 4:
        target_price = current_price * (1 + SCALPING_SETTINGS['profit_target_percent'] / 100)
        stop_loss = current_price * (1 - SCALPING_SETTINGS['stop_loss_percent'] / 100)

        signals.append({
            'symbol': symbol,
            'type': 'خرید',
            'current_price': f"{current_price:.8f}",
            'target_price': f"{target_price:.8f}",
            'stop_loss': f"{stop_loss:.8f}",
            'time': current_time,
            'reasons': "\n".join([f"✅ {reason}" for reason in buy_reasons]),
            'status': 'active',
            'created_at': current_time
        })

    if len(sell_reasons) >= 4:
        target_price = current_price * (1 - SCALPING_SETTINGS['profit_target_percent'] / 100)
        stop_loss = current_price * (1 + SCALPING_SETTINGS['stop_loss_percent'] / 100)

        signals.append({
            'symbol': symbol,
            'type': 'فروش',
            'current_price': f"{current_price:.8f}",
            'target_price': f"{target_price:.8f}",
            'stop_loss': f"{stop_loss:.8f}",
            'time': current_time,
            'reasons': "\n".join([f"✅ {reason}" for reason in sell_reasons]),
            'status': 'active',
            'created_at': current_time
        })

    return signals
