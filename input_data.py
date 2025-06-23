
import streamlit as st
import pandas as pd
import os

def manual_input_form():
    st.subheader("📝 Add Daily Record")
    with st.form("input_form"):
        date = st.date_input("Date")
        sales = st.number_input("Sales", 0)
        customers = st.number_input("Customers", 0)
        weather = st.slider("Weather Index (0 = bad, 10 = excellent)", 0, 10, 5)
        add_ons = st.number_input("Add-on Sales", 0)
        submitted = st.form_submit_button("Add Data")
        if submitted:
            new = pd.DataFrame([[date, sales, customers, weather, add_ons]],
                               columns=["date", "sales", "customers", "weather", "add_ons"])
            path = "data/historical_data.csv"
            if os.path.exists(path):
                old = pd.read_csv(path)
                full = pd.concat([old, new])
            else:
                full = new
            full = full.drop_duplicates(subset=["date"]).sort_values("date")
            full.to_csv(path, index=False)
            st.success("Data saved.")

    if os.path.exists("data/historical_data.csv"):
        df = pd.read_csv("data/historical_data.csv")
        st.dataframe(df)
