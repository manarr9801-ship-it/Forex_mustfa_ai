# =====================================
# Forex_mustfa_ai V4.1
# MAIN ENGINE
# =====================================

import time
from datetime import datetime

from market_data import get_market_data

from ai_engine import analyze_market

from risk_manager import calculate_trade

from telegram_bot import (
    send_telegram,
    build_signal_message
)

from config import (
    SYMBOL,
    CHECK_INTERVAL
)


LAST_SIGNAL = None
LAST_TIME = None



def calculate_indicators(df):


    # EMA

    df["EMA20"] = (
        df["close"]
        .ewm(
            span=20,
            adjust=False
        )
        .mean()
    )


    df["EMA50"] = (
        df["close"]
        .ewm(
            span=50,
            adjust=False
        )
        .mean()
    )



    # RSI

    delta = df["close"].diff()


    gain = delta.where(
        delta > 0,
        0
    )


    loss = -delta.where(
        delta < 0,
        0
    )


    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()


    rs = avg_gain / avg_loss


    df["RSI"] = (
        100 -
        (100 / (1 + rs))
    )



    # MACD

    ema12 = (
        df["close"]
        .ewm(
            span=12,
            adjust=False
        )
        .mean()
    )


    ema26 = (
        df["close"]
        .ewm(
            span=26,
            adjust=False
        )
        .mean()
    )


    df["MACD"] = (
        ema12 - ema26
    )


    df["MACD_SIGNAL"] = (
        df["MACD"]
        .ewm(
            span=9,
            adjust=False
        )
        .mean()
    )



    # ATR

    df["TR"] = (
        df["high"]
        -
        df["low"]
    )


    df["ATR"] = (
        df["TR"]
        .rolling(14)
        .mean()
    )


    return df





def strong_trade_filter(ai_result):


    signal = ai_result["signal"]

    confidence = ai_result["confidence"]



    if signal == "WAIT":

        return False



    if confidence < 75:

        return False



    return True






def run_bot():

    global LAST_SIGNAL
    global LAST_TIME



    print(
        "Forex_mustfa_ai V4.1 Started"
    )



    while True:


        try:


            df = get_market_data()



            if df is None:


                print(
                    "No market data"
                )


                time.sleep(
                    CHECK_INTERVAL
                )


                continue




            df = calculate_indicators(df)




            ai_result = analyze_market(df)




            print(
                "SIGNAL:",
                ai_result["signal"],
                "CONF:",
                ai_result["confidence"]
            )




            if not strong_trade_filter(ai_result):


                print(
                    "Weak signal ignored"
                )


                time.sleep(
                    CHECK_INTERVAL
                )


                continue






            if LAST_SIGNAL == ai_result["signal"]:


                print(
                    "Duplicate signal ignored"
                )


                time.sleep(
                    CHECK_INTERVAL
                )


                continue






            last = df.iloc[-1]



            trade_data = calculate_trade(

                ai_result["price"],

                ai_result["signal"],

                float(last["ATR"]),

                ai_result.get(
                    "trade_type",
                    "NORMAL"
                )

            )






            message = build_signal_message(

                SYMBOL,

                ai_result,

                trade_data

            )






            send_telegram(message)





            LAST_SIGNAL = (
                ai_result["signal"]
            )


            LAST_TIME = (
                datetime.now()
            )





            print(message)




        except Exception as e:


            print(
                "BOT ERROR:",
                e
            )




        time.sleep(
            CHECK_INTERVAL
        )






if __name__ == "__main__":


    run_bot()
