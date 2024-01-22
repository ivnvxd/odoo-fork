from odoo.tests.common import TransactionCase


class TestPropertyTag(TransactionCase):
    def setUp(self):
        super(TestPropertyTag, self).setUp()

        self.PropertyTag = self.env["estate.property.tag"]

        self.test_tag_data = {
            "name": "Test Tag",
            "color": 10,
        }

    def test_tag_creation(self):
        """Test creation of a property tag"""
        tag = self.PropertyTag.create(self.test_tag_data)

        self.assertEqual(tag.name, "Test Tag")
        self.assertEqual(tag.color, 10)

    def test_tag_update(self):
        """Test updating a property tag"""
        tag = self.PropertyTag.create(self.test_tag_data)
        tag.write({"name": "Updated Tag Name", "color": 20})

        self.assertEqual(tag.name, "Updated Tag Name")
        self.assertEqual(tag.color, 20)
