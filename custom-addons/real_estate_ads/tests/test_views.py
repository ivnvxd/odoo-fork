from odoo import tests
from odoo.tests.common import HttpCase


@tests.tagged("post_install", "-at_install")
class TestPropertyViews(HttpCase):
    def setUp(self):
        super(TestPropertyViews, self).setUp()
        self.Property = self.env["estate.property"]

    def test_property_tree_view(self):
        tree_view = self.env.ref("real_estate_ads.estate_property_tree_view")

        self.assertTrue(tree_view, "Tree view not found")
        self.assertIn("name", tree_view.arch_db, "Name field not in tree view")
        self.assertIn("postcode", tree_view.arch_db, "Postcode field not in tree view")

    def test_property_form_view(self):
        form_view = self.env.ref("real_estate_ads.estate_property_form_view")

        self.assertTrue(form_view, "Form view not found")
        self.assertIn("name", form_view.arch_db, "Name field not in form view")
        self.assertIn(
            'widget="char_emojis"', form_view.arch_db, "Char emojis widget not found"
        )

    def test_property_pivot_view(self):
        pivot_view = self.env.ref("real_estate_ads.estate_property_pivot_view")
        self.assertTrue(pivot_view, "Pivot view not found")
        self.assertIn("name", pivot_view.arch_db, "Name field not in pivot view")

    def test_property_graph_view(self):
        graph_view = self.env.ref("real_estate_ads.estate_property_graph_view")

        self.assertTrue(graph_view, "Graph view not found")
        self.assertIn(
            "selling_price", graph_view.arch_db, "Selling price field not in graph view"
        )

    def test_property_kanban_view(self):
        kanban_view = self.env.ref("real_estate_ads.estate_property_kanban_view")

        self.assertTrue(kanban_view, "Kanban view not found")
        self.assertIn(
            '<t t-name="kanban-box">',
            kanban_view.arch_db,
            "Kanban box template not found",
        )

    def test_property_search_view(self):
        search_view = self.env.ref("real_estate_ads.estate_property_search_view")

        self.assertTrue(search_view, "Search view not found")
        self.assertIn(
            'filter string="New"', search_view.arch_db, "New filter not found"
        )

    def test_property_offer_tree_view(self):
        tree_view = self.env.ref("real_estate_ads.estate_property_offer_tree_view")

        self.assertTrue(tree_view, "Property offer tree view not found")
        self.assertIn("price", tree_view.arch_db, "Price field not in tree view")

    def test_property_offer_form_view(self):
        form_view = self.env.ref("real_estate_ads.estate_property_offer_form_view")

        self.assertTrue(form_view, "Property offer form view not found")
        self.assertIn(
            "partner_id", form_view.arch_db, "Partner ID field not in form view"
        )

    def test_property_tag_tree_view(self):
        tree_view = self.env.ref("real_estate_ads.estate_property_tag_tree_view")

        self.assertTrue(tree_view, "Property tag tree view not found")
        self.assertIn("name", tree_view.arch_db, "Name field not in tree view")

    def test_property_tag_form_view(self):
        form_view = self.env.ref("real_estate_ads.estate_property_tag_form_view")

        self.assertTrue(form_view, "Property tag form view not found")
        self.assertIn("color", form_view.arch_db, "Color field not in form view")

    def test_property_type_tree_view(self):
        tree_view = self.env.ref("real_estate_ads.estate_property_type_tree_view")

        self.assertTrue(tree_view, "Property type tree view not found")
        self.assertIn("name", tree_view.arch_db, "Name field not in tree view")

    def test_property_type_form_view(self):
        form_view = self.env.ref("real_estate_ads.estate_property_type_form_view")

        self.assertTrue(form_view, "Property type form view not found")
        self.assertIn("name", form_view.arch_db, "Name field not in form view")
