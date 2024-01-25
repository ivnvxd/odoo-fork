from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestSecurityRules(TransactionCase):
    def setUp(self):
        super(TestSecurityRules, self).setUp()
        self.Property = self.env["estate.property"]
        self.PropertyType = self.env["estate.property.type"]
        self.PropertyTag = self.env["estate.property.tag"]
        self.PropertyOffer = self.env["estate.property.offer"]

        # Create users based on security groups
        self.property_user = self.env.ref("real_estate_ads.group_property_user")
        self.property_manager = self.env.ref("real_estate_ads.group_property_manager")
        self.demo_user = self.env.ref("base.user_demo")
        self.admin_user = self.env.ref("base.user_admin")

        # Create test records
        self.test_property = self.Property.with_user(self.admin_user).create(
            {"name": "Test Property", "sales_id": self.demo_user.id}
        )
        self.test_property_type = self.PropertyType.with_user(self.admin_user).create(
            {"name": "Test Property Type"}
        )
        self.test_property_tag = self.PropertyTag.with_user(self.admin_user).create(
            {"name": "Test Property Tag"}
        )
        self.test_property_offer = self.PropertyOffer.with_user(self.admin_user).create(
            {"name": "Test Property Offer", "property_id": self.test_property.id}
        )

    def test_property_user_access(self):
        """Test property user access rights"""
        # User should have read, write, create, unlink access to their own properties
        property_user_env = self.env(user=self.demo_user)
        self.Property = self.Property.with_env(property_user_env)
        self.Property.create({"name": "New Property", "sales_id": self.demo_user.id})
        test_property = self.Property.search([("name", "=", "New Property")])
        test_property.write({"name": "Updated Property"})
        test_property.unlink()

        # User should not have access to other's properties
        with self.assertRaises(AccessError):
            self.Property.create(
                {"name": "Other Property", "sales_id": self.admin_user.id}
            )

    def test_property_manager_access(self):
        """Test property manager access rights"""
        # Manager should have full access to all properties
        property_manager_env = self.env(user=self.admin_user)
        self.Property = self.Property.with_env(property_manager_env)

        # Test Create
        created_property = self.Property.create({"name": "Manager Property"})
        self.assertTrue(created_property, "Property should be created by manager")

        # Test Search
        test_property = self.Property.search([("name", "=", "Manager Property")])
        self.assertEqual(
            test_property.name,
            "Manager Property",
            "Property should be found by manager",
        )

        # Test Write
        test_property.write({"name": "Updated Manager Property"})
        self.assertEqual(
            test_property.name,
            "Updated Manager Property",
            "Property should be updated by manager",
        )

        # Test Unlink
        property_id = test_property.id
        test_property.unlink()
        self.assertFalse(
            self.Property.search([("id", "=", property_id)]),
            "Property should be deleted by manager",
        )

    def test_property_type_access(self):
        """Test property type access for manager and normal users"""
        # Verify manager has full access to property types
        property_manager_env = self.env(user=self.admin_user)
        self.PropertyType = self.PropertyType.with_env(property_manager_env)
        manager_type = self.PropertyType.create({"name": "Manager Type"})
        manager_type.write({"name": "Updated Manager Type"})
        manager_type.unlink()

        # Verify normal user should not have access to create, write, unlink property types
        property_user_env = self.env(user=self.demo_user)
        self.PropertyType = self.PropertyType.with_env(property_user_env)

        # Test creation access
        with self.assertRaises(AccessError):
            self.PropertyType.create({"name": "User New Type"})

        # Setup a property type record to test write and unlink access
        user_type = self.PropertyType.sudo().create({"name": "User Test Type"})

        # Test write access
        with self.assertRaises(AccessError):
            user_type.with_user(self.demo_user).write({"name": "User Updated Type"})

        # Test unlink access
        with self.assertRaises(AccessError):
            user_type.with_user(self.demo_user).unlink()
