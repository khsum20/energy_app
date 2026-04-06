import os
import pandas as pd
from entsoe import EntsoePandasClient


def get_finnish_prices():
    api_key = os.getenv("ENTSOE_API_KEY")
    if not api_key:
        raise ValueError("ENTSOE_API_KEY is missing")

    client = EntsoePandasClient(api_key=api_key)

    start = pd.Timestamp.now(tz="Europe/Helsinki").normalize()
    end = start + pd.Timedelta(days=1)

    prices = client.query_day_ahead_prices("FI", start=start, end=end)

    # Convert Series -> DataFrame and align column name with your optimizer
    df = prices.reset_index()
    df.columns = ["time", "price"]

    return df[["price"]]
