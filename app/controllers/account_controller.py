from flask import Blueprint, render_template, redirect, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
import re
from ..models.user_model import User
from ..database import db
from ..enums.AccountType import AccountType
from .helpers.anonymous_only import anonymous_only
from .helpers.qr_code_generator import get_b64_encoded_qr_code

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET', 'POST'])
@anonymous_only
def login():
    if request.method == 'POST':
        # Perform authentication here
        email = request.form.get('email')
        password = request.form.get('password')

        validation_error = False

        if email == None or email == '':
            validation_error = True
            flash("Please enter a valid email address to login.", 'error')
        
        if password == None or password == '':
            validation_error = False
            flash("Please enter a valid email address to login.", 'error')

        if validation_error:
            return redirect(request.url)

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

        # If failure, flash an error message and redirect to avoid resubmission
        flash('The email or password provided is invalid! Please verify it has been entered correctly.', 'error')
        return redirect(request.url)
    return render_template('account/login.html')

@account_blueprint.route('/register', methods=['GET', 'POST'])
@anonymous_only
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if email == None or email == '':
            flash('Please enter a first name to register an account.', 'error')
            return redirect('/register')

        user: User = User.query.filter_by(email=email).scalar()
        if user:
            # A user with this email already exists
            flash('The email provided is already registered for an account! Please login instead.', 'error')
            return redirect('/register')
        
        validation_error = False

        if first_name == None or first_name == '':
            validation_error = True
            flash('Please enter a first name to register an account.', 'error')

        if last_name == None or last_name == '':
            validation_error = True
            flash('Please enter a last name to register an account.', 'error')

        if password == None or not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", password):
            # Password does not meet requirements
            # At least eight digiits, has an upper and lower case letter, and one number
            flash('The password entered does not meet the requirements for a strong password.', 'error')
            return redirect('/register')
        
        if confirm_password == None or password != confirm_password:
            # Passwords do not match
            validation_error = True
            flash('The confirmed password does not match the entered password!', 'error')
            
        if validation_error:
            return redirect('/register')

        user = User(first_name=first_name, last_name=last_name, email=email, password=password, account_type=AccountType.PROPERTY_OWNER)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect('/setup_2fa')
    return render_template('account/register.html')

@account_blueprint.route('/logout')
@login_required
def logout():
    session.pop('2fa_verified', None)
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
        otp = request.form.get('verification_code')
        if otp == None or otp == '':
            flash("Please enter a valid OTP to completed 2FA verification.", category='error')
            return redirect(request.url)
        
        if current_user.is_otp_valid(otp):
            current_user.is_2fa_auth_enabled = True
            db.session.commit()
            session['2fa_verified'] = True

            flash('Successfully setup 2FA authentication.', category='success')
            return redirect('/')
        else:
            flash('The OTP entered did not match the expected value. Please try again.',category='error')
            return redirect(request.url)

    # Generating 2FA Authenticator app qr code
    b64_qr_code = get_b64_encoded_qr_code(current_user.get_otp_provisioning_uri())

    return render_template('account/setup_2fa.html', qr_code=b64_qr_code)

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
        otp = request.form.get('verification_code')
        if otp == None or otp == '':
            flash("Please enter a valid OTP to completed 2FA verification.", category='error')
            return redirect(request.url)

        if current_user.is_otp_valid(otp):
            session['2fa_verified'] = True
            flash('Successfully verified 2FA authentication.', category='success')

            redirect_url = request.args.get('next')
            return redirect('/' if redirect_url == None else redirect_url)
        else:
            flash('The OTP entered did not match the expected value. Please try again.',category='error')
            return redirect(request.url)
    return render_template('account/verify_2fa.html')