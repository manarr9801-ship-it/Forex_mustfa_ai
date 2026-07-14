# =====================================
# Forex_mustfa_ai V5
# TELEGRAM COMMANDS
# =====================================

import time


AUTO_TRADE = False



def handle_command(command):

    global AUTO_TRADE


    command = command.lower().strip()



    # حالة النظام

    if command == "/status":

        return """
🧠 Forex_mustfa_ai V5

🟢 Bot Status:
ONLINE

🤖 Auto Trade:
{}
""".format(
            "ON" if AUTO_TRADE else "OFF"
        )



    # تشغيل التداول

    elif command == "/trade_on":

        AUTO_TRADE = True


        return """
⚠️ Auto Trade Activated

Mode:
LIVE CONTROL

Please verify settings.
"""



    # إيقاف التداول

    elif command == "/trade_off":

        AUTO_TRADE = False


        return """
🛑 Auto Trade Disabled

Analysis Only Mode
"""



    # معلومات

    elif command == "/help":

        return """
📌 Forex_mustfa_ai Commands

/status
System status

/trade_on
Enable trading mode

/trade_off
Disable trading mode

/help
Show commands
"""



    else:


        return """
❌ Unknown command

Use:
/help
"""



def get_trade_status():

    return AUTO_TRADE
