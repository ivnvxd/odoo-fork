from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Properties Offers"

    @api.depends("validity", "creation_date")
    # @api.depends_context("uid")
    def _compute_deadline(self):
        # print("self.env.context", self.env.context)
        # print("self._context", self._context)
        for record in self:
            if record.creation_date and record.validity:
                record.deadline = record.creation_date + timedelta(days=record.validity)
            else:
                record.deadline = False

    def _inverse_deadline(self):
        for record in self:
            if record.creation_date and record.deadline:
                record.validity = (record.deadline - record.creation_date).days
            else:
                record.validity = False

    @api.autovacuum
    def _clean_offers(self):
        self.search([("status", "=", "refused")]).unlink()

    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    # @api.model_create_multi
    # def create(self, values):
    #     for rec in values:
    #         if not rec.get("creation_date"):
    #             rec["creation_date"] = fields.Date.today()
    #     return super(PropertyOffer, self).create(values)

    @api.constrains("validity")
    def _check_validity(self):
        for record in self:
            if record.deadline <= record.creation_date:
                raise ValidationError("Deadline must be greater than creation date")

    # _sql_constraints = [
    #     (
    #         "check_validity",
    #         "check(validity > 0)",
    #         "Deadline must be greater than creation date",
    #     )
    # ]

    price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status"
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    validity = fields.Integer(string="Validity (days)")
    # creation_date = fields.Date(string="Creation Date")
    creation_date = fields.Date(string="Creation Date", default=_set_create_date)
    deadline = fields.Date(
        string="Deadline", compute=_compute_deadline, inverse=_inverse_deadline
    )
