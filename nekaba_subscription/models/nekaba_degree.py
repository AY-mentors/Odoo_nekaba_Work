from odoo import models,fields,api
class Degree(models.Model):
    _name = "nekaba.degree"
    name = fields.Char(string="المؤهل")
