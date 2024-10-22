from datetime import datetime
import sqlite3


class Property:
    id = None
    owner = []
    available_date = None
    # Details
    rent_per_month = None
    bedrooms = None
    bathrooms = None
    parking_available = None
    parking_per_month = None
    includes_water = None
    includes_heating = None
    includes_electricity = None
    includes_laundry = None
    # For tenants
    tenants = []
    lease_agreement = None

    def __init__(self, property_id: int):
        self.id = property_id
    #     self.load_property_from_db()
    #
    # def load_property_from_db(self):
    #     """Loads property details from the SQLite database using the property ID."""
    #     connection = sqlite3.connect('rental_management.db')
    #     cursor = connection.cursor()
    #
    #     cursor.execute('SELECT * FROM properties WHERE id = ?', (self.id,))
    #     row = cursor.fetchone()
    #     connection.close()
    #
    #     if row:
    #         # Assign attributes based on the loaded row
    #         self.owner = row[1]
    #         self.available_date = datetime.strptime(row[2], '%Y-%m-%d')
    #         self.rent_per_month = row[3]
    #         self.bedrooms = row[4]
    #         self.bathrooms = row[5]
    #         self.parking_available = bool(row[6])
    #         self.parking_per_month = row[7]
    #         self.includes_water = bool(row[8])
    #         self.includes_heating = bool(row[9])
    #         self.includes_electricity = bool(row[10])
    #         self.includes_laundry = bool(row[11])
    #     else:
    #         raise ValueError(f"Property with ID {self.id} not found.")
    #
    # def update_field(self, field_name, new_value):
    #     """Updates both the in-memory value and the database record."""
    #     setattr(self, field_name, new_value)
    #
    #     connection = sqlite3.connect('rental_management.db')
    #     cursor = connection.cursor()
    #
    #     cursor.execute(f'UPDATE properties SET {field_name} = ? WHERE id = ?', (new_value, self.id))
    #
    #     connection.commit()
    #     connection.close()
    #
    # def __str__(self):
    #     return (f"Property(owner={self.owner}, available_date={self.available_date}, "
    #             f"rent_per_month={self.rent_per_month}, bedrooms={self.bedrooms}, "
    #             f"bathrooms={self.bathrooms}, parking_available={self.parking_available}, "
    #             f"parking_per_month={self.parking_per_month}, includes_water={self.includes_water}, "
    #             f"includes_heating={self.includes_heating}, includes_electricity={self.includes_electricity}, "
    #             f"includes_laundry={self.includes_laundry})")
    #
    # @staticmethod
    # def create_property(owner, available_date, rent_per_month, bedrooms, bathrooms, parking_available,
    #                     parking_per_month, includes_water, includes_heating, includes_electricity, includes_laundry):
    #     """Creates a new property record in the database."""
    #     connection = sqlite3.connect('rental_management.db')
    #     cursor = connection.cursor()
    #
    #     cursor.execute('''
    #     INSERT INTO properties (owner, available_date, rent_per_month, bedrooms, bathrooms, parking_available,
    #                             parking_per_month, includes_water, includes_heating, includes_electricity, includes_laundry)
    #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #     ''', (owner, available_date.strftime('%Y-%m-%d'), rent_per_month, bedrooms, bathrooms,
    #           parking_available, parking_per_month, includes_water, includes_heating, includes_electricity, includes_laundry))
    #
    #     connection.commit()
    #     connection.close()
    #
    # @staticmethod
    # def delete_property(property_id: int):
    #     """Deletes a property from the database by its ID."""
    #     connection = sqlite3.connect(DB_PATH)
    #     cursor = connection.cursor()
    #
    #     cursor.execute('DELETE FROM properties WHERE id = ?', (property_id,))
    #     connection.commit()
    #     connection.close()
