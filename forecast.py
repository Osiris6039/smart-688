
import pandas as pd
import streamlit as st
import xgboost as xgb
from sklearn.model_selection import train_test_split
import os

def forecast_10_days():
    if not os.path.exists("data/historical_data.csv"):
        st.warning("No data found. Please add input data.")
        return
    df = pd.read_csv("data/historical_data.csv")
    if len(df) < 14:
        st.warning("Please input at least 14 days of data.")
        return

    df = df.sort_values("date")
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.dayofweek
    df["add_on_ratio"] = df["add_ons"] / df["sales"]

    X = df[["customers", "weather", "day", "add_on_ratio"]]
    y_sales = df["sales"]
    model_sales = xgb.XGBRegressor()
    model_sales.fit(X, y_sales)

    last_date = df["date"].max()
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=10)
    forecast_df = pd.DataFrame({
        "date": forecast_dates,
        "customers": df["customers"].mean(),
        "weather": df["weather"].mean(),
        "day": forecast_dates.dayofweek,
        "add_on_ratio": 0
    })

    predictions = model_sales.predict(forecast_df[["customers", "weather", "day", "add_on_ratio"]])
    forecast_df["forecast_sales"] = predictions.astype(int)
    forecast_df.to_csv("data/forecast.csv", index=False)
    st.success("📊 Forecast generated!")
    st.dataframe(forecast_df)
