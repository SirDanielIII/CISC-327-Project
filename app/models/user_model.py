from flask_login import UserMixin

class User(UserMixin):
    id: int
    email: str
    password: str
    token_2fa: str | None = None

    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password