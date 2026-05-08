"""
Authentication routes for user registration, login, and logout
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.models import db, User
from functools import wraps


# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration route
    GET: Display registration form
    POST: Process registration form
    """
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        elif User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        
        if not email:
            errors.append('Email is required')
        elif '@' not in email:
            errors.append('Invalid email format')
        elif User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if not password:
            errors.append('Password is required')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # If errors exist, return them
        if errors:
            if request.is_json:
                return jsonify({'success': False, 'errors': errors}), 400
            return render_template('register.html', errors=errors)
        
        try:
            # Create new user
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            
            # Add to database
            db.session.add(new_user)
            db.session.commit()
            
            if request.is_json:
                return jsonify({'success': True, 'message': 'Registration successful'}), 201
            
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            error_msg = 'Registration failed. Please try again.'
            if request.is_json:
                return jsonify({'success': False, 'error': error_msg}), 500
            return render_template('register.html', errors=[error_msg])
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login route
    GET: Display login form
    POST: Process login form
    """
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required')
        
        if not password:
            errors.append('Password is required')
        
        if errors:
            if request.is_json:
                return jsonify({'success': False, 'errors': errors}), 400
            return render_template('login.html', errors=errors)
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            error_msg = 'Invalid username or password'
            if request.is_json:
                return jsonify({'success': False, 'error': error_msg}), 401
            return render_template('login.html', errors=[error_msg])
        
        # Set session
        session['user_id'] = user.id
        session['username'] = user.username
        session.permanent = True
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Login successful'}), 200
        
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    User logout route
    Clears session and redirects to login
    """
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    """
    User profile page
    Displays current user information
    """
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    return render_template('profile.html', user=user)
