from flask_login import UserMixin

next_user_id = 1

class User(UserMixin):
    id: int
    email: str
    password: str
    token_2fa: str | None = None

    def __init__(self, email, password) -> None:
        self.id = next_user_id
        next_user_id = next_user_id + 1
        self.email = email
        self.password = password