from flask_login import UserMixin
from enum import Enum

class UserRoles(Enum):
    TENANT = 1
    PROPETY_OWNER = 2
    ADMINISTRATOR = 3

next_user_id = 1

class User(UserMixin):
    id: int
    email: str
    password: str
    token_2fa: str | None = None
    role: UserRoles

    def __init__(self, email, password, role) -> None:
        self.id = next_user_id
        next_user_id = next_user_id + 1
        self.email = email
        self.password = password
        self.role = role