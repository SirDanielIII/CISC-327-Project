from flask import Flask
from controllers import public_controller, account_controller

app = Flask(__name__)

app.register_blueprint(public_controller.public_blueprint)
app.register_blueprint(account_controller.account_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
