# =====================================
# Forex_mustfa_ai V2
# RISK MANAGER
# =====================================

def calculate_trade(price, signal, atr):

    if signal == "BUY":

        entry = price
        stop_loss = price - (atr * 1.5)

        tp1 = price + (atr * 1.5)
        tp2 = price + (atr * 2)
        tp3 = price + (atr * 3)

    elif signal == "SELL":

        entry = price
        stop_loss = price + (atr * 1.5)

        tp1 = price - (atr * 1.5)
        tp2 = price - (atr * 2)
        tp3 = price - (atr * 3)

    else:

        return {
            "entry": "-",
            "stop_loss": "-",
            "tp1": "-",
            "tp2": "-",
            "tp3": "-",
            "expected_points": "-"
        }


    expected_points = abs(tp2 - entry) * 10000


    return {

        "entry": round(entry,5),

        "stop_loss": round(stop_loss,5),

        "tp1": round(tp1,5),

        "tp2": round(tp2,5),

        "tp3": round(tp3,5),

        "expected_points": round(expected_points,1)

    }
