from odoo import models, fields, api

class MemberShipState(models.Model):
    _name = "nekaba.membership"
    _order = "membership_years desc"

    membership_years = fields.Date(string="سنين الاشتراك")
    pay_state = fields.Boolean(string="حالة الدفع")
    information_id = fields.Many2one("res.partner")













