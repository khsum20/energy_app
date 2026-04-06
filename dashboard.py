import streamlit as st
from data_simulator import generate_data
from optimizer import optimize

st.title("Energy Optimizer")

df = generate_data(24)
result = optimize(df)

st.subheader("Solar and Load")
st.line_chart(result[["solar", "load"]])

st.subheader("Battery State of Charge")
st.line_chart(result["soc"])

st.subheader("Battery Actions")
st.line_chart(result[["charge", "discharge"]])

st.subheader("Grid")
st.line_chart(result[["grid_import", "grid_export"]])

st.subheader("Optimized Data")
st.dataframe(result)
