class User():
    
    email: str
    password: str

    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password