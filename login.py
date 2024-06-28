import streamlit as st
import requests

API_URL = "http://localhost:8000"  # URL of your FastAPI app

st.title("Police Management System")

# Function to validate the user
def validate_user(username, password, role):
    response = requests.post(
        f"{API_URL}/validate_user/",
        json={"username": username, "password": password, "role": role},
    )
    return response.json()

# Function to handle login redirection
def login_redirect():
    st.session_state['logged_in'] = True

# Login form
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Police Station", "Police Officer"])
    login_button = st.button("Login")

    if login_button:
        if username and password:
            result = validate_user(username, password, role.lower())
            if result.get("valid"):
                st.success("Login successful")
                login_redirect()  # Set session state to logged in
                st.experimental_set_query_params(page="app")  # Set the query param for redirection
                st.experimental_rerun()  # This will refresh the app to show the main content
            else:
                st.error("Invalid username or password")
        else:
            st.error("Please enter both username and password")
