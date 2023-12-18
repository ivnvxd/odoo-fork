import logging
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


# class AbstractOffer(models.AbstractModel):
#     _name = "abstract.model.offer"
#     _description = "Abstract Model Offers"

#     partner_email = fields.Char(string="Partner Email")
#     partner_phone = fields.Char(string="Partner Phone")


# class TransientOffer(models.TransientModel):
#     _name = "transient.model.offer"
#     _description = "Transient Model Offers"
#     _transient_max_count = 5
#     _transient_max_hours = 2

#     @api.autovacuum
#     def _transient_vacuum(self):
#         pass

#     partner_email = fields.Char(string="Partner Email")
#     partner_phone = fields.Char(string="Partner Phone")


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    # _inherit = ["abstract.model.offer"]
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

    # def write(self, values):
    #     _logger.info("write: %s", values)
    #     # self.env["res.partner"].browse(1)
    #     res_partner_ids = self.env["res.partner"].search(
    #         [("is_company", "=", True)], limit=5, order="name desc"
    #     )
    #     _logger.info("res_partner_ids: %s", res_partner_ids)
    #     return super(PropertyOffer, self).write(values)

    @api.depends("property_id", "partner_id")
    def _compute_name(self):
        for record in self:
            if record.property_id and record.partner_id:
                record.name = f"{record.property_id.name} - {record.partner_id.name}"
            else:
                record.name = False

    name = fields.Char(string="Description", compute="_compute_name")
    price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status"
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")
    validity = fields.Integer(string="Validity (days)", default=7)
    # creation_date = fields.Date(string="Creation Date")
    creation_date = fields.Date(string="Creation Date", default=_set_create_date)
    deadline = fields.Date(
        string="Deadline", compute=_compute_deadline, inverse=_inverse_deadline
    )

    def action_accept_offer(self):
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.write({"selling_price": self.price, "state": "accepted"})
        self.status = "accepted"

    def _validate_accepted_offer(self):
        offer_ids = self.env["estate.property.offer"].search(
            [("property_id", "=", self.property_id.id), ("status", "=", "accepted")]
        )
        if offer_ids:
            raise ValidationError("You can only accept one offer")

    def action_decline_offer(self):
        self.status = "refused"
        if all(self.property_id.offer_ids.mapped("status")):
            self.property_id.write({"selling_price": 0, "state": "received"})
