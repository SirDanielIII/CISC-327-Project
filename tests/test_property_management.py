from base_test_class import BaseTestClass

class PropertyTests(BaseTestClass):
    def setUp(self) -> None:
        super().setUp()
        self.loginTestUser()

    def test_add_property(self):
        """Test Adding a property"""
        address = '12 Test St'
        property_type = 'Virtual'
        sqrFtg = '12345'
        bedrooms = '4'
        bathrooms = '2'
        rent_price = '1500'
        availability = 'available'

        response = self.client.post('/add_property', data=dict(
            streetAddress=address,
            ptype=property_type,
            sqft=sqrFtg,
            bdr=bedrooms,
            btr=bathrooms,
            price=rent_price,
            availability=availability
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(address), response.data)
        self.assertIn(str.encode(property_type), response.data)
        self.assertIn(str.encode(sqrFtg), response.data)
        self.assertIn(str.encode(bedrooms), response.data)
        self.assertIn(str.encode(bathrooms), response.data)
        self.assertIn(str.encode(rent_price), response.data)
        self.assertIn(b'selected="selected"\n                    \n                    >Available', response.data)

    def test_view_property_details(self):
        """Test viewing a property"""
        address = '123 Test St'
        property_type = 'Virtual'
        sqrFtg = '12345'
        bedrooms = '4'
        bathrooms = '2'
        rent_price = '1500'
        availability = 'available'

        response = self.client.post('/add_property', data=dict(
            streetAddress=address,
            ptype=property_type,
            sqft=sqrFtg,
            bdr=bedrooms,
            btr=bathrooms,
            price=rent_price,
            availability=availability
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(address), response.data)
        self.assertIn(str.encode(property_type), response.data)
        self.assertIn(str.encode(sqrFtg), response.data)
        self.assertIn(str.encode(bedrooms), response.data)
        self.assertIn(str.encode(bathrooms), response.data)
        self.assertIn(str.encode(rent_price), response.data)
        self.assertIn(b'selected="selected"\n                    \n                    >Available', response.data)

        property_id = response.request.path.split('/')[-1]

        response = self.client.get(f'/property_details/{property_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(address), response.data)
        self.assertIn(str.encode(property_type), response.data)
        self.assertIn(str.encode(sqrFtg), response.data)
        self.assertIn(str.encode(bedrooms), response.data)
        self.assertIn(str.encode(bathrooms), response.data)
        self.assertIn(str.encode(rent_price), response.data)
        self.assertIn(b'selected="selected"\n                    \n                    >Available', response.data)


    def test_edit_property(self):
        """Test editing a property"""
        address = '1234 Test St'
        property_type = 'Virtual'
        sqrFtg = '12345'
        bedrooms = '4'
        bathrooms = '2'
        rent_price = '1500'
        availability = 'available'

        response = self.client.post('/add_property', data=dict(
            streetAddress=address,
            ptype=property_type,
            sqft=sqrFtg,
            bdr=bedrooms,
            btr=bathrooms,
            price=rent_price,
            availability=availability
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(address), response.data)
        self.assertIn(str.encode(property_type), response.data)
        self.assertIn(str.encode(sqrFtg), response.data)
        self.assertIn(str.encode(bedrooms), response.data)
        self.assertIn(str.encode(bathrooms), response.data)
        self.assertIn(str.encode(rent_price), response.data)
        self.assertIn(b'selected="selected"\n                    \n                    >Available', response.data)

        property_id = response.request.path.split('/')[-1]

        address='9876 Changed Ave'
        property_type='House'
        sqrFtg='321'
        rent_price='2500'
        bedrooms='7'
        bathrooms='4'
        availability='notAvailable'

        response = self.client.post(f'/property_details/{property_id}', data=dict(
            streetAddress=address,
            ptype=property_type,
            sqft=sqrFtg,
            bdr=bedrooms,
            btr=bathrooms,
            price=rent_price,
            availability=availability
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(address), response.data)
        self.assertIn(str.encode(property_type), response.data)
        self.assertIn(str.encode(sqrFtg), response.data)
        self.assertIn(str.encode(bedrooms), response.data)
        self.assertIn(str.encode(bathrooms), response.data)
        self.assertIn(str.encode(rent_price), response.data)
        self.assertIn(b'selected="selected"\n                    \n                >Not Available', response.data)

    def test_view_properties(self):
        """Test the properties page visibility and
            user properties are visible"""
        response = self.client.get('/properties')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Remove', response.data)
        self.assertIn(b'Add', response.data)

    def test_delete_properties(self):
        """Test deleting two properties at once"""
        address = '12345 Test St'
        property_type = 'Virtual'
        sqrFtg = '12345'
        bedrooms = '4'
        bathrooms = '2'
        rent_price = '1500'
        availability = 'available'

        response = self.client.post('/add_property', data=dict(
            streetAddress=address,
            ptype=property_type,
            sqft=sqrFtg,
            bdr=bedrooms,
            btr=bathrooms,
            price=rent_price,
            availability=availability
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(address), response.data)
        self.assertIn(str.encode(property_type), response.data)
        self.assertIn(str.encode(sqrFtg), response.data)
        self.assertIn(str.encode(bedrooms), response.data)
        self.assertIn(str.encode(bathrooms), response.data)
        self.assertIn(str.encode(rent_price), response.data)
        self.assertIn(b'selected="selected"\n                    \n                    >Available', response.data)

        property_id_1 = response.request.path.split('/')[-1]

        address = '6443 Test St'

        response = self.client.post('/add_property', data=dict(
            streetAddress=address,
            ptype=property_type,
            sqft=sqrFtg,
            bdr=bedrooms,
            btr=bathrooms,
            price=rent_price,
            availability=availability
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str.encode(address), response.data)
        self.assertIn(str.encode(property_type), response.data)
        self.assertIn(str.encode(sqrFtg), response.data)
        self.assertIn(str.encode(bedrooms), response.data)
        self.assertIn(str.encode(bathrooms), response.data)
        self.assertIn(str.encode(rent_price), response.data)
        self.assertIn(b'selected="selected"\n                    \n                    >Available', response.data)

        property_id_2 = response.request.path.split('/')[-1]

        response = self.client.post('/properties', data=dict(
            property_ids=f'{property_id_1},{property_id_2}'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        property_detail_url = '/property_details/'
        self.assertNotIn(str.encode(property_detail_url + property_id_1), response.data)
        self.assertNotIn(str.encode(property_detail_url + property_id_2), response.data)
