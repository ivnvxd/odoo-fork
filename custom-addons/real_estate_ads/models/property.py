from odoo import _, api, fields, models


class Property(models.Model):
    _name = "estate.property"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
        "utm.mixin",
        "website.published.mixin",
        "website.seo.metadata",
    ]
    _description = "Real Estate Properties"

    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="new",
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price", tracking=True)
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_price")
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
        default="north",
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    sales_id = fields.Many2one("res.users", string="Salesperson")
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", domain=[("is_company", "=", True)]
    )

    @api.onchange("living_area", "garden_area")
    def _onchange_total_area(self):
        self.total_area = self.living_area + self.garden_area

    total_area = fields.Integer(string="Total Area (sqm)")
    phone = fields.Char(string="Phone", related="buyer_id.phone")

    def action_sold(self):
        self.state = "sold"

    def action_cancel(self):
        self.state = "cancel"

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute=_compute_offer_count)

    def action_property_view_offers(self):
        return {
            "type": "ir.actions.act_window",
            "name": f"{self.name} - Offers",
            "domain": [("property_id", "=", self.id)],
            "view_mode": "tree,form",
            "res_model": "estate.property.offer",
        }

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0

    # def action_client_action(self):
    #     return {
    #         "type": "ir.actions.client",
    #         "tag": "display_notification",
    #         "params": {
    #             "title": _("Hello World"),
    #             type: "success",
    #             "sticky": True,
    #         },
    #     }

    # def action_url_action(self):
    #     return {
    #         "type": "ir.actions.act_url",
    #         "url": "https://www.odoo.com",
    #         "target": "new",
    #     }

    def _get_report_base_filename(self):
        self.ensure_one()
        return "Estate Property - %s" % (self.name)

    def _compute_website_url(self):
        for record in self:
            record.website_url = "/properties/%s" % record.id


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
