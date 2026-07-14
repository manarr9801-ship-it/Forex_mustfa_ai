# =====================================
# Forex_mustfa_ai V3
# AI ENGINE
# =====================================

from config import CONFIDENCE_LIMIT


def analyze_market(df):

    last = df.iloc[-1]

    buy_score = 0
    sell_score = 0

    reasons = []


    # =========================
    # TREND ANALYSIS
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
    # RSI FILTER
    # =========================

    rsi = last["RSI"]


    if 55 < rsi < 70:

        buy_score += 20
        reasons.append("RSI supports buyers")


    elif 30 < rsi < 45:

        sell_score += 20
        reasons.append("RSI supports sellers")


    elif rsi >= 70:

        reasons.append("RSI overbought - caution")


    elif rsi <= 30:

        reasons.append("RSI oversold - caution")


    # =========================
    # ATR MARKET POWER
    # =========================

    atr = last["ATR"]

    if atr > 0:

        buy_score += 10
        sell_score += 10

        reasons.append("ATR confirms volatility")


    # =========================
    # CONFIDENCE
    # =========================

    confidence = max(
        buy_score,
        sell_score
    )


    # =========================
    # FINAL DECISION
    # =========================

    if buy_score >= CONFIDENCE_LIMIT:

        signal = "BUY"


    elif sell_score >= CONFIDENCE_LIMIT:

        signal = "SELL"


    else:

        signal = "WAIT"


    return {

        "signal": signal,

        "confidence": confidence,

        "reasons": reasons,

        "price": float(last["close"]),

        "atr": float(last["ATR"])

    }
