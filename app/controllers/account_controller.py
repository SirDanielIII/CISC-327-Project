from flask import Blueprint, render_template, redirect, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
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

        redirect_url = request.args.get('next')

        user: User = User.query.filter_by(email=email).scalar()
        if user:
            if user.is_password_valid(password):
                flash('Logged in successfully!', category='success')
                login_user(user)
                if user.is_2fa_auth_enabled:
                    next_url = '/verify_2fa'
                    if redirect_url != None:
                        next_url += f'?next={redirect_url}'
                    return redirect(next_url)
                else:
                    return redirect('/' if redirect_url == None else redirect_url)

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

        user = User(first_name=first_name, last_name=last_name, email=email, password=password, account_type=AccountType.PROPERTY_OWNER)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect('/setup_2fa')
    return render_template('account/register.html')

@account_blueprint.route('/logout')
@login_required
def logout():
    session['2fa_verified'] = False
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect('/')

@account_blueprint.route('/setup_2fa', methods=['GET', 'POST'])
@login_required
def setup_2fa():
    if current_user.is_2fa_auth_enabled:
        flash('You have already enabled 2FA Authentication and cannot access this page.', category='error')
        return redirect('/')

    if request.method == 'POST':
        otp = request.form['verification_code']
        if current_user.is_otp_valid(otp):
            current_user.is_2fa_auth_enabled = True
            db.session.commit()
            session['2fa_verified'] = True

            flash('Successfully setup 2FA authentication.', category='success')
            return redirect('/')
        else:
            flash('The OTP entered did not match the expected value. Please try again.',category='error')
    return render_template('account/setup_2fa.html')

@account_blueprint.route('/verify_2fa', methods=['GET', 'POST'])
@login_required
def verify_2fa():
    if not current_user.is_2fa_auth_enabled:
        flash('You have not enabled 2FA Authentication. Enable it on this page first.', category='error')
        return redirect('/setup_2fa')
    elif session.get('2fa_verified'):
        flash('You have already completed 2FA Authentication and cannot access this page.', category='error')
        return redirect('/')

    if request.method == 'POST':
        otp = request.form['verification_code']
        if current_user.is_otp_valid(otp):
            session['2fa_verified'] = True
            flash('Successfully verified 2FA authentication.', category='success')

            redirect_url = request.args.get('next')
            return redirect('/' if redirect_url == None else redirect_url)
        else:
            flash('The OTP entered did not match the expected value. Please try again.',category='error')
    return render_template('account/verify_2fa.html')