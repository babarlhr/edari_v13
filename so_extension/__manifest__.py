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
    'account',
    'cost_card_template',
    'snailmail_account',
    'mail',
    ],

    # always loaded
    'data': [
        'views/so_ext_view.xml',
        'views/acc_move_ext_view.xml',
        'views/invoice_send_and_print.xml',
    ],

}
