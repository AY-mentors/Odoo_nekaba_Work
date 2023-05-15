from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # @api.onchange('product_id')
    def onchange_product_id(self):
        # if self.product_id.fees == 'registration':
        #     if self.order_id.partner_id.university_id.university_type == "general":
        #         self.write({'price_unit': 1033})
        #     elif self.order_id.partner_id.university_id.university_type == "private":
        #         self.write({'price_unit': 2033})

        if self.product_id.fees == 'penalty':
            count = 0
            if self.order_id.partner_id.membership_ids:
                for line in self.order_id.partner_id.membership_ids:
                    if line.pay_state == False:
                        count = count+1
                if count >= 5 and count < 10:
                    self.write({'product_uom_qty': count})
                elif count < 5:
                    raise UserError("لا يوجد أي غرامات على العضو")
                elif count > 10:
                    self.order_id.partner_id.write({'block_state': 'blocked'})
                    raise UserError('لقد تم شطب العضو لانه تأخر عن دفع الاشتراك أكثر من 10 سنين')
        elif self.product_id.fees in ['Carney extraction', 'development', 'stamps', 'membership']:
            if self.order_id.partner_id.membership_ids:
                count = 1
                for line in self.order_id.partner_id.membership_ids:
                    if line.pay_state == False:
                        count = count + 1
                if count > 1 and count <= 10:
                    self.write({'product_uom_qty': count-1})

                elif count > 10:
                    raise UserError('لقد تم شطب العضو لانه تأخر عن دفع الاشتراك أكثر من 10 سنين')
                elif count < 1:
                    self.write({'product_uom_qty': count})
                # if count > 1:
                #     if self.order_id.partner_id.membership_ids:
                #         for line in self.order_id.partner_id.membership_ids:
                #              line.pay_state = True





    @api.model
    def create(self, values):
        values = super(SaleOrderLine, self).create(values)
        values.onchange_product_id()
        return values

    def write(self, vals):
        # if self.product_id.fees == 'registration':
        #
        #     if self.order_id.partner_id.university_id.university_type == "general":
        #         vals.update({'price_unit': 1033})
        #     elif self.order_id.partner_id.university_id.university_type == "private":
        #         vals.update({'price_unit': 2033})

        # New code to calculate date of years from graduate
        graduation_date = self.order_id.partner_id.graduation_date
        date_one = datetime.now().year
        date_one_1 = int(date_one)
        date_tow = str(graduation_date)
        date_tow_2 = int(date_tow[0:4])

        real_date = (date_one_1 - date_tow_2)

        if self.product_id.fees == 'penalty':
            count = 0
            if self.order_id.partner_id.membership_ids:
                for line in self.order_id.partner_id.membership_ids:
                    if line.pay_state == False:
                        count = count + 1
            if count >= 5:
                vals.update({'product_uom_qty': real_date})
            else:
                raise UserError("لا يوجد أي غرامات على العضو")
        if self.product_id.fees in ['Carney extraction', 'development', 'stamps', 'membership', 'care']:
            count = 1
            if self.order_id.partner_id.membership_ids:
                for line in self.order_id.partner_id.membership_ids:
                    if line.pay_state == False:
                        count = count + 1
            if count > 1:
                vals.update({'product_uom_qty': count - 1})
            else:
                vals.update({'product_uom_qty': count})

        vals = super(SaleOrderLine, self).write(vals)
        return vals






    # @api.onchange('product_uom_qty')
    # def onchange_product_uom_qty(self):
    #     if self.product_uom_qty > 1:
    #         if self.order_id.partner_id.membership_ids:
    #             for line in self.order_id.partner_id.membership_ids:
    #                 if line.pay_state == False:
    #                     self.order_id.partner_id.membership_ids.pay_state = True


    # @api.onchange('date_order')
    # def onchange_pay_check(self):
    #     if self.partner_id.membership_ids:
    #         for line in self.partner_id.membership_ids:
    #             if line.membership_years.year == self.date_order.year:
    #                 raise UserError("قام العضو بدفع رسوم هذه السنة")
