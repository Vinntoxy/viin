# routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import AdminUser, Happening, db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator to protect admin routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = AdminUser.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin/login.html', error='Invalid username or password')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin.admin_login'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    happenings = Happening.query.order_by(Happening.order).all()
    return render_template('admin/dashboard.html', happenings=happenings)

# ... (We'll add more routes here later)
