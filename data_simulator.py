import pandas as pd
import numpy as np


def generate_data(hours=24):
    t = range(hours)

    solar = [max(0, 10 * np.sin((i - 6) / 24 * 2 * np.pi)) for i in t]
    load = [5 + np.random.rand() * 2 for _ in t]
    price = [30 + 40 * np.sin((i - 15) / 24 * 2 * np.pi) for i in t]

    return pd.DataFrame({
        "solar": solar,
        "load": load,
        "price": price
    })
