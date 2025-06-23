
import pandas as pd
import os

def load_data():
    if os.path.exists("data/historical_data.csv"):
        df = pd.read_csv("data/historical_data.csv", parse_dates=['date'])
    else:
        df = pd.DataFrame(columns=['date', 'sales', 'customers', 'weather', 'add_ons'])

    if os.path.exists("data/future_events.csv"):
        events = pd.read_csv("data/future_events.csv", parse_dates=['event_date'])
    else:
        events = pd.DataFrame(columns=['event_date', 'event_name', 'sales_last_year', 'customers_last_year'])

    return df, events

def save_data(new_row):
    df, _ = load_data()
    df = df.append(new_row, ignore_index=True)
    df = df.sort_values(by="date")
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/historical_data.csv", index=False)
    return "✅ Data added successfully!"

def delete_data():
    try:
        df = pd.read_csv("data/historical_data.csv")
        df = df[:-1]
        df.to_csv("data/historical_data.csv", index=False)
        return "🗑️ Latest entry removed."
    except:
        return "⚠️ Nothing to delete."
