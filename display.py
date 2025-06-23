
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

def display_forecast_graph():
    if not os.path.exists("data/forecast.csv"):
        st.warning("Generate forecast first.")
        return
    df = pd.read_csv("data/forecast.csv")
    plt.figure(figsize=(10,4))
    plt.plot(df["date"], df["forecast_sales"], marker='o', color='red', label='Forecast Sales')
    plt.xticks(rotation=45)
    plt.title("📈 10-Day Sales Forecast")
    plt.legend()
    st.pyplot(plt)

def download_csv():
    if os.path.exists("data/forecast.csv"):
        with open("data/forecast.csv", "rb") as f:
            st.download_button("⬇️ Download Forecast", f, file_name="forecast.csv")
