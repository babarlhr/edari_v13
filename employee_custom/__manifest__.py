# -*- coding: utf-8 -*-
{
    'name': 'Employee Custom',
    'version': '13.0.1',
    'description': 'Adding fields to employee model',
    'author': 'Odoo Advantage Ireland',
    'website': 'www.erp.odoo.ie',
    'depends': ['hr', 'hr_gamification', 'mail', 'base', 'account_asset'],
    'data': [
        "security/ir.model.access.csv",
        'views/employee_ext_view.xml',
        'wizard/excel_report_wizard.xml',
    ],
    'installable' : True,
}
