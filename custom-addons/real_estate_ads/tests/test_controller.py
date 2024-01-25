from odoo import tests
from odoo.tests import HttpCase


@tests.tagged("post_install", "-at_install")
class TestPropertyController(HttpCase):
    def setUp(self):
        super(TestPropertyController, self).setUp()

        self.Property = self.env["estate.property"]
        self.test_property = self.Property.create(
            {
                "name": "Test Property",
                "description": "Test Description",
                "expected_price": 100000,
            }
        )

    def test_show_properties(self):
        """Test the show_properties controller"""
        response = self.url_open("/properties")

        self.assertTrue(response.status_code == 200)
        self.assertIn("Test Property", response.text)
