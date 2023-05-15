# -*- coding: utf-8 -*-
import dateutil

from odoo import models, fields, api
from datetime import datetime
import datetime as datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(record.membership_num, record.member_id)))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search(['|', ('membership_num', operator, name), ('member_id', operator, name)] + args,
                               limit=limit)
        return recs.name_get()

    payment_count = fields.Integer(compute="_count_payment")
    membership_num = fields.Char(string="رقم العضوية")
    # general_university = fields.Selection([("helwan", "جامعة حلوان"), ("demitta", "جامعة دمياط"), ("bnisuif", "جامعة بني سويف"), ("banha", "جامعة بنها")],string="جامعات حكومية")
    # private_university = fields.Selection([("6october", "جامعة 6 اكتوبر"), ("badr","جامعة بدر"), ("msa", "جامعة اكتوبر للعلوم الحديثة والاداب طريق الواحات"),
    # ("aai", "المعهد العالي للفنون التطبيقية التجمع الخامس"), ("guc", "الجامعة الالمانية بالقاهرة "),
    # ("mao", "المعهد العالي للفنون التطبيقية بمدينة السادس من اكتوبر")], string="جامعات خاصة")

    # college = fields.Selection(
    #    [("helwan", "كلية الفنون التطبيقية جامعة حلوان"), ("demitta", "كلية الفنون التطبيقية جامعة دمياط"), ("bnisuif", "كلية الفنون التطبيقية جامعة بني سويف"), ("banha", "كلية الفنون التطبيقية جامعة بنها"),
    #     ("6october", "كلية الفنون التطبيقية جامعة 6 اكتوبر"), ("badr", "كلية الفنون التطبيقية جامعة بدر"), ("msa", "جامعة اكنوبر للعلوم الحدبثة والاداب طريق الواحات"),
    #     ("aai", "المعهد العالي للفنون التطبيقية التجمع الخامس"), ("guc", "كلية العلوم التطبيقية و الفنون بالجامعة الالمانية بالقاهرة "),
    #     ("mao", "المعهد العالي للفنون التطبيقية بمدينة السادس من اكتوبر")], string="الكلية")

    mobile2 = fields.Char(string="محمول اخر", size=11)
    carnet_date = fields.Date(default=fields.Date.today, string="تاريخ الاصدار", readonly=True)
    expiration_date = fields.Date(string="تاريخ الانتهاء", compute="calc_expiration_date")
    # logo = fields.Binary()
    university_id = fields.Many2one("nekaba.university", related="college_id.name_id")
    # college_id = fields.Many2one("nekaba.college", string="الكلية", default=1)
    # degree_id = fields.Many2one("nekaba.degree", string="المؤهل", default=1)
    # manufacture_design = fields.Text(string="المجال", required=False, readonly=True, default='تصميم صناعي')
    consultant = fields.Boolean(compute="calc_consultant_years", string="استشاري")
    # birth_date = fields.Date(required=True, string="تاريخ الميلاد")
    gender = fields.Selection([("m", "ذكر"), ("f", "أنثى")], string="النوع")
    member_id = fields.Char(required=True, string="الرقم القومي", size=14)
    birthdate = fields.Char(string='تاريخ الميلاد من الرقم القومي', compute="compute_birthdate")
    date_of_birth = fields.Date(string="تاريخ الميلاد", compute="convert_birthdate")
    # # New code to get end date
    # get_current_year = datetime.datetime.now().year
    # expiration_end_date = fields.Char(string='تاريخ الانتهاء', readonly=True, default="31/12/" + str(get_current_year)+"")
    property_account_receivable_id = fields.Many2one(required=False)
    property_account_payable_id = fields.Many2one(required=False)

    block_state = fields.Selection([("accepted", "مقبول"), ("blocked", "تم الحظر")], default="accepted",
                                   string="الموافقة")
    block_reason = fields.Selection(
        [("public", "أسباب عامة"), ("personal", "أسباب شخصية"), ("delay", "عدم تجديد الاشتراك لمدة 10 سنين")],
        string="سبب الحظر")
    block_reason2 = fields.Char(string="أسباب أخرى")
    graduation_date = fields.Date(string="تاريخ التخرج")
    department = fields.Many2one("hr.department", string="الشعبة", domain="[('parent_id', '=', False)]")
    department1 = fields.Many2one("hr.department", string="التخصص")
    practicing_profession_date = fields.Date(related='graduation_date', string="تاريخ مزاولة المهنة")
    # practicing_profession_date_inherit = fields.Date(compute='get_tow_date', string="تاريخ مزاولة المهنة")
    membership_ids = fields.One2many("nekaba.membership", "information_id")
    consultant_ids = fields.One2many("nekaba.consultant", "consultant_id")
    join_date = fields.Date(default=fields.Date.today, string="تاريخ القيد")
    nationality = fields.Selection([("egyptian", "مصري"), ("other", "جنسية أخري")], default="egyptian",
                                   string="الجنسية")
    country = fields.Many2one("res.country", string="البلد")
    age = fields.Integer(compute="calc_total_age", default=0)
    pension_state = fields.Boolean(compute="calc_pension_years", default=False, string="حالة المعاش")
    naqeeb_id = fields.Many2one('nekaba.naqeeb', string="النقيب")
    consultant_date = fields.Date(default=fields.Date.today, string="تاريخ قيد الاستشاري")
    no_years = fields.Integer(compute="calc_no_of_years", string="عدد سنين اشتراك العضو")
    press = fields.Boolean(default=False)
    press2 = fields.Boolean(default=False)
    press3 = fields.Boolean(default=False)

    def _count_payment(self):
        all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
        all_partners.read(['parent_id'])

        payment_groups = self.env['account.payment'].read_group(
            domain=[('partner_id', 'in', all_partners.ids)],
            fields=['partner_id'], groupby=['partner_id']
        )
        partners = self.browse()
        for group in payment_groups:
            partner = self.browse(group['partner_id'][0])
            while partner:
                if partner in self:
                    partner.payment_count += group['partner_id_count']
                    partners |= partner
                partner = partner.parent_id
        (self - partners).payment_count = 0

    def action_payment_button(self):
        return {

            'name': ('Payment'),  # This is form name, which you can edit according to you

            'view_mode': 'tree,form',  # Here we give view mode type

            'res_model': 'account.payment',  # Here we will provide model name for the form view

            'type': 'ir.actions.act_window',  # This is action which is predefined

            'domain': [('partner_id', '=', self.id)]
            # Here we are call required field, with the help of "self" which invokes a record rule

        }

    # @api.depends('birthdate_str')
    # def _birthdate_str(self):
    #     date_of_birth = datetime.strptime(str(self.birthdate_str), "%Y-%m-%d").date()
    #     self.birthdate_str = date_of_birth

    # @api.constrains('mobile')
    # def _check_mobile_unique(self):
    #     mobile_counts = self.search_count([('mobile', '=', self.mobile), ('id', '!=', self.id)])
    #     print(mobile_counts)
    #     if mobile_counts > 0:
    #         raise UserError("Mobile number already exists!")

    # @api.constrains('phone')
    # def _check_phone_unique(self):
    #     phone_counts = self.search_count([('phone', '=', self.phone), ('id', '!=', self.id)])
    #     print(phone_counts)
    #     if phone_counts > 0:
    #         raise UserError("phone number already exists!")

    @api.constrains('member_id')
    def _check_memberid_unique(self):
        member_id_counts = self.search_count([('member_id', '=', self.member_id), ('id', '!=', self.id)])
        print(member_id_counts)
        if member_id_counts > 0:
            raise UserError("ID number already exists!")

    # @api.constrains('membership_num')
    # def _check_membershipnum_unique(self):
    #     membership_num_counts = self.search_count([('membership_num', '=', self.membership_num), ('id', '!=', self.id)])
    #     print(membership_num_counts)
    #     if membership_num_counts > 0:
    #         raise UserError("membership number already exists!")

    @api.constrains('birth_date')
    def _check_birthdate_validation(self):
        if self.date_of_birth:
            today_date = datetime.date.today()
            lessvalid_date = today_date - relativedelta(years=20)
            mostvalid_date = today_date - relativedelta(years=40)
            if self.date_of_birth > lessvalid_date:
                raise UserError("عمر العضو يجب ان لا يقل عن 20 سنة")
            elif self.date_of_birth < mostvalid_date:
                raise UserError('عمر العضو يجب ان لا يزيد عن 40 سنة')

    @api.constrains('practicing_profession_date', 'graduation_date')
    def _check_dates_validation(self):
        if self.practicing_profession_date:
            today_date = datetime.date.today()
            if self.practicing_profession_date > today_date:
                raise UserError("تاريخ في المستقبل")
        if self.graduation_date:
            today_date = datetime.date.today()
            if self.graduation_date > today_date:
                raise UserError("تاريخ في المستقبل")

    @api.constrains('member_id')
    def _check_length_id(self):
        if len(self.member_id) != 14:
            raise UserError("الرقم القومي لا يقل عن 14 رقم")

    @api.constrains('mobile')
    def _check_length_mobile(self):
        if self.mobile:
            if len(self.mobile) != 11:
                raise UserError("رقم الموبايل لا يقل عن 11 رقم")

    @api.constrains('mobile2')
    def _check_length_mobile2(self):
        if self.mobile2:
            if len(self.mobile2) != 11:
                raise UserError("رقم الموبايل لا يقل عن 11 رقم")

    @api.depends('join_date')
    def create_lines(self):
        if self.join_date:
            today_date = datetime.date.today().year

            exact_years = today_date - self.join_date.year
            # if exact_years == 0:
            exact_years = exact_years + 1
            start_date = self.join_date - relativedelta(years=1)
            for line in range(exact_years):
                start_date += relativedelta(years=1)
                self.env['nekaba.membership'].sudo().create({'membership_years': start_date,
                                                             'information_id': self.id})

            self.press = True

    @api.depends('consultant')
    def create_lines_consultant(self):
        if self.consultant_date:
            today_date = datetime.date.today().year

            exact_years = today_date - self.consultant_date.year
            # if exact_years == 0:
            exact_years = exact_years + 1
            start_date = self.consultant_date - relativedelta(years=1)
            for line in range(exact_years):
                start_date += relativedelta(years=1)
                self.env['nekaba.consultant'].sudo().create({'consultant_years': start_date,
                                                             'consultant_id': self.id})

            self.press2 = True
        print(self.press2)

    @api.depends('join_date')
    def calc_no_of_years(self):
        if self.join_date:
            today_date = datetime.date.today().year
            no_years = today_date - self.join_date.year
            self.no_years = no_years

    @api.depends('date_of_birth')
    def calc_total_age(self):
        if self.date_of_birth:
            today_date = datetime.date.today().year
            total_age = today_date - self.date_of_birth.year
            self.age = total_age
        else:
            self.age = 0

    @api.depends('join_date')
    def calc_pension_years(self):
        if self.nationality == "egyptian":
            if self.age >= 60:
                if self.join_date:
                    today_date = datetime.date.today().year
                    join_years = today_date - self.join_date.year
                    if join_years >= 10:
                        self.pension_state = True
                    elif join_years < 10:
                        self.pension_state = False
            elif self.age < 60:
                self.pension_state = False
        else:
            self.pension_state = False

    @api.depends('join_date')
    def calc_consultant_years(self):
        if self.join_date:
            today_date = datetime.date.today().year
            join_years = today_date - self.join_date.year
            if join_years >= 20:
                self.consultant = True
            elif join_years < 20:
                self.consultant = False

    @api.depends('carnet_date')
    def calc_expiration_date(self):
        for rec in self:
            if rec.carnet_date:
                rec.expiration_date = rec.carnet_date + dateutil.relativedelta.relativedelta(
                    years=1)
            else:
                rec.expiration_date = False

                # department   الشعبة

    # department1  التخصص
    @api.onchange('department')
    def onchange_department1(self):
        domain = {'department1': [('parent_id', '=', self.department.name)]}
        return {'domain': domain}

    # @api.onchange('membership_ids')
    def onchange_delay_block(self):
        if self.membership_ids:
            count = 0
            for line in self.membership_ids:
                if line.pay_state == False:
                    count = count + 1
            if count > 10:
                self.write({'block_state': 'blocked'})
                self.write({'block_reason': 'delay'})
            else:
                pass

    # @api.model
    # def create(self, vals):
    #     new_member = super().create(vals)
    #     memberid_split = new_member.member_id.split()
    #     new_member.birthdate = f"{memberid_split[0][5]}{memberid_split[0][6]}/{memberid_split[0][3]}{memberid_split[0][4]}/{memberid_split[0][1]}{memberid_split[0][2]}"
    #     return new_member

    @api.depends('member_id')
    def compute_birthdate(self):
        for rec in self:
            if rec.member_id:
                memberid_split = rec.member_id.split()
                print(memberid_split[0][0])
                print(f"{memberid_split[0][5]}{memberid_split[0][6]}/{memberid_split[0][3]}{memberid_split[0][4]}/{memberid_split[0][1]}{memberid_split[0][2]}")
                if memberid_split[0][0] == '2':
                    rec.birthdate = f"{memberid_split[0][5]}{memberid_split[0][6]}/{memberid_split[0][3]}{memberid_split[0][4]}/19{memberid_split[0][1]}{memberid_split[0][2]}"
                elif memberid_split[0][0] == '3':
                    rec.birthdate = f"{memberid_split[0][5]}{memberid_split[0][6]}/{memberid_split[0][3]}{memberid_split[0][4]}/20{memberid_split[0][1]}{memberid_split[0][2]}"
                elif memberid_split[0][0] == '4':
                    rec.birthdate = f"{memberid_split[0][5]}{memberid_split[0][6]}/{memberid_split[0][3]}{memberid_split[0][4]}/21{memberid_split[0][1]}{memberid_split[0][2]}"
                else:
                    raise ValidationError("There's Error In Member ID")
                    # rec.birthdate = "There's Error In Member ID"
            else:
                rec.birthdate = '01/01/2023'

    @api.depends('member_id')
    def convert_birthdate(self):
        today_date = datetime.date.today().year
        for rec in self:
            if rec.birthdate:
                try:
                    rec.date_of_birth = datetime.datetime.strptime(str(rec.birthdate), '%d/%m/%Y').date()
                except ValueError:
                    raise ValidationError("There's Error In Member ID")
            else:
                rec.birthdate = today_date
    # @api.model
    # def create(self, values):
    #     values['membership_num'] = self.env['ir.sequence'].next_by_code('res.partner.seq')
    #     values = super(ResPartnerInherit, self).create(values)
    #     values.onchange_delay_block()
    #     return values

    def write(self, vals):
        if self.membership_ids:
            count = 0
            for line in self.membership_ids:
                if line.pay_state == False:
                    count = count + 1
            if count > 10:
                vals.update({'block_state': 'blocked'})
                vals.update({'block_reason': 'delay'})
            else:
                pass
        vals = super(ResPartnerInherit, self).write(vals)
        return vals

    @api.onchange('block_state')
    def onchange_block_state(self):
        if self.block_state == 'blocked':
            self.write({'sale_warn': 'block'})
        else:
            self.write({'sale_warn': 'no-message'})

    @api.onchange('pension_state')
    def onchange_pension_state(self):
        if self.pension_state:
            self.write({'sale_warn': 'warning'})
        else:
            self.write({'sale_warn': 'no-message'})

    # New code get default country
    def default_country(self):
        return self.env['res.country'].search([('name', '=', 'Egypt')], limit=1).id
    country_id = fields.Many2one(required=False, default=default_country)

    # New code get default collage
    def default_collage(self):
        return self.env['nekaba.college'].search([('name', '=', 'كلية فنون تطبيقية')], limit=1).id
    college_id = fields.Many2one("nekaba.college", string="الكلية", default=default_collage)

    # New code get default university
    def default_university(self):
        return self.env['nekaba.degree'].search([('name', '=', 'بكالوريوس فنون تطبيقية')], limit=1).id
    degree_id = fields.Many2one("nekaba.degree", string="المؤهل", default=default_university)

    # # New code get same date for practicing_profession_date_inherit field
    # @api.onchange('graduation_date')
    # def get_tow_date(self):
    #     self.practicing_profession_date = self.graduation_date

    # @api.model
    # def create(self, vals):
    #     vals['membership_num'] = self.env['ir.sequence'].next_by_code('res.partner.seq')
    #     return super(ResPartnerInherit, self).create(vals)


    # def check_pay(self):
    #     self.press3 = True
    #     partners = self.search([])
    #     for rec in partners:
    #         sales_orders = self.env['sale.order'].search(
    #             [('state', '=', 'sale'), ('partner_id', '=', rec._origin.id),
    #              ('years', '=', datetime.date.today().year)])
    #         print(sales_orders)
    #
    #         if sales_orders:
    #             for sale in sales_orders:
    #                 if sale.order_line:
    #                     services = []
    #                     for line in sale.order_line:
    #                         services.append(line.product_id.fees)
    #                     if 'Carney extraction' and 'development' and 'stamps' and 'membership' in services:
    #                         print("hi")
    #                         if line.product_uom_qty > 1:
    #                             if rec.membership_ids:
    #                                 years1 = []
    #                                 for year in rec.membership_ids:
    #                                     year.pay_state = True
    #                                     years1.append(year.membership_years.year)
    #                                 if sale.date_order.year not in years1:
    #                                     self.env['nekaba.membership'].sudo().create(
    #                                         {'membership_years': sale.date_order,
    #                                          'information_id': rec.id,
    #                                          'pay_state': True})
    #                             else:
    #                                 self.env['nekaba.membership'].sudo().create({'membership_years': sale.date_order,
    #                                                                              'information_id': rec.id,
    #                                                                              'pay_state': True})
    #                         elif line.product_uom_qty == 1:
    #                             if rec.membership_ids:
    #                                 years = []
    #                                 for year in rec.membership_ids:
    #                                     years.append(year.membership_years.year)
    #                                 if sale.date_order.year not in years:
    #                                     rec.env['nekaba.membership'].sudo().create(
    #                                         {'membership_years': sale.date_order,
    #                                          'information_id': rec.id,
    #                                          'pay_state': True})
    #                                     print(years)
    #                                 else:
    #                                     for year in rec.membership_ids:
    #                                         year.pay_state = True
    #                             else:
    #                                 self.env['nekaba.membership'].sudo().create({'membership_years': sale.date_order,
    #                                                                              'information_id': rec.id,
    #                                                                              'pay_state': True})

    # if sales.fees in ['Carney extraction', 'development', 'stamps', 'membership']:
    #     if self.membership_ids:
    #         count = 1
    #         for line in self.membership_ids:
    #             if line.pay_state == False:
    #                 count = count+1
    #         if count > 1:
    #             if self.order_id.partner_id.membership_ids:
    #                 for line in self.order_id.partner_id.membership_ids:
    #                     line.pay_state = True
