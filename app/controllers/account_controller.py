from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user_model import User
from ..database import db
from ..enums.AccountType import AccountType
from .helpers.anonymous_only import anonymous_only

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET', 'POST'])
@anonymous_only
def login():
    if request.method == 'POST':
        # Perform authentication here
        email = request.form['email']
        password = request.form['password']

        user: User = User.query.filter_by(email=email).scalar()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user)
                return redirect('/') # TODO

        # If failure, flash an error message and render_template
        flash('The email or password provided is invalid! Please verify it has been entered correctly.', 'error')
    return render_template('account/login.html')

@account_blueprint.route('/register', methods=['GET', 'POST'])
@anonymous_only
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        
        user: User = User.query.filter_by(email=email).scalar()
        if user:
            # A user with this email already exists
            flash('The email provided is already registered for an account! Please login instead.', 'error')
            return render_template('account/register.html')     

        user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password), account_type=AccountType.PROPERTY_OWNER)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect('/setup_2fa')
    return render_template('account/register.html')

@account_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@account_blueprint.route('/setup_2fa', methods=['GET', 'POST'])
@login_required
def setup_2fa():
    if request.method == 'POST':
        # TODO: Backend implementation
        # For now always success
        flash('Successfully setup 2FA authentication.', category='success')
        return redirect('/') # TODO
    return render_template('account/setup_2fa.html')

@account_blueprint.route('/verify_2fa', methods=['GET', 'POST'])
@login_required
def verify_2fa():
    if request.method == 'POST':
        # TODO: Backend implementation
        # For now always success
        return redirect('/') # TODO
    return render_template('account/verify_2fa.html')