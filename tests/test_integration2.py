from base_test_class import BaseTestClass
from app.models import Property

class IntegrationTests(BaseTestClass):

    def test_new_property(self):
        """Test the property addition process"""
        response = self.client.post('/add_property', data=dict(
            streetAddress='3434 Integration Blvd',
            ptype='House',
            sqft='2100',
            bdr='4',
            btr='2',
            price='1850',
            availability='available'
        ), follow_redirects=True)

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Property added successfully", response.data)

        # Ensure the property exists in the database
        property_in_db = self.db.session.query(Property).filter_by(address='3434 Integration Blvd').first()
        self.assertIsNotNone(property_in_db)
        self.assertEqual(property_in_db.property_type, 'House')
        self.assertEqual(property_in_db.square_footage, 2100)
        self.assertEqual(property_in_db.bedrooms, 4)
        self.assertEqual(property_in_db.bathrooms, 2)
        self.assertEqual(property_in_db.rent_per_month, 1850)
        self.assertTrue(property_in_db.available)