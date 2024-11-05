from flask import Blueprint, render_template

public_blueprint = Blueprint('public', __name__)


@public_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def not_found():
    return render_template("not_found.html"), 404
