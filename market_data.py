import os
import pandas as pd
import streamlit as st

try:
    from entsoe import EntsoePandasClient
except ModuleNotFoundError:
    EntsoePandasClient = None


def get_finnish_prices():
    fallback = pd.DataFrame({
        "time": pd.date_range(
            start=pd.Timestamp.now(tz="Europe/Helsinki").normalize(),
            periods=24,
            freq="h"
        ),
        "price": [50.0] * 24
    })

    if EntsoePandasClient is None:
        return fallback

    api_key = st.secrets.get("ENTSOE_API_KEY", os.getenv("ENTSOE_API_KEY"))
    if not api_key:
        return fallback

    try:
        client = EntsoePandasClient(api_key=api_key)

        start = pd.Timestamp.now(tz="Europe/Helsinki").normalize()
        end = start + pd.Timedelta(days=1)

        prices = client.query_day_ahead_prices("FI", start=start, end=end)

        df = prices.reset_index()
        df.columns = ["time", "price"]
        return df[["time", "price"]]
    except Exception:
        return fallback
