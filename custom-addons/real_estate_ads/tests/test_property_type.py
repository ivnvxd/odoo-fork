from odoo.tests.common import TransactionCase


class TestPropertyType(TransactionCase):
    def setUp(self):
        super(TestPropertyType, self).setUp()

        self.PropertyType = self.env["estate.property.type"]

        self.test_type_data = {"name": "Test Type"}

    def test_type_creation(self):
        """Test creation of a property type"""
        property_type = self.PropertyType.create(self.test_type_data)

        self.assertEqual(property_type.name, "Test Type")

    def test_type_update(self):
        """Test updating a property type"""
        property_type = self.PropertyType.create(self.test_type_data)
        property_type.write({"name": "Updated Type Name"})

        self.assertEqual(property_type.name, "Updated Type Name")
