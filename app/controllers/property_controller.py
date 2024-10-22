from flask import Blueprint, render_template, request, redirect, abort, url_for, flash
from flask_login import login_required, current_user
from .helpers.role_required_wrapper import role_required
from enums.AccountType import AccountType
from models.property_model import Property
from models import in_memory_properties
from database.database_manager import DatabaseManager

property_blueprint = Blueprint('property', __name__)

@property_blueprint.route('/properties', methods=['GET', 'POST'])
@login_required
@role_required(AccountType.PROPERTY_OWNER)
def get_properties():
    if request.method == 'POST':
        ids = request.form['property_ids']
        parsed_ids = ids.split(',')
        deleted_count = 0
        for i in reversed(range(len(in_memory_properties))):
            property = in_memory_properties[i]
            for parsed_id in parsed_ids:
                if property.id == parsed_id:
                    for owner in property.owner:
                        if current_user.uuid == owner:
                            in_memory_properties.remove(property)
                            deleted_count+=1
        flash(f'Successfully deleted {deleted_count} properties.',category='success')
        return redirect(url_for('property.get_properties'))

    user_properties = []
    for property in in_memory_properties:
        for property_owner in property.owner:
            if property_owner == current_user.uuid:
                user_properties.append(property)
    return render_template('managementProperties/properties.html', properties=user_properties)

@property_blueprint.route('/property_details/<id>', methods=['GET', 'POST'])
@login_required
@role_required(AccountType.PROPERTY_OWNER)
def property_details(id):
    found_property = None
    for property in in_memory_properties:
        if property.id == id:
            found_property = property
            break
    
    if found_property == None:
        return abort(404)
    
    belongs_to_user = False
    for owner in property.owner:
        if current_user.uuid == owner:
            belongs_to_user = True
            break
    
    if not belongs_to_user:
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

    property_id = DatabaseManager.generate_uuid_for_rental(address, None)
    new_property = Property(property_id)
    new_property.address = address
    new_property.property_type = property_type
    new_property.sqrFtg = sqrFtg
    new_property.bedrooms = bedrooms
    new_property.bathrooms = bathrooms
    new_property.rent_per_month = rent_price
    new_property.available = availability == 'available'
    new_property.owner.append(current_user.uuid)

    in_memory_properties.append(new_property)
    flash(f'Successfully added the new property.',category='success')
    return redirect(url_for('property.property_details', id=new_property.id))
    