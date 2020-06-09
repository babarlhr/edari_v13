# -*- coding: utf-8 -*-
{
    'name': "Custom Holiday Module",

    'summary': """
        Erpify""",
    'author': "Erpify",
    'website': "https://odoo.ie",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
    'base',
    'hr',
    'hr_holidays',
    ],

    # always loaded
    'data': [
        'views/custom_holiday_view.xml',
        "security/ir.model.access.csv",
    ],

}
