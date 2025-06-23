
import streamlit as st
import pandas as pd
from model import train_model, forecast_sales
from utils import load_data, save_data, delete_data, authenticate_user
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Smart AI McDo Forecaster", layout="wide", page_icon="🍟")

# Simple login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter Manager Password:", type="password")
    if password == "mcdo2025":
        st.session_state.authenticated = True
        st.experimental_rerun()
    else:
        st.stop()

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Forecast", "🗂 Add Daily Data", "📅 Future Events"])

with tab1:
    st.title("📊 10-Day Sales & Customer Forecast")
    df, events = load_data()
    if len(df) > 10:
        model = train_model(df, events)
        forecast_df = forecast_sales(model, df, events)
        st.success("Forecast Generated Based on Latest Data")

        st.dataframe(forecast_df, use_container_width=True)

        # Plot forecast
        fig = px.line(forecast_df, x='date', y='sales', title='📈 Forecasted Sales', markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # Download
        st.download_button("⬇️ Download Forecast CSV", forecast_df.to_csv(index=False), "forecast.csv")
    else:
        st.warning("⚠️ Add at least 10 days of data to generate forecast.")

with tab2:
    st.title("📋 Add Daily Sales Data")
    with st.form("daily_data_form"):
        date = st.date_input("Date")
        sales = st.number_input("Sales", step=1)
        customers = st.number_input("Customers", step=1)
        weather = st.selectbox("Weather", ["Sunny", "Rainy", "Cloudy", "Stormy"])
        add_on = st.number_input("Add-On Sales", step=1)
        submit = st.form_submit_button("➕ Add Data")

        if submit:
            new_data = {"date": date, "sales": sales, "customers": customers, "weather": weather, "add_ons": add_on}
            msg = save_data(new_data)
            st.success(msg)

    if st.button("🗑 Clear Latest Entry"):
        msg = delete_data()
        st.warning(msg)

with tab3:
    st.title("🎯 Add Future Events")
    with st.form("future_event_form"):
        event_date = st.date_input("Event Date", key="event")
        event_name = st.text_input("Event Name (e.g. Charter Day)")
        past_sales = st.number_input("Sales Last Year", step=1, key="event_sales")
        past_customers = st.number_input("Customers Last Year", step=1, key="event_customers")
        add = st.form_submit_button("➕ Add Event")

        if add:
            event = {"event_date": event_date, "event_name": event_name, "sales_last_year": past_sales, "customers_last_year": past_customers}
            df_event = pd.read_csv("data/future_events.csv") if os.path.exists("data/future_events.csv") else pd.DataFrame()
            df_event = df_event.append(event, ignore_index=True)
            df_event.to_csv("data/future_events.csv", index=False)
            st.success("✅ Event Added Successfully")

    st.subheader("📅 Saved Events")
    if os.path.exists("data/future_events.csv"):
        st.dataframe(pd.read_csv("data/future_events.csv"), use_container_width=True)
