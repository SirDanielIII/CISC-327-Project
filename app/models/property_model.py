from ..database.database_manager import DatabaseManager, DatabaseType


class Property:
    def __init__(self, property_id: int):
        self.id = property_id
        self.owner = []
        self.available_date = None
        self.address = None
        self.unit = None
        # Details
        self.rent_per_month = None
        self.bedrooms = None
        self.bathrooms = None
        self.parking_available = None
        self.parking_per_month = None
        self.includes_water = None
        self.includes_heating = None
        self.includes_electricity = None
        self.includes_laundry = None
        # For tenants
        tenants = []
        lease_agreement = None
        # Load information from database
        self.load_property_from_db()

    def load_property_from_db(self):
        """Load property details from the property database."""
        db = DatabaseManager.get_db(DatabaseType.PROPERTY)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM properties WHERE id = ?", (self.id,))
        row = cursor.fetchone()
        if row:
            self.address = row['address']
            self.unit = row['unit']
            self.owner = row['owner']
            self.available_date = row['available_date']
            self.rent_per_month = row['rent_per_month']
            self.bedrooms = row['bedrooms']
            self.bathrooms = row['bathrooms']
            self.parking_available = row['parking_available']
            self.parking_per_month = row['parking_per_month']
            self.includes_water = row['includes_water']
            self.includes_heating = row['includes_heating']
            self.includes_electricity = row['includes_electricity']
            self.includes_laundry = row['includes_laundry']

    def save_to_db(self, field, value):
        """Save a field update to the property database."""
        db = DatabaseManager.get_db(DatabaseType.PROPERTY)
        cursor = db.cursor()
        cursor.execute(f"UPDATE properties SET {field} = ? WHERE id = ?", (value, self.id))
        db.commit()

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address
        self.save_to_db("address", address)

    def get_unit(self):
        return self.unit

    def set_unit(self, unit):
        self.unit = unit
        self.save_to_db("unit", unit)

    def get_owner(self):
        return self.owner

    def set_owner(self, owner):
        self.owner = owner
        self.save_to_db("owner", owner)

    def get_available_date(self):
        return self.available_date

    def set_available_date(self, available_date):
        self.available_date = available_date
        self.save_to_db("available_date", available_date)

    def get_rent_per_month(self):
        return self.rent_per_month

    def set_rent_per_month(self, rent):
        self.rent_per_month = rent
        self.save_to_db("rent_per_month", rent)

    def get_bedrooms(self):
        return self.bedrooms

    def set_bedrooms(self, bedrooms):
        self.bedrooms = bedrooms
        self.save_to_db("bedrooms", bedrooms)

    def get_bathrooms(self):
        return self.bathrooms

    def set_bathrooms(self, bathrooms):
        self.bathrooms = bathrooms
        self.save_to_db("bathrooms", bathrooms)

    def get_parking_available(self):
        return self.parking_available

    def set_parking_available(self, available):
        self.parking_available = available
        self.save_to_db("parking_available", available)

    def get_parking_per_month(self):
        return self.parking_per_month

    def set_parking_per_month(self, parking_cost):
        self.parking_per_month = parking_cost
        self.save_to_db("parking_per_month", parking_cost)

    def get_includes_water(self):
        return self.includes_water

    def set_includes_water(self, includes_water):
        self.includes_water = includes_water
        self.save_to_db("includes_water", includes_water)

    def get_includes_heating(self):
        return self.includes_heating

    def set_includes_heating(self, includes_heating):
        self.includes_heating = includes_heating
        self.save_to_db("includes_heating", includes_heating)

    def get_includes_electricity(self):
        return self.includes_electricity

    def set_includes_electricity(self, includes_electricity):
        self.includes_electricity = includes_electricity
        self.save_to_db("includes_electricity", includes_electricity)

    def get_includes_laundry(self):
        return self.includes_laundry

    def set_includes_laundry(self, includes_laundry):
        self.includes_laundry = includes_laundry
        self.save_to_db("includes_laundry", includes_laundry)
