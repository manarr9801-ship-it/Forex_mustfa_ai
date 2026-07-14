# =====================================
# Forex_mustfa_ai V4
# RISK MANAGER
# =====================================


def calculate_trade(price, signal, atr, trade_type="NORMAL"):


    # لا توجد صفقة

    if signal not in ["BUY", "SELL"]:

        return {

            "entry": "-",
            "stop_loss": "-",
            "tp1": "-",
            "tp2": "-",
            "tp3": "-",
            "expected_points": "-",
            "risk_reward": "-",
            "atr": round(atr,5)

        }



    # =========================
    # ATR MANAGEMENT V4
    # =========================


    if trade_type == "STRONG":

        sl_multiplier = 1.8

        tp1_multiplier = 2

        tp2_multiplier = 3

        tp3_multiplier = 5


    else:

        sl_multiplier = 1.5

        tp1_multiplier = 1.5

        tp2_multiplier = 2.5

        tp3_multiplier = 3.5



    sl_distance = atr * sl_multiplier

    tp1_distance = atr * tp1_multiplier

    tp2_distance = atr * tp2_multiplier

    tp3_distance = atr * tp3_multiplier



    # =========================
    # BUY
    # =========================

    if signal == "BUY":


        entry = price

        stop_loss = price - sl_distance

        tp1 = price + tp1_distance

        tp2 = price + tp2_distance

        tp3 = price + tp3_distance



    # =========================
    # SELL
    # =========================

    else:


        entry = price

        stop_loss = price + sl_distance

        tp1 = price - tp1_distance

        tp2 = price - tp2_distance

        tp3 = price - tp3_distance




    # =========================
    # PERFORMANCE
    # =========================


    risk = abs(entry - stop_loss)

    reward = abs(tp2 - entry)


    risk_reward = round(
        reward / risk,
        2
    )


    expected_points = round(
        reward * 10000,
        1
    )



    return {


        "entry": round(entry,5),

        "stop_loss": round(stop_loss,5),

        "tp1": round(tp1,5),

        "tp2": round(tp2,5),

        "tp3": round(tp3,5),

        "expected_points": expected_points,

        "risk_reward": risk_reward,

        "atr": round(atr,5),

        "trade_type": trade_type

    }
