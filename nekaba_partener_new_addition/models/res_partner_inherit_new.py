import dateutil

from odoo import models, fields, api
from datetime import datetime
import datetime as datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    # New code to get end date
    get_current_year = datetime.datetime.now().year
    expiration_end_date = fields.Char(string='تاريخ الانتهاء', readonly=True, default="31/12/" + str(get_current_year) + "")

    manufacture_design = fields.Text(string="المجال", required=False, readonly=True, default='تصميم صناعي')

    property_account_receivable_id = fields.Many2one(required=False)
    property_account_payable_id = fields.Many2one(required=False)
    practicing_profession_date = fields.Date(string="تاريخ مزاولة المهنة")

    practicing_profession_date_inherit = fields.Date(compute='get_tow_date', string="تاريخ مزاولة المهنة")

    # New code get same date for practicing_profession_date_inherit field
    @api.onchange('graduation_date')
    def get_tow_date(self):
        self.practicing_profession_date_inherit = self.graduation_date
