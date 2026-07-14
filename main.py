# -*- coding: utf-8 -*-

from telegram_bot import send_telegram, build_signal_message

from market_data import get_market_data
import requests
import pandas as pd
import time
from ai_engine import analyze_market
from risk_manager import calculate_trade
# =====================================
# TELEGRAM
# =====================================
TOKEN = "8229091266:AAHzWGVuzi_F4KCiJ1naL7_knKPBr21E93k"
CHAT_ID = " 729720320"

# =====================================
# TWELVE DATA
# =====================================
API_KEY = "8ddb1cdc9051436b8fc9bfd775b913fc"

# =====================================
# SETTINGS
# =====================================
SYMBOL = "EUR/USD"
INTERVAL = "1h"
OUTPUTSIZE = 200

AUTO_TRADE = False
CHECK_INTERVAL = 3600
RISK_REWARD = 2




df = get_market_data()

if df is None:
    print("No market data available. Waiting for next cycle...")
    exit()

print(df.tail())

def calculate_indicators(df):
    # EMA 20
    df["EMA20"] = df["close"].ewm(span=20, adjust=False).mean()

    # EMA 50
    df["EMA50"] = df["close"].ewm(span=50, adjust=False).mean()

    # RSI 14
    delta = df["close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df


df = calculate_indicators(df)

print(df[[
    "close",
    "EMA20",
    "EMA50",
    "RSI",
    "MACD",
    "MACD_SIGNAL"
]].tail())

def generate_signal(df):
    last = df.iloc[-1]

    if (
        last["EMA20"] > last["EMA50"] and
        last["MACD"] > last["MACD_SIGNAL"] and
        last["RSI"] > 50
    ):
        signal = "BUY"

    elif (
        last["EMA20"] < last["EMA50"] and
        last["MACD"] < last["MACD_SIGNAL"] and
        last["RSI"] < 50
    ):
        signal = "SELL"

    else:
        signal = "WAIT"

    print("=" * 40)
    print("SIGNAL :", signal)
    print("PRICE  :", last["close"])
    print("EMA20  :", round(last["EMA20"], 5))
    print("EMA50  :", round(last["EMA50"], 5))
    print("RSI    :", round(last["RSI"], 2))
    print("MACD   :", round(last["MACD"], 5))
    print("SIGNAL :", round(last["MACD_SIGNAL"], 5))
    print("=" * 40)

    return signal


generate_signal(df)

BOT_TOKEN = "8229091266:AAHzWGVuzi_F4KCiJ1naL7_knKPBr21E93k"
CHAT_ID = "729720320"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=data)
    return response.json()
    
ai_result = analyze_market(df)

last = df.iloc[-1]

trade_data = calculate_trade(
    ai_result["price"],
    ai_result["signal"],
    0.001
)


signal = ai_result["signal"]
confidence = ai_result["confidence"]
reasons = ai_result["reasons"]
price = ai_result["price"]

atr = ai_result["atr"]

message = f"""
📊 Forex AI Analyzer V2

الزوج: {SYMBOL}

الإشارة: {signal}

الثقة: {confidence}%

السعر: {price}

الأسباب:
{chr(10).join(reasons)}
"""

send_telegram(message)

print("Telegram message sent")
