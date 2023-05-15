from odoo import models, fields, api

class NekabaCollege(models.Model):
    _name = "nekaba.college"
    name = fields.Char(string="الكلية")
    name_id = fields.Many2one("nekaba.university", string="الجامعة")
