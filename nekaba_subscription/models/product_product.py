from odoo import models, fields, api

class ProductProductInherit(models.Model):
    _inherit = "product.product"

    fees = fields.Selection([("Carney extraction", "استخراج الكارنيه"),
                             ("development", "التنمية"), ("stamps", "الدمغات"),
                             ("membership", "الاشتراك"), ("registration", "القيد"),
                             ("penalty","غرامة"),("care","رعاية صحية")], string="الرسوم")

