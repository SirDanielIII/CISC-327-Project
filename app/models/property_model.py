from ..database import db

class Property(db.Model):
    __tablename__ = 'Properties'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    address = db.Column(db.String(150), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    property_type = db.Column(db.String(60), nullable=False)
    square_footage = db.Column(db.Integer, nullable=False)

    owner = db.relationship('User', back_populates='properties')