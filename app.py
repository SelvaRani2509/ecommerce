"""
Employee Management Web Application
Role-based Flask app with Admin and User access
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database file
DATABASE = 'employee.db'

# ---------------- Database Utilities ----------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables and default users"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
    )''')
    
    # Employees table
    conn.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        role TEXT NOT NULL,
        salary REAL NOT NULL
    )''')
    
    # Default admin
    admin_exists = conn.execute('SELECT id FROM users WHERE username = ?', ('Selva Rani',)).fetchone()
    if not admin_exists:
        admin_password = generate_password_hash('Selva#2509rani')
        conn.execute('INSERT INTO users (username,password,name,role) VALUES (?,?,?,?)',
                     ('Selva Rani', admin_password, 'Selva Rani', 'admin'))
    
    # Default normal user
    user_exists = conn.execute('SELECT id FROM users WHERE username = ?', ('user',)).fetchone()
    if not user_exists:
        user_password = generate_password_hash('user123')
        conn.execute('INSERT INTO users (username,password,name,role) VALUES (?,?,?,?)',
                     ('user', user_password, 'Normal User', 'user'))
    
    conn.commit()
    conn.close()

# ---------------- Decorators ----------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated

# ---------------- Routes ----------------

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page accessible by anyone. Redirects based on user role."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Please enter both username and password.', 'warning')
            return render_template('login.html')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            # Set session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['role'] = user['role']

            flash(f'Welcome back, {user["name"]}!', 'success')

            # Redirect based on role
            return redirect(url_for('admin_dashboard') if user['role']=='admin' else url_for('user_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('user_dashboard'))

# ---------------- Admin Dashboard ----------------

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    employee_count = conn.execute('SELECT COUNT(*) as count FROM employees').fetchone()['count']
    conn.close()
    return render_template('admin_dashboard.html', employee_count=employee_count)

# ---------------- User Dashboard ----------------

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html')

# ---------------- Employee Routes ----------------

@app.route('/employees')
@login_required
def employees():
    conn = get_db_connection()
    employees_list = conn.execute('SELECT * FROM employees ORDER BY id').fetchall()
    conn.close()
    return render_template('employees.html', employees=employees_list)

@app.route('/add_employee', methods=['GET','POST'])
@admin_required
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        role = request.form.get('role')
        salary = request.form.get('salary')

        errors = []
        if not name: errors.append('Name is required.')
        if not email: errors.append('Email is required.')
        elif '@' not in email: errors.append('Invalid email format.')
        if not phone: errors.append('Phone is required.')
        if not role: errors.append('Role is required.')
        try:
            salary = float(salary)
            if salary < 0: errors.append('Salary must be positive.')
        except:
            errors.append('Salary must be a number.')

        if errors:
            for error in errors: flash(error,'danger')
            return render_template('add_employee.html')

        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO employees (name,email,phone,role,salary) VALUES (?,?,?,?,?)',
                         (name,email,phone,role,salary))
            conn.commit()
            flash('Employee added successfully!','success')
            return redirect(url_for('employees'))
        except sqlite3.IntegrityError:
            flash('Email already exists.','danger')
        finally:
            conn.close()

    return render_template('add_employee.html')

@app.route('/update_employee')
@admin_required
def update_employee():
    conn = get_db_connection()
    employees_list = conn.execute('SELECT * FROM employees ORDER BY id').fetchall()
    conn.close()
    return render_template('update_employee.html', employees=employees_list)

@app.route('/edit_employee/<int:employee_id>', methods=['GET','POST'])
@admin_required
def edit_employee(employee_id):
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()

    if not employee:
        conn.close()
        flash('Employee not found.','danger')
        return redirect(url_for('employees'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        role = request.form.get('role')
        salary = request.form.get('salary')

        errors=[]
        if not name: errors.append('Name is required.')
        if not email: errors.append('Email is required.')
        elif '@' not in email: errors.append('Invalid email format.')
        if not phone: errors.append('Phone is required.')
        if not role: errors.append('Role is required.')
        try:
            salary = float(salary)
            if salary < 0: errors.append('Salary must be positive.')
        except:
            errors.append('Salary must be a number.')

        if errors:
            for e in errors: flash(e,'danger')
            conn.close()
            return render_template('edit_employee.html', employee=employee)

        try:
            conn.execute('UPDATE employees SET name=?, email=?, phone=?, role=?, salary=? WHERE id=?',
                         (name,email,phone,role,salary,employee_id))
            conn.commit()
            flash('Employee updated successfully!','success')
            conn.close()
            return redirect(url_for('employees'))
        except sqlite3.IntegrityError:
            flash('Email already exists.','danger')
            conn.close()
            return render_template('edit_employee.html', employee=employee)

    conn.close()
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete_employee/<int:employee_id>', methods=['POST'])
@admin_required
def delete_employee(employee_id):
    conn = get_db_connection()
    employee = conn.execute('SELECT * FROM employees WHERE id=?',(employee_id,)).fetchone()
    if not employee:
        conn.close()
        flash('Employee not found.','danger')
        return redirect(url_for('employees'))
    conn.execute('DELETE FROM employees WHERE id=?',(employee_id,))
    conn.commit()
    conn.close()
    flash('Employee deleted successfully!','success')
    return redirect(url_for('employees'))

# ---------------- User Profile ----------------

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# ---------------- Add User ----------------

@app.route('/add_user', methods=['GET','POST'])
@admin_required
def add_user():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')

        errors=[]
        if not username: errors.append('Username is required.')
        if not password: errors.append('Password is required.')
        elif len(password)<6: errors.append('Password must be at least 6 characters.')
        if not name: errors.append('Name is required.')
        if username=='Selva Rani': errors.append('Username reserved for admin.')

        if errors:
            for e in errors: flash(e,'danger')
            return render_template('add_user.html')

        try:
            conn = get_db_connection()
            hashed = generate_password_hash(password)
            conn.execute('INSERT INTO users (username,password,name,role) VALUES (?,?,?,?)',
                         (username,hashed,name,'user'))
            conn.commit()
            flash(f'User "{name}" created successfully!','success')
            return redirect(url_for('admin_dashboard'))
        except sqlite3.IntegrityError:
            flash('Username already exists.','danger')
        finally:
            conn.close()
    return render_template('add_user.html')

# ---------------- Run App ----------------

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    else:
        init_db()
    app.run(debug=True)
