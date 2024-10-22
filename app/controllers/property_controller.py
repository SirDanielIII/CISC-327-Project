from flask import Blueprint, render_template, request, redirect, abort, url_for
from flask_login import login_required, current_user
from .helpers.role_required_wrapper import role_required
from models.user_model import UserRoles
from models.property_model import Property
from models import in_memory_properties

property_blueprint = Blueprint('property', __name__)

@property_blueprint.route('/properties', methods=['GET'])
@login_required
@role_required(UserRoles.PROPERTY_OWNER)
def get_properties():
    user_properties = []
    for property in in_memory_properties:
        if property.owner_id == current_user.id:
            user_properties.append(property)
    return render_template('managementProperties/properties.html', properties=user_properties)

@property_blueprint.route('/property_details/<id>', methods=['GET', 'POST', 'DELETE'])
@login_required
@role_required(UserRoles.PROPERTY_OWNER)
def property_details(id):
    found_property = None
    for property in in_memory_properties:
        if property.id == id:
            found_property = property
            break
    
    if found_property == None:
        return abort(404)
    
    if request.method == 'DELETE':
        in_memory_properties.remove(found_property)
        return redirect(url_for('property.properties'))
    
    if request.method == 'POST':
        # Update property here
        pass

    return render_template('managementProperties/property.html', property=found_property)

@property_blueprint.route('/add_property', methods=['GET', 'POST'])
@login_required
@role_required(UserRoles.PROPERTY_OWNER)
def add_property():
    if request.method == 'GET':
        return render_template('managementProperties/property.html')
    # New property being added
    new_property = Property(current_user.id)
    in_memory_properties.append(new_property)
    return redirect(url_for('property.property_details', id=new_property.id))
    