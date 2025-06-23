
import streamlit as st
import pandas as pd
import os

def future_event_form():
    st.subheader("🎯 Future Events")
    with st.form("event_form"):
        date = st.date_input("Event Date")
        event = st.text_input("Event Name")
        last_sales = st.number_input("Last Year Sales", 0)
        last_customers = st.number_input("Last Year Customers", 0)
        submitted = st.form_submit_button("Add Event")
        if submitted:
            new = pd.DataFrame([[date, event, last_sales, last_customers]],
                               columns=["date", "event", "last_sales", "last_customers"])
            path = "data/future_events.csv"
            if os.path.exists(path):
                old = pd.read_csv(path)
                full = pd.concat([old, new])
            else:
                full = new
            full = full.drop_duplicates(subset=["date"]).sort_values("date")
            full.to_csv(path, index=False)
            st.success("Event saved.")

    if os.path.exists("data/future_events.csv"):
        df = pd.read_csv("data/future_events.csv")
        st.dataframe(df)
