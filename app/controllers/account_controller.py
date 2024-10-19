from flask import Blueprint, render_template, redirect, request, flash
from models import in_memory_users

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform authenitcation here
        email = request.form['email']
        password = request.form['password']
        for user in in_memory_users:
            if user.email == email and user.password == password:
                # If success, redirect to next page
                return redirect('/') # TODO
        # If failure, flash an error message and render_template
        flash('The email or password provided is invalid! Please verify it has been entered correctly.', 'error')
    return render_template('account/login.html')

@account_blueprint.route('/register', methods=['GET'])
def register():
    return render_template('account/register.html')

@account_blueprint.route('/setup_2fa', methods=['GET'])
def setup_2fa():
    return render_template('account/setup_2fa.html')

@account_blueprint.route('/verify_2fa', methods=['GET'])
def verify_2fa():
    return render_template('account/verify_2fa.html')