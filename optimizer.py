import pulp
import pandas as pd


def optimize(df: pd.DataFrame) -> pd.DataFrame:
    n = len(df)
    T = range(n)

    model = pulp.LpProblem("EnergyOptimization", pulp.LpMaximize)

    charge = pulp.LpVariable.dicts("charge", T, lowBound=0, upBound=2)
    discharge = pulp.LpVariable.dicts("discharge", T, lowBound=0, upBound=2)
    grid_import = pulp.LpVariable.dicts("grid_import", T, lowBound=0)
    grid_export = pulp.LpVariable.dicts("grid_export", T, lowBound=0)
    soc = pulp.LpVariable.dicts("soc", T, lowBound=0, upBound=10)

    model += pulp.lpSum(
        df.iloc[t]["price"] * grid_export[t] - df.iloc[t]["price"] * grid_import[t]
        for t in T
    )

    for t in T:
        if t == 0:
            model += soc[t] == 5 + charge[t] - discharge[t]
        else:
            model += soc[t] == soc[t - 1] + charge[t] - discharge[t]

        model += (
            df.iloc[t]["solar"] + grid_import[t] + discharge[t]
            == df.iloc[t]["load"] + charge[t] + grid_export[t]
        )

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    result = df.copy()
    result["charge"] = [charge[t].value() for t in T]
    result["discharge"] = [discharge[t].value() for t in T]
    result["grid_import"] = [grid_import[t].value() for t in T]
    result["grid_export"] = [grid_export[t].value() for t in T]
    result["soc"] = [soc[t].value() for t in T]

    result["profit"] = (
        result["price"] * result["grid_export"]
        - result["price"] * result["grid_import"]
    )

    return result
