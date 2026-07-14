# =====================================
# Forex_mustfa_ai V4
# AI ENGINE
# =====================================

from config import CONFIDENCE_LIMIT


def analyze_market(df):

    last = df.iloc[-1]

    buy_score = 0
    sell_score = 0

    reasons = []


    # =========================
    # TREND
    # =========================

    if last["EMA20"] > last["EMA50"]:

        buy_score += 30
        reasons.append("EMA trend bullish")

    else:

        sell_score += 30
        reasons.append("EMA trend bearish")



    # =========================
    # MACD MOMENTUM
    # =========================

    if last["MACD"] > last["MACD_SIGNAL"]:

        buy_score += 25
        reasons.append("MACD bullish momentum")

    else:

        sell_score += 25
        reasons.append("MACD bearish momentum")



    # =========================
    # RSI INTELLIGENCE
    # =========================

    rsi = last["RSI"]


    if 55 <= rsi < 70:

        buy_score += 15
        reasons.append("RSI buyer strength")


    elif 30 < rsi <= 45:

        sell_score += 15
        reasons.append("RSI seller strength")


    elif rsi >= 70:

        sell_score -= 10
        reasons.append("RSI overbought")


    elif rsi <= 30:

        buy_score -= 10
        reasons.append("RSI oversold")



    # =========================
    # ATR MARKET POWER
    # =========================

    atr = float(last["ATR"])


    if atr > 0:

        buy_score += 10
        sell_score += 10

        reasons.append(
            "ATR confirms volatility"
        )



    # =========================
    # MARKET PRESSURE
    # =========================

    candle_power = (
        last["close"] -
        last["open"]
    )


    if candle_power > 0:

        buy_score += 10

        reasons.append(
            "Buyer pressure detected"
        )


    else:

        sell_score += 10

        reasons.append(
            "Seller pressure detected"
        )



    # =========================
    # FINAL SCORE
    # =========================

    confidence = max(
        buy_score,
        sell_score
    )


    if buy_score >= CONFIDENCE_LIMIT:

        signal = "BUY"


    elif sell_score >= CONFIDENCE_LIMIT:

        signal = "SELL"


    else:

        signal = "WAIT"



    # =========================
    # TRADE TYPE
    # =========================

    if confidence >= 85:

        trade_type = "STRONG"


    elif confidence >= 75:

        trade_type = "NORMAL"


    else:

        trade_type = "WAIT"



    return {

        "signal": signal,

        "confidence": confidence,

        "trade_type": trade_type,

        "reasons": reasons,

        "price": float(last["close"]),

        "atr": atr

    }
