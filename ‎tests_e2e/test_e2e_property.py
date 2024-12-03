from base_test_class import BaseTestClass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AddPropertyTests(BaseTestClass):
    def test_add_property(self):
        """Test process for adding a property"""

        ap_path = self.getFullWebPath('/add_property')
        self.driver.get(ap_path)

        test_address = '123 Test St'
        test_property_type = 'House'
        test_sqft = '4800'
        test_bdr = '4'
        test_btr = '2'
        test_rent = '2700'

        property_address_input = self.driver.find_element(By.NAME, 'streetAddress')
        property_address_input.send_keys(test_address)

        property_ptype_input = self.driver.find_element(By.NAME, 'ptype')
        property_ptype_input.send_keys(test_property_type)

        property_sqft_input = self.driver.find_element(By.NAME, 'sqft')
        property_sqft_input.send_keys(test_sqft)

        property_bdr_input = self.driver.find_element(By.NAME, 'bdr')
        property_bdr_input.send_keys(test_bdr)

        property_btr_input = self.driver.find_element(By.NAME, 'btr')
        property_btr_input.send_keys(test_btr)

        property_rent_input = self.driver.find_element(By.NAME, 'price')
        property_rent_input.send_keys(test_rent)

        availability_dropdown = self.driver.find_element(By.NAME, 'availability')
        for option in availability_dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == 'Available':
                option.click()
                break

        save = self.driver.find_element(By.CLASS_NAME, 'OptionsButton')
        save.click()

        
        