# -*- coding: utf-8 -*-
{
    'name': "Partner Extension",

    'summary': """
        Erpify""",
    'author': "Erpify",
    'website': "https://odoo.ie",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','hr','account','sales_team'],

    # always loaded
    'data': [
        'views/partner_extension.xml',
    ],

}
