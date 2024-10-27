from flask_login import UserMixin
from ..database import db
from ..enums.AccountType import AccountType

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    account_type = db.Column(db.Enum(AccountType), nullable=False)
    token_2fa = db.Column(db.String(1024), nullable=True)

    properties = db.relationship('Property', back_populates='owner', cascade="all, delete-orphan")