# Employee Management Web Application

A professional role-based Employee Management Web Application built with Python Flask, featuring Admin and User roles with different access levels.

## Features

- **Role-Based Access Control**: Two user roles (Admin and Normal User)
- **Session-Based Authentication**: Secure login system with password hashing
- **Admin Features**:
  - Full CRUD operations (Create, Read, Update, Delete)
  - View total employee count
  - Add new employees
  - Edit existing employees
  - Delete employees with confirmation
- **User Features**:
  - Read-only access to employee records
  - View employee list
  - View profile
- **Modern UI**: Bootstrap 5 with custom styling and responsive design
- **Security**: Password hashing, route protection, role-based authorization

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: SQLite
- **Authentication**: Session-based with Werkzeug password hashing

## Project Structure

```
employee/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── employee.db           # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html         # Base template with sidebar
│   ├── login.html        # Login page
│   ├── admin_dashboard.html
│   ├── user_dashboard.html
│   ├── employees.html    # View employees table
│   ├── add_employee.html
│   ├── edit_employee.html
│   └── profile.html
└── static/               # Static files
    └── style.css         # Custom CSS
```

## Installation

1. **Clone or download the project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   - Open your browser and navigate to `http://localhost:5000`

## Default Login Credentials

The application automatically creates default users on first run:

### Admin Account
- **Username**: `Selva Rani`
- **Password**: `Selva#2509rani`
- **Access**: Full CRUD operations
- **Note**: Only this username has admin privileges

### Normal User Account
- **Username**: `user`
- **Password**: `user123`
- **Access**: Read-only (view employees)
- **Note**: Admin can create additional user accounts with different names

## Usage

### For Administrators

1. **Login** with admin credentials
2. **Dashboard**: View total employee count and quick actions
3. **View Employees**: See all employee records in a table
4. **Add Employee**: Create new employee records with validation
5. **Edit Employee**: Update existing employee information
6. **Delete Employee**: Remove employees with confirmation dialog
7. **Profile**: View your account information

### For Normal Users

1. **Login** with user credentials
2. **Dashboard**: View welcome message and available features
3. **View Employees**: Browse employee records (read-only)
4. **Profile**: View your account information

## Security Features

- **Password Hashing**: All passwords are hashed using Werkzeug's security functions
- **Session Management**: Secure session-based authentication
- **Route Protection**: All routes require login
- **Role-Based Authorization**: Admin-only routes are protected
- **Input Validation**: Form validation for all employee data
- **SQL Injection Prevention**: Using parameterized queries

## Database Schema

### Users Table
- `id` (INTEGER, PRIMARY KEY)
- `username` (TEXT, UNIQUE)
- `password` (TEXT, hashed)
- `name` (TEXT)
- `role` (TEXT, 'admin' or 'user')

### Employees Table
- `id` (INTEGER, PRIMARY KEY)
- `name` (TEXT)
- `email` (TEXT, UNIQUE)
- `phone` (TEXT)
- `role` (TEXT)
- `salary` (REAL)

## Customization

### Change Secret Key
In `app.py`, change the `secret_key`:
```python
app.secret_key = 'your-secret-key-change-this-in-production'
```

### Modify Default Users
Edit the `init_db()` function in `app.py` to change default usernames/passwords.

## Development

The application runs in debug mode by default. For production:

1. Set `debug=False` in `app.py`
2. Use a production WSGI server (e.g., Gunicorn)
3. Change the secret key
4. Use a production database (PostgreSQL, MySQL)

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Edge
- Safari

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the code comments or create an issue in the repository.

---

**Note**: This is a demonstration application. For production use, implement additional security measures such as:
- CSRF protection
- Rate limiting
- Input sanitization
- Database connection pooling
- Environment variables for configuration

