import re

from flask import Blueprint, render_template, redirect, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user

from .helpers.anonymous_only import anonymous_only
from .helpers.qr_code_generator import get_b64_encoded_qr_code
from ..database import db
from ..enums.AccountType import AccountType
from ..models.user_model import User

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/login', methods=['GET', 'POST'])
@anonymous_only
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        validation_error = False

        if not email or not re.match(r".+@.+", email):
            validation_error = True
            flash("Please enter a valid email address to login.", 'error')

        if not password:
            validation_error = True
            flash("Please enter a valid password to login.", 'error')

        if validation_error:
            # Render template with the email provided
            return render_template('account/login.html', email=email)

        redirect_url = request.args.get('next')

        user: User = User.query.filter_by(email=email).scalar()
        if user and user.is_password_valid(password):
            flash('Logged in successfully!', category='success')
            login_user(user)
            if user.is_2fa_auth_enabled:
                next_url = '/verify_2fa'
                if redirect_url:
                    next_url += f'?next={redirect_url}'
                return redirect(next_url)
            return redirect(redirect_url or '/')

        flash('The email or password provided is invalid! Please verify it has been entered correctly.', 'error')
        return render_template('account/login.html', email=email)

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
        account_type = request.form.get('type')

        validation_error = False

        if not email or not re.match(r".+@.+", email):
            validation_error = True
            flash("Please enter a valid email address.", 'error')

        if User.query.filter_by(email=email).scalar():
            flash("The email provided is already registered. Please log in.", 'error')
            return render_template('account/register.html', first_name=first_name, last_name=last_name,
                                   email=email, account_type=account_type)

        if not first_name:
            validation_error = True
            flash('Please enter a first name.', 'error')

        if not last_name:
            validation_error = True
            flash('Please enter a last name.', 'error')

        if not password or not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$", password):
            flash('The password does not meet the requirements.', 'error')
            return render_template('account/register.html', first_name=first_name, last_name=last_name,
                                   email=email, account_type=account_type)

        if password != confirm_password:
            validation_error = True
            flash('The confirmed password does not match.', 'error')

        if validation_error:
            return render_template('account/register.html', first_name=first_name, last_name=last_name,
                                   email=email, account_type=account_type)

        account_type = request.form.get('type')
        print(account_type)
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            account_type=AccountType[account_type]  # No need for .upper() since values match
        )

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
        if otp is None or otp == '':
            flash("Please enter a valid OTP to completed 2FA verification.", category='error')
            return redirect(request.url)

        if current_user.is_otp_valid(otp):
            current_user.is_2fa_auth_enabled = True
            db.session.commit()
            session['2fa_verified'] = True

            flash('Successfully setup 2FA authentication.', category='success')
            return redirect('/')
        else:
            flash('The OTP entered did not match the expected value. Please try again.', category='error')
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
        if not otp:
            flash("Please enter a valid OTP to completed 2FA verification.", category='error')
            return redirect(request.url)

        if current_user.is_otp_valid(otp):
            session['2fa_verified'] = True
            flash('Successfully verified 2FA authentication.', category='success')

            redirect_url = request.args.get('next')
            return redirect('/' if redirect_url is None else redirect_url)
        else:
            flash('The OTP entered did not match the expected value. Please try again.', category='error')
            return redirect(request.url)
    return render_template('account/verify_2fa.html')
