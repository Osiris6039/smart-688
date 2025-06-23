
import pandas as pd
import os

def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=True)
    else:
        return pd.DataFrame()

def save_data(df, path):
    df.to_csv(path, index=False)

def delete_data(path):
    if os.path.exists(path):
        os.remove(path)

def authenticate_user(username, password):
    return username == "admin" and password == "mcdo2025"
