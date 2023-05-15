from odoo import fields, models, api


class SalesAddition(models.Model):
    _inherit = 'sale.order'

    # partner_id = fields.Many2one(
    #     'res.partner', string='العضو', readonly=True,
    #     states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
    #     required=False, change_default=True, index=True, tracking=1,
    #     domain="[('type', '!=', 'private'), ('company_id', 'in', (False, company_id))]", )

    # partner_id = fields.Many2one('res.partner', string='العضو', required=False)

    graduation_date = fields.Date(string="تاريخ التخرج", related='partner_id.graduation_date')
    join_date = fields.Date(string="تاريخ القيد", related='partner_id.join_date')
    member_id = fields.Char(string='اسم العضو', related='partner_id.name', readonly=False)



