from odoo import models, fields, api, _


class CountReportWizard(models.TransientModel):
    _name = 'count.report.wizard'

    start_date = fields.Date(string="من تاريخ")
    end_date = fields.Date(string="الى تاريخ")
    department_ids = fields.Many2many('hr.department', string="التخصص")
    university_ids = fields.Many2many('nekaba.university', string="الجامعة")
    state_ids = fields.Many2many('res.country.state', string="المحافظة")

    def check_report(self):
        res = []
        data = {}
        data['form'] = self.read(['department_ids', 'university_ids', 'state_ids', 'start_date', 'end_date'])[0]
        res.append(data)
        return self.print_count_report_wizard1(data)

    def print_count_report_wizard1(self, data):
        domain = []
        if self.start_date:
            domain.append(('join_date', '>', self.start_date))
        if self.end_date:
            domain.append(('join_date', '<', self.end_date))
        if self.department_ids:
            domain.append(('department1', 'in', self.department_ids.ids))
        if self.university_ids:
            domain.append(('university_id', 'in', self.university_ids.ids))
        if self.state_ids:
            domain.append(('state_id', 'in', self.state_ids.ids))
        partners = self.env['res.partner'].search(domain)
        departments = []
        universitys = []
        states = []
        dep_dict = {}
        univ_dict = {}
        state_dict = {}
        for dep in self.department_ids:
            dep_dict[dep.name] = 0
            for partner in partners:
                if dep.id == partner.department1.id:
                    dep_dict[dep.name] += 1

            departments.append(dep.name)
        for univ in self.university_ids:
            univ_dict[univ.name] = 0
            for partner in partners:
                if univ.id == partner.university_id.id:
                    univ_dict[univ.name] += 1
            universitys.append(univ.name)
        for state in self.state_ids:
            state_dict[state.name] = 0
            for partner in partners:
                if state.id == partner.state_id.id:
                    state_dict[state.name] += 1
            states.append(state)

            # partner_dict = {}
            # for partner in partners:
        data['form'].update({'departments': departments,
                             'university_ids': universitys,
                             'state_ids': states,
                             'start_date': self.start_date or False,
                             'end_date': self.end_date or False,
                             'partners': partners.ids,
                             'dep_dict': dep_dict,
                             'univ_dict': univ_dict,
                             'state_dict': state_dict})

        return self.env.ref('nekaba_subscription.nekaba_counting_report').report_action(self, data=data, config=False)


class ReportCounting(models.AbstractModel):
    _name = 'report.nekaba_subscription.nekaba_counting_template'

    # def get_lines(self, employeeName, date_from, date_to):
    #     data = {}
    #     res = []
    #     if date_from <= date_to:
    #         totalAttendance = self.env['hr.attendance'].search(['&', '&', ('employee_id', '=', employeeName),
    #                                                             ('check_in', '>=', date_from), '|',
    #                                                             ('check_out', '<=', date_to),
    #                                                             ('check_out', '=', False)])
    #     else:
    #         raise UserError("Invalid Date")
    #
    #     print(totalAttendance)
    #     return totalAttendance
    #
    @api.model
    def _get_report_values(self, set, data=None):
        departments = data['form']['departments']
        partners1 = data['form']['partners']
        partners = self.env['res.partner'].browse(partners1)
        universitys = data['form']['university_ids']
        states = data['form']['state_ids']
        start_date = data['form']['start_date']
        end_date = data['form']['end_date']
        dep_dict = data['form']['dep_dict']
        univ_dict = data['form']['univ_dict']
        state_dict = data['form']['state_dict']
        set = {
            'doc_model': 'res.partner',
            'departments': departments,
            'universitys': universitys,
            'states': states,
            'start_date': start_date,
            'end_date': end_date,
            'partners': partners,
            'dep_dict': dep_dict,
            'univ_dict': univ_dict,
            'state_dict': state_dict
        }
        return set
