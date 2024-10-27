import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, stamp

DATABASE_NAME = 'rent_management.db'
UNIT_TEST_DATABASE_NAME = f'unit_test_{DATABASE_NAME}'

db = SQLAlchemy()
migrate = Migrate()

def initialize_db(app: Flask, unit_test=False):
    db_directory = os.path.dirname(__file__)

    db_path = os.path.join(db_directory, UNIT_TEST_DATABASE_NAME if unit_test else DATABASE_NAME)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Required for Flask-SqlAlchemy to detect models
    from ..models import User, Property
    db.init_app(app)

    migrations_directory = os.path.join(db_directory, 'migrations')
    migrate.init_app(app, db, directory=migrations_directory)

    with app.app_context():
        if not os.path.exists(DATABASE_NAME):
            # db doesn't exist, creating it...
            db.create_all()
            stamp()

        # Upgrade the db to the latest schema
        upgrade()
