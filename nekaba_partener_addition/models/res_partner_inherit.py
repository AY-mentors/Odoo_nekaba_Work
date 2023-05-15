import dateutil

from odoo import models, fields, api
from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    # practicing_profession_date_inherit = fields.Date(related='join_date', string="تاريخ مزاولة المهنة")
    practicing_profession_date_inherit = fields.Date(string="تاريخ مزاولة المهنة")
    num_of_graduation_years = fields.Integer(compute="calc_no_of_grad_years", string="عدد سنين منذ تخرج العضو")
    age = fields.Integer(compute="calc_age", string="العمر")

    @api.depends('graduation_date')
    def calc_no_of_grad_years(self):
        for rec in self:
            if rec.graduation_date:
                today_date = datetime.date.today().year
                no_years = today_date - rec.graduation_date.year
                rec.num_of_graduation_years = no_years
            else:
                rec.num_of_graduation_years = 0

    @api.depends('date_of_birth')
    def calc_age(self):
        for rec in self:
            if rec.date_of_birth:
                today_date = datetime.date.today().year
                no_years = today_date - rec.date_of_birth.year
                rec.age = no_years
            else:
                rec.age = 0


    @api.model
    def create(self, vals):
        vals['membership_num'] = self.env['ir.sequence'].next_by_code('res.partner.seq')
        return super(ResPartner, self).create(vals)

