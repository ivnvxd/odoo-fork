from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPropertyOffer(TransactionCase):
    def setUp(self):
        super(TestPropertyOffer, self).setUp()
        self.Property = self.env["estate.property"]
        self.PropertyOffer = self.env["estate.property.offer"]
        self.ResPartner = self.env["res.partner"]

        self.test_property = self.Property.create(
            {
                "name": "Test Property",
                "description": "Test Description",
                "expected_price": 100000,
            }
        )

        self.test_partner = self.ResPartner.create(
            {"name": "Test Partner", "email": "partner@example.com"}
        )

        self.test_offer_data = {
            "price": 120000,
            "property_id": self.test_property.id,
            "partner_id": self.test_partner.id,
            "creation_date": date.today(),
        }

    def test_offer_creation(self):
        """Test creation of a property offer"""
        offer = self.PropertyOffer.create(self.test_offer_data)

        self.assertEqual(offer.price, 120000)
        self.assertEqual(offer.property_id.id, self.test_property.id)
        self.assertEqual(offer.partner_id.id, self.test_partner.id)

    def test_compute_deadline(self):
        """Test deadline computation"""
        offer = self.PropertyOffer.create(self.test_offer_data)
        expected_deadline = date.today() + timedelta(days=offer.validity)

        self.assertEqual(offer.deadline, expected_deadline)

    def test_accept_offer(self):
        """Test offer acceptance logic"""
        offer = self.PropertyOffer.create(self.test_offer_data)
        offer.action_accept_offer()

        self.assertEqual(offer.status, "accepted")
        self.assertEqual(self.test_property.state, "accepted")
        self.assertEqual(self.test_property.selling_price, 120000)

    def test_decline_offer(self):
        """Test offer decline logic"""
        offer = self.PropertyOffer.create(self.test_offer_data)
        offer.action_decline_offer()

        self.assertEqual(offer.status, "refused")

    def test_validity_constraint(self):
        """Test the validity constraint"""

        with self.assertRaises(ValidationError):
            self.PropertyOffer.create(
                {
                    "price": 120000,
                    "property_id": self.test_property.id,
                    "partner_id": self.test_partner.id,
                    "creation_date": date.today(),
                    "validity": -5,
                }
            )
