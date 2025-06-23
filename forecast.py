
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import numpy as np

def run_forecast():
    df = pd.read_csv("data/historical_data.csv", parse_dates=["date"])
    df = df.sort_values("date")

    if len(df) < 10:
        return pd.DataFrame(), plt.figure()

    df["dayofweek"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month

    # Convert weather to dummy vars
    weather_encoded = pd.get_dummies(df["weather"], prefix="weather")
    df = pd.concat([df, weather_encoded], axis=1)

    X = df[["customers", "add_on_sales", "dayofweek", "month"] + list(weather_encoded.columns)]
    y = df["sales"]

    model = LinearRegression().fit(X, y)

    # Forecast
    future_dates = pd.date_range(df["date"].max() + timedelta(days=1), periods=10)
    forecast = []
    for d in future_dates:
        dow = d.dayofweek
        mon = d.month
        avg_cust = int(df["customers"].tail(7).mean())
        avg_addon = int(df["add_on_sales"].tail(7).mean())
        weather_cols = {col: 0 for col in weather_encoded.columns}
        weather_cols["weather_Sunny"] = 1  # assume sunny for simplicity
        x_row = [avg_cust, avg_addon, dow, mon] + list(weather_cols.values())
        sales_pred = model.predict([x_row])[0]
        forecast.append({
            "date": d.strftime("%Y-%m-%d"),
            "forecasted_sales": round(sales_pred),
            "expected_customers": avg_cust
        })

    forecast_df = pd.DataFrame(forecast)

    fig, ax = plt.subplots()
    ax.plot(df["date"], df["sales"], label="Historical Sales")
    ax.plot(pd.to_datetime(forecast_df["date"]), forecast_df["forecasted_sales"], label="Forecast", linestyle="--")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    return forecast_df, fig
