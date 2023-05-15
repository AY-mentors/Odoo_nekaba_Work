from odoo import models, fields, api

class NekabaUniversity(models.Model):
    _name = "nekaba.university"
    name = fields.Char(string="الجامعة")
    university_type = fields.Selection([("general", "حكومي"), ("private", "خاص")], default="general",string="نوع الجامعة")
