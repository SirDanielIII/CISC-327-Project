import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

DATABASE_NAME = 'rent_management.db'

db = SQLAlchemy()
migrate = Migrate()

def initialize_db(app: Flask):
    db_directory = os.path.dirname(__file__)
    db_path = os.path.join(db_directory, DATABASE_NAME)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Required for Flask-SqlAlchemy to detect models
    import models
    db.init_app(app)

    migrations_directory = os.path.join(db_directory, 'migrations')
    migrate.init_app(app, db, directory=migrations_directory)

    with app.app_context():
        if not os.path.exists(DATABASE_NAME):
            # db doesn't exist, creating it...
            db.create_all()

        # Upgrade the db to the latest schema
        upgrade()
