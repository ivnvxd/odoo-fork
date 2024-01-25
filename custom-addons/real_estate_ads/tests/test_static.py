from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install")
class TestStaticFiles(HttpCase):
    def test_js_action_loaded(self):
        """Test if the custom JavaScript action is loaded"""
        code = """
            return odoo.define.registry['real_estate_ads.CustomAction'] !== undefined;
        """
        result = self.browser_js(
            "/web", code, "real_estate_ads.CustomAction", timeout=60
        )
        self.assertTrue(result, "Custom JavaScript action should be loaded")

    def test_xml_template_loaded(self):
        """Test if the custom XML template is loaded"""
        code = """
            var ActionManager = odoo.__DEBUG__.services['web.ActionManager'];
            var action = new ActionManager();
            action.appendTo(document.createDocumentFragment()); // Create a detached DOM element
            var has_template = action.loadState({
                action: 'custom_client_action'
            }, {
                clear_breadcrumbs: true
            }).then(function() {
                return action.$el.find('div:contains("Custom Actions")').length > 0;
            });
            return has_template;
        """
        result = self.browser_js(
            "/web", code, "real_estate_ads.CustomAction_template", timeout=60
        )
        self.assertTrue(result, "Custom XML template should be loaded")
