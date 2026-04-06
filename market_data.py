import requests
import pandas as pd

def get_finnish_prices():
    url = "https://www.nordpoolgroup.com/api/marketdata/page/10?currency=EUR&area=FI"

    r = requests.get(url)
    data = r.json()

    rows = data["data"]["Rows"]

    prices = []
    for row in rows:
        try:
            price = float(row["Columns"][0]["Value"].replace(",", "."))
            prices.append(price)
        except:
            prices.append(None)

    df = pd.DataFrame({
        "price": prices
    })

    return df
