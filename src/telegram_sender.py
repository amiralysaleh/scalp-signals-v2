import requests
import os
import time

def send_telegram_message(message):
    """ارسال پیام به کانال تلگرام"""
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables not set")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"Message sent to Telegram successfully")
            return True
        else:
            print(f"Failed to send message to Telegram: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")
        return False
