# -*- coding: utf-8 -*-
{
    'name': "Sale Order Extension",

    'summary': """
        Erpify""",
    'author': "Erpify",
    'website': "https://odoo.ie",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
    'base',
    'sale',
    'cost_card_template',
    ],

    # always loaded
    'data': [
        'views/so_ext_view.xml',
    ],

}
