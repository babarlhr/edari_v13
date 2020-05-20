# -*- coding: utf-8 -*-
{
    'name': "HR Extension",

    'summary': """
        Erpify""",
    'author': "Erpify",
    'website': "https://odoo.ie",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','hr','hr_contract'],

    # always loaded
    'data': [
        'views/hr_employee.xml',
        'views/hr_contract.xml',
        'views/payroll.xml',
    ],

}
