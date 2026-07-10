# =====================================
# Forex_mustfa_ai V2
# RISK MANAGER
# =====================================

def calculate_trade_levels(signal_data):

    signal = signal_data["signal"]
    entry = signal_data["price"]

    stop_distance = 0.0020


    if signal == "BUY":

        stop_loss = entry - stop_distance

        tp1 = entry + stop_distance
        tp2 = entry + (stop_distance * 2)
        tp3 = entry + (stop_distance * 3)


    elif signal == "SELL":

        stop_loss = entry + stop_distance

        tp1 = entry - stop_distance
        tp2 = entry - (stop_distance * 2)
        tp3 = entry - (stop_distance * 3)


    else:

        return {
            "signal": "WAIT",
            "entry": entry
        }


    expected_points = abs(tp2 - entry) * 10000


    return {

        "signal": signal,

        "entry": round(entry, 5),

        "stop_loss": round(stop_loss, 5),

        "tp1": round(tp1, 5),

        "tp2": round(tp2, 5),

        "tp3": round(tp3, 5),

        "expected_points": round(expected_points, 1)

    }
