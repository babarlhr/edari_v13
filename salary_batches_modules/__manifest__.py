# -*- coding: utf-8 -*-
{
    'name': "Salary Batches General",

    'summary': """
        General Module""",
    'author': "Erpify",
    'website': "https://odoo.ie",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
    'base',
    'hr_contract',
    'hr_payroll',
    ],

    # always loaded
    'data': [
        'views/salary_batches_view.xml',
    ],

}
