from flask_login import UserMixin
from pyotp import random_base32, TOTP
from werkzeug.security import generate_password_hash, check_password_hash

from ..database import db
from ..enums.AccountType import AccountType


class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    first_name = db.Column(db.String(40), nullable=True)
    last_name = db.Column(db.String(40), nullable=True)
    password = db.Column(db.String(1024), nullable=False)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    token_2fa = db.Column(db.String(1024), nullable=True)
    is_2fa_auth_enabled = db.Column(db.Boolean, nullable=False, server_default='f', default=False)

    properties = db.relationship('Property', back_populates='owner', cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, password, account_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.account_type = account_type

        self.password = generate_password_hash(password)
        self.token_2fa = random_base32()

        super().__init__()

    def is_password_valid(self, password_input: str) -> bool:
        return check_password_hash(self.password, password_input)

    def is_otp_valid(self, user_otp: str) -> bool:
        totp = TOTP(self.token_2fa)
        return totp.verify(user_otp)

    def get_otp_provisioning_uri(self) -> str:
        totp = TOTP(self.token_2fa)
        return totp.provisioning_uri(name=self.email, issuer_name='Lease Fifty Seven')
