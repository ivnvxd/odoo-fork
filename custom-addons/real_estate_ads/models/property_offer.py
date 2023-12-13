from datetime import timedelta

from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Properties Offers"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status"
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    validity = fields.Integer(string="Validity (days)")
    creation_date = fields.Date(string="Creation Date")

    @api.depends("validity", "creation_date")
    def _compute_deadline(self):
        for record in self:
            if record.creation_date and record.validity:
                record.deadline = record.creation_date + timedelta(days=record.validity)
            else:
                record.deadline = False

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - record.creation_date).days

    deadline = fields.Date(
        string="Deadline", compute=_compute_deadline, inverse=_inverse_deadline
    )
