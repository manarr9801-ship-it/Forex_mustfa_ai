# ==========================================
# Forex_mustfa_ai V4
# Main Configuration
# ==========================================


# ==========================
# Market Settings
# ==========================

SYMBOL = "EUR/USD"
INTERVAL = "1h"
OUTPUT_SIZE = 200


# ==========================
# API
# ==========================

TWELVE_DATA_API_KEY = "PUT_YOUR_API_KEY_HERE"


# ==========================
# Telegram
# ==========================

BOT_TOKEN = "PUT_YOUR_TELEGRAM_TOKEN_HERE"
CHAT_ID = "PUT_YOUR_CHAT_ID_HERE"


# ==========================
# Trading Mode
# ==========================

# False = تحليل وإشارات فقط
# True  = تنفيذ أوامر MT5

AUTO_TRADE = False


# ==========================
# MetaTrader 5
# ==========================

MT5_LOGIN = 0
MT5_PASSWORD = ""
MT5_SERVER = ""

MT5_SYMBOL = "EURUSD"


# ==========================
# Risk Management
# ==========================

RISK_PERCENT = 1

RISK_REWARD = 2


# ==========================
# AI Engine
# ==========================

CONFIDENCE_LIMIT = 70


# ==========================
# Strong Trade Filter
# ==========================

STRONG_TRADE_CONFIDENCE = 85


# ==========================
# Scanner
# ==========================

CHECK_INTERVAL = 3600


# ==========================
# Safety System
# ==========================

MAX_DAILY_TRADES = 3

ENABLE_LOGGING = True

AUTO_RESTART = True


# ==========================
# Notifications
# ==========================

SEND_ERROR_ALERT = True

SEND_START_ALERT = True
