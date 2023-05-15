from odoo import models, fields, api
import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        """ Implementation of additionnal mecanism of Sales Order confirmation.
            This method should be extended when the confirmation should generated
            other documents. In this method, the SO are in 'sale' state (not yet 'done').
        """
        # create an analytic account if at least an expense product
        for order in self:
            if any(expense_policy not in [False, 'no'] for expense_policy in
                   order.order_line.mapped('product_id.expense_policy')):
                if not order.analytic_account_id:
                    order._create_analytic_account()

        return True

    def _prepare_confirmation_values(self):
        return {
            'state': 'sale',
            'date_order': fields.Datetime.now()
        }

    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        for sale in self:
            if self.state == 'sale':
                if sale.order_line:
                    services = []
                    for line in sale.order_line:
                        services.append(line.product_id.fees)
                    if 'Carney extraction' in services:
                        if self.partner_id.age > 40:
                            raise ValidationError("لا يسمح بالاشتراك لمن تجاوز عمرة 40 عام ")
                        elif self.partner_id.num_of_graduation_years > 5:
                            raise ValidationError("لا يسمح بالاشتراك لمن مره علي تخرجة 5 اعوام  ")
                        else:
                            if 'Carney extraction' and 'development' and 'stamps' and 'membership' in services:
                                print("hi")
                                if line.product_uom_qty > 1:
                                    if self.partner_id.membership_ids:
                                        years1 = []
                                        for year in self.partner_id.membership_ids:
                                            year.pay_state = True
                                            years1.append(year.membership_years.year)
                                            if sale.date_order.year not in years1:
                                                self.env['nekaba.membership'].sudo().create(
                                                    {'membership_years': sale.date_order,
                                                     'information_id': self.partner_id.id,
                                                     'pay_state': True})
                                    else:
                                        self.env['nekaba.membership'].sudo().create(
                                            {'membership_years': sale.date_order,
                                             'information_id': self.partner_id.id,
                                             'pay_state': True})
                                elif line.product_uom_qty == 1:
                                    if self.partner_id.membership_ids:
                                        years = []
                                        for year in self.partner_id.membership_ids:
                                            years.append(year.membership_years.year)
                                        if sale.date_order.year not in years:
                                            self.env['nekaba.membership'].sudo().create(
                                                {'membership_years': sale.date_order,
                                                 'information_id': self.partner_id.id,
                                                 'pay_state': True})
                                            print(years)
                                        else:
                                            for year in self.partner_id.membership_ids:
                                                year.pay_state = True
                                    else:
                                        self.env['nekaba.membership'].sudo().create(
                                            {'membership_years': sale.date_order,
                                             'information_id': self.partner_id.id,
                                             'pay_state': True})

            else:
                pass

        return True

    def _get_forbidden_state_confirm(self):
        return {'done', 'cancel'}

    def _prepare_analytic_account_data(self, prefix=None):
        """
        Prepare method for analytic account data

        :param prefix: The prefix of the to-be-created analytic account name
        :type prefix: string
        :return: dictionary of value for new analytic account creation
        """
        name = self.name
        if prefix:
            name = prefix + ": " + self.name
        return {
            'name': name,
            'code': self.client_order_ref,
            'company_id': self.company_id.id,
            'partner_id': self.partner_id.id
        }
