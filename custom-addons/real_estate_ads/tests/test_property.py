from odoo.tests.common import TransactionCase


class TestProperty(TransactionCase):
    def setUp(self):
        super(TestProperty, self).setUp()
        self.test_user = self.env["res.users"].create(
            {"name": "Test User", "login": "test_user", "email": "test@example.com"}
        )

        self.property_type = self.env["estate.property.type"].create(
            {"name": "Test Type"}
        )

        self.test_property_data = {
            "name": "Test Property",
            "description": "Test Description",
            "expected_price": 100000,
            "sales_id": self.test_user.id,
            "type_id": self.property_type.id,
        }

        self.Property = self.env["estate.property"]

    def test_property_creation(self):
        """Test creation of a property"""
        property_record = self.Property.create(self.test_property_data)

        self.assertEqual(property_record.name, "Test Property")
        self.assertEqual(property_record.description, "Test Description")
        self.assertEqual(property_record.expected_price, 100000)
        self.assertEqual(property_record.sales_id.id, self.test_user.id)

    def test_property_update(self):
        """Test updating property fields"""
        property_record = self.Property.create(self.test_property_data)
        property_record.write({"name": "Updated Property Name"})

        self.assertEqual(property_record.name, "Updated Property Name")

    def test_compute_best_offer(self):
        """Test computation of the best offer"""
        property_record = self.Property.create(self.test_property_data)
        self.env["estate.property.offer"].create(
            {"price": 110000, "property_id": property_record.id}
        )
        self.env["estate.property.offer"].create(
            {"price": 120000, "property_id": property_record.id}
        )
        property_record._compute_best_price()

        self.assertEqual(property_record.best_offer, 120000)

    def test_action_sold(self):
        """Test the action_sold method"""
        property_record = self.Property.create(self.test_property_data)
        property_record.action_sold()

        self.assertEqual(property_record.state, "sold")

    def test_action_cancel(self):
        """Test the action_cancel method"""
        property_record = self.Property.create(self.test_property_data)
        property_record.action_cancel()

        self.assertEqual(property_record.state, "cancel")
