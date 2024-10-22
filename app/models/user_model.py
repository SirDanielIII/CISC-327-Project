import hashlib
import secrets
from flask_login import UserMixin

from database.database_manager import DatabaseManager, DatabaseType
from enums.AccountType import AccountType


class User(UserMixin):
    def __init__(self, user_uuid):
        self.uuid = user_uuid
        self.email = None
        self.password = None
        self.account_type = None
        self.token_2fa = None

        # Properties associated with the user
        self.applied_properties = []  # Properties the tenant applied to
        self.current_properties = []  # Properties the tenant is currently living in
        self.managed_properties = []  # Properties managed by the property owner
        self.lease_agreements = []  # Lease agreements associated with the user

        # Load user and associated properties from the database
        #self.load_user_from_db()
        #self.load_associated_properties()

    def get_id(self):
        return self.uuid

    def load_user_from_db(self):
        """Load user details from the user database."""
        db = DatabaseManager.get_db(DatabaseType.USER)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE uuid = ?", (self.uuid,))
        row = cursor.fetchone()
        if row:
            self.email = row['email']
            self.password = row['password']
            self.account_type = AccountType(row['account_type'])
            self.token_2fa = row['token_2fa']
            return True
        return False

    def load_associated_properties(self):
        """Load associated properties based on the user's role."""
        db = DatabaseManager.get_db(DatabaseType.PROPERTY)
        cursor = db.cursor()

        if self.account_type == AccountType.TENANT:
            cursor.execute("SELECT property_id FROM applications WHERE user_id = ?", (self.uuid,))
            self.applied_properties = [row['property_id'] for row in cursor.fetchall()]

            cursor.execute("SELECT property_id FROM tenants WHERE user_id = ?", (self.uuid,))
            self.current_properties = [row['property_id'] for row in cursor.fetchall()]

        elif self.account_type == AccountType.PROPERTY_OWNER:
            cursor.execute("SELECT id FROM properties WHERE owner = ?", (self.uuid,))
            self.managed_properties = [row['id'] for row in cursor.fetchall()]

    def save_to_db(self, field, value):
        """Save a field update to the user database."""
        db = DatabaseManager.get_db(DatabaseType.USER)
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET {field} = ? WHERE uuid = ?", (value, self.uuid))
        db.commit()

    # Getters and Setters
    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email
        self.save_to_db("email", email)

    def get_password(self):
        return self.password

    def set_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.password = hashed_password
        self.save_to_db("password", hashed_password)

    def get_account_type(self):
        return self.account_type

    def set_account_type(self, account_type):
        self.account_type = account_type
        self.save_to_db("account_type", account_type.value)

    def get_token_2fa(self):
        return self.token_2fa

    def set_token_2fa(self, token):
        self.token_2fa = token
        self.save_to_db("token_2fa", token)

    # 2FA Token Management
    def generate_2fa_token(self):
        """Generate a new 2FA token."""
        token = secrets.token_hex(16)
        self.set_token_2fa(token)
        return token

    def check_2fa_token(self, token):
        """Verify if the provided 2FA token matches the stored one."""
        return self.token_2fa == token

    # Password Verification
    def check_password(self, password):
        """Check if the provided password matches the stored one."""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == self.password

    # Role-based Methods

    def apply_for_property(self, property_id):
        """Allow tenants to apply for a property."""
        if self.account_type != AccountType.TENANT:
            raise PermissionError("Only tenants can apply for properties.")
        db = DatabaseManager.get_db(DatabaseType.PROPERTY)
        cursor = db.cursor()
        cursor.execute("INSERT INTO applications (user_id, property_id) VALUES (?, ?)", (self.uuid, property_id))
        db.commit()
        self.applied_properties.append(property_id)

    def delete_application(self, property_id):
        """Allow tenants to delete an application for a property."""
        if self.account_type != AccountType.TENANT:
            raise PermissionError("Only tenants can delete applications.")
        db = DatabaseManager.get_db(DatabaseType.PROPERTY)
        cursor = db.cursor()
        cursor.execute("DELETE FROM applications WHERE user_id = ? AND property_id = ?", (self.uuid, property_id))
        db.commit()
        self.applied_properties.remove(property_id)

    def remove_current_property(self, property_id):
        """Allow tenants to remove a property they are currently renting."""
        if self.account_type != AccountType.TENANT:
            raise PermissionError("Only tenants can remove current properties.")
        db = DatabaseManager.get_db(DatabaseType.PROPERTY)
        cursor = db.cursor()
        cursor.execute("DELETE FROM tenants WHERE user_id = ? AND property_id = ?", (self.uuid, property_id))
        db.commit()
        self.current_properties.remove(property_id)

    def create_property(self, address, unit, **kwargs):
        """Allow property owners to create properties."""
        if self.account_type != AccountType.PROPERTY_OWNER:
            raise PermissionError("Only property owners can create properties.")
        property_id = DatabaseManager.create_property(address=address, unit=unit, owner=self.uuid, **kwargs)
        self.managed_properties.append(property_id)

    def delete_property(self, property_id):
        """Allow property owners to delete managed properties."""
        if self.account_type != AccountType.PROPERTY_OWNER:
            raise PermissionError("Only property owners can delete properties.")
        DatabaseManager.delete_property(property_id)
        self.managed_properties.remove(property_id)

    def create_user(self, email, password, account_type):
        """Allow admins to create new users."""
        if self.account_type != AccountType.ADMINISTRATOR:
            raise PermissionError("Only administrators can create users.")
        return DatabaseManager.create_user(email, password, account_type)

    def delete_user(self, user_uuid):
        """Allow admins to delete users."""
        if self.account_type != AccountType.ADMINISTRATOR:
            raise PermissionError("Only administrators can delete users.")
        DatabaseManager.delete_user(user_uuid)

    # View Properties Methods

    def view_applied_properties(self):
        """View properties the tenant applied to."""
        return self.applied_properties

    def view_current_properties(self):
        """View properties where the tenant currently lives."""
        return self.current_properties

    def view_managed_properties(self):
        """View properties managed by the property owner."""
        return self.managed_properties
