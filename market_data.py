# =====================================
# Forex_mustfa_ai V2
# MARKET DATA
# =====================================

import requests

from config import (
    SYMBOL,
    INTERVAL,
    OUTPUT_SIZE,
    API_KEY
)


def get_market_data():

    url = (
        "https://api.twelvedata.com/time_series"
        f"?symbol={SYMBOL}"
        f"&interval={INTERVAL}"
        f"&outputsize={OUTPUT_SIZE}"
        f"&apikey={API_KEY}"
    )


    try:

        response = requests.get(
            url,
            timeout=20
        )

        data = response.json()


        if "values" not in data:
            print(data)
            return None


        import pandas as pd


        df = pd.DataFrame(
            data["values"]
        )


        df = df.iloc[::-1].reset_index(drop=True)


        for col in [
            "open",
            "high",
            "low",
            "close"
        ]:
            df[col] = df[col].astype(float)


        return df


    except Exception as e:

        print("Market Data Error:", e)

        return None
