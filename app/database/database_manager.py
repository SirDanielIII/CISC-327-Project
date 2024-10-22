import os
import sqlite3
import uuid
from enum import Enum

from flask import g


class DatabaseType(Enum):
    USER = 'user'
    PROPERTY = 'property'


class DatabaseManager(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    USER_DB_PATH = os.path.join(BASE_DIR, 'user_database.db')
    PROPERTY_DB_PATH = os.path.join(BASE_DIR, 'property_database.db')

    @staticmethod
    def get_db(db_type: DatabaseType):
        """Get a database connection (either USER or PROPERTY)."""
        if db_type.value not in g:
            db_path = (DatabaseManager.USER_DB_PATH if db_type == DatabaseType.USER else DatabaseManager.PROPERTY_DB_PATH)
            g[db_type.value] = sqlite3.connect(db_path)
            g[db_type.value].row_factory = sqlite3.Row  # Access columns by name
        return g[db_type.value]

    @staticmethod
    def close_db(exception=None):
        """Close the database connections."""
        for db_type in [DatabaseType.USER, DatabaseType.PROPERTY]:
            db = g.pop(db_type.value, None)
            if db:
                db.close()

    @staticmethod
    def generate_uuid(address, unit):
        """Generate a UUID based on address and unit."""
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{address}-{unit}"))

    @staticmethod
    def init_databases():
        """Initialize both user and property databases."""
        DatabaseManager.init_user_db()
        DatabaseManager.init_property_db()

    @staticmethod
    def init_user_db():
        """Initialize the user database with the 'users' table."""
        db = DatabaseManager.get_db(DatabaseType.USER)
        cursor = db.cursor()
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
        property_id = DatabaseManager.generate_uuid(address, unit)
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
