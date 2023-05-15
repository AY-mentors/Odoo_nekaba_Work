# -*- coding: utf-8 -*-
{
    'name': "nekaba_subscription",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'product', 'sale_management', 'hr'],

    # always loaded
    'data': [
        'reports/nekaba_card_report.xml',
        'reports/nekaba_card_templates.xml',
        'reports/consultant_card_report.xml',
        'reports/consultant_card_templates.xml',
        'reports/nekaba_counting_report.xml',
        'reports/nekaba_counting_templates.xml',
        'sequences/membership_num_sequence.xml',
        'security/ir.model.access.csv',
        'wizards/count_report_wizard_view.xml',
        'views/res_partner_views.xml',
        'views/product_product_view.xml',
        'views/nekaba_university_view.xml',
        'views/nekaba_college_view.xml',
        'views/nekaba_degree_view.xml',
        'views/nekaba_naqeeb_view.xml',
        'views/sale_order_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
