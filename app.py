import streamlit as st
import os
import json
from werkzeug.utils import secure_filename

# Set page configuration
st.set_page_config(page_title="MediSoft", layout="wide")

# File to store user data persistently
USER_DATA_FILE = "users.json"

# Upload directory
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load users from JSON file
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users to JSON file
def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "users" not in st.session_state:
    st.session_state.users = load_users()  # Load users only once at start
if "page" not in st.session_state:
    st.session_state.page = "index"

# Function to handle login
def login():
    st.header("Login")

    with st.form("login_form"):
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            users = load_users()  # Reload users from file
            if user_id in users and users[user_id]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = user_id
                st.success("Login successful!")
                st.session_state.page = "index"
                st.rerun()
            else:
                st.error("Invalid credentials!")

# Function to handle account creation
def create_account():
    st.header("Create Account")

    with st.form("create_account_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        user_id = st.text_input("User ID")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        repassword = st.text_input("Confirm Password", type="password")
        mobile = st.text_input("Mobile Number")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        submit_button = st.form_submit_button("Create Account")

        if submit_button:
            if password != repassword:
                st.error("Passwords do not match!")
            else:
                users = load_users()  # Reload users from file
                if user_id in users:
                    st.error("User ID already exists!")
                else:
                    users[user_id] = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "password": password,  # In a real app, hash the password
                        "mobile": mobile,
                        "gender": gender,
                    }
                    save_users(users)  # Save updated users to file
                    st.success("Account created successfully! You can now log in.")
                    st.session_state.page = "login"
                    st.rerun()

# Function to handle the index (home) page
def index():
    st.title("Welcome to MediSoft")

    users = load_users()  # Ensure we are using the latest user data

    if st.session_state.logged_in and st.session_state.current_user in users:
        user = users[st.session_state.current_user]
        st.write(f"Welcome back, {user['first_name']}!")

        # Image upload section
        st.subheader("Upload Medical Image")
        upload_image()
    else:
        st.write("Please login or create an account to access all features.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="login_button"):
                st.session_state.page = "login"
                st.rerun()
        with col2:
            if st.button("Create Account", key="create_account_button"):
                st.session_state.page = "create_account"
                st.rerun()

# Function to handle image upload
def upload_image():
    st.header("Upload Image")
    
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Create a secure filename
        filename = secure_filename(uploaded_file.name)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Image uploaded successfully as {filename}!")
        # Display the image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

# Sidebar navigation
st.sidebar.title("Navigation")
if st.session_state.logged_in:
    if st.sidebar.button("Home", key="home_sidebar"):
        st.session_state.page = "index"
        st.rerun()
    if st.sidebar.button("Logout", key="logout_sidebar"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.page = "index"
        st.success("You have been logged out.")
        st.rerun()
else:
    if st.sidebar.button("Home", key="home_guest_sidebar"):
        st.session_state.page = "index"
        st.rerun()
    if st.sidebar.button("Login", key="login_sidebar"):
        st.session_state.page = "login"
        st.rerun()
    if st.sidebar.button("Create Account", key="create_account_sidebar"):
        st.session_state.page = "create_account"
        st.rerun()

# Load the appropriate page
if st.session_state.page == "index":
    index()
elif st.session_state.page == "login":
    login()
elif st.session_state.page == "create_account":
    create_account()
