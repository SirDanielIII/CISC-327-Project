from flask import Blueprint, render_template, request, redirect, abort, url_for, flash
from flask_login import login_required, current_user
from .helpers.role_required_wrapper import role_required
from ..enums.AccountType import AccountType
from ..models.property_model import Property
from ..database import db

property_blueprint = Blueprint('property', __name__)

@property_blueprint.route('/properties', methods=['GET', 'POST'])
@login_required
@role_required(AccountType.PROPERTY_OWNER)
def get_properties():
    if request.method == 'POST':
        ids = request.form['property_ids']
        parsed_ids = ids.split(',')
        deleted_count = db.session.query(Property).filter(Property.id.in_(parsed_ids),
                            Property.owner_id == current_user.id).delete(synchronize_session='fetch')
        db.session.commit()
        flash(f'Successfully deleted {deleted_count} properties.',category='success')
        return redirect(url_for('property.get_properties'))

    return render_template('managementProperties/properties.html', properties=current_user.properties)

@property_blueprint.route('/property_details/<id>', methods=['GET', 'POST'])
@login_required
@role_required(AccountType.PROPERTY_OWNER)
def property_details(id: int):
    found_property = db.session.get(Property, id)
    
    if found_property == None:
        return abort(404)
    
    if found_property.owner_id != current_user.id:
        # Property does not belong to requesting user
        return abort(403)
    
    if request.method == 'POST':
        address = request.form['streetAddress']
        property_type = request.form['ptype']
        sqrFtg = request.form['sqft']
        bedrooms = request.form['bdr']
        bathrooms = request.form['btr']
        rent_price = request.form['price']
        availability = request.form['availability']

        found_property.address = address
        found_property.property_type = property_type
        found_property.sqrFtg = sqrFtg
        found_property.bedrooms = bedrooms
        found_property.bathrooms = bathrooms
        found_property.rent_per_month = rent_price
        found_property.available = availability == 'available'

        db.session.commit()
        flash(f'Successfully saved all updated property values.',category='success')

    return render_template('managementProperties/property.html', property=found_property)

@property_blueprint.route('/add_property', methods=['GET', 'POST'])
@login_required
@role_required(AccountType.PROPERTY_OWNER)
def add_property():
    if request.method == 'GET':
        return render_template('managementProperties/property.html', property=None)
    # New property being added
    address = request.form['streetAddress']
    property_type = request.form['ptype']
    sqrFtg = request.form['sqft']
    bedrooms = request.form['bdr']
    bathrooms = request.form['btr']
    rent_price = request.form['price']
    availability = request.form['availability']

    new_property = Property()
    new_property.address = address
    new_property.property_type = property_type
    new_property.square_footage = sqrFtg
    new_property.bedrooms = bedrooms
    new_property.bathrooms = bathrooms
    new_property.rent_per_month = rent_price
    new_property.available = availability == 'available'
    new_property.owner_id = current_user.id

    db.session.add(new_property)
    db.session.commit()
    flash(f'Successfully added the new property.',category='success')
    return redirect(url_for('property.property_details', id=new_property.id))
    