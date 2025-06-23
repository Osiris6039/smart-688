
import pandas as pd
import os

def load_data():
    if not os.path.exists("data/historical_data.csv"):
        return pd.DataFrame(columns=["date", "sales", "customers", "weather", "add_on_sales"])
    return pd.read_csv("data/historical_data.csv", parse_dates=["date"]).sort_values("date")

def save_data(date, sales, customers, weather, add_on_sales):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([{
        "date": pd.to_datetime(date),
        "sales": sales,
        "customers": customers,
        "weather": weather,
        "add_on_sales": add_on_sales
    }])], ignore_index=True)
    df.sort_values("date").to_csv("data/historical_data.csv", index=False)

def delete_data(row_index):
    df = load_data()
    if row_index < len(df):
        df = df.drop(df.index[int(row_index)]).reset_index(drop=True)
        df.to_csv("data/historical_data.csv", index=False)

def authenticate_user(username, password):
    return username == "admin" and password == "mcdo2025"
