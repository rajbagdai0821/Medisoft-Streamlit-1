import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta
import json
import hashlib
import os
from werkzeug.utils import secure_filename

# Page configuration
st.set_page_config(page_title="MediSoft Ultimate", layout="wide", page_icon="🩺")

# File paths
USER_DATA_FILE = "users.json"
UPLOAD_FOLDER = "static/uploads"
MODEL_FILE = "model.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load users from JSON file
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users to JSON file
def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_model():
    try:
        with open(MODEL_FILE, "r") as file:
            model_data = json.load(file)
        return model_data  # Assuming JSON model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

def predict_disease(image):
    if model:
        return random.choice(["Eczema", "Melanoma"])  # Placeholder; replace with real logic
    else:
        return "Model not loaded"
    
# Session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "users" not in st.session_state:
    st.session_state.users = load_users()
if "page" not in st.session_state:
    st.session_state.page = "home"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Custom CSS for modern UI
def load_css():
    st.markdown("""
    <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stMetric {
            border: 1px solid #4CAF50;
            border-radius: 5px;
            padding: 10px;
            text-align: center;
        }
        .stNotification {
            border: 1px solid #ffcc00;
            border-radius: 5px;
            padding: 10px;
            background-color: #fff3cd;
        }
        .stTextInput input {
            border-radius: 5px;
        }
        .stSelectbox select {
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

# Simulate real-time health data
def generate_health_data():
    now = datetime.now()
    data = {
        "Time": [now - timedelta(minutes=i) for i in range(10)][::-1],
        "Heart Rate": [random.randint(60, 80) for _ in range(10)],
        "Blood Pressure": [f"{random.randint(110, 130)}/{random.randint(70, 85)}" for _ in range(10)],
        "Steps": [random.randint(0, 1000) for _ in range(10)],
    }
    return pd.DataFrame(data)

# Home Page
def home():
    st.title("🩺 MediSoft Ultimate")
    st.write("Welcome to the ultimate health and wellness platform!")
    st.write("Please login or create an account to get started.")

# Dashboard Page
def dashboard():
    st.title("📊 Dashboard")
    if st.session_state.logged_in:
        users = st.session_state.users
        current_user = st.session_state.current_user
        user = users[current_user]
        
        st.success(f"Welcome back, **{user['first_name']} {user['last_name']}**! 👋 Let's make today healthier! 💪")

        # Real-Time Health Metrics
        st.subheader("📌 Live Health Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Heart Rate", f"{random.randint(60, 80)} bpm", f"{random.choice(['-2%', '+1%', '0%'])} from last hour")
        with col2:
            st.metric("Blood Pressure", f"{random.randint(110, 130)}/{random.randint(70, 85)} mmHg", "Stable")
        with col3:
            st.metric("Steps", f"{random.randint(0, 1000)}", f"{random.randint(0, 100)}% to goal")
        
        # Interactive Charts
        st.subheader("📈 Real-Time Health Data")
        health_data = generate_health_data()
        fig = px.line(health_data, x="Time", y=["Heart Rate", "Steps"], markers=True, title="Live Health Metrics Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please login to view your dashboard.")

# Upload Image Page
def upload_image():
    st.header("📸 Upload Image for Disease Prediction")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        filename = secure_filename(uploaded_file.name)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"Image uploaded successfully as {filename}!")
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Perform disease prediction
        prediction = predict_disease(uploaded_file)
        st.subheader("🩺 Predicted Disease:")
        st.success(f"**{prediction}**")


# Health Journal Page
def health_journal():
    st.title("📔 Health Journal")
    if st.session_state.logged_in:
        st.write("Log your daily activities here.")
        activity = st.text_input("What did you do today?")
        if st.button("Log Activity"):
            st.success(f"✅ Logged: {activity}")
    else:
        st.info("Please login to use the health journal.")

# AI Assistant Page
def ai_assistant():
    st.title("🤖 AI Health Assistant")
    if st.session_state.logged_in:
        st.write("Ask me anything about your health!")
        query = st.text_input("Your question:")
        if st.button("Ask"):
            st.info(f"AI: Here's some advice based on your query: [Placeholder response]")
    else:
        st.info("Please login to use the AI assistant.")

# Fitness Page
def fitness():
    st.title("🏋️ Fitness")
    if st.session_state.logged_in:
        st.write("Sync your fitness tracker and view your progress.")
        st.write("Coming soon! 🚀")
    else:
        st.info("Please login to view fitness data.")

# Medications Page
def medications():
    st.title("💊 Medications")
    if st.session_state.logged_in:
        st.write("Log and track your medications here.")
        med_name = st.text_input("Medication Name")
        dosage = st.text_input("Dosage")
        time = st.time_input("Time to Take")
        if st.button("Add Medication"):
            st.success(f"✅ Added {med_name} ({dosage}) at {time}")
    else:
        st.info("Please login to track medications.")

# Appointments Page
def appointments():
    st.title("📅 Appointments")
    if st.session_state.logged_in:
        st.write("Schedule and manage your doctor appointments.")
        doctor_name = st.text_input("Doctor's Name")
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        if st.button("Schedule"):
            st.success(f"✅ Appointment with {doctor_name} scheduled on {appointment_date} at {appointment_time}")
    else:
        st.info("Please login to manage appointments.")

# Community Page
def community():
    st.title("🌟 Community")
    if st.session_state.logged_in:
        st.write("Share your health tips and achievements!")
        post = st.text_area("Your post:")
        if st.button("Post"):
            st.success(f"✅ Posted: {post}")
    else:
        st.info("Please login to join the community.")

# Analytics Page
def analytics():
    st.title("📈 Analytics")
    if st.session_state.logged_in:
        st.write("View advanced health analytics and predictive trends.")
        st.write("Coming soon! 🚀")
    else:
        st.info("Please login to view analytics.")

# Profile Page
def profile():
    st.title("👤 Profile")
    if st.session_state.logged_in:
        users = st.session_state.users
        current_user = st.session_state.current_user
        user = users[current_user]
        
        st.subheader("Personal Information")
        st.write(f"**First Name:** {user['first_name']}")
        st.write(f"**Last Name:** {user['last_name']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Mobile:** {user['mobile']}")
        st.write(f"**Gender:** {user['gender']}")
        
        st.subheader("Update Profile")
        with st.form("update_profile_form"):
            new_first_name = st.text_input("First Name", value=user["first_name"])
            new_last_name = st.text_input("Last Name", value=user["last_name"])
            new_email = st.text_input("Email", value=user["email"])
            new_mobile = st.text_input("Mobile Number", value=user["mobile"])
            if st.form_submit_button("Update Profile"):
                users[current_user]["first_name"] = new_first_name
                users[current_user]["last_name"] = new_last_name
                users[current_user]["email"] = new_email
                users[current_user]["mobile"] = new_mobile
                save_users(users)
                st.success("✅ Profile updated successfully!")
    else:
        st.info("Please login to view your profile.")

# Settings Page
def settings():
    st.title("⚙️ Settings")
    if st.session_state.logged_in:
        st.subheader("Change Password")
        with st.form("change_password_form"):
            old_password = st.text_input("Old Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            if st.form_submit_button("Change Password"):
                users = st.session_state.users
                current_user = st.session_state.current_user
                if users[current_user]["password"] == hash_password(old_password):
                    if new_password == confirm_new_password:
                        users[current_user]["password"] = hash_password(new_password)
                        save_users(users)
                        st.success("✅ Password changed successfully!")
                    else:
                        st.error("❌ New passwords do not match!")
                else:
                    st.error("❌ Incorrect old password!")
        
        st.subheader("Theme Settings")
        dark_mode = st.checkbox("Enable Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.success(f"✅ {'Enabled' if dark_mode else 'Disabled'} dark mode!")
    else:
        st.info("Please login to access settings.")

# Sidebar Navigation
def sidebar():
    st.sidebar.title("📌 Navigation")
    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as {st.session_state.current_user}")
        if st.sidebar.button("🏠 Home"):
            st.session_state.page = "home"
        if st.sidebar.button("📊 Dashboard"):
            st.session_state.page = "dashboard"
        if st.sidebar.button("📸 Upload Image"):
            st.session_state.page = "upload_image"
        if st.sidebar.button("📔 Health Journal"):
            st.session_state.page = "health_journal"
        if st.sidebar.button("🤖 AI Assistant"):
            st.session_state.page = "ai_assistant"
        if st.sidebar.button("🏋️ Fitness"):
            st.session_state.page = "fitness"
        if st.sidebar.button("💊 Medications"):
            st.session_state.page = "medications"
        if st.sidebar.button("📅 Appointments"):
            st.session_state.page = "appointments"
        if st.sidebar.button("🌟 Community"):
            st.session_state.page = "community"
        if st.sidebar.button("📈 Analytics"):
            st.session_state.page = "analytics"
        if st.sidebar.button("👤 Profile"):
            st.session_state.page = "profile"
        if st.sidebar.button("⚙️ Settings"):
            st.session_state.page = "settings"
        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.page = "home"
            st.success("✅ Logged out successfully!")
    else:
        if st.sidebar.button("🏠 Home"):
            st.session_state.page = "home"
        if st.sidebar.button("🔑 Login"):
            st.session_state.page = "login"
        if st.sidebar.button("📝 Create Account"):
            st.session_state.page = "register"

# Login Page
def login():
    st.subheader("🔑 Login")
    with st.form("login_form"):
        user_id = st.text_input("👤 User ID")
        password = st.text_input("🔒 Password", type="password")
        if st.form_submit_button("Login"):
            users = load_users()
            if user_id in users and users[user_id]["password"] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.current_user = user_id
                st.success("✅ Login successful!")
                st.session_state.page = "dashboard"
            else:
                st.error("❌ Invalid credentials!")

# Registration Page
def register():
    st.subheader("📝 Create Account")
    with st.form("register_form"):
        first_name = st.text_input("👤 First Name")
        last_name = st.text_input("👤 Last Name")
        user_id = st.text_input("🆔 User ID")
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        confirm_password = st.text_input("🔑 Confirm Password", type="password")
        mobile = st.text_input("📱 Mobile Number")
        gender = st.selectbox("⚧️ Gender", ["Male", "Female", "Other"])
        if st.form_submit_button("Create Account"):
            if password != confirm_password:
                st.error("❌ Passwords do not match!")
            else:
                users = load_users()
                if user_id in users:
                    st.error("❌ User ID already exists!")
                else:
                    users[user_id] = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "password": hash_password(password),
                        "mobile": mobile,
                        "gender": gender,
                    }
                    save_users(users)
                    st.success("✅ Account created successfully! Please login.")
                    st.session_state.page = "login"

# Load the appropriate page
def main():
    load_css()
    sidebar()
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "dashboard":
        dashboard()
    elif st.session_state.page == "upload_image":
        upload_image()
    elif st.session_state.page == "health_journal":
        health_journal()
    elif st.session_state.page == "ai_assistant":
        ai_assistant()
    elif st.session_state.page == "fitness":
        fitness()
    elif st.session_state.page == "medications":
        medications()
    elif st.session_state.page == "appointments":
        appointments()
    elif st.session_state.page == "community":
        community()
    elif st.session_state.page == "analytics":
        analytics()
    elif st.session_state.page == "profile":
        profile()
    elif st.session_state.page == "settings":
        settings()
    elif st.session_state.page == "login":
        login()
    elif st.session_state.page == "register":
        register()

if __name__ == "__main__":
    main()