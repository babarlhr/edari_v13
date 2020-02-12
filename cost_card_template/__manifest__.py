# -*- coding: utf-8 -*-
{
    'name': "Cost Card Template",

    'summary': """
        Erpify""",
    'author': "Erpify",
    'website': "https://odoo.ie",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
    'base',
    'product',
    'hr',
    'account',
    ],

    # always loaded
    'data': [
        'views/cost_card_template_view.xml',
    ],

}
