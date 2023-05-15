from odoo import fields,models,api

class consultant(models.Model):
    _name = "nekaba.consultant"
    _order = "consultant_years desc"

    consultant_years = fields.Date(string="سنين الاشتراك")
    pay_state = fields.Boolean(string="حالة الدفع")
    consultant_id = fields.Many2one("res.partner")
