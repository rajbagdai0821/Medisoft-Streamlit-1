from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "medisoft_secret_key"  # Required for session and flash messages
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mock user database - in a real app, you'd use a proper database
users = {}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('first')
        password = request.form.get('password')
        
        if user_id in users and users[user_id]['password'] == password:
            session['user_id'] = user_id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        full_name = request.form.get('first')
        mobile = request.form.get('number')
        
        # In a real app, you'd save this to a database or send an email
        flash('Your details have been submitted!', 'success')
        return redirect(url_for('index'))
    
    return render_template('contact.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        first_name = request.form.get('first')
        last_name = request.form.get('last')
        user_id = request.form.get('user')
        email = request.form.get('email')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        mobile = request.form.get('mobile')
        gender = request.form.get('gender')
        
        if password != repassword:
            flash('Passwords do not match!', 'error')
            return render_template('create_account.html')
        
        if user_id in users:
            flash('User ID already exists!', 'error')
            return render_template('create_account.html')
        
        # Save user in our mock database
        users[user_id] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,  # In a real app, this should be hashed
            'mobile': mobile,
            'gender': gender
        }
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    
    return render_template('create_account.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # In a real app, you'd process the image here or send it to an AI model
        flash('Image uploaded successfully!', 'success')
        
        # For demo purposes, just redirect back to home
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
