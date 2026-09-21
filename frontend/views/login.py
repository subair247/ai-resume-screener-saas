import streamlit as st
from frontend.utils.api_client import login_user, register_user

def render():
    st.title("Authentication Portal")
    choice = st.selectbox("Choose Action", ["Login", "Register"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if choice == "Login":
        if st.button("Login"):
            res = login_user(email, password)
            if res.status_code == 200:
                st.session_state["token"] = res.json()["access_token"]
                st.session_state["logged_in"] = True
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        if st.button("Register"):
            res = register_user(email, password)
            if res.status_code == 200:
                st.success("Account created successfully. Please login.")
            else:
                st.error("Registration failed")