# ==========================================
# Forex_mustfa_ai V5.2 Stable
# Single File Version
# Analysis Only Mode
# ==========================================

import time
import logging
import requests
import pandas as pd
import numpy as np

try:
    import ta
except:
    ta = None


# ==========================================
# CONFIG
# ==========================================

SYMBOL = "EUR/USD"
INTERVAL = "1h"
OUTPUT_SIZE = 200

TWELVE_DATA_API_KEY = "PUT_YOUR_API_KEY_HERE"

BOT_TOKEN = "PUT_YOUR_TELEGRAM_TOKEN_HERE"
CHAT_ID = "PUT_YOUR_CHAT_ID_HERE"


# Trading Safety
AUTO_TRADE = False

CONFIDENCE_LIMIT = 70

CHECK_INTERVAL = 3600


# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ==========================================
# TELEGRAM SEND
# ==========================================

def send_telegram(message):

    if "PUT_YOUR" in BOT_TOKEN:
        logging.warning(
            "Telegram token not configured"
        )
        return

    try:

        url = (
            f"https://api.telegram.org/"
            f"bot{BOT_TOKEN}/sendMessage"
        )

        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        requests.post(
            url,
            data=data,
            timeout=10
        )


    except Exception as e:

        logging.error(
            f"Telegram error: {e}"
        )
        # ==========================================
# MARKET DATA
# ==========================================

def get_market_data():

    try:

        url = "https://api.twelvedata.com/time_series"

        params = {
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "outputsize": OUTPUT_SIZE,
            "apikey": TWELVE_DATA_API_KEY
        }


        response = requests.get(
            url,
            params=params,
            timeout=15
        )


        data = response.json()


        if "values" not in data:

            logging.warning(
                f"Market data error: {data}"
            )

            return None


        df = pd.DataFrame(
            data["values"]
        )


        for col in [
            "open",
            "high",
            "low",
            "close"
        ]:

            df[col] = df[col].astype(float)


        df = df.sort_index()


        return df


    except Exception as e:

        logging.error(
            f"Market data failed: {e}"
        )

        return None



# ==========================================
# AI ANALYZER
# ==========================================

def analyze_market(df):


    close = df["close"]


    ema20 = (
        close
        .ewm(span=20)
        .mean()
    )


    ema50 = (
        close
        .ewm(span=50)
        .mean()
    )


    buy_score = 0
    sell_score = 0

    reasons = []


    # EMA TREND

    if ema20.iloc[-1] > ema50.iloc[-1]:

        buy_score += 25

        reasons.append(
            "EMA trend bullish"
        )

    else:

        sell_score += 25

        reasons.append(
            "EMA trend bearish"
        )



    # RSI

    if ta:

        try:

            rsi = (
                ta.momentum
                .RSIIndicator(
                    close
                )
                .rsi()
                .iloc[-1]
            )


            if rsi > 55:

                buy_score += 25

                reasons.append(
                    "RSI bullish"
                )


            elif rsi < 45:

                sell_score += 25

                reasons.append(
                    "RSI bearish"
                )


        except Exception as e:

            logging.error(
                f"RSI error {e}"
            )



    # FINAL DECISION

    if buy_score >= sell_score:

        signal = "BUY"

        confidence = buy_score


    else:

        signal = "SELL"

        confidence = sell_score



    if confidence < CONFIDENCE_LIMIT:

        signal = "WAIT"



    return {

        "signal": signal,

        "confidence": confidence,

        "entry": round(
            float(close.iloc[-1]),
            5
        ),

        "reason": ", ".join(
            reasons
        )

    }
    # ==========================================
# RISK MANAGEMENT
# ==========================================

def calculate_levels(signal, entry):

    atr = entry * 0.002

    if signal == "BUY":

        stop_loss = entry - atr

        tp1 = entry + (atr * 1.5)

        tp2 = entry + (atr * 2.5)

        tp3 = entry + (atr * 3.5)


    else:

        stop_loss = entry + atr

        tp1 = entry - (atr * 1.5)

        tp2 = entry - (atr * 2.5)

        tp3 = entry - (atr * 3.5)


    return {

        "SL": round(stop_loss, 5),

        "TP1": round(tp1, 5),

        "TP2": round(tp2, 5),

        "TP3": round(tp3, 5)

    }



# ==========================================
# SIGNAL MESSAGE
# ==========================================

def create_signal_message(result):


    levels = calculate_levels(
        result["signal"],
        result["entry"]
    )


    message = f"""
📊 Forex AI Analyzer V5.2

Pair: {SYMBOL}

Signal: {result['signal']}

Confidence:
{result['confidence']}%

Entry:
{result['entry']}

🛑 Stop Loss:
{levels['SL']}

🎯 TP1:
{levels['TP1']}

🎯 TP2:
{levels['TP2']}

🎯 TP3:
{levels['TP3']}


Reason:
{result['reason']}


🤖 Auto Trade:
OFF

⚠️ Analysis Only
"""


    return message



# ==========================================
# MAIN LOOP
# ==========================================

def start_bot():


    send_telegram(
        "🟢 Forex_mustfa_ai V5.2 Started"
    )


    logging.info(
        "Bot started"
    )


    while True:


        try:


            df = get_market_data()


            if df is None:


                logging.warning(
                    "No market data"
                )


            else:


                result = analyze_market(df)


                logging.info(
                    str(result)
                )


                if result["signal"] != "WAIT":


                    msg = create_signal_message(
                        result
                    )


                    send_telegram(
                        msg
                    )


        except Exception as e:


            logging.error(
                f"MAIN ERROR: {e}"
            )


            send_telegram(
                f"⚠️ Bot Error\n{e}"
            )



        time.sleep(
            CHECK_INTERVAL
        )



# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    start_bot()
