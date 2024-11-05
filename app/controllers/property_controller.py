import re

from flask import Blueprint, render_template, request, redirect, abort, url_for, flash
from flask_login import login_required, current_user

from .helpers.ensure_2fa_verified import ensure_2fa_verified
from .helpers.role_required_wrapper import role_required
from ..database import db
from ..enums.AccountType import AccountType
from ..models.property_model import Property

property_blueprint = Blueprint('property', __name__)


@property_blueprint.route('/properties', methods=['GET', 'POST'])
@login_required
@ensure_2fa_verified
@role_required(AccountType.PROPERTY_OWNER)
def get_properties():
    if request.method == 'POST':
        ids = request.form.get('property_ids')
        if not ids:
            flash('No property IDs provided for deletion.', 'error')
            return redirect(url_for('property.get_properties'))

        parsed_ids = ids.split(',')
        if not all(id_str.isdigit() for id_str in parsed_ids):
            flash('Invalid property IDs provided.', 'error')
            return redirect(url_for('property.get_properties'))

        parsed_ids = [int(id_str) for id_str in parsed_ids]

        deleted_count = db.session.query(Property).filter(
            Property.id.in_(parsed_ids),
            Property.owner_id == current_user.id
        ).delete(synchronize_session='fetch')
        db.session.commit()
        flash(f'Successfully deleted {deleted_count} properties.', category='success')
        return redirect(url_for('property.get_properties'))

    return render_template('managementProperties/properties.html', properties=current_user.properties)


@property_blueprint.route('/property_details/<int:id>', methods=['GET', 'POST'])
@login_required
@ensure_2fa_verified
@role_required(AccountType.PROPERTY_OWNER)
def property_details(id: int):
    found_property = db.session.get(Property, id)

    if found_property is None:
        return abort(404)

    if found_property.owner_id != current_user.id:
        # Property does not belong to requesting user
        return abort(403)

    form_data = {
        'streetAddress': found_property.address,
        'ptype': found_property.property_type,
        'sqft': str(found_property.square_footage),
        'bdr': str(found_property.bedrooms),
        'btr': str(found_property.bathrooms),
        'price': str(found_property.rent_per_month),
        'availability': 'available' if found_property.available else 'unavailable'
    }

    if request.method == 'POST':
        address = request.form.get('streetAddress')
        property_type = request.form.get('ptype')
        sqrFtg = request.form.get('sqft')
        bedrooms = request.form.get('bdr')
        bathrooms = request.form.get('btr')
        rent_price = request.form.get('price')
        availability = request.form.get('availability')

        validation_error = False

        # Update form_data with the new inputs
        form_data.update({
            'streetAddress': address,
            'ptype': property_type,
            'sqft': sqrFtg,
            'bdr': bedrooms,
            'btr': bathrooms,
            'price': rent_price,
            'availability': availability
        })

        if not address:
            flash('Please enter an address.', 'error')
            validation_error = True

        if not property_type:
            flash('Please select a property type.', 'error')
            validation_error = True

        if not sqrFtg or not sqrFtg.isdigit():
            flash('Please enter a valid square footage.', 'error')
            validation_error = True

        if not bedrooms or not bedrooms.isdigit():
            flash('Please enter a valid number of bedrooms.', 'error')
            validation_error = True

        if not bathrooms or not bathrooms.isdigit():
            flash('Please enter a valid number of bathrooms.', 'error')
            validation_error = True

        if not rent_price or not re.match(r'^\d+(\.\d{1,2})?$', rent_price):
            flash('Please enter a valid rent price.', 'error')
            validation_error = True

        if availability not in ['available', 'unavailable']:
            flash('Please select availability status.', 'error')
            validation_error = True

        if validation_error:
            return render_template('managementProperties/property.html', form_data=form_data, property=found_property)

        # Update the property with validated data
        found_property.address = address
        found_property.property_type = property_type
        found_property.square_footage = int(sqrFtg)
        found_property.bedrooms = int(bedrooms)
        found_property.bathrooms = int(bathrooms)
        found_property.rent_per_month = float(rent_price)
        found_property.available = availability == 'available'

        db.session.commit()
        flash('Successfully saved all updated property values.', category='success')
        return redirect(url_for('property.property_details', id=id))

    return render_template('managementProperties/property.html', form_data=form_data, property=found_property)


@property_blueprint.route('/add_property', methods=['GET', 'POST'])
@login_required
@ensure_2fa_verified
@role_required(AccountType.PROPERTY_OWNER)
def add_property():
    form_data = {}

    if request.method == 'POST':
        # Collect form data
        address = request.form.get('streetAddress')
        property_type = request.form.get('ptype')
        sqrFtg = request.form.get('sqft')
        bedrooms = request.form.get('bdr')
        bathrooms = request.form.get('btr')
        rent_price = request.form.get('price')
        availability = request.form.get('availability')

        form_data = {
            'streetAddress': address,
            'ptype': property_type,
            'sqft': sqrFtg,
            'bdr': bedrooms,
            'btr': bathrooms,
            'price': rent_price,
            'availability': availability
        }

        validation_error = False

        if not address:
            flash('Please enter an address.', 'error')
            validation_error = True

        if not property_type:
            flash('Please specify the property type.', 'error')
            validation_error = True

        if not sqrFtg or not sqrFtg.isdigit():
            flash('Please enter a valid square footage.', 'error')
            validation_error = True

        if not bedrooms or not bedrooms.isdigit():
            flash('Please enter a valid number of bedrooms.', 'error')
            validation_error = True

        if not bathrooms or not bathrooms.isdigit():
            flash('Please enter a valid number of bathrooms.', 'error')
            validation_error = True

        if not rent_price or not re.match(r'^\d+(\.\d{1,2})?$', rent_price):
            flash('Please enter a valid rent price.', 'error')
            validation_error = True

        if availability not in ['available', 'unavailable']:
            flash('Please select availability status.', 'error')
            validation_error = True

        if validation_error:
            return render_template('managementProperties/property.html', form_data=form_data, property=None)

        new_property = Property(
            address=address,
            property_type=property_type,
            square_footage=int(sqrFtg),
            bedrooms=int(bedrooms),
            bathrooms=int(bathrooms),
            rent_per_month=float(rent_price),
            available=(availability == 'available'),
            owner_id=current_user.id
        )

        db.session.add(new_property)
        db.session.commit()
        flash('Successfully added the new property.', category='success')
        return redirect(url_for('property.property_details', id=new_property.id))

    return render_template('managementProperties/property.html', form_data=form_data, property=None)
