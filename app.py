
import streamlit as st
from utils.helper import load_data, save_data, delete_data, authenticate_user
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="McDo Smart Forecaster", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid credentials")
else:
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio("Go to", ["Forecast", "Add Data", "Future Events", "Database"])

    data = load_data("data/historical_data.csv")

    if page == "Forecast":
        st.title("📈 Sales and Customer Forecasting")
        if len(data) < 10:
            st.warning("Need at least 10 rows of data for forecasting.")
        else:
            # Forecast logic here (placeholder)
            forecast = data.tail(10).copy()
            forecast["date"] = pd.date_range(start=datetime.today(), periods=10)
            st.subheader("🔮 10-Day Forecast")
            st.dataframe(forecast)

            fig = px.line(forecast, x="date", y=["sales", "customers"], title="Forecast Graph")
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Add Data":
        st.title("➕ Add Historical Data")
        with st.form("data_form"):
            date = st.date_input("Date")
            sales = st.number_input("Sales", step=1)
            customers = st.number_input("Customers", step=1)
            weather = st.selectbox("Weather", ["Sunny", "Rainy", "Cloudy"])
            addon = st.number_input("Add-On Sales", step=1)
            submitted = st.form_submit_button("Add Data")
            if submitted:
                new_row = pd.DataFrame([{
                    "date": pd.to_datetime(date),
                    "sales": sales,
                    "customers": customers,
                    "weather": weather,
                    "add_on_sales": addon
                }])
                data = pd.concat([data, new_row], ignore_index=True)
                save_data(data, "data/historical_data.csv")
                st.success("Data saved.")

    elif page == "Future Events":
        st.title("📅 Input Future Events")
        event_data = load_data("data/future_events.csv")
        with st.form("event_form"):
            event_date = st.date_input("Event Date")
            event_name = st.text_input("Event Name")
            last_year_sales = st.number_input("Sales Last Year", step=1)
            last_year_customers = st.number_input("Customers Last Year", step=1)
            submitted = st.form_submit_button("Add Event")
            if submitted:
                new_row = pd.DataFrame([{
                    "event_date": pd.to_datetime(event_date),
                    "event": event_name,
                    "sales_last_year": last_year_sales,
                    "customers_last_year": last_year_customers
                }])
                event_data = pd.concat([event_data, new_row], ignore_index=True)
                save_data(event_data, "data/future_events.csv")
                st.success("Event saved.")

    elif page == "Database":
        st.title("📂 Manage Data")
        st.subheader("Historical Data")
        st.dataframe(data)
        if st.button("Clear Historical Data"):
            delete_data("data/historical_data.csv")
            st.success("Historical data cleared.")

        st.subheader("Future Events")
        future_data = load_data("data/future_events.csv")
        st.dataframe(future_data)
        if st.button("Clear Future Events"):
            delete_data("data/future_events.csv")
            st.success("Future events cleared.")
