# =====================================
# Forex_mustfa_ai V2
# AI ENGINE
# =====================================

from config import CONFIDENCE_LIMIT


def analyze_market(df):

    last = df.iloc[-1]

    buy_score = 0
    sell_score = 0

    reasons = []

    if last["EMA20"] > last["EMA50"]:
        buy_score += 25
        reasons.append("EMA trend bullish")
    else:
        sell_score += 25
        reasons.append("EMA trend bearish")


    if last["MACD"] > last["MACD_SIGNAL"]:
        buy_score += 25
        reasons.append("MACD positive")
    else:
        sell_score += 25
        reasons.append("MACD negative")


    if last["RSI"] > 55:
        buy_score += 20
        reasons.append("RSI supports buyers")

    elif last["RSI"] < 45:
        sell_score += 20
        reasons.append("RSI supports sellers")


    # ATR
    atr_value = float(last["ATR"]) if "ATR" in df.columns else 0


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

return {
    "signal": signal,
    "confidence": confidence,
    "reasons": reasons,
    "price": float(last["close"]),
    "atr": float(last["ATR"])
}
 
