import streamlit as st

def login(user_db):
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email in user_db and user_db[email] == password:
            st.success("Login Successful")
        else:
            st.error("Invalid login credentials.")
