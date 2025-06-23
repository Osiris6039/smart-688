
import streamlit as st
import pandas as pd
from utils import load_data, save_data, delete_data, authenticate_user
from forecast import run_forecast

st.set_page_config(page_title="McDo AI Forecaster", layout="wide")

# Login section
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

# Main app
st.title("🍟 McDo AI Sales & Customer Forecasting")

tab1, tab2, tab3 = st.tabs(["📊 Forecast", "📥 Data Entry", "📅 Future Events"])

with tab1:
    forecast_df, fig = run_forecast()
    st.subheader("📈 10-Day Forecast")
    st.dataframe(forecast_df)
    st.pyplot(fig)
    st.download_button("⬇️ Download Forecast CSV", forecast_df.to_csv(index=False), "forecast.csv", "text/csv")

with tab2:
    st.subheader("📥 Add Daily Data")
    sales = st.number_input("Sales", step=1000)
    customers = st.number_input("Customers", step=1)
    date = st.date_input("Date")
    weather = st.selectbox("Weather", ["Sunny", "Rainy", "Cloudy"])
    addon_sales = st.number_input("Add-On Sales (optional)", step=1)
    if st.button("Add Data"):
        save_data(date, sales, customers, weather, addon_sales)
        st.success("Data added successfully!")

    st.divider()
    df = load_data()
    st.dataframe(df)
    if st.checkbox("🗑️ Enable Delete Mode"):
        row_to_delete = st.number_input("Row # to delete", step=1)
        if st.button("Delete Row"):
            delete_data(row_to_delete)
            st.success("Deleted!")

with tab3:
    st.subheader("📅 Add Future Event Reference")
    f_date = st.date_input("Future Event Date")
    event_name = st.text_input("Event Name")
    last_year_sales = st.number_input("Last Year Sales on This Event", step=1000)
    last_year_customers = st.number_input("Last Year Customers on This Event", step=1)
    if st.button("Add Event"):
        df = pd.read_csv("data/future_events.csv")
        df = pd.concat([df, pd.DataFrame([{
            "event_date": f_date,
            "event_name": event_name,
            "sales_last_year": last_year_sales,
            "customers_last_year": last_year_customers
        }])], ignore_index=True)
        df.sort_values("event_date").to_csv("data/future_events.csv", index=False)
        st.success("Future event added!")
