# signup.py

import streamlit as st

def sign_up(user_db):
    """Handle user signup."""
    st.header("Sign Up")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Sign Up"):
        if username in user_db:
            st.error("Username already exists. Please choose a different one.")
        else:
            user_db[username] = password
            st.success("User created successfully! You can now log in.")