from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import uuid
import os
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key_change_in_production')

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'inventory.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database_if_needed():
    """Initialize the database if it doesn't exist or is empty"""
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    
    # Check if database needs initialization
    needs_init = False
    
    if not os.path.exists(DATABASE):
        needs_init = True
        print("Database file not found, initializing...")
    else:
        # Check if the users table exists
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cursor.fetchone() is None:
                needs_init = True
                print("Database exists but tables are missing, initializing...")
            conn.close()
        except Exception as e:
            needs_init = True
            print(f"Database error, reinitializing: {e}")
    
    if needs_init:
        # Import and run the initialization function
        from __init__ import init_database
        init_database()
        print("Database initialized successfully!")

# Initialize database on startup
init_database_if_needed()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        
        if user and user['password'] == hashlib.sha256(password.encode()).hexdigest():
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            db.close()
            return redirect(url_for('dashboard'))
        else:
            db.close()
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('register.html')
        
        db = get_db()
        
        # Check if username already exists
        existing_user = db.execute(
            'SELECT username FROM users WHERE username = ?', 
            (username,)
        ).fetchone()
        
        if existing_user:
            db.close()
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        # Generate a unique email using username + timestamp to avoid UNIQUE constraint issues
        import time
        unique_email = f"{username}_{int(time.time())}@techcorp.local"
        try:
            db.execute(
                '''INSERT INTO users (username, email, password, first_name, last_name, role, 
                   phone, address, city, postal_code, country, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (username, unique_email, hashed_password, '', '', 'employee',
                 '', '', '', '', '', datetime.now())
            )
            db.commit()
            db.close()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.close()
            flash('An error occurred while creating your account', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    
    total_items = db.execute('SELECT COUNT(*) as count FROM inventory_items').fetchone()['count']
    total_value = db.execute('SELECT SUM(quantity * price) as value FROM inventory_items').fetchone()['value'] or 0
    low_stock = db.execute('SELECT COUNT(*) as count FROM inventory_items WHERE quantity < 10').fetchone()['count']
    
    recent_items = db.execute(
        'SELECT * FROM inventory_items ORDER BY last_updated DESC LIMIT 5'
    ).fetchall()
    
    db.close()
    
    return render_template('dashboard.html', 
                         total_items=total_items,
                         total_value=total_value,
                         low_stock=low_stock,
                         recent_items=recent_items)

@app.route('/inventory')
def inventory():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    items = db.execute('SELECT * FROM inventory_items ORDER BY name').fetchall()
    db.close()
    
    return render_template('inventory.html', items=items)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        current_password = request.form['current_password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and user['password'] == hashlib.sha256(current_password.encode()).hexdigest():
            token = str(uuid.uuid4())
            db.execute(
                'INSERT INTO password_reset_tokens (username, token) VALUES (?, ?)',
                (username, token)
            )
            db.commit()
            db.close()
            
            # Redirection directe vers reset password avec le token
            return redirect(url_for('reset_password') + f'?temp-forgot-password-token={token}')
        else:
            db.close()
            flash('Invalid username or current password', 'error')
    
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('temp-forgot-password-token', '')
    
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('reset_password.html', token=token, username=username)
        
        # VULNERABILITY: Token validation is missing!
        # The application doesn't verify if the token is valid or even exists
        db = get_db()
        
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        db.execute(
            'UPDATE users SET password = ? WHERE username = ?',
            (hashed_password, username)
        )
        db.commit()
        db.close()
        
        flash('Password successfully reset! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    # Get username from token for display
    db = get_db()
    token_row = db.execute(
        'SELECT username FROM password_reset_tokens WHERE token = ? AND used = FALSE',
        (token,)
    ).fetchone()
    
    username = token_row['username'] if token_row else ''
    db.close()
    
    return render_template('reset_password.html', token=token, username=username)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    user = db.execute(
        'SELECT username, email, role, first_name, last_name, phone, address, city, postal_code, country, created_at FROM users WHERE id = ?', 
        (session['user_id'],)
    ).fetchone()
    db.close()
    
    return render_template('profile.html', user=user)

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Check if user is admin
    db = get_db()
    user = db.execute(
        'SELECT role FROM users WHERE id = ?', 
        (session['user_id'],)
    ).fetchone()
    
    if not user or user['role'] != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all users with their personal information
    users = db.execute(
        'SELECT id, username, email, role, first_name, last_name, phone, address, city, postal_code, country, created_at FROM users ORDER BY created_at DESC'
    ).fetchall()
    db.close()
    
    return render_template('admin.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3206, debug=False)
