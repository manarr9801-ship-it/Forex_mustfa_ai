# =====================================
# Forex_mustfa_ai V5
# TELEGRAM BOT + COMMANDS
# =====================================

import requests
import time

from config import BOT_TOKEN, CHAT_ID

from telegram_commands import handle_command



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





def get_updates(offset=None):

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/getUpdates"
    )


    params = {
        "timeout": 30
    }


    if offset:

        params["offset"] = offset



    try:

        response = requests.get(
            url,
            params=params,
            timeout=35
        )

        return response.json()


    except Exception:

        return {}





def listen_commands():


    offset = None


    while True:


        updates = get_updates(offset)


        if "result" in updates:


            for update in updates["result"]:


                offset = (
                    update["update_id"] + 1
                )


                try:


                    message = update["message"]

                    text = (
                        message
                        .get("text","")
                    )


                    chat_id = (
                        message["chat"]["id"]
                    )



                    if str(chat_id) != str(CHAT_ID):

                        continue



                    reply = handle_command(text)



                    send_telegram(reply)



                except Exception as e:


                    print(
                        "COMMAND ERROR:",
                        e
                    )



        time.sleep(2)





def build_signal_message(
        symbol,
        ai_result,
        trade_data
):


    message = f"""
🧠 *Forex_mustfa_ai V5*

💱 الزوج:
{symbol}


📢 القرار:
*{ai_result.get('signal')}*


🎯 الثقة:
{ai_result.get('confidence')}%


📊 النوع:
{ai_result.get('trade_type','NORMAL')}


💰 الدخول:
{trade_data.get('entry','-')}


🛑 SL:
{trade_data.get('stop_loss','-')}


🎯 TP1:
{trade_data.get('tp1','-')}


🎯 TP2:
{trade_data.get('tp2','-')}


🎯 TP3:
{trade_data.get('tp3','-')}


📈 Expected Pips:
{trade_data.get('expected_points','-')}


⚖️ Risk Reward:
{trade_data.get('risk_reward','-')}


📏 ATR:
{trade_data.get('atr','-')}


🧠 الأسباب:
"""


    for reason in ai_result.get(
        "reasons",
        []
    ):

        message += (
            f"\n• {reason}"
        )



    message += """

🤖 Auto Trade: OFF

⚠️ Analysis Only
"""


    return message
