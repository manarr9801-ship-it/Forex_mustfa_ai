# =====================================
# Forex_mustfa_ai V4
# TELEGRAM BOT
# =====================================

import requests

from config import BOT_TOKEN, CHAT_ID



def send_telegram(message):

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )


    data = {

        "chat_id": CHAT_ID,

        "text": message,

        "parse_mode": "Markdown"

    }


    try:

        response = requests.post(

            url,

            data=data,

            timeout=20

        )


        return response.json()


    except Exception as e:


        return {

            "error": str(e)

        }




def build_signal_message(
        symbol,
        ai_result,
        trade_data
):


    confidence = ai_result.get(
        "confidence",
        0
    )


    if confidence >= 85:

        strength = "🔥 STRONG TRADE"

    else:

        strength = "⚡ NORMAL TRADE"



    message = f"""

🧠 *Forex_mustfa_ai V4*

{strength}


💱 الزوج:
{symbol}


📢 القرار:
*{ai_result.get('signal','WAIT')}*


🎯 الثقة:
{confidence}%


📊 نوع الصفقة:
{trade_data.get('trade_type','NORMAL')}



💰 الدخول:
{trade_data.get('entry','-')}


🛑 وقف الخسارة:
{trade_data.get('stop_loss','-')}



🎯 TP1:
{trade_data.get('tp1','-')}


🎯 TP2:
{trade_data.get('tp2','-')}


🎯 TP3:
{trade_data.get('tp3','-')}



📈 النقاط المتوقعة:
{trade_data.get('expected_points','-')}


⚖️ Risk Reward:
{trade_data.get('risk_reward','-')}



📏 ATR:
{trade_data.get('atr','-')}



🧠 الأسباب:
"""


    for reason in ai_result.get("reasons", []):

        message += f"\n• {reason}"



    message += """



🤖 Auto Trade: OFF

⚠️ تحليل فقط وليس تنفيذ أوامر

"""


    return message
