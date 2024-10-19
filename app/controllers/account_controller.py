from flask import Blueprint, render_template, redirect

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET'])
def login():
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