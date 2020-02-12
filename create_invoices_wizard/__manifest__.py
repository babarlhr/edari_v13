# -*- coding: utf-8 -*-
{
    'name': "Create Invoice Wizard",

    'summary': """
        Erpify""",
    'author': "Erpify",
    'website': "https://odoo.ie",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'views/wizard_view.xml',
    ],

}
