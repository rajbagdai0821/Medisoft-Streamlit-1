import streamlit as st
import pandas as pd
import plotly.express as px
import random
import numpy as np
from datetime import datetime, timedelta
import json
import hashlib
import os
from werkzeug.utils import secure_filename
from PIL import Image

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

# Load AI Model
@st.cache_resource
def load_model():
    with open(MODEL_FILE, "r") as file:
        model = json.load(file)  # Assuming JSON model structure
    return model

model = load_model()

# Function to predict disease based on image (Placeholder, replace with actual model logic)
def predict_disease(image):
    # This is a placeholder prediction logic
    # Replace with actual image processing and model inference
    return random.choice(["Pneumonia", "Healthy", "Tuberculosis", "COVID-19"])

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

# Sidebar Navigation
def sidebar():
    st.sidebar.title("📌 Navigation")
    if st.session_state.get("logged_in"):
        if st.sidebar.button("📸 Upload Image"):
            st.session_state.page = "upload_image"

# Load the appropriate page
def main():
    sidebar()
    if st.session_state.get("page") == "upload_image":
        upload_image()

if __name__ == "__main__":
    main()
