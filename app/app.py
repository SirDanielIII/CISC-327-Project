from flask import Flask
from flask_login import LoginManager

from controllers import public_controller, account_controller, property_controller
from database.database_manager import DatabaseManager
from models import in_memory_users

def create_app():
    app = Flask(__name__)
    app.secret_key = '743e38e4152d2160384c9027fb6b8b85'

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'account.login'


    #@app.teardown_appcontext
    #def close_db(exception=None):
    #    """Close the database connections after each request."""
    #    DatabaseManager.close_db()


    @login_manager.user_loader
    def user_loader(usr_id: str):
        for user in in_memory_users:
            if user.uuid == usr_id:
                return user
        return None

    app.register_blueprint(public_controller.public_blueprint)
    app.register_blueprint(account_controller.account_blueprint)
    app.register_blueprint(property_controller.property_blueprint)
    return app

if __name__ == '__main__':
    #with app.app_context():
    #    DatabaseManager.init_databases()
    app = create_app()
    app.run(debug=True)
