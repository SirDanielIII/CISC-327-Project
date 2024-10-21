from flask import Flask
from flask_login import LoginManager
from controllers import public_controller, account_controller, property_controller
from models import in_memory_users

app = Flask(__name__)
app.secret_key = '743e38e4152d2160384c9027fb6b8b85'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'account.login'

@login_manager.user_loader
def user_loader(idStr: str):
    if idStr.isdigit():
        id = int(idStr)
        for user in in_memory_users:
            if user.id == id:
                return user
            pass
    return None

app.register_blueprint(public_controller.public_blueprint)
app.register_blueprint(account_controller.account_blueprint)
app.register_blueprint(property_controller.property_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
