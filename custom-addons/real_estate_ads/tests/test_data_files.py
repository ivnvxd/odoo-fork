from odoo.tests.common import TransactionCase


class TestDataFiles(TransactionCase):
    def setUp(self):
        super(TestDataFiles, self).setUp()
        self.PropertyType = self.env["estate.property.type"]
        self.MailTemplate = self.env["mail.template"]

    def test_property_types_loaded(self):
        """Test if property types from CSV and XML are correctly loaded"""
        # List of expected property types
        expected_types = ["House", "Apartment", "Penthouse", "Castle"]

        # Check each type is correctly loaded
        for prop_type in expected_types:
            type_record = self.PropertyType.search([("name", "=", prop_type)])
            self.assertTrue(
                type_record, f"Property type '{prop_type}' should be loaded"
            )

    def test_mail_template_loaded(self):
        """Test if mail template is correctly loaded"""
        template = self.MailTemplate.search(
            [("model_id.model", "=", "estate.property")]
        )
        self.assertTrue(template, "Mail template for estate.property should be loaded")
        self.assertEqual(
            template.email_from,
            "from@email.com",
            "Mail template 'email_from' field mismatch",
        )
        self.assertEqual(
            template.subject,
            "New Information on {{object.name}}",
            "Mail template 'subject' field mismatch",
        )
