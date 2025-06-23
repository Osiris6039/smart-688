
import streamlit as st

def login():
    st.sidebar.subheader("🔐 Login")
    password = st.sidebar.text_input("Enter password", type="password")
    if password == "mcdo123":
        return True
    elif password != "":
        st.sidebar.error("Wrong password.")
    return False
