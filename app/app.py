from flask import Flask
from flask_login import LoginManager

from .database import initialize_db

def create_app(unit_test=False):
    app = Flask(__name__)
    app.secret_key = '743e38e4152d2160384c9027fb6b8b85'

    initialize_db(app, unit_test)

    from .models import User

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'account.login'

    @login_manager.user_loader
    def user_loader(usr_id: str):
        if usr_id.isdigit():
            return User.query.get(int(usr_id))
        return None
    
    from .controllers import public_controller, account_controller, property_controller

    app.register_blueprint(public_controller.public_blueprint)
    app.register_blueprint(account_controller.account_blueprint)
    app.register_blueprint(property_controller.property_blueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
