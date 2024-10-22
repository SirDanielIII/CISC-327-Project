from flask_login import UserMixin
from enum import Enum

class UserRoles(Enum):
    TENANT = 1
    PROPETY_OWNER = 2
    ADMINISTRATOR = 3

class User(UserMixin):
    next_user_id = 1

    def __init__(self, name, email, password, role: UserRoles) -> None:
        self.id = User.next_user_id
        User.next_user_id = User.next_user_id + 1
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.token_2fa: str | None = None