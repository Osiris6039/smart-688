
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import numpy as np
from datetime import timedelta

def train_model(data, events):
    data = data.copy()
    data['date'] = pd.to_datetime(data['date'])
    data['day_of_week'] = data['date'].dt.dayofweek
    data['is_weekend'] = data['day_of_week'].isin([5, 6]).astype(int)
    data['month'] = data['date'].dt.month

    if events is not None:
        events['event_date'] = pd.to_datetime(events['event_date'])
        data = pd.merge(data, events, left_on='date', right_on='event_date', how='left')
        data['event_name'] = data['event_name'].fillna("None")

    features = ['customers', 'weather', 'add_ons', 'is_weekend', 'month', 'event_name']
    X = data[features]
    y = data['sales']

    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['weather', 'event_name']),
        ('num', SimpleImputer(strategy='mean'), ['customers', 'add_ons', 'is_weekend', 'month'])
    ])

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', GradientBoostingRegressor(n_estimators=200))
    ])

    model.fit(X, y)
    return model

def forecast_sales(model, df, events):
    last_date = pd.to_datetime(df['date'].max())
    forecast_data = []

    for i in range(1, 11):
        future_date = last_date + timedelta(days=i)
        dow = future_date.dayofweek
        is_weekend = 1 if dow in [5, 6] else 0
        month = future_date.month

        match_event = events[events['event_date'] == future_date] if events is not None else pd.DataFrame()
        event = match_event.iloc[0] if not match_event.empty else {'event_name': "None", 'sales_last_year': 0, 'customers_last_year': 0}

        forecast_data.append({
            'date': future_date,
            'customers': event['customers_last_year'],
            'weather': 'Sunny',
            'add_ons': 0,
            'is_weekend': is_weekend,
            'month': month,
            'event_name': event['event_name']
        })

    forecast_df = pd.DataFrame(forecast_data)
    forecast_df['sales'] = model.predict(forecast_df.drop(columns='date'))
    return forecast_df[['date', 'sales']]
