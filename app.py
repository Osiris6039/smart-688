
import streamlit as st
from utils.auth import login
from utils.forecast import forecast_10_days
from utils.input_data import manual_input_form
from utils.events import future_event_form
from utils.display import display_forecast_graph, download_csv

# Secure login
if not login():
    st.stop()

st.title("🍟 McDo AI Sales & Customer Forecaster")
menu = ["📈 Forecast", "📝 Input Data", "🎯 Future Events"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "📈 Forecast":
    forecast_10_days()
    display_forecast_graph()
    download_csv()

elif choice == "📝 Input Data":
    manual_input_form()

elif choice == "🎯 Future Events":
    future_event_form()
