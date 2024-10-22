import os
import sqlite3
import uuid

from flask import g

from enums.DatabaseType import DatabaseType


class DatabaseManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    USER_DB_PATH = os.path.join(BASE_DIR, 'user_database.db')
    PROPERTY_DB_PATH = os.path.join(BASE_DIR, 'property_database.db')

    @staticmethod
    def get_db(db_type: DatabaseType):
        """Get a database connection."""
        if db_type.value not in g:
            db_path = (
                DatabaseManager.USER_DB_PATH if db_type == DatabaseType.USER
                else DatabaseManager.PROPERTY_DB_PATH
            )
            g[db_type.value] = sqlite3.connect(db_path)
            g[db_type.value].row_factory = sqlite3.Row
        return g[db_type.value]

    @staticmethod
    def close_db(exception=None):
        """Close all open database connections."""
        for db_type in [DatabaseType.USER, DatabaseType.PROPERTY]:
            db = g.pop(db_type.value, None)
            if db:
                db.close()

    @staticmethod
    def generate_uuid_for_rental(address, unit):
        """Generate a UUID based on address and unit."""
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{address}-{unit}"))

    @staticmethod
    def generate_uuid_for_user(email):
        """Generate a UUID based on the user's email."""
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, email))

    @staticmethod
    def init_property_db():
        """Initialize the property database with the 'properties' table."""
        db = DatabaseManager.get_db(DatabaseType.PROPERTY)
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id TEXT PRIMARY KEY,
                address TEXT NOT NULL,
                unit TEXT NOT NULL,
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
        db.commit()

    @staticmethod
    def create_property(address, unit, owner, available_date, rent_per_month, bedrooms,
                        bathrooms, parking_available, parking_per_month, includes_water,
                        includes_heating, includes_electricity, includes_laundry):
        """Create a new property and save it to the database."""
        property_id = DatabaseManager.generate_uuid_for_rental(address, unit)
        db = DatabaseManager.get_db(DatabaseType.PROPERTY)
        cursor = db.cursor()
        cursor.execute('''
                INSERT INTO properties (id, address, unit, owner, available_date, rent_per_month, 
                bedrooms, bathrooms, parking_available, parking_per_month, includes_water, 
                includes_heating, includes_electricity, includes_laundry)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (property_id, address, unit, owner, available_date, rent_per_month, bedrooms,
                  bathrooms, parking_available, parking_per_month, includes_water,
                  includes_heating, includes_electricity, includes_laundry))
        db.commit()
        return property_id

    @staticmethod
    def delete_property(property_id):
        """Delete a property from the property database."""
        db = DatabaseManager.get_db(DatabaseType.PROPERTY)
        cursor = db.cursor()
        cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
        db.commit()

    @staticmethod
    def init_user_db():
        """Create the 'users' table if it doesn't exist."""
        db = DatabaseManager.get_db(DatabaseType.USER)
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                uuid TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                account_type INTEGER NOT NULL,
                token_2fa TEXT
            );
        ''')
        db.commit()

    @staticmethod
    def create_user(email, password, account_type):
        """Create a new user in the database."""
        usr_id = DatabaseManager.generate_uuid_for_user(email)
        db = DatabaseManager.get_db(DatabaseType.USER)
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO users (uuid, email, password, account_type)
            VALUES (?, ?, ?, ?);
        ''', (usr_id, email, password, account_type.value))
        db.commit()
        return usr_id

    @staticmethod
    def delete_user(user_uuid):
        """Delete a user from the database."""
        db = DatabaseManager.get_db(DatabaseType.USER)
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE uuid = ?", (user_uuid,))
        db.commit()

    @staticmethod
    def init_databases():
        """Initialize both databases."""
        DatabaseManager.init_user_db()
        DatabaseManager.init_property_db()
