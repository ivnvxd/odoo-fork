from odoo.tests.common import TransactionCase


class TestReportGeneration(TransactionCase):
    def setUp(self):
        super(TestReportGeneration, self).setUp()
        self.Property = self.env["estate.property"]
        self.IrActionsReport = self.env["ir.actions.report"]

        # Create a test property record
        self.test_property = self.Property.create(
            {
                "name": "Test Property",
            }
        )

    def test_property_report_generation(self):
        """Test if the property report is correctly generated"""
        # Find the property report action
        property_report = self.IrActionsReport.search(
            [("model", "=", "estate.property"), ("report_type", "=", "qweb-pdf")]
        )
        self.assertTrue(property_report, "Property report action should exist")

        # Render the report
        report_content, report_type = property_report._render(
            property_report, self.test_property.ids
        )
        self.assertTrue(report_content, "Property report should be rendered")
        self.assertEqual(
            report_type,
            "html",
            "Property report should be of type HTML",
        )
