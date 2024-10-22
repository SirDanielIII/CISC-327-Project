import os
import sqlite3

from flask import Flask, g
from flask_login import LoginManager

from controllers import public_controller, account_controller, property_controller
from models import in_memory_users

app = Flask(__name__)
app.secret_key = '743e38e4152d2160384c9027fb6b8b85'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'account.login'

# Set the database path next to app.py
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')


def get_db():
    """Establish and cache a database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row  # Access columns by name
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    """Close the database connection after each request."""
    db = g.pop('db', None)
    if db:
        db.close()


def init_db():
    """Create the required tables if they don't exist."""
    db = get_db()
    cursor = db.cursor()

    # Create 'properties' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            available_date TEXT NOT NULL,
            rent_per_month INTEGER NOT NULL,
            bedrooms INTEGER NOT NULL,
            bathrooms INTEGER NOT NULL,
            parking_available BOOLEAN NOT NULL,
            parking_per_month INTEGER,
            includes_water BOOLEAN NOT NULL,
            includes_heating BOOLEAN NOT NULL,
            includes_electricity BOOLEAN NOT NULL,
            includes_laundry BOOLEAN NOT NULL
        );
    ''')

    # Create 'users' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            is_admin BOOLEAN DEFAULT 0
        );
    ''')

    db.commit()


def check_and_initialize_db():
    """Check if the database exists and initialize if not."""
    if not os.path.exists(DB_PATH):
        print("[WARNING] Database not found. Initializing...")
        init_db()
    else:
        print("[INFO] Database already exists. No initialization needed.")


@login_manager.user_loader
def user_loader(user_id: str):
    """Load a user by ID."""
    if user_id.isdigit():
        user_id = int(user_id)
        for user in in_memory_users:
            if user.id == user_id:
                return user
    return None


# Register blueprints
app.register_blueprint(public_controller.public_blueprint)
app.register_blueprint(account_controller.account_blueprint)
app.register_blueprint(property_controller.property_blueprint)

if __name__ == '__main__':
    # Ensure database is initialized only once at the start
    with app.app_context():
        check_and_initialize_db()

    app.run(debug=True)
