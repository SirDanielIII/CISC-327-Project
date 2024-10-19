from flask import Flask
from controllers import public_controller

app = Flask(__name__)

app.register_blueprint(public_controller.public_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
